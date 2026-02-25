# Energielabel Inschatting Tool - Project Documentatie

**Laatste update:** 9 januari 2026
**Status:** Prototype v5.20 LIVE op Render.com
**Live URL:** https://energielabel-tool.onrender.com
**GitHub:** https://github.com/rondema/energielabel-tool
**Adviseur:** M. Rondema (vakbekwaamheidsnr: 55151558)

### Deployment Info (9 jan 2026)
- **Hosting:** Render.com (gratis tier)
- **Database:** Gefilterde regio (68MB) - Amsterdam, Amstelveen, Aalsmeer, Hoofddorp
- **Postcodes:** 10xx, 11xx, 14xx, 21xx (~587.000 labels)
- **Auto-deploy:** Push naar GitHub → automatisch live binnen 2 min

---

## Inhoudsopgave

1. [Project Overzicht](#1-project-overzicht)
2. [Wat is Bereikt](#2-wat-is-bereikt)
3. [Bestanden Overzicht](#3-bestanden-overzicht)
4. [Technische Documentatie](#4-technische-documentatie)
5. [Gevalideerde Data](#5-gevalideerde-data)
6. [Volgende Stappen](#6-volgende-stappen)
7. [Hoe Verder te Werken](#7-hoe-verder-te-werken)

---

## 1. Project Overzicht

### Doel
Een energielabel inschatting tool bouwen voor een duurzaamheidswebsite waarmee gebruikers snel een indicatie kunnen krijgen van hun energielabel, vergelijkbaar met hoe een ervaren EP-adviseur ter plekke een inschatting maakt.

### Doelgroepen
- **Huiseigenaren**: Hypotheekkorting, verduurzaming plannen
- **Verkopers**: Verplicht label bij verkoop
- **Verhuurders**: WWS punten systeem
- **Makelaars**: Bulk-inschattingen (B2B potentieel)

### Twee gebruikerstypes
1. **VEL-label (pre-2021)**: Geen EP2 bekend → volledige inschatting nodig
2. **Nieuw label (post-2021)**: EP2 bekend → focus op "wat-als" scenario's

---

## 2. Wat is Bereikt

### Sessie 30 december 2025
- [x] Briefing geanalyseerd
- [x] 366 uniec3 bestanden geanalyseerd
- [x] Database aangemaakt (JSON + CSV)

### Sessie 31 december 2025
- [x] Officiële EP2 labelgrenzen vastgelegd
- [x] Praktijkkennis adviseur gedocumenteerd
- [x] Voorbeeld A+++ label geanalyseerd
- [x] Database impact per factor geanalyseerd (359 woningen)
- [x] Bouwbesluit Rc-eisen per bouwjaar opgezocht
- [x] Compactheid (Als/Ag) per woningtype vastgelegd
- [x] 4 testcases doorlopen
- [x] Tool-architectuur uitgewerkt
- [x] **Correctiefactoren gevalideerd** (exacte match!)
- [x] **Bouwjaar geëxtraheerd uit 353 uniec3 bestanden**
- [x] **Basis EP2 tabel gevalideerd en gecorrigeerd**
- [x] **Werkend prototype gebouwd** (HTML/CSS/JS)

### Sessie 3 januari 2026
- [x] EP-Online totaalbestand gedownload (5.7M labels!)
- [x] SQLite database voor lokale buurt-queries (<2ms)
- [x] Buurt labels feature met uitklapbare adressenlijst
- [x] Automatisch invullen bouwjaar/oppervlakte/woningtype
- [x] **Keuze-knoppen: Second Opinion vs Verduurzamen Simuleren**
- [x] **Vergelijkingsfunctie met officieel label**
- [x] **Zonnepanelen aangepast naar NTA8800 forfaitair (289 Wp)**
  - 175 Wp/m² × 1,65m² = 289 Wp per paneel
  - Monokristallijn silicium vanaf 2018
- [x] **EP2/VEL kolom in buurt labels tabel** (v5.5)
  - VEL = oude labels zonder EP2 waarde
  - kWh = nieuwe labels met EP2 waarde
- [x] **Buurt fallback voor onbekende adressen** (v5.6)
  - Als adres niet gevonden → buurt gemiddelden gebruiken
  - Bouwjaar, oppervlakte, woningtype automatisch ingevuld

### Sessie 4 januari 2026
- [x] **EP2 staffel tooltip** (v5.7)
  - Hover over EP2 waarde toont visuele staffel
  - Alle labels A++++ t/m G met grenswaarden
- [x] **Toevoeging veld** (v5.8)
  - Nieuw invoerveld voor huisnummer toevoeging (A, B, -1)
  - Server ondersteunt toevoeging in EP-Online lookup
- [x] **Verbeterde tabel kolommen**
  - Type kolom: Oud/Nieuw/Geen (i.p.v. VEL/kWh)
  - EP2 kolom met interactieve tooltip
- [x] **Stap terug knop** (v5.10-v5.13)
  - "← Terug" knop rechtsboven op resultaat pagina
  - Behoudt ingevulde waarden bij teruggaan
- [x] **Fix buurt labels met gevonden postcode** (v5.11)
  - Straatnaam invoer (bijv. "Nierop") werkt nu correct
  - Gebruikt gevonden postcode voor buurt query
- [x] **BAG WFS integratie** (v5.14)
  - Bouwjaar en oppervlakte nu uit officiële BAG WFS service
  - Gratis PDOK endpoint, geen API key nodig
- [x] **BAG = authoratieve bron** (v5.16)
  - Bouwjaar/oppervlakte ALTIJD uit BAG (Kadaster)
  - Geen buurt gemiddelden meer voor deze velden
  - Woningtype alleen uit EP-Online of handmatig
- [x] **Reset knop visueel verbeterd** (v5.17)
  - Gradient achtergrond, witte tekst, shadow
  - Nu duidelijk herkenbaar als knop
- [x] **CV-ketel opties op basis van leeftijd** (v5.17)
  - Gebruikers weten vaak niet welk type ketel, wel hoe oud
  - Opties: onbekend, 0-5 jaar, 5-10 jaar, 10-15 jaar, 15+ jaar
  - Oudere ketels = lagere prestatie (VR niveau bij 15+)
- [x] **Beglazing opties uitgebreid** (v5.20)
  - HR glas als aparte optie (-10 kWh/m²)
  - Mix van dubbel en HR glas (-5 kWh/m²)
  - Glassoorten: enkel (+40), dubbel (0), mix (-5), HR (-10), HR++ (-20), triple (-30)
- [x] **Documentatie basisprincipe berekeningen**
  - Nieuw: `inspiration/BASISPRINCIPE_BEREKENINGEN_ENERGIELABEL.txt`
  - Uitleg voor collega's hoe de inschatting tot stand komt
  - Bevat: basistabel, correctiefactoren, voorbeeldberekening

---

## 3. Bestanden Overzicht

### Kernbestanden

| Bestand | Beschrijving |
|---------|--------------|
| `TOOL_ARCHITECTUUR.txt` | Complete berekeningslogica v2.0 (gevalideerd) |
| `PRAKTIJKKENNIS_ADVISEUR.txt` | Trucs en beslisregels van ervaren adviseur |
| `DATABASE_ANALYSE_IMPACT.txt` | Kwantitatieve impact per factor |
| `BOUWBESLUIT_RC_EISEN_PER_BOUWJAAR.txt` | Historische isolatie-eisen |
| `energielabel_database.json` | 366 woningen met bouwjaar |
| `energielabel_database.csv` | Backup van database |
| `PROJECT_DOCUMENTATIE.md` | Dit bestand |

### Prototype

| Bestand | Beschrijving |
|---------|--------------|
| `prototype/energielabel-tool-v5.html` | Actuele versie v5.8 |
| `prototype/server.py` | Proxy server voor APIs + SQLite (poort 8892) |

### Sessie Documentatie

| Bestand | Beschrijving |
|---------|--------------|
| `Chat Conversatie/INDEX_SESSIES.txt` | Overzicht alle sessies |
| `Chat Conversatie/sessie_2025-12-31_BELANGRIJKE_INZICHTEN.txt` | Kernkennis sessie 1 |
| `Chat Conversatie/sessie_2025-12-31_DEEL2_TOOLVISIE.txt` | Tool visie en architectuur |

### Bronbestanden

| Map | Beschrijving |
|-----|--------------|
| `Energielabel/` | Voorbeeld PDF energielabels |
| `NTA8800_Kennisbank/` | Geëxtraheerde NTA 8800 (nog opschonen) |
| `COMPLETED/` (iCloud) | 366 originele uniec3 bestanden |

---

## 4. Technische Documentatie

### EP2 Labelgrenzen (Officieel)

| Label | EP2 bereik (kWh/m²) |
|-------|---------------------|
| A++++ | < 0 |
| A+++ | 0 - 50 |
| A++ | 50 - 75 |
| A+ | 75 - 105 |
| A | 105 - 160 |
| B | 160 - 190 |
| C | 190 - 250 |
| D | 250 - 290 |
| E | 290 - 335 |
| F | 335 - 380 |
| G | > 380 |

### Basis EP2 Tabel (Gevalideerd)

| Bouwjaar | Appartement | Tussenwoning | Hoek/2^1 | Vrijstaand |
|----------|-------------|--------------|----------|------------|
| Voor 1965 | 230 | 250 | 290 | 330 |
| 1965-1974 | 200 | 220 | 260 | 300 |
| 1975-1982 | 175 | 190 | 230 | 270 |
| 1983-1991 | 160 | 175 | 210 | 250 |
| 1992-1999 | 140 | 155 | 185 | 215 |
| 2000-2011 | 120 | 135 | 165 | 195 |
| 2012-2014 | 85 | 95 | 115 | 135 |
| 2015-2020 | 55 | 70 | 90 | 110 |
| 2021+ | 25 | 40 | 60 | 80 |

### Correctiefactoren (Gevalideerd ✓)

**Verwarming** (v5.17: op basis van ketelleeftijd):
| Type | Correctie | Toelichting |
|------|-----------|-------------|
| CV-ketel (onbekend) | 0 | HR 107 niveau (standaard aanname) |
| CV-ketel (tot 5 jaar) | -25 | Goed presterend, nieuw |
| CV-ketel (5-10 jaar) | -15 | Redelijk presterend |
| CV-ketel (10-15 jaar) | 0 | HR 100 niveau |
| CV-ketel (15+ jaar) | +15 | VR ketel niveau |
| Warmtepomp | -110 | -109.1 in database |
| Stadsverwarming | +30 | +29.8 in database |
| Elektrisch | +20 | +17.1 in database |

**Ventilatie** (aangepast voor correlatie):
| Type | Correctie |
|------|-----------|
| Natuurlijk | 0 |
| Mech. afzuig oud (pre-2010) | +10 |
| Mech. afzuig nieuw | -30 |
| WTW balansventilatie | -60 |

**Afgifte** (gecorrigeerd voor WP-correlatie):
| Type | Correctie |
|------|-----------|
| Radiatoren | 0 |
| Vloerverwarming | -40 |
| LT-radiatoren | -30 |

**Zonnepanelen** (NTA8800 forfaitair vanaf 2018):
```
Correctie = -(panelen × 289 × 0.9 × 1.45) / m²
```
*289 Wp = 175 Wp/m² × 1,65m² (monokristallijn silicium vanaf 2018)*

---

## 5. Gevalideerde Data

### Validatie Samenvatting

| Onderdeel | Status | Bron |
|-----------|--------|------|
| Verwarming correcties | ✓ Exact match | 285 woningen |
| Ventilatie correcties | ✓ Aangepast | 343 woningen |
| Afgifte correcties | ✓ Aangepast | 333 woningen |
| Labelgrenzen | ✓ Exact match | Alle woningen |
| Basis EP2 tabel | ✓ Gecorrigeerd | 353 woningen met bouwjaar |

### Belangrijke Inzichten

1. **Bouwjaar = Isolatie**: Bouwbesluit-eisen bepalen automatisch de basiswaarden
2. **Warmtepomp + PV = Grootste impact**: Elk >100 kWh/m² besparing
3. **Vloerisolatie = Minimale impact**: Alleen comfort, niet label
4. **Kwaliteitsverklaring = +25 kWh/m² besparing**
5. **Hoekwoning scoort ~1 label lager dan tussenwoning** (compactheid)

---

## 6. Volgende Stappen

### Afgerond ✓
1. ~~Correctiefactoren valideren tegen database~~
2. ~~Bouwjaar extraheren uit uniec3~~
3. ~~Basis EP2 tabel valideren en corrigeren~~
4. ~~Prototype bouwen~~

### Nog te doen
1. [x] ~~BAG API integratie~~ → Via PDOK/EP-Online data
2. [x] ~~EP-online.nl API toegang~~ → Lokale SQLite met 5.7M labels
3. [ ] Kennisbank opschonen (irrelevante NTA8800 weg)
4. [ ] Gebruikerstests met echte cases
5. [ ] Integratie in duurzaamheidswebsite
6. [ ] B2B makelaar dashboard (fase 2)

---

## 7. Hoe Verder te Werken

### Bij nieuwe sessie
Start met het lezen van dit bestand of de INDEX:
```
Lees /Users/markrondema/Desktop/CLAUDE PROJECTS/ENERGIELABEL BEREKENEN/PROJECT_DOCUMENTATIE.md
```

Of:
```
Lees /Users/markrondema/Desktop/CLAUDE PROJECTS/ENERGIELABEL BEREKENEN/Chat Conversatie/INDEX_SESSIES.txt
```

### Prototype testen
Start server en open in browser:
```bash
cd /Users/markrondema/Desktop/CLAUDE\ PROJECTS/ENERGIELABEL\ BEREKENEN/prototype
python3 server.py  # Start op poort 8892
open http://localhost:8892
```

### Database gebruiken
```python
import json
with open('energielabel_database.json', 'r') as f:
    data = json.load(f)
# Nu heb je 366 woningen met bouwjaar, EP2, etc.
```

---

## Contactgegevens

**Project eigenaar:** M. Rondema
**Vakbekwaamheidsnummer:** 55151558
**Project locatie:** `/Users/markrondema/Desktop/CLAUDE PROJECTS/ENERGIELABEL BEREKENEN/`

---

*Laatste update: 4 januari 2026, 16:30 - v5.20 + basisprincipe documentatie*
