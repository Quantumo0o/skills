# OpenClaw Self-Improve Checklists

## Preflight (all modes)
- Confirm mode (`audit-only`, `proposal-only`, `approved-implementation`).
- Confirm objective and measurable success criteria.
- Pick a primary metric set from `references/playbooks.md` if the objective is broad.
- Confirm target repo path.
- Run scaffold with `--dry-run` once to confirm resolved values.
- Scaffold a fresh run directory with `init-improvement-run.sh`.
- Capture current commit and branch.

## Mode: audit-only
- Capture reproducible symptom or baseline scenario.
- Capture baseline metrics.
- List top risks and unknowns.
- Do not draft implementation edits.

## Mode: proposal-only
- Complete all audit-only items.
- Create 1 to 3 hypotheses.
- Rank by impact and risk.
- Draft minimal change plan and rollback plan.
- Define exact validation commands and pass criteria.
- Set `Approval Status` to `pending` in `proposal.md`.

## Mode: approved-implementation
- Confirm proposal is explicitly approved and still relevant to current commit.
- Apply only approved edits.
- Run the agreed validation gate.
- Record baseline vs new values in `validation.md`.
- Update `outcome.md` with residual risk and next step.
- Run `validate-improvement-run.sh --run-dir <run-dir>` before handoff.
- If machine-consumed output is needed, run `export-improvement-run-json.py --run-dir <run-dir>`.
- If automation or CI depends on JSON artifacts, run `validate-improvement-run.sh --run-dir <run-dir> --require-json`.

## Completion Gate
- All required files exist: `run-info.md`, `baseline.md`, `hypotheses.md`, `proposal.md`, `validation.md`, `outcome.md`.
- Artifact validator passes.
- Validation result is explicit (`pass`, `fail`, `blocked`, or `inconclusive`).
- Status is filled in `baseline.md`, `validation.md`, and `outcome.md`.
- Rollback path is documented for behavior-changing edits.
- If automation or CI will consume the run, export `run-info.json` and `summary.json`.
- If automation or CI will consume the run, validator passes with `--require-json`.
