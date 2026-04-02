# Improvement Playbooks

Use this file when the user gives a broad goal but not a precise metric set. Pick one primary playbook and keep the first iteration small.

## Reliability
- Start metrics:
  - failing tests or workflows
  - flake rate
  - retry count
  - explicit error count
- Strong validation gates:
  - deterministic scoped tests
  - repeated reruns for stability
  - before/after failure counts
- Common failure modes:
  - ambient environment leakage into tests
  - hidden dependency on local state
  - broad fixes without a reproduced baseline

## Performance
- Start metrics:
  - p50 or p95 latency
  - startup time
  - memory or CPU usage
  - tokens or tool calls per task
- Strong validation gates:
  - same input before/after timings
  - warmed and cold run comparisons
  - no regression in correctness checks
- Common failure modes:
  - comparing different workloads
  - trading correctness for speed without measuring it
  - using noisy one-off timings as proof

## Quality
- Start metrics:
  - regression count
  - user-visible defect count
  - touched-area test coverage
  - correctness on representative examples
- Strong validation gates:
  - focused tests on touched files
  - one representative end-to-end scenario
  - explicit rollback path for behavior changes
- Common failure modes:
  - vague claims like "better UX" without concrete checks
  - broad refactors mixed into targeted fixes
  - no evidence tied to the changed behavior

## Cost
- Start metrics:
  - tokens per workflow
  - paid API calls per task
  - unnecessary tool invocations
  - repeated retries from avoidable failures
- Strong validation gates:
  - before/after task cost comparison
  - same scenario replay with identical scope
  - no drop in reliability or correctness
- Common failure modes:
  - reducing cost by silently skipping work
  - measuring only one unusually cheap run
  - untracked hidden costs moved to another step
