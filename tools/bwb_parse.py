"""Turns the cached BWB versions into scripts/netherlands-law/corpus.json (see scripts/gitlaw_common/SCHEMA.md).

    python -X utf8 scripts/netherlands-law/parse.py            # corpus.json: the acts with no "part" in acts.json
    python -X utf8 scripts/netherlands-law/parse.py <part>...  # corpus.d/<part>.json for each part named

Reads only .cache/ (written by fetch.py); no network. Deterministic: the same cache gives the same bytes.

What it does, per act in acts.json:
- takes every version ("toestand") the BWB manifest still shows (zichtdatum_eind 9999-12-31; a superseded _0 is
  replaced by the corrected _1 for the same day), in order of its in-force date (datum_inwerkingtreding);
- writes one unit per article (artikel), plus one `inhoud` unit holding the act's headings (Boek, Titel, Hoofdstuk,
  Afdeling, Paragraaf). Articles the BWB marks "vervallen" (repealed) or "nogniet" (not yet in force) are absent;
- credits each changed article to the Staatsblad publication the BWB names on that article (bron="Stb.2017-82"),
  but only when the article's own in-force date (inwerking) is the version's day. Anything else is left
  uncredited, so the builder commits it as unexplained, by the publisher;
- names each law by the Staatsblad issue's own metadata title (officielebekendmakingen.nl), where it has one.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fetch  # noqa: E402

RETRIEVED = '2026-10-28'
STRUCT = {'boek', 'deel', 'titeldeel', 'hoofdstuk', 'afdeling', 'paragraaf', 'sub-paragraaf', 'circulaire.divisie',
          'divisie'}
SKIP = {'meta-data', 'kop', 'lidnr', 'li.nr', 'jcis', 'jci'}
GONE = {'vervallen', 'nogniet'}
ROMAN = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
log: Counter = Counter()
notes: list[str] = []


def roman(s: str) -> int | None:
    if not re.fullmatch(r'[IVXLC]+', s):
        return None
    total = 0
    for a, b in zip(s, s[1:] + ' '):
        v = ROMAN[a]
        total += -v if b != ' ' and ROMAN[b] > v else v
    return total


def norm(s: str) -> str:
    s = s.replace('\xa0', ' ').replace(' ', ' ').replace(' ', ' ').replace('\xad', '')
    s = s.replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
    s = re.sub(r'\s+', ' ', s).strip()
    return re.sub(r' ([,.;:])(?=\s|$)', r'\1', s)


def inline(el: ET.Element) -> str:
    """The running text of an element: references and emphasis as plain text, editorial notes in brackets."""
    out = [el.text or '']
    for ch in el:
        if ch.tag not in SKIP and ch.tag not in ('noot', 'voetnoot', 'aanhaling.noot'):
            t = inline(ch)
            out.append(f'[{norm(t)}]' if ch.tag == 'redactie' and norm(t) else t)
        out.append(ch.tail or '')
    return ''.join(out)


BLOCKS = {'al', 'lid', 'lijst', 'li', 'table', 'tgroup', 'tbody', 'thead', 'row', 'tussenkop', 'al-groep',
          'structuurtekst', 'definitielijst', 'definitie-item', 'aanhaling', 'artikel', 'wat', 'nadruk'}


def implicit_marker(lijst: ET.Element, i: int) -> str:
    """The number of the i-th item of a list that numbers itself (<lijst type="a" start="1" nr-sluiting=".">, items
    without li.nr), as wetten.overheid.nl prints it; '' for unmarked lists."""
    kind = lijst.get('type') or ''
    try:
        n = int(lijst.get('start') or 1) + i
    except ValueError:
        n = 1 + i
    if kind == '1':
        mark = str(n)
    elif kind in ('a', 'A') and n <= 26:
        mark = chr(ord(kind) + n - 1)
    elif kind in ('i', 'I'):
        vals = [(10, 'x'), (9, 'ix'), (5, 'v'), (4, 'iv'), (1, 'i')]
        mark, m = '', n
        for v, r in vals:
            while m >= v:
                mark, m = mark + r, m - v
        mark = mark.upper() if kind == 'I' else mark
    else:
        return ''
    return mark + (lijst.get('nr-sluiting') or '')


def running_text(el: ET.Element, blocks: set = BLOCKS) -> bool:
    """Mixed content with only inline children (e.g. <term>per Nm<sup>3</sup></term>): one line of running text.
    Before 2026-11-02 such an element was walked as a block, keeping only its children's text (Wbm art. 27, 36i)."""
    if any(g.tag in blocks for g in el):
        return False
    return bool((el.text or '').strip()) or any((g.tail or '').strip() for g in el if g.tag not in SKIP)


def render(el: ET.Element, blocks: set = BLOCKS) -> list[str]:
    """One line per paragraph, list item or table row."""
    lines: list[str] = []
    for ch in el:
        if ch.tag in SKIP:
            continue
        if ch.tag == 'lid':
            nr = norm(inline(ch.find('lidnr'))) if ch.find('lidnr') is not None else ''
            sub = render(ch, blocks)
            if nr and sub:
                sub[0] = f'{nr}{"" if nr[-1] in ".)" else "."} {sub[0]}'
            elif nr:
                sub = [nr]
            lines += sub
        elif ch.tag == 'li':
            nr = norm(inline(ch.find('li.nr'))) if ch.find('li.nr') is not None else ''
            if not nr and el.tag == 'lijst':
                nr = implicit_marker(el, [c for c in el if c.tag == 'li'].index(ch))
            sub = render(ch, blocks)
            if not sub and (ch.text or '').strip():
                sub = [norm(inline(ch))]
            if nr and sub:
                sub[0] = f'{nr} {sub[0]}'
            elif nr:
                sub = [nr]
            lines += sub
        elif ch.tag == 'row':
            cells = [norm(inline(e)) for e in ch if e.tag == 'entry']
            if any(cells):
                lines.append(' | '.join(cells))
        elif ch.tag in ('al', 'tussenkop', 'kop.al') or not any(g.tag not in SKIP for g in ch) or running_text(ch, blocks):
            t = norm(inline(ch))
            if t:
                lines.append(t)
        else:
            lines += render(ch, blocks)
    return lines


def article_key(nr: str, label: str) -> str:
    n = nr.strip()
    m = re.fullmatch(r'(\d+)\s*([a-z]*)', n.lower())
    if m:
        return f'art-{int(m.group(1)):03d}{m.group(2)}'
    parts = re.split(r'\s*[.:]\s*', n.lower())
    if len(parts) > 1 and all(re.fullmatch(r'\d+', p) for p in parts[:-1]) and re.fullmatch(r'\d+[a-z]*', parts[-1]):
        # chapter-numbered articles (Awb "4:84a", Sv Boek 5 "5.3.10"): every number zero-padded, the last to 3
        pads = [2] * (len(parts) - 1) + [3]
        return 'art-' + '-'.join(re.sub(r'^\d+', lambda d: str(int(d.group())).zfill(w), p)
                                 for p, w in zip(parts, pads))
    r = roman(n)
    if r:
        return f'add-art-{r:02d}'
    slug = re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
    log['article number not numeric'] += 1
    return f'art-{slug or re.sub(r"[^a-z0-9]+", "-", label.lower())}'


def heading(el: ET.Element) -> str:
    kop = el.find('kop')
    if kop is None:
        return ''
    parts = [norm(inline(kop.find(t))) for t in ('label', 'nr') if kop.find(t) is not None]
    head = ' '.join(p for p in parts if p)
    titel = kop.find('titel')
    if titel is not None and norm(inline(titel)):
        head = f'{head}. {norm(inline(titel))}' if head else norm(inline(titel))
    return head


def read_version(raw: bytes, bijlage_keys: bool = False, single_file: bool = False) -> dict:
    """units {key: {label, kind, text}}, attrs {key: article attributes}, gone {key: attrs}, struct attrs.

    bijlage_keys (acts.json "bijlage_keys"): articles inside an annex (bijlage) are keyed bijlage-<n>-art-...,
    so an annex's Artikel 1 does not collide with the act's own, and an annex article with no source of its own
    takes the annex's (bron, inwerking), where the BWB records it.

    single_file (acts.json "single_file", breadth parts from 2026-11-05 only; no earlier part sets it): when the
    usual walk finds no article, the articles are looked for anywhere in the text (treaties: verdrag/verdragtekst),
    and if there are none at all (circulaires, beleidsregels, most treaties' free text) the whole text of the
    regulation, minus its title elements, is one unit 'tekst' (headings as '## ' lines). Without the flag nothing
    changes, so every earlier part re-parses byte for byte."""
    root = ET.fromstring(raw)
    units: dict = {}
    attrs: dict = {}
    gone: dict = {}
    toc: list[str] = []
    struct: list[dict] = []
    n_b = [0]
    anywhere = [False]

    def walk(el: ET.Element, depth: int, prefix: str = '', inherit: dict | None = None) -> None:
        for ch in el:
            if ch.tag == 'meta-data':
                continue
            if ch.tag == 'artikel':
                kop = ch.find('kop')
                nr = norm(inline(kop.find('nr'))) if kop is not None and kop.find('nr') is not None else ''
                key = prefix + (article_key(nr, ch.get('label', '')) if nr else 'art-000')
                if ch.get('status') in GONE:
                    gone[key] = dict(ch.attrib)
                    continue
                if key in units:
                    log[f'duplicate article key {key}'] += 1
                    i = 2
                    while f'{key}-{i}' in units:
                        i += 1
                    key = f'{key}-{i}'
                head = heading(ch) or ch.get('label', key)
                body = render(ch)
                lab = f'Art. {nr}' if nr else head
                if prefix.startswith('bijlage-'):
                    lab = f'Bijlage {prefix.split("-")[1]}, {lab}'
                units[key] = {'label': lab, 'kind': 'art',
                              'text': '\n'.join([f'# {head}'] + body) + '\n'}
                attrs[key] = dict(ch.attrib)
                if inherit and 'bron' not in ch.attrib:
                    attrs[key].update(inherit)  # an annex article without its own source: the annex's
            elif ch.tag in STRUCT:
                if ch.get('status') not in GONE:
                    h = heading(ch)
                    if h:
                        toc.append('#' * min(depth + 2, 6) + ' ' + h)
                        struct.append(dict(ch.attrib))
                walk(ch, depth + 1, prefix, inherit)
            elif ch.tag == 'bijlage' and bijlage_keys:
                kop = ch.find('kop')
                bnr = norm(inline(kop.find('nr'))) if kop is not None and kop.find('nr') is not None else ''
                n_b[0] += 1
                tag = re.sub(r'[^a-z0-9]+', '-', bnr.lower()).strip('-') or str(n_b[0])
                walk(ch, depth, f'bijlage-{tag}-', {a: ch.get(a) for a in ('bron', 'inwerking', 'ondertekening_bron',
                                                                        'publicatie_bron') if ch.get(a)})
            elif ch.tag in ('wetgeving', 'wet-besluit', 'wettekst', 'regeling', 'regeling-tekst', 'bijlage'):
                walk(ch, depth, prefix, inherit)
            elif anywhere[0] and ch.tag not in SKIP and ch.tag not in NOTES:
                walk(ch, depth, prefix, inherit)
    body = root.find('wetgeving') if root.find('wetgeving') is not None else root
    walk(body, 0)
    mode = None
    if single_file and not any(u['kind'] == 'art' for u in units.values()):
        units.clear(); attrs.clear(); gone.clear(); toc.clear(); struct.clear()
        anywhere[0] = True
        walk(body, 0)
        mode = 'articles-anywhere'
        if not any(u['kind'] == 'art' for u in units.values()):
            units.clear(); attrs.clear(); gone.clear(); toc.clear(); struct.clear()
            lines = flat([ch for ch in body if ch.tag not in TITLE_TAGS])
            mode = 'text'
            if lines:
                units['tekst'] = {'label': 'Tekst', 'kind': 'art', 'text': '\n'.join(['# Tekst'] + lines) + '\n'}
                attrs['tekst'] = {a: body.get(a) for a in ('inwerkingtredingsdatum',) if body.get(a)}
    if toc:
        units['inhoud'] = {'label': 'Inhoud', 'kind': 'contents', 'text': '\n'.join(['# Inhoud'] + toc) + '\n'}
    corrections = len(root.findall('./redactionele-correcties/redactionele-correctie'))
    return {'units': units, 'attrs': attrs, 'gone': gone, 'struct': struct, 'corrections': corrections,
            **({'single_file': mode} if mode else {})}


NOTES = ('noot', 'voetnoot', 'aanhaling.noot')
# single-file text only: emphasis is running text (<datum>de <nadruk>eenendertigste</nadruk> juli 2014</datum>)
FLAT_BLOCKS = BLOCKS - {'nadruk'}
TITLE_TAGS = {'intitule', 'citeertitel', 'meta-data', 'jcis', 'jci'} | set(NOTES)


def strip_notes(el: ET.Element) -> ET.Element:
    """A deep copy of el without footnotes (their tails kept), so render() never prints a note's text."""
    import copy
    c = copy.deepcopy(el)

    def clean(e: ET.Element) -> None:
        prev = None
        for ch in list(e):
            if ch.tag in NOTES:
                if ch.tail:
                    if prev is None:
                        e.text = (e.text or '') + ch.tail
                    else:
                        prev.tail = (prev.tail or '') + ch.tail
                e.remove(ch)
                continue
            clean(ch)
            prev = ch
    clean(c)
    return c


def flat(children: list) -> list[str]:
    """Single-file text: headings ('## ' + label, number and title) and every block in document order."""
    lines: list[str] = []
    for ch in children:
        if ch.tag in TITLE_TAGS - {'intitule', 'citeertitel'}:
            continue
        if ch.tag == 'kop':
            t = norm(inline(ch))
            if t:
                lines.append('## ' + t)
        elif ch.find('.//kop') is not None:
            if (ch.text or '').strip():
                lines.append(norm(ch.text))
            lines += flat(list(ch))
        else:
            wrap = ET.Element('wrap')
            wrap.append(strip_notes(ch))
            lines += render(wrap, FLAT_BLOCKS)
    return lines


def law_key(bron: str) -> str | None:
    m = re.fullmatch(r'(\w+)\.(\d{4})-(\d+)', bron or '')
    return f'{m.group(1).lower()}-{m.group(2)}-{m.group(3)}' if m else None


def wti_laws(raw: bytes) -> dict[str, list[str]]:
    """{in-force day: [Staatsblad ids that the WTI lists as taking effect that day]}"""
    out: dict[str, list[str]] = {}
    for m in re.finditer(rb'<datum waarde="(\d{4}-\d\d-\d\d)">(.*?)</datum>', raw, re.S):
        ids = []
        for o in re.findall(rb'<ontstaansbron>(.*?)</ontstaansbron>', m.group(2), re.S):
            ids += re.findall(rb'urlidentifier="([a-z]+-\d{4}-\d+)"', o)
        out[m.group(1).decode()] = sorted({i.decode() for i in ids})
    return out


def law_meta(bron: str) -> dict:
    p = fetch.cache_path(fetch.law_url(bron))
    if not p.exists():
        return {}
    s = p.read_text(encoding='utf-8')
    get = lambda name: (re.search(rf'name="{re.escape(name)}"[^>]*content="([^"]*)"', s) or [None, None])[1]
    import html
    return {'title': html.unescape(get('DC.title') or ''), 'signed': get('OVERHEIDop.datumOndertekening'),
            'issued': get('DCTERMS.issued'), 'type': get('DC.type')}


def build_act(slug: str, spec: dict, laws: dict, uses: Counter) -> dict:
    bwb = spec['bwb']
    exprs = sorted((e for e in fetch.expressions(fetch.fetch(fetch.manifest_url(bwb), offline=True))
                    if e['seen_until'] == '9999-12-31'), key=lambda e: e['from'])
    # Breadth mode (Alan, 2026-11-02 "speed up coverage"): acts.json "current_label" pins the one toestand used, the
    # one in force on "as_of" (or, for a repealed act, its last); the act's other toestanden stay in the stored zip.
    current = spec.get('current_label')
    all_exprs = exprs
    if current:
        exprs = [e for e in exprs if e['label'] == current]
        if not exprs:
            raise SystemExit(f'{slug}: current_label {current} is not a visible toestand')
    wti_raw = fetch.fetch(fetch.wti_url(bwb), offline=True)
    wti = wti_laws(wti_raw)
    # From part 68 on: a publication the WTI names is credited from its label (and the WTI's dates) alone.
    pubs = fetch.wti_publications(wti_raw) if fetch.wti_label_mode(spec.get('part')) else {}
    versions = []
    prev = None
    dropped = 0

    def credit(attr: dict | None, day: str) -> list[str]:
        if not attr or attr.get('inwerking') != day or not law_key(attr.get('bron')):
            return []
        key = law_key(attr['bron'])
        if key not in laws:
            m = law_meta(attr['bron']) if key not in pubs else {'signed': pubs[key]['signed'],
                                                                   'issued': pubs[key]['issued']}
            if key in pubs:
                log['credited from the WTI label (no title lookup)'] += 1
            year, nr = key.split('-')[1:]
            title = m.get('title') or ''
            stcrt = key.startswith('stcrt-')  # a Staatscourant publication (e.g. a ministerial regulation)
            kind = 'decree' if stcrt or re.match(r'(Koninklijk )?[Bb]esluit', title) else 'law'
            laws[key] = {'label': f'{"Stcrt." if stcrt else "Stb."} {year}, {nr}',
                         'title': title or f'{"Staatscourant" if stcrt else "Staatsblad"} {year}, nr. {nr}',
                         'kind': kind, 'enacted': attr.get('ondertekening_bron') or m.get('signed'),
                         'published': attr.get('publicatie_bron') or m.get('issued'),
                         'url': f'https://zoek.officielebekendmakingen.nl/{key}' if int(year) >= 1995 else None,
                         'temporary_until': None, 'restores': None, 'note': None}
            for d in ('enacted', 'published'):
                if laws[key][d] and not re.fullmatch(r'\d{4}-\d\d-\d\d', laws[key][d]):
                    laws[key][d] = None
        uses[key] += 1
        return [key]

    for e in exprs:
        url = fetch.version_url(bwb, e['label'])
        raw = fetch.fetch(url, offline=True)
        v = read_version(raw, spec.get('bijlage_keys', False), spec.get('single_file', False))
        day = e['from']
        if prev is None:
            # The first version is the act as enacted only if every article still carries the act's own
            # enacting publication (the bron on its intitule) and took effect on this day.
            first = {(a.get('bron'), a.get('inwerking')) for a in v['attrs'].values()}
            enacting = (re.search(rb'<intitule [^>]*?\sbron="([^"]+)"', raw) or [None, b''])[1].decode()
            first_law = None
            if len(first) == 1:
                bron, inw = next(iter(first))
                if inw == day and law_key(bron) and bron == enacting and not current:
                    first_law = credit({'bron': bron, 'inwerking': inw, **next(iter(v['attrs'].values()))}, day)[0]
            ver = {'from': day, 'source_url': url, 'sha256': hashlib.sha256(raw).hexdigest(), 'units': v['units'],
                   'credits': {}}
            versions.append(ver)
            prev = v
            continue
        changes = {}
        credits = {}
        for k in sorted(set(prev['units']) | set(v['units'])):
            a, b = prev['units'].get(k), v['units'].get(k)
            if a == b:
                continue
            changes[k] = b
            if k == 'inhoud':
                c = sorted({x for s in v['struct'] for x in credit(s, day)})
            elif b is None:
                c = credit(v['gone'].get(k), day)
                if not c and len(wti.get(day, [])) == 1 and wti[day][0].startswith('stb-'):
                    c = credit({'bron': 'Stb.' + wti[day][0][4:], 'inwerking': day}, day)
                    log['removal credited from the WTI (the only law that day)'] += 1
            else:
                c = credit(v['attrs'].get(k), day)
            if c:
                credits[k] = c
            else:
                log['unexplained unit change'] += 1
        # A Besluit publishing the text of the revised Grondwet (Art. 141 Gw) is the bron the BWB gives the
        # wording, but the revision laws the WTI lists for the same day made the change: say so on the Besluit.
        for k in {x for c in credits.values() for x in c}:
            if 'ter bekendmaking van de tekst' in (laws[k]['title'] or '') and not laws[k]['note']:
                others = [o for o in wti.get(day, []) if o != k]
                if others:
                    labels = '; '.join('Stb. {}, {}'.format(*o.split('-')[1:]) for o in others)
                    laws[k]['note'] = (f'Publishes the text of the revised {spec["title"]} (Art. 141 Grondwet); the BWB names '
                                       f'it as the source of the wording. The revision laws the BWB lists as taking '
                                       f'effect the same day: {labels}.')
        if not changes:
            dropped += 1
            prev = v
            continue
        ver = {'from': day, 'source_url': url, 'sha256': hashlib.sha256(raw).hexdigest(), 'changes': changes,
               'credits': credits}
        if any(k not in credits for k in changes) and v['corrections']:
            ver['note'] = (f'The BWB lists {v["corrections"]} editorial correction(s) (redactionele correcties) in '
                           'this version; changes it does not attribute to a law are committed as unexplained.')
        versions.append(ver)
        prev = v
    # Whole-act repeal (coordinator, Alan's option 2, 2026-11-02; parts in wti_label_mode only): when the act's last
    # BWB version has an end date, a final version the day after removes every unit, credited to the publication the
    # WTI lists that day as "intrekking-regeling" (else the publisher, unexplained).
    last = all_exprs[-1] if all_exprs else None
    if current and last and last['label'] != current:
        last = None   # a current-text act whose last toestand is a later one: not repealed
    import datetime as _dt
    repeal_day = (None if not last or last['until'] in (None, '9999-12-31') else
                  (_dt.date.fromisoformat(last['until']) + _dt.timedelta(days=1)).isoformat())
    if current and repeal_day and repeal_day > spec['as_of']:
        repeal_day = None   # ends after the as-of day: not repealed yet
    if fetch.wti_label_mode(spec.get('part')) and repeal_day and versions:
        day = repeal_day
        repealer = None
        for m in re.finditer(rb'<datum waarde="' + day.encode() + rb'">(.*?)</datum>', wti_raw, re.S):
            for d in re.findall(rb'<details>(.*?)</details>', m.group(1), re.S):
                if b'<betreft>intrekking-regeling</betreft>' in d:
                    o = re.search(rb'<ontstaansbron>.*?urlidentifier="((stb|stcrt)-(\d{4})-(\d+))"', d, re.S)
                    if o and repealer is None:
                        repealer = f'{o.group(2).decode().capitalize()}.{o.group(3).decode()}-{o.group(4).decode()}'
        state: dict = {}
        for v in versions:
            if 'units' in v:
                state = dict(v['units'])
            for k, x in (v.get('changes') or {}).items():
                if x is None:
                    state.pop(k, None)
                else:
                    state[k] = x
        c = credit({'bron': repealer, 'inwerking': day}, day) if repealer else []
        if not c:
            log['whole-act repeal without a WTI-named law'] += 1
        versions.append({'from': day, 'source_url': fetch.wti_url(bwb), 'sha256': hashlib.sha256(wti_raw).hexdigest(),
                         'changes': {k: None for k in sorted(state)},
                         'credits': {k: c for k in sorted(state)} if c else {},
                         'note': f'Repealed in full: the BWB\'s last version ends {last["until"]}, and its amendment '
                                 f'record (WTI) lists the repeal (intrekking-regeling) on {day}'
                                 + (f' by {c[0].split("-")[0].capitalize()}. {c[0].split("-")[1]}, {c[0].split("-")[2]}.'
                                    if c else ', naming no publication.')})
        log['whole-act repeal'] += 1
    if dropped:
        notes.append(f'{slug}: {dropped} BWB version(s) change no rendered text (only metadata or references) and '
                     'are not separate versions here.')
    if current:
        first_law = None   # current text only: the builder commits it as "oldest version available"
    return {'slug': slug, 'short': spec['short'], 'title': spec['title'],
            'url': f'https://wetten.overheid.nl/{bwb}', 'first_law': first_law, 'earlier_laws': [],
            'versions': versions}


PART_RETRIEVED = '2026-10-29'


def write_part(part: str) -> None:
    """corpus.d/<part>.json: the acts acts.json assigns to that part, with only the laws they credit."""
    laws: dict = {}
    uses: Counter = Counter()
    specs = {slug: spec for slug, spec in fetch.ACTS.items() if spec.get('part') == part}
    if not specs:
        raise SystemExit(f'no acts in part {part}')
    acts = [build_act(slug, spec, laws, uses) for slug, spec in specs.items()]
    reqs = sum(1 for _ in open(fetch.CACHE / 'requests.jsonl', encoding='utf-8'))
    retrieved, how = PART_RETRIEVED, 'manifest.xml, every toestand XML still visible in the manifest, and the WTI.'
    # Parts fetched as work-level zips (fetch.py --zip, from 2026-11-02): the retrieval day is the day of the act's
    # zip, and `requests` counts only this part's own repository requests, so a re-parse gives the same bytes
    # whatever else was fetched since.
    zl = fetch.CACHE / 'zip-extracts.jsonl'
    zips = {}
    if zl.exists():
        for line in open(zl, encoding='utf-8'):
            r = json.loads(line)
            zips.setdefault(r['zip'], r['at'][:10])
    mine = [zips.get(fetch.zip_url(s['bwb'])) for s in specs.values()]
    if any(mine):
        retrieved = max(d for d in mine if d)
        ids = {s['bwb'] for s in specs.values()}
        reqs = sum(1 for line in open(fetch.CACHE / 'requests.jsonl', encoding='utf-8')
                   if (m := re.search(r'/bwb/(BWB[RV]\d{7})[/?]', line)) and m.group(1) in ids)
        how = ('one work-level zip per act (?output=zip: manifest.xml, the WTI and every toestand XML), of which '
               'every toestand still visible in the manifest is used.')
    names = ', '.join(f"{s['title']} ({s['bwb']})" for s in specs.values())
    starts = ', '.join(f"{a['title']} {a['versions'][0]['from']}" for a in acts)
    breadth = [s for s in specs.values() if s.get('current_label')]
    if breadth:
        how = ('one work-level zip per act (?output=zip: manifest.xml, the WTI and every toestand XML), of which one '
               'toestand per act is used: the one in force on the as-of day, or for a repealed act its last.')
        nz = [s['title'] for s in breadth if s.get('no_zip')]
        if nz:
            how += (f' For {len(nz)} act(s) whose zip the repository did not deliver ({"; ".join(nz)}), the '
                    'manifest, the WTI and that toestand were read as separate files.')
    data = {
        'sources': [
            {'name': 'Basiswettenbestand (BWB), wetten.overheid.nl', 'url': 'https://repository.officiele-overheidspublicaties.nl/bwb/',
             'retrieved': retrieved, 'requests': reqs, 'licence': 'CC0 1.0',
             'notes': f'{names}: {how}'},
            {'name': 'officielebekendmakingen.nl (Staatsblad metadata)', 'url': 'https://zoek.officielebekendmakingen.nl/',
             'retrieved': retrieved, 'requests': None, 'licence': 'CC0 1.0',
             'notes': 'Title, signature and publication date of each crediting Staatsblad issue, 1995 onwards.'},
        ],
        'laws': dict(sorted(laws.items())),
        'acts': acts,
        'applies': [],
        'decisions': ([
            f'{names}: built by the same method as the rest of the corpus (every BWB toestand still visible, dated by '
            'datum_inwerkingtreding, articles credited to their bron when their inwerking is the day of the version).',
            f'History starts at the oldest version the BWB holds: {starts}; earlier history is not reconstructed.',
        ] if not breadth else [
            f'Current text only (breadth first, Alan 2026-11-02): {len(breadth)} acts, each with one version, the BWB '
            'toestand in force on the as-of day ' + ', '.join(sorted({s["as_of"] for s in breadth})) + ' (its label '
            'is in the version\'s source_url, its sha256 is pinned), dated by that toestand\'s own in-force day '
            '(datum_inwerkingtreding) and committed by the publisher as the oldest version available (first_law '
            'null). The act\'s earlier toestanden are in the BWB and are not yet included; they can be added later as '
            'history.',
            'A current-text act whose BWB versions have all ended is repealed: its one version is its last toestand, '
            'followed on the day after that toestand ends by a version that removes every provision, credited to the '
            'publication the act\'s amendment record (WTI) lists as the repeal (intrekking-regeling) that day, or to '
            'the publisher where the record names none.',
        ]) + (['Where the BWB names a Staatscourant publication as the source of a wording (bron="Stcrt.YYYY-N", '
              'for example a ministerial regulation adjusting amounts), it is labelled "Stcrt." and counted as a '
              'decree.'] if any(k.startswith('stcrt-') for k in laws) else [])
          + (['An amending publication that the act\'s WTI (amendment record) names is credited by its label alone '
              '("Stb. YYYY, N" or "Stcrt. YYYY, N"), with the signature and publication dates the WTI gives; its title '
              'is given only where the record names it (an officielebekendmakingen.nl title is used only for a '
              'source the WTI does not list).']
             if any(fetch.wti_label_mode(s.get('part')) for s in specs.values()) else []) + notes,
        'ai_use': ['none: no model wrote, summarised or classified any text in this part. The parser was written by '
                   'Claude Code (claude-opus-5-5).'],
    }
    out = HERE / 'corpus.d'
    out.mkdir(exist_ok=True)
    tmp = out / f'{part}.json.tmp'
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    tmp.replace(out / f'{part}.json')
    for a in acts:
        print(a['slug'], len(a['versions']), 'versions', 'first_law', a['first_law'])
    print(part, 'laws', len(laws), dict(log))


def main() -> None:
    if len(sys.argv) > 1:
        for part in sys.argv[1:]:
            log.clear()
            notes.clear()
            write_part(part)
        return
    laws: dict = {}
    uses: Counter = Counter()
    specs = {slug: spec for slug, spec in fetch.ACTS.items() if not spec.get('part')}
    acts = [build_act(slug, spec, laws, uses) for slug, spec in specs.items()]
    reqs = sum(1 for _ in open(fetch.CACHE / 'requests.jsonl', encoding='utf-8'))
    corpus = {
        'country': {
            'code': 'NL', 'name': 'Netherlands', 'slug': 'netherlands', 'lang': 'nl', 'tz': 'Europe/Amsterdam',
            'future_branch': 'toekomst',
            'publisher': {'name': 'KOOP, wetten.overheid.nl (Basiswettenbestand)', 'email': 'bwb@wetten-overheid.invalid'},
            'default_in_force_rule': {
                'text': 'Bekendmakingswet art. 10(1): where a law names no date, it takes effect on the first day of '
                        'the second calendar month after its publication. Every version here carries the BWB\'s own '
                        'in-force date (datum_inwerkingtreding), which already applies each law\'s own commencement.',
                'source': 'https://wetten.overheid.nl/jci1.3:c:BWBR0004287&artikel=10'},
            'licence_note': 'Wet- en regelgeving: Basiswettenbestand (wetten.overheid.nl), KOOP, Ministerie van '
                            'Binnenlandse Zaken en Koninkrijksrelaties; open data, CC0 1.0 (public domain dedication).',
        },
        'sources': [
            {'name': 'Basiswettenbestand (BWB), wetten.overheid.nl', 'url': 'https://repository.officiele-overheidspublicaties.nl/bwb/',
             'retrieved': RETRIEVED, 'requests': reqs, 'licence': 'CC0 1.0',
             'notes': 'Per act: manifest.xml (every dated version), the toestand XML of each version, and the WTI '
                      '(wetstechnische informatie). Versions in the BWB start between 2002 and 2018 depending on the act.'},
            {'name': 'officielebekendmakingen.nl (Staatsblad metadata)', 'url': 'https://zoek.officielebekendmakingen.nl/',
             'retrieved': RETRIEVED, 'requests': None, 'licence': 'CC0 1.0',
             'notes': 'Title, signature and publication date of each crediting Staatsblad issue, 1995 onwards.'},
        ],
        'laws': dict(sorted(laws.items())),
        'acts': acts,
        'applies': [],
        'decisions': [
            'Acts: the Grondwet, Burgerlijk Wetboek Boek 1, the Wetboek van Strafrecht and the UAVG (Phase 1), chosen because the BWB holds dated versions for each.',
            'History starts at the oldest version the BWB holds for each act (2002 for the codes and the Grondwet, 2018 for the UAVG); earlier history is not reconstructed.',
            'Only versions still visible in the BWB manifest (zichtdatum_eind 9999-12-31) are used; where the BWB re-issued a day as _1, the _1 replaces the _0.',
            'Each version is dated by the BWB\'s datum_inwerkingtreding, the day it took effect.',
            'A changed article is credited to the Staatsblad publication the BWB names on that article (bron), only when the article\'s own inwerking date equals the version\'s day; otherwise it is left unexplained.',
            'A removed article is credited to the bron on its "vervallen" entry; if it vanished without one, to the only Staatsblad issue the WTI lists for that day, if there is exactly one.',
            'Articles marked "vervallen" (repealed) or "nogniet" (not yet in force) are absent from the tree; the BWB\'s "Vervallen" placeholders are not kept as text.',
            'Editorial notes (redactie) are kept in square brackets; footnotes and metadata are dropped.',
            'Headings of Boeken, Titels, Hoofdstukken, Afdelingen and Paragrafen are kept in one inhoud unit per act, credited to the bron of the headings that took effect that day.',
            'Law kind: a Staatsblad title starting "Besluit" is a decree; everything else is a law.',
            'Grondwet 2018-12-21: the BWB credits the text to Stb. 2019, 33 (the Besluit of 16 January 2019 publishing the revised Grondwet, Art. 141 Gw) with in-force date 2018-12-21, before that Besluit was signed; the in-force date is kept as the BWB gives it.',
        ] + notes,
        'ai_use': ['none: no model wrote, summarised or classified any text in this corpus. The parser was written by Claude Code (claude-opus-5-5).'],
    }
    tmp = HERE / 'corpus.json.tmp'
    tmp.write_text(json.dumps(corpus, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    tmp.replace(HERE / 'corpus.json')
    for a in acts:
        print(a['slug'], len(a['versions']), 'versions', 'first_law', a['first_law'])
    print('laws', len(laws), dict(log))


if __name__ == '__main__':
    main()
