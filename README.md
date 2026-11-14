# Nederland: wetgevingsgeschiedenis in git

**Nederlands** · **[Or read it in English](README.en.md)**

<picture>
<source media="(prefers-color-scheme: dark)" srcset="data/nl/effort-dark.svg">
<img alt="De wetgeving van Nederland in deze repository: wat erin staat, wijzigingen per jaar van inwerkingtreding, volledigheid ten opzichte van de officiële bronnen en juistheid van wat is opgenomen" src="data/nl/effort-light.svg" width="880">
</picture>

Het recht van Nederland als git-geschiedenis: één bestand per artikel, één commit per versie op de dag waarop die in werking trad, en als auteur van elke commit de regeling die de wijziging aanbracht, aangeduid met haar publicatie in het Staatsblad of de Staatscourant. `git blame` noemt bij elk artikel de regeling die erachter zit; `git log` toont elke wijziging van een artikel; met een datum krijgt u de tekst die op die dag gold.

Onderdeel van [lexifina/global-law](https://github.com/lexifina/global-law), één git-geschiedenis van het recht van alle landen: dit is het nationale recht van Nederland, dat global-law inleest onder `netherlands/national/acts/`.

**Wat er nu in staat:** de Grondwet, het Statuut voor het Koninkrijk en 42.434 regelingen uit het Basiswettenbestand (3.507 wetten, 4.851 algemene maatregelen van bestuur en koninklijke besluiten, 21.392 ministeriële regelingen, 6.520 regelingen van zelfstandige bestuursorganen en voormalige productschappen, 2.815 beleidsregels, circulaires en reglementen, en 3.349 verdragen), met 72.144 versies; en 853 lokale regelingen van de provincies Drenthe en Flevoland, met 1.343 versies. [`PLAN.md`](PLAN.md) somt elk onderdeel op dat deze repository moet gaan bevatten en hoe ver elk onderdeel is; [`local/README.md`](local/README.md) somt de lokale regelingen per overheid op.

Elke regeling staat in `<soort>/<jaar>/<nummer>/`, naar haar eerste publicatie in het Staatsblad (wetten en koninklijke besluiten) of de Staatscourant (de rest): `wet/1991/600-BWBR0005290/` is Burgerlijk Wetboek Boek 7, waarvan titel 10 de arbeidsovereenkomst is, met het BWB-id erbij omdat Stb. 1991, 600 ook de Boeken 3, 5 en 6 bevat; de Grondwet staat in [`grondwet/1815/`](grondwet/1815/). Verdragen staan in `verdrag/<jaar van sluiting>/<verdragnummer>/` en lokale regelingen in `local/<overheid>/<jaar>/<CVDR-id>/`. Tot 13 november 2026 waren de regelingen mappen met hun id als naam (`bw-boek-7/`); [`data/paths.json`](data/paths.json) koppelt elk id aan zijn map.

De tekst is in het Nederlands, zoals het BWB en het CVDR hem publiceren; verdragen staan er ook in de andere talen waarin het BWB ze geeft. Een Engelse vertaling maakt geen deel uit van dit archief.

## Vragen als git-commando's

| Vraag | Commando |
| --- | --- |
| Elke wijziging van artikel 7:670 BW (opzegverboden) | `git log -p --follow --word-diff -- wet/1991/600-BWBR0005290/art-670.md` |
| Welke regeling schreef elke regel van artikel 7:670? | `git blame wet/1991/600-BWBR0005290/art-670.md` |
| Elke versie van Boek 7, met de dag waarop die in werking trad | `git log --format="%h %(trailers:key=In-force,valueonly,separator=) %an" -- wet/1991/600-BWBR0005290 bw-boek-7` |
| Artikel 7:670 zoals het gold op 1 januari 2015 | `python tools/geldend_op.py 2015-01-01 bw7 670` |

**Buiten git** bieden we dit archief ook openbaar en gratis aan:

- **[Vraag Claude naar het Nederlandse recht](https://global-law.lexifina.com/v1/try_claude?country=netherlands)**: opent Claude met een eerste vraag klaar.
- **[Vraag het ChatGPT](https://global-law.lexifina.com/v1/try_chatgpt?country=netherlands)**: dezelfde vraag in ChatGPT.
- **[Roep de API aan in uw browser](https://global-law.lexifina.com/v1/search_law?query=vakantiedagen&jurisdictions=netherlands)**: een zoekopdracht naar „vakantiedagen” in het Nederlandse recht, met het antwoord in JSON. De documentatie staat [hier](https://lexifina.com/api/global-law).

Beide assistenten lezen het archief via de gratis Global law-connector (MCP, `https://global-law.lexifina.com/mcp`); de eerste keer geeft de chat u de link waarmee u de connector toevoegt. Stel uw vraag in het Nederlands of in het Engels.

**Eenvoudig zelf te draaien.** U hebt alleen git en Python nodig, en de tools draaien op uw eigen computer:

```sh
git clone --depth 1 https://github.com/lexifina/global-law && cd global-law
python3 tools/countries.py add netherlands/national/acts
python3 tools/law.py show 2026-01-01 netherlands/national/acts/wet/1991/600-BWBR0005290/art-670.md
```

Geopend in Claude Code, Cursor, VS Code of Codex start de kloon ook een lokale MCP-server met dezelfde tools ([MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md)).

## Datums

Elke commit is gedateerd om 12.00 uur Amsterdamse tijd (Europe/Amsterdam) op de dag waarop de versie in werking trad, en die dag staat ook in de trailer `In-force:`:

- bij een nationale regeling de datum van inwerkingtreding die het BWB voor elke geconsolideerde versie geeft (`datum_inwerkingtreding`), waarin de eigen inwerkingtredingsregels van de regeling al zijn verwerkt;
- bij een lokale regeling de dag die het CVDR voor elke versie geeft;
- git kan geen data vóór 1970 opslaan, daarom zijn de 1.100 oudere versies gedateerd vanaf 1970-01-01, met telkens één seconde ertussen, en staat de echte dag in `In-force:`. Vraag naar een datum met `tools/geldend_op.py`, niet met `git log --before`.

Elke wijziging wordt toegeschreven aan de publicatie die het BWB of het CVDR ervoor noemt (`Stb. 2014, 504`, `prb-2026-18788 (Drenthe)`); noemt de bron er geen, dan aan KOOP, de uitgever. De eerste versie van elke regeling is de oudste die het BWB bewaart (bij de wetboeken vanaf 2002), toegeschreven aan KOOP.

## Hoe het wordt gecontroleerd

- Nationale versies worden uit git teruggelezen op de dag waarop elk ervan in werking trad en op de dag ervoor, en moeten overeenkomen met het corpus (`tools/check_repo.py`); [`REPRODUCE.md`](REPRODUCE.md) legt de uitkomsten vast.
- Elke lokale regeling wordt woord voor woord gecontroleerd tegen de XML van het CVDR; een regeling die niet slaagt, wordt achtergehouden en later opnieuw geprobeerd.
- De trailers van elke commit zijn geldig; er zijn geen merge-commits en geen commits gedateerd na de build.
- De geschiedenis wordt alleen aangevuld: `main` groeit alleen, en geen gepubliceerde commit wordt herschreven.

## Wat er niet in staat

- **Het meeste lokale recht.** 853 van de 285.881 lokale regelingen in het CVDR staan hier; de andere 10 provincies, alle 342 gemeenten, de 21 waterschappen, gemeenschappelijke regelingen en de Caribische openbare lichamen nog niet.
- **Eerdere versies van veel regelingen.** 72.144 van de 148.873 geconsolideerde versies in het BWB staan hier; 7.934 regelingen zijn alleen met hun huidige tekst opgenomen, en de geschiedenis vóór de oudste versie in het BWB wordt niet gereconstrueerd.
- **Enkele nationale regelingen.** 4.624 van de 47.060 regelingen in het BWB staan hier niet, de meeste ingetrokken of vervallen.
- **EU-recht, wetsvoorstellen en Kamerstukken, de adviezen van de Raad van State en de teksten van de publicatiebladen zelf** zijn geplande onderdelen (zie `PLAN.md`).
- **Rechtspraak** staat in 15 afzonderlijke repositories, met 932.076 uitspraken (opgesomd in `PLAN.md`).

## Bronnen

| Bron | Soort | Eerdere versies | Opmerkingen |
| --- | --- | --- | --- |
| [Basiswettenbestand](https://wetten.overheid.nl) (KOOP) | Officiële geconsolideerde nationale wetgeving en verdragen | ja, elke geconsolideerde versie die het BWB bewaart | De tekst van elke versie, de dag van inwerkingtreding en de publicatie achter elke wijziging |
| [Officiële bekendmakingen](https://zoek.officielebekendmakingen.nl) | Staatsblad, Staatscourant, provinciebladen | zoals gepubliceerd | De publicatie van elke wijziging en haar data |
| [CVDR](https://lokaleregelgeving.overheid.nl) (KOOP) | Lokale regelingen | ja, elke geconsolideerde versie die het CVDR bewaart | Regelingen van alle Nederlandse overheden; tot nu toe Drenthe en Flevoland |

## Licentie

Zie [`LICENSE`](LICENSE). KOOP publiceert het BWB en officielebekendmakingen.nl als open data onder CC0 1.0, op Nederlandse wetten, besluiten en verordeningen rust geen auteursrecht (art. 11 Auteurswet), en elk CVDR-record vermeldt dat het vrij is van auteursrecht en databankrecht. De geschiedenis, de commitberichten, de tabellen en de tools zijn CC0 1.0.

Geen enkel AI-model heeft wettekst geschreven of gewijzigd; de scripts zijn geschreven door een AI-model (zie [`REPRODUCE.md`](REPRODUCE.md)).

Dit is een vertaling van de Engelse versie ([README.en.md](README.en.md)); bij verschillen geldt de Engelse versie.

## Meer

Uit de repository [lexifina/global-law](https://github.com/lexifina/global-law) (in het Engels):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): alle functies en wat elk corpus moet ondersteunen (`git blame`, `law.py`, MCP-tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): vragen en antwoorden · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): wijzigingen voorstellen · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): MCP-server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): hoe het is gemaakt · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): hoe actueel elk corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): of de updates werken · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): hoe elke officiële bron op wijzigingen wordt gevolgd
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): hoe snel de tools zijn, gemeten
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): grafieken en verbanden in het recht van de hele wereld
- [Kwetsbaarheden](https://github.com/lexifina/global-law/tree/main/vulnerabilities): fouten in regelingen zoals ze zijn gepubliceerd
