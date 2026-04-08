# Context Guardian

`context-guardian` is a production-ready continuity layer for long-running autonomous agent work.

## What it does
- measures context pressure,
- writes checkpoints and summaries to disk,
- restores the important task state before the next action,
- stops autonomous execution when fidelity is too low,
- keeps the runtime bundle ahead of stale chat history.

## Files
- `SKILL.md` — skill entrypoint and workflow
- `scripts/context_guardian.py` — reference implementation
- `scripts/test_context_guardian.py` — tests
- `references/task-state-schema.md` — canonical state model
- `references/summary-template.md` — summary format
- `references/config-example.yaml` — configuration example
- `references/persisted-task-state.example.json` — saved state example
- `references/summary-example.md` — saved summary example
- `references/integration-checklist.md` — integration checklist

## Usage
1. Add the module to the host agent loop.
2. Load `task_state.json` and the latest summary at session start.
3. Rebuild the working bundle before each major action.
4. Check pressure before each major action.
5. Checkpoint before destructive work and at critical pressure.
6. Stop and recover if confidence is too low.

## Enable it
- Copy the reference module into the host project.
- Wire `ContextMonitor` into the agent loop.
- Wire `CheckpointStore` into planner/tool events.
- Wire `MemoryAssembler` before major model calls.
- Wire `SafetyGate` before autonomous continuation.
- Configure paths and thresholds in the host project.

## Tests
Run the included tests with your normal Python test runner once the module is placed in a Python environment that can import `context_guardian`.
