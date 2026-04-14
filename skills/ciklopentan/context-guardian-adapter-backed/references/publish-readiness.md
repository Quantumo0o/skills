# Publish Readiness

A release is publish-ready only when all items below are true.

- Runtime mode wording is honest and consistent.
- `advisory` and `adapter-backed` semantics are clearly separated.
- `SKILL.md` states that no core patch is required.
- Adapter contract exists and matches examples.
- Storage layout is upgrade-safe and persistent.
- Example config exists.
- Example state and summary files exist.
- Reference runtime and tests exist.
- Plugin/wrapper example exists.
- `.clawhubignore` excludes runtime junk and local state.
- `CHANGELOG.md` has a release entry.
- Package scope is explicitly documented.
