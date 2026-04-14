# Changelog

## 2.2.0 - 2026-04-11

- Added `plugin/openclaw-runtime-plugin/` as an official native OpenClaw hook-only integration package.
- Wired adapter-backed continuity into official OpenClaw hooks without patching core.
- Added plugin smoke test and runtime package metadata.
- Preserved upgrade-safe external storage and no-core-patch deployment model.

## 2.1.0 - 2026-04-11

- Added `plugin/context-guardian-adapter.js` as a working Node-based external adapter CLI.
- Added `plugin/test_context_guardian_adapter.js` for adapter smoke tests.
- Upgraded the package from example-only plugin surface to a real adapter-backed implementation path.
- Kept durable state, summaries, snapshots, halt/resume, and working-bundle assembly outside OpenClaw core.
- Preserved the installable skill + external adapter model without any core patch.

## 2.0.0 - 2026-04-11

- Reframed `context-guardian` as an installable, upgrade-safe skill package.
- Split runtime semantics into `advisory`, `adapter-backed`, and `core-embedded`.
- Made `adapter-backed` the recommended production path.
- Added explicit statement that no core patch, no OpenClaw fork, and no bundled runtime modification are required.
- Added formal external adapter contract.
- Added upgrade-safe storage layout and config example.
- Added OpenClaw plugin/wrapper example files.
- Kept Python scripts as deterministic reference runtime and tests.
- Tightened package scope for clean ClawHub publication.
