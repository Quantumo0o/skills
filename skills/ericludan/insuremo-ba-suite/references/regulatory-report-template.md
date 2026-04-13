# Regulatory Report Template — Agent 3 Output
# Version 1.0 | 2026-03-25

---

## Purpose

Standardized template for Agent 3 (Regulatory Compliance) output.
Covers: MAS (SG), BNM (MY), HKIA (HK), OID (VN), OJK (ID), and SEA-common.

---

## Document Header

```markdown
---
Document Type : Compliance Check / Regulatory Report
Project       : [Project Code]
Feature       : [Feature Name]
Version       : 1.0
Status        : Draft / Final
Created       : YYYY-MM-DD
Author        : [BA Name]
Markets       : [SG / MY / HK / VN / ID / ALL]
---
```
---

## Template Content

```markdown
# Regulatory Report: [Feature Name]
# Markets: [SG | MY | HK | VN | ID | ALL]

---

## 1. Executive Summary

[2-3 sentences: which markets, which regulations apply, overall compliance status]

---

## 2. Market Regulatory Mapping

| Market | Regulator | Applicable Regulation | Status | Gap Count |
|--------|-----------|---------------------|--------|-----------|
| SG     | MAS       | [Regulation name]   | ✅ Compliant / ⚠️ Gap | N |
| MY     | BNM       | [Regulation name]   | ✅ Compliant / ⚠️ Gap | N |
| HK     | HKIA      | [Regulation name]   | ✅ Compliant / ⚠️ Gap | N |
| VN     | OID       | [Regulation name]   | ✅ Compliant / ⚠️ Gap | N |
| ID     | OJK       | [Regulation name]   | ✅ Compliant / ⚠️ Gap | N |

---

## 3. Regulation Detail

### 3.1 Singapore (MAS)

#### Applicable Clauses
| Clause | Requirement | InsureMO Current State | Gap? |
|--------|-------------|----------------------|------|
| [Ref]  | [Text]      | [Description]        | Yes/No |

#### Compliance Assessment
**Status:** ✅ Compliant / ⚠️ Partial / 🔴 Non-Compliant

**Findings:**
- [Finding 1]
- [Finding 2]

#### Required Actions (if gap exists)
| Priority | Action | Owner | Deadline |
|----------|--------|-------|----------|
| [High/Med/Low] | [Description] | [Role] | YYYY-MM-DD |

---

### 3.2 Malaysia (BNM)
[same structure as 3.1]

### 3.3 Hong Kong (HKIA)
[same structure as 3.1]

### 3.4 Vietnam (OID)
[same structure as 3.1]

### 3.5 Indonesia (OJK)
[same structure as 3.1]

---

## 4. SEA-Common Requirements

| Ref | Requirement | Applicability | Status |
|-----|-------------|--------------|--------|
| SEA-COM-001 | [Text] | [All/SG/MY/etc.] | ✅/⚠️/🔴 |

---

## 5. Action Items Summary

| ID | Market | Issue | Priority | Owner | Deadline |
|----|--------|-------|----------|-------|----------|
| RA-001 | [Market] | [Description] | High/Med/Low | [Role] | YYYY-MM-DD |

---

## 6. Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Business Analyst | [Name] | YYYY-MM-DD | |
| Compliance | [Name] | YYYY-MM-DD | |
| Underwriting | [Name] | YYYY-MM-DD | |

---

## Usage Notes

- **Trigger:** Agent 3 runs for every product/project regardless of market
- **Market scope:** If project is single-market, mark other markets as N/A (not blank)
- **Gap threshold:** If any market has ≥1 non-compliant items → overall status = Non-Compliant
- **Update cadence:** Re-run Agent 3 if regulatory requirements change or product design changes
```