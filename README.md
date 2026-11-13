<picture>
<source media="(prefers-color-scheme: dark)" srcset="data/effort-dark.svg">
<img alt="Dutch law in this repository: what it holds, changes by the year they took effect, completeness against the official sources, and the correctness of what is held" src="data/effort-light.svg" width="880">
</picture>

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is the Netherlands' national law, which global-law reads at `netherlands/national/acts/`.


## How the repository is laid out

Every act is a folder `<kind>/<year>/<number>/`, named after its official identifiers, as in [romania-law](https://github.com/lexifina/romania-law) and [japan-law](https://github.com/lexifina/japan-law): the kind the Basiswettenbestand gives the regulation, and the year and number of its original publication (Staatsblad for laws and royal decrees, Staatscourant for the rest; `stb-`/`stcrt-`/`trb-` in front when it appeared in the other gazette). Treaties are `verdrag/<year concluded>/<Treaty database number>/`. Where two acts share a publication number (before 2009 a Staatscourant number is a whole issue) the BWB id is added (`ministeriele-regeling/1995/244-BWBR0007685`); where no publication is known the folder is the BWB id. Inside a folder each article is its own file and `README.md` lists them.

| Folder | Holds | Acts |
| --- | --- | ---: |
| `ministeriele-regeling/` | ministerial regulations (Staatscourant year and number) | 19,708 |
| `zbo/` | regulations of independent bodies (ZBO) | 3,970 |
| `amvb/` | orders in council (AMvB) | 3,656 |
| `verdrag/` | treaties (year concluded, Treaty database number) | 3,349 |
| `wet/` | laws (Staatsblad year and number; wet/1992/315 is the Awb) | 3,204 |
| `pbo/` | regulations of former product boards (PBO) | 2,550 |
| `beleidsregel/` | policy rules | 2,321 |
| `archiefselectielijst/` | archive selection lists (ministerial regulations) | 1,315 |
| `kb/` | royal decrees (KB) | 877 |
| `circulaire/` | circulars | 422 |
| `ministeriele-regeling-bes/` | ministerial regulations for the BES islands | 369 |
| `amvb-bes/` | orders in council for the BES islands | 230 |
| `wet-bes/` | laws for Bonaire, Sint Eustatius and Saba | 185 |
| `rijkswet/` | Kingdom acts (rijkswetten) | 118 |
| `rijkskb/` | Kingdom royal decrees | 85 |
| `reglement/` | reglementen | 50 |
| `beleidsregel-bes/` | policy rules for the BES islands | 20 |
| `rijksamvb/` | Kingdom orders in council | 3 |
| `circulaire-bes/` | circulars for the BES islands | 2 |
| `grondwet/` | the Constitution (grondwet/1815) | 1 |
| `statuut/` | the Charter for the Kingdom (statuut/1954) | 1 |
| `local/<authority>/<year>/<CVDR id>/` | local regulations of provinces, water boards, municipalities and joint arrangements (CVDR) | |
| `data/` | tables: `paths.json` (every act id to its folder), `versions.json`, `laws.csv`, `commits.csv` | |
| `tools/` | the builder and the readers | |

Until 2026-11-13 the acts were folders named by their id at the top level (`awb/`, `grondwet/`). [`data/paths.json`](data/paths.json) maps every old name to its folder, and `git log --follow` follows a file across the move:

```
python -c "import json; print(json.load(open('data/paths.json'))['paths']['awb'])"   # wet/1992/315
git log --follow --oneline -- wet/1992/315/art-01-001.md
```

## What this repository holds, and the plan

[PLAN.md](PLAN.md) lists every part of Dutch law this repository is meant to hold, with what is published so far against the official counts: national legislation from the Basiswettenbestand (every law, order in council, ministerial regulation, independent-body regulation, policy rule and treaty, in force and repealed), local legislation of every municipality, province, water board, joint arrangement and Caribbean public body from the Centrale Voorziening Decentrale Regelgeving (in [local/](local/), one folder per authority), case law (in separate repositories, listed in PLAN.md), and next treaties, EU law and bills. It is regenerated with each documentation commit.

Texts are copied from the official XML as published (wetten.overheid.nl / lokaleregelgeving.overheid.nl, KOOP; free of copyright under Auteurswet art. 11 and released as open data) and checked word for word against it. Each commit is dated the day the text took effect and credited to the publication that made the change.
