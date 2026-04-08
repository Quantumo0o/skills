---
name: qwen-orchestrator
description: >
  Qwen Chat (chat.qwen.ai) access via Puppeteer browser automation with CDP interceptor.
  Persistent daemon (~35ms startup), health checks, graceful shutdown, PM2 management.
  Configurable via `.qwen.json`. Use when: (1) need Qwen responses without API key,
  (2) code analysis, review, or generation, (3) text analysis, summarization, translation,
  (4) web search via Qwen's built-in search, (5) "consult Qwen" or ask-qwen.sh.
---

# Qwen Orchestrator v1.2.0

**What this is:** Browser automation that talks to Qwen Chat via Puppeteer.
**Default runtime policy:** before sending a prompt, qwen-orchestrator should switch the Qwen mode selector to thinking mode when the selector is available.
**What this is NOT:** A general AI router or multi-model orchestrator. It's one browser → one LLM.

## Execution

**Working directory rule:** Unless a command here uses an absolute path, run qwen-orchestrator commands from the skill root: `~/.openclaw/workspace/skills/qwen-orchestrator`.
If you are not already there, run:

```bash
cd ~/.openclaw/workspace/skills/qwen-orchestrator
```

## Quick Start
```bash
# Simple question
ask-qwen.sh "What is HTTP?"

# Session (keeps context between questions)
ask-qwen.sh "Explain OAuth2" --session work
ask-qwen.sh "What about OpenID Connect?" --session work
ask-qwen.sh --session work --end-session

# With daemon (fast startup ~35ms vs ~15s cold)
ask-qwen.sh "Question" --daemon

# With web search
ask-qwen.sh "Latest news about AI" --search

# Pipe content
cat code.py | ask-qwen.sh "Find bugs"
ask-qwen.sh --stdin < code.py
ask-qwen.sh <<'EOF'
Long multi-line prompt here
EOF
```

## When to use qwen-orchestrator

| Task | qwen-orchestrator | Direct API | Manual browser |
|------|-------------------|------------|----------------|
| Code analysis / review | ✅ Fast, no API key | Needs API | ❌ Slow |
| Text analysis / summary | ✅ (with --daemon) | Needs API | ❌ Tedious |
| Web search via Qwen | ✅ (with --search) | Needs API | ❌ |
| Brainstorming | ❌ (Dual Thinking) | Needs API | ❌ |
| Web scraping | ❌ Wrong tool | ❌ | ✅ |

**Rule:** Need LLM reasoning without API key → qwen-orchestrator.
Need browser tasks (scrape, click, fill forms) → use `agent-browser` skill instead.

## All Flags
| Flag | Purpose |
|------|---------|
| `--session NAME` | Persistent context across requests |
| `--daemon` | Use running Chrome daemon (~35ms startup) |
| `--search` | Enable Qwen web search |
| `--new-chat` | Start new chat within existing session |
| `--end-session` | Close and clean up session |
| `--visible` | Open visible browser (for auth/CAPTCHA fixes) |
| `--wait` | Wait for manual auth completion (with --visible) |
| `--close` | Force close browser after request |
| `--dry-run` | Test auth + composer without sending prompt |
| `--stdin` | Explicitly read prompt body from stdin |
| `--debug` | Verbose debug output |
| `--verbose` | More detailed logs |
| `-h, --help` | Show help |

## Health check
```bash
# 1. Daemon running?
pm2 status | grep -q "qwen-daemon.*online" || echo "Daemon down"

# 2. Dry-run path works?
ask-qwen.sh --dry-run --daemon || echo "Qwen dry-run failed"

# 3. Real response path works?
ask-qwen.sh "OK" --daemon | grep -q "OK" || echo "Qwen not responding"
```

## Failure Recovery (mandatory routing)

### Symptom → exact command
| If you see this symptom | Run this exact command | Then verify with |
|---|---|---|
| `Connection refused`, daemon not online | `pm2 restart qwen-daemon && sleep 8 && ask-qwen.sh --dry-run --daemon` | `ask-qwen.sh "Say OK" --daemon` |
| `auth expired`, `CAPTCHA`, login page | `cd ~/.openclaw/workspace/skills/qwen-orchestrator && pm2 stop qwen-daemon && rm -f .daemon-ws-endpoint && bash ask-qwen.sh --visible --wait --dry-run && pm2 start qwen-daemon` | `bash ask-qwen.sh --dry-run --daemon` |
| response cuts off | `ask-qwen.sh "Part 1" --session temp && ask-qwen.sh "Continue" --session temp` | `ask-qwen.sh --session temp --end-session` |
| `lock`, `Singleton`, profile already in use | `cd ~/.openclaw/workspace/skills/qwen-orchestrator && rm -f .profile/Singleton* && pm2 restart qwen-daemon` | `bash ask-qwen.sh --dry-run` |
| selector not found | `ask-qwen.sh --dry-run --visible` | only after manual inspection consider selector edits |

## Daemon Setup
```bash
cd ~/.openclaw/workspace/skills/qwen-orchestrator && bash scripts/setup-daemon.sh
```

## Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success — response received |
| 1 | Config/arg error or runtime failure |

## Configuration (.qwen.json)
```json
{
  "browserLaunchTimeout": 30000,
  "answerTimeout": 600000,
  "composerTimeout": 10000,
  "navigationTimeout": 30000,
  "idleTimeout": 15000,
  "heartbeatInterval": 15000,
  "domErrorIdleMs": 25000,
  "maxContinueRounds": 30,
  "logToFile": true,
  "logPath": ".logs/qwen.log"
}
```

## Minimal Decision Rules

- Need fastest normal run → `--daemon`
- Need context across prompts → `--session`
- New Qwen chat → `--new-chat`
- Close chat → `--end-session`
- Before sending a prompt → force the Qwen mode selector to thinking mode if the selector exists
- Auth repair → stop daemon → `--visible --wait --dry-run`
- Health check → `--dry-run`
- Long answers → `--session` + chunk
- Browser automation → use `agent-browser`
- Need deeper runtime details or repair commands → read `REFERENCE.md`. Purpose: debug failures.
