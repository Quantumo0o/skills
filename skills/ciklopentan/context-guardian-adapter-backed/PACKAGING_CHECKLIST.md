# Packaging Checklist

Version target: 2.2.0
Slug target: context-guardian-adapter-backed

## Include in published package

- `SKILL.md`
- `README.md`
- `references/`
- `scripts/context_guardian.py`
- `scripts/test_context_guardian.py`
- `plugin/`
- `plugin/context-guardian-adapter.js`
- `plugin/test_context_guardian_adapter.js`
- `plugin/openclaw-runtime-plugin/`
- `PACKAGING_CHECKLIST.md`
- `CHANGELOG.md`
- `.clawhubignore`

## Exclude from published package

- `.clawhub/`
- `_meta.json`
- `__pycache__/`
- `*.pyc`, `*.pyo`
- `.pytest_cache/`, `.mypy_cache/`
- `.context_guardian/`
- temporary test output directories
- local logs
- local snapshots
- local secrets

## Pre-publish checks

- [ ] File tree matches intended publish scope.
- [ ] `SKILL.md` includes runtime mode split and exact no-core-patch wording.
- [ ] Adapter contract exists.
- [ ] Storage layout exists.
- [ ] Config example exists.
- [ ] Plugin example exists.
- [ ] Working Node adapter CLI exists.
- [ ] Native OpenClaw runtime plugin package exists.
- [ ] Python tests pass.
- [ ] Node adapter tests pass.
- [ ] Native plugin smoke test passes.
- [ ] Weak-model validation passes.
- [ ] `.clawhubignore` excludes local runtime state.
- [ ] Version and changelog match publish target.
