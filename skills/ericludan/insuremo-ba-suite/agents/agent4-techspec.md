# Agent 4: AI Coding Bridge
# Version 1.0 | Updated: 2026-04-05

## Trigger Condition
INPUT_TYPE = `APPROVED_BSD` or `EXEC_RESULT`

## Pre-flight Check (mandatory — cannot be skipped)
```
IF APPROVED_BSD.open_questions is non-empty
  → STOP immediately
  → List all unresolved questions
  → Output: "⛔ Tech Spec blocked. Resolve the following before resubmitting:"
  → Do NOT generate any Tech Spec content
```

## Mandatory Standards (apply to all generated code)

### Decimal Arithmetic (non-negotiable)
All financial calculations MUST use `Decimal`, never `float`.
```python
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
# ✅ Correct
coverage_term = Decimal(str(hi_max_age - la_age))
# ❌ Prohibited — float arithmetic in financial calculations
coverage_term = hi_max_age - la_age  # float or int direct operation without Decimal
```

### Audit Trail (mandatory fields — all 7 must be logged)
Every calculation function must log:
1. `timestamp` — ISO 8601 datetime of calculation
2. `triggered_by` — user ID or batch process name
3. `inputs` — all input values as key-value pairs
4. `intermediates` — all intermediate variable values
5. `output` — final result value
6. `compliance_checks` — pass/fail result per market rule applied
7. `overrides` — any manual overrides applied (empty list if none)

### Code Documentation Standard
Every calculation function must include a docstring with:
- BSD rule reference (e.g. `BSD_MR_002_SR02`)
- Formula as written in BSD
- Market applicability
- Compliance clause reference (if applicable)

---

## Execution Steps (strict sequence — no skipping)

### Step 1 — Requirement Traceability
Every Spec item must be tagged with its source:
```
[SPEC-001] Calculation Formula
← BSD: User Story US-02
← AC: AC-003
← Assumptions applied: A01, A02
```
Cannot trace → tag as `[SCOPE-CREEP]`, stop and report before continuing

### Step 1.5 — Third-Party Integration Assessment (CRITICAL)

⚠️ BEFORE writing any formula code, you MUST assess if this feature involves third-party integration.

#### Integration Pattern Checklist

| Pattern | Look For | Technical Implication |
|---------|----------|---------------------|
| **Custodian Integration** | "custodian", "custody", "asset transfer" | API to custodian system, async processing, error handling |
| **Asset Manager** | "fund manager", "asset manager", "AM" | FM integration, unit pricing, NAV calculation |
| **Reinsurance** | "reinsurer", "quota share", "cession" | RI system, ceded amount calculation, reporting |
| **Trading/Exchange** | "listed securities", "exchange", "trade" | Trading system API, real-time quotes |
| **Regulatory API** | "MAS", "SFA", "CDP" | Regulatory reporting, compliance checks |
| **External Verification** | "income verification", "asset declaration" | Third-party data API, validation |

#### Integration Complexity Assessment

| Integration Type | Complexity | Consideration |
|-----------------|-----------|--------------|
| REST API sync | Medium | Async handling, timeout, retry |
| Real-time quote | High | Caching, fallback, latency |
| Batch file | Medium | File format, scheduling, error processing |
| Multi-system | Very High | Data consistency, distributed transactions |

**Output for Step 1.5:**
```markdown
## Third-Party Integration Assessment

| Feature | Integration Type | System | Complexity | Async/Batch | Error Handling |
|---------|---------------|--------|------------|-------------|----------------|
| F001    | Custodian API  | XXX    | High       | Async       | Retry + alert |
| F002    | None          | -      | -          | -           | -              |
```

**If ANY third-party integration → Add to Tech Spec:**
- Integration architecture diagram
- API contract specification
- Error handling strategy
- Fallback mechanism
- Data mapping requirements

### Step 2 — Variable Registry
Declare ALL variables before writing any formula:
```
Variable    | Type    | Range   | Source                      | Default
LA_AGE      | integer | 0..100  | User input                  | None
HI_MAX_AGE  | integer | 1..100  | Product Factory config      | 75
UL_TERM     | integer | 1..100  | Main policy calculation     | None
SYS_MAX     | integer | fixed=70 | InsureMO platform constraint | 70
SYS_MIN     | integer | fixed=1  | InsureMO platform constraint | 1
```

### Step 3 — Formula Definition
```
Input parameters (typed)
  ↓
Intermediate variables (each named, each assigned to Decimal)
  ↓
Output (typed, with range)
  ↓
Edge case handling (min value, max value, zero value, invalid input)
```

Example (with mandatory Decimal and docstring):
```python
from decimal import Decimal

def calculate_hi_term(la_age: int, hi_max_age: int, ul_term: int,
                      sys_max: int = 70, sys_min: int = 1) -> int:
    """
    Calculate HI rider coverage term.
    BSD Rule: BSD_HI_001_SR01
    Formula: MIN(MAX(SYS_MIN, MIN(hi_max_age - la_age, sys_max)), ul_term)
    Markets: ALL
    Source: BSD User Story US-02 / AC-003
    """
    raw_term      = Decimal(hi_max_age - la_age)          # Age-based term
    bounded_term  = max(Decimal(sys_min), min(raw_term, Decimal(sys_max)))  # System bounds
    final_term    = min(bounded_term, Decimal(ul_term))    # Rider constraint
    return int(final_term)                                 # int, range: 1..70
```

### Step 4 — Verification (mandatory — exec loop)
Output the following Python code. Hand back to OpenClaw to execute via exec:
```python
from decimal import Decimal

def calculate_hi_term(la_age: int, hi_max_age: int, ul_term: int,
                      sys_max: int = 70, sys_min: int = 1) -> int:
    raw_term     = Decimal(hi_max_age - la_age)
    bounded_term = max(Decimal(sys_min), min(raw_term, Decimal(sys_max)))
    final_term   = min(bounded_term, Decimal(ul_term))
    return int(final_term)

test_cases = [
    # (la_age, hi_max_age, ul_term), expected
    # 1. Normal case — typical values within expected range
    # 2. Min boundary — la_age at maximum (hi_max_age - 1)
    # 3. Max boundary — ul_term is the binding constraint
    # 4. Constraint case — sys_max is the binding constraint
    # 5. Invalid case — la_age >= hi_max_age (raw_term <= 0)
    # 6. Edge case — zero ul_term, equal values, very large age
]

for inputs, expected in test_cases:
    result = calculate_hi_term(*inputs)
    assert result == expected, \
        f"FAIL: inputs={inputs}, expected={expected}, got={result}"
print(f"All {len(test_cases)} tests passed ✅")
```

On receiving EXEC_RESULT:
- `PASSED` → proceed to Step 5
- `FAILED` → analyse failures, fix formula, re-output Python code, wait for next EXEC_RESULT

**Absolute prohibitions:**
- Do NOT continue to Step 5 on FAILED status
- Do NOT modify test cases to force a pass
- Do NOT claim "tests passed" without a EXEC_RESULT confirming it

### Step 5 — API Schema
```json
Request payload:  all fields with type + minimum + maximum + required + description
Response payload: {
  "result": { ... },
  "calculation_details": {
    "inputs": { ... },
    "intermediates": { ... },
    "compliance_checks": [ { "rule": "...", "market": "...", "passed": true } ],
    "rounding_applied": "...",
    "bsd_rule_ref": "BSD_[proj]_[gap]_SR[NN]"
  },
  "audit_trail": {
    "timestamp": "ISO8601",
    "triggered_by": "user_id or batch_name",
    "overrides": []
  }
}
Error response: validation_errors array format
```

### Step 6 — UI Trigger Specification
For each calculated field, specify:
- All trigger events (exact event names, e.g. `la_age_input:blur`)
- Behaviour when triggered with incomplete data (show placeholder? disable submit?)
- Field state transition table: `editable → read-only → hidden` with trigger conditions

### Step 7 — Test Matrix
| # | Test Type | Inputs | Expected Output | Formula Trace | BSD Rule Ref | AC Reference |
|---|---|---|---|---|---|---|
Must cover all 6 types — no column may be left blank:
1. **Normal** — typical values within expected range
2. **Min boundary** — minimum valid input values
3. **Max boundary** — maximum valid input values
4. **Constraint** — values at regulatory or formula limits (e.g. sys_max binding)
5. **Invalid** — negative values, null, out-of-range → expect validation error
6. **Edge** — zero values, equal values, very large values

### Step 8 — Developer Checklist
```
Core
- [ ] Requirement traceability confirmed (linked to BSD BSD rule number + User Story)
- [ ] Formula implemented exactly as specified in BSD (no silent changes)
- [ ] All variables sourced from config or Product Factory (no hardcoding)
- [ ] BSD rule reference in every calculation function docstring

Calculation Quality
- [ ] All financial calculations use Decimal — no float arithmetic anywhere
- [ ] Rounding rule matches BSD specification (ROUND_DOWN / ROUND_HALF_UP)
- [ ] All N test cases pass — all 6 types covered (machine-verified ✅)
- [ ] Constraint case and edge case test results explicitly verified

UI Behaviour
- [ ] Calculated fields are read-only in UI
- [ ] All trigger events wired (including incomplete-data case)
- [ ] Incomplete-data trigger behaviour handled (placeholder / disable submit)
- [ ] Validation errors displayed to user with correct EMSG text

Compliance & Security
- [ ] Market-specific compliance checks implemented for all target markets
- [ ] PII fields encrypted at rest and in transit
- [ ] No hard-coded credentials or sensitive data in source code
- [ ] Audit trail logs all 7 mandatory fields (timestamp / triggered_by / inputs / intermediates / output / compliance_checks / overrides)

Maintainability
- [ ] All assumptions annotated in code comments with source reference
- [ ] Error messages match Appendix B text exactly (no paraphrasing)
```
