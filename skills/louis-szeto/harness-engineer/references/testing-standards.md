# TESTING STANDARDS

Testing is the primary deterministic verification layer. LLM judgment is never a
substitute for a failing test. Deterministic constraints are always checked before
LLM-based review.

---

## VERIFICATION ORDER (deterministic first)

1. Pre-commit hooks (linter, formatter, type-checker) -- must pass before ANY test run
2. Unit tests
3. Integration tests
4. E2E tests
5. Then: 3-layer recursive review cycle (agents/reviewer.md)

LLM review runs LAST, after all deterministic checks pass.
A passing LLM review does not override a failing test.

---

## PRE-COMMIT HOOKS (mandatory)

Every repo using this harness must have pre-commit hooks that:
  - Run the linter (no lint errors allowed)
  - Run the type-checker if applicable (no type errors)
  - Run a formatter check (no unformatted files)
  - Block the commit if any hook fails

Pre-commit hooks are deterministic, fast, and do not require LLM judgment.
They catch the largest class of common errors at zero extra cost.

Configure in .pre-commit-config.yaml or equivalent for the stack.

---

## REQUIRED TESTS

Unit tests:
  - Coverage >= 90% on all changed files (CONFIG.yaml testing.coverage_minimum)
  - Each test must be deterministic -- no random failures, no time-dependent assertions
  - Each test must be isolated -- no shared mutable state between tests
  - Fast: < 100ms per test

Integration tests:
  - At least one per major code path affected by the plan
  - Test the contract between components, not internals

E2E tests:
  - At least one per user-facing behavior in the plan
  - Exercises the full stack from input to output

---

## RECOMMENDED (required on critical paths)

Fuzz tests:
  - All input parsing, serialization, external data ingestion

Property-based tests:
  - Algorithms with invariants

---

## COVERAGE RULE

Minimum 90% line coverage on changed files.
Coverage alone is insufficient. Tests must assert correct behavior, not just execute lines.
A test that always passes regardless of code is worse than no test.

---

## TEST QUALITY RULES

- Tests must be meaningful -- assert the behavior described in the plan
- Tests must be maintainable -- clear test name, clear assertion message
- Tests must not suppress errors -- no bare except, no ignoring failures

---

## FAILURE PROTOCOL

When tests fail:
1. collect_logs() immediately
2. Identify the smallest failing case
3. Dispatch debugger_agent with failure log and test output
4. Identify harness gap category (runtime/observability.md)
5. Do NOT merge. Do NOT advance cycle phase.
6. Write MEMORY.md entry (EPISODIC type)

---

## TEST RESULT FORMAT (required from tester_agent)

```json
{
  "phase": "unit | integration | e2e | fuzz",
  "passed": 0,
  "failed": 0,
  "skipped": 0,
  "coverage": "0%",
  "failures": [
    {
      "test": "test_name",
      "file": "tests/path.test.ts",
      "reason": "AssertionError: expected X got Y",
      "log_ref": "CYCLE-NNN tool-log entry ID"
    }
  ]
}
```

Note: log_ref points to a tool-log entry ID -- never raw log content.
