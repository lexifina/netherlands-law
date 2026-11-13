"""Publish every CVDR regulation (local legislation) on netherlands-law main, authority by authority, append-only.

    python -X utf8 cvdr_run.py run [--threads 6] [--batch 400] [--only <authority slug>...] [--max-batches N]
    python -X utf8 cvdr_run.py status

Reads state/cvdr-index.json.gz (cvdr_index.py). For each batch of regulations of one authority: fetches every
version's XML from repository.officiele-overheidspublicaties.nl (in memory only; sha256 kept), reads it
(cvdr_parse.read) and checks it word for word against the XML (cvdr_parse.verify); a regulation any of whose
versions fails is held (state/cvdr-held.jsonl), never published. Then the commits are made with the repository's
own builder (tools/build.py plan / start_message / change_message, author date noon on the in-force day, committer
Lexifina), one documentation commit (each regulation's README.md, local/<authority>/README.md, local/README.md and
data/local/<authority>.csv), the tip is checked against the versions in force on the docs date, and main is
pushed. Resumable: published regulations are listed in state/cvdr-published.jsonl. Stops on a block (HTTP 403/429
from the source: state/BLOCKED), on state/CVDR-STOP, or when C: has less than 10 GB free.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STATE = ROOT / 'state'
REPO = ROOT / 'repo-local'
LOG = ROOT / 'logs' / 'cvdr-run.log'
PUBLISHED = STATE / 'cvdr-published.jsonl'
HELD = STATE / 'cvdr-held.jsonl'
LOCK = STATE / 'push.lock'
STOP = STATE / 'CVDR-STOP'
BLOCKED = STATE / 'BLOCKED'
UA = 'lexifina-law-archive/1.0 (+https://github.com/lexifina/netherlands-law)'
TYPE_ORDER = ['Provincie', 'Waterschap', 'Gemeente', 'RegionaalSamenwerkingsorgaan', 'Deelgemeente',
              'CaribischOpenbaarLichaam', 'Koninkrijksdeel', 'NederlandseAntillen']
CVDR_PUBLISHER = {'name': 'KOOP, lokaleregelgeving.overheid.nl (CVDR)', 'email': 'cvdr@lokaleregelgeving-overheid.invalid'}
TYPE_NAME = {'Gemeente': 'gemeente', 'Provincie': 'provincie', 'Waterschap': 'waterschap',
             'RegionaalSamenwerkingsorgaan': 'gemeenschappelijke regeling / regionaal samenwerkingsorgaan',
             'Deelgemeente': 'deelgemeente', 'Koninkrijksdeel': 'land in het Koninkrijk',
             'NederlandseAntillen': 'Nederlandse Antillen', 'CaribischOpenbaarLichaam': 'openbaar lichaam (Caribisch Nederland)'}

sys.path.insert(0, str(HERE))
import cvdr_parse as C  # noqa: E402

_log_lock = threading.Lock()


def log(msg: str) -> None:
    line = f'{time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())} {msg}'
    with _log_lock:
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    print(line, flush=True)


def git(*args, inp=None, check=True) -> str:
    r = subprocess.run(['git', *args], cwd=REPO, capture_output=True, encoding='utf-8', input=inp)
    if check and r.returncode:
        raise RuntimeError(f'git {" ".join(args[:3])}: {r.stderr.strip()[:500]}')
    return r.stdout


class Blocked(Exception):
    pass


class Fetcher:
    def __init__(self, threads: int):
        self.threads = threads
        self.n = 0
        self.errors = 0
        self.lock = threading.Lock()
        self.pause_until = 0.0

    def get(self, url: str) -> bytes:
        delay = 3
        for attempt in range(6):
            wait = self.pause_until - time.time()
            if wait > 0:
                time.sleep(wait)
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=90) as r:
                    b = r.read()
                with self.lock:
                    self.n += 1
                return b
            except urllib.error.HTTPError as e:
                if e.code in (403, 429):
                    ra = e.headers.get('Retry-After')
                    if e.code == 429 and ra and ra.isdigit() and int(ra) <= 300 and attempt < 3:
                        self.pause_until = time.time() + int(ra)
                        continue
                    raise Blocked(f'HTTP {e.code} on {url}')
                if e.code == 404:
                    raise
                with self.lock:
                    self.errors += 1
            except Exception:
                with self.lock:
                    self.errors += 1
                if attempt == 5:
                    raise
            time.sleep(delay)
            delay *= 2
        raise RuntimeError(f'failed: {url}')


def law_key(auth: str, pub: str) -> str:
    h = hashlib.sha1(pub.encode('utf-8')).hexdigest()[:6]
    s = re.sub(r'[^a-z0-9]+', '-', C.P.norm(pub).lower().encode('ascii', 'ignore').decode()).strip('-')[:30].strip('-')
    return f'{auth[:24].strip("-")}-{s}-{h}' if s else f'{auth[:24].strip("-")}-{h}'


NO_PUB = re.compile(r'^\s*(onbekend|unknown|n\.?v\.?t\.?|geen|-+|\.)?\s*\.?\s*$', re.I)


def build_work(w: dict, raws: dict, docs_date: str, laws: dict) -> tuple[dict | None, str]:
    """The corpus act for one regulation, or None and the reason it is held."""
    exprs = [e for e in w['exprs']]
    if any(not e['from'] for e in exprs):
        return None, 'a version has no in-force date'
    exprs.sort(key=lambda e: (e['from'], e['n']))
    versions = []
    first_law = None
    for i, e in enumerate(exprs):
        raw = raws[e['n']]
        units = C.read(raw)
        missing, extra, detail = C.verify(raw, units)
        if missing or extra:
            return None, f'version {e["n"]}: text check failed ({missing} words missing, {extra} extra: {detail})'
        if not units:
            return None, f'version {e["n"]}: no text'
        bad = [k for k in units if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', k) or k == 'readme']
        if bad:
            return None, f'version {e["n"]}: unit keys {bad[:3]}'
        key = None
        if e['pub'] and not NO_PUB.match(e['pub']):
            key = law_key(w['auth'], e['pub'])
            label = f'{C.P.norm(e["pub"])} ({w["name"]})'
            if key in laws and laws[key]['label'] != label:
                return None, f'law key clash {key}'
            laws.setdefault(key, {'label': label, 'kind': 'decree', 'title': None,
                                  'enacted': e['issued'] if re.fullmatch(r'\d{4}-\d\d-\d\d', e['issued'] or '') else None,
                                  'published': None, 'url': None, 'temporary_until': None, 'restores': None,
                                  'note': None})
        v = {'from': e['from'], 'source_url': e['url'], 'sha256': hashlib.sha256(raw).hexdigest(), 'units': units}
        if versions and versions[-1]['from'] == e['from']:
            v['same_day'] = True
        if versions:
            prev = versions[-1]['units']
            changed = [k for k in set(prev) | set(units) if prev.get(k, {}).get('text') != units.get(k, {}).get('text')]
            v['credits'] = {k: [key] for k in sorted(changed)} if key else {}
            if e['betreft']:
                v['note'] = f'CVDR: {C.P.norm(e["betreft"])} (version {e["n"]} of {w["id"]}).'
        else:
            v['credits'] = {}
            if key and re.match(r'\s*nieuw', e['betreft'] or '', re.I):
                first_law = key
            elif e['betreft']:
                v['note'] = f'CVDR: {C.P.norm(e["betreft"])} (version {e["n"]} of {w["id"]}).'
        versions.append(v)
    last = exprs[-1]
    if last['until'] and last['until'] > versions[-1]['from']:
        versions.append({'from': last['until'], 'source_url': last['page'] or w['work_url'], 'units': {}, 'credits': {},
                         'note': f'No longer in force: CVDR gives {last["until"]} as the day this regulation ceased to '
                                 'apply (uitwerkingtredingDatum of its last version) and names no withdrawing '
                                 'publication, so this commit is not credited to one.'})
    versions = [v for v in versions if v['from'] <= docs_date]
    if not versions:
        return None, 'not yet in force'
    if versions[0].get('same_day'):
        versions[0].pop('same_day')
    title = C.P.norm(w['title'])
    return {'slug': w['path'], 'short': title, 'title': title, 'url': w['work_url'], 'first_law': first_law,
            'earlier_laws': [], 'publisher': CVDR_PUBLISHER, 'versions': versions,
            '_cvdr': {'id': w['id'], 'auth': w['auth'], 'name': w['name'], 'type': w['type'],
                      'status': 'expired' if versions[-1]['units'] == {} else 'in force',
                      'first': versions[0]['from'], 'n': len([v for v in versions if v['units']])}}, ''


def disk_free_gb() -> float:
    return shutil.disk_usage('C:\\').free / 2**30


def acquire_lock():
    while True:
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return
        except FileExistsError:
            time.sleep(15)


def release_lock():
    try:
        LOCK.unlink()
    except FileNotFoundError:
        pass


def sync_main():
    git('fetch', '-q', '--depth=1', 'origin', 'main')
    git('update-ref', 'refs/heads/main', git('rev-parse', 'origin/main').strip())


def authority_docs(auth: str, regs: list[dict]) -> dict[str, str]:
    regs = sorted(regs, key=lambda r: (r['first'], int(r['id'][4:])))
    name, typ = regs[0]['name'], regs[0]['type']
    live = sum(1 for r in regs if r['status'] == 'in force')
    rows = [f'# {name} ({TYPE_NAME.get(typ, typ)})', '',
            f'Local regulations of {name} from the Centrale Voorziening Decentrale Regelgeving (CVDR, '
            f'lokaleregelgeving.overheid.nl): {len(regs):,} regulations published here, {live:,} of them in force, '
            'each with every consolidated version CVDR keeps. One folder per regulation '
            '(<year it first took effect>/<CVDR id>/), one file per article.', '',
            '| CVDR | Regulation | In force from | Versions | Status |', '| --- | --- | --- | ---: | --- |']
    for r in regs:
        rel = r['path'][len(f'local/{auth}/'):]
        t = r['title'].replace('|', '/')
        rows.append(f'| [{r["id"]}]({r["url"]}) | [{t}]({rel}/README.md) | {r["first"]} | {r["n"]} | {r["status"]} |')
    buf = io.StringIO()
    wr = csv.writer(buf, lineterminator='\n')
    wr.writerow(['cvdr', 'title', 'path', 'first_in_force', 'versions', 'status', 'url'])
    for r in regs:
        wr.writerow([r['id'], r['title'], r['path'], r['first'], r['n'], r['status'], r['url']])
    return {f'local/{auth}/README.md': '\n'.join(rows) + '\n', f'data/local/{auth}.csv': buf.getvalue()}


def top_docs(all_regs: dict[str, list[dict]], index_counts: dict) -> str:
    rows = ['# Local regulations (CVDR)', '',
            'Every regulation of the Dutch municipalities, provinces, water boards, joint arrangements and Caribbean '
            'public bodies that the Centrale Voorziening Decentrale Regelgeving (lokaleregelgeving.overheid.nl, KOOP) '
            'holds, with every consolidated version it keeps: one folder per authority, then per year the regulation '
            'first took effect, then per CVDR id; one file per article. Texts are copied from the CVDR XML as '
            'published (free of copyright and database right, as each CVDR record states) and checked word for word '
            'against it; images in the texts are not reproduced (their place is marked "[afbeelding]").', '',
            '| Authority | Kind | Published | In CVDR |', '| --- | --- | ---: | ---: |']
    for auth in sorted(all_regs):
        regs = all_regs[auth]
        rows.append(f'| [{regs[0]["name"]}]({auth}/README.md) | {TYPE_NAME.get(regs[0]["type"], regs[0]["type"])} | '
                    f'{len(regs):,} | {index_counts.get(auth, 0):,} |')
    return '\n'.join(rows) + '\n'


def load_published() -> dict[str, dict]:
    out = {}
    if PUBLISHED.exists():
        for line in PUBLISHED.read_text(encoding='utf-8').splitlines():
            if line.strip():
                r = json.loads(line)
                out[r['id']] = r
    return out


def run(a):
    with gzip.open(STATE / 'cvdr-index.json.gz', 'rt', encoding='utf-8') as g:
        works = json.load(g)['works']
    published = load_published()
    held = set()
    if HELD.exists():
        held = {json.loads(l)['id'] for l in HELD.read_text(encoding='utf-8').splitlines() if l.strip()}
    index_counts: dict = {}
    for w in works.values():
        index_counts[w['auth']] = index_counts.get(w['auth'], 0) + 1
    order = sorted(works.values(), key=lambda w: (TYPE_ORDER.index(w['type']) if w['type'] in TYPE_ORDER else 99,
                                                  w['auth'], int(w['id'][4:])))
    todo = [w for w in order if w['id'] not in published and w['id'] not in held
            and (not a.only or w['auth'] in a.only)]
    log(f'start: {len(works):,} regulations, {len(published):,} published, {len(held):,} held, {len(todo):,} to do')
    sys.path.insert(0, str(HERE / 'builder'))
    import build as B
    import append as A
    import check_repo as K
    fetcher = Fetcher(a.threads)
    batches = 0
    i = 0
    while i < len(todo):
        if STOP.exists():
            log('STOP file: stopping at a batch boundary'); break
        if BLOCKED.exists():
            log('BLOCKED file present: stopping'); break
        if disk_free_gb() < 10:
            log(f'disk floor: {disk_free_gb():.1f} GB free < 10 GB; stopping'); break
        auth = todo[i]['auth']
        batch = []
        while i < len(todo) and todo[i]['auth'] == auth and len(batch) < a.batch:
            batch.append(todo[i]); i += 1
        docs_date = time.strftime('%Y-%m-%d', time.gmtime())
        t0 = time.time()
        urls = [(w['id'], e['n'], e['url']) for w in batch for e in w['exprs']]
        raws: dict = {}
        failed: dict = {}
        try:
            with cf.ThreadPoolExecutor(a.threads) as ex:
                futs = {ex.submit(fetcher.get, u): (wid, n) for wid, n, u in urls}
                for f in cf.as_completed(futs):
                    wid, n = futs[f]
                    try:
                        raws.setdefault(wid, {})[n] = f.result()
                    except Blocked:
                        raise
                    except Exception as exc:
                        failed[wid] = f'fetch failed for version {n}: {str(exc)[:200]}'
        except Blocked as exc:
            BLOCKED.write_text(f'{time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())} {exc}\n', encoding='utf-8')
            log(f'BLOCKED: {exc}'); break
        t_fetch = time.time() - t0
        laws: dict = {}
        acts, holds = [], []
        for w in batch:
            if w['id'] in failed:
                holds.append({'id': w['id'], 'auth': w['auth'], 'reason': failed[w['id']]}); continue
            try:
                act, why = build_work(w, raws.get(w['id'], {}), docs_date, laws)
            except Exception as exc:  # a reader error holds the regulation, never the run
                act, why = None, f'reader error: {type(exc).__name__}: {str(exc)[:200]}'
            if act:
                acts.append(act)
            else:
                holds.append({'id': w['id'], 'auth': w['auth'], 'reason': why})
        raws.clear()
        if holds:
            with open(HELD, 'a', encoding='utf-8') as f:
                for h in holds:
                    f.write(json.dumps(h, ensure_ascii=False) + '\n')
        if not acts:
            log(f'{auth}: batch of {len(batch)}: nothing publishable ({len(holds)} held)'); continue
        base = json.loads((ROOT / 'src' / 'corpus.json').read_text(encoding='utf-8'))['country']
        c = {'country': {**base, 'publisher': CVDR_PUBLISHER}, 'laws': laws, 'acts': acts, 'applies': [],
             '_docs_date': docs_date}
        old_key = B.KEY
        B.KEY = re.compile(r'^[a-z0-9][a-z0-9/-]*$')
        try:
            errs = B.validate(c)
        finally:
            B.KEY = old_key
        errs += [f'law key {k}' for k in laws if '/' in k]
        if errs:
            log(f'{auth}: corpus problems, batch skipped: {errs[:5]}')
            with open(HELD, 'a', encoding='utf-8') as f:
                for x in acts:
                    f.write(json.dumps({'id': x['_cvdr']['id'], 'auth': auth, 'reason': 'corpus problems: ' + '; '.join(errs[:3])},
                                       ensure_ascii=False) + '\n')
            continue
        acquire_lock()
        try:
            sync_main()
            head = git('rev-parse', 'main').strip()
            head_ct, head_tz = git('log', '-1', '--format=%ct %ci', 'main').split()[0::3]
            present = set()
            for k in range(0, len(acts), 50):
                out = git('ls-tree', '--name-only', 'main', '--', *[x['slug'] for x in acts[k:k + 50]])
                present |= set(out.split())
            if present:
                log(f'{auth}: {len(present)} regulation folders already on main; left out')
                acts = [x for x in acts if x['slug'] not in present]
                c['acts'] = acts
            commits = B.plan(c)
            committer = ('Lexifina', 'netherlands-law@lexifina.com')
            clock = B.Clock(c['country']['tz'])
            w_ = A.Appender(REPO, head, int(head_ct), head_tz)
            log_rows = []
            for x in commits:
                if x['kind'] == 'start':
                    author, msg, trailers = B.start_message(c, x)
                    files = B.act_files(x['act'], x['version']['units'], None)
                else:
                    author, msg, trailers = B.change_message(c, x)
                    files = {}
                    for p in x['parts']:
                        files.update(B.act_files(p['act'], p['cur']['units'], p['prev']['units'], p['keys']))
                acts_of = [x['act']] if x['kind'] == 'start' else [p['act'] for p in x['parts']]
                trailers = trailers + sorted({f'CVDR: {y["_cvdr"]["id"]}' for y in acts_of})
                B.check_trailers(trailers)
                if not (author[1].endswith('.invalid') or author[1].endswith('@lexifina.com')):
                    raise RuntimeError(f'author e-mail {author[1]!r}')
                text = '\n'.join(msg).rstrip('\n') + '\n\n' + '\n'.join(trailers) + '\n'
                w_.commit(author, clock.stamp(x['day']), committer, text, files)
                log_rows.append({'day': x['day'], 'kind': x['kind'], 'law': x.get('law'), 'acts': [y['slug'] for y in acts_of],
                                 'units': len(files), 'branch': 'main'})
            t = B.tables(c, log_rows)
            docs = {k: v for k, v in t.items() if k.endswith('/README.md') and k.startswith('local/')}
            new_regs = [{'id': x['_cvdr']['id'], 'title': x['title'], 'path': x['slug'], 'url': x['url'],
                         'first': x['_cvdr']['first'], 'n': x['_cvdr']['n'], 'status': x['_cvdr']['status'],
                         'auth': x['_cvdr']['auth'], 'name': x['_cvdr']['name'], 'type': x['_cvdr']['type'],
                         'versions': len(x['versions'])} for x in acts]
            by_auth: dict = {}
            for r in list(published.values()) + new_regs:
                by_auth.setdefault(r['auth'], []).append(r)
            docs.update(authority_docs(auth, by_auth[auth]))
            docs['local/README.md'] = top_docs(by_auth, index_counts)
            docs['tools/cvdr_run.py'] = Path(__file__).read_text(encoding='utf-8').replace('\r\n', '\n')
            docs['tools/cvdr_parse.py'] = (HERE / 'cvdr_parse.py').read_text(encoding='utf-8').replace('\r\n', '\n')
            docs['tools/cvdr_index.py'] = (HERE / 'cvdr_index.py').read_text(encoding='utf-8').replace('\r\n', '\n')
            docs['tools/bwb_parse.py'] = (HERE / 'bwb_parse.py').read_text(encoding='utf-8').replace('\r\n', '\n')
            ts, tz = clock.stamp(docs_date).split()
            name = acts[0]['_cvdr']['name']
            nv = sum(r['versions'] for r in new_regs)
            w_.commit(committer, f'{min(int(ts), int(time.time()))} {tz}', committer,
                      f'Local regulations: {name}, {len(acts)} regulations from CVDR\n\n'
                      f'Appended {len(log_rows)} commits to {head[:12]}: {len(acts)} regulations of {name} '
                      f'({nv} versions, each read from its CVDR XML and checked word for word against it; '
                      f'{len(holds)} held back in this batch). Documentation: each regulation\'s README.md, '
                      f'local/{auth}/README.md, local/README.md, data/local/{auth}.csv; tools/cvdr_*.py made these '
                      f'commits. Data retrieved {docs_date}.\n', docs)
            w_.finish()
            new_head = git('rev-parse', 'main').strip()
            # Tip check: every regulation's files are its version in force on the docs date.
            tree = {}
            slugs = [x['slug'] for x in acts]
            for k in range(0, len(slugs), 50):
                for line in git('ls-tree', '-r', new_head, '--', *slugs[k:k + 50]).splitlines():
                    meta, path = line.split('\t', 1)
                    tree[path] = meta.split()[2]
            bad = 0
            for x in acts:
                v = A.corpus_on(x['versions'], docs_date)
                want = {f'{x["slug"]}/{k}.md': K.blob_oid(u['text']) for k, u in (v['units'] if v else {}).items()}
                have = {p: o for p, o in tree.items() if p.startswith(x['slug'] + '/') and not p.endswith('/README.md')}
                if have != want or f'{x["slug"]}/README.md' not in tree:
                    bad += 1
            if bad:
                git('update-ref', 'refs/heads/main', head)
                raise RuntimeError(f'tip check: {bad} regulations differ; batch not pushed')
            r = subprocess.run(['git', 'push', 'origin', 'main'], cwd=REPO, capture_output=True, encoding='utf-8')
            if r.returncode:
                git('update-ref', 'refs/heads/main', head)
                raise RuntimeError(f'push failed: {r.stderr.strip()[-400:]}')
        finally:
            release_lock()
        with open(PUBLISHED, 'a', encoding='utf-8') as f:
            for rr in new_regs:
                f.write(json.dumps(rr, ensure_ascii=False) + '\n')
                published[rr['id']] = rr
        batches += 1
        log(f'{auth}: pushed {len(acts)} regulations, {len(log_rows)} commits, {len(holds)} held; '
            f'fetch {t_fetch:.0f}s for {len(urls)} versions; total {time.time() - t0:.0f}s; '
            f'main {new_head[:12]}; requests {fetcher.n}, errors {fetcher.errors}; free {disk_free_gb():.1f} GB')
        status = {'state': 'running', 'updated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'pid': os.getpid(),
                  'published': len(published), 'last_authority': auth, 'main': new_head[:12], 'batches': batches}
        (STATE / 'cvdr-status.json').write_text(json.dumps(status, indent=1), encoding='utf-8')
        if a.max_batches and batches >= a.max_batches:
            break
        # Shallow clone housekeeping: drop the objects already pushed once the clone grows past ~1.5 GB.
        if batches % 25 == 0:
            size = sum(f.stat().st_size for f in (REPO / '.git' / 'objects').rglob('*') if f.is_file())
            if size > 1.5 * 2**30:
                log(f'repo-local objects {size / 2**30:.2f} GB: re-cloning shallow')
                reclone()
    (STATE / 'cvdr-status.json').write_text(json.dumps({'state': 'stopped', 'updated': time.strftime(
        '%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'published': len(published)}, indent=1), encoding='utf-8')
    log('stopped')


def reclone():
    tmp = REPO.with_name('repo-local.new')
    if tmp.exists():
        shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run(['git', 'clone', '-q', '--depth', '1', '--filter=blob:none', '--no-checkout', '--single-branch',
                    '--branch', 'main', 'https://github.com/lexifina/netherlands-law.git', str(tmp)], check=True)
    old = REPO.with_name('repo-local.old')
    REPO.rename(old)
    tmp.rename(REPO)

    def onerr(func, path, exc):
        os.chmod(path, 0o666)
        func(path)
    shutil.rmtree(old, onerror=onerr)


def status():
    pub = load_published()
    held = HELD.read_text(encoding='utf-8').count('\n') if HELD.exists() else 0
    print(json.dumps({'published': len(pub), 'versions': sum(r['versions'] for r in pub.values()), 'held': held,
                      'status': json.loads((STATE / 'cvdr-status.json').read_text()) if (STATE / 'cvdr-status.json').exists() else None},
                     indent=1))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['run', 'status'])
    ap.add_argument('--threads', type=int, default=6)
    ap.add_argument('--batch', type=int, default=400)
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--max-batches', type=int, default=0)
    a = ap.parse_args()
    if a.cmd == 'status':
        status()
    else:
        (STATE / 'cvdr.pid').write_text(str(os.getpid()))
        run(a)
