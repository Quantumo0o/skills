---
name: ghibli-style-skill
description: Generate ghibli style images using the Neta AI API. Returns a direct image URL.
tools: Bash
---

# Ghibli Style Image Generator

Generate stunning studio ghibli ai art generator images from a text description. Get back a direct image URL instantly.

## When to use
Use when someone asks to generate or create studio ghibli ai art generator images.

## Quick start
```bash
node ghiblistyle.js "your description here"
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)


## Token

Requires a Neta API token via `NETA_TOKEN` env var or `--token` flag.
- Global: <https://www.neta.art/open/>
- China:  <https://app.nieta.art/security>

```bash
export NETA_TOKEN=your_token_here
```

## Install
```bash
npx skills add wkl-nieta/ghibli-style-skill
```
