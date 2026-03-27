# Akkualle SEO Plugin

Automatisches SEO-Monitoring und Content-Optimierung für akku-alle.de

## Features

- Tägliches SEO-Audit (via v9 API)
- META_DESCRIPTION Checks (max 155 chars)
- THIN_CONTENT Detection (min 500 Wörter)
- Keyword-Ranking Tracking (GSC)
- Automatische Content-Vorschläge

## CLI Commands

```bash
# SEO Audit starten
python3 ~/.openclaw/skills/akkualle-seo/seo_audit.py

# Meta Descriptions fixen
python3 ~/.openclaw/skills/akkualle-seo/fix_meta.py

# Thin Content erweitern
python3 ~/.openclaw/skills/akkualle-seo/expand_content.py
```

## API Integration

**v9 API Endpoint:** `POST https://akku-alle.de/api/admin`
**Secret:** `akkualle-johny-2026-geheim`

**Verfügbare Actions:**
- `v9.health` - Health Check
- `v9.seo.auditAll` - SEO Audit
- `v9.content.gaps` - Content Lücken finden
- `blog.update` - Blog Posts aktualisieren

## Cron Jobs

```bash
# Täglich um 06:00 SEO Audit
0 6 * * * python3 ~/.openclaw/skills/akkualle-seo/seo_audit.py
```

## Monetarisierung

Dieser Skill kann auf ClawHub veröffentlicht werden:
- **Preis:** 19€/Monat
- **Zielgruppe:** E-Commerce, Affiliate-Seiten
- **USP:** v9 API Integration + Auto-Fix
