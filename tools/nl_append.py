"""Append whole new acts (verified corpus.d parts) to the published netherlands-law main, append-only.

    python -X utf8 nl_append.py --src <country folder> --repo <clone> --docs-date YYYY-MM-DD --parts a.json b.json
                                [--dry-run]

The same commits tools/append.py makes for an act main does not hold yet (tools/build.py plan, start_message,
change_message, act_files; author date noon local on the in-force day; committer Lexifina, one second per commit
after the published head; tags <act>/<day> and law/<key> that do not exist yet), but it reads only the parts it
appends: an act whose folder main already has is left out (never extended or rewritten here). Each part must carry
its <part>.PUBLISH marker matching its bytes. The documentation commit then extends data/commits.csv, data/laws.csv,
data/versions.json, data/parts.json and tools/acts.json with the new rows, adds each new act's README.md, and leaves
every other file as published.
"""
import argparse
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def git(repo, *args, inp=None):
    r = subprocess.run(['git', *args], cwd=repo, capture_output=True, input=inp, encoding='utf-8')
    if r.returncode:
        raise SystemExit(f'git {" ".join(args[:3])}: {r.stderr.strip()}')
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--repo', required=True)
    ap.add_argument('--docs-date', required=True)
    ap.add_argument('--parts', nargs='+', required=True)
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    src, repo = Path(a.src).resolve(), Path(a.repo).resolve()
    sys.path.insert(0, str(repo / 'tools'))
    import build as B
    import append as A
    import check_repo as K
    import publish_marker

    # A scratch country folder: corpus.json = the country block only (no acts), corpus.d = the parts to append.
    tmp = Path(tempfile.mkdtemp(prefix='nl-append-', dir=str(src.parent / 'state')))
    try:
        base = json.loads((src / 'corpus.json').read_text(encoding='utf-8'))
        (tmp / 'corpus.json').write_text(json.dumps({'country': base['country'], 'laws': {}, 'acts': []},
                                                    ensure_ascii=False), encoding='utf-8', newline='\n')
        (tmp / 'corpus.d').mkdir()
        names = []
        for name in a.parts:
            name = name if name.endswith('.json') else name + '.json'
            p = src / 'corpus.d' / name
            state, detail = publish_marker.status(p)
            if state not in ('legacy', 'match'):
                raise SystemExit(f'{name}: not verified ({state}: {detail})')
            for suffix in ('', ''):
                pass
            os.link(p, tmp / 'corpus.d' / name)
            os.link(p.with_suffix('.PUBLISH'), tmp / 'corpus.d' / p.with_suffix('.PUBLISH').name)
            names.append(name)
        part_records = {}
        c, raw = B.load(tmp, part_records=part_records)
        errs = B.validate(c)
        if errs:
            raise SystemExit('corpus has problems:\n  ' + '\n  '.join(errs[:40]))
        c['_docs_date'] = a.docs_date
    finally:
        pass

    if git(repo, 'status', '--porcelain', '--untracked-files=no').strip():
        raise SystemExit('clone has uncommitted changes')
    head = git(repo, 'rev-parse', 'main').strip()
    origin = git(repo, 'rev-parse', 'origin/main').strip()
    if origin != head:
        raise SystemExit(f'main {head[:12]} != origin/main {origin[:12]}')
    head_ct, head_tz = git(repo, 'log', '-1', '--format=%ct %ci', 'main').split()[0::3]
    on_main = set(git(repo, 'ls-tree', '--name-only', 'main').split('\n'))
    skipped = [x['slug'] for x in c['acts'] if x['slug'] in on_main]
    sub = dict(c)
    sub['acts'] = [{**x, 'versions': [v for v in x['versions'] if v['from'] <= a.docs_date]} for x in c['acts']
                   if x['slug'] not in on_main]
    sub['acts'] = [x for x in sub['acts'] if x['versions']]
    commits = B.plan(sub) if sub['acts'] else []
    co = c['country']
    committer = ('Lexifina', f'{co["slug"]}-law@lexifina.com')
    clock = B.Clock(co['tz'])
    planned = []
    for x in commits:
        if x['kind'] == 'start':
            author, msg, trailers = B.start_message(c, x)
            files = B.act_files(x['act'], x['version']['units'], None)
            touched = [x['act']['slug']]
        else:
            author, msg, trailers = B.change_message(c, x)
            files = {}
            for p in x['parts']:
                files.update(B.act_files(p['act'], p['cur']['units'], p['prev']['units'], p['keys']))
            touched = [p['act']['slug'] for p in x['parts']]
        B.check_trailers(trailers)
        if not (author[1].endswith('.invalid') or author[1].endswith('@lexifina.com')):
            raise SystemExit(f'author e-mail {author[1]!r} is not .invalid or @lexifina.com')
        planned.append({'x': x, 'author': author, 'files': files, 'touched': touched,
                        'text': '\n'.join(msg).rstrip('\n') + '\n\n' + '\n'.join(trailers) + '\n'})
    summary = {'head': head[:12], 'parts': names, 'new_acts': len(sub['acts']), 'skipped_on_main': len(skipped),
               'commits': len(planned)}
    if a.dry_run or not planned:
        print(json.dumps(summary, ensure_ascii=False))
        shutil.rmtree(tmp, ignore_errors=True)
        return
    existing_tags = set(git(repo, 'tag', '--list').split())
    w = A.Appender(repo, head, int(head_ct), head_tz)
    tags, log = {}, []
    for e in planned:
        x = e['x']
        mark = w.commit(e['author'], clock.stamp(x['day']), committer, e['text'], e['files'])
        for s in e['touched']:
            tags.setdefault(f'{s}/{x["day"]}', mark)
        if x['kind'] == 'law':
            tags.setdefault(f'law/{x["law"]}', mark)
        elif x['kind'] == 'start' and x['act'].get('first_law'):
            tags.setdefault(f'law/{x["act"]["first_law"]}', mark)
        log.append({'day': x['day'], 'kind': x['kind'],
                    'law': x.get('law') or (x['act'].get('first_law') if x['kind'] == 'start' else None),
                    'acts': e['touched'], 'units': len(e['files']), 'branch': 'main'})

    # Documentation: extend the published tables with the new rows; everything else stays as published.
    t = B.tables(sub, log)
    docs = {k: v for k, v in t.items() if k.endswith('/README.md') and not k.startswith('data/')}
    commits_csv = git(repo, 'show', 'main:data/commits.csv')
    new_rows = t['data/commits.csv'].split('\n', 1)[1]
    docs['data/commits.csv'] = commits_csv + new_rows
    laws_text = git(repo, 'show', 'main:data/laws.csv')
    rows = list(csv.reader(io.StringIO(laws_text)))
    header, body = rows[0], rows[1:]
    index = {r[0]: i for i, r in enumerate(body)}
    for r in list(csv.reader(io.StringIO(t['data/laws.csv'])))[1:]:
        if r[0] in index:
            old = body[index[r[0]]]
            ds = sorted(set(old[6].split()) | set(r[6].split()))
            old[6] = ' '.join(ds)
            old[7] = str(int(old[7] or 0) + int(r[7] or 0))
        else:
            index[r[0]] = len(body)
            body.append(r)
    buf = io.StringIO()
    wr = csv.writer(buf, lineterminator='\n')
    wr.writerow(header)
    wr.writerows(body)
    docs['data/laws.csv'] = buf.getvalue()
    vj = json.loads(git(repo, 'show', 'main:data/versions.json'))
    vj['acts'].extend(json.loads(t['data/versions.json'])['acts'])
    docs['data/versions.json'] = json.dumps(vj, ensure_ascii=False, indent=1) + '\n'
    pj = json.loads(git(repo, 'show', 'main:data/parts.json'))
    for name, rec in part_records.items():
        rec = {**rec, 'acts': sorted(set(rec['acts']) - set(skipped))}
        pj['parts'][name] = rec
    docs['data/parts.json'] = json.dumps(pj, ensure_ascii=False, sort_keys=True, indent=1) + '\n'
    aj = json.loads(git(repo, 'show', 'main:tools/acts.json'))
    src_acts = json.loads((src / 'acts.json').read_text(encoding='utf-8'))
    for x in sub['acts']:
        if x['slug'] in src_acts and x['slug'] not in aj:
            aj[x['slug']] = src_acts[x['slug']]
    docs['tools/acts.json'] = json.dumps(aj, ensure_ascii=False, indent=1) + '\n'
    docs['tools/nl_append.py'] = Path(__file__).read_text(encoding='utf-8').replace('\r\n', '\n')
    jur = json.loads(git(repo, 'show', 'main:jurisdiction.json'))
    n_acts = len(vj['acts'])
    n_versions = sum(len(x['versions']) for x in vj['acts'])
    import re
    m = re.search(r'\((\d[\d,]*) with history from their oldest BWB version, (\d[\d,]*) with their current text only\)',
                  jur.get('build', ''))
    hist = int(m.group(1).replace(',', '')) if m else 0
    first = min(v['from'] for x in vj['acts'] for v in x['versions'])[:4]
    last = max(v['from'] for x in vj['acts'] for v in x['versions'] if v['from'] <= a.docs_date)[:4]
    jur['build'] = (f'built: {n_acts} regulations from the Basiswettenbestand (BWB), {n_versions:,} versions, '
                    f'{first}-{last} ({hist:,} with history from their oldest BWB version, {n_acts - hist:,} with '
                    f'their current text only); see README.md for the list')
    docs['jurisdiction.json'] = json.dumps(jur, ensure_ascii=False, indent=2) + '\n'
    ts, tz = clock.stamp(a.docs_date).split()
    w.commit(committer, f'{min(int(ts), int(time.time()))} {tz}', committer,
             f'Documentation: tables and tools for {len(sub["acts"])} appended acts\n\n'
             f'Appended {len(log)} commits to {head[:12]}: the acts of the verified parts {", ".join(n[:-5] for n in names)} '
             f'(each checked word for word against its own BWB toestand XML; see data/parts.json). data/commits.csv, '
             f'data/laws.csv, data/versions.json, data/parts.json, tools/acts.json and jurisdiction.json are extended '
             f'with their rows; tools/nl_append.py made these commits. Data retrieved {a.docs_date}.\n', docs)
    for name, mark in sorted(tags.items()):
        if name not in existing_tags:
            w.tag(name, mark)
    w.finish()
    new_head = git(repo, 'rev-parse', 'main').strip()
    if subprocess.run(['git', 'merge-base', '--is-ancestor', head, new_head], cwd=repo).returncode:
        raise SystemExit('internal: published head not an ancestor')
    # Check: at the new tip each appended act's files equal its corpus version in force on the docs date.
    bad = 0
    tree = {}
    for line in git(repo, 'ls-tree', '-r', new_head, '--', *[x['slug'] for x in sub['acts']]).splitlines():
        meta, path = line.split('\t', 1)
        tree[path] = meta.split()[2]
    for x in sub['acts']:
        v = A.corpus_on(x['versions'], a.docs_date)
        want = {f'{x["slug"]}/{k}.md': K.blob_oid(u['text']) for k, u in (v['units'] if v else {}).items()}
        have = {p: o for p, o in tree.items() if p.startswith(x['slug'] + '/') and not p.endswith('/README.md')}
        if have != want:
            bad += 1
            if bad < 5:
                print('MISMATCH', x['slug'], len(have), len(want), file=sys.stderr)
    new_tags = sorted(n for n in tags if n not in existing_tags)
    (src.parent / 'state' / 'new_tags.txt').write_text('\n'.join(new_tags) + '\n', encoding='utf-8')
    summary.update({'main': new_head[:12], 'tags_added': len(new_tags), 'tip_mismatches': bad})
    print(json.dumps(summary, ensure_ascii=False))
    shutil.rmtree(tmp, ignore_errors=True)
    if bad:
        raise SystemExit('tip mismatches: not pushing')


if __name__ == '__main__':
    main()
