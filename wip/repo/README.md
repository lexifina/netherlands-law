# Netherlands: law history in git

The law of the Netherlands as a git history: one file per article, one commit per law on the day it took effect, and the Staatsblad publication that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to an article; `tools/geldend_op.py` (or `tools/on.py`) gives the text in force on any day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `nl/`. Every version is a dated version ("toestand") of the official consolidated text in the [Basiswettenbestand (BWB)](https://wetten.overheid.nl), the database behind wetten.overheid.nl, published by KOOP under CC0.

**What is in it now**

| Folder | Act | BWB id | Versions | History |
| --- | --- | --- | ---: | --- |
| `grondwet/` | [Grondwet](https://wetten.overheid.nl/BWBR0001840) | BWBR0001840 | 11 | 2002-03-21 to 2023-02-22 |
| `bw-boek-1/` | [Burgerlijk Wetboek Boek 1](https://wetten.overheid.nl/BWBR0002656) (persons and family law) | BWBR0002656 | 58 | 2002-01-01 to 2025-07-05 |
| `wetboek-van-strafrecht/` | [Wetboek van Strafrecht](https://wetten.overheid.nl/BWBR0001854) (Criminal Code) | BWBR0001854 | 119 | 2002-04-01 to 2026-07-01 |
| `uavg/` | [Uitvoeringswet Algemene verordening gegevensbescherming](https://wetten.overheid.nl/BWBR0040940) (GDPR Implementation Act) | BWBR0040940 | 6 | 2018-05-25 to 2026-09-01 |

Each history starts at the oldest version the BWB publishes for that act: 2002 for the Grondwet and the two codes, and the act as enacted (Stb. 2018, 144) for the UAVG. Each folder's `README.md` lists every article, how often it changed and when.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did Article 1 of the Grondwet say the day before the 2023 revision? | `python tools/geldend_op.py 2023-02-21 gw 1` |
| And after it? | `python tools/geldend_op.py 2023-02-22 gw 1` |
| The same, with raw git (bash) | `git show $(git rev-list -1 --before="2023-02-22T23:59:59Z" main -- grondwet/art-001.md):grondwet/art-001.md` |
| The same, in PowerShell | `$r = git rev-list -1 --before="2023-02-22T23:59:59Z" main -- grondwet/art-001.md; git show "$($r):grondwet/art-001.md"` |
| Which law wrote each line? | `git blame wetboek-van-strafrecht/art-240.md` |
| Every change, word by word | `git log -p --word-diff wetboek-van-strafrecht/art-240.md` |
| Every law in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one law changed | `git show law/stb-2023-62` (tags `law/<key>` mark each law's commit) |
| The whole act on a date | `python tools/geldend_op.py 01-01-2020 bw1` |
| Which law gave an article its wording on a date | `python tools/geldend_op.py --law 2026-10-29 uavg 23` |

`tools/geldend_op.py` takes dates as `YYYY-MM-DD` or `DD-MM-YYYY`, acts by folder name or abbreviation (`gw`, `bw1`, `sr`, `uavg`), and articles by number (`240`, `19f`, `Artikel 23`) or, for the Grondwet's additional articles, by Roman numeral (`IX`). It is a thin wrapper around `tools/on.py`.

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## Dates

- Each commit is dated at **noon, Europe/Amsterdam, on the day the change took effect**. The day is also in the `In-force:` trailer, which the tools read; the signature (ondertekening) and Staatsblad publication dates are trailers too, where the BWB or officielebekendmakingen.nl gives them.
- **The day is the BWB's.** Each version is a BWB toestand, and its date is the toestand's in-force date (datum_inwerkingtreding), which already applies each law's own commencement provision or Royal Decree. Where a law names no date, the Bekendmakingswet (art. 10(1)) applies: the first day of the second calendar month after publication.
- Laws published but not yet in force go on the branch `toekomst`. On the retrieval day (28 October 2026) there were none.
- `--before="YYYY-MM-DD"` alone uses your clock's time of day, so a law that took effect that day may be missed before noon. Use `T23:59:59Z` as above, or the tools.

## How it is checked

- Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`. Results are in `REPRODUCE.md`.
- **Against wetten.overheid.nl:** `tools/verify.py` reads each act on wetten.overheid.nl as in force on the day it is run and compares it with the last version here. On 29 October 2026 the in-force date the site gives ("Geldend van … t/m heden") equalled the last version of all four acts, and all 1,396 articles matched word for word. The site's only extra entries were placeholders for repealed articles ("Vervallen per …") and UAVG art. 23a, which the BWB marks as not yet in force.
- **Every version is its own dated toestand:** each was parsed from the BWB's XML of exactly that version, whose sha256 is recorded with the version. The BWB manifests were read again on 29 October 2026 and listed no version newer than the ones built here.
- The repository is rebuilt from the same data a second time and must give identical hashes.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist, so `git blame` and `git log --author` name laws. The committer is always Lexifina.

- **Credits come only from the BWB's own notes.** Each article in a BWB toestand names the Staatsblad publication that gave it its current wording (`bron="Stb.2023-62"`) and the day that wording took effect (`inwerking`). A changed article is credited to that publication only when its `inwerking` is the version's day. A repealed article is credited to the publication on its "vervallen" entry, or, if it vanished without one, to the only publication the BWB's amendment record (WTI) lists for that day.
- **Unexplained changes** (5 commits) are committed by the publisher, KOOP, and labelled "unexplained": the table of headings in 2003, 2006 and 2009, BW Boek 1 arts. 263a–263b on 2015-01-01, and nine Criminal Code articles (240a–240c, 248a–248f) on 2024-07-01, which disappeared on a day several laws took effect, none of them named on the articles.
- **Grondwet revisions.** For a revised Grondwet the BWB names as the source of the wording the Besluit that publishes the revised text (Art. 141 Grondwet); that Besluit is the author, and its commit message names the revision laws the BWB lists for the same day. On 2018-12-21 the BWB dates the text before the Besluit of 16 January 2019 (Stb. 2019, 33) that published it; the date is kept as the BWB gives it.
- **The first commit** of the UAVG is the act as enacted (Stb. 2018, 144). For the Grondwet and the codes, it is the oldest version the BWB holds, credited to the publisher.
- Blame credits whole lines (one paragraph, member or list item per line). Use `git log -p --word-diff` to see exactly which words each change made.

## What it does not show

- **History before the BWB.** The BWB's versions start in 2002 (2018 for the UAVG); earlier changes are not separate commits, and the 2002 text is one commit.
- **Repealed and not-yet-in-force articles.** Articles the BWB marks "vervallen" or "nogniet" are absent from the tree, not kept as placeholders.
- **Footnotes and metadata.** They are dropped. Editorial notes (redactie) are kept in square brackets.
- **Headings above the article** (Boek, Titel, Hoofdstuk, Afdeling, Paragraaf) are kept in one `inhoud.md` file per act, not in the article files.
- **BWB versions that change no text** (3, where only metadata or references changed) are not separate versions.

## How it is built

`tools/fetch.py` downloads, per act, the BWB manifest (every dated version), the XML of each version and the WTI (amendment record) from the BWB repository (repository.officiele-overheidspublicaties.nl), plus the metadata of every Staatsblad issue named as a source (zoek.officielebekendmakingen.nl), with curl, at most 3 requests a second, cached by the sha256 of the URL. `tools/parse.py` reads only that cache and writes `corpus.json`: one file per article, dates from each toestand, credits from each article's `bron`. The shared builder `tools/build.py` turns that into the commits. `REPRODUCE.md` lists every source, command, tool version and decision, and the result of the hash-for-hash rebuild.

## Sources

| Source | What it gives | Used for |
| --- | --- | --- |
| [Basiswettenbestand (BWB), wetten.overheid.nl](https://wetten.overheid.nl) | Official consolidated text of every national regulation, as dated versions ("toestanden") in XML, with the source and in-force date of each article; CC0 | The text, dates and credits of every version |
| [officielebekendmakingen.nl](https://zoek.officielebekendmakingen.nl) | The Staatsblad: each publication's title, signature and publication date; CC0 | Naming the laws |
| [bwb2md](https://github.com/PatrickB-Private/bwb2md) (MIT) | A converter from BWB XML to Markdown | Not used; listed as prior art |

General research guides that cover every country: [GlobaLex](https://www.nyulawglobal.org/globalex/) and the [Law Library of Congress Guide to Law Online](https://www.loc.gov/research-centers/law-library-of-congress/researcher-resources/guide-to-law-online/).

## Licence

See [LICENSE](LICENSE). Wet- en regelgeving: Basiswettenbestand (wetten.overheid.nl), KOOP, Ministerie van Binnenlandse Zaken en Koninkrijksrelaties; open data, CC0 1.0. Dutch statutes are also outside copyright (Auteurswet art. 11). Lexifina's arrangement, messages, tables and tools are CC0.

This repository is not legal advice. The authentic text is the one published in the Staatsblad; wetten.overheid.nl is the official consolidation.

## Nederlands

Deze repository bevat Nederlandse wetgeving als git-geschiedenis: één bestand per artikel, één commit per wet op de dag van inwerkingtreding, met de Staatsbladpublicatie die de wijziging aanbracht als auteur van de commit. `git blame` toont per alinea de wet die de tekst gaf; `python tools/geldend_op.py <datum> <wet> [artikel]` toont de tekst die op een dag gold, bijvoorbeeld `python tools/geldend_op.py 21-02-2023 gw 1`.

- **Bron:** het Basiswettenbestand (BWB) achter wetten.overheid.nl (KOOP, CC0). Elke versie is een toestand van de geconsolideerde tekst, gedateerd op de datum van inwerkingtreding die het BWB geeft.
- **Inhoud:** de Grondwet (vanaf 2002), Burgerlijk Wetboek Boek 1 (vanaf 2002), het Wetboek van Strafrecht (vanaf 2002) en de Uitvoeringswet AVG (vanaf de oorspronkelijke tekst, 2018). Eerdere geschiedenis staat niet in het BWB en is niet gereconstrueerd.
- **Toerekening:** een gewijzigd artikel wordt alleen toegeschreven aan de Staatsbladpublicatie die het BWB bij dat artikel als bron noemt, als de inwerkingtredingsdatum daarvan gelijk is aan de dag van de versie. Wat het BWB niet verklaart, staat als "unexplained" op naam van de uitgever.
- **Controle:** elke versie wordt op haar eigen dag en de dag ervoor teruggelezen; de laatste versie van elke wet is op 29 oktober 2026 woord voor woord vergeleken met wetten.overheid.nl (1.396 artikelen, geen verschillen).
- Vervallen artikelen en artikelen die nog niet in werking zijn getreden, staan niet in de boom; wetten die wel zijn gepubliceerd maar nog niet gelden, komen op de branch `toekomst`.

Dit is geen juridisch advies. De authentieke tekst is die in het Staatsblad.
