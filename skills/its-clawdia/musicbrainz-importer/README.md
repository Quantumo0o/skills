# MusicBrainz Importer

An [OpenClaw](https://openclaw.ai) skill for looking up and adding music metadata on [MusicBrainz](https://musicbrainz.org).

## What it does

- **Look up** artists, releases, and release groups on MusicBrainz via API
- **Find** MusicBrainz entries linked to Spotify URLs
- **Add artists** to MusicBrainz via browser automation (Playwright)
- **Add releases** with full metadata: tracklists, release dates, Spotify links, cover art
- **Upload cover art** from Spotify to MusicBrainz releases

## Requirements

- **Node.js** (for Playwright scripts)
- **Playwright** with Chromium (`npx playwright install chromium`)
- **curl** and **jq** (for API lookups)
- A [MusicBrainz account](https://musicbrainz.org/register) (for write operations)

## Install

### Via ClawHub

```bash
openclaw skills install musicbrainz-importer
```

### Manual

Clone into your OpenClaw skills directory:

```bash
git clone https://github.com/its-clawdia/musicbrainz-importer.git ~/.openclaw/skills/musicbrainz
```

## Setup

Store your MusicBrainz credentials for write operations:

```bash
cat > ~/.openclaw/skills/musicbrainz/.credentials.json << 'EOF'
{"username": "YOUR_MB_USERNAME", "password": "YOUR_MB_PASSWORD"}
EOF
```

Verify with:

```bash
bash ~/.openclaw/skills/musicbrainz/scripts/preflight.sh
```

## License

MIT
