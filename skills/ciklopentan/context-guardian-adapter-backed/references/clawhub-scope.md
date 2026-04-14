# ClawHub Packaging Scope

Publish target: installable skill package with adapter-backed deployment model.

## In scope

- `SKILL.md`
- `README.md`
- `references/`
- `scripts/`
- `plugin/`
- `PACKAGING_CHECKLIST.md`
- `CHANGELOG.md`
- `.clawhubignore`

## Out of scope

- local runtime state
- host secrets
- `.clawhub/`
- `_meta.json`
- cache directories
- test residue
- workspace-specific `.context_guardian/` data

## Honest publication statement

This package is installable on its own.
Near-full production behavior is delivered through external adapter-backed deployment.
No core patch is required for that deployment path.
