---
name: multi-agent-protocol
version: 1.0.0
description: >
  Production protocol for multi-agent collaboration in OpenClaw. Combines Spec-First task
  definition, two-stage review (Spec + Quality), beads dependency graph as task bus,
  blackboard.json for direct inter-agent communication, Circuit Breaker retry strategy,
  and git worktree isolation for parallel implementation. Use when orchestrating 2+
  sub-agents on complex tasks requiring coordination, quality gates, and fault tolerance.
author: lebo
license: MIT
keywords:
  - multi-agent
  - orchestration
  - spec-first
  - circuit-breaker
  - blackboard
  - beads
  - review
  - fault-tolerance
  - parallel-agents
  - sessions_spawn
---

# Multi-Agent Collaboration Protocol

Production playbook for orchestrating multiple sub-agents in OpenClaw with structured task
flow, quality gates, inter-agent communication, and automatic fault recovery.

Synthesized from community research: `subagent-driven-development`, `beads`, `swarm-self-heal`,
`agent-team-orchestration`, and `http-retry-circuit-breaker` patterns.

---

## When to Use

Use this skill when:
- Spawning 2+ sub-agents on a complex task
- Tasks have dependencies between agents
- Quality matters (not just "done", but "correct and well-built")
- You need fault tolerance without manual intervention
- Multiple agents need to share state without going through the orchestrator

**Don't use for:**
- Single-agent tasks (unnecessary overhead)
- One-off spawns with no handoff
- Simple question delegation

---

## Core Principles

1. **Spec-First** — No spawning without a spec file. No spec = no work starts.
2. **Two-Stage Review** — Every implementation goes through Spec Review, then Quality Review.
3. **Serial Implementation** — Only one Implementer runs at a time. Parallel = research/analysis only.
4. **Blackboard Communication** — Agents read/write a shared file directly. Orchestrator is not a relay.
5. **Circuit Breaker** — Failures have a ceiling. After threshold → alert human, don't loop forever.
6. **Fixed sessionKeys** — Same role = same sessionKey = agent memory persists across spawns.

---

## Directory Layout

```
{project-root}/
  .beads/              ← beads task graph (git-tracked, auto-managed)
  specs/
    {task-id}.md       ← Task spec (MUST exist before spawning Implementer)
  shared/
    blackboard.json    ← Live state bus (any agent reads/writes directly)
    artifacts/
      {role}/          ← Each agent's output artifacts
```

---

## Task Lifecycle

```
Write Spec → bd create → bd ready → Claim → Implement → Self-Review
  → Spec Review → Quality Review → bd close → bd sync
```

---

## Step 1 — Write the Spec

Before spawning anything, create `specs/{task-id}.md`:

```markdown
## Goal
What is the final state? (observable, verifiable)

## Scope
What is included / explicitly excluded?

## Inputs
Files, paths, dependencies, environment requirements.

## Outputs
Exact artifact paths and formats expected.

## Acceptance Criteria
Checklist. Each item must be independently verifiable.
- [ ] criterion 1
- [ ] criterion 2

## Risks
Known unknowns, edge cases, things to watch out for.
```

**No acceptance criteria = spec is incomplete. Don't spawn yet.**

---

## Step 2 — Create Task in beads

```bash
# Initialize beads in project (first time only)
bd init --quiet

# Create task
bd create "Task title" -p 1 --json
# → returns task id like bd-a1b2

# Add dependencies if needed
bd dep add bd-child bd-parent     # child is blocked by parent

# Check what's ready to start
bd ready --json
```

---

## Step 3 — Spawn Implementer

The task prompt must be **self-contained** — the agent cannot see your conversation history.

```
sessions_spawn({
  task: "
    You are implementing task {task-id}.

    ## Spec
    {paste full spec content here — do not tell agent to read a file}

    ## Working Directory
    {absolute path}

    ## Output Path
    shared/artifacts/implementer/

    ## Context from Dependencies
    {paste relevant artifacts from blackboard.json if any}

    ## Before Starting
    If anything in the spec is unclear, ask now before writing code.

    ## Your Responsibilities
    1. Implement exactly what the spec says (nothing more, nothing less)
    2. Write tests
    3. Commit your work
    4. Self-review against spec acceptance criteria
    5. Update shared/blackboard.json with your status and artifact path
    6. Report: what you built, test results, artifact paths, known issues
  ",
  sessionKey: "implementer",
  runTimeoutSeconds: 600
})
```

**Update blackboard on spawn:**
```json
{
  "agents": {
    "implementer": { "status": "running", "task": "bd-a1b2", "artifact": null, "ts": "..." }
  }
}
```

---

## Step 4 — Spec Review

**Do not trust the implementer's self-report. Read the code.**

```
sessions_spawn({
  task: "
    You are a Spec Compliance Reviewer.

    ## Your Job
    Verify the implementation matches the spec — by reading the actual code,
    not by trusting the implementer's report.

    ## Spec (the standard)
    {paste full spec}

    ## Implementer's Report
    {paste implementer output}

    ## Artifact Location
    shared/artifacts/implementer/

    ## What to Check
    - MISSING: Requirements in spec not implemented
    - EXTRA: Things implemented that weren't requested
    - MISUNDERSTOOD: Implementation interprets spec differently than intended

    ## Output Format
    ✅ Spec compliant — all requirements verified by code inspection
    OR
    ❌ Issues found:
    - [file:line] Missing: {requirement}
    - [file:line] Extra: {what was added}
    - [file:line] Misunderstood: {intended vs actual}
  ",
  sessionKey: "spec-reviewer",
  runTimeoutSeconds: 300
})
```

**Rules:**
- Spec Review must pass before Quality Review begins
- Issues found → same Implementer (same sessionKey) fixes → re-review
- "Close enough" is not acceptable

---

## Step 5 — Quality Review

Only run after Spec Review passes.

```
sessions_spawn({
  task: "
    You are a Code Quality Reviewer. The spec compliance has already been verified.
    Your job is to check implementation quality.

    ## Artifact Location
    shared/artifacts/implementer/

    ## What to Check
    - Names match behavior (not implementation details)
    - No over-engineering (YAGNI)
    - Follows existing project patterns
    - Tests verify behavior, not mock internals
    - No magic numbers or unexplained inline constants
    - No leftover debug code or TODOs

    ## Output Format
    ✅ Approved
    OR
    ❌ Issues:
    - [CRITICAL] {issue} — must fix before merge
    - [IMPORTANT] {issue} — should fix
    - [MINOR] {issue} — optional
  ",
  sessionKey: "quality-reviewer",
  runTimeoutSeconds: 300
})
```

---

## Step 6 — Close Task

```bash
bd close bd-a1b2 --reason "Implemented and reviewed" --json
bd sync    # Always sync before ending session
```

---

## Blackboard Protocol

`shared/blackboard.json` is the inter-agent state bus. Any agent reads/writes directly.
The orchestrator does **not** relay information — agents get it from the blackboard.

### Schema

```json
{
  "agents": {
    "{role}": {
      "status": "idle | running | done | failed",
      "task": "bd-xxxx",
      "artifact": "shared/artifacts/{role}/output.md",
      "ts": "ISO-8601 timestamp"
    }
  },
  "tasks": {
    "bd-xxxx": {
      "retry_count": 0,
      "last_error": null,
      "circuit_status": "closed"
    }
  },
  "signals": [
    {
      "from": "{role}",
      "to": "{role}",
      "type": "ready_for_review | blocked | artifact_ready",
      "payload": "path or message",
      "ts": "ISO-8601 timestamp"
    }
  ]
}
```

### Agent Responsibilities

| Event | Action |
|-------|--------|
| Spawn starts | Write `status: running` |
| Work complete | Write `status: done` + `artifact` path |
| Task fails | Write `status: failed` + `error` |
| Needs another agent's output | Read `agents.{role}.artifact` from blackboard |

---

## Circuit Breaker — Retry Strategy

```
On task failure:

L1 — Auto-retry (same agent, same sessionKey)
  When: retry_count < 2
  Delay: 30s backoff
  For: transient errors, timeouts

L2 — Escalate (stronger model, same sessionKey)
  When: retry_count == 2
  Action: override model to a higher-reasoning option
  For: task is hard, needs better reasoning

L3 — Circuit Open (stop, alert human)
  When: retry_count >= 3
  Action:
    - Write blackboard tasks.{id}.circuit_status = "circuit_open"
    - Alert user: task name, failure reason, retry history
    - bd update {id} --status blocked
  For: task itself is broken, retrying won't help
```

---

## Parallelism Rules

| Task Type | Parallel? | Reason |
|-----------|-----------|--------|
| Implementation (writes code) | ❌ Serial only | Code conflicts |
| Research / analysis | ✅ Yes | Read-only |
| Documentation (different files) | ✅ Yes | File isolation |
| Review (different tasks) | ✅ Yes | Read-only |

### When You Truly Need Parallel Implementation — git worktree

```bash
git worktree add ../workspace-{role} -b agent/{role}/{task-id}
```

- Pass the worktree path as working directory in spawn prompt
- After completion: PR → orchestrator reviews diff → merge

---

## Fixed sessionKey Convention

Same role across spawns → same sessionKey → agent remembers previous context.

| Role | sessionKey | Retains |
|------|-----------|---------|
| Implementer | `implementer` | Codebase knowledge, past decisions |
| Spec Reviewer | `spec-reviewer` | Review standards, past findings |
| Quality Reviewer | `quality-reviewer` | Code style patterns, project conventions |
| Researcher | `researcher` | Research context, sources |

---

## Orchestrator Boundaries

**Do:**
- Write spec files
- Manage beads (`bd create`, `bd dep add`, `bd ready`, `bd close`, `bd sync`)
- Spawn role agents
- Read blackboard to determine next phase
- Execute Circuit Breaker logic
- Report progress to user

**Don't:**
- Write implementation code directly
- Relay information between agents (they read blackboard)
- Spawn Implementer without a spec file

---

## Watchdog (optional but recommended)

Install `swarm-self-heal` and run periodic health checks:

```bash
bash skills/swarm-self-heal/scripts/check.sh
```

Configure as a cron job (every 30 minutes) to detect:
- Silent agents (no blackboard update past timeout)
- `circuit_open` tasks needing human intervention
- Gateway health

---

## Session End Checklist

```bash
bd sync            # Flush all task state to git
bd ready --json    # Show next unblocked tasks (for handoff notes)
```

Write your own status to blackboard: `status: done | paused`.

---

## Quick Reference

```bash
# Initialize
bd init --quiet

# Task management
bd create "Title" -p 1 --json
bd dep add bd-child bd-parent
bd ready --json
bd update bd-xxxx --status in_progress --assignee implementer --json
bd close bd-xxxx --reason "done" --json
bd sync

# Dependency visualization
bd dep tree bd-xxxx
bd blocked --json
```
