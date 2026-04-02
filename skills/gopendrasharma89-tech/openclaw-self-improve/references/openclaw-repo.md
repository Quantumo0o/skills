# OpenClaw Repo Map (Quick Reference)

## Repo Location
- Default local repo path: `/root/openclaw`
- If missing, ask user for repo path or clone source.

## Key Docs
- `/root/openclaw/README.md` for setup and runtime usage.
- `/root/openclaw/AGENTS.md` for repo guardrails and verification expectations.
- `/root/openclaw/docs/help/testing.md` for test lanes and scoped test guidance.

## Common Commands
- Install deps: `pnpm install` or `corepack pnpm install`
- Dev command: `pnpm openclaw ...` or `pnpm dev`
- Local quality gate: `pnpm check`
- Build gate: `pnpm build`
- Full tests: `pnpm test`
- Scoped test: `pnpm test -- <path-or-filter>`

If `pnpm` is missing in the shell, retry the same command with `corepack pnpm ...`.

## Typical Improvement Targets
- Agent behavior and prompts: `/root/openclaw/src/agents/`
- Gateway behavior: `/root/openclaw/src/gateway/`
- CLI and commands: `/root/openclaw/src/cli/`, `/root/openclaw/src/commands/`
- Plugin surfaces: `/root/openclaw/packages/`

## Validation Guidance
- For narrow changes, run focused tests on touched files first.
- If change affects shared runtime boundaries, run broader gate (`pnpm check`, `pnpm test`, `pnpm build`).
- Record exact commands and outcomes in `validation.md`.

## Safety Reminders
- Do not touch secrets, credential stores, or production config values during exploratory runs.
- Do not publish or version-bump without explicit user request.
- Keep diffs minimal and avoid unrelated cleanup during improvement cycles.
