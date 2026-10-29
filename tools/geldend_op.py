"""Prints Dutch law as it was in force ("geldend op") on a given day, read from this repository's history.

    python tools/geldend_op.py 2026-10-29 gw 23          # Grondwet art. 23 today
    python tools/geldend_op.py 01-01-2019 gw IX          # additional article IX of the Grondwet (add-art-09)
    python tools/geldend_op.py 2024-06-30 sr 240a        # Wetboek van Strafrecht art. 240a, the day before 1 July 2024
    python tools/geldend_op.py 2020-01-01 bw1            # the whole of Boek 1 BW on 1 January 2020
    python tools/geldend_op.py --law 2026-09-01 uavg 23  # also name the Staatsblad publication behind that wording

A thin wrapper around tools/on.py: the version is chosen by each commit's `In-force:` trailer, never by its commit
date. It only translates Dutch usage into on.py's arguments:
- dates as YYYY-MM-DD or DD-MM-YYYY;
- the act by folder name or abbreviation: gw (grondwet), bw1 / bw-1 (bw-boek-1; likewise bw2-bw7, bw10),
  sr (wetboek-van-strafrecht), sv (wetboek-van-strafvordering), rv (wetboek-van-burgerlijke-rechtsvordering), awb,
  aw (auteurswet), wvk (wetboek-van-koophandel), uavg, or any folder name;
- the article as a number ("23", "240a", "Artikel 23", "art. 23") or, for the Grondwet's additional articles, a Roman
  numeral ("IX"), or chapter-numbered ("4:84a" in the Awb); "Algemene bepaling" (the Grondwet's unnumbered article) is art-000.
Standard library only.
"""
import re
import runpy
import sys
from pathlib import Path

ACTS = {'gw': 'grondwet', 'grondwet': 'grondwet', 'bw1': 'bw-boek-1', 'bw-1': 'bw-boek-1', 'bw-boek-1': 'bw-boek-1',
        'sr': 'wetboek-van-strafrecht', 'wvsr': 'wetboek-van-strafrecht', 'wetboek-van-strafrecht': 'wetboek-van-strafrecht',
        'uavg': 'uavg',
        'sv': 'wetboek-van-strafvordering', 'wetboek-van-strafvordering': 'wetboek-van-strafvordering',
        'rv': 'wetboek-van-burgerlijke-rechtsvordering',
        'wetboek-van-burgerlijke-rechtsvordering': 'wetboek-van-burgerlijke-rechtsvordering',
        'awb': 'awb', 'aw': 'auteurswet', 'wvk': 'wetboek-van-koophandel'}
for _n in (2, 3, 4, 5, 6, 7, 10):
    ACTS[f'bw{_n}'] = ACTS[f'bw-{_n}'] = ACTS[f'bw-boek-{_n}'] = f'bw-boek-{_n}'
ROMAN = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}


def day(s: str) -> str:
    m = re.fullmatch(r'(\d{1,2})-(\d{1,2})-(\d{4})', s)
    return f'{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}' if m else s


def roman(s: str) -> int | None:
    if not re.fullmatch(r'[IVXLC]+', s):
        return None
    total = 0
    for a, b in zip(s, s[1:] + ' '):
        v = ROMAN[a]
        total += -v if b != ' ' and ROMAN[b] > v else v
    return total


def unit(s: str) -> str:
    s = re.sub(r'^(artikel|art\.?)\s*', '', s.strip(), flags=re.I).strip()
    if s.lower() in ('algemene bepaling', 'algemene-bepaling'):
        return 'art-000'
    r = roman(s)
    if r:
        return f'add-art-{r:02d}'
    m = re.fullmatch(r'(\d+)\s*([a-z]*)', s.lower())
    if m:
        return f'art-{int(m.group(1)):03d}{m.group(2)}'
    parts = re.split(r'\s*[.:]\s*', s.lower())
    if len(parts) > 1 and all(p.isdigit() for p in parts[:-1]) and re.fullmatch(r'\d+[a-z]*', parts[-1]):
        # chapter-numbered articles: Awb 4:84a -> art-04-084a, Sv 5.3.10 -> art-05-03-010
        pads = [2] * (len(parts) - 1) + [3]
        return 'art-' + '-'.join(re.sub(r'^\d+', lambda d: str(int(d.group())).zfill(w), p)
                                 for p, w in zip(parts, pads))
    return s


if __name__ == '__main__':
    law = '--law' in sys.argv[1:]
    args = [a for a in sys.argv[1:] if a != '--law']
    if not args:
        sys.exit(__doc__)
    args[0] = day(args[0])
    if len(args) > 1:
        args[1] = ACTS.get(args[1].lower(), args[1])
    if len(args) > 2:
        args[2:] = [unit(' '.join(args[2:]))]
    sys.argv = [str(Path(__file__).with_name('on.py'))] + (['--law'] if law else []) + args
    runpy.run_path(sys.argv[0], run_name='__main__')
