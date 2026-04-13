# InsureMO Platform Guide — Customer Service (CS / Policy Servicing)
# Source: Customer Service User Guide V25.04 (Traditional) + Customer Service ILP User Guide V25.04
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb-full.md instead
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"how does CS work in InsureMO"** — navigation paths, prerequisites, field behaviour, workflow config parameters, and business rules for each CS alteration item.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for a CS-related gap
- Agent 6 is generating a **Config Runbook** for CS items
- A BA needs to verify what **preconditions** the system enforces before allowing an alteration

---

## Module Overview

```
Customer Service (CS) Module
│
├── CS Registration          ← Entry point for all alterations
├── CS Data Entry            ← Alteration item workbench
├── CS Underwriting          ← Auto-UW or manual UW routing
├── CS Approval              ← 2nd-level approval workflow
├── CS In-Force              ← Collection and effective date
├── CS Watch List            ← Task release and reassignment
├── CS Query                 ← Search and view CS applications
├── CS Reversal              ← Undo completed alterations
└── CS Policy Servicing Quotation  ← Pre-transaction quotation
```

---

## CS Workflow — Standard Sequence

```
Step 1: CS Registration
  └─► Step 2: CS Data Entry (alteration item entry + Apply Change)
        └─► Step 3: CS Underwriting (if Need UW = Yes OR health declaration = Yes)
              ├─► Auto-UW passed → Step 4
              └─► Manual UW → UW Workbench → Step 4
        └─► Step 4: CS Approval (if Need Approval = Yes OR auto-approval fails)
              └─► Step 5: CS In-Force (if collection required)
                    └─► Alteration effective
```

**Optional workflow steps:**
- Step 7: Reject application (during Entry, UW, or Approval stage)
- Step 8: Cancel application (before In-Force)
- Step 9: Reverse alteration (after In-Force, for eligible items)

**Workflow config parameters** (controlled in CS Workflow Configuration table):

| Parameter | Values | Effect |
|---|---|---|
| `Need UW` | Y / N | Routes to UW workbench if Y |
| `Health Declaration` | Y / N | Triggers UW if Y |
| `Need Approval` | Y / N | Escalates to 2nd-level approval if Y |
| `Financial Impact` | Y / N | Determines whether collection/refund applies |
| `Allow Reversal` | Y / N | Controls whether alteration can be reversed post-inforce |

---

## Menu Navigation

| Action | Path |
|---|---|
| Register new CS application | Customer Service > Registration |
| CS data entry workbench | Customer Service > WorkList > Data Entry |
| CS approval queue | Customer Service > WorkList > Approve |
| CS pending in-force queue | Customer Service > WorkList > Pending In Force |
| CS watch list | Customer Service > Watch List |
| Query CS application | Customer Service > Query |
| Reverse alteration | Customer Service > Reversal |
| PS Quotation | Customer Service > Policy Servicing Quotation |
| FATCA Information | Customer Service > FATCA Information |

---

## CS Alteration Items — Master List

Items are classified by product applicability and financial impact.

### Applies to Both Traditional and ILP

| Alteration Item | Financial Impact | Need UW (default) | Reversible |
|---|---|---|---|
| Add Rider | Yes | Possible | Yes |
| Apply Policy Loan | Yes | No | Yes |
| Cancellation (Void Policy) | Yes | No | No |
| Change Assignment | No | No | No |
| Change Beneficial Owner | No | No | No |
| Change Birth Date or Gender | Yes | Yes | Yes |
| Change Contact Information | No | No | Yes |
| Change Disbursement Method | No | No | Yes |
| Change Discount Type | No | No | Yes |
| Change HPS Exemption Information | No | No | Yes |
| Change Occupation | Yes | Yes | Yes |
| Change of Benefit Level (Health) | Yes | Yes | Yes |
| Change Payer | No | No | Yes |
| Change Payment Frequency | Yes | No | Yes |
| Change Payment Method | No | No | No |
| Change Policy Holder | No | No | No |
| Change Smoker Status | Yes | Yes | Yes |
| Change Survival Benefit or Cash Bonus Option | No | No | Yes |
| Change Term | Yes | Possible | Yes |
| Delete Rider | Yes | No | Yes |
| Freelook | Yes | No | No |
| Nomination — Beneficiary | No | No | Yes |
| Nomination — Trustee | No | No | Yes |
| Reinstatement | Yes | Yes | No |
| Underwriting Review | Yes | Yes | N/A |

### Traditional Policy Only

| Alteration Item | Financial Impact | Notes |
|---|---|---|
| Change Benefits | Yes | Changes benefit amount / type on traditional plan |
| Decrease Sum Assured / Partial Surrender | Yes | Includes partial surrender for traditional |
| Increase Sum Assured | Yes | Requires UW |
| Perform Reduced Paid Up | Yes | Converts to paid-up; product must allow it |
| Policy Suspension | No | Suspends policy; no premium collection |
| Premium Adjustment | Yes | Adjusts premium amount; Regular premium only |
| Reversionary Bonus Surrender | Yes | Surrenders bonus only; policy remains inforce |
| Termination / Surrender | Yes | Full surrender; policy terminates |
| Transfer of Coverage | Yes | Transfers coverage to another policy |

### ILP Only

| Alteration Item | Financial Impact | Notes |
|---|---|---|
| ILP Ad-hoc Single Premium Top-Up | Yes | Additional investment top-up |
| ILP Change Investment Regular Premium | No | Increase / decrease investment premium |
| ILP Change Regular Premium Apportionment | No | Redirect premium among funds |
| ILP Decrease Sum Assured | No | Reduces SA; no financial transaction |
| ILP Full Surrender | Yes | Full surrender; policy terminates |
| ILP Increase Sum Assured | No | Increases SA; no additional premium |
| ILP Life Replacement Option | Yes | Replaces insured life |
| ILP Partial Withdraw | Yes | Withdraws from policy fund |
| ILP Set or Change Recurring Single Premium (RSP) | Yes | Sets / changes RSP amount and frequency |
| ILP Set/Cancel Premium Holiday | No | Ceases regular premium collection |
| ILP Set or Change Regular Withdrawal Plan | No | Sets / changes automatic withdrawal schedule |
| ILP Switch Fund Ad Hoc | Yes | Switches units between funds |

---

## Per-Item Reference

### Add Rider
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes (additional premium collected)
**Navigation:** CS Registration → select 'Add Rider' → CS Data Entry

**Prerequisites:**
- Policy status is 'Inforce'
- Premium status of main product is NOT 'Premium Waived'
- ILP only: policy does NOT have Potential Lapse Date
- ILP only: policy does NOT have miscellaneous debts
- ILP only: policy does NOT have pending fund transactions

**Key fields:**
- Commencement type: Immediately / Commencement Date / Next Due Date
- If new LA: enter new LA information separately
- Benefit Information Entry: same as NB benefit entry

**Result:** New rider displayed in Add Rider section; amount to collect generated in Collection/Refund Summary

---

### Apply Policy Loan
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes
**Navigation:** CS Registration → select 'Apply Policy Loan' → CS Data Entry

**Prerequisites:**
- Policy status is 'Inforce'
- Policy does NOT have Potential Lapse Date
- ILP only: policy has units
- ILP only: no pending fund transactions
- Policy Loan is allowed (product configuration)

**Key fields:**
- Loan Date (mandatory)
- Loan Amount (mandatory)

---

### Cancellation (Void Policy)
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes (refund of premiums paid)
**Navigation:** CS Registration → select 'Cancellation (Void Policy)' → CS Data Entry

**Prerequisites:**
- Policy has been reinstated before cancellation
- User confirmed only refund of total premium paid from last lapse date

**Key fields:**
- Effective date type: Immediately / Commencement Date
- Validity Date
- Calculate button: system calculates refund amount before Apply Change

**Business rule:** Applies when LA dies by suicide within 1 year from Date of Issue / last Reinstatement Date / effective date of any SA increase. Policy terminates; premiums refunded without interest.

**Not reversible.**

---

### Change Assignment
**Product Scope:** Both Traditional and ILP
**Financial Impact:** No
**Navigation:** CS Registration → select 'Change Assignment' → CS Data Entry

**Prerequisites:**
- Policy status is NOT terminated
- Policy does NOT have any beneficiary
- Allow Assignment = Yes in product definition for main plan

**Operations:**
- Change assignment type (Absolute / Collateral)
- Add assignee
- Delete assignee
- Change assignee information

**Not reversible.**

---

### Change Birth Date or Gender
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes (premium recalculation)
**Navigation:** CS Registration → select 'Change Birth Date or Gender' → CS Data Entry

**Prerequisites:** None stated (system validates after entry)

**Result:** Benefit Information after Change section displayed showing recalculated values.

---

### Change Beneficial Owner
**Product Scope:** Both Traditional and ILP
**Financial Impact:** No
**Navigation:** CS Registration → select 'Change Beneficial Owner' → CS Data Entry

**Operations:** Add new beneficial owner via '+' icon on Change Beneficial Owner Alteration Item section.

---

### Change Benefits
**Product Scope:** Traditional Only
**Financial Impact:** Yes
**Navigation:** CS Registration → select 'Change Benefits' → CS Data Entry

**Operations:** Select a benefit from benefit table → click Change icon → modify values in Benefit Information After Change section → Apply Change.

---

### Change Contact Information
**Product Scope:** Both Traditional and ILP
**Financial Impact:** No
**Navigation:** CS Registration → select 'Change Contact Information' → CS Data Entry

**Operations:** Select contact type to change; modify fields; Apply Change.

---

### Change Disbursement Method
**Product Scope:** Both Traditional and ILP
**Financial Impact:** No
**Navigation:** CS Registration → select 'Change Disbursement Method' → CS Data Entry

**System default rule:** System will default 'Disbursement Method' based on premium collection method when refund is generated. User can manually overwrite. This will be only valid for the current transaction and will not update back the policy-level disbursement method.

---

### Change Discount Type
**Product Scope:** Both Traditional and ILP
**Financial Impact:** No
**Navigation:** CS Registration → select 'Change Discount Type' → CS Data Entry

---

### Change HPS Exemption Information
**Product Scope:** Both Traditional and ILP
**Financial Impact:** No
**Navigation:** CS Registration → select 'Change HPS Exemption Information' → CS Data Entry

**Key field:** HPS Exemption Indicator (select from dropdown)

---

### Change Occupation
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes (loading may change)
**Navigation:** CS Registration → select 'Change Occupation' → CS Data Entry

**Triggers UW** if new occupation is higher risk than current.

---

### Change of Benefit Level (Health)
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes
**Navigation:** CS Registration → select 'Change of Benefit Level (Health)' → CS Data Entry

---

### Change Payer
**Product Scope:** Both Traditional and ILP
**Financial Impact:** No
**Navigation:** CS Registration → select 'Change Payer' → CS Data Entry

---

### Change Payment Frequency
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes (premium amount changes with frequency)
**Navigation:** CS Registration → select 'Change Payment Frequency' → CS Data Entry

**Prerequisites:**
- Traditional policies: specific conditions apply per product
- ILP policies: specific conditions apply per product

---

### Change Payment Method
**Product Scope:** Both Traditional and ILP
**Financial Impact:** No
**Navigation:** CS Registration → select 'Change Payment Method' → CS Data Entry

**Prerequisites:** Policy is NOT terminated.

**e-Submission support:** System provides API for front-end portals to submit Change Payment Method and GIRO arrangement. If STP rules pass → auto-processed. If STP fails → placed in Upcoming Transaction queue.

**Not reversible.**

---

### Change Policy Holder
**Product Scope:** Both Traditional and ILP
**Financial Impact:** No
**Not reversible.**

---

### Change Smoker Status
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes (premium recalculation)
**Prerequisites:** Policy is NOT terminated.

---

### Change Survival Benefit or Cash Bonus Option
**Product Scope:** Both Traditional and ILP
**Financial Impact:** No

---

### Change Term
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes

**Prerequisites:**
- Policy is NOT an issue-without-premium policy
- Policy is without indexation
- Policy status is 'Inforce' or 'Lapse'
- ILP: cannot have Potential Lapse Date or Projected Lapse Date

---

### Decrease Sum Assured / Partial Surrender
**Product Scope:** Traditional Only
**Financial Impact:** Yes

**Prerequisites:**
- Policy status is 'Inforce' or 'Lapse'
- ILP unit-linked: should NOT have Potential Lapse Date

---

### Delete Rider
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes (premium reduction)

**Prerequisites:**
- Policy status is 'Inforce' or 'Lapse'
- Policy must have at least one rider

---

### Freelook
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes (full premium refund)

---

### Increase Sum Assured
**Product Scope:** Traditional Only
**Financial Impact:** Yes (additional premium; UW required)

**Prerequisites:** Policy status is 'Inforce'

---

### Nomination — Beneficiary
**Product Scope:** Both Traditional and ILP
**Financial Impact:** No

**Prerequisites:**
- First-party policy: must NOT be under assignment
- Third-party policy: must be under absolute assignment; assignee must be the nominee

---

### Nomination — Trustee
**Product Scope:** Both Traditional and ILP
**Financial Impact:** No

**Prerequisites:**
- Policy is NOT assigned
- Policy is NOT an issue-without-premium policy
- Policy is NOT a third-party policy
- Policy status is NOT terminated

---

### Perform Reduced Paid Up
**Product Scope:** Traditional Only
**Financial Impact:** Yes

**Prerequisites:**
- Policy status is 'Inforce'
- Policy is without indexation
- Policy is NOT investment-linked
- Main benefit allows Reduced Paid-Up as defined in product configuration

---

### Policy Suspension
**Product Scope:** Traditional Only (and ILP per Table 3 in guide)
**Financial Impact:** No

**Prerequisites:** Policy status is 'Inforce'

---

### Premium Adjustment
**Product Scope:** Traditional Only
**Financial Impact:** Yes

**Prerequisites:**
- Policy status is 'Inforce'
- Premium status is 'Regular'

---

### Reinstatement
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes (back-premiums + interest collected)

**Prerequisites:**
- Policy status is 'Lapsed'
- Reinstatement must happen within the period defined in product after lapse date
- Health declaration typically required (UW triggered)

---

### Reversionary Bonus Surrender
**Product Scope:** Traditional Only
**Financial Impact:** Yes (partial surrender of bonus)

**Prerequisites:**
- Policy status is 'Inforce'
- Benefit allows surrender bonus only as defined in product
- CS user has registered a Reversionary Bonus Surrender application successfully

---

### Termination / Surrender
**Product Scope:** Traditional Only
**Financial Impact:** Yes (full surrender value paid)

**Prerequisites:**
- Policy status is 'Inforce' or 'Lapsed' (NOT terminated)
- Policy is NOT investment-linked (use ILP Full Surrender for ILP)

---

### Transfer of Coverage
**Product Scope:** Traditional Only
**Financial Impact:** Yes

**Prerequisites:**
- Policy status is 'Inforce'
- Main benefit: Allow Transfer Coverage = Yes in product definition
- Other party-level validations (FCC validation, same customer validation)

---

### Underwriting Review
**Product Scope:** Both Traditional and ILP
**Financial Impact:** Yes

**Prerequisites:** Policy status is 'Inforce'

---

### ILP Ad-hoc Single Premium Top-Up
**Product Scope:** ILP Only
**Financial Impact:** Yes

**Prerequisites:**
- Policy status is 'Inforce'
- Policy is investment-linked
- Policy is NOT in premium holiday
- Product is allowed for top-up (product definition)
- Policyholder age does NOT exceed pre-defined maximum age for top-up (product definition)

---

### ILP Change Investment Regular Premium
**Product Scope:** ILP Only
**Financial Impact:** No (changes investment premium amount, not sum assured)

**Prerequisites:**
- Policy status is 'Inforce'
- Policy is investment-linked
- Premium status is 'Regular'

**Warning conditions (user can click Continue to proceed):**
- Policy has miscellaneous debt
- Policy has Potential Lapse Date

---

### ILP Change Regular Premium Apportionment
**Product Scope:** ILP Only
**Financial Impact:** No

**Prerequisites:**
- Policy status is 'Inforce' or 'Lapse'
- Policy is investment-linked
- Main benefit premium status is 'Regular'

---

### ILP Decrease Sum Assured
**Product Scope:** ILP Only
**Financial Impact:** No

**Prerequisites:**
- Policy status is 'Inforce' or 'Lapse'
- Policy is investment-linked

---

### ILP Full Surrender
**Product Scope:** ILP Only
**Financial Impact:** Yes (full fund value paid; policy terminates)

**Prerequisites:**
- Policy status is 'Inforce' or 'Lapse'
- Policy is investment-linked

---

### ILP Increase Sum Assured
**Product Scope:** ILP Only
**Financial Impact:** No (SA increase via coverage change, not premium)

**Prerequisites:**
- Policy status is 'Inforce'
- Policy is investment-linked
- Policy does NOT have miscellaneous debts
- Policy does NOT have Potential Lapse Date

---

### ILP Life Replacement Option
**Product Scope:** ILP Only
**Financial Impact:** Yes

**Operations:** Replace insured life; add new insured if required.

---

### ILP Partial Withdraw
**Product Scope:** ILP Only
**Financial Impact:** Yes (fund units redeemed)

**Prerequisites:**
- Policy status is 'Inforce'
- Policy is investment-linked
- Product is allowed for partial withdrawal (product definition)

**Withdraw methods:** By Units / By Value (both support Dual Accounts)

---

### ILP Set or Change Recurring Single Premium (RSP)
**Product Scope:** ILP Only
**Financial Impact:** Yes

**Prerequisites:**
- Policy status is 'Inforce'
- Policy is investment-linked
- Policy is NOT frozen by other CS or Claim transaction
- Main benefit is allowed to have RSP in Product Configuration
- No pending fund transaction under the policy
- Policy is NOT within Premium Holiday Period (PH Indicator ≠ Yes)

**Key fields:**
- RSP Amount
- Payment Frequency
- RSP Next Due Date (system-calculated for new RSP = Start Date)
- Start Date

**Navigation:** Customer Service > Registration (separate registration screen for RSP)

---

### ILP Set/Cancel Premium Holiday
**Product Scope:** ILP Only
**Financial Impact:** No

**Prerequisites:**
- Policy status is 'Inforce'
- Policy premium status is 'Regular'
- Policy is an ILP policy
- Policy is NOT suspended by other transactions
- Product allows premium holiday = Yes (product definition)
- Premium Due Date ≥ Commencement Date + Premium Holiday Start Months (product-configured)

**Warning conditions (user can click Continue to proceed):**
- Policy has Potential Lapse Date
- Policy has Projected Lapse Date

---

### ILP Set or Change Regular Withdrawal Plan
**Product Scope:** ILP Only
**Financial Impact:** No (sets up automatic future withdrawals)

---

### ILP Switch Fund Ad Hoc
**Product Scope:** ILP Only
**Financial Impact:** Yes (fund units moved)

**Prerequisites:**
- Policy status is 'Inforce'
- Policy is investment-linked

**Switch methods:** By Units / By Value / By Percent

---

## CS Application Status Reference

| Status | When Set |
|---|---|
| Pending Data Entry | CS registered |
| Processing in Progress | Processor accesses CS application |
| Pending Underwriting | CS submitted for UW |
| Underwriting in Progress | Underwriter accesses UW task |
| Completed | UW accepted (standard) + no approval + no pending collection |
| Pending UW Confirmation | UW accepted with loading + no approval + no pending collection |
| Disposing Underwriting Decision | Processor accesses application post-UW |
| Re-Underwriting | Processor sends back to UW |
| Pending Approve | UW accepted + need approval + no pending collection |
| Approving | Approver accesses approval task |
| Approved | Approver approves + collection required |
| Back Entry | Approval returned to processor |
| Rejected | Processor rejects transaction |
| Canceled | Processor cancels transaction |
| Undo | Processor reverses completed transaction |

---

## Reverse Alteration

**Purpose:** Undo a completed alteration (client request or human error)

**Prerequisites:**
- Application status is 'Inforce'
- Policy is NOT frozen

**Alterations that CANNOT be reversed:**
- Claim Acceptance
- Change Policy Holder
- Change Beneficiary
- Change Assignment
- Change Payment Method
- Reversal (cannot reverse a reversal)

**Navigation:** Customer Service > Reversal → search by policy number → select transaction → select reversal reason → Submit

**Note:** If transaction has confirmed payment, user must cancel payment first before reversal.

---

## Task Assignment Configuration

| Task | Sale Channel | VIP Customer | User Role | Assignment Strategy | Max Count |
|---|---|---|---|---|---|
| CS Entry | $ALL$ | $ALL$ | $ALL$ | 1-Push | 9999 |
| CS Waiting Force | $ALL$ | $ALL$ | $ALL$ | 2-Pull | 9999 |
| CS Waiting UW | $ALL$ | $ALL$ | $ALL$ | 2-Pull | 9999 |
| CS Approve | $ALL$ | $ALL$ | $ALL$ | 1-Push | 9999 |

Assignment strategies:
- **Push (1-Push):** Task auto-assigned to specific user when created
- **Pull (2-Pull):** Task placed in pool; user claims from pool

---

## CS Registration Field Reference

| Field | Description | Default |
|---|---|---|
| Policy No. | Policy number to be altered | — (mandatory) |
| Branch Received | Branch handling the request | Login user's branch (editable) |
| Touch Point | Channel through which request received | CS Counter (editable) |
| Application Date | Effective date at application level | Current system date |
| Policy Alteration Item | One or more items to be altered | — (mandatory; sorted A–Z) |
| Document Type | Document submission status | Yes / No |
| Register Comment | Free-text comment for registration | — (optional) |

Touch Point options: Telephone / Email / Mail / Agent Counter / CS Counter / Web Service / Fax / Letter / Dropbox

---

## CS Application Entry Field Reference (Common Sections)

### Application Info Area
| Field | Description |
|---|---|
| Application No. | Hyperlink to access data entry UI |
| Policy No. | Policy being altered |
| Product Code | Main product code |
| Linked Policy No. | For bundled policy: linked policy number |
| New Image Upload | Flag if new document image uploaded but unmapped to CS transaction |

### Policy Info Area
| Field | Description |
|---|---|
| Application Status | Current workflow status (see status reference above) |
| Requirement Letter Status | Latest requirement letter status (printed / to be printed / replied) |
| Registration Date | Date CS application was registered |
| TAT (Days) | Turnaround time: registration date to system date |
| Policy Holder Name | Name of policy holder |
| CS Auto Cancellation Date | Auto-set by system or manually set by user |

### Collection / Refund Summary Section
Displays fee changes per alteration item and product.
If premium refund generated: system defaults disbursement method based on premium collection method.
User can manually overwrite disbursement method for the current transaction only (does not update policy-level record).

### Generate Letter Field
| Value | Behaviour |
|---|---|
| Yes | System generates PS endorsement letter data after PS inforce |
| No | System does NOT generate PS letter data after PS inforce |
Default: No. User can change during CS Entry. Read-only during CS Approval.

---

## e-Submission API Support

System provides API for front-end portals to submit the following changes without going through full CS workflow:

| Function | API Capability |
|---|---|
| Make premium payment | Query outstanding billing; update payment status |
| Change payment method | Query eligible policies; validate STP rules; submit change |
| GIRO arrangement | Query eligible policies; submit arrangement |

**STP processing:**
- If e-submission passes STP rules → auto-processed; query via CS > Query
- If e-submission fails STP rules (e.g. policy suspended) → placed in CS > Upcoming Transaction queue; can be viewed or cancelled

---

## Policy Servicing Quotation

**Purpose:** Calculate and preview the financial impact of a reinstatement or other alteration before committing.

**Navigation:** Customer Service > Policy Servicing Quotation

**Steps:**
1. Select Quotation Type and enter Policy No. (both mandatory)
2. System displays policy data in Policy Information Section
3. Enter Validity Date → system enables [Calculate] button
4. System calculates reinstatement amounts and displays results per section

---

## Config Gaps Commonly Encountered in CS

| Scenario | Gap Type | Config Location |
|---|---|---|
| Need UW = Y/N per alteration item | Config Gap | CS Workflow Configuration → Need UW per item |
| Need Approval = Y/N per alteration item | Config Gap | CS Workflow Configuration → Need Approval per item |
| Allow product to have RSP | Config Gap | Product Factory → ILP Rules → RSP Allowed |
| Premium Holiday Start Months | Config Gap | Product Factory → ILP Rules → PH Start Month |
| Allow partial withdrawal | Config Gap | Product Factory → ILP Rules → Partial Withdrawal |
| Allow top-up | Config Gap | Product Factory → ILP Rules → Top-Up Allowed |
| Max age for top-up | Config Gap | Product Factory → ILP Rules → Top-Up Max Age |
| Allow reduced paid-up | Config Gap | Product Factory → Traditional Rules → Allow RPU |
| Allow transfer of coverage | Config Gap | Product Factory → Traditional Rules → Allow Transfer Coverage |
| Allow policy loan | Config Gap | Product Factory → Loan Rules → Policy Loan Allowed |
| Task assignment strategy per CS task | Config Gap | CS Assignment Strategy Configuration table |
| Touch Point options available | Config Gap | CS → Touch Point Config |
| Document checklist per alteration item | Config Gap | CS → Document Checklist Config |

---

## Shield Policy CS (from CS Shield UG V25.04)

### Shield-Specific CS Workflow
Shield policies (Singapore/HK government schemes) have modified CS flow:

1. CS Registration: Shield product code validation
2. Customer matching: CPF account verification required
3. UW: Medical board referral for sum >= threshold
4. In-force: Auto-triggered on premium receipt + UW approval

### Shield CS Screens
| Screen | Path | Notes |
|---|---|---|
| Shield NB Registration | New Business > Registration > Shield Tab | CPF account mandatory |
| Shield CS Alteration | Customer Service > Shield Policy Alteration | SA increase requires re-UW |
| Shield Surrender | Customer Service > Surrender > Shield | CPF return calculation applies |


## ILP CS Items (from CS ILP UG V25.04)

### ILP-Specific CS Items
| CS Item | Description | Screen Path |
|---|---|---|
| ILP Fund Switch | Switch between funds | Customer Service > Fund Switch |
| ILP Top-up | Add additional premium to fund | Customer Service > Top-up |
| ILP Partial Surrender | Partial withdrawal from fund value | Customer Service > Partial Surrender |
| ILP Full Surrender | Full fund redemption | Customer Service > Surrender |
| ILP RSP Change | Modify Regular Savings Plan amount | Customer Service > RSP Change |
| ILP Fund Reallocation | Change fund allocation percentages | Customer Service > Fund Reallocation |



## LTC Policy CS (from CS LTC UG V25.04)

### LTC-Specific CS Workflow
LTC (Long-Term Care) policies have modified CS flow:

1. CS Registration: LTC product code validation
2. Disability assessment: Triggered on claim
3. Benefit payment: Monthly disbursement while disabled

### LTC CS Screens
| Screen | Path | Notes |
|---|---|---|
| LTC NB Registration | New Business > Registration > LTC Tab | Health declaration mandatory |
| LTC Disability Claim | Claims > LTC Disability Claim | Medical assessment required |
| LTC Benefit Payment | Claims > LTC Benefit Payment | Monthly auto-trigger |


## CS Alteration Items (from CS Traditional UG V25.04)

### Alteration Types
| Alteration | Description | Screen Path |
|---|---|---|
| SA Increase | Increase sum assured | Customer Service > SA Increase |
| SA Decrease | Decrease sum assured | Customer Service > SA Decrease |
| Premium Mode Change | Change payment frequency | Customer Service > Mode Change |
| Fund Switch | ILP only: change fund allocation | Customer Service > Fund Switch |
| Rider Add | Add new rider to existing policy | Customer Service > Rider Add |
| Rider Remove | Remove rider (not allowed for some products) | Customer Service > Rider Remove |
| Policy Reinstatement | Reinstate lapsed policy | Customer Service > Reinstatement |
| Change of Payer | Change premium payer | Customer Service > Change Payer |
| Change of Beneficiary | Update nomination | Customer Service > Nominee Change |



## Surrender Rules (from CS Traditional UG V25.04)

### Surrender Triggers
| Scenario | System Behaviour |
|---|---|
| Policy in force | Surrender value = SV (fund value for ILP) |
| ILP policy | Surrender value = Units x NAV - Surrender Charge |
| Traditional policy | Surrender value = Accumulated Paid-Up Value - Outstanding loans |
| Surrender during free-look | Full premium refund |
| Surrender within 1 year | Surrender charge applies per product table |

### Surrender Charge
| Surrender Year | Charge (% of SV) |
|---|---|
| Year 1 | Product-defined (typically 5-10%) |
| Year 2 | Product-defined (typically 3-5%) |
| Year 3+ | Product-defined |


## Policy Loan (from CS Traditional UG V25.04)

### Loan Rules
| Rule | Description |
|---|---|
| Max Loan % | Typically 80-90% of SV/Cash Value |
| Interest Rate | Per product/company config |
| Loan Repayment | Via GIRO or manual payment |
| Outstanding Loan | Deducted from death benefit |
| Outstanding Loan | Deducted from surrender value |
| Loan > SV | System blocks: loan cannot exceed SV |


## Reinstatement (from CS Traditional UG V25.04)

### Reinstatement Rules
| Condition | Rule |
|---|---|
| Time limit | Lapse date + 1 year (product-specific) |
| Outstanding premium | Must pay all arrears |
| Interest on arrears | Calculated per product rate table |
| UW re-evaluation | Required if lapse > 60/90 days |
| Loan reinstatement | Outstanding loan must be repaid or reinstated |
| ILP reinstatement | Fund value + arrears + charges |


## Policy Servicing Quotation (from CS UG)

CS can generate on-demand quotations for:
- Revised SA illustration
- Revised premium projection
- Surrender value projection
- Loan eligibility estimate

Quotations are NOT policy contracts — for reference only.


## FATCA Information (from CS UG V25.04)

FATCA compliance fields captured in CS:
- FATCA Status: Individual / Entity / Passive Non-Financial Foreign Entity
- GIIN (for entities)
- W-8BEN / W-9 forms (US tax status)
- TIN (Tax Identification Number)

Referenced from: ps-regulatory.md for FATCA rules.


## CS Watch List Operations (from CS UG)

### Watch List Actions
| Action | Description |
|---|---|
| Release | Return task to shared pool |
| Reassign (Push) | Manually assign to specific user |
| Reassign (Auto) | Assign by task auto-assign strategy |
| Export | Download task list to Excel |



## CS Rejection & Cancellation (from CS UG)

| Action | Condition | Outcome |
|---|---|---|
| Reject CS Application | Missing compulsory info | Task returned to originator |
| Cancel CS Application | Client request before inforce | No financial impact |
| Reverse Alteration | Error in completed CS | Reverts to prior state |


## INVARIANT Declarations (CS Module)

The following system constraints apply across all CS transactions:

```
INVARIANT 1: CS alteration cannot proceed if policy is frozen by another CS or Claim transaction
  Enforced at: CS Registration + CS Data Entry → Apply Change
  Error if violated: System displays "Policy is frozen" error; blocks alteration item

INVARIANT 2: ILP alterations require policy to be investment-linked
  Enforced at: CS Registration → alteration item selection
  Error if violated: ILP-only items hidden or disabled for non-ILP policies

INVARIANT 3: Financial impact alterations generate Collection/Refund Summary entry
  Enforced at: CS Data Entry → Apply Change
  Effect: Amount to Collect or Refund calculated; must be settled before In-Force

INVARIANT 4: Rider_Term ≤ Base_Policy_Term on Add Rider
  Enforced at: CS Data Entry → Add Rider → Apply Change
  Error if violated: System validation error; blocks Apply Change
```

---

## ⚠️ Limitations & Unsupported Scenarios

> This section documents known limitations and scenarios NOT supported by the system. Updated: 2026-03-14

### Nomination & Beneficiary

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Change Beneficiary | Only supports **individual** beneficiaries | Code | Corporate/Legal entity not supported |
| Change Beneficiary | Maximum number of beneficiaries per policy: **TBC** | Unknown | Requires testing/verification |
| Change Trustee | Only supports **individual** trustees | Code | Corporate trustee not supported |
| Nomination (General) | Policy must NOT be under assignment (absolute) | Config | Prerequisite in ps-cs |

### Policy Financial Alterations

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Policy Loan | Only available for Whole Life / Endowment products | Code | ILP/Investment-linked not supported |
| APL (Auto Premium Loan) | Only for regular premium policies | Code | Single premium policies excluded |
| Reduced Paid-Up (RPU) | Traditional products only | Code | ILP not supported |
| Top-up | May have product-specific limits | Config | Check ps-product-factory |

### General Limitations

| Limitation | Type | Workaround |
|------------|------|------------|
| Reversal: Change Beneficiary cannot be reversed | Code | Manual correction required |
| Reversal: Change PH cannot be reversed | Code | Manual correction required |
| Financial alterations require full settlement before Apply Change | Workflow | Cannot split transactions |

---

## Related Files

| File | Purpose |
|---|---|
| `insuremo-ootb-full.md` | CS OOTB capability classification (use for Gap Analysis) |
| `ps-product-factory.md` | Product Factory config for product-level CS rules (RSP, loan, RPU flags) |
| `output-templates.md` | BSD output templates for CS-related gaps |
