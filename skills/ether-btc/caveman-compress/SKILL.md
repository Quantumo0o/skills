---
name: caveman-compress
description: >
  Compress workspace bootstrap files into caveman-speak to reduce input tokens
  on every session load. Creates .original.md backups before overwriting.
triggers:
  - "/caveman:compress <filepath>"
  - "compress memory file"
  - "caveman compress"
deactivation: null
persistence: none  # Single-shot operation
---

# Caveman Input Compression Skill

## Identity

Compress natural language workspace files into caveman-speak (~45% fewer input tokens). Creates `.original.md` backup before overwriting.

## Supported Files

Always safe to compress:
- `SOUL.md` ✅
- `IDENTITY.md` ✅
- `USER.md` ✅

Feature-flagged (requires env var set):
- `AGENTS.md` 🔒 (`CAVEMAN_COMPRESS_AGENTS=1`)
- `HEARTBEAT.md` 🔒 (`CAVEMAN_COMPRESS_HEARTBEAT=1`)
- `MEMORY.md` 🔒 (`CAVEMAN_COMPRESS_MEMORY=1`)

## Security

- No shell=True in subprocess calls
- No user content as shell arguments
- Files >500KB rejected
- `.original.md` backup created before overwrite
- Aborts if backup already exists (prevents accidental overwrite)

## API Fallback Chain

Models tried in order:
1. **claude CLI** (desktop auth) - Primary
2. **MiniMax** (OpenAI-compatible) - Requires `MINIMAX_BASE_URL` + `MINIMAX_API_KEY`
3. **DeepSeek** (OpenAI-compatible) - Requires `DEEPSEEK_API_KEY`

Uses subprocess + curl, no OpenAI SDK required.

## Usage

```bash
# Compress a specific file
python3 -m skills.caveman_compress.scripts.compress /home/pi/.openclaw/workspace/SOUL.md

# Dry run (no write, just preview)
python3 -m skills.caveman_compress.scripts.compress --dry-run /home/pi/.openclaw/workspace/SOUL.md

# Feature flags (environment variables)
CAVEMAN_COMPRESS_AGENTS=1 /home/pi/.openclaw/workspace/scripts/caveman-enable.sh
```

## Model Override

Set `COMPRESSION_MODEL` env var to use specific model:
```bash
COMPRESSION_MODEL=deepseek32 python3 -m skills.caveman_compress.scripts.compress SOUL.md
```

Default: `deepseek32` (cheap, fast)

## References

- Upstream: https://github.com/JuliusBrussee/caveman
- Paper: arXiv 2604.00025 — "Brevity Constraints Reverse Performance Hierarchies"
- Project: memory/projects/caveman-token-reducer/
