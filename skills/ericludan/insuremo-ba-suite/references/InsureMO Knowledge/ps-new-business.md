# InsureMO Platform Guide — New Business (NB)
# Source: New Business User Guide V2022 (eBaoTech)
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb-full.md instead
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"how does New Business work in InsureMO"** — navigation paths, prerequisites, field behaviour, workflow config parameters, and business rules for each NB stage.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for an NB-related gap
- Agent 6 is generating a **Config Runbook** for NB items
- A BA needs to verify what **preconditions** the system enforces before allowing a stage transition

---

## Module Overview

```
New Business (NB) Module
│
├── NB Registration          ← Initial proposal registration (reception)
├── NB Data Entry            ← Full policy information entry workbench
├── NB Verification          ← QC check after data entry
├── NB Underwriting          ← Auto-UW or manual UW routing (see ps-underwriting.md)
├── NB Collection            ← Premium collection before inforce
├── NB Inforce               ← Policy activation (auto or manual trigger)
├── NB Pending Issue         ← Proposals accepted but not yet inforced
├── NB Withdrawal            ← Manual proposal withdrawal
├── NB Reverse New Business  ← Revert completed/inforced policy to a prior stage
├── NB Query                 ← Search and view NB proposals/policies
└── NB Watch List            ← Task release and reassignment
```

---

## NB Workflow — Standard Sequence

```
Step 1: NB Registration (Initial Registration)
  └─► Step 2: NB Data Entry
        └─► Step 3: NB Verification
              └─► Step 4: NB Underwriting (if auto-UW fails)
                    └─► Step 5: NB Collection (if premium required before inforce)
                          └─► Step 6: NB Inforce (auto-triggered or manual)
                                └─► Policy In-Force
```

**Optional workflow steps:**
- Step 7: Withdrawal (before inforce; manual or batch auto-withdrawal)
- Step 8: Reverse New Business (revert to a prior stage; including post-inforce)
- Step 9: Pending Issue follow-up (accepted but blocked from inforcing)

**Proposal status flow:**

| Status | Set When |
|---|---|
| Waiting for Data Entry | Registration submitted |
| Data Entry in Progress | Processor opens NB task |
| Waiting for Verification | Data Entry submitted |
| Verification in Progress | Verifier opens task |
| Waiting for Underwriting | Verification submitted with UW issues |
| Underwriting in Progress | Underwriter opens UW task |
| Accepted | UW decision = Accepted, all criteria met |
| Conditionally Accepted | UW decision = Conditionally Accepted |
| Postponed | UW decision = Postponed |
| Declined | UW decision = Declined |
| Inforce | All inforce criteria met; policy activated |
| Withdrawn | Manual or batch withdrawal submitted |

---

## Menu Navigation

| Action | Path |
|---|---|
| Register new proposal | New Business > Registration |
| NB data entry worklist | New Business > Work List (Data Entry tab) |
| NB verification worklist | New Business > Work List (Verification tab) |
| Pending issue worklist | New Business > Work List (Pending Issue tab) |
| Withdraw proposal | New Business > Withdraw Proposal |
| Reverse new business | New Business > Reverse New Business |
| Query proposal / policy | New Business > Query |
| Watch list (task mgmt) | New Business > Watch List |
| Declaration Question config | New Business > Configuration > Declaration Question |
| Declaration Form config | New Business > Configuration > Declaration Form |

---

## Stage 1: Initial Registration

### Overview
After receiving a proposal from the sales channel, counter staff registers basic proposal information. This is called **Initial Registration** or **Reception**.

### Prerequisites
- None (entry point for all new business)

### Steps
1. Navigate to **New Business > Registration**
2. Enter: Proposal No. (optional), Proposal Sign Date, Producing Agent, Main Product
3. Select Currency and Proposal Submission Date
4. Click **Submit**

### Result
- Proposal No. and Policy No. are generated
- Proposal status → **Waiting for Data Entry**
- Click **Go to Data Entry** to proceed immediately

### Key Field Rules — Registration Page

| Field | Rule |
|---|---|
| Proposal Sign Date | Must be ≤ current system date; must not be > 12 months before current date; cannot be earlier than product launch date |
| Producing Agent | Must be valid, active, and have qualification to sell the selected product |
| Main Product | Must be the main product (not a rider); must be on sale (end date > submission date); agent must be qualified to sell it |
| Agent branch | If Individual Agent or Company Direct: branch must be allowed to sell the product. Otherwise: agent branch must have agreement with insurer |

---

## Stage 2: Data Entry

### Overview
Data Entry (detailed registration) is where users input all policy information from the application form across multiple sections.

### Prerequisites
- Initial Registration completed
- Proposal status is **Waiting for Data Entry** or **Data Entry in Progress**

### Navigation
New Business > Work List → Data Entry tab → search → click hyperlink

### UI Notes
- All sections can be folded/unfolded
- A right-margin navigator allows fast section-jumping
- **Unsaved data is lost** if you leave without clicking SAVE

### Sections in Data Entry

| Section | Purpose |
|---|---|
| Basic Information | Proposal/policy identifiers, dates, agent, flags |
| Policyholder Information | PH individual or organization details |
| Life Assured Information | LA details; can add multiple LAs |
| Payer Information | Payer individual or organization details |
| Payment Information | Premium payment method and disbursement |
| Product Information | Main product + riders/waivers |
| Nomination Beneficiary | Beneficiary details and sharing |
| Nomination Trustee | Trustee details |
| Beneficial Owner | Beneficial owner details |
| Trusted Individual | Trusted individual details |
| Declaration Information | Declaration Q&A per customer role |
| Proposal Issue | Outstanding issues list |

---

### Section: Basic Information

Key field rules:

| Field | Rule |
|---|---|
| Proposal Sign Date | Not earlier than product launch date; not later than registration date; not > 12 months before current date |
| Commencement Date | Defaults to Submission Date; cannot be later than current system date; can be backdated if product allows and period not exceeded |
| Backdating Indicator | Only settable to Yes if product allows backdating; when Yes, commencement date becomes editable; changing it triggers warning to resubmit benefit entry for recalculation |
| Backdating > 183 days | System calculates overdue interest on total enforcing premium |
| Discount Type = Staff | System validates that both PH and main insured are staff |
| Delivery Preference Type | Email requires PH email; Physical Copy requires mailing address |

---

### Section: Policyholder Information

- PH type: **Individual** or **Organization**
- Search existing customer by name (search icon, top-right of section)
- Reset icon clears all fields

**Customer matching on Validate / Submit:**
- If 5 basic fields (ID type + ID No. + Full Name + DOB + Gender) match an existing customer → **update** existing customer
- If not all 5 match → **create** new customer
- Similar customer found → system raises outstanding issue

**Cascade on PH change/delete:**
- Deleting or updating PH cascades to: Life Assured, Payer, Beneficiary, Trustee, Beneficial Owner, Trusted Individual, Declaration, Product information

---

### Section: Life Assured Information

- Relationship options: **Self** | Spouse | Parent | Child | Others
- If **Self**: LA info copied from PH; PH fields used
- If **Others**: relationship type dropdown + separate info entry
- Can add **multiple LAs** using Add button

**Cascade on LA change/delete:**
- Delete LA → related Payer, Declaration, Product deleted
- Update DOB / Gender / Occupation / Preferred Life Indicator / Smoker Indicator → system syncs to Product section and recalculates

---

### Section: Payer Information

| Payer Type | Options |
|---|---|
| Individual | Same as Policyholder / Main LA / Additional LA / Others |
| Organization | Same as Policyholder / Others only |

---

### Section: Payment Information (Premium Payment & Disbursement Method)

- Supported methods: **Cash**, **Cheque**, **Direct Debit**, **Credit Card**
- New business payment method auto-applied to Renew and Disbursement by default
- Uncheck "Apply For Renew Payment Method" or "Apply For Disbursement Method" to set separately

| Method | Additional Fields Required |
|---|---|
| Cash / Cheque | Payer = Policyholder or Life Assured |
| Direct Debit / Credit Card | Payer + Account No. + Bank info |

---

### Section: Product Information

#### Main Product
- Pre-populated from Registration; system applies default field values from product definition
- Coverage Term / Premium Term linked: selecting one filters the other to valid values only
- Delete main product → **all products deleted**
- Click **Add** after filling compulsory fields to confirm; declaration info generated automatically

#### Supported Product Types
- Traditional Product
- Annuity Product
- Investment Product (ILP) — includes fund allocation, STU, RSP, RTU sub-sections
- Variable Annuity Product
- Hospital Benefit Product
- Mortgage Product — requires Mortgage detail table (Year From / Year To / Interest Rate)
- Joint Life Product
- Indexation Product

#### Riders and Waivers (Optional)
- Added after main product is confirmed
- Filtered from dropdown based on main product
- **WOP (Waive Policy) waiver rules:**
  - Adding 1st WOP → system auto-adds WOP to all existing riders
  - Adding new rider when WOP exists → system auto-adds WOP to new rider
  - Deleting any WOP → system deletes **all** WOPs
- **Embedded Rider rules:**
  - Auto-attached if coverage/premium term + SA match main benefit
  - If only one config defined, auto-attach with that config
  - If mismatch → not auto-attached; proposal issue raised for manual entry
  - System checks if user manually removed embedded riders; if so, raises proposal issue

---

### Section: Nomination Beneficiary

- Nomination Type mandatory if valid beneficiary named
- Nomination Date mandatory if nomination type selected
- Nomination Types: Revocable (49M) | Trust Nomination (49L) | Section 73 CLPA
- Total sharing percentage of all beneficiaries must equal **100%**

---

### Section: Nomination Trustee

- Can add multiple trustees (Individual or Organization)
- System records party info and displays in Underwriting / Common Query

---

### Section: Beneficial Owner

- Can add multiple beneficial owners (no limit)
- Relationship = Self → auto-populates PH info (read-only)
- Relationship = Others → relationship dropdown shown; detail fields required

---

### Section: Trusted Individual

- Can add multiple trusted individuals (no limit)
- Relationship = Self → auto-populates PH info (read-only); disabled if PH is Organization
- Fields: Basic Information, Identifier Information, Contact Number/Email

---

### Section: Declaration Information

- Lists all LAs and PH; click Edit per customer to enter declaration Q&A, then Confirm
- All customers in the list must have declaration confirmed before submission

**Configure Declaration Question:**
New Business > Configuration > Declaration Question → Edit / Delete / New Question

**Configure Declaration Form:**
New Business > Configuration > Declaration Form → Edit / Copy / Delete / Export / New Form
- Map forms to products and roles via Declaration Form Mapping table
- Questions can be reordered by drag-and-drop

---

### Data Entry Actions (Bottom Bar)

| Action | Behaviour |
|---|---|
| Comment | Leave/view comments; user decides sensitive or public |
| Validate | System auto-checks and surfaces proposal issues (Outstanding Issue tab) |
| Data Entry Submit | Runs full validation; on success, status → Waiting for Verification |

### Proposal Issues

- Auto-generated issues: resolved by system → auto set to "Deleted"
- Manual issues: user can "Ignore" or "Close"
- Add manual issue: Proposal Issue tab → Add icon → enter issue + comment → Confirm

**Submit blocked if any of:**
- Compulsory field not filled
- Beneficiary sharing ≠ 100%
- Declaration not submitted
- Pending cause not empty
- Query letter requiring reply not replied/deleted/discarded

---

## Stage 3: Verification

### Overview
Verification checks data entry for errors. Verifier can modify directly or send back to data entry.

### Prerequisites
- Data Entry submitted; proposal status = **Waiting for Verification** or **Verification in Progress**

### Navigation
New Business > Work List > Verification tab → search → click hyperlink

### Key Behaviours
- Verification page is identical to Data Entry page; all fields fully editable
- Modify and click Save; or click **Back to Data Entry** to return proposal
- Comment available (same as Data Entry)
- Proposal Issues: same as Data Entry stage

### Verification Submit Results

| Condition | Outcome |
|---|---|
| Underwriting issues exist | → Waiting for Underwriting |
| No underwriting issues | Proposal auto-accepted |
| Rejection issues exist | System auto-declines proposal |

---

## Stage 4: Underwriting

Handled by Underwriting Workbench — refer to **ps-underwriting.md** for full detail.

Auto-UW runs after Verification Submit. If manual evaluation required, proposal routed to UW worklist.

---

## Stage 5: Pending Issue

### Overview
Proposals that are accepted or conditionally accepted but cannot be inforced yet (e.g. short payment, age limit exceeded) are placed in the Pending Issue worklist.

### Prerequisites
- UW decision = Accepted or Conditionally Accepted
- Proposal has a "not inforce" reason blocking activation

### Navigation
New Business > Work List > Pending Issue tab

### Not Inforce Reasons

| Reason | Meaning |
|---|---|
| Premium Shortage | Insufficient initial premium collected |
| Age Increased - Premium Shortage | Age changed at issuance; initial premium now insufficient |
| Age Increased - Exceed Age Limit | LA age now exceeds product age limit |

### Actions from Pending Issue

| Action | Behaviour |
|---|---|
| INFORCE | Manually triggers inforce API for selected proposal |
| BATCH INFORCE | Triggers inforce for multiple selected records |
| REMIND | Opens Send Reminder window; send to Agent and/or Policyholder by SMS/Email |
| MORE > Withdraw Proposal | Routes to Withdraw page with proposal pre-populated |
| MORE > Reverse New Business | Routes to Reverse page with proposal pre-populated |
| MORE > Query | Opens NB Query for proposal detail |

---

## Stage 6: Inforce

### Overview
A policy is inforced when it passes all required validations. Inforce can be triggered automatically or manually.

### Inforce Triggers (Auto)
- Consent Received Indicator updated to Y (conditionally accepted cases)
- Direct Debit account updated (when renewal method = Direct Debit)
- UW complete and status = Accepted
- Overdue interest waived
- Payment collection cancelled but remaining balance sufficient

### Inforce Criteria (All Must Be Met)
- Proposal status = Accepted or Conditionally Accepted
- Consent Given Indicator = Y
- For monthly frequency: Direct Debit account number available
- Premium fully paid within tolerance limit

### Inforce Date Calculation
- = Latest of: Consent Given Date, Effective Date of Full Payment, Direct Debit Date, LCA Date

### Commencement Date Rules

| Condition | Commencement Date |
|---|---|
| Backdating case | As per user input |
| Standard LCA, health warranty not expired | Later of LCA date and effective full payment date |
| Standard LCA, health warranty expired | Latest of LCA date, effective full payment date, health warranty extended date |
| Substandard LCA | Latest of consent given date, effective full payment date, health warranty extended date |
| SG Shield product, registered Mon or Tue | Next Monday |
| SG Shield product, registered Wed–Sun | Next Monday |

### Backdating Commencement Date Adjustment

| Condition | Action |
|---|---|
| Auto backdate indicator = Y AND First of Month = N AND age increases | Commencement date → DOB of LA − 1 day (earliest DOB for multi-LA) |
| Auto backdate indicator = N AND First of Month = Y | Commencement date → first day of the month |

### System Actions on Inforce
1. Set Inforcing Date
2. Update Commencement Date
3. Recalculate LA age based on commencement date
4. Recalculate proposal premium
5. Update policy and benefit information
6. Generate fund transaction application (investment products)
7. Update and insert fee records; apply General Suspense to premium income
8. Refund excess premium (if Advance Premium Indicator = N → general suspense for refund; if Y → APA)
9. Generate policy documents
10. Generate LCA if Generate LCA Indicator = Y (then set indicator to N)
11. Record supervisor hierarchy of service agent

### Short Payment Rules

| Condition | Outcome |
|---|---|
| Suspense ≥ Total Enforcing Premium | Regarded as fully paid; validation passed |
| Pre-defined fixed tolerance > shortfall > 0 | Regarded as fully paid; short payment record inserted (Company waives) |
| Shortfall exceeds tolerance | Validation fails; Not Inforce Reason = "Premium Shortage" |

---

## Reversal and Withdrawal

### Withdraw Proposal

**Prerequisites:**
- Proposal status is NOT: Withdrawn, Inforce, Postponed, Declined, or renewal policy status
- Refund payee is determined

**Navigation:** New Business > Withdraw Proposal

**Steps:**
1. Enter Policy No. or Proposal No. → Search
2. Complete Withdrawal Information section (Reason, Claw Back Medical Fee, Disbursement Method)
3. Click Submit

**Result:** System generates payment record with status = Temporary Fee Status For Approval

**Withdraw Reasons:** Client request | Non-acceptance of counter offer letter | Auto Cancellation | Others

**Auto-withdrawal batch:** Separate process (refer to User Guide_Auto Proposal Withdrawal Batch)

---

### Reverse New Business

**Purpose:** Revert a proposal/policy back to a prior workflow stage (Data Entry, Verification, or Underwriting).

**Prerequisites:**
- Policy status = Withdrawn / Declined / Postponed / Accepted / Conditionally Accepted / Inforce
- Policy NOT frozen by CS or Claims
- No CS or Claim history
- Policy not renewed or in renewal progress
- No pending financial transactions

**Navigation:** New Business > Reverse New Business

**Reversal Routing Rules:**

| Policy Status | Can Revert To |
|---|---|
| Inforce | Data Entry / Verification / Underwriting |
| Accepted or Conditionally Accepted | Data Entry / Verification / Underwriting |
| Postponed or Declined | Data Entry / Verification / Underwriting |
| Withdrawn (last workflow = Data Entry) | Data Entry only |
| Withdrawn (last workflow = Verification) | Data Entry / Verification |
| Withdrawn (last workflow = Underwriting) | Data Entry / Verification / Underwriting |

**Note:** If premium refund for withdrawn/declined/postponed proposal has already been paid, after reversal the proposal must go through initial premium collection again.

---

## NB Query

**Navigation:** New Business > Query

- Search by Policy No., Proposal No., Policy Status, Registration Period, Branch, Agent, Customer Name, Submission Period, ID Type/No.
- Click hyperlink to view proposal detail
- Fields under Policy Information and Proposal Issue tabs: **read-only** (snapshot at NB stage)
- For inforced policies, NB query shows snapshot data; CS/Claim changes not reflected — use **Common Query** for latest data
- Fields displaying **latest data** regardless: Policy Status, Short Payment Amount, Not Inforce Reason

---

## NB Watch List

**Purpose:** Release and reassign NB tasks (Data Entry and Verification stages).

**Navigation:** New Business > Watch List

**Operations:**

| Purpose | Operation |
|---|---|
| Release task | Select tasks → RELEASE (tasks returned to shared pool) |
| Export tasks | EXPORT → downloads all results to Excel |
| Reassign (Push) | Select tasks → Reassign Strategy = Push → select target user → REASSIGN |
| Reassign (Auto) | Select tasks → Reassign Strategy = Task Auto Assign Strategy → REASSIGN |

---

## e-Submission

NB Workbench can receive electronic proposals from Agent Portal or Customer Portal via e-submission API. Proposal is routed per pre-defined workflow rules.

---

## Proposal Rules Reference

### Submission Warning Checks (non-blocking)

1. PH email address is empty
2. LA age on current date ≠ age on commencement date AND backdate indicator = No
3. LA age on current date + 1 month ≠ age on commencement date AND backdate indicator = No
4. Last Review Date blank OR older than X days (default X = 30; system-configurable)
5. PVC Indicator = Yes → warning to check VOS process

### Submission Rules (Proposal Issue Generated if Failed)

1. Fund premium apportionment missing for UL/ILP product
2. Mandatory fields missing: Basic Info, PH, LA, Payment, Product
3. Fund allocation mandatory fields missing (Regular/Single/Top-Up premium)
4. Data appropriateness failures
5. Agent status = Invalid
6. Beneficiary/nominee share ≠ 100% within same order
7. Fund apportionment sum ≠ 100%
8. Annual Income not entered for proposer
9. Mortgage: Deferred Level Term < Min Month of Level Period (when With Level Cover Period = Y)
10. Mortgage: Deferred Level Term > Max Month of Level Period (when With Level Cover Period = Y)
11. Backdating: Commencement Date earlier than product's Earliest Date for Backdating
12. Backdating: Backdating period > product's Max Period for Backdating
13. Rider Premium Term > Main Product Premium Term
14. Rider Coverage Term > Main Product Coverage Term
15. Reversal deleted original product
16. Sum of specific riders' SA ≥ main product SA (when "Sum of SA not greater than Parent SA = Yes")
17. Accelerating rider SA ≥ basic product SA and 1st party waiver is attached → not allowed

### Singapore-Specific Rules

1. Shield product: both PH and LA citizenship must be "Singapore Citizen" or "Singapore Permanent Resident"
2. Shield insured: relationship with PH cannot be "Employer" or "Employee"
3. Non-Shield insured: relationship cannot be "Granddaughter", "Grandson", "Grandmother", "Grandfather"
4. Each insured can have max 1 inforced Shield Main Policy and 1 inforced Shield Rider Policy with non-overlapping coverage periods

---

## Config Gaps Commonly Encountered in NB

| Scenario | Gap Type | Config Location |
|---|---|---|
| Backdating allowed per product | Config Gap | Product Factory → NB Rules → Backdating Allowed Indicator |
| Max backdating period | Config Gap | Product Factory → NB Rules → Max Period for Backdating |
| Earliest backdating date | Config Gap | Product Factory → NB Rules → Earliest Date for Backdating |
| WOP auto-attachment | Config Gap | Product Factory → Waiver Rules → Waiver Type = Waive Policy |
| Embedded rider configuration | Config Gap | Product Factory → Rider Rules → Embedded Rider |
| Coverage/Premium term matrix | Config Gap | Product Factory → Coverage-Premium Term Relationship Matrix |
| Declaration form mapping | Config Gap | NB Configuration → Declaration Form Mapping |
| Manual UW Indicator per product | Config Gap | Product Factory → NB Rules → Manual UW Indicator |
| Advance Premium Indicator | Config Gap | Product Factory → NB Rules → Advance Premium Indicator |
| Generate LCA Indicator | Config Gap | Product Factory → NB Rules → Generate LCA Indicator |
| Auto backdate indicator per benefit | Config Gap | Product Factory → Benefit Definition → Backdating Indicator |
| First of Month indicator per benefit | Config Gap | Product Factory → Benefit Definition → First of Month |
| Short payment tolerance amount | Config Gap | System Rate Table → Short Payment Tolerance |
| Inforcing installment per product | Config Gap | System Rate Table → Inforcing Installment |
| QA rate configuration | Config Gap | UW QA Config Table → Submit Channel / Sales Channel / Product / QA Rate |
| Task auto-assign strategy | Config Gap | NB Assignment Strategy Configuration |
| Auto-withdrawal batch criteria | Config Gap | Auto Proposal Withdrawal Batch Config |

---

## ILP / Investment Product Rules (from NB UG)

Referenced from: `ps-investment.md` for fund-level rules.

In NB Data Entry > Product Information > ILP Product:

See fund allocation rules in ps-investment.md.

## Premium Types (from NB UG)

| Premium Mode | Formula | Notes |
|---|---|---|
| Annual | Total Annual Premium x 1 | Standard |
| Semi-Annual | Total Annual Premium / 2 | 2x per year |
| Quarterly | Total Annual Premium / 4 | 4x per year |
| Monthly | Total Annual Premium / 12 | 12x per year |
| Single | Total premium paid upfront | No ongoing collection |



## Sum Assured Rules (from NB UG)

| Rule | Description | Enforced At |
|---|---|---|
| Min SA | Product minimum sum assured | Data Entry Submit |
| Max SA | Product maximum sum assured | Data Entry Submit |
| SA multiple of | SA must be in increments | Data Entry Submit |
| Rider SA <= Main SA | Rider cannot exceed main benefit SA | Data Entry Submit |
| Accelerated rider | Cannot exceed main SA | Data Entry Submit |
| SA banding | SA in different bands may have different rates | Data Entry Submit |


## e-Policy Issuance (from NB UG)

### e-Policy Flow
1. Policy Inforced
2. System auto-generates e-Policy document
3. If Delivery Preference = Email: auto-send to PH email
4. If Delivery Preference = Physical: pending dispatch queue

### Documents Generated on Inforce
- Policy Contract
- Benefit Illustration
- Policy Schedule
- Nomination Certificate
- LCA (if Generate LCA Indicator = Y)


## Data Entry Field Detail (from NB UG)

### Basic Information Fields
| Field | Rule | Enforced At |
|---|---|---|
| Proposal Sign Date | <= Current Date; >= product launch date; not > 12 months before today | Submit |
| Commencement Date | <= Current Date; can be backdated if product allows | Submit |
| Backdating Indicator | Y only if product allows backdating | Field Entry |
| Backdating > 183 days | Overdue interest calculated | Submit |
| Discount Type = Staff | Both PH and LA must be staff | Submit |
| Delivery Preference = Email | PH email required | Field Entry |
| Delivery Preference = Physical | Mailing address required | Field Entry |



### Customer Information Fields
| Field | Rule | Mandatory |
|---|---|---|
| ID Type | Valid code from ID Type table | Y |
| ID No. | Format validated by ID Type | Y |
| Full Name | Must match ID exactly | Y |
| Date of Birth | Valid date; age auto-calculated | Y |
| Gender | M / F / Unknown | Y |
| Nationality | From country code table | Y |
| Occupation | From occupation table; affects UW | Y |
| Smoker Indicator | Affects premium rate | Y |
| Annual Income | Required for HNW products | Conditional |
| Email | Valid email format | Conditional |
| Contact No. | Valid phone format | Y |


## INVARIANT Declarations (NB Module)

```
INVARIANT 1: Proposal cannot proceed to Verification if compulsory fields are missing
  Enforced at: Data Entry Submit
  Error if violated: System shows error message; blocks submission

INVARIANT 2: Beneficiary sharing must total 100% within the same order
  Enforced at: Data Entry Submit + Verification Submit
  Error if violated: System shows error message; blocks submission

INVARIANT 3: Declaration must be confirmed for all customers before submission
  Enforced at: Data Entry Submit
  Error if violated: System shows error message; blocks submission

INVARIANT 4: Deleting main product deletes ALL products on the policy
  Enforced at: Product Information → Delete main product
  Effect: All riders and waivers removed immediately

INVARIANT 5: Rider Term ≤ Main Product Term (Coverage and Premium)
  Enforced at: Data Entry Submit + Verification Submit
  Error if violated: Proposal issue generated

INVARIANT 6: Reverse New Business blocked if CS/Claim history exists or policy is frozen
  Enforced at: New Business > Reverse New Business → Submit
  Error if violated: System blocks reversal

INVARIANT 7: WOP deletion removes all WOP instances across all riders
  Enforced at: Product Information → Delete WOP waiver
  Effect: All WOP records on policy deleted automatically
```

---

## ⚠️ Limitations & Unsupported Scenarios

> This section documents known limitations and scenarios NOT supported by the system. Updated: 2026-03-14

### Premium & Payment

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| In-kind Premium Payment | Not supported | Code | Cannot use securities/funds/assets as premium payment |
| Premium Payment Methods | Limited to cash, cheque, GIRO, credit card | Code | Other payment methods require development |
| Premium Collection (Recurring) | Only via GIRO | Config | Other methods need customization |

### Product Types

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Product Type Support | Limited to Traditional + ILP | Code | Other product types require development |
| Multi-Currency | Limited to configured currencies | Config | Cannot add new currencies without IT |

### Underwriting

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Joint-Life UW | Limited configurations | Config | Complex scenarios require development |
| Financial UW (HNW) | Not supported | Code | Requires custom HNW module |
| Cross-Border UW | Not supported | Code | Country-specific rules require development |

### Application Process

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Third-Party Application | Limited support | Code | Full third-party applications need development |
| Corporate Application | Limited support | Code | Corporate policyholder has restrictions |

---

## Related Files

| File | Purpose |
|---|---|
| `ps-underwriting.md` | Underwriting workbench detail (NB, CS, Claim UW) |
| `ps-customer-service.md` | CS / Policy Servicing module detail |
| `insuremo-ootb-full.md` | NB OOTB capability classification (use for Gap Analysis) |
| `ps-product-factory.md` | Product Factory config for NB-related product rules |
| `output-templates.md` | BSD output templates for NB-related gaps |