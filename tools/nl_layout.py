"""netherlands-law's act folder layout: <kind>/<year>/<number>/ (as romania-law and japan-law), data/paths.json.

An act's folder comes from its official identifiers in the BWB:
  kind    the BWB soort-regeling (wet, amvb, kb, ministeriele-regeling, zbo, pbo, beleidsregel, circulaire, reglement,
          verdrag, rijkswet, rijkskb, rijksamvb, archiefselectielijst, and the -bes variants);
  year    the year of the regulation's original publication (Staatsblad, Staatscourant); for a treaty, the year it was
          concluded; else the year it was signed; else the year of its oldest BWB version;
  number  the original publication number, plain when it is the kind's own gazette (Staatsblad for wet/amvb/kb/
          rijks*, Staatscourant for the rest) and prefixed (stb-, stcrt-, trb-) otherwise; a treaty's number in the
          Treaty database (verdragnummer); else the BWB id.
Acts sharing a kind/year/number (a pre-2009 Staatscourant number is a whole issue) each get -<BWB id>. The Grondwet
and the Statuut are grondwet/1815 and statuut/1954.

meta(act) reads the identifiers from the first bytes of the act's official XML (HTTP Range) and, for a treaty, its
WTI; place(records) assigns folders. Standard library only.
"""
import collections
import json
import re
import subprocess
import time
import urllib.error
import urllib.request

LAYOUT = '<kind>/<year>/<number>'
KIND = {'wet': 'wet', 'AMvB': 'amvb', 'KB': 'kb', 'ministeriele-regeling': 'ministeriele-regeling',
        'ministeriele-regeling-archiefselectielijst': 'archiefselectielijst', 'zbo': 'zbo', 'pbo': 'pbo',
        'beleidsregel': 'beleidsregel', 'circulaire': 'circulaire', 'reglement': 'reglement', 'verdrag': 'verdrag',
        'rijkswet': 'rijkswet', 'rijksKB': 'rijkskb', 'rijksAMvB': 'rijksamvb', 'wet-BES': 'wet-bes',
        'AMvB-BES': 'amvb-bes', 'ministeriele-regeling-BES': 'ministeriele-regeling-bes',
        'beleidsregel-BES': 'beleidsregel-bes', 'circulaire-BES': 'circulaire-bes'}
STB_KINDS = {'wet', 'amvb', 'kb', 'rijkswet', 'rijkskb', 'rijksamvb', 'wet-bes', 'amvb-bes'}
SPECIAL = {'BWBR0001840': 'grondwet/1815', 'BWBR0002154': 'statuut/1954'}
REPO = 'https://repository.officiele-overheidspublicaties.nl/bwb'


def _get(url, a, b):
    req = urllib.request.Request(url, headers={'User-Agent': 'lexifina-law-layout', 'Range': f'bytes={a}-{b}'})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            if e.code == 416:
                return ''
            if e.code not in (429, 500, 502, 503, 504):
                raise
            ra = e.headers.get('Retry-After')
            time.sleep(float(ra) if ra and ra.isdigit() else 5 * (attempt + 1))
        except Exception:
            time.sleep(3 * (attempt + 1))
    raise RuntimeError('gave up ' + url)


def meta(bwb: str, toestand_url: str) -> dict:
    """The identifiers place() needs, from the official XML of one version (any) and, for a treaty, the WTI."""
    rec = {'bwb': bwb}
    if not toestand_url or toestand_url.endswith('.WTI'):  # the newest toestand XML, named at the top of the manifest
        h = _get(f'{REPO}/{bwb}/manifest.xml', 0, 4095)
        li = re.search(r'_latestItem="([^"]+)"', h)
        toestand_url = f'{REPO}/{bwb}/{li.group(1)}' if li else ''
    t = _get(toestand_url, 0, 32767) if toestand_url else ''
    if t and '<brondata' not in t and len(t) >= 32000:
        t += _get(toestand_url, 32768, 262143)
    m = re.search(r'<oorspronkelijk>(.*?)</oorspronkelijk>', t, re.S)
    if m:
        p = re.search(r'<publicatie\b([^>]*)>(.*?)</publicatie>', m.group(1), re.S)
        if p:
            s = re.search(r'\bsoort="([^"]*)"', p.group(1))
            rec['pub_soort'] = s.group(1) if s else ''
            for k, tag in (('jaar', 'publicatiejaar'), ('nr', 'publicatienr')):
                x = re.search(fr'<{tag}>(.*?)</{tag}>', p.group(2), re.S)
                rec[k] = re.sub(r'\s+', ' ', x.group(1)).strip() if x else ''
            d = re.search(r'<ondertekeningsdatum isodatum="([^"]*)"', p.group(2))
            rec['ondertekening'] = d.group(1) if d else ''
    vn = re.search(r'\bverdragnummer="(\d+)"', t)
    if vn:
        rec['verdragnummer'] = vn.group(1)
    if bwb.startswith('BWBV'):
        w = _get(f'{REPO}/{bwb}/{bwb}.WTI', 0, 16383)
        d = re.search(r'<totstandkoming>.*?<datum>(\d{4}-\d\d-\d\d)</datum>', w, re.S)
        rec['totstandkoming'] = d.group(1) if d else ''
        x = re.search(r'<extra-informatie>(\d+)</extra-informatie>', w)
        if x and not rec.get('verdragnummer'):
            rec['verdragnummer'] = x.group(1)
    elif 'jaar' not in rec:
        d = re.search(r'ondertekening_bron="(\d{4}-\d\d-\d\d)"', t) or re.search(r'<ondertekeningsdatum isodatum="(\d{4}-\d\d-\d\d)"', t)
        rec['ondertekening'] = d.group(1) if d else ''
        b = re.search(r'\bbron="(Stb|Stcrt|Trb)\.?\s*(\d{4})-([^"]+)"', t)
        if b:
            rec.update(pub_soort=b.group(1), jaar=b.group(2), nr=b.group(3))
    return rec


def clean(n: str) -> str:
    n = re.sub(r'[\s/\\]+', '-', (n or '').strip())
    n = re.sub(r'[^0-9A-Za-z.-]', '', n).strip('-.').lower()  # lower case: folders that differ only in case clash on Windows/macOS
    return n if re.search(r'[0-9]', n) else ''


def want(rec: dict, bwb_type: str, first_from: str) -> tuple[str, str, str]:
    """(kind, year, number) for one act before collisions are resolved."""
    bwb = rec['bwb']
    kind = KIND.get(bwb_type, re.sub(r'[^a-z0-9-]', '', (bwb_type or 'regeling').lower()) or 'regeling')
    if kind == 'verdrag' or bwb.startswith('BWBV'):
        kind = 'verdrag'
        year = (rec.get('totstandkoming') or rec.get('jaar') or first_from or '')[:4]
        return kind, year, clean(rec.get('verdragnummer') or '') or bwb
    nr, jaar = clean(rec.get('nr') or ''), (rec.get('jaar') or '')[:4]
    if nr and re.fullmatch(r'\d{4}', jaar):
        soort = (rec.get('pub_soort') or '').lower().rstrip('.')
        home = 'stb' if kind in STB_KINDS else 'stcrt'
        return kind, jaar, nr if soort in ('', home) else f'{soort}-{nr}'
    year = (rec.get('ondertekening') or first_from or '')[:4]
    return kind, year, bwb


def place(acts: list[dict], taken: set[str] = frozenset()) -> dict[str, str]:
    """acts: [{'slug', 'bwb', 'type', 'first_from', 'meta'}] -> {slug: folder}. Folders in `taken` (already on main)
    are never reused: a new act colliding with one gets -<BWB id>."""
    w = {}
    for a in acts:
        if a['bwb'] in SPECIAL:
            w[a['slug']] = (SPECIAL[a['bwb']], None)
            continue
        k, y, n = want(a['meta'], a['type'], a.get('first_from', ''))
        if not re.fullmatch(r'\d{4}', y or ''):
            y = 'onbekend'
        w[a['slug']] = ((k, y, n), a['bwb'])
    groups = collections.Counter(v for v, _ in w.values() if isinstance(v, tuple))
    out = {}
    for slug, (v, bwb) in w.items():
        if isinstance(v, str):
            out[slug] = v
            continue
        k, y, n = v
        f = f'{k}/{y}/{n}'
        if (groups[v] > 1 and n != bwb) or f in taken:
            f = f'{k}/{y}/{n}-{bwb}'
        out[slug] = f
    return out


# ---------- reading the layout of a clone (for the append/plan/check tools) ----------

def _show(repo, spec):
    p = subprocess.run(['git', 'show', spec], cwd=str(repo), capture_output=True, encoding='utf-8')
    return p.stdout if p.returncode == 0 else ''


def paths_json(repo, ref='main') -> dict:
    """main's data/paths.json ({'layout', 'since', 'note', 'paths': {act id: folder}}), or {} before the move."""
    t = _show(repo, f'{ref}:data/paths.json')
    try:
        return json.loads(t) if t else {}
    except ValueError:
        return {}


def folders(repo, ref='main') -> dict:
    """act id (slug) -> its folder on `ref`; an act missing from paths.json is still in its slug folder."""
    return dict(paths_json(repo, ref).get('paths') or {})


def held_slugs(repo, ref='main') -> set:
    """Act ids `ref` holds: the slug folders still at the top level plus every act data/paths.json places."""
    p = subprocess.run(['git', 'ls-tree', '--name-only', ref], cwd=str(repo), capture_output=True, encoding='utf-8')
    return set(p.stdout.split('\n')) | set(folders(repo, ref))


def remap(files: dict, where: dict) -> dict:
    """Files keyed '<slug>/<file>' -> '<folder>/<file>' for the slugs in `where`."""
    out = {}
    for path, data in files.items():
        head, sep, rest = path.partition('/')
        out[(where[head] + sep + rest) if sep and head in where else path] = data
    return out
