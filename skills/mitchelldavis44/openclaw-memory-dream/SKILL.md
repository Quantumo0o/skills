# Memory Dream

Auto-consolidates agent memory files after sessions — like REM sleep for AI agents.

## What it does

After a configurable number of sessions, Memory Dream wakes up in the background, reads your `MEMORY.md` + daily logs, and asks an LLM to prune stale context and tighten what remains. It writes the consolidated version back and commits it.

Without it: `MEMORY.md` grows unbounded until it gets truncated on load.  
With it: memory stays tight, relevant, and useful automatically.

## Installation

```bash
openclaw plugins install @mitchelldavis44/openclaw-memory-dream
```

## Configuration (openclaw.json)

```json
{
  "plugins": {
    "memory-dream": {
      "minSessions": 5,
      "minHours": 24,
      "model": "anthropic/claude-haiku-4"
    }
  }
}
```

| Option | Default | Description |
|--------|---------|-------------|
| `minSessions` | `5` | Sessions since last consolidation before triggering |
| `minHours` | `24` | Hours since last consolidation before triggering |
| `model` | Haiku | LLM used for consolidation (cheap model recommended) |

## How it works

1. `session_end` hook fires after each conversation
2. Scheduler checks trigger conditions (session count + time elapsed)
3. If triggered: acquires lock, reads MEMORY.md + daily logs via LCM summaries
4. Calls configured LLM to consolidate — removing stale entries, tightening what remains
5. Writes consolidated memory back, commits to git
6. Releases lock, resets session counter

## Tools

- `memory_dream_status` — returns session count since last consolidation, time since last run, next trigger estimate, and whether consolidation is currently running
