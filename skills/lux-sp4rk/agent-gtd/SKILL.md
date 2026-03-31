---
name: agent-gtd
description: "Executive function system for AI agents: GTD-style task management, error/learning capture, and periodic self-review using Taskwarrior. Use when: (1) tracking multi-step goals or internal agent tasks, (2) logging command failures, user corrections, or missing capabilities, (3) running a self-improvement or review loop, (4) managing continuity across sessions, (5) triaging a backlog of agent work. Reference implementation uses Taskwarrior; patterns are portable to other task backends."
version: 1.1.0
---

# Agent GTD

A complete executive function stack for AI agents. Three layers working together:

| Layer | Tool | Role |
|---|---|---|
| **RAM** | Taskwarrior | Actionable tasks, current focus, backlog |
| **Hard Drive** | Markdown files | Context, decisions, lore, "why" |
| **Workbench** | `ops/session_state.md` | What I was doing 5 seconds ago |

Rule of thumb: task to finish → Taskwarrior. Fact to remember → Markdown. Mid-task state → session_state.

---

## Installation

**Taskwarrior** (required)
```bash
# Debian/Ubuntu
sudo apt install taskwarrior
# macOS
brew install task
# Arch
sudo pacman -S task
```

**Python 3** (required for helper scripts)

**Timewarrior** (optional — enables vitality heartbeat)
```bash
# Debian/Ubuntu
sudo apt install timewarrior
# macOS
brew install timewarrior
```

**ClawVault** (optional — structured session handoffs)
Falls back gracefully if absent; `task_manager.py sleep` prints a warning but continues.

---

## Quick Reference

```bash
# Add to inbox
task add +in "thing to process"

# Triage inbox
task +in list

# Add internal task
task add project:Internal "description" +next priority:M

# Log a failure
task add project:Internal.Learnings +error "what broke"
task annotate <id> "fix: what resolved it"

# See what's next
task next

# Run a review
# → follow references/review-runbook.md
```

---

## 1. The Inbox (Capture)

Everything goes into the inbox first. No processing at capture time.

```bash
task add +in "description"
task in   # custom report: lists all +in items
```

Inbox items carry high urgency (+15.0) to surface in default reports.

---

## 2. Triage Flow

For each item in `task in`:

1. **Actionable?** No → delete or annotate as reference.
2. **< 2 minutes?** Do it now, mark done.
3. **Multi-step?** Create a `project:` and tag the first step `+next`.
4. **Delegate?** Tag `+waiting`, add `wait:` date, annotate who/what.
5. **Defer?** Assign project, tag `+next`, move on.

---

## 3. Project Taxonomy

```
Internal           # Agent-internal work
  Internal.Ops     # Infra, config, tooling
  Internal.Learnings  # Errors, corrections, feature gaps
Goals              # High-level strategic goals
<ProjectName>      # Active user projects
  <ProjectName>.Ops
```

---

## 4. Task Attributes

```bash
priority:H / M / L          # Impact
brainpower:H / M / L        # Cognitive load (H=architecture, L=routine)
estimate:<minutes>           # Time budget
wait:<date>                  # Snooze (hide until date)
due:<date>                   # Hard deadline
```

**Selection pattern:**
```bash
task next brainpower:L estimate:5    # Quick wins
task next brainpower:H priority:H   # Deep work
```

---

## 5. Error & Learning Capture

Log immediately. Don't wait for review time.

| Situation | Tag | Example |
|---|---|---|
| Command / tool fails | `+error` | `task add project:Internal.Learnings +error "git push rejected: token expired"` |
| User corrects agent | `+learning` | `task add project:Internal.Learnings +learning "pnpm not npm on this project"` |
| Missing capability | `+featreq` | `task add project:Internal.Learnings +featreq "user wanted calendar invite generation"` |

Use `task annotate <id> "..."` for fix details or stack traces.

**Automated promotion:** `promote_learnings.py` runs every 6 hours via cron. It scans `memory/lessons/` for error-like entries that recur 3+ times in 7 days — then auto-creates a Taskwarrior task in `project:Internal.Learnings` with the fix description. No manual tracking needed for recurring errors.

**Manual promotion rule:** If the recurring error has a structural fix (not just a one-liner), promote it to `TOOLS.md`, `AGENTS.md`, or `SOUL.md`. Mark the Taskwarrior task done, note the promotion target in the final annotation.

```bash
# Query learnings
task project:Internal.Learnings list
task +error list
task +error +<area> list
```

---

## 6. Backlog Triage

Run when the task list exceeds ~20 items or burndown stalls.

### Tickler / Think Pattern
```bash
# Snooze: hide until a future date
task add +tickle wait:2025-03-01 "revisit X"

# Deferred decision: force a yes/no when it resurfaces
task add +tickle +think wait:+3d "Should I do Y? (yes/no)"
```
**No double-snooze rule:** when a `+think` task resurfaces, decide immediately. No re-snoozing.

### Rule of 3
Pick only **3 tasks per day** to actually finish during autonomous chew-through. Focus beats volume. Prioritize:
1. Anything blocking other tasks (dependency-first)
2. Low-hanging fruit solvable in < 5 min (`exec`, `edit`, `web_search`)
3. Highest-urgency `+next` task

### Priority Pivot
When project focus shifts, bulk-modify to keep the list honest:
```bash
task project:OldProject modify -next priority:L
task project:NewProject modify +next priority:H
```

### Stale Task Triage Gate

**Trigger:** `task status:pending age.before:14days count` exceeds **50**, halt new work and triage.

**Decision Tree (for each stale task):**
1. **Unblocked + HIGH/MEDIUM priority?** → Must close by next heartbeat OR deprioritize with annotation.
2. **Blocking other work?** → Escalate now (bump to `+next`, add due date).
3. **Tagged `+waiting`?** → OK (delegated). Review wait condition; reschedule if stale.
4. **Appears in high-level goals (e.g., MEMORY.md)?** → Resurrect with `+next`. Add sub-tasks if needed.
5. **Old "Explore" or "Maybe"?** → Delete. (It survived 14 days; it's not critical.)
6. **Ref task linking to closed external issue?** → Delete. (Issue is resolved; task served its purpose.)
7. **Everything else?** → Move to `memory/backlog.md` (Cold Storage). Add timestamp + rationale.

**Output:** Run count again. If still >50, log concern and escalate to user.

### Weekly Prune
Every Monday (or during review loops):
- **Age Out:** Any task older than 14 days with no progress gets deleted or moved to cold storage.
- **Prune the "Maybe":** If a task description starts with "Maybe" or "Explore," and hasn't been touched in a week, delete it.

---

## 7. Witness Gates (High-Stakes Actions)

Tag destructive or irreversible tasks `+gate`. Do not auto-complete them.

```bash
task add project:Internal +gate "push to main branch"
```

When attempting to complete a `+gate` task via `task_manager.py done <id>`, the script will return:
```json
{"status": "gated", "message": "Witness Gate Active...", "task": {...}}
```

**Action:** Pause and notify the human. Do not bypass autonomously. Wait for explicit approval, then use `--witnessed` flag:
```bash
python3 scripts/task_manager.py done <id> --witnessed
```

---

## 8. Session Close Protocol

**Trigger:** User signals end of session ("sleep", "done", "signing off") OR at the end of a review.

**Goal:** Produce a populated handoff — never empty next steps.

Run `scripts/sleep.sh "<summary>"` (validates next steps are non-empty before writing). Full runbook → `references/review-runbook.md`.

---

## 9. Periodic Review

Run at natural breakpoints: session start, after completing a feature, weekly.

→ See `references/review-runbook.md` for the full 7-step runbook.

**Quick review (< 5 min):**
```bash
task +in list          # clear inbox
task +error list       # any unresolved failures?
task next              # confirm focus is right
task project:Internal.Learnings +error status:pending list  # promote if 3+ recurrences
```

---

## 10. Session Continuity

Pick → Log (to `ops/session_state.md`) → Work → Done → Wipe. On session start: `cat ops/session_state.md` and `task active` to recover state. Minimal format:
```
[YYYY-MM-DD HH:MM] Focus: <task> (#<id>)
Last action: <what was done>
Open loops: <anything unfinished>
Blockers: <none | description>
```

---

## 11. Vitality Heartbeat

Monitor agent activity and alert on sustained silence during mission hours.

```bash
python3 scripts/vitality_check.py   # run manually
# or: cron every hour during mission hours
```

→ See `references/vitality-heartbeat.md` for full implementation details.

**Concept:** If silence exceeds threshold (default: 8 hours) during mission hours (default: 14:00-02:00 UTC), alert the human with:
- Hours silent
- Last known active timestamp
- Last known task (from `task active` or `ops/session_state.md`)

---

## Scripts

This skill includes helper scripts in `scripts/`:

| Script | Purpose |
|---|---|
| `task_manager.py` | JSON API wrapper for Taskwarrior (list, capture, done, delete, witness gates) |
| `vitality_check.py` | Silence detection during mission hours |
| `sleep.sh` | Session close wrapper with next-step validation |

---

## References

- `references/taskwarrior-schema.md` — Installation, `.taskrc` config, UDAs, custom reports, tag taxonomy
- `references/review-runbook.md` — Periodic review loop (2 min → 20 min depth levels)
- `references/vitality-heartbeat.md` — Agent silence detection and alerting
- `references/executive-stack.md` — Async execution pattern: Taskwarrior → Pueue bridge (future/advanced)
