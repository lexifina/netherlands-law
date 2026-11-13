"""Index of every CVDR regulation (work) and its consolidated versions (expressions) from the SRU harvest.

    python -X utf8 cvdr_index.py            # writes state/cvdr-index.json.gz and prints counts by authority type

Per work: authority (type + name -> folder local/<authority>/), title, folder local/<authority>/<year>/<cvdr id>
(year = first version's in-force year; an authority-year with more than 900 regulations is split by the id's last
digit: <year>/<d>/<cvdr id>), and the versions in expression order with their in-force/out-of-force days, the
publication CVDR names (isFormatOf), the kind of change (betreft), the issue date and the XML URL.
"""
import collections
import glob
import hashlib
import gzip
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE = HERE.parent / 'state'
PREFIX = {'Gemeente': 'gemeente', 'Provincie': 'provincie', 'Waterschap': 'waterschap',
          'RegionaalSamenwerkingsorgaan': 'regio', 'Deelgemeente': 'deelgemeente', 'Koninkrijksdeel': 'land',
          'NederlandseAntillen': 'nederlandse-antillen', 'CaribischOpenbaarLichaam': 'openbaar-lichaam'}


def slug(s: str, n: int = 60) -> str:
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:n].strip('-')


def one(v):
    if isinstance(v, list):
        return '; '.join(x for x in v if x)
    return v or ''


def authority(r: dict) -> tuple[str, str, str]:
    t = r.get('organisatietype') or 'Overig'
    name = one(r.get('creator')) or 'onbekend'
    pre = PREFIX.get(t, slug(t))
    n = slug(name, 70)
    if pre == 'nederlandse-antillen' and n in ('nederlandse-antillen', ''):
        s = pre
    elif n.startswith(pre + '-') or (pre == 'waterschap' and n.startswith(('hoogheemraadschap', 'wetterskip'))):
        s = n  # the name already says what it is (Waterschap Aa en Maas, Hoogheemraadschap van Delfland)
    else:
        s = f'{pre}-{n}'
    return t, name, s


def main():
    recs = []
    for f in sorted(glob.glob(str(STATE / 'sru-cvdr' / 'p*.jsonl.gz'))):
        with gzip.open(f, 'rt', encoding='utf-8') as g:
            recs += [json.loads(l) for l in g]
    works: dict = {}
    for r in recs:
        w, e = r['identifier'].split('_')
        t, name, aslug = authority(r)
        x = works.setdefault(w, {'id': w, 'type': t, 'name': name, 'auth': aslug, 'exprs': {}})
        x['exprs'][int(e)] = {
            'n': int(e), 'from': (r.get('inwerkingtredingDatum') or '')[:10],
            'until': (r.get('uitwerkingtredingDatum') or '')[:10], 'betreft': one(r.get('betreft')),
            'pub': one(r.get('isFormatOf')), 'issued': (one(r.get('issued')) or '')[:10],
            'title': one(r.get('title')), 'url': r.get('publicatieurl_xml') or '',
            'page': r.get('preferred_url') or '', 'modified': r.get('modified') or '',
            'type': one(r.get('type')), 'ratified': one(r.get('isRatifiedBy'))}
    for w, x in works.items():
        x['exprs'] = [x['exprs'][k] for k in sorted(x['exprs'])]
        x['title'] = x['exprs'][-1]['title'] or x['exprs'][0]['title'] or w
        x['auth'] = x['auth'] or 'onbekend'
        starts = [e['from'] for e in x['exprs'] if e['from']]
        x['year'] = (min(starts) if starts else '0000')[:4]
        x['work_url'] = f'https://lokaleregelgeving.overheid.nl/{w}'
    # One authority slug must name one authority: names that differ only in case are one authority (shown under its
    # most frequent spelling); different authorities whose slugs collide get a short hash of their name.
    names = collections.defaultdict(collections.Counter)
    for x in works.values():
        names[x['auth']][(x['type'], x['name'])] += 1
    for a_, n in names.items():
        if len({(t, nm.lower()) for t, nm in n}) > 1:
            for x in works.values():
                if x['auth'] == a_:
                    x['auth'] = f"{a_[:60]}-{hashlib.sha1(x['name'].lower().encode()).hexdigest()[:4]}"
    canon = collections.defaultdict(collections.Counter)
    for x in works.values():
        canon[x['auth']][x['name']] += 1
    for x in works.values():
        x['name'] = canon[x['auth']].most_common(1)[0][0]
    names = canon
    per = collections.Counter((x['auth'], x['year']) for x in works.values())
    for w, x in works.items():
        num = w[4:]
        sub = f'{x["year"]}/{num[-1]}' if per[(x['auth'], x['year'])] > 900 else x['year']
        x['path'] = f'local/{x["auth"]}/{sub}/{w.lower()}'
    out = STATE / 'cvdr-index.json.gz'
    with gzip.open(out, 'wt', encoding='utf-8') as g:
        json.dump({'records': len(recs), 'works': works}, g, ensure_ascii=False)
    by_type = collections.defaultdict(lambda: [set(), 0, 0, 0])
    for x in works.values():
        b = by_type[x['type']]
        b[0].add(x['auth']); b[1] += 1; b[2] += len(x['exprs'])
        b[3] += 1 if not x['exprs'][-1]['until'] else 0
    print(f'records {len(recs):,}  works {len(works):,}  authorities {len(names):,}')
    for t, (a, n, v, live) in sorted(by_type.items(), key=lambda kv: -kv[1][1]):
        print(f'{t}: {len(a)} authorities, {n:,} regulations ({live:,} in force), {v:,} versions')
    print('max per dir', max(collections.Counter(x['path'].rsplit('/', 1)[0] for x in works.values()).values()))


if __name__ == '__main__':
    main()
