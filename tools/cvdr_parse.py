"""Read one CVDR expression (repository.officiele-overheidspublicaties.nl/cvdr/<work>/<n>/xml/<work>_<n>.xml) into units.

Units, in the BWB corpus's style (tools/bwb_parse.py, the BWB reader, does the text rendering):
  aanhef            the preamble (Aanhef)
  art-...           one per article of the regulation text; structural headings in one `inhoud` unit
  tekst             the regulation text when it has no articles (headings as '## ' lines)
  slot              the closing formula and signature (regeling-sluiting)
  bijlage-<n>[-art-...]  each annex (its articles separately when it has any)
  toelichting       the explanatory note (nota-toelichting), part of the published text
The title (intitule) is the act's title, not a unit. Images (plaatje/illustratie) are not reproduced: their place
holds a line "[afbeelding: <name>]" so the omission is visible.

verify(raw, units) is independent of the rendering: it compares the multiset of words in the XML body (minus the
title, footnotes and the attribute-only list markers) with the words of the units minus the headings this reader
adds itself; returns (missing, extra) word counts.
"""
from __future__ import annotations

import copy
import re
import sys
import types
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

sys.modules.setdefault('fetch', types.ModuleType('fetch'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bwb_parse as P  # noqa: E402

OWN_HEADS = {'Aanhef', 'Inhoud', 'Tekst', 'Slotformulering', 'Toelichting'}


def strip_ns(root: ET.Element) -> ET.Element:
    for el in root.iter():
        if isinstance(el.tag, str) and '}' in el.tag:
            el.tag = el.tag.rsplit('}', 1)[1]
    return root


def prepare(el: ET.Element) -> ET.Element:
    """CVDR writes list numbers as li/@nr; the BWB reader reads a <li.nr> child. Images become a visible note."""
    for li in el.iter('li'):
        if li.get('nr') is not None and li.find('li.nr') is None:
            n = ET.Element('li.nr')
            n.text = li.get('nr')
            n.tail = li.text
            li.text = None
            li.insert(0, n)
    # Block children the BWB reader reads as one line (kop label + nr + titel; several <al> in a table cell; names in
    # a signature) get a space between them, as the official page prints them apart.
    for parent in el.iter():
        kids = list(parent)
        for a in kids[:-1]:
            if (a.tag in ('label', 'nr', 'titel', 'al', 'naam', 'functie', 'voornaam', 'achternaam', 'tussenvoegsel')
                    and not (a.tail or '')[:1].isspace()):
                a.tail = ' ' + (a.tail or '')
    for parent in el.iter():
        for i, ch in enumerate(list(parent)):
            if ch.tag == 'illustratie':
                name = ch.get('naam') or ch.get('name') or ''
                al = ET.Element('al')
                al.text = f'[afbeelding{": " + name if name else ""}]'
                al.tail = ch.tail
                parent.remove(ch)
                parent.insert(i, al)
    return el


def flat_unit(key: str, label: str, el: ET.Element) -> dict | None:
    lines = P.flat(list(el))
    if not lines:
        return None
    return {'label': label, 'kind': 'art', 'text': '\n'.join([f'# {label}'] + lines) + '\n'}


def articles(el: ET.Element, prefix: str = '') -> dict:
    """Articles anywhere in el, one unit each (heading + rendered body, as the BWB reader writes them); structural
    headings (hoofdstuk, afdeling, paragraaf ...) and any text outside the articles, in document order, in one
    `inhoud` unit. Without any article the whole of el is one `tekst` unit."""
    if el.find('.//artikel') is None:
        lines = P.flat(list(el))
        return {prefix + 'tekst': {'label': (f'{prefix.rstrip("-").replace("bijlage-", "Bijlage ")}, ' if prefix else '')
                                   + 'Tekst', 'kind': 'art', 'text': '\n'.join(['# Tekst'] + lines) + '\n'}} if lines else {}
    units: dict = {}
    toc: list[str] = []

    def walk(e: ET.Element, depth: int) -> None:
        for ch in e:
            if ch.tag in ('meta-data', 'jcis', 'jci') or ch.tag in P.NOTES:
                continue
            if ch.tag == 'artikel':
                kop = ch.find('kop')
                nr = P.norm(P.inline(kop.find('nr'))) if kop is not None and kop.find('nr') is not None else ''
                key = prefix + (P.article_key(nr, ch.get('label', '')) if nr else 'art-000')
                if key in units:
                    i = 2
                    while f'{key}-{i}' in units:
                        i += 1
                    key = f'{key}-{i}'
                head = P.heading(ch)
                body = P.render(P.strip_notes(ch))
                lab = f'Art. {nr}' if nr else (head or 'Artikel')
                if prefix:
                    lab = f'{prefix.rstrip("-").replace("bijlage-", "Bijlage ")}, {lab}'
                units[key] = {'label': lab, 'kind': 'art',
                              'text': '\n'.join(([f'# {head}'] if head else []) + body) + '\n'}
            elif ch.find('.//artikel') is not None:
                h = P.heading(ch)
                if h:
                    toc.append('#' * min(depth + 2, 6) + ' ' + h)
                if (ch.text or '').strip():
                    toc.append(P.norm(ch.text))
                walk(ch, depth + 1)
            elif ch.tag == 'kop':
                continue  # the heading of the element being walked (already in toc)
            else:
                toc.extend(P.flat([ch]))
    if el.find('kop') is not None and P.heading(el):
        toc.append('## ' + P.heading(el))
    walk(el, 0)
    if toc:
        units[prefix + 'inhoud'] = {'label': (f'{prefix.rstrip("-").replace("bijlage-", "Bijlage ")}, ' if prefix else '')
                                    + 'Inhoud', 'kind': 'contents', 'text': '\n'.join(['# Inhoud'] + toc) + '\n'}
    return units


def read(raw: bytes) -> dict:
    root = prepare(strip_ns(ET.fromstring(raw)))
    body = root.find('body')
    reg = body.find('regeling') if body is not None else None
    units: dict = {}
    if reg is None:
        return units
    nb = 0
    for ch in reg:
        if ch.tag == 'aanhef':
            u = flat_unit('aanhef', 'Aanhef', ch)
            if u:
                units['aanhef'] = u
        elif ch.tag == 'regeling-tekst':
            units.update(articles(ch))
        elif ch.tag == 'regeling-sluiting':
            u = flat_unit('slot', 'Slotformulering', ch)
            if u:
                units['slot'] = u
        elif ch.tag == 'bijlage':
            nb += 1
            if ch.find('.//artikel') is not None:
                units.update(articles(ch, f'bijlage-{nb}-'))
            else:
                u = flat_unit(f'bijlage-{nb}', f'Bijlage {nb}', ch)
                if u:
                    units[f'bijlage-{nb}'] = u
        elif ch.tag == 'nota-toelichting':
            u = flat_unit('toelichting', 'Toelichting', ch)
            if u:
                units['toelichting' if 'toelichting' not in units else f'toelichting-{len(units)}'] = u
        else:
            u = flat_unit(ch.tag, ch.tag, ch)
            if u:
                key = re.sub(r'[^a-z0-9]+', '-', ch.tag.lower()).strip('-') or 'overig'
                units[key] = u
    return units


def words(s: str) -> list[str]:
    return re.findall(r'\w+', P.norm(s).lower())


INLINE = {'vet', 'cursief', 'onderstreept', 'sup', 'sub', 'extref', 'intref', 'nadruk', 'term', 'datum', 'naam',
          'voornaam', 'achternaam', 'functie', 'unl', 'inf', 'super', 'font', 'span', 'a', 'b', 'i', 'u', 'redactie',
          'aanhaling', 'citaat', 'tussenvoegsel', 'deze', 'gegeven', 'dagtekening', 'plaats'}
SKIPV = {'noot', 'voetnoot', 'aanhaling.noot', 'meta-data', 'jcis', 'jci', 'intitule', 'meta'}


def xml_text(el: ET.Element) -> str:
    """All text of el in document order; inline elements run on, every other element is a word boundary."""
    out = []

    def go(e):
        if e.tag in SKIPV:
            return
        sep = '' if e.tag in INLINE else ' '
        out.append(sep)
        if e.tag == 'li' and e.get('nr'):
            out.append(e.get('nr') + ' ')
        if e.tag == 'illustratie':
            out.append(' afbeelding ' + (e.get('naam') or e.get('name') or '') + ' ')
        out.append(e.text or '')
        for ch in e:
            go(ch)
            out.append(ch.tail or '')
        out.append(sep)
    go(el)
    return ''.join(out)


def verify(raw: bytes, units: dict) -> tuple[int, int, list]:
    root = strip_ns(ET.fromstring(raw))
    reg = root.find('body/regeling')
    want: Counter = Counter(words(xml_text(reg))) if reg is not None else Counter()
    have: Counter = Counter()
    for k, u in units.items():
        lines = u['text'].split('\n')
        first = lines[0][2:] if lines[0].startswith('# ') else lines[0]
        if first in OWN_HEADS or re.fullmatch(r'Bijlage \d+', first):
            lines = lines[1:]
        for line in lines:
            have.update(words(line.replace(' | ', ' ')))
    missing = want - have
    extra = have - want
    # Words split or joined at a different place (a boundary between two inline runs) are not lost or added text:
    # they pass only when the missing and the extra words hold exactly the same letters and digits.
    def chars(c: Counter) -> Counter:
        return Counter(x for w, n in c.items() for x in w * n)
    if missing and chars(missing) == chars(extra):
        return 0, 0, ['boundaries', sum(missing.values()), sum(extra.values())]
    return sum(missing.values()), sum(extra.values()), [list(missing.items())[:8], list(extra.items())[:8]]
