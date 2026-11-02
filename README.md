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
| `bw-boek-2/` | [Burgerlijk Wetboek Boek 2](https://wetten.overheid.nl/BWBR0003045) (legal persons, companies) | BWBR0003045 | 87 | 2002-04-23 to 2026-07-01 |
| `bw-boek-3/` | [Burgerlijk Wetboek Boek 3](https://wetten.overheid.nl/BWBR0005291) (property law, general) | BWBR0005291 | 47 | 2002-01-01 to 2025-07-01 |
| `bw-boek-4/` | [Burgerlijk Wetboek Boek 4](https://wetten.overheid.nl/BWBR0002761) (succession) | BWBR0002761 | 18 | 2002-01-01 to 2025-07-01 |
| `bw-boek-5/` | [Burgerlijk Wetboek Boek 5](https://wetten.overheid.nl/BWBR0005288) (real rights) | BWBR0005288 | 13 | 2002-01-01 to 2024-01-01 |
| `bw-boek-6/` | [Burgerlijk Wetboek Boek 6](https://wetten.overheid.nl/BWBR0005289) (obligations and contracts, tort) | BWBR0005289 | 63 | 2002-04-12 to 2026-07-16 |
| `bw-boek-7/` | [Burgerlijk Wetboek Boek 7](https://wetten.overheid.nl/BWBR0005290) (specific contracts: sale, lease, employment, ...) | BWBR0005290 | 131 | 2002-04-01 to 2026-10-08 |
| `bw-boek-10/` | [Burgerlijk Wetboek Boek 10](https://wetten.overheid.nl/BWBR0030068) (private international law) | BWBR0030068 | 16 | 2012-01-01 to 2026-07-01 |
| `wetboek-van-strafvordering/` | [Wetboek van Strafvordering](https://wetten.overheid.nl/BWBR0001903) (Code of Criminal Procedure) | BWBR0001903 | 126 | 2002-03-08 to 2026-07-01 |
| `wetboek-van-burgerlijke-rechtsvordering/` | [Wetboek van Burgerlijke Rechtsvordering](https://wetten.overheid.nl/BWBR0001827) (Code of Civil Procedure) | BWBR0001827 | 97 | 2002-01-01 to 2026-07-14 |
| `awb/` | [Algemene wet bestuursrecht](https://wetten.overheid.nl/BWBR0005537) (General Administrative Law Act) | BWBR0005537 | 151 | 2002-04-01 to 2026-08-15 |
| `auteurswet/` | [Auteurswet](https://wetten.overheid.nl/BWBR0001886) (Copyright Act) | BWBR0001886 | 28 | 2002-01-01 to 2026-01-01 |
| `wft/` | [Wet op het financieel toezicht](https://wetten.overheid.nl/BWBR0020368) (Financial Supervision Act) | BWBR0020368 | 132 | 2007-01-01 to 2026-09-29 |
| `omgevingswet/` | [Omgevingswet](https://wetten.overheid.nl/BWBR0037885) (Environment and Planning Act) | BWBR0037885 | 6 | 2024-01-01 to 2026-07-01 |
| `vreemdelingenwet-2000/` | [Vreemdelingenwet 2000](https://wetten.overheid.nl/BWBR0011823) (Aliens Act 2000) | BWBR0011823 | 67 | 2002-01-01 to 2026-10-16 |
| `wet-arbeid-vreemdelingen/` | [Wet arbeid vreemdelingen](https://wetten.overheid.nl/BWBR0007149) (Foreign Nationals Employment Act) | BWBR0007149 | 30 | 2002-01-01 to 2026-06-12 |
| `participatiewet/` | [Participatiewet](https://wetten.overheid.nl/BWBR0015703) (Participation Act (social assistance)) | BWBR0015703 | 106 | 2004-01-01 to 2026-07-01 |
| `zorgverzekeringswet/` | [Zorgverzekeringswet](https://wetten.overheid.nl/BWBR0018450) (Health Insurance Act) | BWBR0018450 | 62 | 2006-01-01 to 2026-01-01 |
| `jeugdwet/` | [Jeugdwet](https://wetten.overheid.nl/BWBR0034925) (Youth Act) | BWBR0034925 | 30 | 2014-03-15 to 2026-01-01 |
| `wmo-2015/` | [Wet maatschappelijke ondersteuning 2015](https://wetten.overheid.nl/BWBR0035362) (Social Support Act 2015) | BWBR0035362 | 27 | 2014-07-19 to 2026-07-01 |
| `wet-langdurige-zorg/` | [Wet langdurige zorg](https://wetten.overheid.nl/BWBR0035917) (Long-term Care Act) | BWBR0035917 | 30 | 2014-10-01 to 2026-01-01 |
| `wet-inkomstenbelasting-2001/` | [Wet inkomstenbelasting 2001](https://wetten.overheid.nl/BWBR0011353) (Income Tax Act 2001) | BWBR0011353 | 100 | 2002-04-01 to 2026-02-21 |
| `wet-omzetbelasting-1968/` | [Wet op de omzetbelasting 1968](https://wetten.overheid.nl/BWBR0002629) (VAT Act 1968) | BWBR0002629 | 43 | 2002-01-01 to 2026-01-01 |
| `awr/` | [Algemene wet inzake rijksbelastingen](https://wetten.overheid.nl/BWBR0002320) (General Tax Act) | BWBR0002320 | 77 | 2002-04-01 to 2026-10-01 |
| `opiumwet/` | [Opiumwet](https://wetten.overheid.nl/BWBR0001941) (Opium Act) | BWBR0001941 | 27 | 2002-03-01 to 2026-07-09 |
| `wegenverkeerswet-1994/` | [Wegenverkeerswet 1994](https://wetten.overheid.nl/BWBR0006622) (Road Traffic Act 1994) | BWBR0006622 | 97 | 2002-01-01 to 2026-09-01 |
| `wet-politiegegevens/` | [Wet politiegegevens](https://wetten.overheid.nl/BWBR0022463) (Police Data Act) | BWBR0022463 | 18 | 2008-01-01 to 2026-09-01 |
| `gemeentewet/` | [Gemeentewet](https://wetten.overheid.nl/BWBR0005416) (Municipalities Act) | BWBR0005416 | 91 | 2002-03-07 to 2026-06-04 |
| `wet-open-overheid/` | [Wet open overheid](https://wetten.overheid.nl/BWBR0045754) (Open Government Act) | BWBR0045754 | 4 | 2022-05-01 to 2025-02-12 |
| `wet-rechterlijke-organisatie/` | [Wet op de rechterlijke organisatie](https://wetten.overheid.nl/BWBR0001830) (Judiciary Organisation Act) | BWBR0001830 | 43 | 2002-01-01 to 2025-07-01 |
| `woningwet/` | [Woningwet](https://wetten.overheid.nl/BWBR0005181) (Housing Act) | BWBR0005181 | 72 | 2002-01-01 to 2026-07-01 |
| `faillissementswet/` | [Faillissementswet](https://wetten.overheid.nl/BWBR0001860) (Bankruptcy Act) | BWBR0001860 | 71 | 2002-01-01 to 2026-09-01 |
| `arbeidsomstandighedenwet/` | [Arbeidsomstandighedenwet](https://wetten.overheid.nl/BWBR0010346) (Working Conditions Act) | BWBR0010346 | 32 | 2002-04-01 to 2026-07-01 |
| `wetboek-van-koophandel/` | [Wetboek van Koophandel](https://wetten.overheid.nl/BWBR0001838) (Commercial Code) | BWBR0001838 | 15 | 2002-04-01 to 2025-07-01 |
| `wet-milieubeheer/` | [Wet milieubeheer](https://wetten.overheid.nl/BWBR0003245) (Environmental Management Act) | BWBR0003245 | 128 | 2002-04-01 to 2026-10-22 |
| `wet-loonbelasting-1964/` | [Wet op de loonbelasting 1964](https://wetten.overheid.nl/BWBR0002471) (Wage Tax Act 1964) | BWBR0002471 | 59 | 2002-04-01 to 2026-10-08 |
| `wet-vennootschapsbelasting-1969/` | [Wet op de vennootschapsbelasting 1969](https://wetten.overheid.nl/BWBR0002672) (Corporate Income Tax Act 1969) | BWBR0002672 | 63 | 2002-01-01 to 2026-01-01 |
| `successiewet-1956/` | [Successiewet 1956](https://wetten.overheid.nl/BWBR0002226) (Inheritance and Gift Tax Act 1956) | BWBR0002226 | 32 | 2002-01-01 to 2026-01-01 |
| `wet-op-het-notarisambt/` | [Wet op het notarisambt](https://wetten.overheid.nl/BWBR0010388) (Notaries Act) | BWBR0010388 | 48 | 2002-01-01 to 2024-01-01 |
| `advocatenwet/` | [Advocatenwet](https://wetten.overheid.nl/BWBR0002093) (Lawyers Act) | BWBR0002093 | 36 | 2002-01-01 to 2026-01-01 |
| `werkloosheidswet/` | [Werkloosheidswet](https://wetten.overheid.nl/BWBR0004045) (Unemployment Insurance Act) | BWBR0004045 | 83 | 2002-04-01 to 2026-10-08 |
| `wet-wia/` | [Wet werk en inkomen naar arbeidsvermogen](https://wetten.overheid.nl/BWBR0019057) (Work and Income (Capacity for Work) Act) | BWBR0019057 | 65 | 2005-12-09 to 2026-07-01 |
| `algemene-ouderdomswet/` | [Algemene Ouderdomswet](https://wetten.overheid.nl/BWBR0002221) (General Old Age Pensions Act) | BWBR0002221 | 67 | 2002-01-01 to 2026-07-01 |
| `wet-kinderopvang/` | [Wet kinderopvang](https://wetten.overheid.nl/BWBR0017017) (Childcare Act) | BWBR0017017 | 63 | 2004-10-30 to 2026-08-01 |
| `wet-economische-delicten/` | [Wet op de economische delicten](https://wetten.overheid.nl/BWBR0002063) (Economic Offences Act) | BWBR0002063 | 254 | 2002-04-01 to 2026-09-22 |
| `penitentiaire-beginselenwet/` | [Penitentiaire beginselenwet](https://wetten.overheid.nl/BWBR0009709) (Penitentiary Principles Act) | BWBR0009709 | 28 | 2002-03-08 to 2025-11-01 |
| `wet-wapens-en-munitie/` | [Wet wapens en munitie](https://wetten.overheid.nl/BWBR0008804) (Weapons and Ammunition Act) | BWBR0008804 | 37 | 2002-04-01 to 2026-07-01 |
| `politiewet-2012/` | [Politiewet 2012](https://wetten.overheid.nl/BWBR0031788) (Police Act 2012) | BWBR0031788 | 21 | 2013-01-01 to 2026-06-12 |
| `provinciewet/` | [Provinciewet](https://wetten.overheid.nl/BWBR0005645) (Provinces Act) | BWBR0005645 | 74 | 2002-01-16 to 2026-07-01 |
| `invorderingswet-1990/` | [Invorderingswet 1990](https://wetten.overheid.nl/BWBR0004770) (Tax Collection Act 1990) | BWBR0004770 | 64 | 2002-01-01 to 2026-10-01 |
| `wet-op-de-identificatieplicht/` | [Wet op de identificatieplicht](https://wetten.overheid.nl/BWBR0006297) (Compulsory Identification Act) | BWBR0006297 | 7 | 2001-04-01 to 2026-10-01 |
| `wet-structuur-uitvoeringsorganisatie-werk-en-inkomen/` | [Wet structuur uitvoeringsorganisatie werk en inkomen](https://wetten.overheid.nl/BWBR0013060) (Work and Income Implementation Structure Act (SUWI)) | BWBR0013060 | 63 | 2002-04-01 to 2026-07-01 |
| `wet-justitiele-en-strafvorderlijke-gegevens/` | [Wet justitiële en strafvorderlijke gegevens](https://wetten.overheid.nl/BWBR0014194) (Judicial and Criminal Procedure Data Act) | BWBR0014194 | 30 | 2004-04-01 to 2026-09-01 |
| `handelsregisterwet-2007/` | [Handelsregisterwet 2007](https://wetten.overheid.nl/BWBR0021777) (Trade Register Act 2007) | BWBR0021777 | 33 | 2008-01-01 to 2025-07-16 |
| `wet-algemene-bepalingen-burgerservicenummer/` | [Wet algemene bepalingen burgerservicenummer](https://wetten.overheid.nl/BWBR0022428) (Citizen Service Number (BSN) Act) | BWBR0022428 | 7 | 2007-11-26 to 2025-11-11 |
| `wet-op-de-arbeidsongeschiktheidsverzekering/` | [Wet op de arbeidsongeschiktheidsverzekering](https://wetten.overheid.nl/BWBR0002524) (Disability Insurance Act (WAO)) | BWBR0002524 | 80 | 2002-04-01 to 2026-10-08 |
| `algemene-nabestaandenwet/` | [Algemene nabestaandenwet](https://wetten.overheid.nl/BWBR0007795) (Surviving Dependants Act) | BWBR0007795 | 72 | 2002-01-01 to 2026-07-01 |
| `wet-financiering-sociale-verzekeringen/` | [Wet financiering sociale verzekeringen](https://wetten.overheid.nl/BWBR0017745) (Social Insurance Financing Act) | BWBR0017745 | 65 | 2005-12-09 to 2026-07-01 |
| `pensioenwet/` | [Pensioenwet](https://wetten.overheid.nl/BWBR0020809) (Pensions Act) | BWBR0020809 | 55 | 2007-01-01 to 2026-01-01 |
| `wet-op-het-hoger-onderwijs-en-wetenschappelijk-onderzoek/` | [Wet op het hoger onderwijs en wetenschappelijk onderzoek](https://wetten.overheid.nl/BWBR0005682) (Higher Education and Research Act) | BWBR0005682 | 127 | 2002-01-01 to 2026-08-01 |
| `algemene-termijnenwet/` | [Algemene termijnenwet](https://wetten.overheid.nl/BWBR0002448) (General Time Limits Act) | BWBR0002448 | 2 | 1999-02-17 to 2010-10-10 |
| `wet-arbeidsongeschiktheidsvoorziening-jonggehandicapten/` | [Wet arbeidsongeschiktheidsvoorziening jonggehandicapten](https://wetten.overheid.nl/BWBR0008657) (Young Disabled Persons Act (Wajong)) | BWBR0008657 | 67 | 2002-01-01 to 2026-07-01 |
| `kaderwet-zelfstandige-bestuursorganen/` | [Kaderwet zelfstandige bestuursorganen](https://wetten.overheid.nl/BWBR0020495) (Independent Administrative Bodies Framework Act) | BWBR0020495 | 7 | 2007-02-01 to 2022-07-01 |
| `wet-arbeidsongeschiktheidsverzekering-zelfstandigen/` | [Wet arbeidsongeschiktheidsverzekering zelfstandigen](https://wetten.overheid.nl/BWBR0008656) (Self-Employed Disability Insurance Act) | BWBR0008656 | 64 | 2002-01-01 to 2026-07-01 |
| `wet-verplichte-beroepspensioenregeling/` | [Wet verplichte beroepspensioenregeling](https://wetten.overheid.nl/BWBR0018831) (Compulsory Occupational Pension Scheme Act) | BWBR0018831 | 55 | 2006-01-01 to 2026-01-01 |
| `wet-minimumloon-en-minimumvakantiebijslag/` | [Wet minimumloon en minimumvakantiebijslag](https://wetten.overheid.nl/BWBR0002638) (Minimum Wage and Holiday Allowance Act) | BWBR0002638 | 59 | 2002-01-01 to 2026-07-01 |
| `wet-gemeenschappelijke-regelingen/` | [Wet gemeenschappelijke regelingen](https://wetten.overheid.nl/BWBR0003740) (Joint Arrangements Act) | BWBR0003740 | 19 | 2002-03-07 to 2025-02-12 |
| `wet-educatie-en-beroepsonderwijs/` | [Wet educatie en beroepsonderwijs](https://wetten.overheid.nl/BWBR0007625) (Adult and Vocational Education Act) | BWBR0007625 | 100 | 2001-12-22 to 2026-08-01 |
| `algemene-wet-inkomensafhankelijke-regelingen/` | [Algemene wet inkomensafhankelijke regelingen](https://wetten.overheid.nl/BWBR0018472) (General Act on Income-Related Schemes (allowances)) | BWBR0018472 | 47 | 2005-09-01 to 2026-10-01 |
| `wet-marktordening-gezondheidszorg/` | [Wet marktordening gezondheidszorg](https://wetten.overheid.nl/BWBR0020078) (Healthcare Market Regulation Act) | BWBR0020078 | 44 | 2006-10-01 to 2026-09-01 |
| `wet-publieke-gezondheid/` | [Wet publieke gezondheid](https://wetten.overheid.nl/BWBR0024705) (Public Health Act) | BWBR0024705 | 46 | 2008-12-01 to 2026-01-01 |
| `algemene-kinderbijslagwet/` | [Algemene Kinderbijslagwet](https://wetten.overheid.nl/BWBR0002368) (General Child Benefit Act) | BWBR0002368 | 70 | 2002-01-01 to 2026-08-01 |
| `wet-inkomensvoorziening-oudere-en-gedeeltelijk-arbeidsongeschikte-gewezen-zelfstandigen/` | [Wet inkomensvoorziening oudere en gedeeltelijk arbeidsongeschikte gewezen zelfstandigen](https://wetten.overheid.nl/BWBR0004163) (Income Provision for Older and Partially Disabled Former Self-Employed Persons Act (IOAZ)) | BWBR0004163 | 88 | 2002-01-01 to 2026-07-01 |
| `kadasterwet/` | [Kadasterwet](https://wetten.overheid.nl/BWBR0004541) (Land Registry Act) | BWBR0004541 | 40 | 2002-04-01 to 2026-01-01 |
| `algemene-wet-op-het-binnentreden/` | [Algemene wet op het binnentreden](https://wetten.overheid.nl/BWBR0006763) (General Act on Entry into Dwellings) | BWBR0006763 | 2 | 1999-06-01 to 2010-07-01 |
| `wet-arbeid-en-zorg/` | [Wet arbeid en zorg](https://wetten.overheid.nl/BWBR0013008) (Work and Care Act) | BWBR0013008 | 38 | 2002-01-01 to 2025-01-01 |
| `geneesmiddelenwet/` | [Geneesmiddelenwet](https://wetten.overheid.nl/BWBR0021505) (Medicines Act) | BWBR0021505 | 30 | 2007-07-01 to 2025-09-09 |
| `wet-veiligheidsregios/` | [Wet veiligheidsregio’s](https://wetten.overheid.nl/BWBR0027466) (Safety Regions Act) | BWBR0027466 | 22 | 2010-10-01 to 2026-06-12 |
| `wet-inkomensvoorziening-oudere-en-gedeeltelijk-arbeidsongeschikte-werkloze-werknemers/` | [Wet inkomensvoorziening oudere en gedeeltelijk arbeidsongeschikte werkloze werknemers](https://wetten.overheid.nl/BWBR0004044) (Income Provision for Older and Partially Disabled Unemployed Employees Act (IOAW)) | BWBR0004044 | 87 | 2002-01-01 to 2026-07-01 |
| `wet-op-het-consumentenkrediet/` | [Wet op het consumentenkrediet](https://wetten.overheid.nl/BWBR0004815) (Consumer Credit Act) | BWBR0004815 | 17 | 2002-03-08 to 2019-01-01 |
| `burgerlijk-wetboek-boek-8/` | [Burgerlijk Wetboek Boek 8](https://wetten.overheid.nl/BWBR0005034) (Civil Code Book 8 (transport law)) | BWBR0005034 | 33 | 2002-01-01 to 2026-07-01 |
| `archiefwet-1995/` | [Archiefwet 1995](https://wetten.overheid.nl/BWBR0007376) (Public Records Act 1995) | BWBR0007376 | 15 | 2001-09-01 to 2024-06-19 |
| `beginselenwet-justitiele-jeugdinrichtingen/` | [Beginselenwet justitiële jeugdinrichtingen](https://wetten.overheid.nl/BWBR0011756) (Juvenile Custodial Institutions Act) | BWBR0011756 | 30 | 2002-03-08 to 2023-01-01 |
| `wet-verplichte-deelneming-in-een-bedrijfstakpensioenfonds-2000/` | [Wet verplichte deelneming in een bedrijfstakpensioenfonds 2000](https://wetten.overheid.nl/BWBR0012092) (Compulsory Participation in an Industry-wide Pension Fund Act 2000) | BWBR0012092 | 15 | 2002-01-01 to 2026-01-01 |
| `algemene-douanewet/` | [Algemene douanewet](https://wetten.overheid.nl/BWBR0023746) (General Customs Act) | BWBR0023746 | 35 | 2008-08-01 to 2026-07-01 |
| `dienstenwet/` | [Dienstenwet](https://wetten.overheid.nl/BWBR0026759) (Services Act) | BWBR0026759 | 13 | 2009-12-07 to 2026-01-01 |
| `ambtenarenwet-2017/` | [Ambtenarenwet 2017](https://wetten.overheid.nl/BWBR0001947) (Civil Servants Act 2017) | BWBR0001947 | 39 | 2002-03-07 to 2025-07-01 |
| `kernenergiewet/` | [Kernenergiewet](https://wetten.overheid.nl/BWBR0002402) (Nuclear Energy Act) | BWBR0002402 | 34 | 2002-03-01 to 2024-07-01 |
| `wet-op-de-ondernemingsraden/` | [Wet op de ondernemingsraden](https://wetten.overheid.nl/BWBR0002747) (Works Councils Act) | BWBR0002747 | 31 | 2002-01-01 to 2023-02-18 |
| `wet-arbeidsongeschiktheidsvoorziening-militairen/` | [Wet arbeidsongeschiktheidsvoorziening militairen](https://wetten.overheid.nl/BWBR0002822) (Military Disability Provision Act) | BWBR0002822 | 7 | 2002-02-15 to 2015-01-01 |
| `wet-nationale-ombudsman/` | [Wet Nationale ombudsman](https://wetten.overheid.nl/BWBR0003372) (National Ombudsman Act) | BWBR0003372 | 17 | 2002-03-12 to 2022-07-01 |
| `wet-op-het-primair-onderwijs/` | [Wet op het primair onderwijs](https://wetten.overheid.nl/BWBR0003420) (Primary Education Act) | BWBR0003420 | 101 | 2002-03-20 to 2026-08-01 |
| `wet-op-de-expertisecentra/` | [Wet op de expertisecentra](https://wetten.overheid.nl/BWBR0003549) (Expertise Centres Act (special education)) | BWBR0003549 | 94 | 2002-03-20 to 2026-08-01 |
| `toeslagenwet/` | [Toeslagenwet](https://wetten.overheid.nl/BWBR0004043) (Supplementary Benefits Act) | BWBR0004043 | 58 | 2002-04-01 to 2026-07-01 |
| `wet-luchtvaart/` | [Wet luchtvaart](https://wetten.overheid.nl/BWBR0005555) (Aviation Act) | BWBR0005555 | 84 | 2001-10-01 to 2026-07-01 |
| `wet-op-de-rechtsbijstand/` | [Wet op de rechtsbijstand](https://wetten.overheid.nl/BWBR0006368) (Legal Aid Act) | BWBR0006368 | 58 | 2002-01-01 to 2026-09-01 |
| `wet-sociale-werkvoorziening/` | [Wet sociale werkvoorziening](https://wetten.overheid.nl/BWBR0008903) (Sheltered Employment Act) | BWBR0008903 | 16 | 2002-01-01 to 2015-07-01 |
| `rijkswet-instelling-exclusieve-economische-zone/` | [Rijkswet instelling exclusieve economische zone](https://wetten.overheid.nl/BWBR0010480) (Kingdom Act establishing an Exclusive Economic Zone) | BWBR0010480 | 2 | 2000-04-28 to 2023-01-01 |
| `wet-personenvervoer-2000/` | [Wet personenvervoer 2000](https://wetten.overheid.nl/BWBR0011470) (Passenger Transport Act 2000) | BWBR0011470 | 44 | 2002-01-01 to 2026-07-01 |
| `wet-op-de-rechterlijke-indeling/` | [Wet op de rechterlijke indeling](https://wetten.overheid.nl/BWBR0002080) | BWBR0002080 | 29 | 2002-01-01 to 2023-01-01 |
| `landbouwwet/` | [Landbouwwet](https://wetten.overheid.nl/BWBR0002252) | BWBR0002252 | 12 | 2000-03-08 to 2019-01-01 |
| `prijzenwet/` | [Prijzenwet](https://wetten.overheid.nl/BWBR0002353) | BWBR0002353 | 9 | 1998-01-01 to 2022-05-28 |
| `wet-tarieven-in-strafzaken/` | [Wet tarieven in strafzaken](https://wetten.overheid.nl/BWBR0002406) | BWBR0002406 | 11 | 2002-01-01 to 2025-07-01 |
| `belastingregeling-voor-het-koninkrijk/` | [Belastingregeling voor het Koninkrijk](https://wetten.overheid.nl/BWBR0002464) | BWBR0002464 | 3 | 2002-01-01 to 2010-10-10 |
| `wet-op-de-dividendbelasting-1965/` | [Wet op de dividendbelasting 1965](https://wetten.overheid.nl/BWBR0002515) | BWBR0002515 | 30 | 2002-01-01 to 2025-01-01 |
| `uitleveringswet/` | [Uitleveringswet](https://wetten.overheid.nl/BWBR0002559) | BWBR0002559 | 37 | 2002-01-01 to 2025-07-01 |
| `kostenwet-invordering-rijksbelastingen/` | [Kostenwet invordering rijksbelastingen](https://wetten.overheid.nl/BWBR0002645) | BWBR0002645 | 26 | 2002-01-01 to 2026-01-01 |
| `landbouwkwaliteitswet/` | [Landbouwkwaliteitswet](https://wetten.overheid.nl/BWBR0002755) | BWBR0002755 | 16 | 2002-01-01 to 2021-03-01 |
| `wet-uitkeringen-vervolgingsslachtoffers-1940-1945/` | [Wet uitkeringen vervolgingsslachtoffers 1940-1945](https://wetten.overheid.nl/BWBR0002844) | BWBR0002844 | 69 | 2002-03-01 to 2026-07-01 |
| `wet-afbreking-zwangerschap/` | [Wet afbreking zwangerschap](https://wetten.overheid.nl/BWBR0003396) | BWBR0003396 | 10 | 2002-01-01 to 2025-01-01 |
| `leegstandwet/` | [Leegstandwet](https://wetten.overheid.nl/BWBR0003403) | BWBR0003403 | 15 | 1994-01-01 to 2024-07-01 |
| `wet-uitkeringen-burger-oorlogsslachtoffers-1940-1945/` | [Wet uitkeringen burger-oorlogsslachtoffers 1940-1945](https://wetten.overheid.nl/BWBR0003664) | BWBR0003664 | 56 | 2002-03-01 to 2026-07-01 |
| `wet-buitengewoon-pensioen-indisch-verzet/` | [Wet buitengewoon pensioen Indisch verzet](https://wetten.overheid.nl/BWBR0003968) | BWBR0003968 | 52 | 2002-03-01 to 2026-07-01 |
| `wet-overdracht-tenuitvoerlegging-strafvonnissen/` | [Wet overdracht tenuitvoerlegging strafvonnissen](https://wetten.overheid.nl/BWBR0004028) | BWBR0004028 | 18 | 2002-01-01 to 2025-07-01 |
| `meststoffenwet/` | [Meststoffenwet](https://wetten.overheid.nl/BWBR0004054) | BWBR0004054 | 34 | 2002-01-01 to 2025-12-09 |
| `wet-opneming-buitenlandse-kinderen-ter-adoptie/` | [Wet opneming buitenlandse kinderen ter adoptie](https://wetten.overheid.nl/BWBR0004447) | BWBR0004447 | 9 | 2001-04-01 to 2018-08-01 |
| `waterschapswet/` | [Waterschapswet](https://wetten.overheid.nl/BWBR0005108) | BWBR0005108 | 68 | 2002-01-16 to 2026-01-01 |
| `wet-op-de-accijns/` | [Wet op de accijns](https://wetten.overheid.nl/BWBR0005251) | BWBR0005251 | 71 | 2002-04-01 to 2026-06-20 |
| `wet-financiele-betrekkingen-buitenland-1994/` | [Wet financiële betrekkingen buitenland 1994](https://wetten.overheid.nl/BWBR0006547) | BWBR0006547 | 8 | 2002-01-01 to 2013-01-01 |
| `wet-explosieven-voor-civiel-gebruik/` | [Wet explosieven voor civiel gebruik](https://wetten.overheid.nl/BWBR0006803) | BWBR0006803 | 17 | 1998-01-01 to 2023-04-19 |
| `wet-vermindering-afdracht-loonbelasting-en-premie-voor-de-volksverzekeringen/` | [Wet vermindering afdracht loonbelasting en premie voor de volksverzekeringen](https://wetten.overheid.nl/BWBR0007746) | BWBR0007746 | 38 | 2002-02-01 to 2026-01-01 |
| `wet-privatisering-abp/` | [Wet privatisering ABP](https://wetten.overheid.nl/BWBR0007791) | BWBR0007791 | 19 | 2002-01-01 to 2026-06-04 |
| `kaderwet-szw-subsidies/` | [Kaderwet SZW-subsidies](https://wetten.overheid.nl/BWBR0008754) | BWBR0008754 | 10 | 2001-01-01 to 2016-01-01 |
| `wet-bescherming-antarctica/` | [Wet bescherming Antarctica](https://wetten.overheid.nl/BWBR0009449) | BWBR0009449 | 12 | 2001-04-01 to 2024-01-01 |
| `wet-overige-ocw-subsidies/` | [Wet overige OCW-subsidies](https://wetten.overheid.nl/BWBR0009458) | BWBR0009458 | 12 | 2001-05-11 to 2019-01-01 |
| `wet-tegemoetkoming-onderwijsbijdrage-en-schoolkosten/` | [Wet tegemoetkoming onderwijsbijdrage en schoolkosten](https://wetten.overheid.nl/BWBR0012438) | BWBR0012438 | 67 | 2002-02-17 to 2026-01-01 |
| `wet-op-het-btw-compensatiefonds/` | [Wet op het BTW-compensatiefonds](https://wetten.overheid.nl/BWBR0013817) | BWBR0013817 | 8 | 2003-01-01 to 2023-01-01 |
| `uitvoeringswet-huurprijzen-woonruimte/` | [Uitvoeringswet huurprijzen woonruimte](https://wetten.overheid.nl/BWBR0014315) | BWBR0014315 | 45 | 2002-07-01 to 2026-06-04 |
| `spoorwegwet/` | [Spoorwegwet](https://wetten.overheid.nl/BWBR0015007) | BWBR0015007 | 44 | 2004-12-31 to 2026-06-04 |
| `rijkswet-onderzoeksraad-voor-veiligheid/` | [Rijkswet Onderzoeksraad voor veiligheid](https://wetten.overheid.nl/BWBR0017613) | BWBR0017613 | 9 | 2005-02-01 to 2022-05-01 |
| `wet-toelating-zorginstellingen/` | [Wet toelating zorginstellingen](https://wetten.overheid.nl/BWBR0018906) | BWBR0018906 | 19 | 2006-01-01 to 2022-01-01 |
| `wet-toezicht-financiele-verslaggeving/` | [Wet toezicht financiële verslaggeving](https://wetten.overheid.nl/BWBR0020369) | BWBR0020369 | 17 | 2006-12-31 to 2025-03-01 |
| `wet-handhaving-consumentenbescherming/` | [Wet handhaving consumentenbescherming](https://wetten.overheid.nl/BWBR0020586) | BWBR0020586 | 44 | 2006-12-29 to 2026-06-25 |
| `wet-op-het-kindgebonden-budget/` | [Wet op het kindgebonden budget](https://wetten.overheid.nl/BWBR0022751) | BWBR0022751 | 32 | 2007-11-03 to 2026-07-01 |
| `wet-tijdelijk-huisverbod/` | [Wet tijdelijk huisverbod](https://wetten.overheid.nl/BWBR0024649) | BWBR0024649 | 8 | 2009-01-01 to 2020-07-01 |
| `wet-wegvervoer-goederen/` | [Wet wegvervoer goederen](https://wetten.overheid.nl/BWBR0024800) | BWBR0024800 | 10 | 2009-05-01 to 2024-01-01 |
| `wet-uitvoering-eu-handelingen-energie-efficientie/` | [Wet uitvoering EU-handelingen energie-efficiëntie](https://wetten.overheid.nl/BWBR0029672) | BWBR0029672 | 19 | 2011-03-05 to 2026-01-01 |
| `wet-college-voor-de-rechten-van-de-mens/` | [Wet College voor de rechten van de mens](https://wetten.overheid.nl/BWBR0030733) | BWBR0030733 | 7 | 2011-12-17 to 2026-01-01 |
| `wet-lokaal-spoor/` | [Wet lokaal spoor](https://wetten.overheid.nl/BWBR0034363) | BWBR0034363 | 8 | 2013-12-14 to 2024-01-01 |
| `wet-bescherming-staatsgeheimen/` | [Wet bescherming staatsgeheimen](https://wetten.overheid.nl/BWBR0002074) | BWBR0002074 | 3 | 1999-06-01 to 2013-01-01 |
| `gezondheidswet/` | [Gezondheidswet](https://wetten.overheid.nl/BWBR0002202) | BWBR0002202 | 21 | 1998-01-01 to 2025-07-05 |
| `luchtvaartwet/` | [Luchtvaartwet](https://wetten.overheid.nl/BWBR0002267) | BWBR0002267 | 41 | 2002-01-01 to 2026-07-01 |
| `wet-op-de-kansspelbelasting/` | [Wet op de kansspelbelasting](https://wetten.overheid.nl/BWBR0002359) | BWBR0002359 | 13 | 2002-01-01 to 2026-01-01 |
| `wet-gewetensbezwaren-militaire-dienst/` | [Wet gewetensbezwaren militaire dienst](https://wetten.overheid.nl/BWBR0002386) | BWBR0002386 | 8 | 2002-01-01 to 2020-01-01 |
| `hamsterwet/` | [Hamsterwet](https://wetten.overheid.nl/BWBR0002389) | BWBR0002389 | 8 | 1997-05-01 to 2020-07-17 |
| `noodwet-voedselvoorziening/` | [Noodwet voedselvoorziening](https://wetten.overheid.nl/BWBR0002392) | BWBR0002392 | 7 | 2000-03-08 to 2015-01-01 |
| `alcoholwet/` | [Alcoholwet](https://wetten.overheid.nl/BWBR0002458) | BWBR0002458 | 22 | 2000-11-01 to 2025-02-12 |
| `gerechtsdeurwaarderswet/` | [Gerechtsdeurwaarderswet](https://wetten.overheid.nl/BWBR0012197) | BWBR0012197 | 32 | 2002-01-01 to 2025-01-01 |
| `wet-bevordering-integriteitsbeoordelingen-door-het-openbaar-bestuur/` | [Wet bevordering integriteitsbeoordelingen door het openbaar bestuur](https://wetten.overheid.nl/BWBR0013798) | BWBR0013798 | 40 | 2002-09-01 to 2025-07-16 |
| `mijnbouwwet/` | [Mijnbouwwet](https://wetten.overheid.nl/BWBR0014168) | BWBR0014168 | 72 | 2003-01-01 to 2026-06-04 |
| `wet-toezicht-accountantsorganisaties/` | [Wet toezicht accountantsorganisaties](https://wetten.overheid.nl/BWBR0019468) | BWBR0019468 | 24 | 2006-10-01 to 2026-09-01 |
| `wet-ter-voorkoming-van-witwassen-en-financieren-van-terrorisme/` | [Wet ter voorkoming van witwassen en financieren van terrorisme](https://wetten.overheid.nl/BWBR0024282) | BWBR0024282 | 37 | 2008-08-01 to 2026-07-01 |
| `drinkwaterwet/` | [Drinkwaterwet](https://wetten.overheid.nl/BWBR0026338) | BWBR0026338 | 14 | 2011-07-01 to 2024-01-01 |
| `wet-dieren/` | [Wet dieren](https://wetten.overheid.nl/BWBR0030250) | BWBR0030250 | 19 | 2013-01-01 to 2025-01-01 |
| `wet-ambtenaren-defensie/` | [Wet ambtenaren defensie](https://wetten.overheid.nl/BWBR0001952) | BWBR0001952 | 20 | 2002-01-01 to 2026-01-01 |
| `wet-aansprakelijkheidsverzekering-motorrijtuigen/` | [Wet aansprakelijkheidsverzekering motorrijtuigen](https://wetten.overheid.nl/BWBR0002415) | BWBR0002415 | 21 | 2002-01-01 to 2025-07-24 |
| `bekendmakingswet/` | [Bekendmakingswet](https://wetten.overheid.nl/BWBR0004287) | BWBR0004287 | 8 | 1995-05-17 to 2024-01-01 |
| `wet-administratiefrechtelijke-handhaving-verkeersvoorschriften/` | [Wet administratiefrechtelijke handhaving verkeersvoorschriften](https://wetten.overheid.nl/BWBR0004581) | BWBR0004581 | 32 | 2002-03-12 to 2026-09-01 |
| `wet-op-de-belasting-van-personenauto-s-en-motorrijwielen-1992/` | [Wet op de belasting van personenauto's en motorrijwielen 1992](https://wetten.overheid.nl/BWBR0005806) | BWBR0005806 | 42 | 2002-01-01 to 2026-01-01 |
| `wet-op-de-beroepen-in-de-individuele-gezondheidszorg/` | [Wet op de beroepen in de individuele gezondheidszorg](https://wetten.overheid.nl/BWBR0006251) | BWBR0006251 | 46 | 2002-01-01 to 2025-07-05 |
| `wet-centraal-orgaan-opvang-asielzoekers/` | [Wet Centraal Orgaan opvang asielzoekers](https://wetten.overheid.nl/BWBR0006685) | BWBR0006685 | 15 | 2001-04-01 to 2026-06-04 |
| `wet-waardering-onroerende-zaken/` | [Wet waardering onroerende zaken](https://wetten.overheid.nl/BWBR0007119) | BWBR0007119 | 25 | 2002-01-01 to 2026-07-01 |
| `wet-belastingen-op-milieugrondslag/` | [Wet belastingen op milieugrondslag](https://wetten.overheid.nl/BWBR0007168) | BWBR0007168 | 57 | 2002-01-01 to 2026-06-04 |
| `arbeidstijdenwet/` | [Arbeidstijdenwet](https://wetten.overheid.nl/BWBR0007671) | BWBR0007671 | 33 | 1999-11-01 to 2025-07-01 |
| `wet-op-de-huurtoeslag/` | [Wet op de huurtoeslag](https://wetten.overheid.nl/BWBR0008659) | BWBR0008659 | 51 | 2002-01-01 to 2026-01-01 |
| `wet-allocatie-arbeidskrachten-door-intermediairs/` | [Wet allocatie arbeidskrachten door intermediairs](https://wetten.overheid.nl/BWBR0009616) | BWBR0009616 | 25 | 2002-01-01 to 2026-07-01 |
| `telecommunicatiewet/` | [Telecommunicatiewet](https://wetten.overheid.nl/BWBR0009950) | BWBR0009950 | 74 | 2002-01-01 to 2026-08-15 |
| `postwet-2009/` | [Postwet 2009](https://wetten.overheid.nl/BWBR0025572) | BWBR0025572 | 15 | 2009-04-01 to 2019-01-01 |
| `wet-basisregistratie-personen/` | [Wet basisregistratie personen](https://wetten.overheid.nl/BWBR0033715) | BWBR0033715 | 18 | 2014-01-06 to 2026-10-01 |
| `natuurschoonwet-1928/` | [Natuurschoonwet 1928](https://wetten.overheid.nl/BWBR0001939) | BWBR0001939 | 13 | 2001-01-01 to 2021-01-01 |
| `wet-op-de-raad-van-state/` | [Wet op de Raad van State](https://wetten.overheid.nl/BWBR0002367) | BWBR0002367 | 33 | 2002-04-01 to 2022-05-01 |
| `wet-op-belastingen-van-rechtsverkeer/` | [Wet op belastingen van rechtsverkeer](https://wetten.overheid.nl/BWBR0002740) | BWBR0002740 | 39 | 2002-04-01 to 2026-01-01 |
| `wet-giraal-effectenverkeer/` | [Wet giraal effectenverkeer](https://wetten.overheid.nl/BWBR0003109) | BWBR0003109 | 16 | 2000-11-22 to 2023-01-01 |
| `sanctiewet-1977/` | [Sanctiewet 1977](https://wetten.overheid.nl/BWBR0003296) | BWBR0003296 | 21 | 2001-04-01 to 2025-03-01 |
| `scheepvaartverkeerswet/` | [Scheepvaartverkeerswet](https://wetten.overheid.nl/BWBR0004364) | BWBR0004364 | 27 | 2001-09-01 to 2026-06-04 |
| `wet-vervoer-gevaarlijke-stoffen/` | [Wet vervoer gevaarlijke stoffen](https://wetten.overheid.nl/BWBR0007606) | BWBR0007606 | 14 | 2002-03-01 to 2025-01-01 |
| `coordinatiewet-uitzonderingstoestanden/` | [Coördinatiewet uitzonderingstoestanden](https://wetten.overheid.nl/BWBR0007981) | BWBR0007981 | 2 | 2001-04-01 to 2010-10-10 |
| `financiele-verhoudingswet/` | [Financiële-verhoudingswet](https://wetten.overheid.nl/BWBR0008290) | BWBR0008290 | 9 | 1999-02-17 to 2024-01-01 |
| `wet-rechtspositie-rechterlijke-ambtenaren/` | [Wet rechtspositie rechterlijke ambtenaren](https://wetten.overheid.nl/BWBR0008365) | BWBR0008365 | 37 | 2002-01-01 to 2026-01-01 |
| `beginselenwet-verpleging-ter-beschikking-gestelden/` | [Beginselenwet verpleging ter beschikking gestelden](https://wetten.overheid.nl/BWBR0008765) | BWBR0008765 | 19 | 2002-01-01 to 2025-07-01 |
| `bankwet-1998/` | [Bankwet 1998](https://wetten.overheid.nl/BWBR0009508) | BWBR0009508 | 20 | 2002-01-28 to 2026-09-22 |
| `wet-studiefinanciering-2000/` | [Wet studiefinanciering 2000](https://wetten.overheid.nl/BWBR0011453) | BWBR0011453 | 98 | 2002-02-08 to 2026-08-01 |
| `zaaizaad-en-plantgoedwet-2005/` | [Zaaizaad- en plantgoedwet 2005](https://wetten.overheid.nl/BWBR0018040) | BWBR0018040 | 18 | 2006-02-01 to 2025-01-01 |
| `wet-op-de-zorgtoeslag/` | [Wet op de zorgtoeslag](https://wetten.overheid.nl/BWBR0018451) | BWBR0018451 | 28 | 2006-01-01 to 2026-01-01 |
| `wet-op-de-bijzondere-opsporingsdiensten/` | [Wet op de bijzondere opsporingsdiensten](https://wetten.overheid.nl/BWBR0019919) | BWBR0019919 | 7 | 2007-06-01 to 2025-07-01 |
| `wet-gewasbeschermingsmiddelen-en-biociden/` | [Wet gewasbeschermingsmiddelen en biociden](https://wetten.overheid.nl/BWBR0021670) | BWBR0021670 | 20 | 2007-10-17 to 2026-01-01 |
| `wet-griffierechten-burgerlijke-zaken/` | [Wet griffierechten burgerlijke zaken](https://wetten.overheid.nl/BWBR0028899) | BWBR0028899 | 24 | 2010-11-01 to 2026-01-01 |
| `wet-gemeentelijke-schuldhulpverlening/` | [Wet gemeentelijke schuldhulpverlening](https://wetten.overheid.nl/BWBR0031331) | BWBR0031331 | 9 | 2012-07-01 to 2026-07-01 |
| `aanbestedingswet-2012/` | [Aanbestedingswet 2012](https://wetten.overheid.nl/BWBR0032203) | BWBR0032203 | 15 | 2013-04-01 to 2026-04-30 |
| `wet-op-het-accountantsberoep/` | [Wet op het accountantsberoep](https://wetten.overheid.nl/BWBR0032573) | BWBR0032573 | 10 | 2011-01-01 to 2026-09-01 |
| `instellingswet-autoriteit-consument-en-markt/` | [Instellingswet Autoriteit Consument en Markt](https://wetten.overheid.nl/BWBR0033043) | BWBR0033043 | 15 | 2013-04-01 to 2025-09-01 |
| `warmtewet/` | [Warmtewet](https://wetten.overheid.nl/BWBR0033729) | BWBR0033729 | 19 | 2014-01-01 to 2026-01-01 |
| `warenwet/` | [Warenwet](https://wetten.overheid.nl/BWBR0001969) | BWBR0001969 | 34 | 2002-01-01 to 2025-07-12 |
| `wet-buitengewoon-pensioen-1940-1945/` | [Wet buitengewoon pensioen 1940-1945](https://wetten.overheid.nl/BWBR0002032) | BWBR0002032 | 32 | 2002-01-01 to 2025-01-01 |
| `wet-buitengewoon-pensioen-zeelieden-oorlogsslachtoffers/` | [Wet buitengewoon pensioen zeelieden-oorlogsslachtoffers](https://wetten.overheid.nl/BWBR0002035) | BWBR0002035 | 31 | 2002-01-01 to 2025-01-01 |
| `wet-op-de-kansspelen/` | [Wet op de kansspelen](https://wetten.overheid.nl/BWBR0002469) | BWBR0002469 | 24 | 2002-01-01 to 2025-02-12 |
| `registratiewet-1970/` | [Registratiewet 1970](https://wetten.overheid.nl/BWBR0002739) | BWBR0002739 | 10 | 1999-09-01 to 2023-01-01 |
| `wet-melding-collectief-ontslag/` | [Wet melding collectief ontslag](https://wetten.overheid.nl/BWBR0003026) | BWBR0003026 | 6 | 2002-01-01 to 2018-01-01 |
| `wedervergeldingswet-zeescheepvaart/` | [Wedervergeldingswet zeescheepvaart](https://wetten.overheid.nl/BWBR0003104) | BWBR0003104 | 4 | 1999-02-17 to 2025-07-01 |
| `wet-uitvoering-internationaal-energieprogramma/` | [Wet uitvoering Internationaal Energieprogramma](https://wetten.overheid.nl/BWBR0003235) | BWBR0003235 | 8 | 1998-01-01 to 2021-07-01 |
| `wet-schadefonds-olietankschepen/` | [Wet schadefonds olietankschepen](https://wetten.overheid.nl/BWBR0003400) | BWBR0003400 | 8 | 1997-11-15 to 2019-01-01 |
| `wet-vervoer-over-zee/` | [Wet vervoer over zee](https://wetten.overheid.nl/BWBR0003528) | BWBR0003528 | 6 | 1998-01-01 to 2016-05-01 |
| `wet-voorkoming-verontreiniging-door-schepen/` | [Wet voorkoming verontreiniging door schepen](https://wetten.overheid.nl/BWBR0003642) | BWBR0003642 | 18 | 2000-10-18 to 2025-09-17 |
| `prijzennoodwet/` | [Prijzennoodwet](https://wetten.overheid.nl/BWBR0003734) | BWBR0003734 | 8 | 1997-05-01 to 2019-01-01 |
| `wet-bescherming-oorspronkelijke-topografieen-van-halfgeleiderprodukten/` | [Wet bescherming oorspronkelijke topografieën van halfgeleiderprodukten](https://wetten.overheid.nl/BWBR0004224) | BWBR0004224 | 7 | 2002-01-01 to 2020-02-01 |
| `tabaks-en-rookwarenwet/` | [Tabaks- en rookwarenwet](https://wetten.overheid.nl/BWBR0004302) | BWBR0004302 | 35 | 2000-06-21 to 2026-07-01 |
| `wet-schadeloosstelling-leden-tweede-kamer/` | [Wet schadeloosstelling leden Tweede Kamer](https://wetten.overheid.nl/BWBR0004939) | BWBR0004939 | 44 | 2002-01-01 to 2026-07-07 |
| `wet-op-de-lijkbezorging/` | [Wet op de lijkbezorging](https://wetten.overheid.nl/BWBR0005009) | BWBR0005009 | 22 | 2002-04-01 to 2026-07-01 |
| `wet-op-de-verbruiksbelasting-van-alcoholvrije-dranken/` | [Wet op de verbruiksbelasting van alcoholvrije dranken](https://wetten.overheid.nl/BWBR0005802) | BWBR0005802 | 15 | 2002-04-01 to 2025-01-01 |
| `wet-op-de-naburige-rechten/` | [Wet op de naburige rechten](https://wetten.overheid.nl/BWBR0005921) | BWBR0005921 | 21 | 2002-01-01 to 2026-01-01 |
| `wet-op-de-motorrijtuigenbelasting-1994/` | [Wet op de motorrijtuigenbelasting 1994](https://wetten.overheid.nl/BWBR0006324) | BWBR0006324 | 46 | 2002-01-01 to 2026-07-01 |
| `wet-verevening-pensioenrechten-bij-scheiding/` | [Wet verevening pensioenrechten bij scheiding](https://wetten.overheid.nl/BWBR0006641) | BWBR0006641 | 11 | 2002-02-15 to 2021-07-10 |
| `wet-toezicht-effectenverkeer-1995/` | [Wet toezicht effectenverkeer 1995](https://wetten.overheid.nl/BWBR0007657) | BWBR0007657 | 23 | 2002-01-01 to 2022-10-01 |
| `winkeltijdenwet/` | [Winkeltijdenwet](https://wetten.overheid.nl/BWBR0007952) | BWBR0007952 | 5 | 1998-01-01 to 2022-01-01 |
| `kaderwet-adviescolleges/` | [Kaderwet adviescolleges](https://wetten.overheid.nl/BWBR0008159) | BWBR0008159 | 6 | 1997-01-01 to 2022-07-01 |
| `wet-op-de-europese-ondernemingsraden/` | [Wet op de Europese ondernemingsraden](https://wetten.overheid.nl/BWBR0008508) | BWBR0008508 | 8 | 2002-01-01 to 2017-12-16 |
| `wet-particuliere-beveiligingsorganisaties-en-recherchebureaus/` | [Wet particuliere beveiligingsorganisaties en recherchebureaus](https://wetten.overheid.nl/BWBR0008973) | BWBR0008973 | 11 | 2002-01-01 to 2025-07-01 |
| `wet-op-bijzondere-medische-verrichtingen/` | [Wet op bijzondere medische verrichtingen](https://wetten.overheid.nl/BWBR0008974) | BWBR0008974 | 8 | 2001-01-01 to 2025-07-05 |
| `wet-op-de-formeel-buitenlandse-vennootschappen/` | [Wet op de formeel buitenlandse vennootschappen](https://wetten.overheid.nl/BWBR0009191) | BWBR0009191 | 9 | 1999-02-17 to 2020-02-01 |
| `wet-overheidspersoneel-onder-de-werknemersverzekeringen/` | [Wet overheidspersoneel onder de werknemersverzekeringen](https://wetten.overheid.nl/BWBR0009267) | BWBR0009267 | 13 | 2002-02-15 to 2018-01-01 |
| `invoeringswet-wet-inkomstenbelasting-2001/` | [Invoeringswet Wet inkomstenbelasting 2001](https://wetten.overheid.nl/BWBR0011354) | BWBR0011354 | 23 | 2002-01-01 to 2026-01-01 |
| `overgangswet-elektriciteitsproductiesector/` | [Overgangswet elektriciteitsproductiesector](https://wetten.overheid.nl/BWBR0012088) | BWBR0012088 | 5 | 2002-01-01 to 2013-01-01 |
| `wet-toetsing-levensbeeindiging-op-verzoek-en-hulp-bij-zelfdoding/` | [Wet toetsing levensbeëindiging op verzoek en hulp bij zelfdoding](https://wetten.overheid.nl/BWBR0012410) | BWBR0012410 | 7 | 2002-04-01 to 2021-10-01 |
| `wet-capaciteitsbeheersing-binnenvaartvloot/` | [Wet capaciteitsbeheersing binnenvaartvloot](https://wetten.overheid.nl/BWBR0012950) | BWBR0012950 | 7 | 2001-11-23 to 2015-01-01 |
| `wet-toezicht-en-geschillenbeslechting-collectieve-beheersorganisaties-auteurs-en-naburige-rechten/` | [Wet toezicht en geschillenbeslechting collectieve beheersorganisaties auteurs- en naburige rechten](https://wetten.overheid.nl/BWBR0014779) | BWBR0014779 | 17 | 2003-07-15 to 2025-07-01 |
| `wet-controle-op-rechtspersonen/` | [Wet controle op rechtspersonen](https://wetten.overheid.nl/BWBR0015049) | BWBR0015049 | 10 | 2005-01-01 to 2018-09-19 |
| `wet-op-het-centraal-bureau-voor-de-statistiek/` | [Wet op het Centraal bureau voor de statistiek](https://wetten.overheid.nl/BWBR0015926) | BWBR0015926 | 18 | 2004-01-03 to 2025-09-01 |
| `overleveringswet/` | [Overleveringswet](https://wetten.overheid.nl/BWBR0016664) | BWBR0016664 | 24 | 2004-05-12 to 2025-07-01 |
| `wet-rol-werknemers-bij-europese-rechtspersonen/` | [Wet rol werknemers bij Europese rechtspersonen](https://wetten.overheid.nl/BWBR0018115) | BWBR0018115 | 5 | 2005-04-01 to 2022-01-01 |
| `wet-invoering-en-financiering-wet-werk-en-inkomen-naar-arbeidsvermogen/` | [Wet Invoering en financiering Wet werk en inkomen naar arbeidsvermogen](https://wetten.overheid.nl/BWBR0019058) | BWBR0019058 | 13 | 2004-10-01 to 2015-01-01 |
| `metrologiewet/` | [Metrologiewet](https://wetten.overheid.nl/BWBR0019517) | BWBR0019517 | 13 | 2006-11-29 to 2023-04-19 |
| `invoerings-en-aanpassingswet-pensioenwet/` | [Invoerings- en aanpassingswet Pensioenwet](https://wetten.overheid.nl/BWBR0020828) | BWBR0020828 | 8 | 2007-01-01 to 2019-01-01 |
| `binnenvaartwet/` | [Binnenvaartwet](https://wetten.overheid.nl/BWBR0023009) | BWBR0023009 | 13 | 2009-07-01 to 2025-06-01 |
| `algemene-wet-erkenning-eu-beroepskwalificaties/` | [Algemene wet erkenning EU-beroepskwalificaties](https://wetten.overheid.nl/BWBR0023066) | BWBR0023066 | 10 | 2007-01-01 to 2021-08-26 |
| `wet-basisregistratie-adressen-en-gebouwen/` | [Wet basisregistratie adressen en gebouwen](https://wetten.overheid.nl/BWBR0023466) | BWBR0023466 | 8 | 2009-07-01 to 2025-02-12 |
| `wet-op-de-parlementaire-enquete-2008/` | [Wet op de parlementaire enquête 2008](https://wetten.overheid.nl/BWBR0023825) | BWBR0023825 | 15 | 2008-05-09 to 2025-02-12 |
| `wet-aanvullende-bepalingen-verwerking-persoonsgegevens-in-de-zorg/` | [Wet aanvullende bepalingen verwerking persoonsgegevens in de zorg](https://wetten.overheid.nl/BWBR0023864) | BWBR0023864 | 18 | 2008-06-01 to 2025-07-05 |
| `wet-strategische-diensten/` | [Wet strategische diensten](https://wetten.overheid.nl/BWBR0030545) | BWBR0030545 | 11 | 2012-01-01 to 2024-12-19 |
| `wet-naleving-europese-regelgeving-publieke-entiteiten/` | [Wet Naleving Europese regelgeving publieke entiteiten](https://wetten.overheid.nl/BWBR0031640) | BWBR0031640 | 5 | 2012-06-13 to 2016-07-01 |
| `wet-wederzijdse-erkenning-en-tenuitvoerlegging-vrijheidsbenemende-en-voorwaardelijke-sancties/` | [Wet wederzijdse erkenning en tenuitvoerlegging vrijheidsbenemende en voorwaardelijke sancties](https://wetten.overheid.nl/BWBR0031814) | BWBR0031814 | 7 | 2012-11-01 to 2024-10-01 |
| `wet-verbod-pelsdierhouderij/` | [Wet verbod pelsdierhouderij](https://wetten.overheid.nl/BWBR0032739) | BWBR0032739 | 6 | 2013-01-15 to 2024-01-01 |
| `wet-voorraadvorming-aardolieproducten-2012/` | [Wet voorraadvorming aardolieproducten 2012](https://wetten.overheid.nl/BWBR0032775) | BWBR0032775 | 4 | 2013-04-01 to 2021-07-23 |
| `aanbestedingswet-op-defensie-en-veiligheidsgebied/` | [Aanbestedingswet op defensie- en veiligheidsgebied](https://wetten.overheid.nl/BWBR0032898) | BWBR0032898 | 8 | 2013-02-16 to 2019-04-18 |
| `wet-basisregistratie-grootschalige-topografie/` | [Wet basisregistratie grootschalige topografie](https://wetten.overheid.nl/BWBR0034026) | BWBR0034026 | 6 | 2016-01-01 to 2025-02-12 |
| `huisvestingswet-2014/` | [Huisvestingswet 2014](https://wetten.overheid.nl/BWBR0035303) | BWBR0035303 | 19 | 2015-01-01 to 2026-11-01 |
| `wet-algemene-bepalingen/` | [Wet algemene bepalingen](https://wetten.overheid.nl/BWBR0001833) | BWBR0001833 | 3 | 1992-01-01 to 2012-01-01 |
| `wet-ministeriele-verantwoordelijkheid-en-ambtsdelicten-leden-staten-generaal-ministers-en-staatssecretarissen/` | [Wet ministeriële verantwoordelijkheid en ambtsdelicten leden Staten-Generaal, ministers en staatssecretarissen](https://wetten.overheid.nl/BWBR0001844) | BWBR0001844 | 3 | 1998-01-01 to 2018-09-19 |
| `schepenwet/` | [Schepenwet](https://wetten.overheid.nl/BWBR0001876) | BWBR0001876 | 8 | 2002-01-01 to 2026-07-01 |
| `handelsnaamwet/` | [Handelsnaamwet](https://wetten.overheid.nl/BWBR0001906) | BWBR0001906 | 5 | 2002-01-01 to 2017-09-01 |
| `wet-op-de-collectieve-arbeidsovereenkomst/` | [Wet op de collectieve arbeidsovereenkomst](https://wetten.overheid.nl/BWBR0001937) | BWBR0001937 | 4 | 1997-05-14 to 2007-01-01 |
| `wegenwet/` | [Wegenwet](https://wetten.overheid.nl/BWBR0001948) | BWBR0001948 | 12 | 1999-02-17 to 2024-01-01 |
| `wet-op-het-algemeen-verbindend-en-het-onverbindend-verklaren-van-bepalingen-van-collectieve-arbeidsovereenkomsten/` | [Wet op het algemeen verbindend en het onverbindend verklaren van bepalingen van collectieve arbeidsovereenkomsten](https://wetten.overheid.nl/BWBR0001987) | BWBR0001987 | 18 | 1999-12-24 to 2026-07-01 |
| `wet-medewerking-verdedigingsvoorbereiding/` | [Wet medewerking verdedigingsvoorbereiding](https://wetten.overheid.nl/BWBR0001995) | BWBR0001995 | 7 | 1998-01-01 to 2021-07-01 |
| `bodemproductiewet-1939/` | [Bodemproductiewet 1939](https://wetten.overheid.nl/BWBR0001996) | BWBR0001996 | 4 | 1998-01-01 to 2019-01-01 |
| `distributiewet/` | [Distributiewet](https://wetten.overheid.nl/BWBR0001997) | BWBR0001997 | 8 | 1999-02-17 to 2020-07-17 |
| `wet-op-de-sociaal-economische-raad/` | [Wet op de Sociaal-Economische Raad](https://wetten.overheid.nl/BWBR0002058) | BWBR0002058 | 18 | 1999-07-01 to 2023-01-01 |
| `garantiewet-burgerlijk-overheidspersoneel-indonesie/` | [Garantiewet Burgerlijk Overheidspersoneel Indonesië](https://wetten.overheid.nl/BWBR0002060) | BWBR0002060 | 4 | 2002-01-01 to 2013-01-01 |
| `garantiewet-militairen-k-n-i-l/` | [Garantiewet Militairen K.N.I.L.](https://wetten.overheid.nl/BWBR0002077) | BWBR0002077 | 2 | 2002-01-01 to 2011-02-23 |
| `wet-onderstandsregeling-ingevolge-artikel-2-van-de-garantiewet-burgerlijk-overheidspersoneel-indonesie/` | [Wet onderstandsregeling ingevolge artikel 2 van de Garantiewet Burgerlijk Overheidspersoneel Indonesië](https://wetten.overheid.nl/BWBR0002083) | BWBR0002083 | 1 | 1998-04-01 to 1998-04-01 |
| `wet-pensioenvoorzieningen-k-n-i-l/` | [Wet pensioenvoorzieningen K.N.I.L.](https://wetten.overheid.nl/BWBR0002090) | BWBR0002090 | 1 | 1952-07-14 to 1952-07-14 |
| `wet-bescherming-bevolking/` | [Wet bescherming bevolking](https://wetten.overheid.nl/BWBR0002096) | BWBR0002096 | 1 | 1986-07-01 to 1986-07-01 |
| `statuut-voor-het-koninkrijk-der-nederlanden/` | [Statuut voor het Koninkrijk der Nederlanden](https://wetten.overheid.nl/BWBR0002154) | BWBR0002154 | 5 | 1998-10-09 to 2024-01-01 |
| `toeslagwet-indonesische-pensioenen-1956/` | [Toeslagwet Indonesische pensioenen 1956](https://wetten.overheid.nl/BWBR0002251) | BWBR0002251 | 4 | 2002-01-01 to 2015-01-01 |
| `instellingswet-bijstandkorps-burgerlijke-rijksambtenaren-bestemd-voor-dienst-in-nederlands-nieuw-guinea/` | [Instellingswet Bijstandkorps burgerlijke rijksambtenaren bestemd voor dienst in Nederlands-Nieuw-Guinea](https://wetten.overheid.nl/BWBR0002370) | BWBR0002370 | 1 | 2002-01-01 to 2002-01-01 |
| `uitvoeringswet-nederlands-duits-grensverdrag/` | [Uitvoeringswet Nederlands-Duits Grensverdrag](https://wetten.overheid.nl/BWBR0002412) | BWBR0002412 | 3 | 1994-01-01 to 2026-06-04 |
| `samenloopregeling-indonesische-pensioenen-1960/` | [Samenloopregeling Indonesische pensioenen 1960](https://wetten.overheid.nl/BWBR0002414) | BWBR0002414 | 6 | 2002-01-01 to 2015-01-01 |
| `visserijwet-1963/` | [Visserijwet 1963](https://wetten.overheid.nl/BWBR0002416) | BWBR0002416 | 15 | 2002-02-01 to 2024-04-01 |
| `wet-tot-uitvoering-van-de-verordening-no-11-van-de-raad-van-de-europese-economische-gemeenschap/` | [Wet tot uitvoering van de Verordening No. 11 van de Raad van de Europese Economische Gemeenschap](https://wetten.overheid.nl/BWBR0002419) | BWBR0002419 | 2 | 1998-01-01 to 2013-01-01 |
| `verhaalswet-ongevallen-ambtenaren/` | [Verhaalswet ongevallen ambtenaren](https://wetten.overheid.nl/BWBR0002500) | BWBR0002500 | 3 | 1965-09-15 to 2020-01-01 |
| `uitkeringswet-gewezen-militairen/` | [Uitkeringswet gewezen militairen](https://wetten.overheid.nl/BWBR0002540) | BWBR0002540 | 5 | 2002-02-15 to 2020-01-01 |
| `liquidatiewet-ongevallenwetten/` | [Liquidatiewet ongevallenwetten](https://wetten.overheid.nl/BWBR0002553) | BWBR0002553 | 5 | 1999-07-01 to 2015-01-01 |
| `overgangswet-nieuw-burgerlijk-wetboek/` | [Overgangswet nieuw Burgerlijk Wetboek](https://wetten.overheid.nl/BWBR0002565) | BWBR0002565 | 49 | 2002-01-01 to 2026-06-04 |
| `leerplichtwet-1969/` | [Leerplichtwet 1969](https://wetten.overheid.nl/BWBR0002628) | BWBR0002628 | 38 | 2002-02-08 to 2026-08-01 |
| `algemene-pensioen-en-uitkeringswet-politieke-ambtsdragers/` | [Algemene pensioen- en uitkeringswet politieke ambtsdragers](https://wetten.overheid.nl/BWBR0002691) | BWBR0002691 | 44 | 2002-01-01 to 2026-04-24 |
| `wet-op-de-loonvorming/` | [Wet op de loonvorming](https://wetten.overheid.nl/BWBR0002698) | BWBR0002698 | 7 | 1999-02-17 to 2026-01-01 |
| `experimentenwet-onderwijs/` | [Experimentenwet onderwijs](https://wetten.overheid.nl/BWBR0002718) | BWBR0002718 | 15 | 2000-09-01 to 2022-08-01 |
| `noodwet-geneeskundigen/` | [Noodwet Geneeskundigen](https://wetten.overheid.nl/BWBR0002758) | BWBR0002758 | 4 | 2001-09-01 to 2021-07-01 |
| `noodwet-arbeidsvoorziening/` | [Noodwet Arbeidsvoorziening](https://wetten.overheid.nl/BWBR0002759) | BWBR0002759 | 6 | 2002-01-01 to 2014-01-06 |
| `wet-ambtelijk-toezicht-bij-openbare-verkopingen/` | [Wet ambtelijk toezicht bij openbare verkopingen](https://wetten.overheid.nl/BWBR0002798) | BWBR0002798 | 1 | 2002-01-01 to 2002-01-01 |
| `wet-aansprakelijkheid-olietankschepen/` | [Wet aansprakelijkheid olietankschepen](https://wetten.overheid.nl/BWBR0002976) | BWBR0002976 | 12 | 1999-02-17 to 2025-07-01 |
| `wet-op-het-centraal-testamentenregister/` | [Wet op het centraal testamentenregister](https://wetten.overheid.nl/BWBR0003080) | BWBR0003080 | 5 | 1999-10-01 to 2014-07-01 |
| `noodwet-financieel-verkeer/` | [Noodwet financieel verkeer](https://wetten.overheid.nl/BWBR0003173) | BWBR0003173 | 5 | 1998-06-01 to 2007-11-01 |
| `wet-grensoverschrijdend-vervoer-van-aan-bederf-onderhevige-levensmiddelen/` | [Wet grensoverschrijdend vervoer van aan bederf onderhevige levensmiddelen](https://wetten.overheid.nl/BWBR0003186) | BWBR0003186 | 1 | 1998-01-01 to 1998-01-01 |
| `wet-gelijke-behandeling-van-mannen-en-vrouwen/` | [Wet gelijke behandeling van mannen en vrouwen](https://wetten.overheid.nl/BWBR0003299) | BWBR0003299 | 11 | 2001-01-01 to 2026-01-01 |
| `wet-op-de-consignatie-van-gelden/` | [Wet op de consignatie van gelden](https://wetten.overheid.nl/BWBR0003338) | BWBR0003338 | 1 | 2002-01-01 to 2002-01-01 |
| `uitvoeringswet-verdrag-biologische-wapens/` | [Uitvoeringswet verdrag biologische wapens](https://wetten.overheid.nl/BWBR0003385) | BWBR0003385 | 5 | 1998-01-01 to 2025-07-05 |
| `wet-agrarisch-grondverkeer/` | [Wet agrarisch grondverkeer](https://wetten.overheid.nl/BWBR0003386) | BWBR0003386 | 20 | 2002-04-01 to 2026-06-04 |
| `wet-algemene-regels-herindeling/` | [Wet algemene regels herindeling](https://wetten.overheid.nl/BWBR0003718) | BWBR0003718 | 23 | 2002-01-01 to 2024-01-01 |
| `wet-inzake-spaarbewijzen/` | [Wet inzake spaarbewijzen](https://wetten.overheid.nl/BWBR0003797) | BWBR0003797 | 2 | 1996-06-01 to 2005-01-01 |

Each history starts at the oldest version the BWB publishes for that act: 2002 for the Grondwet and the codes (2012 for Boek 10, the act as enacted, Stb. 2011, 272), the act as enacted (Stb. 2018, 144) for the UAVG, and the dates in the table for the other acts (the Jeugdwet and the Wmo 2015 start with the act as enacted). Each folder's `README.md` lists every article, how often it changed and when.

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

`tools/geldend_op.py` takes dates as `YYYY-MM-DD` or `DD-MM-YYYY`, acts by folder name or abbreviation (`gw`, `bw1` to `bw7`, `bw10`, `sr`, `sv`, `rv`, `awb`, `aw`, `wvk`, `uavg`, or any folder name), and articles by number (`240`, `19f`, `Artikel 23`), by chapter number (`4:84a` in the Awb, file `awb/art-04-084a.md`) or, for the Grondwet's additional articles, by Roman numeral (`IX`). It is a thin wrapper around `tools/on.py`.

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## Dates

- Each commit is dated at **noon, Europe/Amsterdam, on the day the change took effect**. The day is also in the `In-force:` trailer, which the tools read; the signature (ondertekening) and Staatsblad publication dates are trailers too, where the BWB or officielebekendmakingen.nl gives them.
- **The day is the BWB's.** Each version is a BWB toestand, and its date is the toestand's in-force date (datum_inwerkingtreding), which already applies each law's own commencement provision or Royal Decree. Where a law names no date, the Bekendmakingswet (art. 10(1)) applies: the first day of the second calendar month after publication.
- Laws published but not yet in force go on the branch `toekomst`. On the retrieval day (28 October 2026) there were none.
- `--before="YYYY-MM-DD"` alone uses your clock's time of day, so a law that took effect that day may be missed before noon. Use `T23:59:59Z` as above, or the tools.

## How it is checked

- Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`. Results are in `REPRODUCE.md`.
- **Against the BWB's own XML, every version:** each version of each act, as it reads in this repository, was compared article by article and word by word with the BWB XML of that version (whose sha256 is recorded), read independently of the conversion. For every act in the table: 0 differences. The only words the files add are list markers the XML leaves implicit (a., b., 1., ...).
- **Against wetten.overheid.nl:** for the first 52 acts, the last version was compared word for word with the act as wetten.overheid.nl showed it in force on 29 and 30 October 2026: all 15,205 articles matched. For the three acts where the site's date was later (Opiumwet, Gemeentewet, Wet open overheid), the later BWB version changes no text, so it is not a separate version here. For the acts added later, at least one act in every twenty was compared word for word with an Internet Archive copy of its wetten.overheid.nl page, against the version in force on the date that page gives: 0 differences. The site's only extra entries are placeholders for repealed articles ("Vervallen per …"), notices of future changes ("Vervalt op …") and articles the BWB marks as not yet in force or repealed.
- **Every version is its own dated toestand:** each was parsed from the BWB's XML of exactly that version, whose sha256 is recorded with the version. The BWB manifests were read again on 29 October 2026 and listed no version newer than the ones built here.
- The repository is rebuilt from the same data a second time and must give identical hashes.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist, so `git blame` and `git log --author` name laws. The committer is always Lexifina.

- **Credits come only from the BWB's own notes.** Each article in a BWB toestand names the Staatsblad publication that gave it its current wording (`bron="Stb.2023-62"`) and the day that wording took effect (`inwerking`). A changed article is credited to that publication only when its `inwerking` is the version's day. A repealed article is credited to the publication on its "vervallen" entry, or, if it vanished without one, to the only publication the BWB's amendment record (WTI) lists for that day.
- **Unexplained changes** are committed by the publisher, KOOP, and labelled "unexplained" (a few per cent of all commits; `REPRODUCE.md` gives the exact count). Most are tables of headings (`inhoud.md`) or articles that disappeared on a day several laws took effect, none of them named on the articles: BW Boek 1 arts. 263a–263b on 2015-01-01, nine Criminal Code articles (240a–240c, 248a–248f) on 2024-07-01, 69 Code of Criminal Procedure articles on 2020-01-01, 17 Code of Civil Procedure articles on 2023-05-01. The rest are single articles the BWB changed without naming a source for that day (for example BW Boek 7 arts. 400–404 on 2007-10-31). `git log --author=KOOP` lists them all.
- **Annexes.** An article in an annex (bijlage) of the Awb that names no source of its own is credited to the source the BWB records for the annex, when that took effect on the version's day.
- **Staatscourant.** A few wordings (amounts adjusted by ministerial regulation, for example in BW Boek 7 and the Code of Civil Procedure) have a Staatscourant publication as their source; those authors are labelled "Stcrt." and counted as decrees.
- **Names of amending publications.** For the acts added from part 68 on, a publication the act's amendment record (WTI) names is identified by its label ("Stb. 2025, 352" or "Stcrt. YYYY, N") with the signature and publication dates the record gives; its title is given only where the record names it. Titles from officielebekendmakingen.nl are used for the earlier acts, and for a source the record does not list.
- **Grondwet revisions.** For a revised Grondwet the BWB names as the source of the wording the Besluit that publishes the revised text (Art. 141 Grondwet); that Besluit is the author, and its commit message names the revision laws the BWB lists for the same day. On 2018-12-21 the BWB dates the text before the Besluit of 16 January 2019 (Stb. 2019, 33) that published it; the date is kept as the BWB gives it.
- **The first commit** of the UAVG is the act as enacted (Stb. 2018, 144). For the Grondwet and the codes, it is the oldest version the BWB holds, credited to the publisher.
- Blame credits whole lines (one paragraph, member or list item per line). Use `git log -p --word-diff` to see exactly which words each change made.

## What it does not show

- **History before the BWB.** The BWB's versions of most acts start in 2002 (a few earlier, and later for acts made since; the table gives each act's first date); earlier changes are not separate commits, and the oldest text is one commit.
- **Repealed and not-yet-in-force articles.** Articles the BWB marks "vervallen" or "nogniet" are absent from the tree, not kept as placeholders.
- **Footnotes and metadata.** They are dropped. Editorial notes (redactie) are kept in square brackets.
- **Headings above the article** (Boek, Titel, Hoofdstuk, Afdeling, Paragraaf) are kept in one `inhoud.md` file per act, not in the article files.
- **BWB versions that change no text** (where only metadata or references changed; `REPRODUCE.md` gives the count per act) are not separate versions.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

The data is, per act, the BWB manifest (every dated version), the XML of each version and the WTI (amendment record) from the BWB repository (repository.officiele-overheidspublicaties.nl), plus the metadata of every Staatsblad or Staatscourant issue named as a source (zoek.officielebekendmakingen.nl). Each version becomes one file per article, dated by its toestand and credited from each article's `bron`; the sha256 of every version's XML is recorded with the version.

## Sources

| Source | What it gives | Used for |
| --- | --- | --- |
| [Basiswettenbestand (BWB), wetten.overheid.nl](https://wetten.overheid.nl) | Official consolidated text of every national regulation, as dated versions ("toestanden") in XML, with the source and in-force date of each article; CC0 | The text, dates and credits of every version |
| [officielebekendmakingen.nl](https://zoek.officielebekendmakingen.nl) | The Staatsblad: each publication's title, signature and publication date; CC0 | Naming the laws |
| [Internet Archive](https://web.archive.org) copies of wetten.overheid.nl pages | The act as the site showed it in force on a past day; each copy's capture date is in the data | Spot checks of the text, one act in twenty or more |
| [bwb2md](https://github.com/PatrickB-Private/bwb2md) (MIT) | A converter from BWB XML to Markdown | Not used; listed as prior art |

General research guides that cover every country: [GlobaLex](https://www.nyulawglobal.org/globalex/) and the [Law Library of Congress Guide to Law Online](https://www.loc.gov/research-centers/law-library-of-congress/researcher-resources/guide-to-law-online/).

## Licence

See [LICENSE](LICENSE). Wet- en regelgeving: Basiswettenbestand (wetten.overheid.nl), KOOP, Ministerie van Binnenlandse Zaken en Koninkrijksrelaties; open data, CC0 1.0. Dutch statutes are also outside copyright (Auteurswet art. 11). Lexifina's arrangement, messages, tables and tools are CC0.

This repository is not legal advice. The authentic text is the one published in the Staatsblad; wetten.overheid.nl is the official consolidation.

## Nederlands

Deze repository bevat Nederlandse wetgeving als git-geschiedenis: één bestand per artikel, één commit per wet op de dag van inwerkingtreding, met de Staatsbladpublicatie die de wijziging aanbracht als auteur van de commit. `git blame` toont per alinea de wet die de tekst gaf; `python tools/geldend_op.py <datum> <wet> [artikel]` toont de tekst die op een dag gold, bijvoorbeeld `python tools/geldend_op.py 21-02-2023 gw 1`.

- **Bron:** het Basiswettenbestand (BWB) achter wetten.overheid.nl (KOOP, CC0). Elke versie is een toestand van de geconsolideerde tekst, gedateerd op de datum van inwerkingtreding die het BWB geeft.
- **Inhoud:** de Grondwet (vanaf 2002), het Burgerlijk Wetboek Boeken 1 tot en met 7 (vanaf 2002) en Boek 10 (vanaf de oorspronkelijke tekst, 2012), het Wetboek van Strafrecht, het Wetboek van Strafvordering, het Wetboek van Burgerlijke Rechtsvordering, de Algemene wet bestuursrecht en de Auteurswet (alle vanaf 2002), de Uitvoeringswet AVG (vanaf de oorspronkelijke tekst, 2018) en 37 andere wetten, waaronder het Wetboek van Koophandel, de Wft, de Omgevingswet, de Vreemdelingenwet 2000, de Participatiewet, de Zorgverzekeringswet, de Wet inkomstenbelasting 2001, de AWR, de Opiumwet, de Wegenverkeerswet 1994, de Gemeentewet, de Woo, de Faillissementswet, de Arbeidsomstandighedenwet, de Wet milieubeheer, de loon-, vennootschaps- en successiebelasting, de Werkloosheidswet, de Wet WIA, de AOW, de Wet op de economische delicten, de Politiewet 2012 en de Provinciewet, en daarna steeds meer formele wetten uit het BWB, de meest aangehaalde eerst (zie de tabel). Eerdere geschiedenis staat niet in het BWB en is niet gereconstrueerd.
- **Toerekening:** een gewijzigd artikel wordt alleen toegeschreven aan de Staatsbladpublicatie die het BWB bij dat artikel als bron noemt, als de inwerkingtredingsdatum daarvan gelijk is aan de dag van de versie. Wat het BWB niet verklaart, staat als "unexplained" op naam van de uitgever.
- **Controle:** elke versie wordt op haar eigen dag en de dag ervoor teruggelezen, en woord voor woord vergeleken met de BWB-XML van die versie (geen verschillen); de laatste versie van de eerste 52 wetten is op 29 en 30 oktober 2026 woord voor woord vergeleken met wetten.overheid.nl (15.205 artikelen, geen verschillen), en van de later toegevoegde wetten minstens één op de twintig met een kopie van de pagina in het Internet Archive.
- Vervallen artikelen en artikelen die nog niet in werking zijn getreden, staan niet in de boom; wetten die wel zijn gepubliceerd maar nog niet gelden, komen op de branch `toekomst`.

Dit is geen juridisch advies. De authentieke tekst is die in het Staatsblad.
