# InsureMO Platform Guide — Underwriting (UW)
# Source: Underwriting User Guide V2022 (eBaoTech)
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb-full.md instead
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"how does Underwriting work in InsureMO"** — navigation paths, prerequisites, field behaviour, workflow config parameters, and business rules for the UW Workbench.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for a UW-related gap
- Agent 6 is generating a **Config Runbook** for UW items
- A BA needs to verify what **auto-UW rules** apply or what the **escalation chain** looks like

---

## Module Overview

```
Underwriting (UW) Workbench — Centralized, handles UW from:
│
├── New Business (NB)        ← Most common source
├── Customer Service (CS)    ← CS alterations requiring UW
├── Claim                    ← Claim-related UW review
└── LCA Reply                ← Consent update after conditional acceptance
```

The UW Workbench is **shared** across all source types. NB and CS UW operations are identical. Claim UW is lighter: review application info, input comments, submit.

---

## UW Workflow — Standard Sequence

```
Step 1: Auto-UW triggered after NB Verification Submit or CS Apply Change
  ├─► Auto-UW passes → Proposal accepted (no manual UW needed)
  └─► Auto-UW fails (issues raised) → Proposal routed to UW Worklist

Step 2: Retrieve UW Task (Underwriter opens task from worklist)

Step 3: Review UW Worksheet
  ├── Policy Information
  ├── Medical/Non-Medical Code Information
  ├── Risk Summary (aggregation, NB/Claim/CS history)
  ├── Letters
  ├── Life Survey
  ├── UW Comments History
  ├── UW Decision and Escalation History
  └── LCA

Step 4: Check and Close UW/Proposal Issues

Step 5: Make UW Decision (UW Decision tab)
  ├── Accepted / Postponed / Declined → applied to all products
  └── Conditionally Accepted → set per product; add loading, exclusion, condition, endorsement

Step 6: Underwriting Submit
  ├─► Within authority → UW complete; proposal routed per decision
  └─► Beyond authority → Escalated to senior underwriter
```

**Optional steps:**
- Generate letters for UW issues
- Request Medical Exam
- Create/Reverse Medical Billing
- Generate Ad Hoc Letter
- Print UW Worksheet (PDF)
- Back to Data Entry (send proposal back)

---

## Menu Navigation

| Action | Path |
|---|---|
| UW worklist | Underwriting > Work List |
| UW query | Underwriting > Query (read-only view) |
| Create medical billing | Underwriting > Medical Billing > Create Medical Billing |
| Reverse medical billing | Underwriting > Medical Billing > Reverse Medical Billing |
| Ad hoc letter generation | Underwriting > Ad Hoc Letter Generation |

---

## UW Task Retrieval

### Prerequisites
- Proposal status = **Waiting for Underwriting** or **Underwriting in Progress**
- User has access authority for the case level

### Navigation
Underwriting > Work List → set search criteria → Search → click hyperlink

### Search Criteria

| Field | Description |
|---|---|
| Underwriting Type | New Business / Claim / Customer Service (multi-select) |
| Policy No. | Direct lookup |
| Proposal No. | Direct lookup |
| Customer Name | Policy holder name |
| Registration Period | UW task creation date range |
| Task Status | UW task status dropdown |
| Sub Task Status | UW sub-task status dropdown |
| TAT (Days) | Current date − Application registration date |

### Search Result Columns
Proposal No., Policy No., Underwriting Type, Application Branch, Task Status, Sub Task Status, TAT (Days), Operated By, Registration Date

---

## UW Main Page

The UW main page is composed of:
- **Application Information** section (top) — read-only summary
- Three working tabs: **UW Worksheet** | **UW/Proposal Issues** | **UW Decision**
- Bottom bar: COMMENT | SAVE & EXIT | BACK TO DATA ENTRY | SUBMIT

### Application Information Section

| Field | Description |
|---|---|
| Underwriting Type | Source: New Business / Customer Service / Claim |
| Proposal No. | Proposal identifier |
| UW Application Date | Date UW task was created |
| Pending Reason | Current pending reason (e.g. New for Underwriting, Escalated to next level) |
| Application Information (hyperlink) | Opens full NB query page for the policy |
| Image (hyperlink) | Opens DMS for policy/client images (when integrated) |

### Comment Feature
- Available on all three tabs via COMMENT button
- User chooses **Sensitive** or **Public**
- History comments visible in Comment History and in UW Comments History section of Worksheet
- For claim cases with multiple policies: submitting UW for one policy **auto-submits** UW for other policies in the same claim case

---

## UW Worksheet

Provides all risk estimation dimensions in one place. Underwriter can complete all work without switching screens.

### Sub-section: Policy Information

Displays:
- Proposal Sign Date, Sales Channel, Producing Agent, Producing Agent Reporting Manager, Currency
- Product table: Product, Product Type, Life Assured, Age, Occupation Class, Coverage Term, Premium Term, Payment Frequency, SA/Unit/Level, Annual Premium, Total Annual Premium
- Party table: Party Role, Customer Name, ID Type/Number, DOB, Gender, Relationship with PH, Annual Income, Occupation, Smoker Status, Risk Indicator, Medical Report (VIEW link), Declaration (VIEW link), Fraud, Fraud On Policies, Bankruptcy Status

**Actions:**

| Action | Result |
|---|---|
| Click customer name hyperlink | Opens detailed customer info in core system (no separate login) |
| Click VIEW under Medical Report | Shows all medical reports (image or OCR + image) |
| Click VIEW under Declaration | Shows declaration content (image or input + image) |

---

### Sub-section: Medical/Non-Medical Code Information

- Displays existing customer LIA codes with description
- Highlights high-risk items or conditions
- Shown per Life Assured
- Fields: Policy No., Code, Code Category, LIA Code Type, Medical/Non-Medical Code Description

**Add/Edit Medical/Non-Medical Code:**
- Click Medical/Non-Medical Code Information hyperlink on UW Decision tab
- Shows: Life Assured Info (Name, DOB, Gender, ID Type, ID No.) + existing codes table
- Click ADD A NEW MEDICAL/NON-MEDICAL CODE INFORMATION to add; DELETE to remove

---

### Sub-section: Risk Summary

Displays risk aggregation and history across all life assureds.

**Risk Aggregation table:**

| Column | Description |
|---|---|
| Risk Type | Death / TPD / etc. |
| Applying | Risk SA on current proposal |
| Inforce | Risk SA on inforced policies |
| Terminated | Risk SA on terminated policies |
| Declined/Postponed | Risk SA on declined/postponed policies |
| USAR | Total risk inforce in current year |
| TSAR | Total risk sum assured |

**Total Premium summary:** Applying, Inforce, Terminate, Declined/Postponed, Total Annual Premium, Total Single Premium

**NB Application History:** All NB policies for the same LA — Policy No., Product Code, Product Type, NB UW Decision, Commencement Date, Policy Status, Premium Status, Payment Frequency, SA/Unit/Level, Annual Premium, Auto UW Indicator, Policy Currency

**Claim History:** Claim No., Policy No., Product Code, Claim Type, Event Date, Claim Nature, Diagnosis, Claim Status, Claim Decision, Claim Amount, Settle Date

**Risk Related CS History:** CS No., Policy No., Product Code, Product Type, CS Item, CS Application Date, CS Status, Auto UW Indicator, UW Decision, UW Complete Date, Underwriter

> **Note:** All history records shown for the same LA regardless of whether those policies have UW records. Field values only display when system is integrated with corresponding third-party system.

**Hyperlink Actions:**

| Hyperlink | Result |
|---|---|
| Policy No. / Claim No. / CS No. | Pop-up: common/claim/CS query |
| NB/CS UW Decision | Pop-up: UW query for that NB/CS change |

---

### Sub-section: Letters

Lists all generated letters related to the current case.

| Column | Description |
|---|---|
| Document Name | Letter name |
| Document No. | Hyperlink → PDF of letter |
| Generate Date | Date generated |
| Generate By | User who generated |
| Replied | Reply info; hyperlink shows replied image |
| Update Date | Last update |
| Update By | Last updater |
| Document Status | To be submitted / To be printed / To be published / Printed / Published / Replied |

---

### Sub-section: Life Survey

- Shows survey object, survey content, requested date, requested by, survey report (VIEW hyperlink), updated date, updated by, survey status
- Field values display only when integrated with third-party investigation system

---

### Sub-section: UW Comments History

- All UW comments for current case
- Shows user, organization, and comment date

---

### Sub-section: UW Decision and Escalation History

- All previously made UW decisions and escalation records
- Shows decision-maker, organization, and operation date

---

### Sub-section: LCA (Letter of Conditional Acceptance)

| Column | Description |
|---|---|
| Document Name | LCA document name |
| Document No. | Hyperlink → PDF |
| Generate Date / Generate By | Generation info |
| Replied / Update Date / Update By | Update info |
| Document Status | To be submitted → To be printed/published → Printed/Published → Replied |
| Consent Given Indicator | Agree / Reject (set by processor after LCA returned) |
| Consent Given Date | Auto-set when Consent Given Indicator updated |

**Update rules:**
- Consent Given Indicator must be selected before clicking UPDATE
- Clicking UPDATE: document status → Replied; Consent Given Date → current system date
- DELETE only available when status = To be submitted

---

### Print Worksheet

- Button at bottom of UW Worksheet
- Generates PDF of entire worksheet
- Can be printed or emailed as attachment

---

## UW / Proposal Issues Tab

### Check UW Issues

**Prerequisite:** UW task retrieved and open

**Operations:**

| Purpose | Operation |
|---|---|
| Check UW Issues | Review listed issues; select + click Letter Generate to send query letter; Add new issues by category (Admin, Medical, Medical Examination, Payment, etc.); Manually Close or Delete open issues |
| Check Proposal Issues | Review NB-stage manual proposal issues; Manually Close or Delete |
| Add Manual Issue | Click ADD A MANUAL ISSUE → enter issue text + comment → Confirm |
| Follow Up Query Letter | Reply query letters from UW stage |
| Update LCA | Update LCA status (consent given/rejected) |

**Issue Status:**
- **Closed** — issue has been handled
- **Ignored** — underwriter deems it non-impactful
- Both Closed and Ignored count as resolved (allow UW submit to proceed)

> All UW issues must be closed before Underwriting Submit is allowed.

### Generate Letter Window

- Letter Content: select from predefined items (e.g. More documents required, Signature not provided, Request Medical Exam) + Free Text
- Addressee: Policy Holder and/or Service Agent
- Send Method: Mail / E-mail / etc.
- Actions: PREVIEW | GENERATE LETTER | CLOSE

### Medical Exam Window

- Select Party Name(s) for exam
- Medical Exam Item: move items from Unselected to Selected panel
- Special Medical Exam Item: add custom items with description
- Actions: CONFIRM | CLOSE

---

## UW Decision Tab

**Prerequisite:** All UW issues closed; risk estimation complete

### Making a Decision

**Step 1:** Click Medical/Non-Medical Code Information hyperlink (optional) to review/edit LIA codes

**Step 2:** Select Underwriting Decision

| Decision | Behaviour |
|---|---|
| Accepted | Applied to all products in the case |
| Postponed | Applied to all products in the case |
| Declined | Applied to all products in the case |
| Conditionally Accepted | Product list shown; set decision per product; add conditions |

**Step 3 (Conditionally Accepted only):** For each product, add one or more of:

| Condition Type | Window Fields |
|---|---|
| Extra Loading — Health | Loading Type, Duration (year), Amount, Extra Premium Amount; Calculate Extra Premium |
| Extra Loading — Occupation | Loading Type, Duration (year), Amount, Extra Premium Amount; Calculate Extra Premium |
| Extra Loading — Other | Loading Type, Duration (year), Amount, Reason, Extra Premium Amount; Calculate Extra Premium |
| Restrict SA | Coverage Term, Premium Term, Sum Assured |
| Exclusion | Exclusion Code, Exclusion Comment, Review Period (Month), Exclusion Wordings, Life Assured |
| Condition | Condition Code, Comments |
| Endorsement | Endorsement Code, Comments |

> Exclusions and Endorsements will be printed on policy documents. A policy can have multiple of each.

**UW Decision field rules:**
- If valid LCA exists and Consent Given Indicator = Reject → UW Decision fields are **read-only**
- Fields only editable when no valid LCA exists OR LCA status = Rejected

**Step 4:** Enter Reason (for Declined/Postponed) and UW Decision Comments (optional)

**Step 5:** Click GENERATE LCA (if Conditionally Accepted and LCA required)

**Step 6:** Click SUBMIT (or handle pending letters/surveys first — see Underwriting Submit below)

---

## Underwriting Submit

### Submit Flow

**Check A — Pending Letters/Surveys:**

| Condition | Action |
|---|---|
| Letters to-be-submitted | Status → To be printed/published; case stays UW in Progress; Pending Letter = Yes; continue to survey check |
| Surveys to-be-submitted | Status → Submitted; case disappears from pool; UW in Progress with Survey Status = Submitted |

**Check B — UW Decision:**

| Condition | Action |
|---|---|
| No decision for any product | Error: "Please input UW decision" |
| Decision exists | Check for pending LCA |

**Check C — Pending LCA:**

| Condition | Action |
|---|---|
| LCA to be submitted AND within user authority | LCA status → To Be Printed; case status stays UW in Progress |
| LCA to be submitted AND beyond user authority | Case escalated; status → Pending Approval; LCA stays To Be Submitted |

**Check D — Underwriter Authority:**

| Condition | Action |
|---|---|
| Within authority | UW status → Completed; worksheet/issues/decision data retained |
| Beyond authority | Case escalated; status → Pending Approval (shown in approval pool) |

### Post-Submit Outcomes by Decision

| Decision | System Action |
|---|---|
| Accepted | Recalculates total inforce premium; updates standard/extra premium; proposal routed to enforcement workflow |
| Conditionally Accepted | Generates LCA (if Generate LCA Indicator = Y); awaits consent; when consent received, inforce triggers |
| Declined | Generates Decline letter; refunds premium |
| Postponed | Generates Postpone letter; refunds premium |

### Premium Recalculation on Submit

When UW decision is Accepted/Conditionally Accepted, system recalculates premium if any of these changed:
- Preferred Life Indicator
- Smoker Indicator
- Occupation Class
- Accident Class
- Occupation

Total enforcing premium amount updated accordingly. Declined/Postponed benefits: **no** premium recalculation, but decline/postpone letters generated.

### Batch Decision Processing
- Accepted / Declined / Postponed: select multiple products → batch process
- Conditionally Accepted: **must process each product individually**
- If existing decisions differ across products: cannot batch update; must update one by one

---

## Underwriting Query

**Navigation:** Underwriting > Query (or via hyperlink from NB/CS query result)

**Purpose:** View ongoing and completed UW applications in read-only mode.

**Queryable UW Statuses:** Waiting for Underwriting | Underwriting in Progress | Escalated | Underwriting Completed | Cancellation | Invalid

**Detail page:** Same UI as UW worklist page, but all fields are **inaccessible (read-only)**

**Search Criteria:**

| Field | Description |
|---|---|
| Customer Name | Policy holder name |
| Registration Period | UW task created date |
| Application Source | New Business / Customer Service / Claim |
| Underwriting Status | UW task status dropdown |

---

## Medical Billing

### Create Medical Billing

**Navigation:** Underwriting > Medical Billing > Create Medical Billing

**Use case:** Record medical check fees for UW or claim cases requiring medical examination.

**Steps:**
1. Select Business Type; enter Policy No. and/or Claim Case No. → SEARCH
2. Review Policy Information (auto-populated): Policy Holder, ID Type/Number, Agent
3. Fill Medical Billing Information per exam record: Clinic, Medical Type, GST Inclusive/Absorbed, Fee Amount, GST Amount, Exam Date, Invoice No., Payable To, Disbursement Method, Comment
4. Click ADD to add more records; CONFIRM to submit

### Reverse Medical Billing

**Navigation:** Underwriting > Medical Billing > Reverse Medical Billing

**Steps:**
1. Search by Business Type, Policy No., Clinic, Exam Date range, Medical Status
2. Select billing record(s) to reverse
3. Click REVERSE

---

## Ad Hoc Letter Generation

**Navigation:** Underwriting > Ad Hoc Letter Generation

**Use case:** Generate letters requesting medical records from hospitals/clinics.

**Steps:**
1. Select Letter Name; enter Policy No. → SEARCH
2. Review Policy Information (auto-populated)
3. Select Hospital Name (address auto-shown)
4. Select Patient(s) from party list
5. Fill "We understand that" and "We would like to request for" text fields
6. Select Note Points; add Free Text if needed
7. Click GENERATE LETTER (optionally tick Reminder)

---

## Auto-UW Rules Reference

The following conditions cause a proposal to **fail auto-UW** and be routed to manual underwriting. A proposal issue is raised for each failure.

| # | Condition | Issue Message |
|---|---|---|
| 1 | LA has settled claim history | "The insured {name} has claim history, manual UW is mandatory" |
| 2 | PH-LA relationship is not Self, Child, Spouse, or Parent | "The relationship between the insured {name} and proposer is not applicable" |
| 3 | LA has prior UW history of Conditional Accepted, Postpone, or Decline (status not invalid/cancelled) | "Postpone, decline or conditional accepted decisions have been given to existing policies linked to insured {name}, manual UW is mandatory" |
| 4 | LA Occupation Class ≥ 3 for main product OR > 3 for rider | "The risk of insured's ({name}) job class is too high..." |
| 5 | Product Manual UW Indicator = Y | "{ProductId} needs manual UW as defined" |
| 6 | Beneficiary-insured relationship does not satisfy insurable interest | "The relationship between beneficiary {name} and insured is not applicable" |
| 7 | BMI outside acceptable range for age/gender | "Actual BMI of {name} is {value}. Manual Underwriting is required" |
| 8 | Annual Premium / Annual Income ratio > 1/4 | "Annual premium to annual income of proposer ratio is too high" (Annual income converted to base currency for comparison) |
| 9 | LA's aggregated SA for any cover type exceeds Max Per Life Limit | "Aggregated life SA of {cover type} for the insured {name} exceeds Max Per Life Limit" |
| 10 | Any health declaration question answered "Yes" | "For question '{question}' in Health Declaration - {customer name}, the answer is Yes. Manual Underwriting is required" (raised per question) |
| 11 | Product claim loss ratio > 15% (system parameter) | "Claim loss ratio of {product code} is over 15%. Manual Underwriting is required" |
| 12 | Customer 5-key info partially matches existing customer (ID match OR Name+DOB+Gender match but not all 5) | ID match: "There exists a similar customer to {name} with the same ID type and ID number. Manual underwriting is required." Name+DOB+Gender match: similar message with name/gender/DOB |
| 13 | Policy selected for QA sampling (per QA rate config) | "Manual underwriting is required for Quality Assurance" |
| 14 | Customer 5-key info or partial match found in blacklist | "Customer {name} is in blacklist. Manual underwriting is required" |
| 15 | Backdating: Commencement Date < product's Earliest Date for Backdating | "Commencement date should be equal to or later than {date}" |
| 16 | Backdating: Backdating period > product's Max Period for Backdating | "Backdating period should be no more than {max period}" |

### Risk Aggregation Cover Types
Death | Accidental Death | Accidental Death & Disability | DD Accelerated | DD Additional | Hospital Cash | Hospitalization | TPD Accelerated | TPD Additional | Waive

### Risk Aggregation Trigger Conditions
- First time after case passes UW Process Control (UPC)
- Prior to routing case back to UW worklist
- For CS application type: prior to routing to UW worklist

---

## UW Operation Rules

1. **Issue status:** Closed = handled; Ignored = underwriter deems non-impactful. Both allow UW to proceed.
2. **Non-standard terms** (endorsements, conditions, exclusions): printed on policy documents; a policy can have multiple of each.
3. **Unclosed outstanding issues + Make Benefit Decision:** system shows warning (non-blocking at that step).
4. **Batch processing:** Accepted/Declined/Postponed can be bulk-applied; Conditionally Accepted must be done one product at a time.
5. **Existing decisions differ across products:** cannot batch-update; must update individually.
6. **UW Submit all-products check:** system verifies all products have UW status = Underwriting Completed AND all letters settled. If not, error shown.
7. **Underwriting authority check:** if UW limit (highest among all products) is within user's authority → proceed. If beyond → escalate.

---

## Escalation Rules

| Condition | Action |
|---|---|
| User has authority | UW submit proceeds; decision applied; proposal routed per decision |
| User lacks authority | Proposal escalated to senior; status → Waiting for Underwriting; Pending Reason = "Escalated to next level"; UW status → Escalated |

Escalation follows the same submit path — senior underwriter retrieves from worklist and submits with their authority level.

---

## Update Consent for LCA Rules

1. Default Consent Given Date = current system date
2. Consent Given Indicator must be selected before UPDATE
3. On UPDATE: document status → Replied; Consent Given Date auto-set to current system date
4. If Consent = Agree → inforce triggers when all other inforce criteria are met
5. If Consent = Reject → UW Decision fields become read-only; underwriter must revise decision

---

## UW Status Reference

| UW Status | When Set |
|---|---|
| Waiting for Underwriting | Routed from NB Verification or CS Apply Change |
| Underwriting in Progress | Underwriter opens task |
| Escalated | Beyond current user's authority on Submit |
| Underwriting Completed | Within authority + no pending letters + no pending LCA |
| Pending Approval | Beyond authority on LCA submit |
| Cancellation | CS application cancelled post-UW |
| Invalid | Proposal/policy invalidated |

---

## Config Gaps Commonly Encountered in UW

| Scenario | Gap Type | Config Location |
|---|---|---|
| Manual UW Indicator per product | Config Gap | Product Factory → NB Rules → Manual UW Indicator |
| Max Per Life Limit per cover type | Config Gap | Product Factory → Risk Aggregation → Max Per Life Limit |
| Aggregation risk type per benefit | Config Gap | Product Factory → Benefit Definition → Aggregation Risk Type |
| Annual premium / annual income ratio threshold (1/4) | System Parameter | UW Rules Config → Premium-Income Ratio |
| Claim loss ratio threshold (15%) | System Parameter | UW Rules Config → Claim Loss Ratio |
| QA sampling rate | Config Gap | UW QA Config Table → Submit Channel / Sales Channel / Product / QA Rate |
| Underwriter authority limits | Config Gap | User Authority Config → UW Limit per user/role |
| Blacklist maintenance | Operational | Customer Blacklist Table |
| BMI range per age/gender | Config Gap | UW Rules Config → BMI Range Table |
| Occupation Class risk thresholds | Config Gap | UW Rules Config → Occupation Class Limit |
| Insurable interest relationship mapping | Config Gap | UW Rules Config → Insurable Interest Relationship |
| LCA generation indicator per product | Config Gap | Product Factory → NB Rules → Generate LCA Indicator |
| Declaration health question trigger | Config Gap | NB Declaration Form → Question Answer Trigger UW |

---

## INVARIANT Declarations (UW Module)

```
INVARIANT 1: All UW issues must be closed before Underwriting Submit is allowed
  Enforced at: Underwriting > Submit button
  Error if violated: System blocks submit; displays outstanding issue count

INVARIANT 2: All products must have UW status = Underwriting Completed before Submit
  Enforced at: Underwriting Submit → all-products check
  Error if violated: "Not all products have been underwritten or not all letters have been settled"

INVARIANT 3: Conditionally Accepted UW decision cannot be bulk-applied across products
  Enforced at: UW Decision tab → batch decision
  Effect: Underwriter must process each product individually for conditional acceptance

INVARIANT 4: If valid LCA exists and Consent Given Indicator = Reject → UW Decision fields are read-only
  Enforced at: UW Decision tab → field editability
  Effect: Underwriter cannot change decision until LCA is resolved or invalidated

INVARIANT 5: Escalation is determined by underwriter authority at Submit time
  Enforced at: Underwriting Submit → authority check
  Effect: Case escalated to senior if UW limit exceeds current user's authority; no manual override

INVARIANT 6: For claim cases with multiple policies, submitting UW for one policy auto-submits all others in the same claim case
  Enforced at: Underwriting Submit (Claim type)
  Effect: All sibling UW tasks submitted simultaneously
```

---

## ⚠️ Limitations & Unsupported Scenarios

> This section documents known limitations and scenarios NOT supported by the system. Updated: 2026-03-14

### Underwriting Rules

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Financial UW (HNW) | Not supported | Code | High Net Worth underwriting requires custom module |
| Cross-Border Guidelines | Not supported | Code | Country-specific sales rules require development |
| Custom UW Questions | Limited to predefined templates | Config | Complex HNW questionnaires need development |
| Income Verification | Not automated | Config | Manual verification only |

### Risk Assessment

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Anti-Money Laundering | Basic checks only | Config | Advanced AML requires integration |
| Sanctions Screening | Limited databases | Config | Additional screening needs development |
| Cross-Policy Limits | Not fully automated | Config | Manual monitoring required |

### Investor Classification (MAS SFA 4A)

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| AI/Non-AI Classification | Not supported | Code | Requires development for MAS SFA 4A criteria |
| Annual Income Threshold | Not automated | Config | Manual verification of $2M+ income |
| Net Asset Verification | Not automated | Code | Requires asset declaration system |

---

## Related Files

| File | Purpose |
|---|---|
| `ps-new-business.md` | NB module detail (registration through inforce) |
| `ps-customer-service.md` | CS / Policy Servicing module (CS alterations requiring UW) |
| `insuremo-ootb-full.md` | UW OOTB capability classification (use for Gap Analysis) |
| `ps-product-factory.md` | Product Factory config for UW-related rules (manual UW, aggregation, LCA) |
| `output-templates.md` | BSD output templates for UW-related gaps |