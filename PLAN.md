# The plan: every source a Dutch lawyer or citizen needs

This is the plan for this repository, part by part, with what is published so far. It is regenerated with each documentation commit, so the gap can be followed over time.

**56.5%** of the plan is published, weighted by how binding each source is and how often it is used. Updated 2026-11-13 02:33 UTC.

| Part | Will be in | Weight | Progress | How | Status |
| --- | --- | ---: | --- | --- | --- |
| **Primary legislation (national, BWB)** | | | | | |
| Grondwet, Statuut, codes and formal laws (wetten, rijkswetten, BES-wetten) | <act>/ (e.g. grondwet/, bw-boek-6/, awb/) | 16.2% | 3,470 of 3,517 acts (2,767 of 2,807 in force) · 98.7% | the BWB XML as published; history from the oldest BWB version for the codes and most-cited laws, current text for the rest | collecting |
| Orders in council (AMvB's, Koninklijke Besluiten) | <act>/ | 9.1% | 4,773 of 4,877 acts (2,505 of 2,584 in force) · 97.9% | the BWB XML as published | collecting |
| Every consolidated version (toestand) of every BWB regulation | versions in each act folder | 8.1% | 70,046 of 148,873 versions · 47.1% | older versions of acts held with their current text only are back-fills: appended as labelled corrections (needs a decision) | planned |
| **Secondary legislation (national, BWB)** | | | | | |
| Ministerial regulations (ministeriële regelingen, incl. BES and archive lists) | <act>/ | 9.1% | 21,389 of 23,176 regulations (8,848 of 9,327 in force) · 92.3% | the BWB XML as published | collecting |
| Regulations of independent bodies (ZBO) and former product boards (PBO) | <act>/ | 3.0% | 6,520 of 7,353 regulations (2,397 of 2,531 in force) · 88.7% | the BWB XML as published | collecting |
| Policy rules, circulars and reglementen | <act>/ | 3.0% | 2,815 of 4,431 documents (1,422 of 1,485 in force) · 63.5% | the BWB XML as published | collecting |
| **Local legislation (CVDR)** | | | | | |
| Provinces (12) | local/provincie-<name>/ | 4.0% | 0 of 9,697 regulations; 0 of 12 authorities; 0 of 17,188 versions · 0.0% | CVDR XML (lokaleregelgeving.overheid.nl), every consolidated version, checked word for word | starting |
| Water boards (21 today, 29 with former boards) | local/<water board>/ | 2.0% | 0 of 4,882 regulations; 0 of 29 authorities; 0 of 6,941 versions · 0.0% | CVDR XML (lokaleregelgeving.overheid.nl), every consolidated version, checked word for word | starting |
| Municipalities (342 today, 457 with merged former municipalities) | local/gemeente-<name>/ | 14.1% | 0 of 256,270 regulations; 0 of 457 authorities; 0 of 303,613 versions · 0.0% | CVDR XML (lokaleregelgeving.overheid.nl), every consolidated version, checked word for word | starting |
| Joint arrangements (gemeenschappelijke regelingen) | local/regio-<name>/ | 1.5% | 0 of 8,634 regulations; 0 of 270 authorities; 0 of 10,394 versions · 0.0% | CVDR XML (lokaleregelgeving.overheid.nl), every consolidated version, checked word for word | starting |
| Caribbean Netherlands (Bonaire, Saba, Sint Eustatius) and Curaçao, Sint Maarten, the former Netherlands Antilles | local/openbaar-lichaam-<island>/, local/land-<country>/, local/nederlandse-antillen/ | 1.0% | 0 of 5,439 regulations; 0 of 6 authorities; 0 of 6,243 versions · 0.0% | CVDR XML (lokaleregelgeving.overheid.nl), every consolidated version, checked word for word | starting |
| Former Amsterdam boroughs (deelgemeenten) | local/deelgemeente-<name>/ | 0.2% | 0 of 959 regulations; 0 of 7 authorities; 0 of 1,220 versions · 0.0% | CVDR XML (lokaleregelgeving.overheid.nl), every consolidated version, checked word for word | starting |
| **Case law** | | | | | |
| Court decisions (Rechtspraak open data): Hoge Raad, Raad van State, CRvB, CBb, courts of appeal, district courts | 15 separate repositories (see below) | 12.1% | 932,076 commits in 15 repositories; 974,751 ECLIs with a document at data.rechtspraak.nl · 95.6% | one commit per decision, dated the day decided (separate repositories) | collecting |
| **Treaties and EU** | | | | | |
| Treaties (BWB treaty texts, Tractatenblad) | <treaty>/ | 3.0% | 1,371 of 3,706 treaties in the BWB · 37.0% | the BWB treaty XML as published; Tractatenblad references next | collecting |
| EU law in Dutch and transposition links | eu/, data/eu-transposition.csv | 3.0% | target being counted · 0.0% | EUR-Lex Dutch texts and national transposition measures | planned |
| **Parliament, gazettes, oversight** | | | | | |
| Staatsblad / Staatscourant references | Law: and Source: trailers of each commit | 2.0% | the amending publication named on every credited commit (40,338 of 47,060 BWB regulations held); gazette texts themselves not yet · 85.7% | the BWB amendment records (WTI); officielebekendmakingen.nl | collecting |
| Bills and parliamentary papers (Kamerstukken), drafts in consultation (labelled "not law") | wetsvoorstel/, consultatie/ | 2.5% | target being counted · 0.0% | officielebekendmakingen.nl Kamerstukken; internetconsultatie.nl | planned |
| Raad van State advisory opinions on bills | advies-raad-van-state/ | 1.0% | target being counted · 0.0% | raadvanstate.nl / Kamerstukken | planned |
| Oversight: Nationale ombudsman, Algemene Rekenkamer, Kiesraad | toezicht/<body>/ | 1.0% | target being counted · 0.0% | each body's own publications | planned |
| **Historical law** | | | | | |
| Repealed and expired regulations (national and local) | in the same folders, with a repeal commit | 3.8% | 21,028 of 24,729 expired BWB regulations; 0 of 185,341 expired CVDR regulations · 10.0% | last version, then a commit removing the text | collecting |

Progress counts what is on `main`; targets are the official counts: the BWB's own SRU listing (47,060 regulation ids, 148,873 versions), the CVDR's SRU listing (285,881 regulations of every Dutch municipality, province, water board, joint arrangement and Caribbean public body, 345,599 versions) and data.rechtspraak.nl's ECLI count. 0 CVDR regulations are held back because their text did not pass the word-for-word check; they are retried after reader fixes.

## Case law

Court decisions are kept in separate repositories, one commit per decision:

- [lexifina/netherlands-gerechtshoven-caselaw](https://github.com/lexifina/netherlands-gerechtshoven-caselaw): 168,520 commits
- [lexifina/netherlands-rechtbanken-den-haag-caselaw](https://github.com/lexifina/netherlands-rechtbanken-den-haag-caselaw): 123,134 commits
- [lexifina/netherlands-raad-van-state-caselaw](https://github.com/lexifina/netherlands-raad-van-state-caselaw): 100,820 commits
- [lexifina/netherlands-centrale-raad-van-beroep-caselaw](https://github.com/lexifina/netherlands-centrale-raad-van-beroep-caselaw): 87,927 commits
- [lexifina/netherlands-hoge-raad-caselaw](https://github.com/lexifina/netherlands-hoge-raad-caselaw): 80,524 commits
- [lexifina/netherlands-rechtbanken-rotterdam-caselaw](https://github.com/lexifina/netherlands-rechtbanken-rotterdam-caselaw): 55,523 commits
- [lexifina/netherlands-rechtbanken-zeeland-west-brabant-caselaw](https://github.com/lexifina/netherlands-rechtbanken-zeeland-west-brabant-caselaw): 52,698 commits
- [lexifina/netherlands-rechtbanken-midden-nederland-caselaw](https://github.com/lexifina/netherlands-rechtbanken-midden-nederland-caselaw): 52,490 commits
- [lexifina/netherlands-rechtbanken-amsterdam-caselaw](https://github.com/lexifina/netherlands-rechtbanken-amsterdam-caselaw): 46,962 commits
- [lexifina/netherlands-rechtbanken-noord-holland-caselaw](https://github.com/lexifina/netherlands-rechtbanken-noord-holland-caselaw): 41,621 commits
- [lexifina/netherlands-rechtbanken-gelderland-caselaw](https://github.com/lexifina/netherlands-rechtbanken-gelderland-caselaw): 37,168 commits
- [lexifina/netherlands-rechtbanken-overijssel-caselaw](https://github.com/lexifina/netherlands-rechtbanken-overijssel-caselaw): 23,919 commits
- [lexifina/netherlands-rechtbanken-limburg-caselaw](https://github.com/lexifina/netherlands-rechtbanken-limburg-caselaw): 23,416 commits
- [lexifina/netherlands-overige-caselaw](https://github.com/lexifina/netherlands-overige-caselaw): 21,429 commits
- [lexifina/netherlands-college-van-beroep-caselaw](https://github.com/lexifina/netherlands-college-van-beroep-caselaw): 15,925 commits
