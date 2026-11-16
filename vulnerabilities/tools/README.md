# Tools

The scripts behind this Netherlands-only run of global-law's vulnerability detectors. They run inside a copy of
[global-law/vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts) (Python 3.11+,
`pip install duckdb pyarrow`), with a bare clone of this repository at `sources/corpus/netherlands-law.git`, a blobless bare
clone of global-law at `sources/global-law.git`, and a `pins.json` that names only netherlands-law, its commit, its language
(`nl`) and its code (`NL`). `build_vulns.py`, `flags_chart.py`, `late_ext_select.py`, `late_ext_rebut.py`, `hist.py` and
`config.json` sit three folders up, next to the copy of global-law (`gl/vulnerabilities/scripts/`).

| Script | What it does |
| --- | --- |
| `run.sh` | Indexes the history and texts, maps the history to the act folders since the move, adds this repository's history rows, and runs the detectors (`bash run.sh <shards>`) |
| `map_moved.py` | This repository moved its acts from folders named by id (`bw-boek-7/`) to `<kind>/<year>/<number>/` on 13 November 2026; using `data/paths.json` at the pin, it rewrites the paths in the history table to each act's folder since the move, so an act's history is not split in two (here 42,436 folders, 2,130,845 paths) |
| `add_root.py` | Builds the history rows from this repository's own commits, so the history detectors read every change; unchanged here: the `Kind:` values this repository uses (`law`, `decree`, `publisher`) are already among those that count as law, and all 65,701 dated commits do |
| `run_triage.sh` | The model review: the 40 strongest flags per category, the 40 strongest lapsed time limits in law texts, and the empty periods |
| `rerun_refs.sh` | The second round of `patch_nl.py`: the reference scan again, the three detectors that read it, and the model review of references to deleted provisions only (earlier reviews of the other categories kept) |
| `late_ext_select.py` | Chooses the empty periods for global-law's review of that category: those whose old and new dates open the same sentence (here 5), and, below 40, the shortest of the rest (here all 19) |
| `late_ext_rebut.py` | Adds the second, arguing-against pass to the empty-period review, as `triage.py` does for the other categories |
| `build_vulns.py` | Builds `data/flags.csv`, `data/reviewed.csv` and `data/by_category.csv` from the findings and the model review |
| `flags_chart.py` | Draws the chart at the top of the READMEs, in Dutch and English, light and dark |
| `config.json` | The repository, the Dutch category names, the folders and files that are not law (circulars, tables of contents, README files, `data/`, `tools/`), and the chart's labels |
| `hist.py` | The hand check: one file's full history across the move, with each change's in-force date, act and diff (`python -X utf8 hist.py <path> --diff`), a commit's trailers and files (`--commit <sha>`), and a search of the text at the pin (`--grep <regex> <folder>`) |
| `patch_detectors.py` | Fixes blind spots found in runs on several country repositories in the copy of global-law's scripts (`python -X utf8 patch_detectors.py <scripts dir>`; a fix already in place is skipped) |
| `patch_nl.py` | The Dutch fixes found by this run (below) |
| `patch_detectors_vi.py`, `patch_es.py`, `patch_ca.py`, `patch_en.py`, `patch_de.py`, `patch_en_et.py`, `patch_co.py`, `patch_sv.py`, `patch_pt.py`, `patch_ru.py`, `patch_r18.py`, `patch_xk.py`, `patch_mo.py`, `patch_lu.py`, `patch_li.py`, `patch_mx.py`, `patch_mn.py`, `patch_mt.py`, `patch_np.py`, `patch_en_nr.py`, `patch_dv.py`, `patch_az.py` | The same for other languages and countries (found by other runs); applied here before the run, they change little or nothing in Dutch text, but `redo.py` runs them on every repository |
| `apply_patches.py` | Runs the patches above once each, in a fixed order (`patch_nl.py` last), and records them in the scripts folder (`.kit_patches.json`) |
| `redo.py` | Runs the patches, then again only the scans and detectors the fixes change, the model review of lapsed time limits, references to deleted provisions and empty periods, and the build (`python -X utf8 redo.py <run folder> [--keep-reviews] [--full]`; `--keep-reviews` keeps every review already made and reviews only new strong flags; `--full` runs every step again through `run.sh`, sends every category to the model and keeps every review already made; `EMBED_FONTS` names the script that embeds the chart's fonts) |

The model review needs `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` and `LLM_AUTH` set for an OpenAI-compatible Responses API.
`run_triage.sh` was given the circulars (`circulaire/`, `circulaire-bes/`), `data/`, `tools/`, the tables of contents
(`inhoud.md`) and the README files as the files that are not law.

## Changes made for this repository

`patch_nl.py` (markers that survive later edits; `apply_patches.py` runs it after all the others). Its first round was applied
before the full run, its second through `rerun_refs.sh`, its third and fourth by running the currency scan, the placeholder
detector and the dead-fine detector again. After the second round the references to deleted provisions were reviewed again;
the third and fourth touch only categories the model does not review. `patch_ar.py`, `patch_en_nz.py`, `patch_nb.py`,
`patch_mk.py` and `patch_pa.py` were written for other runs after this one and were not applied.

- `ingest/textscan.py`: a date written with hyphens was read month first, the US order ("12-01-2020" as 1 December), so a day
  above 12 was dropped and the rest were read with day and month swapped; for `nl` the two are swapped back ("t/m
  31-12-2025"). And "tot" after "terug" is retroactive effect, not a time limit ("Artikel I werkt terug tot en met 1 januari
  2013", "met terugwerkende kracht tot 1 januari 2011"). Lapsed time limits went from 9,465 to 6,454.
- `ingest/refscan.py` (read by the reference, placeholder and dead-fine detectors): another act named after the reference
  and its subunits ("artikel 15, eerste lid, van de Wet minimumloon", "artikel 9 van de wet" in an order in council,
  "artikel 12 van Verordening (EU) 2023/2405") was read as an article of the citing act, and "artikel 3.3" or "artikel
  7:670" (chapter or book, then article) as article 3 or 7. A second round, after the hand check: "2.134" read as the
  number 2134, a list of numbers and subunits longer than the 70 characters read after a reference ("de artikelen 43,
  tweede lid, 53, tweede lid, tweede volzin en 55b, tweede lid, van de Woningwet"), and "van de kaderrichtlijn
  afvalstoffen". References to deleted provisions went from 1,106 to 462, then 373.
- `detectors/placeholder_ref.py`: an article that withdraws another act or sets the act's own end ("De Wet personenvervoer
  wordt ingetrokken.", "Deze regeling vervalt met ingang van 1 augustus 2027.") was read as a placeholder. A fourth round,
  after reading a sample: Dutch uses "vervalt" (lapses) and "vervallen" in ordinary text ("Het auteursrecht vervalt door
  verloop van 70 jaren", art. 37 Auteurswet), and any article of 400 characters or less with the word near its start was
  read as one; a placeholder is now the word alone ("[Vervallen]", "Vervallen.", "[Vervallen door vernummering.]").
  References to “vervallen” articles went from 631 to 153 in the first two rounds, then 91; dead fines stayed at 3.
- `detectors/currency_scan.py`: the Dutch guilder, replaced by the euro on 1 January 2002, was not read at all; for the code
  `NL` it is now read as "100 gulden", "ƒ 1.000", "f 26,50", "fl. 200,-", "Hfl. 500" and "NLG 50.000", not as "f1" (a
  factor or an item), "f 2°" (an item), or the guilders and florins of the Caribbean parts of the Kingdom ("Antilliaanse
  gulden", "Caribische gulden", "Arubaanse florin", "NAf.", "Afl.") and Suriname. In Dutch "kroon" is a crown, not the
  Estonian kroon. A third round, after the hand check: the two 2010 tariff regulations for Curaçao and Sint Maarten (under the
  Schepenwet and for fishing vessels) write their Antillean guilders "f 305,–"; a guilder form in an act whose README title
  names Curaçao, Sint Maarten, Aruba, the Antilles, the Caribbean Netherlands, Bonaire, Sint Eustatius or Saba is left out
  (99 flags). Dead currencies went from 71 to 1,673, then 1,574.

Not changed, and stated in the EDGE-CASES: the reference scan still stops at a word it does not expect in a list of subunits
("eerste tot en met het zesde lid", "veertigste, onderscheidenlijk eenenveertigste, lid"), so an EU regulation or directive
named after such a list is read as the citing act; ranges ("de artikelen 126 tot en met 137") count every number in them;
`notes_scan.py` reads the words "niet uitvoerbaar" (not practicable) as a publisher's note, though in Dutch law text they are
the law's own words; `dup_labels.py` reads table rows that begin with an article ("Artikel 23, eerste lid, onderdeel a |
…") as numbered units; and the history detectors read a local regulation's file as one provision, though its files are
numbered by position and hold different articles over time.
