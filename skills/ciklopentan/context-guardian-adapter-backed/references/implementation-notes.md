# Implementation Notes

Use Python as the deterministic reference runtime.
Use Node.js or TypeScript for the preferred external adapter/plugin path.
Keep the adapter thin.
Keep storage filesystem-first.
Keep state outside bundled runtime code.

## Recommended architecture

- Skill package ships the contract, examples, schema, and deterministic references.
- External adapter owns persistence, pressure input, halt, resume, and wrapper hooks.
- Host runtime consumes the adapter outputs without needing core patches.

## OpenClaw-specific practical path

- Install the skill normally.
- Run a workspace-level adapter or plugin beside OpenClaw.
- Mount a persistent root path for continuity state.
- Call the adapter around major actions.
- Keep `scripts/context_guardian.py` as the truth reference for storage semantics and tests.

## Reference/runtime split

- Python files are deterministic reference and tests only.
- Node path is the preferred production adapter implementation.
- The package now includes a native OpenClaw hook-only plugin package that calls the adapter through official plugin hooks.
- The external adapter exposes a small surface: `status`, `ensure`, `checkpoint`, `bundle`, `halt`, `resume`.
