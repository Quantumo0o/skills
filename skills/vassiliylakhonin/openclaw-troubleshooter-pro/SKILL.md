---
name: openclaw-troubleshooter-pro
description: Fast, symptom-first troubleshooting for OpenClaw incidents with minimal downtime. Use when OpenClaw is failing or unstable (status unreachable, missing scope/operator.read, gateway closed 1000, tool calls hang, cron misbehavior, channel delivery failures, model/provider routing mismatch, session wedges). Prioritize read-only checks first, then safe fixes with explicit verification gates.
---

# OpenClaw Troubleshooter Pro

Diagnose by **symptom first**. Keep output short, command-first, and verifiable.

## Core Rules

1. Start with read-only diagnostics.
2. Prefer the shortest path to isolate root cause.
3. Do not apply destructive or broad config changes without explicit user confirmation.
4. After each fix, run a verification gate.
5. If unresolved, provide a tight escalation bundle (what was checked, evidence, likely root causes).

## Response Format

Use this structure:

## Command
[exact command(s)]

## What It Checks
[one line]

## Expected
[success signal]

## If Fails
[next command or branch]

## 0) Baseline Snapshot

Run first:

```bash
openclaw status
openclaw gateway health
openclaw gateway status
```

If any command errors, capture exact stderr and continue with relevant branch below.

---

## 1) Symptom: `status unreachable` / `missing scope: operator.read`

```bash
openclaw status
openclaw gateway health
openclaw gateway restart
openclaw status
```

If still failing:

```bash
openclaw logs --limit 200
```

Check for auth/session mismatch, token resolution issues, or loopback regression signals.

Verification gate:
- `openclaw status` returns healthy/reachable.

---

## 2) Symptom: `gateway closed (1000 normal closure)` on CLI ops

```bash
openclaw gateway status
openclaw gateway health
openclaw gateway restart
openclaw gateway health
```

If command-specific (e.g., cron/list) still fails, collect targeted evidence:

```bash
openclaw logs --limit 300
```

Verification gate:
- Failing command works twice in a row.

---

## 3) Symptom: tool calls hang / session wedges

Quick containment:

```bash
openclaw gateway health
openclaw gateway restart
```

Then retest minimal action in a fresh session.

Verification gate:
- Tool call returns normally in fresh session.
- Original symptom is reproducible or confirmed cleared.

---

## 4) Symptom: cron behaves oddly (`list`/`run` issues)

```bash
openclaw cron status
openclaw cron list
```

If scheduler is running but command fails, capture logs:

```bash
openclaw logs --limit 300
```

Verification gate:
- `cron list` succeeds.
- One known job can run successfully.

---

## 5) Symptom: channel delivery failures (Telegram/Discord/WhatsApp/Slack)

Run service health first:

```bash
openclaw status
openclaw gateway health
openclaw logs --limit 300
```

Then isolate by channel-specific errors (listener missing, proxy failure, auth/relink state).

Verification gate:
- one inbound + one outbound message path succeeds for target channel.

---

## 6) Symptom: model/provider routing mismatch

Check current model selection path and provider-qualified refs in active UI/CLI flow.

Baseline checks:

```bash
openclaw status
openclaw logs --limit 300
```

Look for signs of bare model IDs being resolved against default provider.

Verification gate:
- requests route to intended provider consistently.

---

## Safe Fix Policy

Before any risky change, ask for explicit confirmation when action is:
- irreversible,
- broad config mutation,
- external side-effect beyond diagnostics.

---

## Escalation Bundle (when unresolved)

Provide:
1. Symptom statement (1 line)
2. Commands run (exact)
3. Key outputs/errors (trimmed)
4. What is ruled out
5. Top 2 likely root causes
6. Next best test/fix
