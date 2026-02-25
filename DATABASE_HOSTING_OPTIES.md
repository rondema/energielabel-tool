# Database Hosting Opties - Energielabel Tool

## Huidige Situatie (9 januari 2026)
- **Gefilterde database:** 68MB (alleen regio Amsterdam/Amstelveen/Aalsmeer/Hoofddorp)
- **Hosting:** Render.com (gratis tier)
- **URL:** https://energielabel-tool.onrender.com
- **Beperking:** Alleen postcodes 10xx, 11xx, 14xx, 21xx

## Opties voor Volledige Database (5.7M labels, 1GB)

### Optie 1: Supabase (PostgreSQL)
- **Kosten:** Gratis tot 500MB, daarna $25/maand
- **Voordelen:** Makkelijke setup, goede documentatie
- **Nadelen:** 500MB limiet te klein voor volledige database
- **URL:** https://supabase.com

### Optie 2: PlanetScale (MySQL)
- **Kosten:** Gratis tot 5GB
- **Voordelen:** Ruim genoeg voor volledige database
- **Nadelen:** MySQL ipv SQLite (kleine aanpassingen nodig)
- **URL:** https://planetscale.com

### Optie 3: Neon (PostgreSQL)
- **Kosten:** Gratis tot 512MB, daarna $19/maand
- **Voordelen:** Serverless, snel
- **Nadelen:** Gratis tier te klein
- **URL:** https://neon.tech

### Optie 4: Render PostgreSQL
- **Kosten:** Gratis 90 dagen, daarna $7/maand
- **Voordelen:** Alles bij één provider
- **Nadelen:** Betaald na 90 dagen
- **URL:** https://render.com

### Optie 5: DigitalOcean VPS
- **Kosten:** $6/maand (1GB RAM droplet)
- **Voordelen:** Volledige controle, alle data
- **Nadelen:** Zelf beheren
- **URL:** https://digitalocean.com

### Optie 6: Railway
- **Kosten:** $5/maand na gratis credits
- **Voordelen:** Simpele setup
- **URL:** https://railway.app

## Aanbeveling
Voor productie met heel Nederland: **PlanetScale** (gratis 5GB) of **DigitalOcean** ($6/maand).

Voor nu is de gefilterde database (regio) voldoende voor testen en demonstraties.
