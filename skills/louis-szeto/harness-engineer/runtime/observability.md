# OBSERVABILITY AND FEEDBACK CLOSED-LOOP

Observability is not logging. It is the closed loop that feeds harness failures back
into harness improvements. The target of analysis is always the harness, never the model.

---

## EXECUTION TRACKING

Every cycle produces an execution trace in docs/generated/tool-logs/:
  - One entry per tool call (metadata only -- see tools/execution-protocol.md)
  - One cycle summary in docs/status/CYCLE-NNN.md

The cycle summary records:
  - Tasks attempted, completed, failed
  - Tool calls made per agent (counts only, no payloads)
  - Duration per phase
  - Test results (aggregate counts + coverage)
  - Abnormalities detected

---

## QUALITY CATEGORIZATION

After each VERIFY phase, categorize every output:

TIER 1 -- Critical (block cycle advance):
  - Failing tests
  - Security scan findings
  - Reviewer veto

TIER 2 -- High (address this cycle):
  - Coverage below threshold
  - Performance regression
  - Constraint violation

TIER 3 -- Medium (backlog with priority score):
  - Code smell / dead code
  - Doc gaps
  - Minor reviewer comments

TIER 4 -- Low (GC agent, next cycle):
  - Style inconsistencies
  - Optimization opportunities
  - Refactoring candidates

Only Tier 1 blocks cycle advance. Tier 2-4 are scored and queued.

---

## ABNORMALITY DETECTION

Trigger debugger_agent immediately on:
  - Any test that was passing and is now failing (regression)
  - Any tool call that returns an unexpected structure
  - A sub-agent that produces output not matching its EXPECTED OUTPUT field
  - The same failure appearing in tool-logs more than once
  - A cycle that takes more than 2x its historical average duration
  - An agent that exceeds its context limit without triggering the 40% rule

Do not continue the cycle on abnormality. Stop, diagnose, write MEMORY.md entry, then
decide: fix in this cycle, or checkpoint and escalate to human.

---

## FEEDBACK CLOSED-LOOP

This is the most important part of observability. When a failure occurs:

WRONG QUESTION: "Why did the model get this wrong?"
RIGHT QUESTION:  "What was missing from the harness that allowed this to happen?"

Harness gap categories:
  MISSING CONSTRAINT  -- a rule that would have prevented this does not exist
  MISSING TEST        -- a test that would have caught this was not written
  MISSING CONTEXT     -- the agent lacked information it needed (context engineering gap)
  MISSING TOOL        -- the agent could not verify something it needed to verify
  MISSING REVIEW      -- the review cycle did not catch this (review scope gap)
  MISSING CHECKPOINT  -- a context reset lost state that should have been persisted

For every failure, identify the harness gap category and create the missing element.
Record the gap category in MEMORY.md. Update references/constraints.md if it is a
MISSING CONSTRAINT.

---

## HARNESS IMPROVEMENT CYCLE

At the end of every 5 cycles, run a harness review:

1. Aggregate CYCLE-NNN.md summaries
2. Identify the most frequent gap categories
3. Draft harness improvements (new constraints, tests, or context rules)
4. Surface to human for approval (P6 gate)
5. Apply approved improvements to this skill's reference files (append-only)
6. Commit changes to the skill under docs/harness-improvements/

The harness should become measurably more effective over time.
Track: regression rate, average cycle duration, context resets per cycle.
