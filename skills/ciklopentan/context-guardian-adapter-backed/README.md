# Context Guardian

Installable context continuity skill for OpenClaw and similar agent hosts.

## Release focus

This package is structured for **installable, upgrade-safe, adapter-backed deployment**.
It does **not** require patching OpenClaw core.

## Runtime model

- `advisory` — skill-only, best-effort, no hard guarantees
- `adapter-backed` — recommended production path, full durable continuity via external adapter
- `core-embedded` — optional future architecture, not required and not the target here

## Package contents

- `SKILL.md` — execution contract and mode split
- `references/` — schemas, storage rules, examples, integration contract
- `scripts/` — deterministic Python reference runtime and tests
- `plugin/` — external adapter/plugin layer for OpenClaw-style deployment, including a working Node adapter CLI

## Honest claim

This package gives a production-ready **adapter-backed model** without requiring a core patch.
It now includes a real Node-based external adapter CLI for durable state, summaries, halt/resume, and working-bundle assembly.
It also includes an optional native OpenClaw hook-only plugin package that integrates the adapter through official plugin hooks without patching core.
If deployed in `advisory` mode only, it remains useful but does not claim hard continuity guarantees.
