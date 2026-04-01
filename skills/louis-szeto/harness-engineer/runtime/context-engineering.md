# CONTEXT ENGINEERING

Context is a finite resource with diminishing returns. Treat it like working memory.
Every token added depletes the agent's attention budget. Curate aggressively.

---

## THE 40% RULE

Monitor context consumption continuously. When the context window reaches 40% full:

OPTION A -- Compact in place:
  - Summarize the conversation history, preserving:
    - Architecture decisions and ADRs
    - Unresolved bugs and blockers
    - Current task state and next steps
    - The five most recently accessed files
  - Discard: raw tool output, redundant messages, completed task details
  - Continue in the same session with the compacted context

OPTION B -- Sub-agent handoff (preferred for research/exploration):
  - Write a HANDOFF.md (see templates/handoff.md) with full state
  - Spawn a fresh sub-agent with only the handoff and relevant files
  - Sub-agent returns a condensed summary (target: 1000-2000 tokens)
  - Main agent receives summary only -- not the sub-agent's full trace

OPTION C -- Context reset (for context anxiety or session end):
  - Write docs/status/HANDOFF.md with checkpoint state
  - Start a new chat/session
  - New agent reads HANDOFF.md and PROGRESS.md and resumes

Do not wait until 90%+ to act. The degradation is gradual, not a cliff.
A noisy context at 60%+ produces measurably worse agent decisions.

---

## GROUND TRUTH HIERARCHY

When sources conflict, trust in this order:

1. The codebase (what is actually running)
2. CLAUDE.md / AGENTS.md (explicitly maintained base knowledge)
3. Runtime logs and error output (real-time state)
4. docs/ (written by humans -- may be stale)
5. MEMORY.md (harness-derived -- may lag reality)

Never infer or assume. If a file cannot be accessed, it does not exist.

---

## SESSION START PROTOCOL

Every session begins with this sequence:

1. Check for CLAUDE.md and AGENTS.md -- read both if present
2. Check for docs/status/PROGRESS.md -- if present, this is a resumption
3. Check for docs/status/HANDOFF.md -- if present, load checkpoint state
4. Read MEMORY.md -- reload failure patterns and prevention rules
5. Check references/constraints.md -- apply all prevention rules
6. Only then: begin planning or continue from checkpoint

---

## THREE-PHASE SUB-AGENT MODEL

Every non-trivial task is executed by three sequential sub-agents, each with a
strictly limited context and tool set.

PHASE 1 -- RESEARCHER
  Role: Compress information. Find truth. Stay objective.
  Input: task description + relevant file list
  Process: read files, read logs, read code -- do not plan, do not opine
  Output: a compressed summary of system state (what is true, what files matter)
  Rule: researcher produces NO implementation plans and NO opinions
  Context limit: 40% before outsourcing to nested sub-agent

PHASE 2 -- PLANNER
  Role: Convert research into leverage. Align intent.
  Input: researcher output
  Process: produce exact implementation steps with filenames, line numbers, snippets
  Output: a plan document (templates/plan.md) with explicit testing steps
  Rule: planner exists for alignment -- to make implementer catch errors early
  The plan is the contract. Implementer must not deviate without a plan revision.
  Context limit: 40%

PHASE 3 -- IMPLEMENTER + REVIEWER CYCLE
  Role: Execute the plan. Do not improvise.
  Input: planner output (plan document)
  Process: write code, run tests, commit checkpoints
  Constraint: reviewer sub-agent checks each output against the plan (not just correctness)
  Context limit: 40% per implementer instance -- reset between major tasks

See agents/dispatcher.md for dispatch format.
See agents/researcher.md, agents/planner.md, agents/implementer.md for agent specs.

---

## COMPACTION RULES

What to keep (high-signal):
  - Unresolved errors and their root causes
  - Architecture and design decisions made
  - Current task and immediate next steps
  - File paths that were modified
  - Prevention rules activated this session

What to discard (low-signal):
  - Raw tool output (keep only the outcome summary)
  - Completed task details
  - Redundant messages and acknowledgments
  - Early exploration that reached a dead end

Never compact prevention rules or active constraints. These must persist.
