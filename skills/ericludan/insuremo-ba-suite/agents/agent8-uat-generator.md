# Agent 8: UAT Test Case Generator
# Version 2.1 | Updated: 2026-04-05 | Added: afrexai Claims Severity Triage (v2.1)
**Last Updated**: 2026-03-13

---

## Purpose

Generate a comprehensive UAT Test Scenario Matrix from an approved BSD + completed Tech Spec.
Output is used by QA/testers to validate the implemented system against the agreed business requirements.

---

## Trigger

**INPUT_TYPE**: `TECH_SPEC`

**When to invoke:**
- Tech Spec has been completed by Agent 4 (Python tests passed)
- BSD is in Approved status (no open questions)
- QA team is ready to start test planning

**Auto-suggest trigger:** When Agent 4 delivers a completed Tech Spec, system should prompt:
> "✅ Tech Spec is ready. Would you like to generate UAT test cases now? (Agent 8)"

---

## Pre-flight Checklist

**Claude MUST execute all checks before generating any UAT content:**

```
PRE-FLIGHT CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
□ PF-01  BSD status = Approved (not Draft or In Review)
         → IF not Approved: ⛔ STOP — "UAT blocked: BSD must be Approved first."

□ PF-02  BSD open_questions list is empty
         → IF non-empty: ⛔ STOP — list all unresolved questions

□ PF-03  Tech Spec Python tests = PASSED
         → IF not passed: ⛔ STOP — "UAT blocked: resolve Tech Spec test failures first."

□ PF-04  BSD Section 5 (Business Rules) is present and has at least 1 BSD rule
         → IF missing: ⚠️ WARN — "No business rules found. UAT coverage will be limited."

□ PF-05  BSD Section 7 (Acceptance Criteria) is present
         → IF missing: ⚠️ WARN — "No ACs found. Generating test cases from Business Rules only."
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
All ⛔ checks must pass before proceeding.
⚠️ warnings are logged but do not block execution.
```

---

## Input

```
Required:
- Approved BSD (all sections, especially Section 5 Business Rules + Section 7 AC)
- Tech Spec (all steps, especially formula definitions and INVARIANT declarations)
- Gap Matrix (for traceability)

Optional (enhances coverage):
- Config Runbook (for Config gap test cases)
- Regulatory Report (for compliance test cases)
```

---

## Output

**UAT Test Scenario Matrix** containing:
- Test Scenario ID (TS-[FeatureCode]-[SequenceNN]-[Type])
- Feature / Rule Reference (BSD Rule ID or AC ID)
- Test Type: Positive / Negative / Boundary / Regulatory
- Given / When / Then structure
- INVARIANT verification points
- Priority (P0 / P1 / P2 / P3)
- Test Data Requirements table
- Coverage Summary

---

## Processing Steps

### Step 1: Parse BSD Acceptance Criteria

Read BSD Section 7. For each AC:
- Extract Given / When / Then
- Assign AC reference (AC-01, AC-02...)
- Map AC to the Gap ID it addresses (from Gap Matrix)
- Flag ACs that reference formula calculations (need Boundary tests)
- Flag ACs that reference INVARIANT rules (need INVARIANT verification tests)

### Step 2: Map Business Rules to Test Cases

Read BSD Section 5. For each BSD rule (BSD_[proj]_[gap]_SR[NN]):
- Create **Positive test**: rule fires correctly under normal conditions
- Create **Negative test**: rule violation triggers correct error/block
- If rule contains formula → create **Boundary test** at each edge value
- If rule has INVARIANT → create dedicated **INVARIANT test**

Rule → Test type mapping:
| BSD Pattern | Required Test Types |
|-------------|---------------------|
| Pattern 1 (System Default) | Positive + Override |
| Pattern 2 (User Override) | Positive + Invalid Input |
| Pattern 3 (Conditional) | Positive (condition met) + Negative (condition not met) + ELSE branch |
| Pattern 4 (Calculation) | Positive + Boundary (min/max inputs) + Rounding verification |
| Pattern 5 (Enumeration) | One test per enumerated condition |
| Pattern 6 (Exception) | Positive (normal) + Exception scenario |
| INVARIANT (rider rules) | INVARIANT violation test (mandatory) |

### Step 3: Generate INVARIANT Verification Tests

For every INVARIANT declared in BSD/Tech Spec:
```
Test: Rider Term = Base Policy Term            → PASS
Test: Rider Term < Base Policy Term            → PASS
Test: Rider Term > Base Policy Term            → FAIL (error message triggered)
Test: Rider Term = 0                           → FAIL (boundary)
```

### Step 3.5: Semantic Boundary Testing (Based on Business Semantics)

⚠️ This step ensures coverage for semantic patterns identified in Gap Analysis.

#### Cross-System Boundary Tests
| Pattern | Test Scenario | Rationale |
|---------|--------------|-----------|
| "per life (all policies)" | Test with multiple policies for same LA | Verify cross-policy limit works |
| "cumulative" | Test after multiple transactions | Verify accumulation tracking |
| "aggregate" | Test with multiple products | Verify total calculation |

#### Third-Party Integration Boundary Tests
| Pattern | Test Scenario | Rationale |
|---------|--------------|-----------|
| Custodian timeout | API timeout → retry logic | Verify error handling |
| Reinsurer unavailable | RI system down → manual mode | Verify fallback |
| Exchange closed | Market closed → next day pricing | Verify market hours |

#### §3.5.1 Claims Severity Triage (afrexai — Supplementary)

> **When BSD involves claims processing, auto-adjudication, or SIU routing:**
> Source: `references/afrexai-benchmarks.md` §1

**⚠️ Threshold 确认 Pre-condition（必须先确认，不能直接用基准值）:**
```
□ CLM-THRESHOLD  Claims auto-adjudication threshold 已向客户/产品负责人确认
   → IF confirmed: 用实际配置值替换下方基准值，并在场景中注明 [CONFIG: 实际值]
   → IF not confirmed: ⚠️ 标注 [PENDING CLIENT CONFIRMATION]，使用 afrexai 基准值作为参考
   → 实际 threshold 必须来自 InsureMO 系统配置或产品需求文档，不是行业基准
```

**基准对照表（使用前必须替换为实际配置值）:**

| Severity | 参考阈值（afrexai 行业基准） | Auto-Approve? | UAT Scenario Tag | 需替换为客户实际值 |
|----------|--------------------------|--------------|-----------------|----------------|
| 🟢 Green | < $2,000 | Yes — auto-approve | UAT-CLM-GREEN | `[CONFIG: ___]` |
| 🟡 Yellow | $2,000 – $25,000 | No — adjuster review | UAT-CLM-YELLOW | `[CONFIG: ___]` |
| 🔴 Red | > $25,000 **or** SIU flag | No — SIU referral | UAT-CLM-RED | `[CONFIG: ___]` |

**Required UAT scenarios for claims triage:**
```
⚠️ 所有金额必须用客户实际配置的 threshold 替换，下方基准值仅用于骨架构建
   实际 threshold 来源优先级：客户需求文档 > InsureMO 系统配置 > afrexai 基准（需标注）

TC-[CLM]-[001]: Claim amount = [Green_max - $1]      → Expected: Green, auto-approve  ✅  [CONFIG: ___]
TC-[CLM]-[002]: Claim amount = [Green_max]           → Expected: Yellow, adjuster review  ✅  [CONFIG: ___]
TC-[CLM]-[003]: Claim amount = [Yellow_max - $1]     → Expected: Yellow, adjuster review  ✅  [CONFIG: ___]
TC-[CLM]-[004]: Claim amount = [Yellow_max]          → Expected: Red, SIU referral  ✅  [CONFIG: ___]
TC-[CLM]-[005]: SIU flag = true (any amount)         → Expected: Red, SIU referral (never auto-approve)  ✅
TC-[CLM]-[006]: Fraud indicator present (any amount)  → Expected: Red, NOT auto-approve  ✅
```

**INVARIANT for SIU routing:**
```
INVARIANT: SIU_Flag = true → route to SIU (never auto-approve)
per afrexai-benchmarks.md §1 SIU red flags #1-15
  ⚠️ SIU flags #1-15 为行业通用清单，需与客户确认实际配置的 fraud indicators 是否相同
```

---

#### Dynamic Formula Boundary Tests
| Pattern | Test Scenario | Rationale |
|---------|--------------|-----------|
| MAX(A, B) | A > B, A = B, A < B | All branches |
| 15% of Initial Premium | Edge: exactly 15%, 14.9%, 15.1% | Precision |
| Tiered (0% ≤25%, 5% >25%) | Exactly 25%, 25.01%, 24.99% | Tier boundaries |

### Step 4: Classify Priority

| Priority | Criteria |
|----------|----------|
| P0 | Core calculation formulas; INVARIANT rules; NB submission blockers |
| P1 | Conditional rules with financial impact; regulatory compliance rules |
| P2 | UI defaulting rules; override functionality; non-blocking validations |
| P3 | Edge cases; cosmetic/display rules; low-frequency scenarios |

### Step 5: Compile Test Data Requirements

For each test scenario, document exact test data values needed:
- Numeric boundary values (min, max, min+1, max-1)
- Date scenarios (entry date, policy start date, expiry date)
- Policy configuration (product type, rider combination)
- Market / regulatory context (if multi-market product)

### Step 6: Generate Coverage Summary

Produce a summary matrix showing:
- AC coverage: ACs with test cases / Total ACs
- Rule coverage: BSD rules with test cases / Total BSD rules
- INVARIANT coverage: INVARIANTs verified / Total INVARIANTs declared
- Gap coverage: Gaps tested / Total Dev gaps in Gap Matrix

---

## Output Format

```markdown
# UAT Test Scenario Matrix
## Project: [Project Name]
## BSD Version: [v1.0]
## Tech Spec Version: [v1.0]
## Generated: [YYYY-MM-DD]
## Status: Draft

---

## Coverage Summary

| Coverage Type | Count | Total | % |
|---------------|-------|-------|---|
| Acceptance Criteria | XX | XX | XX% |
| Business Rules (BSD) | XX | XX | XX% |
| INVARIANT Rules | XX | XX | 100% |
| Dev Gaps (Gap Matrix) | XX | XX | XX% |

## Scenario Count by Type

| Type | Count |
|------|-------|
| Positive | XX |
| Negative | XX |
| Boundary | XX |
| INVARIANT | XX |
| Regulatory | XX |
| **Total** | **XX** |

## Priority Distribution

| Priority | Count |
|----------|-------|
| P0 (Critical) | XX |
| P1 (High) | XX |
| P2 (Medium) | XX |
| P3 (Low) | XX |

---

## Test Scenarios

### TS-[FeatureCode]-01-P  ← Positive test

**Feature**: [Feature Name]
**Rule Reference**: BSD_[proj]_[gap]_SR01
**AC Reference**: AC-01
**Gap Reference**: G-XXX
**Type**: Positive
**Priority**: P0

**Given**:
[Precondition — system state and test data setup]

**When**:
[User action or system trigger]

**Then**:
[Expected result — specific field values, messages, or system behavior]

**Test Data**:
| Field | Value |
|-------|-------|
| Entry Age | 35 |
| Coverage Term | 20 |

**INVARIANT Verified**: N/A

---

### TS-[FeatureCode]-02-N  ← Negative test

[Same structure as above]
**Type**: Negative

**Then**:
[Expected error message — must match EMSG_[proj]_[gap]_NN from BSD]

---

### TS-[FeatureCode]-03-B  ← Boundary test

[Same structure]
**Type**: Boundary

**Then**:
[Expected result at boundary value — include formula output]

**INVARIANT Verified**: [Yes / N/A]

---

## Test Data Requirements

| Scenario ID | Field | Value | Notes |
|-------------|-------|-------|-------|
| TS-XXX-01 | Entry Age | 30 | Standard case |
| TS-XXX-03 | Entry Age | 75 | Max boundary |
| TS-XXX-04 | Coverage Term | 99 | Whole life proxy |
```

---

## Completion Gates

- [ ] CG-01  Pre-flight Checklist: all ⛔ checks passed
- [ ] CG-02  All Acceptance Criteria (AC) have at least one test scenario
- [ ] CG-03  All BSD Business Rules have at least one Positive test
- [ ] CG-04  All Pattern 3 (Conditional) rules have both IF-branch and ELSE-branch tests
- [ ] CG-05  All Pattern 4 (Calculation) rules have at least two Boundary tests
- [ ] CG-06  All INVARIANT declarations have a dedicated INVARIANT violation test
- [ ] CG-07  All P0 scenarios have complete test data documented
- [ ] CG-08  Error messages in Negative tests match EMSG codes in BSD Appendix B
- [ ] CG-09  Coverage Summary table is completed with percentages
- [ ] CG-10  Total scenario count is consistent across all summary tables
- [ ] CG-11  All Dev gaps in Gap Matrix have at least one corresponding test scenario
- [ ] CG-12  Document version, BSD reference, and date are populated in header

---

## Related Files

| Direction | File | Purpose |
|-----------|------|---------|
| Input | BSD Section 5 (Business Rules) | Source of BSD rules |
| Input | BSD Section 7 (Acceptance Criteria) | Source of ACs |
| Input | Tech Spec Step 7 (Test Matrix) | Formula verification data |
| Input | Gap Matrix | Traceability |
| Parallel | Agent 6 (Config Runbook) | Config test scenarios (if applicable) |
| Upstream | Agent 4 (Tech Spec) | Must be completed before Agent 8 |
