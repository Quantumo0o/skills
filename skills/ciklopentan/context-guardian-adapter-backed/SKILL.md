---
name: context-guardian
description: Installable context continuity skill for autonomous agents. Use when long tasks need durable checkpoints, restart-safe summaries, halt/resume control, and an upgrade-safe adapter-backed deployment path without patching OpenClaw core.
---

# Context Guardian

Use this skill to keep long-running agent work resumable, loss-aware, and restart-safe.
Use it when task continuity must survive context compaction, process restarts, or host upgrades.

## Runtime Modes

This skill has exactly three runtime modes.
Do not blur them.

### 1. `advisory`
- Use the skill instructions and references only.
- Treat persistence and recovery as best-effort.
- Do not claim hard continuity guarantees.
- Use this mode for manual runs, low-risk automation, or early adoption.

### 2. `adapter-backed`
- This is the recommended default production path.
- Use the installable skill package plus an external adapter, plugin, wrapper, or sidecar.
- Keep durable task state, summaries, halt signals, and resume entrypoints outside chat history.
- Do not patch OpenClaw core for this mode.

### 3. `core-embedded`
- This is an optional future architecture.
- It is not required.
- It is not the default.
- Do not treat it as the target implementation for this package or for ClawHub publication.

## Recommended OpenClaw Integration

Use `adapter-backed` mode for production OpenClaw deployments.
Run the skill as an installable package.
Run the durable execution layer outside core as a plugin, wrapper, or sidecar.
Use the external adapter to call the reference runtime in `scripts/context_guardian.py` or an equivalent implementation that obeys the same contract.
Use `plugin/context-guardian-adapter.js` when you need the packaged working Node adapter CLI.
Use `plugin/openclaw-runtime-plugin/` when you want official OpenClaw native hook integration without patching core.
Read `references/runtime-modes.md` when choosing deployment shape. Purpose: select runtime mode.
Read `references/adapter-contract.md` when wiring the external layer. Purpose: implement adapter contract.
Read `plugin/README.md` when deploying beside OpenClaw. Purpose: deploy plugin wrapper.

## Advisory vs Adapter-Backed Semantics

Use these rules exactly.

- `advisory` mode can guide checkpoints, summaries, and recovery discipline, but it does not create hard guarantees by itself.
- `adapter-backed` mode is the full production path for this package.
- Full durable guarantees require persistent storage, explicit halt handling, explicit resume handling, and adapter-owned pressure input.
- Critical continuity state must not live only in chat history.
- Critical continuity state must not depend only on the model context window.
- Halt, resume, and checkpoint behavior must rely on persistent storage outside core runtime memory.

## What this skill does not require

- no core patch required
- no OpenClaw fork required
- no direct modification of bundled runtime required

## External Adapter Requirements

The external adapter must provide all required capabilities and hook points from `references/adapter-contract.md`.
Use a filesystem-first persistent root.
Use atomic writes.
Use stable resumable paths.
Do not store the only copy of critical task state in prompts or conversation history.
Read `references/storage-layout.md` when selecting directories. Purpose: place durable files.
Read `references/config-example.yaml` when defining host config. Purpose: mirror config shape.

## Upgrade-Safe Storage Rule

Store continuity state outside bundled runtime code and outside ephemeral container layers.
Use a stable configurable root path.
Use schema-versioned state files.
Use atomic writes and safe migration.
Do not require rewriting OpenClaw internals when the skill version changes.
Do not place durable state under locations that disappear on package update.

## ClawHub Packaging Scope

Publish the installable skill package only.
Package these components:
- `SKILL.md`
- `README.md`
- `references/`
- `scripts/`
- `plugin/`
- `PACKAGING_CHECKLIST.md`
- `CHANGELOG.md`
- `.clawhubignore`

Do not package local runtime junk, cached state, or host-specific secrets.
The published unit is the installable skill.
The recommended deployment model is adapter-backed.

## Execution

Follow this order.
Do not skip steps.

1. Read `references/runtime-modes.md` when the host mode is unclear. Purpose: choose execution mode.
2. Read `references/task-state-schema.md` when state fields are needed. Purpose: load state schema.
3. Read `references/summary-template.md` when writing or validating summaries. Purpose: shape summary.
4. Read `references/adapter-contract.md` when the host claims durable support. Purpose: verify adapter behavior.
5. Read `references/storage-layout.md` when state paths must be created or checked. Purpose: verify storage layout.
6. If the host is `advisory` only, write or update guidance artifacts, state the limits, and stop before claiming durable guarantees.
7. If the host is `adapter-backed`, load the latest durable state, load the latest summary, read adapter pressure, and continue only if all required inputs exist.
8. If the host cannot provide durable state read/write, summary read/write, pressure input, halt path, and resume entrypoint, downgrade to `advisory`, state that downgrade, and stop before claiming production semantics.
9. If pressure is critical, write checkpoint + summary, emit halt through the adapter, and stop autonomous execution.
10. If pressure is not critical, build a working bundle from goal, phase, next action, last successful action, constraints, and relevant artifacts, execute exactly one checkpointable major action, write updated state, refresh summary when required, and then continue to Step 1.
11. If state is missing, invalid, or ambiguous, stop and recover from the latest durable state instead of guessing.
12. If `next_action` is terminal, write final state + summary, emit completion through the adapter, and stop.

## Required agent rules

- Do not promise durable recovery in `advisory` mode.
- Do not continue after a critical halt signal.
- Do not treat chat history as the only recovery source.
- Do not guess missing state that should be loaded from persistent storage.
- Do not chain multiple risky actions when one checkpointable action is enough.

## Deterministic implementation reference

Use `scripts/context_guardian.py` as the deterministic reference runtime.
Use `scripts/test_context_guardian.py` as the deterministic behavior test suite.
Use `plugin/context-guardian-adapter.js` as the packaged working Node adapter CLI.
Use `plugin/test_context_guardian_adapter.js` as the adapter behavior smoke test.
Use `plugin/openclaw-runtime-plugin/` as the packaged native OpenClaw hook-only integration path.
Use `plugin/openclaw.plugin.json.example` as the example manifest for an external OpenClaw-side adapter deployment.

## Completion standard

A valid production deployment for this skill must:
- install as a normal skill package,
- keep continuity storage outside core patches,
- use an external adapter for durable state, summaries, pressure, halt, and resume,
- separate `advisory` and `adapter-backed` semantics honestly,
- recover from latest durable state after restart,
- remain upgrade-safe across OpenClaw updates.
