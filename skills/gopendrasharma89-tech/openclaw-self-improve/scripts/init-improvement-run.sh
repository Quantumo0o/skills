#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  init-improvement-run.sh --repo <path> [options]

Options:
  --timestamp <YYYYMMDD-HHMMSS>   Fixed run timestamp (default: current UTC)
  --mode <audit-only|proposal-only|approved-implementation>
  --objective <text>
  --scope <text>
  --validation-gate <text>
  --dry-run                        Print resolved values without creating files
  --force                          Overwrite an existing run directory safely

Creates:
  <repo>/.openclaw-self-improve/<timestamp>/
with files:
  run-info.md baseline.md hypotheses.md proposal.md validation.md outcome.md
USAGE
}

REPO=""
TIMESTAMP="$(date -u +%Y%m%d-%H%M%S)"
MODE="proposal-only"
OBJECTIVE=""
SCOPE=""
VALIDATION_GATE=""
DRY_RUN="false"
FORCE="false"

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      REPO="${2:-}"
      shift 2
      ;;
    --timestamp)
      TIMESTAMP="${2:-}"
      shift 2
      ;;
    --mode)
      MODE="${2:-}"
      shift 2
      ;;
    --objective)
      OBJECTIVE="${2:-}"
      shift 2
      ;;
    --scope)
      SCOPE="${2:-}"
      shift 2
      ;;
    --validation-gate)
      VALIDATION_GATE="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN="true"
      shift
      ;;
    --force)
      FORCE="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

REPO="$(trim "$REPO")"
MODE="$(trim "$MODE")"
TIMESTAMP="$(trim "$TIMESTAMP")"
OBJECTIVE="$(trim "$OBJECTIVE")"
SCOPE="$(trim "$SCOPE")"
VALIDATION_GATE="$(trim "$VALIDATION_GATE")"

if [[ -z "$REPO" ]]; then
  echo "Missing required --repo <path>" >&2
  usage >&2
  exit 1
fi

if [[ ! -d "$REPO" ]]; then
  echo "Repo path does not exist: $REPO" >&2
  exit 1
fi

case "$MODE" in
  audit-only|proposal-only|approved-implementation)
    ;;
  *)
    echo "Invalid --mode value: $MODE" >&2
    exit 1
    ;;
esac

if [[ ! "$TIMESTAMP" =~ ^[0-9]{8}-[0-9]{6}$ ]]; then
  echo "Invalid --timestamp format: $TIMESTAMP (expected YYYYMMDD-HHMMSS)" >&2
  exit 1
fi

REPO_ABS="$(cd "$REPO" && pwd)"
RUN_DIR="$REPO_ABS/.openclaw-self-improve/$TIMESTAMP"

if [[ -e "$RUN_DIR" ]]; then
  if [[ "$FORCE" != "true" ]]; then
    echo "Run directory already exists: $RUN_DIR" >&2
    echo "Use a different --timestamp or pass --force." >&2
    exit 1
  fi
  if [[ ! -d "$RUN_DIR" ]]; then
    echo "Existing path is not a directory: $RUN_DIR" >&2
    exit 1
  fi
fi

GIT_COMMIT="n/a"
GIT_BRANCH="n/a"
if git -C "$REPO_ABS" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  GIT_COMMIT="$(git -C "$REPO_ABS" rev-parse --short HEAD 2>/dev/null || echo n/a)"
  GIT_BRANCH="$(git -C "$REPO_ABS" rev-parse --abbrev-ref HEAD 2>/dev/null || echo n/a)"
fi

OBJECTIVE_VALUE="${OBJECTIVE:-TODO: define objective}"
SCOPE_VALUE="${SCOPE:-$REPO_ABS}"
VALIDATION_VALUE="${VALIDATION_GATE:-TODO: define validation gate commands}"

if [[ "$DRY_RUN" == "true" ]]; then
  cat <<EOF_DRYRUN
Dry run (no files created):
- Timestamp (UTC): $TIMESTAMP
- Mode: $MODE
- Repo: $REPO_ABS
- Objective: $OBJECTIVE_VALUE
- Scope: $SCOPE_VALUE
- Validation Gate: $VALIDATION_VALUE
- Run Dir: $RUN_DIR
EOF_DRYRUN
  exit 0
fi

mkdir -p "$RUN_DIR"

if [[ "$FORCE" == "true" ]]; then
  rm -f \
    "$RUN_DIR/run-info.md" \
    "$RUN_DIR/baseline.md" \
    "$RUN_DIR/hypotheses.md" \
    "$RUN_DIR/proposal.md" \
    "$RUN_DIR/validation.md" \
    "$RUN_DIR/outcome.md"
  if find "$RUN_DIR" -mindepth 1 -maxdepth 1 -print -quit | grep -q .; then
    echo "Refusing --force overwrite; directory has unexpected files: $RUN_DIR" >&2
    exit 1
  fi
fi

cat > "$RUN_DIR/run-info.md" <<EOF_INFO
# Run Info

- Timestamp (UTC): $TIMESTAMP
- Mode: $MODE
- Repo: $REPO_ABS
- Objective: $OBJECTIVE_VALUE
- Scope: $SCOPE_VALUE
- Validation Gate: $VALIDATION_VALUE
EOF_INFO

cat > "$RUN_DIR/baseline.md" <<EOF_BASELINE
# Baseline

## Objective
$OBJECTIVE_VALUE

## Scope
$SCOPE_VALUE

## Repo State
- Commit: $GIT_COMMIT
- Branch: $GIT_BRANCH

## Reproduction

## Metrics

## Risks

## Status
- pass|fail|blocked|inconclusive
EOF_BASELINE

cat > "$RUN_DIR/hypotheses.md" <<'EOF_HYP'
# Hypotheses

## Hypothesis 1

## Hypothesis 2

## Hypothesis 3

## Ranking
EOF_HYP

cat > "$RUN_DIR/proposal.md" <<EOF_PROP
# Proposal

## Selected Hypothesis

## Planned Changes

## Files To Edit

## Validation Gate
$VALIDATION_VALUE

## Rollback Plan

## Approval Status
- pending
EOF_PROP

cat > "$RUN_DIR/validation.md" <<EOF_VAL
# Validation

## Commands Run
$VALIDATION_VALUE

## Results

## Baseline vs New

## Pass/Fail

## Status
- pass|fail|blocked|inconclusive
EOF_VAL

cat > "$RUN_DIR/outcome.md" <<'EOF_OUT'
# Outcome

## Summary

## Evidence

## Residual Risk

## Next Iteration

## Status
- pass|fail|blocked|inconclusive
EOF_OUT

echo "$RUN_DIR"
