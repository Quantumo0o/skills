# Qwen Orchestrator Reference

## Purpose
Operational reference for `qwen-orchestrator`.
Use this file when debugging runtime failures, daemon issues, auth problems, or selector drift.

## Architecture
- `ask-qwen.sh` — shell wrapper for normal use
- `ask-puppeteer.js` — main runtime
- `qwen-daemon.js` — persistent browser daemon for fast startup
- `auth-check.js` — Qwen-specific auth detection
- `.qwen.json` — runtime config overrides

## Expected Files
- `.daemon-ws-endpoint` — daemon websocket endpoint
- `.sessions/*.json` — saved chat/session metadata
- `.logs/qwen.log` — optional runtime log
- `.diagnostics/` — screenshots, traces, summaries on failures

## Daemon Commands
```bash
cd ~/.openclaw/workspace/skills/qwen-orchestrator
bash scripts/setup-daemon.sh
pm2 status qwen-daemon
pm2 restart qwen-daemon
pm2 stop qwen-daemon
```

## Auth Repair
If Qwen opens login/auth screens or dry-run says auth is missing:
```bash
cd ~/.openclaw/workspace/skills/qwen-orchestrator
pm2 stop qwen-daemon
rm -f .daemon-ws-endpoint
bash ask-qwen.sh --visible --wait --dry-run
pm2 start qwen-daemon
bash ask-qwen.sh --dry-run --daemon
```

## Lock Repair
If Chromium profile lock errors appear:
```bash
cd ~/.openclaw/workspace/skills/qwen-orchestrator
rm -f .profile/Singleton*
pm2 restart qwen-daemon
bash ask-qwen.sh --dry-run
```

## Manual Smoke Tests
```bash
# CLI help
bash ask-qwen.sh --help

# Auth + composer only
bash ask-qwen.sh --dry-run

# Daemon path
bash ask-qwen.sh --dry-run --daemon

# Real prompt
bash ask-qwen.sh "Say OK"

# Session path
bash ask-qwen.sh --session test "Say OK"
bash ask-qwen.sh --session test --end-session
```

## Known Risks
- Qwen DOM/selectors may drift.
- Daemon mode depends on a valid `.daemon-ws-endpoint`.
- Search toggle may need selector updates if chat.qwen.ai UI changes.
- Browser auth state is profile-backed; profile corruption can require re-login.
