---
name: context-guardian
description: Production-ready context continuity skill for autonomous AI agents. Use when tasks may outlive a single LLM context window, when you need durable checkpoints, structured summaries, restart recovery, pressure-aware trimming, or when the agent must stop safely instead of continuing blindly after context loss.
---

# Context Guardian

## Overview

Use this skill to keep long-running agent work resumable, loss-aware, and safe. It adds context pressure monitoring, durable checkpoints, structured summaries, recovery loading, and a safety gate that stops autonomous execution when fidelity is too low.

## Execution

### Preflight
- Load the latest task state before any new action.
- Load the latest structured summary before any new action.
- Rebuild the working context bundle before each major model call.
- Keep the bundle focused on: current goal, current phase, latest checkpoint, latest summary, active constraints, last successful action, next action, and relevant artifacts.

### Pressure thresholds
- warning_threshold = 0.55
- compress_threshold = 0.70
- critical_threshold = 0.85

### Pressure rules
- warning: checkpoint soon.
- compress: write checkpoint and summary before the next major action.
- critical: stop autonomous execution unless a fresh checkpoint already exists and state confidence is high.
- If context pressure is critical and no fresh checkpoint exists, emit `STATUS:HALT_CONTEXT_LIMIT`, write checkpoint + summary, and stop.

### 1. Inspect the existing agent shape
Read `references/integration-checklist.md` when you wire the module into the host agent loop. Purpose: identify the smallest safe integration point.

### 2. Use the canonical state model
Represent task continuity with the task state object in `references/task-state-schema.md`. Keep the object current in both JSON and human-readable markdown.

### 3. Build the runtime bundle before major actions
Before each major model call, rebuild the working context bundle from the latest checkpoint, the latest summary, the current goal, the current phase, active constraints, the last successful action, the next action, and relevant artifacts. Keep the bundle ahead of stale conversation history.

### 4. Write checkpoints often
Write a checkpoint after any state mutation, before any destructive action, when context pressure enters compress or critical ranges, before ending a run, and after any failure that changes the plan.

### 5. Summarize deterministically
Compress stale history into the structured summary format in `references/summary-template.md`. Preserve goal, phase, completed steps, failed attempts, decisions, files touched, important tool outputs, blockers, next action, invariants, and constraints.

### 6. Stop safely when fidelity is low
If confidence is low, do not improvise.
If state confidence is low and context pressure is critical, stop autonomous execution and ask for confirmation after writing checkpoint + summary.

### 7. Integrate with the agent loop
If the project already has a planner, update state alongside planner steps. If the project already has a tool runner, intercept tool results and append checkpoint events. If the project already has a memory module, reuse it instead of duplicating storage.

### 8. Read the references when implementing
Read `references/task-state-schema.md` when you need the canonical task state fields. Purpose: keep state shape stable.
Read `references/summary-template.md` when you need the summary format. Purpose: keep summaries compact and loss-aware.
Use `references/config-example.yaml` to confirm configuration shape, paths, and thresholds.
Use `references/persisted-task-state.example.json` to verify the persisted state example.
Read `references/summary-example.md` when you need a concrete summary example. Purpose: match the expected markdown output.
Read `references/integration-checklist.md` when you wire the module into an agent loop. Purpose: avoid missing hooks.

### Do not
- Do not continue blindly after context loss.
- Do not depend on raw history alone for recovery.
- Do not keep stale checkpoints when a fresh one is required.

## Resources

### scripts/
Use the Python module in `scripts/context_guardian.py` as the deterministic implementation reference. Use `scripts/test_context_guardian.py` to validate checkpoint creation, summary generation, restart recovery, critical-threshold stop behavior, and trimming policy.

### references/
The references directory contains the schema, template, config example, and integration checklist. Keep these files in sync with the implementation.

## Completion standard

A valid implementation must:
- persist durable task state outside the LLM context,
- recreate a working bundle before each major action,
- checkpoint and summarize on pressure or on progress,
- stop when context fidelity is too low,
- recover from restart using the latest durable state,
- keep thresholds and paths configurable,
- include tests and examples.
