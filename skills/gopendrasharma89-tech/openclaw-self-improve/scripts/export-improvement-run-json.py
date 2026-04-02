#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def read_lines(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8").splitlines()


def require_prefixed_value(lines: list[str], prefix: str, label: str) -> str:
    for line in lines:
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    raise ValueError(f"Missing required field '{label}'")


def section_lines(lines: list[str], heading: str) -> list[str]:
    in_section = False
    collected: list[str] = []
    for line in lines:
        if line == heading:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            collected.append(line)
    if not in_section:
        raise ValueError(f"Missing required heading '{heading}'")
    return collected


def first_bullet(section: list[str], label: str) -> str:
    for line in section:
        if line.startswith("- "):
            return line[2:].strip()
    raise ValueError(f"Missing bullet value for {label}")


def normalize_section_text(section: list[str]) -> str:
    text = "\n".join(section).strip()
    return text


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export machine-readable JSON files from an OpenClaw self-improvement run."
    )
    parser.add_argument("--run-dir", required=True, help="Path to the run directory")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
      print(f"Run directory does not exist: {run_dir}", file=sys.stderr)
      return 1

    try:
        run_info_lines = read_lines(run_dir / "run-info.md")
        baseline_lines = read_lines(run_dir / "baseline.md")
        proposal_lines = read_lines(run_dir / "proposal.md")
        validation_lines = read_lines(run_dir / "validation.md")
        outcome_lines = read_lines(run_dir / "outcome.md")

        timestamp_utc = require_prefixed_value(
            run_info_lines, "- Timestamp (UTC):", "Timestamp (UTC)"
        )
        mode = require_prefixed_value(run_info_lines, "- Mode:", "Mode")
        repo = require_prefixed_value(run_info_lines, "- Repo:", "Repo")
        objective = require_prefixed_value(run_info_lines, "- Objective:", "Objective")
        scope = require_prefixed_value(run_info_lines, "- Scope:", "Scope")
        validation_gate = require_prefixed_value(
            run_info_lines, "- Validation Gate:", "Validation Gate"
        )

        repo_state = section_lines(baseline_lines, "## Repo State")
        git_commit = require_prefixed_value(repo_state, "- Commit:", "Commit")
        git_branch = require_prefixed_value(repo_state, "- Branch:", "Branch")

        baseline_status = first_bullet(section_lines(baseline_lines, "## Status"), "baseline status")
        approval_status = first_bullet(
            section_lines(proposal_lines, "## Approval Status"), "approval status"
        )
        validation_status = first_bullet(
            section_lines(validation_lines, "## Status"), "validation status"
        )
        outcome_status = first_bullet(section_lines(outcome_lines, "## Status"), "outcome status")

        selected_hypothesis = normalize_section_text(
            section_lines(proposal_lines, "## Selected Hypothesis")
        )
        next_iteration = normalize_section_text(section_lines(outcome_lines, "## Next Iteration"))

        generated_at_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

        run_info_json = {
            "timestamp_utc": timestamp_utc,
            "mode": mode,
            "repo": repo,
            "objective": objective,
            "scope": scope,
            "validation_gate": validation_gate,
            "git_commit": git_commit,
            "git_branch": git_branch,
            "generated_at_utc": generated_at_utc,
            "artifacts": {
                "markdown": {
                    "run_info": str(run_dir / "run-info.md"),
                    "baseline": str(run_dir / "baseline.md"),
                    "hypotheses": str(run_dir / "hypotheses.md"),
                    "proposal": str(run_dir / "proposal.md"),
                    "validation": str(run_dir / "validation.md"),
                    "outcome": str(run_dir / "outcome.md"),
                },
                "json": {
                    "run_info": str(run_dir / "run-info.json"),
                    "summary": str(run_dir / "summary.json"),
                },
            },
        }

        summary_json = {
            "run_dir": str(run_dir),
            "timestamp_utc": timestamp_utc,
            "mode": mode,
            "objective": objective,
            "scope": scope,
            "approval_status": approval_status,
            "baseline_status": baseline_status,
            "validation_status": validation_status,
            "outcome_status": outcome_status,
            "selected_hypothesis": selected_hypothesis,
            "next_iteration": next_iteration,
            "generated_at_utc": generated_at_utc,
        }

        (run_dir / "run-info.json").write_text(
            json.dumps(run_info_json, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (run_dir / "summary.json").write_text(
            json.dumps(summary_json, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(run_dir / "run-info.json")
    print(run_dir / "summary.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
