# AUTONOMY RULES AND HUMAN SUPERVISION

These rules govern agent behavior without direct human input, and define the points
where human oversight is mandatory.

---

## LIFESPAN HOOKS

The harness surfaces to the human at these fixed points:

on-start:
  Surface: session type (new / resume), cycle number, checkpoint state
  Wait: human acknowledgment before proceeding

on-plan-complete:
  Surface: PLAN-NNN.md for human review and approval
  Wait: explicit human approval -- do not implement without it

on-cycle-complete:
  Surface: CYCLE-NNN.md summary (what built, what failed, what learned)
  Wait: in single-pass mode only -- otherwise log and continue

on-error (Tier 1 failure after N retries):
  Surface: failure description, harness gap category, proposed fix
  Wait: human decision -- fix this cycle, defer, or halt

on-halt:
  Surface: reason for halt, HANDOFF.md location, recovery instructions
  Wait: n/a (terminal)

---

## MANDATORY HUMAN APPROVAL GATES

GATE 1 -- Plan approval (before any implementation)
  Triggered by: planner sub-agent completing PLAN-NNN.md
  What human reviews: scope, approach, test criteria, risks
  What blocks without approval: entire Phase 4 (BUILD)

GATE 2 -- Architecture change
  Triggered by: any ADR that proposes a change to existing architecture
  What human reviews: ADR rationale, trade-offs, rollback plan
  What blocks without approval: the architectural change itself

GATE 3 -- Failure retry exhaustion
  Triggered by: CONFIG.yaml retry_limit hit on a critical-path task
  What human reviews: failure summary, harness gap, proposed fix options
  What blocks without approval: further retries

GATE 4 -- Harness improvement
  Triggered by: harness review proposing changes to skill reference files
  What human reviews: proposed improvements (append-only to constraints, etc.)
  What blocks without approval: changes to any skill file

---

## AGENTS MUST

- Prefer action over speculation -- use tools to resolve uncertainty
- Verify everything -- no assumed correctness
- Document decisions -- every non-trivial choice must be traceable
- Prefer reversible actions -- flag irreversible ones and pause for confirmation
- Monitor context -- apply 40% rule before context degrades agent quality

---

## ESCALATION PROTOCOL

When blocked:
1. Search for the answer (code_search, web_search with staging gate)
2. Test a hypothesis with the smallest possible change
3. Try an alternative approach (document alternatives considered)
4. Log the failure in MEMORY.md and continue other tasks if parallel
5. Halt only if the blocked task is a hard dependency for all other work
   and retry limit is hit -- then trigger on-error hook

---

## NEVER

- Stop due to uncertainty -- search or test instead
- Assume correctness without tool-based validation
- Make destructive changes without explicit approval
- Run the same failing operation more than CONFIG.yaml retry_limit times
- Fabricate file contents, test results, or git state
- Allow a sub-agent to exceed 40% context without triggering compact or handoff
- Skip a human gate

---

## PROTECTED PATHS (enforced by tool-router)

Agents may READ but never WRITE, OVERWRITE, or DELETE:
  SKILL.md
  CONFIG.yaml
  agents/**
  runtime/**
  tools/**
  references/harness-rules.md

The one writable reference file is references/constraints.md -- agents may APPEND
Prevention Rules only. They may never delete or overwrite existing constraints.

Writes to protected paths are blocked by the router and logged as BLOCKED_WRITE events.
The dispatcher is notified and the cycle pauses for human review.
