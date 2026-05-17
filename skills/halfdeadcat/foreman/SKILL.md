---
name: foreman
description: Orchestrate sub-agent workers and shell jobs with progress tracking, cron-based heartbeat monitoring, crash detection, and alerting. Use when spawning sub-agents for parallel tasks, running background shell jobs/builds/deploys, or when work needs to survive session restarts.
---

# Foreman — Work Orchestration

## Overview

Foreman provides three orchestration modes:

1. **Agent Tasks** — spawn sub-agents via `sessions_spawn`, track via `.foreman/*.json` status files. Pair with ClawFlow for durable flow identity.
2. **Shell Jobs** — bash scripts/builds/deploys with automatic Slack heartbeats, crash detection, and cron-based monitoring.
3. **Hybrid** — agent creates a ClawFlow flow, then spawns a shell job as one of its tasks. Cron monitor catches crashes even if the agent session dies.

---

## Mode 1: Agent Tasks (recommended: pair with ClawFlow)

**When to use:** sub-agents, ACP sessions, multi-step async work, anything that needs to survive session restarts.

**Use ClawFlow for:** flow identity, durable state, waiting across sessions.  
**Foreman adds:** exec hygiene conventions, model selection, spawn-time instructions, status files.

**Fallback (if ClawFlow unavailable):** write `.foreman/*.json` status files manually (see schema below).

### Worker Prompt Template

Include this in every `sessions_spawn` task. Replace `{TASK}`, `{RUN_ID}`, `{LABEL}`, and `{PARENT_SESSION}`.

```
You are a Foreman worker (🤖 {LABEL}).

TASK: {TASK}

RULES:
1. Report progress to the main agent using: sessions_send(sessionKey="{PARENT_SESSION}", message="🤖 [{LABEL}]: your update")
2. Send updates when: starting, completing major steps, encountering errors, finishing
3. Write status updates to ~/.openclaw/workspace/.foreman/{RUN_ID}.json using this format:
   {"run_id":"{RUN_ID}","label":"{LABEL}","status":"running","step":"current step description","progress":50,"error":null,"question":null,"updated":"ISO-8601"}
4. Valid status values: "starting", "running", "blocked", "error", "done"
5. Update the status file at each major step and when finishing
6. If you need clarification or hit an unrecoverable error, set status to "blocked" with a "question" field, send a sessions_send with your question, then STOP and wait for a steer message
7. On completion, set status to "done" with progress 100
8. Do NOT message Discord/Slack directly — always go through sessions_send to the main agent

EXEC HYGIENE (mandatory — context blowup prevention):
- Pipe ALL potentially verbose commands through `tail -20` or `grep -E 'ERROR|WARN|success|done|failed'`
- Examples: `docker build ... 2>&1 | tail -20`, `pip install ... 2>&1 | tail -10`
- Never let raw build logs, install output, or long file listings land unfiltered in context
- If a command produces >50 lines, it must be filtered
```

### Status File Schema

Path: `~/.openclaw/workspace/.foreman/<run-id>.json`

```json
{
  "run_id": "uuid",
  "label": "descriptive-name",
  "status": "starting|running|blocked|error|done",
  "step": "human-readable current step",
  "progress": 0,
  "error": "error message or null",
  "question": "question for foreman or null",
  "updated": "2026-03-05T20:00:00Z"
}
```

### Spawn Steps

```
1. Generate run ID: $(uuidgen | tr '[:upper:]' '[:lower:]')
2. Create status dir: mkdir -p ~/.openclaw/workspace/.foreman
3. Write initial status file with status "starting"
4. ⚠️  COMPACT PARENT SESSION before spawning (mandatory — prevents context overflow deadlock)
   bash skills/foreman/scripts/compact-before-spawn.sh "<current-session-key>"
   • Trims parent session to last 8 exchange pairs + synthetic summary
   • Reloads session in gateway so it takes effect immediately
   • Get current session key from runtime metadata (e.g. "agent:main:slack:direct:u0am4blbuuw")
   • Skip only if session is brand new (<20 lines)
5. sessions_spawn with worker prompt template above
6. Track childSessionKey for steer/kill
```

**Why compaction matters:** When a sub-agent announces completion, the parent session must have enough headroom to receive it. A bloated parent (>30 messages) causes the announce to fail, retrying 4×120s = 8-minute deadlock. Compact first, spawn second.

### Handle Blocked Workers

When a worker sets `status: "blocked"`:
1. Read the question from the status file
2. Answer it yourself or relay to user
3. `subagents(action=steer, target=<session>, message=<answer>)` to unblock
4. Worker updates status back to "running"

---

## Mode 2: Shell Jobs

**When to use:** bash scripts, builds, deploys, data pipelines — anything running as an OS process.

### Lifecycle

```
job_init "$JOB_ID" "$LABEL"      # Write /tmp/swabby-jobs/<id>.json + .pid
job_register_cron "$JOB_ID"      # Install 5-min cron heartbeat
job_trap "$JOB_ID"               # Set EXIT trap → ✅/❌ alert + cleanup

job_progress "$JOB_ID" "Phase 2" # Update progress message (call anytime)
```

- **Heartbeat:** monitor.sh sends Slack update every 5 minutes with label + elapsed time
- **Clean exit:** trap fires → sends ✅/❌ → removes cron → deletes status files
- **Crash:** monitor.sh notices dead PID → sends ⚠️ alert → cleans up

### Template

```bash
# 1. Copy the template
cp skills/foreman/scripts/template-wrapper.sh scripts/jobs/my-job.sh

# 2. Edit: set JOB_ID, LABEL, replace job logic section
# 3. Test manually first
bash scripts/jobs/my-job.sh

# 4. Run in background when ready
bash scripts/jobs/my-job.sh &
```

### Status Files

Path: `/tmp/swabby-jobs/<job_id>.json`

```json
{
  "job_id": "my-job-1234567890",
  "label": "My Job",
  "pid": 12345,
  "started": 1712345678,
  "progress": "Phase 2 of 3",
  "last_update": 1712345900
}
```

---

## Mode 3: Hybrid

Agent creates a ClawFlow flow → spawns shell job as one of its tasks.

```
1. Create ClawFlow flow for identity + state
2. Use job wrapper for the OS-level work
3. Cron monitor catches crashes even if agent session dies
4. Flow completion requires both: agent task done + shell job exit 0
```

This gives you durable state (ClawFlow), structured output, AND crash-safe monitoring.

---

## Configuration

| Env var | Default | Purpose |
|---------|---------|---------|
| `FOREMAN_ALERT_TARGET` | `$SLACK_TO` | Who receives alerts (user ID) |
| `FOREMAN_ALERT_CHANNEL` | `$SLACK_CHANNEL` or `slack` | Which channel |

Backward compatible: if `FOREMAN_ALERT_TARGET` is unset, falls back to `SLACK_TO`. Same for channel.

Set in shell before running a job, or export in `~/.bashrc`:
```bash
export FOREMAN_ALERT_TARGET="U0AM4BLBUUW"
export FOREMAN_ALERT_CHANNEL="slack"
```

---

## Context Hygiene (CRITICAL)

See full reference: `references/exec-hygiene.md`

Short version:
- Pipe all verbose commands through `tail -20` or `grep -E 'ERROR|WARN|...'`
- Always set `runTimeoutSeconds` on workers (never 0)
- Exec-heavy workers: use `model: "anthropic/claude-sonnet-4-6"`, not inherited Opus

---

---

## Agent Task Monitor (`agent-monitor.sh`)

A cron-based monitor that watches `~/.openclaw/workspace/.foreman/*.json` for active agent tasks and sends Slack alerts.

**What it does:**
- Scans all `.foreman/*.json` files every 2 minutes
- Sends status updates to Slack for recently-updated tasks (age < 2 min)
- Alerts once per task that goes stale (no update > 10 min): `⚠️ [label]: STALE — status - step (progress%) — no update for Nmin`
- Cleans up terminal tasks (`done|error|completed`) older than 60 minutes
- Prevents overlapping runs via lock file
- Deduplicates stale alerts via `/tmp/agent-monitor-state.json`

**Cron install:**
```bash
# Check current crontab first
crontab -l

# Add (if not already present)
(crontab -l 2>/dev/null; echo '*/2 * * * * /home/swabby/repos/swabby-brain/skills/foreman/scripts/agent-monitor.sh >> /tmp/agent-monitor.log 2>&1') | crontab -
```

**Configuration:**
| Env var | Default | Purpose |
|---------|---------|--------|
| `FOREMAN_ALERT_TARGET` | `U0AM4BLBUUW` | Slack user ID to alert |
| `FOREMAN_ALERT_CHANNEL` | `slack` | Channel for alerts |
| `STALE_THRESHOLD_MIN` | `10` | Minutes before stale alert |
| `CLEANUP_THRESHOLD_MIN` | `60` | Minutes after terminal to delete |

**Monitoring:**
```bash
tail -f /tmp/agent-monitor.log
cat /tmp/agent-monitor-state.json  # stale alert dedup state
```

---

## Quick Reference

| Action | Tool/Command |
|--------|-------------|
| Spawn agent worker | `sessions_spawn` with worker template above |
| Check agent status | `exec: cat ~/.openclaw/workspace/.foreman/<id>.json` |
| Check all status | `exec: bash skills/foreman/scripts/foreman-status.sh` |
| Steer worker | `subagents(action=steer, target=<key>, message=...)` |
| Kill worker | `subagents(action=kill, target=<key>)` |
| List agent sessions | `subagents(action=list)` |
| Clean agent tasks | `exec: bash skills/foreman/scripts/foreman-cleanup.sh` |
| New shell job | Copy `skills/foreman/scripts/template-wrapper.sh` |
| Update job progress | `job_progress "$JOB_ID" "message"` |
| Check shell jobs | `ls /tmp/swabby-jobs/*.json` |
| Monitor agent tasks | `bash skills/foreman/scripts/agent-monitor.sh` |
| Agent monitor log | `tail -f /tmp/agent-monitor.log` |
| Model selection | Sonnet for exec, inherit for reasoning |
| Timeout guidance | See `references/exec-hygiene.md` |
