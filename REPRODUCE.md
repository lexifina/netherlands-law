# How this repository was made (Netherlands)

This file is written by the build on 2026-10-28, the day the source data was retrieved. Everything below is enough to rebuild this repository hash for hash.

## Sources

| Source | Address | Retrieved | Requests | Licence |
| --- | --- | --- | ---: | --- |
| Basiswettenbestand (BWB), wetten.overheid.nl | <https://repository.officiele-overheidspublicaties.nl/bwb/> | 2026-10-28 | 537 | CC0 1.0 |
| officielebekendmakingen.nl (Staatsblad metadata) | <https://zoek.officielebekendmakingen.nl/> | 2026-10-28 | None | CC0 1.0 |

Every response is cached by the sha256 of its URL, and the table above lists every source with its retrieval date. Lexifina keeps its fetch scripts privately; `tools/parse.py` reads only the cache and writes `corpus.json`, so the same cache always gives the same corpus.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `grondwet` | Grondwet | 11 | 2002-03-21 to 2023-02-22 |
| `bw-boek-1` | Burgerlijk Wetboek Boek 1 | 58 | 2002-01-01 to 2025-07-05 |
| `wetboek-van-strafrecht` | Wetboek van Strafrecht | 119 | 2002-04-01 to 2026-07-01 |
| `uavg` | Uitvoeringswet Algemene verordening gegevensbescherming | 6 | 2018-05-25 to 2026-09-01 |

The build made 281 commits:

| Commits | Kind |
| ---: | --- |
| 4 | first version of an act |
| 272 | one law on its in-force day |
| 5 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `toekomst`: laws not yet in force on 2026-10-28.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 248 laws in the record.
- 442 tags.

## Dates

Each commit is dated at noon (Europe/Amsterdam) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Bekendmakingswet art. 10(1): where a law names no date, it takes effect on the first day of the second calendar month after its publication. Every version here carries the BWB's own in-force date (datum_inwerkingtreding), which already applies each law's own commencement. https://wetten.overheid.nl/jci1.3:c:BWBR0004287&artikel=10

## Commands, in order

```sh
# fill the cache from the sources listed above (network; Lexifina's fetch scripts are kept privately)
python -X utf8 tools/parse.py                  # cache -> corpus.json (no network)
python -X utf8 tools/build.py <folder> --repo <empty folder> --docs-date 2026-10-28
python -X utf8 tools/check_repo.py <repo> --corpus <folder>/corpus.json --write
python -X utf8 tools/build.py <folder> --repo <another empty folder> --docs-date 2026-10-28 --compare <repo>
```

In the main Lexifina repository these files live as follows:
- `fetch.py`, `parse.py` and `repo/`: in `scripts/netherlands-law/`.
- `build.py`, `check_repo.py` (`check.py` there) and `on.py`: in `scripts/gitlaw_common/`, with the corpus format in `SCHEMA.md`.

## Exact inputs

- `corpus.json` sha256 `2b6524d20d6f0b546e81cb0df1c9dcd428227143ebdffb3faab2edae455a9359` (3354156 bytes)
- Script blob hashes (`git hash-object`):

| Script | Blob |
| --- | --- |
| build.py | `833a2433a3ea96fd87477ccc7a2ed47dc9e24b48` |
| check.py | `426d4cfb32ce103715be6a00865c0a7bca81a56a` |
| on.py | `644a6c0857fbcc72562032b58d57aa113fee0641` |
| fetch.py | `b592f7d2b451d61cf53b6d184103ca7c091c28cf` |
| parse.py | `ddbc47543b6f6dc0e158ac14777940805355cc84` |

- Tools:
  - Python 3.14.0
  - git version 2.52.0.windows.1
  - curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 WinIDN WinLDAP

## Checks

194 versions of 4 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

Not yet run for this build.

These results are from the check run on the build before this one, from the same corpus.

## Decisions made by hand

- Acts: the Grondwet, Burgerlijk Wetboek Boek 1, the Wetboek van Strafrecht and the UAVG (Phase 1), chosen because the BWB holds dated versions for each.
- History starts at the oldest version the BWB holds for each act (2002 for the codes and the Grondwet, 2018 for the UAVG); earlier history is not reconstructed.
- Only versions still visible in the BWB manifest (zichtdatum_eind 9999-12-31) are used; where the BWB re-issued a day as _1, the _1 replaces the _0.
- Each version is dated by the BWB's datum_inwerkingtreding, the day it took effect.
- A changed article is credited to the Staatsblad publication the BWB names on that article (bron), only when the article's own inwerking date equals the version's day; otherwise it is left unexplained.
- A removed article is credited to the bron on its "vervallen" entry; if it vanished without one, to the only Staatsblad issue the WTI lists for that day, if there is exactly one.
- Articles marked "vervallen" (repealed) or "nogniet" (not yet in force) are absent from the tree; the BWB's "Vervallen" placeholders are not kept as text.
- Editorial notes (redactie) are kept in square brackets; footnotes and metadata are dropped.
- Headings of Boeken, Titels, Hoofdstukken, Afdelingen and Paragrafen are kept in one inhoud unit per act, credited to the bron of the headings that took effect that day.
- Law kind: a Staatsblad title starting "Besluit" is a decree; everything else is a law.
- Grondwet 2018-12-21: the BWB credits the text to Stb. 2019, 33 (the Besluit of 16 January 2019 publishing the revised Grondwet, Art. 141 Gw) with in-force date 2018-12-21, before that Besluit was signed; the in-force date is kept as the BWB gives it.
- bw-boek-1: 2 BWB version(s) change no rendered text (only metadata or references) and are not separate versions here.
- wetboek-van-strafrecht: 1 BWB version(s) change no rendered text (only metadata or references) and are not separate versions here.

## What AI did and did not do

The fetch, parse and check scripts were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above, through code that anyone can rerun.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none: no model wrote, summarised or classified any text in this corpus. The parser was written by Claude Code (claude-opus-5-5).
