# Standard Output Templates
# Version 3.0 — aligned with eBaoTech BSD document structure
# Based on: BSD_Policy_Servicing_MVP3_Blueprint_1_3_V0_7, BSD_BCP_MVP3_Blueprint_1_V0_3, BSD_Finance_MVP3_T2_1_V0_4
# Last updated: 2026-04-03 — v3.0: BSD v9.0 Full vs Lite format separation; Appendix C: Full vs Lite decision guide; Appendix D: Example Table standard format (Pattern 7); UAT Scenario ID column mandatory

> Standard file headers and structure templates for each Agent's output.
> Ensures consistent formatting across BAs and projects.
> These templates reflect the actual document format used in production InsureMO projects.

---

## File Naming Convention

```
[DocType]_[ProjectCode]_[FeatureName]_v[N.N].[ext]

Examples:
RequirementBrief_PS3_HI_RiderTerm_20260309.md
GapMatrix_PS3_HI_RiderTerm_20260309.md
BSD_PS3_HI_RiderTerm_v0.1.md              ← BSD output uses BSD naming
TechSpec_PS3_HI_RiderTerm_v1.0.md
ComplianceCheck_PS3_HI_RiderTerm_MY_20260309.md
ConfigRunbook_PS3_HI_RiderTerm_MY_20260309.md
ImpactMatrix_PS3_HI_RiderTerm_20260309.md
ProductProfile_[ProductName]_[Market]_20260309.md
```

---

## Standard Document Header (all documents)

```markdown
---
Document Type : [BSD / Requirement Brief / Gap Matrix / Tech Spec / Compliance Check / Config Runbook / Impact Matrix]
Project       : [e.g. Policy Servicing MVP3]
Feature       : [e.g. ILP Recurring Single Premium]
BSD Reference : [BSD_PS3_036 / N/A]
Version       : 0.1
Status        : [Draft / Under Review / Approved]
Created       : YYYY-MM-DD
Last Updated  : YYYY-MM-DD
Author        : [BA Name]
Reviewer      : [TBD]
Markets       : [MY / SG / ALL]
---
```

Change Record table (required on all documents):
```markdown
| Date       | Author | Version | Note          | Reviewer |
|------------|--------|---------|---------------|----------|
| YYYY-MM-DD | [name] | V0.1    | Initial draft |          |
```

Related Documents (if applicable):
```markdown
| Release Date | Title of Document | Version |
|--------------|-------------------|---------|
```

Sign-off Form (required on BSD / BSD):
```markdown
| Name | Department and Role | Signature | Sign-off Date |
|------|---------------------|-----------|---------------|
```

---

## Requirement Brief Template (Agent 0 output)

```markdown
# Requirement Brief: [Feature Name]
[Standard document header]

## 1. Overview
[2-3 sentences: business context + what this requirement addresses]

## 2. End Users
[List of roles who will use or be affected by this feature]

## 3. Problem Statement
[Who + what problem + business consequences of current state]

Key Pain Points:
- [Pain point 1: frequency, impact]
- [Pain point 2: frequency, impact]

## 4. As-Is Process
1. [Step 1]
2. [Step 2]

## 5. To-Be Target
[Desired new system behaviour — no implementation details]

## 6. Scope
In scope: [products, markets, screens, PS items, batch names]
Explicitly out of scope: [list — must be client-confirmed, not BA-assumed]

## 7. Stakeholder Map
| Stakeholder | Department and Role | Primary Concern | Sign-off Required? |
|-------------|---------------------|-----------------|--------------------|

## 8. Assumption Register
| ID   | Assumption | Source | Status | Impact if Wrong |
|------|------------|--------|--------|-----------------|

## 9. Open Questions
| ID   | Question | Owner | Due Date | Blocks Implementation? |
|------|----------|-------|----------|------------------------|

## 10. Acronyms
| Acronym | Description |
|---------|-------------|
```

---

## Gap Matrix Template (Agent 1 output)

```markdown
# Gap Matrix: [Feature Name]
[Standard document header]

## Gaps Covered
| Gap Number | Gap Name | Gap Type | OOTB Support | Solution / Config Path | Impact: Billing | Impact: Claims | Impact: RI | Priority |
|------------|----------|----------|--------------|------------------------|-----------------|----------------|------------|----------|

## Change Requests Covered
| CR ID | CR Description | Section | Approved by Users? | Approved by CC Board? |
|-------|----------------|---------|--------------------|-----------------------|

## Summary
- OOTB Supported : X items
- Config Gap      : X items (Product Factory config only)
- Dev Gap         : X items (requires development scheduling)
- Process Gap     : X items (business process change required)
- High Priority   : X | Medium: X | Low (Backlog): X
```

---

## BSD / BSD Template (Agent 2 output)

This is the primary delivery document format used in InsureMO projects.
One BSD file covers all gaps in a single feature or sprint epic.

> **Writing Standard:** Business Rules sections MUST use BSD business language — 7 Patterns defined below.
> Primary audience: business stakeholders. Rules must be readable and verifiable without developer interpretation.
> **Dual-expression rule (mandatory for all formulas):** Every calculation must include BOTH a business-language sentence AND a precise mathematical formula on the next line.
> **Example Table (mandatory for all formula rules):** Every rule containing a formula must include a "For Example" table with concrete numbers.
> **Enumeration rule:** Any rule with 3 or more steps must use Pattern 5 numbered structure — prose paragraphs are prohibited.
> **G6/G7 mandatory for Dev Gap BSDs:** Section 4 Data Dictionary and Section 2.5 Non-Functional Requirements must be completed for Dev Gap features. Write "N/A" only if no new fields are introduced.
> Technical variable names (snake_case) belong in Formula Reference within the rule cell and in Appendix B — not in the rule body.
> Cross-reference: output-standards.md RED LINE 9 (no bare formula) and RED LINE 10 (no prose rules) apply to all Business Rules output.

```markdown
# BSD: [Feature Name]
# [BSD Reference]
[Standard document header including Change Record, Related Documents, Sign-off Form]

---

# Chapter 1: Introduction

## 1.1 Overview
[2-3 sentences describing the business context and what this BSD addresses]

## 1.2 End Users
[Roles: e.g. CS User, PS User, Underwriter, Batch Process]

## 1.3 Glossary

### 1.3.1 Definitions
[Free-text definitions for project-specific terms, or "N/A"]

### 1.3.2 Acronyms
| Acronym | Description |
|---------|-------------|
| PS      | Policy Servicing |
| CS      | Customer Service |
| ILP     | Investment-Linked Policy |
| [add]   | [add]       |

---

# Chapter 2: Requirements

## 2.1 Gaps Covered
| Gap Number | Gap Name | BSD Chapter / Rule Numbers |
|------------|----------|---------------------------|
| PS3_036    | [Name]   | 3.1.5 Business Rules       |
|            |          | BSD_PS3_036_SR01           |
|            |          | BSD_PS3_036_SR02           |

---

# Chapter 3: Business Solutions

## 3.1 [Gap Name]

### 3.1.1 Solution Summary
To enhance the following:
1. [Specific system change 1]
2. [Specific system change 2]

### 3.1.2 Solution Assumptions
[Numbered list, or "N/A"]

### 3.1.3 Business Process Flow Diagram
[Figure N: [Diagram Name], or "N/A"]

### 3.1.4 Function Description

**Preconditions:**
1. [Condition 1]
2. [Condition 2]
(or "N/A")

**Normal Flow:**
1. [User/system action 1]
2. [User/system action 2]
3. The process ends.

**Use / Trigger:**
[What triggers this: user action / batch schedule / policy event, or "N/A"]

### 3.1.5 Business Rules

| Rule Number           | Rule Description                     |
|-----------------------|--------------------------------------|
| BSD_[proj]_[gap]_SR01 | [Rule name — short title]            |
| BSD_[proj]_[gap]_SR01 | [Full rule detail — conditions + logic + formula + EMSG references] |
| BSD_[proj]_[gap]_SR02 | [Rule name]                          |
| BSD_[proj]_[gap]_SR02 | [Full rule detail]                   |

Rule content structure (apply inside each rule detail cell):

> **BSD Business Language — 7 Writing Patterns**  
> Full reference: `references/bsd-patterns.md`  
> Agent 2 MUST read bsd-patterns.md before writing any business rules.

### 3.1.6 User Experience

**Menu Navigation:**
| First Level Menu | Second Level Menu | Third Level Menu |
|------------------|-------------------|------------------|
| Customer Service | Worklist          | [PS Item Name]   |
| Query            | Common Query      | [Query Name]     |
(or "N/A" for batch-only gaps)

**User Interface:**
[Figure N: Screen Name]
(or "N/A")

**Field Description:**
| Field Name | Existing or New | Field Type | Format (Input) | Field Size | Selection List Options | Default Value | Is Mandatory? | Read Only / Editable | Validation |
|------------|-----------------|------------|----------------|------------|------------------------|---------------|---------------|----------------------|------------|
| [name]     | New / Existing  | [type]     | [format]       | [(9,2)/NA] | [options or NA]        | [default/NA]  | Yes/No        | Editable/Read Only   | [rule or EMSG ref] |

Field Type options: Free Text / Dropdown list / Date / Option / Checkbox / Button / Hyperlink / Number
Format options: N/A / YYYY/MM/DD / DD/MM/YYYY / Number / (9,2) / (3,0)

### 3.1.7 Configuration Task
[Numbered list of Product Factory config steps, or "N/A"]

---

## 3.2 [Next Gap Name]
[Same subsections 3.2.1 through 3.2.7]

---

## 2.5 Non-Functional Requirements

> **Required for all Dev Gap features. For Config Gap features, write "N/A — no performance/concurrency requirements."**

| Category | Requirement | Acceptance Criteria |
|----------|-----------|-------------------|
| **Concurrency** | [e.g., Circuit breaker must handle ≤100 concurrent requests per policy per day] | Load test with 100 simultaneous users on same policy |
| **Performance** | [e.g., NAV recalculation must complete within X seconds] | Response time < Xs at P95 under load |
| **Scalability** | [e.g., Supports up to N policies per batch run] | Batch processes N policies within SLA window |
| **Monitoring / Logging** | [e.g., RecalcCounter must be logged with timestamp and user ID] | Audit log shows RecalcCounter increment for every trigger |
| **Error Handling** | [e.g., If recalc fails, rollback transaction and emit EMSG-VUL-PS-003-XX] | Negative test passes |
| **Data Retention** | [e.g., Historical recalc records retained for 7 years] | Compliance audit confirmed |

---

## 4 Data Dictionary

> **Required for all Dev Gap features.** If all fields are existing InsureMO fields, write "N/A — no new fields introduced."

| Field / Variable Name | Data Type | Precision / Format | Persisted? (Table.Column) | New or Existing | Source / Notes |
|-----------------------|-----------|-------------------|---------------------------|-----------------|----------------|
| [PFV_snapshot] | Numeric | (18,6) | [FundValueSnapshots.PFV] | New | Calculated at T_submission |
| [RecalcCounter_Today] | Integer | — | [PolicyFlags.RecalcCnt] | New | Reset daily at batch |
| [CachedLimit_Today] | Numeric | (18,6) | [PolicyFlags.CachedFWL] | New | Updated on each recalc |
| [ExcessAmount] | Numeric | (18,6) | [WithdrawalTx.ExcessAmt] | New | = Requested − FreeWithdrawalLimit_used |

**Persistence rules:**
- All new fields must be added to the **Change Data Capture (CDC)** log for audit trail
- New database columns must be documented in the **Data Migration section** of Agent 9's output
- Agent 6 must update Product Factory schema documentation for any new CFG entries

---

## Sign-off Form

| Name | Department and Role | Signature | Sign-off Date |
|------|---------------------|-----------|---------------|
| | | | |

---

# Appendix A: Referenced BSDs
| BSD File Name | BSD Title | Description |
|---------------|-----------|-------------|

# Appendix B: Error & Warning Messages
| Error/Warning Code   | Screen Name | Description |
|----------------------|-------------|-------------|
| EMSG_[proj]_[gap]_001 | [screen] | [exact message text] |
| EMSG_[proj]_[gap]_002 | [screen] | [exact message text] |
```

---

## Tech Spec Template (Agent 4 output)

```markdown
# Tech Spec: [Feature Name]
[Standard document header]
Verification Status: ⏳ Pending / ✅ Machine-verified YYYY-MM-DD

## 1. Requirement Traceability
| Spec Item   | Source BSD Rule         | BSD User Story | Assumptions Applied |
|-------------|-------------------------|----------------|---------------------|
| [SPEC-001]  | BSD_[proj]_[gap]_SR[NN] | US-01 / AC-001 | A01, A02            |

## 2. Variable Registry
| Variable    | Type    | Range      | Source                    | Default |
|-------------|---------|------------|---------------------------|---------|
| [VAR_NAME]  | Integer | [range]    | [Product Factory / Input] | [value] |

## 3. Formula Definition
[Pseudocode — input → intermediates → output → edge case handling]

## 4. Verification Result
[Python code]
✅ All N tests passed (YYYY-MM-DD)
(or ⛔ FAILED — pending fix)

## 5. API Schema
[JSON Schema: Request / Response / Error with validation_errors array]

## 6. UI Trigger Specification
| Field ID | Trigger Event | Behaviour on Incomplete Data | State Transition |
|----------|---------------|------------------------------|------------------|

## 7. Test Matrix
| # | Test Type | Inputs | Expected Output | Formula Trace | BSD Rule Ref | AC Ref |
|---|-----------|--------|-----------------|---------------|--------------|--------|

## 8. Developer Checklist
- [ ] All SPEC items traced to BSD rule number
- [ ] Formula implemented exactly as specified
- [ ] All variables sourced from config (no hardcoding)
- [ ] All N test cases pass (machine-verified ✅)
- [ ] Calculated fields are read-only in UI
- [ ] All trigger events wired (including incomplete-data case)
- [ ] Error messages match Appendix B text exactly (no paraphrasing)
- [ ] Audit trail logged to policy database
```

---

## Product Profile Template (Agent 5 output)

```markdown
# Product Profile: [Product Name]
[Standard document header]

## Product Identity Card
Product Name:           [as stated in spec]
Product Code:           [if stated]
Product Type:           [Term / Endowment / Whole Life / UL / ILP / Medical / PA / CI / Takaful]
Sub-type:               [Participating / Non-Participating / Unit-Linked]
Target Market(s):       [MY / SG / TH / PH / ID]
Target Currency:        [MYR / SGD / USD / THB / PHP / IDR]
Distribution Channel:   [Tied Agent / Broker / Bancassurance / Direct / Online]
Takaful Flag:           [Yes / No / NOT STATED]
Spec Completeness:      [Complete / Partial — list missing sections if Partial]

## Dimension 1: Coverage & Benefits
[Benefit table: trigger / formula / exclusions per benefit]

## Dimension 2: Eligibility & UW Parameters
[Issue age, max age, ANB vs ALB flag, NML, BMI, occupation classes]

## Dimension 3: Premium Structure
[Payment term, frequency, modal factors, rate table presence, APL]

## Dimension 4: Rider Structure
[Per rider: attachment rule, term rule, benefit formula, standalone flag]
INVARIANT CHECK: Rider_Term ≤ Base_Policy_Term — [STATED / NOT STATED → flag]

## Dimension 5: Policy Values & Exit Scenarios
[SV, CSV, loan, reinstatement, free-look, paid-up]

## Dimension 6: Configurable Parameters (Product Factory Candidates)
| Param ID | Parameter Name | Value in Spec | Type | Notes |
|----------|----------------|---------------|------|-------|

## Dimension 7: Regulatory & Compliance Markers
| Market | Regulation Referenced | Requirement Summary | Verification Needed? |
|--------|-----------------------|---------------------|----------------------|

## Formula Inventory
### FORMULA-001: [Formula Name]
Source:      [Page / Section]
Original:    "[Exact quote]"
Structured:  result = f(var1, var2)
Variables:   var1 = [def], var2 = [def]
Edge cases stated:   [list or "None stated"]
Edge cases missing:  [list — flag for Agent 1]

## UNKNOWN Register
| UNKNOWN-ID | Section | Issue | Priority | Recommended Action |
|------------|---------|-------|----------|--------------------|
| UNKNOWN-001 | [dim] | [issue] | High / Medium / Low | [action] |

## Product Profile Summary
DIMENSIONS EXTRACTED: [N]/7
FORMULAS FOUND:        [N]
CONFIGURABLE PARAMS:   [N]
UNKNOWNS FLAGGED:      [N] — [X] High / [Y] Medium / [Z] Low

RECOMMENDED NEXT STEP:
→ If UNKNOWN High = 0: Proceed to Agent 1 Gap Analysis
→ If UNKNOWN High > 0: Resolve listed items first
```

---

## Configuration Runbook Template (Agent 6 output)

```markdown
# Configuration Runbook: [Product Name] — [Market]
[Standard document header]

## Scope
Total Config Gap items: [N]
Product Factory modules: [list]
Markets: [list]
Rate tables required: [N]

## Configuration Sequence
[Phase 1–6 dependency map with CHG-IDs assigned to each phase]

## CFG-001: [Configuration Item Name]
Gap Source: [F-NNN]
Phase: [1–6]
Module: Product Factory → [Module] → [Sub-section]

Prerequisite Check:
  ✅ [Prerequisite 1]

Configuration Steps:
Step 1: [action]
Step 2: [action — Field name + valid range + default]

Market-Specific Values: [table if values differ]
INVARIANT: [if rider config]
Verification: [test quote steps]
Common Errors: [list]

## Open Items
| ID | Item | Blocked By | Owner |
|----|------|------------|-------|

## Summary
[Config item count by phase + RECOMMENDED NEXT STEP]
```

---

## Impact Matrix Template (Agent 7 output)

```markdown
# Impact Matrix: [Change Reference]
[Standard document header]

## Change Inventory
| Change ID | Change Description | Change Type | Source |
|-----------|-------------------|-------------|--------|

## Module Impact Matrix
| Module           | CHG-001 | CHG-002 | Overall |
|------------------|---------|---------|---------|
| Product Factory  | 🔴      | ⚪      | Direct  |
| New Business     | 🟡      | 🔴      | Direct  |
[...all 12 modules]

## Per-Module Detailed Impact
[One section per 🔴 Direct module — what changes + test scenarios + downstream trigger]

## Impact Cascade Map
[One cascade per CHG-ID showing flow through modules]

## Effort & Scope Sizing
| Module | Effort Type | Estimated Days | Assumptions |
|--------|-------------|----------------|-------------|
| TOTAL  |             | [N days]       |             |

## Summary
Changes: [N] | 🔴 Direct: [N modules] | 🟡 Indirect: [N modules]
Total effort: [N days] (excl. UAT + deployment)
Key risks: [table]
RECOMMENDED NEXT STEPS: [list]
```

---

---

## Appendix C: BSD v9.0 Format — Full vs Lite Selection Guide (v3.1)

### Decision Tree

```
START: What type of gap is this?
│
├─ DEV GAP
│   ├─ Has formula (Pattern 4)?        → Full (mandatory Example Table)
│   ├─ Has feedback loop (⚡ ripple)?  → Full
│   ├─ Touches ≥ 3 modules?            → Full
│   ├─ Has OPEN UNKNOWNs blocking dev? → Full
│   └─ NONE of above + ≤ 2 Dev items + no cross-module?
│       → Consider: can it be deferred to config?
│           If YES → treat as Config Gap → Lite
│           If NO  → Full (minimal Dev item still needs SR + Assumptions)
│
├─ CONFIG GAP
│   └─ ALL of (pure config, no formula, no ripple, no compliance, no OPEN UNKNOWNs)?
│       ├─ YES → Lite
│       └─ NO  → Full (Config Gap with complexity)
│
└─ MIXED (some Dev items + some Config items)
    → Write SEPARATE BSDs: one Full (Dev) + one Lite (Config)
    → Never combine in one Lite BSD
```

### Dev Gap → Full (always)
Use v9.0 **Full** if ANY of:
| Condition | Why Full Required |
|-----------|-------------------|
| Contains a formula (Pattern 4) | Example Table is mandatory for formula verification |
| Has a feedback loop (⚡ RIPPLE CHAIN) | Ripple propagation must be documented in Ch.2 |
| Touches ≥ 3 InsureMO modules | Cross-module impact must be traced in Ch.2 §2.3 |
| Has OPEN UNKNOWNs blocking implementation | Cannot defer — must be resolved before dev starts |
| Has compliance requirements (MAS/BNM/HKIA) | Regulatory section Ch.2 §2.2 required |
| Requires new data elements (not in existing tables) | Ch.6 Data Dictionary required |
| Has non-functional requirements (performance/concurrency) | Ch.7 NFR required |

### Config Gap → Lite (default)
Use v9.0 **Lite** if ALL of:
| Condition | Interpretation |
|-----------|----------------|
| Pure Product Factory configuration | No new screens, CS items, or batch processes |
| No formula / calculation logic | No Pattern 4 rules |
| No cross-module ripple | Change does not trigger downstream modules |
| No compliance sensitivity | No MAS/BNM/HKIA regulatory touchpoints |
| All parameters confirmed (no OPEN UNKNOWNs) | No missing rate tables, attachment conditions |

### Config Gap → Upgrade to Full if ANY of:
| Condition | Action |
|-----------|--------|
| Config involves new computed field derived from formula | Add Example Table (Ch.3 §3.X.6) |
| Config triggers changes in ≥ 2 other modules | Add Ch.2 §2.3 Ripple + Full format |
| Config has OPEN UNKNOWN about rate/table | Keep Lite but note UNKNOWN in Appendix B |
| Config is rate-table driven with boundary conditions | Consider Full with Example Table |

### Mixed Project Rule
> **One BSD per gap classification. Do NOT combine Dev and Config in one Lite BSD.**
> If a feature has 3 Dev Gaps and 2 Config Gaps → write TWO BSDs:
> - BSD_[proj]_[feature]_Full_v9.0 (for Dev Gaps)
> - BSD_[proj]_[feature]_Lite_v9.0 (for Config Gaps)
> Cross-reference each other in Appendix A.

### "Too Small for Full?" Decision
| Situation | Decision |
|-----------|----------|
| Single Dev Gap, no formula, 1 module, no unknowns | Still use Full — SR + Assumptions + NFR are the minimum viable BSD |
| Dev Gap with all parameters configurable (no code change) | Reclassify as Config Gap → Lite |
| Dev Gap that is essentially a configuration workaround | Still Dev — workaround logic needs documenting |

### Quick Reference Card

| | Full (Dev) | Lite (Config) |
|---|---|---|
| Formula / Example Table | ✅ Required | ❌ Not needed |
| Ch.6 Data Dictionary | ✅ Required | ❌ Not needed |
| Ch.7 NFR | ✅ Required | ❌ Not needed |
| Ch.2 Ripple Map | ✅ If ≥3 modules | ❌ Not needed |
| Assumptions Register | ✅ Required | ⚠️ Only if needed |
| Open Questions | ✅ Required | ⚠️ Only if blocking |
| Typical length | 10–20 pages | 2–4 pages |
| Sign-off required | All stakeholders | Config approver only |

---

### BSD v9.0 Full Format (Dev Gaps)

```
# BSD_{Project}_{Feature}_v9.0

[Standard Header — see above]

# Chapter 1: Introduction
## 1.1 Overview         [2-3 sentences: business context + what changes]
## 1.2 End Users        [Stakeholder table — per module convention]
## 1.3 Glossary         [New terms only; do NOT redefine common terms]
## 1.4 Assumption Register [Structured: ID / Assumption / Source / Status / Impact]
## 1.5 Open Questions   [Owner / SLA / Blocking tag]

# Chapter 2: Requirements
## 2.1 Gaps Covered     [Gap → BSD Chapter mapping]
## 2.2 Compliance Requirements (Agent 3)  [Agent 3 output — C-ID table]
## 2.3 Ripple Propagation Chain (Agent 7) [Ripple map — ⚡FEEDBACK LOOP MARKER]

# Chapter 3: Business Solutions
## 3.X [Gap Name]
### 3.X.1 Solution Summary   [To enhance the following: numbered list]
### 3.X.2 Solution Assumptions [A-table: ID / Assumption / Source / Status]
### 3.X.3 Business Process Flow Diagram  [N/A if described in Normal Flow]
### 3.X.4 Function Description   [Preconditions / Normal Flow / Use/Trigger]
### 3.X.5 Business Rules
  Rule Number: BSD_..._SR01
  Rule Title: [Short Title]
  STEP 1 — Business Sentence: [What the system does, in business language]
  STEP 2 — Precise Formula: [Formula block — use ONLY for Pattern 4]
  Constants: [Every magic number → source citation]
  Rule Conditions:
    a. ✓ If [condition]: [then outcome]
    b. ✓ If [condition]: [then outcome]
  INVARIANT: [The one rule that must always hold — state explicitly]
    → Enforced at: [Screen / CS Item / Batch]
    → If violated: [What breaks]

### 3.X.6 Example Table
  > Pattern 7 — Example Table (mandatory for Pattern 4 rules)
  > Format: | Case | Input A | Input B | Expected Output | UAT Scenario | Notes |
  > Each row = one boundary condition scenario
  [BC-01 through BC-N: numeric, not alphabetic]

### 3.X.7 User Experience
  [Menu Navigation / Field Description — N/A if batch-only]
### 3.X.8 Configuration Task   [N/A for Dev Gaps]

# Chapter 6: Data Dictionary (G6)

> **Required for all Dev Gap features.** Documents all new or modified data elements introduced by the development. Config Gaps: write "N/A — no new data elements" unless Product Factory introduces new computed fields.

## 6.1 New Data Elements

| Field ID | Field Name | Table Name | Field Type | Length | Description | Source | Default Value | Validation Rules | Related BSD Rule |
|----------|-----------|-----------|-----------|--------|-------------|--------|--------------|-----------------|-----------------|
| DE-001 | [FieldName] | [DB_TABLE] | [VARCHAR/INT/DECIMAL/DATE] | [(n,m)] | [Business description] | [User Input / System Calculated / Config] | [value or N/A] | [rule or N/A] | BSD_..._SRnn |

## 6.2 Modified Data Elements (Existing Fields)

| Field ID | Field Name | Table Name | Original Definition | New Definition | Change Reason | Related BSD Rule |
|----------|-----------|-----------|--------------------|--------------------|---------------|-----------------|
| MD-001 | [FieldName] | [DB_TABLE] | [original] | [modified] | [reason] | BSD_..._SRnn |

## 6.3 Data Element Lifecycle

| Field ID | Created By | Created At | Modified By | Modified At | Retention Period | Archival Rule |
|----------|-----------|-----------|------------|------------|-----------------|---------------|
| DE-001 | [CS Item / Batch / API] | [Policy Inception] | [Trigger event] | [Date] | [X years / Policy Life] | [Rule] |

## 6.4 Integration Points

| Field ID | External System | Integration Method | Data Direction | Frequency |
|----------|----------------|-------------------|---------------|-----------|
| DE-001 | [Custodian / RI / AM] | [API / Batch File / DB Link] | [Inbound / Outbound] | [Real-time / Daily / Monthly] |

---

# Chapter 7: Non-Functional Requirements (G7)

> **Required for all Dev Gap features.** Defines performance, concurrency, scalability, monitoring, and data retention requirements.
> For Config Gap features: write "N/A — no performance/concurrency requirements" unless explicitly required by the change.

## 7.1 Performance Requirements

| Requirement ID | Requirement | Acceptance Criteria | Test Method |
|----------------|-----------|---------------------|-------------|
| PERF-001 | [e.g., NAV recalculation must complete within X seconds per policy] | Response time < Xs at P95 under [N] concurrent policies | Load test with [N] simultaneous requests |
| PERF-002 | [Batch processing: N policies must complete within SLA window] | Batch processes N policies within [X] hour(s) | Batch run with N policies |

## 7.2 Concurrency Requirements

| Requirement ID | Requirement | Acceptance Criteria | Test Method |
|----------------|-----------|---------------------|-------------|
| CONC-001 | [e.g., System must handle ≤100 concurrent TI claims per policy per day] | Load test with 100 simultaneous users on same policy — no data corruption | Concurrent load test |
| CONC-002 | [e.g., Circuit breaker must prevent cascade failures across modules] | [Criteria] | Chaos engineering test |

## 7.3 Scalability Requirements

| Requirement ID | Requirement | Acceptance Criteria | Test Method |
|----------------|-----------|---------------------|-------------|
| SCALE-001 | [e.g., System supports up to N policies per batch run without degradation] | Batch processes N policies within SLA window | Scale test: N → 1.5N → 2N |

## 7.4 Monitoring and Logging Requirements

| Requirement ID | Requirement | Logged Data | Retention | Alert Threshold |
|----------------|-----------|-------------|-----------|----------------|
| MON-001 | [e.g., RecalcCounter must be logged with timestamp, user ID, and policy ID] | [Field changes, user actions, system events] | [X days / 7 years] | [Threshold] |
| MON-002 | [e.g., All claim adjudication events must be auditable] | [Event type, timestamp, actor, result] | [X years] | [Criteria] |

## 7.5 Error Handling Requirements

| Requirement ID | Requirement | Expected Behavior | Fallback Action |
|----------------|-----------|-------------------|----------------|
| ERR-001 | [e.g., If recalc fails, rollback transaction and emit EMSG-VUL-PS-003-XX] | [Behavior] | [Fallback] | Negative test passes |
| ERR-002 | [e.g., External system timeout must not block policy transaction] | [Behavior] | [Circuit breaker pattern] | |

## 7.6 Data Retention Requirements

| Requirement ID | Requirement | Retention Period | Archival Trigger | Deletion Method |
|----------------|-----------|----------------|-----------------|----------------|
| RET-001 | [e.g., Historical recalc records retained for 7 years] | [X years] | [Trigger] | [Method] |
| RET-002 | [e.g., Audit trail never deleted — compliance requirement] | [Permanent / X years] | [Never] | [N/A — permanent] |

---

# Appendix A: Referenced Documents
# Appendix B: Error and Warning Messages   [Complete message text — not just codes]
# Appendix C: Compliance Summary          [C-ID table from Agent 3]

---

## Pre-Output Checkpoint (Agent 2 Self-Verification)

> **Agent 2 must complete this checkpoint BEFORE finalizing the BSD output.**
> This is a self-check, not a sign-off. Fill in the verification column as you write.
>
> **Gate Context:** Pre-work quality gates (GATE-A/B/C) are defined in `agents/agent2-bsd.md` Step 0.5. The checkpoint below is the **output gate** — run after the BSD draft is complete. GATE-A (Q01–Q04, Q05, Q14, Q17) are P0 blockers; GATE-B items (Q11, Q12) are Implementation Gates, not BA sign-off gates.

### Mode B Note — TBD Fields
> If this BSD was produced via Mode B (natural language input), all fields marked [TBD] by the Pre-Processor MUST appear in Ch.1 §1.5 Open Questions with owner/SLA. C11 above tracks remaining TBD count. BSD cannot be signed off if TBD count > 0.

### Step 1 — Completeness Sweep

| # | Check | Method | Result |
|---|-------|--------|--------|
| C1 | Every Gap ID in Gap Matrix → has a corresponding BSD rule | Cross-reference Gap Matrix file | ☐ All covered / ☐ Gap(s) missing: ___ |
| C2 | Every BSD rule → traces to a Gap ID | Check Ch.2 §2.1 table | ☐ All traced / ☐ Orphan rules: ___ |
| C3 | Every Pattern 4 rule → has Example Table | Check Ch.3 §3.X.6 | ☐ All complete / ☐ Missing table: ___ |
| C4 | Every EMSG code referenced in rules → listed in Appendix B | Search rule text for "EMSG" | ☐ All listed / ☐ Missing: ___ |
| C5 | Every Assumption in §1.4 → has owner and due date | Check A-table | ☐ All assigned / ☐ Missing: ___ |
| C6 | Every Open Question in §1.5 → has owner, SLA, blocking flag | Check OQ-table | ☐ All assigned / ☐ Missing: ___ |
| C7 | Every Dev Gap → has Limitation Source or Semantic Justification | Check Ch.3 §3.X.2 | ☐ All complete / ☐ Gap: ___ |
| C8 | R10-flagged items → R10_Flag = YES in Gap Matrix AND BSD notes | Cross-ref Gap Matrix | ☐ Verified / ☐ Not flagged |
| C9 | Ch.6 (Data Dictionary) → all new fields have DE-ID | Check Ch.6 table | ☐ All assigned / ☐ Missing: ___ |
| C10 | Ch.7 (NFR) → all Dev Gaps have NFR entries | Check Ch.7 table | ☐ All complete / ☐ Missing: ___ |
| C11 | Mode B TBD count = 0 | Count [TBD] fields in Mode B Pre-Processor output. Any remaining TBD → BSD header must declare "KB verification status: Partial" and each TBD must appear as an Open Question in Ch.1 §1.5 with owner/SLA | ☐ 0 TBD / ☐ N remaining — cannot sign off until resolved |

### Step 2 — Anti-Pattern Check

| # | Check | Method | Result |
|---|-------|--------|--------|
| P1 | No bare formula in rule text | Search for "=" or "(" in rule cells without Step 1 business sentence | ☐ Clean / ☐ Found: ___ |
| P2 | No prose paragraphs in Business Rules section | Rules use numbered/table format | ☐ Clean / ☐ Found prose in: ___ |
| P3 | No TBD/TODO/___ in any rule | Search for "TBD", "TODO", "___" | ☐ Clean / ☐ Found: ___ |
| P4 | No placeholder text in Example Tables | All BC table cells filled | ☐ Clean / ☐ Empty cells in: ___ |
| P5 | All cross-references valid (no "see X" where X doesn't exist) | Verify every "see Ch.X" reference | ☐ Clean / ☐ Broken ref: ___ |
| P6 | All section numbers match content (Ch.3 §3.X.6 = Example Table) | Verify structure | ☐ Clean / ☐ Mismatch: ___ |
| P7 | No Config Gaps included in this Full BSD | Check Gap IDs in Ch.2 | ☐ Clean / ☐ Config Gaps found: ___ |

### Step 3 — Final Confirmation

> **Before marking F6 = Ready**, confirm GATE-A P0 results (Q01/Q02/Q03/Q04/Q05/Q14/Q17):
> - All P0 = YES → proceed to F6
> - Any P0 = NO → stop, resolve in agent2-bsd.md Step 0.5 GATE-A first



| # | Confirmation | Agent 2 Declaration |
|---|-------------|---------------------|
| F1 | I have read the corresponding ps-*.md files for every Gap covered | ☐ Confirmed |
| F2 | I have read the relevant V3 UG files for every Gap covered | ☐ Confirmed |
| F3 | Every ps-* citation in the BSD refers to the correct section number | ☐ Confirmed |
| F4 | This BSD uses Full format correctly (no Config Gap shortcuts) | ☐ Confirmed |
| F5 | R10 scanner was run on the source spec — results considered | ☐ Confirmed |
| F6 | This BSD is ready for review — no blockers remaining | ☐ Ready / ☐ Blockers: ___ (include C11 TBD count if > 0) |

**Checkpoint Result:**
```
☐ ALL CLEAR — BSD ready for review
☐ ISSUES FOUND — resolve items marked ☐ before output
```

---

## Sign-off Form

> **Complete Pre-Output Checkpoint above before proceeding to sign-off.**

### Sign-off

| Role | Name | Signature | Date |
|------|------|----------|------|
| Business Analyst | | | |
| Underwriter / Compliance | | | |
| IT / Developer | | | |
| Product Owner | | | |
```

---

### BSD v9.0 Lite Format (Config Gaps)

```
# BSD_{Project}_{Feature}_Lite_v9.0

[Standard Header — same as Full]
Version:       0.1
Status:        Draft
Classification: CONFIG GAP — Lite Format

---

# Chapter 1: Introduction

## 1.1 Overview
[1 paragraph: what product and what is being configured. Include product name, market, and distribution channel.]

## 1.2 Scope

**In Scope:**
- [Product: e.g., HSBC Life Privilege Wealth VUL — SG market]
- [Gaps covered: CF-001 through CF-NN — list Gap IDs from Gap Matrix]
- [Configuration modules: Product Factory → ILP Rules → X, Y, Z]

**Out of Scope:**
- [Dev Gaps — these go in a separate Full BSD]
- [Features not listed in Gap Matrix]
- [Other markets]

## 1.3 Product Factory Configuration Paths

> **This section is mandatory for Lite BSD.** Lists all Product Factory navigation paths for this configuration.

| Config ID | InsureMO Module | Navigation Path | KB Reference |
|-----------|----------------|-----------------|---------------|
| CF-001 | Product Factory → ILP Rules → Premium Charge | [exact PF screen path] | ps-product-factory.md S.XX |
| CF-002 | Product Factory → ILP Rules → Min Premium | [exact PF screen path] | ps-product-factory.md S.XX |
| CF-003 | CS Config → Cancellation Rules → Free-Look | [exact CS screen path] | ps-customer-service.md S.XX |

---

# Chapter 2: Configuration Requirements

## 2.1 Gaps Covered

| Gap ID | Feature | Config Item | Priority | Config Status |
|--------|---------|------------|----------|--------------|
| VUL_PREM_001 | Min Initial Premium USD 200K | CF-001 | P2 | Confirmed |
| VUL_PREM_002 | Min Additional Premium USD 10K | CF-002 | P3 | Confirmed |

## 2.2 Configuration Sequence

> **MANDATORY: Follow this sequence to respect dependencies between config items.**
> If a config item has prerequisites, it must be configured AFTER its prerequisites.

| Step | Config Item | Action | Prerequisite |
|------|------------|--------|-------------|
| 1 | CF-001 | Navigate to [Screen] → Set [Field] = [Value] | None |
| 2 | CF-002 | Navigate to [Screen] → Set [Field] = [Value] | CF-001 must be saved first |
| 3 | CF-003 | Navigate to [Screen] → Set [Field] = [Value] | None |

**Navigation Template (copy for each config item):**
```
Screen:    Product Factory → ILP Rules → [Sub-section]
Field:     [Exact field name as shown in InsureMO]
Value:     [Value from spec — include units, e.g., USD 200,000]
Valid Range: [Min / Max if applicable]
Default:   [What is the InsureMO default before config]
KB Ref:    ps-[module].md S.XX — confirms configurable, no code change
```

## 2.3 Configuration Detail

### CF-001: [Config Item Name]
| Field | Value | Valid Range | Default | KB Ref |
|-------|-------|------------|---------|--------|
| [Field 1] | [Value from spec] | [Min–Max or list] | [InsureMO default] | ps-xxx.md S.XX |
| [Field 2] | [Value from spec] | [Min–Max or list] | [InsureMO default] | ps-xxx.md S.XX |

**Config Notes:**
- [Any special instructions, warnings, or dependencies]
- [e.g., "This field is disabled until CF-002 is saved"]

### CF-002: [Config Item Name]
[Same structure as CF-001]

---

## 2.4 Configuration Summary Table

| Config ID | Gap Source | Product Factory Module | Field Name | Configured Value | KB Source |
|-----------|-----------|----------------------|------------|-----------------|-----------|
| CF-001 | VUL_PREM_001 | Product Factory → ILP Rules → Min Premium | MinInitialPremium | USD 200,000 | ps-product-factory.md S.XX |
| CF-002 | VUL_PREM_002 | Product Factory → ILP Rules → Min Top-up | MinAdditionalPremium | USD 10,000 | ps-product-factory.md S.XX |
| CF-003 | VUL_PS_009 | CS Config → Cancellation Rules → Free-Look Period | FreeLookDays | 14 | ps-customer-service.md S.394 |

---

## 2.5 Verification Test Scenarios

| Scenario ID | Test Objective | Pre-condition | Test Input | Expected Result | Pass/Fail |
|-------------|--------------|--------------|-----------|-----------------|----------|
| TS-01 | Verify Min Initial Premium enforcement | NB Data Entry screen | IP = USD 199,999 | System rejects with error | ☐ |
| TS-02 | Verify Min Initial Premium accepted | NB Data Entry screen | IP = USD 200,000 | System accepts | ☐ |
| TS-03 | Verify Min Additional Premium enforcement | In-force policy | AP = USD 9,999 | System rejects with error | ☐ |
| TS-04 | Verify Free-Look period | Policy issued | Cancellation within 14 days | Full premium refund | ☐ |
| TS-05 | Verify Free-Look expiry | Policy issued | Cancellation on Day 15 | Free-Look expired | ☐ |

---

## 2.6 Configuration Dependencies

| Config ID | Depends On | Dependency Type | Notes |
|-----------|----------|----------------|-------|
| CF-002 | CF-001 | Must be saved after | Both in ILP Rules module |
| CF-003 | None | — | Independent CS Config |

---

# Appendix A: Referenced Documents

| Document | Title | Relevance |
|----------|-------|----------|
| [Gap Matrix file] | Gap Matrix for [Product] | Source of gap classifications |
| ps-product-factory.md | InsureMO Product Factory KB | Config path confirmation |
| ps-customer-service.md | InsureMO CS KB | Free-Look and CS config |

---

# Appendix B: Open Questions

| ID | Question | Owner | Due Date | Blocking? |
|----|----------|-------|----------|-----------|

[Delete this section if no open questions]

---

## Sign-off Form

| Role | Name | Signature | Date |
|------|------|----------|------|
| Business Analyst | | | |
| Config Approver | | | |
| Product Owner | | | |

### Config Gap Completeness Checklist (Lite)

> **All items must be verified before sign-off.**

| # | Completeness Item | Verification | Sign-off Required |
|---|------------------|-------------|-----------------|
| 1 | All Gap IDs from Gap Matrix are covered in §2.1 | | Config Approver |
| 2 | All config items have a Product Factory navigation path | | Config Approver |
| 3 | All config values match spec (exact numbers/strings) | | BA + Config |
| 4 | Config sequence respects dependencies (§2.6) | | Config Approver |
| 5 | Verification test scenarios cover boundary conditions | | Config Approver |
| 6 | No OPEN UNKNOWNs remain for this configuration | | BA |
| 7 | KB reference cited for every config item | | BA |
| 8 | No Dev Gaps included in this Lite BSD | | BA |

```

**Key differences — Full vs Lite:**

| Section | v9.0 Full (Dev) | v9.0 Lite (Config) |
|---------|----------------|-------------------|
| Chapter 1 | Full: End Users, Glossary, Assumptions, Open Questions | Lite: Overview, Scope, Assumptions (minimal) |
| Chapter 2 | Full: Compliance + Ripple chains | Lite: Config steps + summary table |
| Chapter 3 | Full: Preconditions, Normal Flow, SR01/02, INVARIANT, Example Table | Lite: Numbered config steps only |
| Example Table | Required (Pattern 4) | Not required (no formulas) |
| Appendix B | EMSG full text required | Open Questions only (if any) |
| Sign-off | All stakeholders | Config approver only |
| Typical length | 10-20 pages | 2-4 pages |

---

## Appendix D: Example Table — Standard Format (Pattern 7)

> **Every Pattern 4 rule MUST have an Example Table.**
> The format below is the ONLY accepted format. Do not invent column layouts.

**Rule for column design:**
- First columns = all inputs (ordered by what changes in the scenario)
- Last column = the output being calculated
- Last column = expected result
- UAT Scenario column = links to UAT test case (format: UAT-[GAPID]-[NN])
- Notes column = edge case explanation only

**Required columns for ALL Example Tables:**
```
| Case | [Input A] | [Input B] | [Input C] | [Expected Output] | UAT Scenario | Notes |
```

**Minimum rows:** 3
- At least 1 normal/happy-path case
- At least 1 boundary condition
- At least 1 error/rejection case

**Common mistake — wrong:**
```
| Example | Scenario | Result | Notes |    ← Scenario is prose, not an input column
```

**Correct:**
```
| Case | AccumulatedTI (USD) | ProposedTI (USD) | RemainingCapacity (USD) | TI_Benefit_Payable (USD) | UAT Scenario | Notes |
```

**UAT Scenario ID format:** `UAT-[GapID]-[NN]`
- Example: `UAT-BEN-003-01`
- NN is sequential: 01, 02, 03...
- Links directly to UAT test case ID in test management tool

---

## Rule Number Reference

```
BSD Rule:      BSD_[ProjectCode]_[GapNumber]_SR[NN]
               e.g. BSD_PS3_036_SR01

Error Message: EMSG_[ProjectCode]_[GapNumber]_[NN]
               e.g. EMSG_PS3_036_001

Gap Number:    [ProjectCode]_[SequentialNumber]
               e.g. PS3_036

SPEC Item:     SPEC-[NNN]
               e.g. SPEC-001

Config Item:   CFG-[NNN]
               e.g. CFG-001

Change ID:     CHG-[NNN]
               e.g. CHG-001

Unknown:       UNKNOWN-[NNN]
               e.g. UNKNOWN-001

Formula:       FORMULA-[NNN]
               e.g. FORMULA-001

Assumption:    A[NN]
               e.g. A01

User Story:    US-[NN]
               e.g. US-01

AC:            AC-[NN]
               e.g. AC-01
```
