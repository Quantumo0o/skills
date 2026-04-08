# Implementation Notes

Use Python for the reference module when the host project does not already mandate a different language.

Recommended layout:
- `scripts/context_guardian.py` — reference implementation
- `references/task-state-schema.md` — canonical state contract
- `references/summary-template.md` — structured summary format
- `references/config-example.yaml` — configuration shape
- `references/persisted-task-state.example.json` — persisted state example
- `references/summary-example.md` — markdown summary example
- `references/integration-checklist.md` — host loop integration checklist
- `scripts/test_context_guardian.py` — behavior tests

Practical rule:
- Keep low-value conversation history out of the working bundle once durable state exists.
- Always prefer a fresh checkpoint over guessing.
