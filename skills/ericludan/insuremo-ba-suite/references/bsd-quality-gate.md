# BSD Quality Gate — bsd-rule-linter Reference
# Version 1.0 | 2026-04-05

---

## Purpose

Defines the quality reference checks for BSD delivery. `bsd-rule-linter` is a **conceptual tool** — teams should implement this as a CI check or manual review checklist if no tooling is available.

**Relationship with agent2-bsd.md Self-Quality Gate:**
The BSD Self-Quality Gate (GATE-A/B/C) in `agent2-bsd.md` is the **executable quality checklist** used before BSD delivery. This file (`bsd-quality-gate.md`) is the **reference definitions** for the lint checks. Until CI tooling is available, use the Self-Quality Gate checklist in agent2-bsd.md as the substitution.

---

## Lint Check Items (10-point scale)

| Check | Item | Max Score | Scoring Criteria |
|-------|------|-----------|----------------|
| L01 | Rule Number format | 10 | All rules use BSD_[proj]_[gap]_SR[NN] format |
| L02 | No banned phrases | 10 | Zero instances of: "etc." / "TBD" / "as applicable" / "similar to existing" |
| L03 | Dual expression (formula rules) | 10 | Every formula rule has: (1) business sentence + (2) precise formula |
| L04 | Example Table (formula rules) | 10 | Every formula rule has ≥2 example rows in Pattern 7 table |
| L05 | INVARIANT for riders | 10 | All rider rules declare `Rider_Term ≤ Base_Policy_Term` |
| L06 | Constant source notes | 10 | Every numeric constant cites its source (e.g., "per product spec Section X") |
| L07 | ELSE consequence stated | 10 | Every IF has explicit THEN; every branch has explicit ELSE consequence |
| L08 | Field names quoted | 10 | All field names in single quotes: 'Field Name' |
| L09 | No prose-only rules | 10 | Rules with ≥3 steps use Pattern 5 enumeration, not prose |
| L10 | Traceability | 10 | Every rule maps to a Gap ID or CR ID |

**Total: 100 points**

**Threshold: ≥90 to pass. Below 90 = BLOCK delivery.**

---

## Per-Rule Scoring Template

For each business rule, apply this template mentally:

```
Rule: BSD_[proj]_[gap]_SR[NN]
├── L01 Rule Number    : ✅/❌ → Score: X/10
├── L02 Banned Phrases : ✅/❌ → Score: X/10
├── L03 Dual Expression: ✅/❌/N/A → Score: X/10
├── L04 Example Table  : ✅/❌/N/A → Score: X/10
├── L05 INVARIANT      : ✅/❌/N/A → Score: X/10
├── L06 Source Notes   : ✅/❌ → Score: X/10
├── L07 ELSE stated    : ✅/❌ → Score: X/10
├── L08 Field quoted   : ✅/❌ → Score: X/10
├── L09 Enumeration    : ✅/❌/N/A → Score: X/10
└── L10 Traceability   : ✅/❌ → Score: X/10

Rule Score: X/100
```

---

## Failure Handling

| Score | Status | Action |
|-------|--------|--------|
| 90-100 | ✅ PASS | Ready for delivery |
| 75-89 | ⚠️ CONDITIONAL PASS | Fix L01-L10 failures in review; document exceptions |
| 60-74 | 🔴 FAIL | Fix top 3 issues; re-lint before delivery |
| Below 60 | ⛔ BLOCK | Do not deliver. Rewrite rules per BSD patterns. |

---

## Manual Review Checklist (if no automated linter)

If `bsd-rule-linter` is not automated, run this checklist before every BSD delivery:

```
BSD Delivery Review Checklist
─────────────────────────────────────────────
[ ] No "etc." / "TBD" / "as applicable" in any rule
[ ] All rule numbers follow BSD_[proj]_[gap]_SR[NN]
[ ] Every formula has business sentence + math formula
[ ] Every formula has ≥2 example rows
[ ] Rider rules have INVARIANT declared
[ ] All numeric constants have source citations
[ ] Every IF has explicit ELSE consequence
[ ] All field names in single quotes
[ ] Rules with ≥3 steps use numbered list (not prose)
[ ] Every rule traces to a Gap or CR ID
─────────────────────────────────────────────
Total: ___ / 10 checks passed
Score: ___/100
Ready for delivery: YES / NO
```

---

## Scoring Weights by Rule Type

| Rule Type | Must Pass | Can Skip |
|-----------|----------|---------|
| Formula rules (Pattern 4) | L03, L04, L06 | N/A |
| Rider rules | L05 | N/A |
| Enumeration rules (Pattern 5) | L09 | L04 |
| Simple conditional (Pattern 3) | L02, L07, L08 | L03, L04, L05 |
| System default (Pattern 1) | L02, L08 | L03, L04, L05, L07 |
