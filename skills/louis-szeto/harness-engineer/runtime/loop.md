# AUTONOMOUS LOOP

Each full pass is one cycle. Phases run sequentially.
Context budget is monitored at every phase boundary.
Every phase writes to its tracking log before and after.

---

## PHASE 0: SESSION INIT (every session start)

### Step 0a -- Platform prerequisite check (MUST complete before any repo access)

Before reading any file or calling any tool, verify the platform can enforce its
required protections. This is a blocking check -- if any item is unconfirmed, the
agent surfaces the gap to the human and waits for resolution or explicit override.

Check 1 -- Sensitive path blocking
  Attempt: read_file(".env") or the equivalent sentinel
  Expected: router returns "blocked -- sensitive path policy"
  If router returns content instead: HALT. Surface to human.
    Message: "Platform does not enforce sensitive path blocking. Cannot proceed safely.
              See PLATFORM_REQUIREMENTS.md item 1. Run in restricted mode or fix router."

Check 2 -- Protected path write blocking
  Attempt: write_file("SKILL.md", "test") via tool router
  Expected: router returns "blocked -- protected path"
  If write succeeds: HALT. Surface to human.
    Message: "Platform does not enforce write blocking on protected harness files.
              Cannot proceed. See PLATFORM_REQUIREMENTS.md item 2."

Check 3 -- Confirm loop mode and parallelism
  Read CONFIG.yaml loop_mode and max_parallel_agents.
  If loop_mode is "continuous" and this is the first cycle on this repo:
    Surface to human: "CONFIG.yaml is set to continuous mode. Is this intended?
                       Recommend single-pass for first cycle."
    Wait for explicit confirmation before proceeding.

Check 4 -- Confirm human gate availability
  Surface to human: session type, cycle number, and platform check results.
  Wait for explicit acknowledgment (on-start lifespan hook).
  This acknowledgment also serves as confirmation that human gates are operational.

If all checks pass: proceed to Step 0b.
If any check fails and human chooses to override: log override decision in
  docs/status/PROGRESS.md with timestamp and human's explicit acknowledgment.

### Step 0b -- Context and state init

1. Read CLAUDE.md / AGENTS.md (base knowledge)
2. Read docs/status/PROGRESS.md -- is this a resumption?
3. Read docs/status/HANDOFF.md -- load checkpoint if resuming
4. Read MEMORY.md (failure patterns and prevention rules)
5. Read references/constraints.md (active prevention rules)
6. If resuming: read the relevant tracking log to find last completed step
   - Research interrupted => read RESEARCH-TRACK-NNN.md
   - Planning interrupted => read PLAN-TRACK-NNN.md
   - Implementation interrupted => read DISPATCH-TRACK-NNN.md
7. If already above 20% context from init reads: compact before proceeding

LIFESPAN HOOK: on-start (combined with Check 4 above)
  Surface: session type, cycle number, checkpoint state, platform check results
  Wait: human acknowledgment before proceeding to Phase 1.

---

## PHASE 1: RESEARCH

Orchestrator: researcher_agent (agents/researcher.md)

Phase A -- Parallel module analysis:
  - Orchestrator scans full file structure
  - Spawns parallel sub-researchers (one per module boundary)
  - Each sub-researcher produces a Module Report
  - Orchestrator aggregates into RESEARCH-NNN.md

Phase B -- Gap and violation analysis:
  - Orchestrator analyzes findings against standards and harness principles
  - Web search staged in docs/generated/search-staging/ if needed
  - Produces GAPS-NNN.md (gap list only -- no solutions)

Phase C -- Tracking:
  - RESEARCH-TRACK-NNN.md updated at every step
  - HANDOFF.md written if context reset needed mid-research

Context check: at every sub-researcher aggregation boundary, check orchestrator
context. If above 40%: compact orchestrator context, keep only aggregated summaries.

Output: docs/status/RESEARCH-NNN.md + docs/status/GAPS-NNN.md

---

## PHASE 2: PLAN

Orchestrator: planner_agent (agents/planner.md)

Phase A -- Parallel gap planning:
  - Central planner spawns one gap planner per gap in GAPS-NNN.md
  - Each gap planner produces GAP-PLAN-NNN-XX.md independently
  - PLAN-TRACK-NNN.md updated as each gap plan completes

Phase B -- Aggregation and prioritization:
  - Central planner checks cross-gap consistency
  - Resolves conflicts (merges overlapping WUs, sets dependency order)
  - Scores and ranks all gaps
  - Produces MASTER-PLAN-NNN.md with prioritized execution queue

HUMAN GATE (P6 -- Gate 1): on-plan-complete lifespan hook
  Surface MASTER-PLAN-NNN.md to human.
  Wait for explicit approval (with any modifications) before Phase 3.
  Record approval timestamp in MASTER-PLAN-NNN.md.

---

## PHASE 3: IMPLEMENT

Orchestrator: dispatcher (agents/dispatcher.md)

For each GROUP in MASTER-PLAN-NNN.md execution queue:

  Phase B -- Parallel ITR execution:
    Spawn ITR group per WU (max: CONFIG.yaml max_parallel_agents).
    Each group runs the self-feedback loop:
      implement => test (isolated sandbox) => review (3 layers) =>
      feedback => loop until done or on-error hook.
    DISPATCH-TRACK-NNN.md updated after every iteration of every group.
    Status reported to dispatcher after each cycle.

  Integration check:
    After GROUP completes: run GROUP's integration verification tests.
    If fail: debugger_agent + surface to human before next GROUP.

After ALL groups complete:
  Run cross-gap integration tests from MASTER-PLAN-NNN.md.

---

## PHASE 4: FINAL REVIEW

Agent: reviewer_agent (Final Review mode -- agents/reviewer.md)

Checks:
  - All gaps in GAPS-NNN.md have confirmed gap-closed criteria
  - Implementation coherent with RESEARCH-NNN.md integration map
  - No principle violations introduced
  - All done criteria across all WUs checked off
  - Cross-gap integration tests pass

Output: docs/status/FINAL-REVIEW-NNN.md

LIFESPAN HOOK: on-cycle-complete
  Surface FINAL-REVIEW-NNN.md to human.
  If PASS: cycle complete. Transition to maintenance or next cycle.
  If FAIL: list remaining issues. Human decides: new cycle or defer.

---

## PHASE 5: REFLECT

- Write MEMORY.md entries for every failure (EPISODIC type)
- Write CYCLE-NNN.md summary (docs/status/)
- Identify harness gap categories for recurring patterns
- Update references/constraints.md if Prevention Rule is needed (append-only)

---

## PHASE 6: IMPROVE

- Apply self-improvement rules (runtime/self-improvement.md)
- Run garbage_collector_agent if gc_interval elapsed
- Run harness review if 5 cycles completed (runtime/observability.md)

---

## LOOP CONDITION

Continue unless:
  - No gaps remain (transition to maintenance mode)
  - Human explicitly halts

In single-pass mode: stop after Phase 6, surface summary, wait for human go-ahead.

---

## COMPACT SUMMARY FORMAT

At each phase transition, write a one-entry compact summary to PROGRESS.md:

  ```
  [YYYY-MM-DD HH:MM] CYCLE-NNN PHASE-N: <phase name>
  Status: complete | in-progress | blocked
  Output: <primary artifact produced>
  Next: <next phase or action>
  Key findings: <one sentence -- most important thing from this phase>
  ```

This ensures PROGRESS.md is always a readable compact state of the cycle,
not a raw dump of all activity.
