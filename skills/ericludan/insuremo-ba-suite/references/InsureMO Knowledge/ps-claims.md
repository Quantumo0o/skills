# InsureMO Platform Guide — Claims
# Source: Claims User Guide V24.05 (2024-09-05)
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb.md instead
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"how does Claims work in InsureMO"** — workflow stages, prerequisites, navigation paths, field behaviour, system rules, and business logic for each step of the claims process.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for a Claims-related gap
- Agent 6 is generating a **Config Runbook** for Claims configuration items
- A BA needs to verify what **system-enforced conditions** apply before classifying a requirement as Dev Gap

---

## Module Overview

```
Claims Module
│
├── Standard Claims
│   ├── Case Registration          ← FNOL entry, case number generation
│   ├── Case Acceptance            ← Auto or Manual acceptance, product selection
│   ├── Case Evaluation            ← TPD/Death / Medical / Waiver evaluation, liability compute
│   ├── Make Disbursement Plan     ← Lump Sum or Installment, payee selection
│   └── Case Approval              ← Auto or Manual approval, settlement
│
├── Fast Claims                    ← Medical / micro / self-registration; auto-approved by default
│
├── Sub-Tasks (available at multiple stages)
│   ├── Document List
│   ├── Query Letter
│   ├── Medical Bill Entry
│   ├── Escalation
│   └── Underwriting (during Evaluation)
│
└── Advanced Functions
    ├── Claims Watch List          ← Task reassignment
    ├── Change Disbursement Plan   ← Post-approval installment changes
    ├── Cancel a Case
    ├── Reverse Case
    ├── Claims Query
    ├── Copy Case
    ├── Add Insured for Claim
    └── Medical Report Fee Payment (Create / Reverse Medical Billing)
```

---

## Claims Workflow — Standard Sequence

```
Case Registration
  └─► Case Acceptance (Auto or Manual)
        └─► Case Evaluation
              ├─► Make Disbursement Plan
              └─► Case Approval (Auto or Manual)
                    └─► Case Settled
```

### Standard Claim Types
- **Normal Claim:** Registration → Acceptance → Evaluation → Approval (none can be skipped)
- **Auto Acceptance and Auto Approval Claim:** Same as Normal Claim but Acceptance or Approval steps can be performed automatically based on configured rules

### Fast Claims
Typically for medical claims, micro products, or customer self-registration cases. Registration and Acceptance are completed by the front end; system directs to Evaluation. Usually auto-approved; configurable random manual approval rules can be set.

---

## Menu Navigation

| Action | Path |
|---|---|
| Register a claim case | Claims > Registration |
| Claims work list (all stages) | Claims > Work List |
| Claims watch list (reassign tasks) | Claims > Watch List |
| Change Disbursement Plan | Claims > Change Disbursement Plan |
| Cancel a Case | Claims > Cancel Case |
| Reverse a Case | Claims > Reverse Case |
| Query claim case | Claims > Query |
| Copy a Case | Claims > Copy Case |
| Add Insured for Claim | Claim > Add Insured for Claim |
| Create Medical Billing | Claim > Medical Billing > Create Medical Billing |
| Reverse Medical Billing | Claim > Medical Billing > Reverse Medical Billing |

---

## Case Status Reference

| Status | Stage |
|---|---|
| Pending | Registration — case pended before submission |
| Waiting for Acceptance | After registration submitted |
| Acceptance in Progress | Acceptance user has opened the case |
| Pend at Acceptance | Case pended at acceptance stage |
| Waiting for Evaluation | Acceptance complete |
| Evaluation in Progress | Evaluation user has opened the case |
| Waiting for Escalation | Escalation submitted at evaluation |
| Escalated | Escalation responded |
| Waiting for Reply | Query letter sent, awaiting reply |
| Waiting for Approval | Evaluation submitted |
| Approval in Progress | Approval user has opened the case |
| Settled | Case approved and payment generated |
| Cancelled | Case cancelled at any stage before settlement |
| Withdrawn | Case withdrawn at Acceptance or later stages |
| Void | Case reversed after settlement |

---

## Part 1 — Case Registration

**Purpose:** Register basic claim information when a customer reports a claim event.
**Navigation:** Claims > Registration
**Also supports:** Submitting claim applications electronically from front-end systems (e.g. customer portal)

### Prerequisites
- Customer reports a claim event

### Steps
1. Claims > Registration → Customer Search page
2. Search by insured name, ID no., or policy no. (Quick Search or Advance Search)
3. Select target record → Submit → Case Registration page
4. Enter Claim Information and Reporter Information; add General Comments if needed
5. Click **Submit** to submit (system auto-generates claim case number) OR **Pend** to suspend
6. After registration: click **Register Another Case** to redo, or **Exit** to return to worklist
7. Click **Next** to proceed to Case Acceptance stage

### Case Number Generation Rule
Format: `XXXYYYY00001`
- `XXX` = DescAbbr configured in TClaimType table by claim type (e.g. DTH = Death, CIC = Critical Illness, MED = Medical)
- `YYYY` = claim submission year
- `00001` = running sequence number

### Claim Type DescAbbr Reference

| Claim Type | Type Code | DescAbbr |
|---|---|---|
| Death | 1 | DTH |
| Total and Permanent Disability | 2 | TPD |
| Terminal Illness | 3 | TIC |
| Critical Illness | 4 | CIC |
| Medical | 7 | MED |
| Maternity | 6 | MAT |
| Pay Care | 10 | PCC |
| Waiver | 8 | PWC |
| Long Term Care | 9 | LTC |
| Others | 5 | OTH |
| Accident | 11 | ACC |

### Duplicate Case Rule
When clicking Submit: if another case exists with the same Event Date + Life Assured + Type of Claim, system prompts: *"Similar case exists in the system! Do you want to save this case?"* — click OK to proceed or Cancel to abort.

### Registration Field Reference

| Field | Description | Rules |
|---|---|---|
| Policy No. | Policy number of customer | Search key |
| Insured Name | Name of Life Assured | Search key |
| Gender | Gender of Life Assured | Options: Female / Male / Unknown |
| ID Type | Party ID type (e.g. Passport) | — |
| ID Number | Party ID number | — |
| Event Date | Date the claim event occurred | Must be ≤ system date; updatable at Acceptance stage |
| Event Details | Description of incident | Free text |
| Claim Nature | Nature of claim event | Options: Illness / Accident / Suicide |
| Type of Claim | Claim type | Select from configured list (Death, Medical, etc.) |
| Case Classification | Classification of case | Options: New Claim / Further Claim / Adjustment / Special / Appeal / (configurable via code table) |
| Original Case No. | Reference to original case | Mandatory if Case Classification = Appeal |
| Notification Date | Date insurer notified | Default = system date; updatable |

---

## Part 2 — Case Acceptance

### Auto Acceptance

System accepts automatically when ALL of the following conditions are met (configurable):
- Claim Nature is selected
- Event Date is entered
- Submit Channel = Manual Registration
- Case Type = Medical
- Case Classification = New Claim
- Policy status is In-Force on event day
- Policy is NOT suspended by CS or blocked by other claims
- No similar case validation check exists
- Product status is In-Force on event day
- Liability of the product is within the liability covered by this claim type

If any condition fails → Manual Acceptance required.

**Auto Acceptance sequence:**
1. System checks auto acceptance validity
2. System updates claim policy and product information
3. System books claim reserve for the case
4. System updates acceptance decision to Accept → proceeds to Case Evaluation

### Manual Acceptance

**Prerequisites:** Case status = Waiting for Acceptance / Acceptance in Progress / Pend at Acceptance

**Navigation:** Claims > Work List → click Case No. → Case Acceptance Entry page

**Steps:**
1. Case Acceptance Entry page — update Claim Info if necessary
   - For Medical Claim: enter Hospital Code from dropdown
   - If diagnosis code needed: click Diagnosis Code → fuzzy search by code or description
2. Update Claimant Info if necessary
3. Click **Next** → Acceptance Decision page (displays all policies of the Life Assured)
4. Click policy hyperlink → Acceptance Policy page → set **Accept Product** indicator to Y for accepted products → Save
5. Click Back → Acceptance Decision page
6. From Acceptance Decision, optional sub-tasks:
   - Click **Escalation** if case needs escalation
   - Click **Document List** to manage documents
   - Click **Query Letters** if more documents/signature/compliance form needed
   - Click **Medical Bill** if medical case (view/create medical bill)
7. Select from **Acceptance Decision** dropdown:
   - **Accept** → proceed to submission
   - **Cancel** → select Cancel Reason → Submit → case status = Cancelled
   - **Pend** → Submit → case status = Pend at Acceptance
   - **Withdrawn** → select withdraw reason → Submit → case status = Withdrawn at Acceptance
8. Click **Submit** → if valid: case status → Waiting for Evaluation; if invalid: return to step 1

### Policy / Product Acceptance Rules

Products/Policies that **CANNOT be accepted** (any of these conditions):
- Policy is Frozen by CS or CLM
- Insured on policy differs from case's insured
- Product has no liability mapped with the claim type
- Case Classification ≠ Special AND product status at event date = Terminated
- Case Classification ≠ Special AND product status at event date = Lapsed AND event date > lapse date + grace period
- Event date < Risk Commencement Date OR Event date > Coverage end date
- Commencement date is blank OR Coverage end date is blank

### Policy Lock (Freeze) Indicator by Claim Type

| Claim Type | LockPolicyIndi | EditLockPolicy |
|---|---|---|
| Death (DTH) | Y | N |
| TPD | N | Y |
| Terminal Illness | — | — |
| Critical Illness | — | — |
| Medical (MED) | N | N |
| Maternity | — | — |
| Pay Care | — | — |
| Waiver | — | — |
| Long Term Care (LTC) | N | N |
| Others (OTH) | N | N |
| Accident (ACC) | N | N |

### Diagnosis Code Rules
- System supports effective date and end date per diagnosis code version
- At acceptance, system compares claim event date with effective/end date of diagnosis code version; displays the matching version
- Warning displayed if Diagnosis Code is null upon acceptance entry submit (all claim types)

### Acceptance Submission Validation (on Submit in Acceptance Summary)

| Condition | System Action |
|---|---|
| Policy has outstanding premium | Warning message |
| Required document with Completeness ≠ Y AND Waive ≠ N | Warning: "There is uncompleted required document. Please confirm to continue?" |
| Medical claim with no medical bill entered | Warning: "No medical bill information entered. Please confirm." |
| Query letter not replied | Error: "Query letter is not replied." |
| Price Effective Date ≠ Notification Date or Notification Date + 1 working day | Error: "Invalid Price Effective Date." |
| Accepted policies with different policy currencies | Warning |
| Accepted policies with different policy owner/service agent | Warning (policy owners = policyholder, assignee, or trustee) |

### Acceptance Field Reference

| Field | Description |
|---|---|
| Claim Info section | Updatable claim information; hospital code for medical claims |
| Claimant Info section | Claimant details |
| Acceptance Decision | Accept / Cancel / Pend / Withdrawn |
| Notified Amount | Displayed per accepted product; updatable |
| Accept Product indicator | Y = accepted; set per product on Acceptance Policy page |

---

## Part 3 — Case Evaluation

### Evaluation Workflow
Three evaluation types, each with its own sub-process:
1. **Evaluate TPD or Death Claims**
2. **Evaluate Medical Claims**
3. **Evaluate Waive Claims**

### Prerequisites
Case status = Waiting for Evaluation (reached after Acceptance)

### Navigation
Claims > Work List → click Case No. → Case Evaluation page

### Check Claim Information (Common First Step)
On Case Summary of Evaluation page:
- Click **Edit Info** to update case information
- Click **Medical Bill** (Medical claims) to view/update medical fee bill
- Click **Document List** to view documents
- Click **Query Letters** to send query letter
- Click **Underwriting** to send to UW workbench

### Evaluate TPD or Death Claims

1. Case Evaluation-Policy page: view policy info, accepted products, policy payment summary
   - Click **Evaluate More Products** to accept additional products (e.g. terminate main product when evaluating accelerated rider)
2. Click accepted product
3. Under **Liability Evaluation** area: select liability checkboxes
   - Liabilities sorted by configured sequence (regardless of product code)
4. Click **Compute** → calculates:
   - **Evaluation Payment** = amount calculated by configured claim formula
   - **Claimed Payment** = amount after configured claim Accutors (accumulators)
   - User can adjust **Actual Payment** amount
5. (Optional) Click Claimed amount hyperlink → view detailed Accumulator information
6. (Optional) Click Remaining Limit hyperlink → view accumulator history
7. If product payment adjustment needed: update **Payment Amount** in Product Adjustment section + add Remarks
   - Adjustment items (SB, CB, TB, RB, IB) at product level: user manually inputs adjusted amount; system generates receivable/payable for GL
   - **Survival Benefit Clawback**: system defaults to sum of SB with due date paid after event date; user can adjust; system generates separate fee record
   - Warning if SB allocated after event date was used to repay policy loan/APL
   - Bonus (RB, TB, SB, CB) calculated at product level
8. Select **Claim Decision**:
   - **Admit** — admit product evaluation
   - **Ex-gratia-Full** — permit by ex-gratia full
   - **Ex-gratia-Partial** — permit by ex-gratia partial (adjust payment amount)
   - **Repudiate** — repudiate; total product payment = 0; if reason = "Reject - Others", allow detailed reason text
   - **Cancel** — cancel product
   - **Withdrawn** — withdraw product (select reason)
   - **Denied & Rescind with refund** — void policy/product; Trad: auto-refund total paid premium from commencement/reinstatement date (later); ILP: auto-refund TIV
9. Click **Save** → Policy Payment Summary updated
   - Update **Premium Collect To** date → system auto re-computes refund and outstanding premium
   - **Premium Collection To** defaults: for Death/TPD/CI → next anniversary after event date (termination or not); for other claim types → no outstanding premium deducted
   - LAAR warning: if evaluated product has LAAR Indicator = Yes and total actual payment ≥ inforce SA at event date
10. (Optional) Escalation if needed
11. Go to Benefit Amount Allocation → Make Disbursement Plan
12. Click **Submit** → proceeds to Claim Approval

### Evaluate Medical Claims

Steps 1–3: same as TPD/Death except Medical Bill Auto Select is available
- Click **Auto Select**: system auto-selects liabilities based on input medical bills; evaluation sequence set by predefined sequence in Product Factory

Steps 4–8: same as TPD/Death

Step 9 — Additional: (Optional) Adjust Reimbursable
- Click **Adjust Reimbursable** → Medical Bill Allocation page → adjust claimed medical bill amount in Inpatient/Outpatient sections

Step 10: If product terminated → update Premium Collect to date; OS and refund premium recalculated

Steps 11–15: same as TPD/Death

### Evaluate Waive Claims

Key difference in step 8 (Waiver-specific decisions):
- Set **Premium Waive** = Yes for waiver products
- **Waiver Inforce:**
  - Waiver Start Date defaults to NDD after event date
  - Waiver End Date defaults to premium end date of waived product
  - For waiver benefit itself: waiver end = min(waived product premium end date, waiver premium end date)
  - User can update both dates; updates to both waived product and waiver
- **Waiver Terminated:**
  - Waiver Start Date defaults to NDD after event date
  - Waiver End Date defaults to premium end date of waived product
- For product with waiver liability (not a separate waiver benefit): waiver start/end based on evaluated product; product's own premium is waived

### ILP Evaluation Rules

| Condition | Evaluation Rule |
|---|---|
| Global param: sell all fund at acceptance = N; formula = MAX(Inforce SA, TIV); TIV at Admission > SA | Evaluation Amount = 0 |
| Global param: sell all fund at acceptance = N; formula = MAX(Inforce SA, TIV); TIV at Admission < SA | Evaluation Amount = Inforce SA - TIV at Admission |
| Global param: sell all fund at acceptance = N; formula = Inforce SA + TIV | Evaluation Amount = Inforce SA |
| Global param: sell all fund at acceptance = N | TIV Payable = Units at Event Date × Price at Admission Price Effective Date + Saving Account Value at Admission; not updatable; displayed only when TIV at Admission > 0 |
| Global param: sell all fund at acceptance = Y | TIV for evaluation = calculated from pending fund transactions with available price; evaluation amount excludes TIV |

**Abnormal Settlement Rate:** default = guaranteed rate; user can modify.

### Evaluation Submission Validation (on Submit in Case Evaluation)

| Condition | System Action |
|---|---|
| Total Payment Amount by Claim Type / Claim Decision exceeds claim officer's authority | Error |
| UW request not responded | Blocked |
| Escalation to investigator/officer not responded | Blocked |
| Query letter not replied | Error: "Query letter is not replied." |
| Disbursement Amount ≠ Allocated Disbursement Amount for any policy | Error |
| Not all policies under case have been evaluated | Blocked |
| Case information updated after products evaluated | Must re-evaluate before submitting |
| Admission Price Effective Date updated after ILP product evaluated | Must re-evaluate all ILP products |
| Required document with Completeness ≠ Y AND Waive ≠ N | Warning: "There is uncompleted required document. Please confirm to continue?" |
| CI claim with ongoing TPD claim (unpaid installments) on same policy | Warning |

---

## Part 4 — Make Disbursement Plan

**Purpose:** Allocate claim benefit amount to beneficiaries or other payees.
**When:** After evaluation, under Benefit Amount Allocation section of Case Summary page
**Available payment types:** Lump Sum / Installment

### System Default Payee Rules

**Death Claims:**

| Condition | Default Payee |
|---|---|
| No assignee, trustee, or beneficiary nominee | Policyholder (3rd party policy) / No default (1st party policy) |
| No assignee or trustee; beneficiary nominee(s) exist | Nominees by share percentage |
| Assignee only (absolute / collateral / official) | Assignee |
| Trustee(s) (with or without nominees) | Trustee(s) without share percentage; user selects one for payout |

**Non-Death Claims:**

| Condition | Default Payee |
|---|---|
| No assignee, trustee, or beneficiary nominee | Policyholder (both 1st and 3rd party policy) |
| No assignee or trustee; beneficiary nominee(s) exist | Nominees by share percentage |
| Assignee only (absolute / collateral / official) | Assignee |
| Trustee(s) (with or without nominees) | Trustee(s) without share percentage; user selects one for payout |

**Note:**
- 1st party policy = Policyholder is the same person as Life Insured
- 3rd party policy = Policyholder is different from Life Insured
- Trustee can co-exist with beneficiary nominee
- Assignee CANNOT co-exist with beneficiary nominee
- Assignee and Trustee CANNOT co-exist

### Lump Sum Disbursement Steps
1. Click **+ Lump Sum**
2. Select payee (search existing customer / select from default payee list / Add New Customer)
3. Select Payment Method; enter payment currency and payment information
   - Direct Credit: enter account number manually or search existing
   - Direct Debit: enter account number manually
4. Input Disbursement Percentage or Amount
5. (Optional) Pending = Yes + Remark if pending this plan
6. Click **Save**

### Installment Disbursement Steps
1. Click **+ Installment**
2. Select payee; select Payment Method; enter payment information
3. Input Disbursement Percentage or Amount
4. (Optional) Pending Payment = Yes + Remark
5. Under **Installment Information**: enter mandatory fields → click **Auto-Generate**
   → System generates installment plan; displays in Installment Details section
6. In **Installment Details**: change **Pending** indicator to N for installments to be paid in this claim (others paid after settlement)
7. (Optional) Add / Edit / Delete individual installments via buttons in Installment Details
8. Click **Save**

### Disbursement Submission Validation

| Condition | System Action |
|---|---|
| Mandatory fields missing | Error |
| Benefit amount exceeds balance amount | Error |
| Payment method = Transfer to Policy; policy number not in system | Error |
| Payment method = Internal Transfer; policy status = Terminated | Error |
| Payee's country of valid address or nationalities trigger overseas payment (Telegraphic Transfer) | Warning |
| Payee's bankruptcy indicator = Yes | Warning |

### Installment Plan Field Reference

| Field | Allowed Values | Description |
|---|---|---|
| Installment Type | TPD / AETPD / ETPD / LTC / Paycare / Other | Type of installment |
| Net Benefit Amount | Amount | Total payment in pay currency |
| Start Date | Date | Date of initial installment payment |
| Frequency | Yearly / Half Yearly / Quarterly / Monthly | Default = Yearly if Installment Type = TPD |
| Amount Per Time | Amount | Amount per installment |
| Times Pay-Off | Integer | Number of installments |
| Increase Inst By (%) | ≤ 999.99 | Required for TPD on ETPD/AETPD accelerated option only |
| Pending | Yes / No | Whether to pend this installment |
| Review Date | Date | Mandatory when Pending = Yes |

---

## Part 5 — Case Approval

### Auto Approval

System approves automatically when ALL of the following conditions are met (configurable):
- Type of Claim = Medical
- Case Classification = New Claim
- Total payment amount ≤ 1,000.00
- No manual adjustment on product evaluation amount
- No product terminated
- No adjustment on claim payment at policy level
- Case Evaluation decision = Admit

If any condition fails → Manual Approval required.

**Auto Approval sequence:**
1. System checks auto-approval validity; if valid → auto-approves
2. System updates claim policy and product information
3. System updates case status to Settled
4. System generates relevant claim payment records
5. System generates claim settlement letter
6. System generates SMS notification → sends to claimant and agent via third party

### Manual Approval

**Prerequisites:** Case status = Waiting for Approval / Approval in Progress / Waiting for Escalation / Escalated / Waiting for Reply

**Navigation:** Claims > Work List → click Case No. → Case Approval page

**Steps:**
1. Select from **Approval Decision** dropdown:
   - **Agree** — accept the claim case
   - **Reject** — reject the case
2. Click **Submit** → system:
   - Checks claim decision; updates case status accordingly
   - Generates claim settlement letter
   - Generates claim payment record; all claim accounting transactions posted to financial transaction history table

### Approval Rules

1. Warning messages and conditions are configurable (conditions: liability ID/name, main plan, rider, claim type)
2. Claim officer can only pick up cases where total claim amount is within their authority limitation
   - Total claim amount INCLUDES premium waived amount of all evaluated products when decision ≠ Repudiate/Cancel/Withdrawn
   - Total claim amount EXCLUDES premium waived amount when decision = Repudiate/Cancel/Withdrawn
3. After approval, system updates:

**Product Termination Rules:**
- Updates evaluated product status to Terminated
- If Product In Force = No AND Product = Main Plan → policy status = Terminated; all riders = Terminated
- Termination Date = Termination Effective Date

**Product Waiver Rules** (when product waive indicator = Yes):
- Waiver start date → Waiver Effective Start Date
- Waiver end date → Waiver Effective End Date
- Sum assured waived = 100% Sum Assured
- Premium status → Premium Waived

**Party Update Rules:**
- If Death claim → party status of Life Assured updated to Death

4. Payment record aggregation: records aggregated by policy number + payee ID + payment date + payment currency

---

## Part 6 — Sub-Tasks

### Document List

**Available at:** Acceptance stage, Evaluation stage
**Prerequisites:** Claim case in Acceptance or Evaluation stage

**Steps:**
1. On Acceptance Summary or Case Evaluation page → click **Document List**
2. Check **Required Documents** and **Optional Documents** sections
3. To add new document: in **Additional Document** section, enter Document Name + description + No. of copies
4. Click **Save**

**Document List Fields:**

| Field | Description |
|---|---|
| Last Submission Date | Default = system date; not later than system date |
| Completeness | Default = Y in Required Document tab; user can update |
| Waive | Default = N in Required Document tab; user can update |
| Required Document | Configured list; multiple documents selectable |
| Optional Document | Configured list; multiple documents selectable |
| Additional Document | User-added documents; can be deleted |

---

### Query Letter

**Purpose:** Request additional documents, signature, or compliance forms from claimant.
**Available at:** Acceptance, Evaluation, Approval stage
**Navigation:** Click **Query Letter** button on relevant case page

**Steps:**
1. Click Query Letter
2. In **Generate Claim Query Letter** section: enter Receiver and receiver information
3. Click **Generate Letter** → letter added with status **To be Printed**
   - **NOTE:** If letter is Printed and not replied, case CANNOT move to next step
4. After claimant provides required info: select **Replied** from Letter List dropdown
5. Click **Update Status** → click **Back**

**Query Letter Fields:**

| Field | Description |
|---|---|
| Document No. | System-generated; non-editable |
| Document Name | Default = "Query Letter" |
| Generate Date | System-generated on click of Generate Letter; non-editable |
| Generate By | Username of generating user; system-generated; non-editable |
| Status | To be Printed → Replied (via Update Status button) |
| Reply Date | Date letter is replied |
| Receiver | Select Policy Role or claim role of addressee |
| Receiver Name | Auto-fills from role; free text when "Other" is selected |
| Letter Content | Predefined or updatable options |

---

### Medical Bill Entry

**Available at:** Acceptance stage, Evaluation stage (read-only at Approval)
**Prerequisites:** Case is a Medical claim in Acceptance or Evaluation stage

**Steps:**
1. Click **Medical Bill** → Medical Bill Summary page (default)
2. Click **Inpatient Medical Bill** or **Outpatient Medical Bill** to enter new bill
3. Input medical bill information in **New Bill** tab
4. Click **Save** (added bills can be deleted via Delete button)
5. Click **Exit** to return to acceptance/evaluation page

**Medical Bill Fields:**

| Field | Description | Notes |
|---|---|---|
| Medical Bill Type | Inpatient / Outpatient | — |
| Bill No. | Sequence number | Auto-generated |
| Bill Currency | Currency of input bill | — |
| Bill Date | Creation date of medical bill | — |
| Hospital Code | Select from configured hospital list | — |
| The 3rd party SMM paid amount | Total SMM paid by other insurance/3rd party in bill currency | — |
| Surgical Code | Surgery codes in this bill | — |
| Start Date ~ End Date | Inpatient only | Start and end date + time |
| Admission Days | Inpatient only | Auto-calculated: 24 hours = 1 whole day |
| Bill Amount | Bill amount per item | — |
| Exclude Item | Excluded amount in bill currency | — |
| 3rd Party Paid Amount | 3rd party paid amount per item | — |
| 3rd Party SMM Amount | Auto-calculated: `Round((total 3rd SMM amount × item's (bill amount - excluded amount) / (total bill amount - total exclude amount), 2))`; last item gets remaining balance | — |
| Claimed Amount | `= Bill Amount - Exclude Item - 3rd Party Paid Amount - 3rd Party SMM Amount` | Auto-calculated |

**Note:** Items differ between Inpatient and Outpatient bills (configurable). Mapping exists between liability and bill type + item; used to get initial parameters for liability during calculation.

---

### Escalation

**Purpose:** Send case to senior claim officer or investigator during acceptance, evaluation, or approval.
**Available at:** Acceptance in Progress / Waiting for Evaluation / Evaluation in Progress / Approval in Progress

**Steps:**
1. On Acceptance Summary / Case Evaluation / Case Approval page → click **Escalation**
2. Enter escalation content in **Comment** box
3. Select **Escalate to Claim Officer** or **Submit to Investigator**
4. Select target from dropdown; update **Due Date** (default = system date + 1 day)
5. Click **Submit**
6. Senior officer/investigator: Claims > Work List → search by criteria → click Case No. → Escalation Reply page → enter reply comment → Submit

**Escalation Rules:**
- Escalation with status Responded or Withdrawn **cannot be withdrawn**

**Escalation Field Reference:**

| Field | Description |
|---|---|
| Escalation Type | Escalate to Claim Officer / Submit to Investigator |
| Escalation To | Select from dropdown (enabled after type selected) |
| Due Date | Default: system date + 1 day |
| Escalation Officer | Current claim user; read-only |
| Escalation Date | System date; read-only |
| Comment | Free text |
| Escalation History | View history and withdraw escalation |

---

### Underwriting (during Evaluation)

**Purpose:** Submit claim case to UW workbench for underwriting decision before case approval.
**Prerequisites:** Case status = Evaluation in Progress; UW must be completed before case approval

**Steps:**
1. On Evaluation page → click **Underwriting**
2. In claim underwriting application UI: select Policy, input content, send selected policies to UW workbench
3. Underwriter retrieves policy in UW workbench and replies
4. After receiving UW comments: continue evaluation

---

## Part 7 — Advanced Functions

### Claims Watch List

**Purpose:** Reassign tasks to claim officers or exclude current user.
**Navigation:** Claims > Watch List

**Steps:**
1. Claims > Watch List → enter criteria → Search
2. In Search Result: click case number → Reassign
3. On Reassign To page: select Reassignment Strategy:
   - **Reassign to Designated User**: select user from dropdown → Submit
   - **Revert**: select Exclude Current User or not → Submit

---

### Change Disbursement Plan

**Purpose:** Modify outstanding installment payments after case settlement.
**Prerequisites:**
- Case Status = Settled
- Case has pending payment or unpaid payment

**Navigation:** Claims > Change Disbursement Plan

**Steps:**
1. Enter Case No. → system displays case information (only if status = Settled)
2. In **Outstanding Payment Allocation** area:
   - **Terminate Installment**: terminates the installment
   - **Change to Lump Sum**: converts installment to lump sum (only when unpaid installments remain)
   - **EDIT**: change pending status (Yes/No) or interest
3. Payee maintenance: Delete existing / click +Lump Sum or +Installment to add
4. For pending payment release: on Change Disbursement page → Pending Payment = No → Save → Back
5. Click **Submit** → fee records generated/updated

---

### Cancel a Case

**Purpose:** Cancel a claim case directly.
**Prerequisites:**
- Case is at registration / acceptance / evaluation / approval stage
- Case status ≠ Settled / Cancelled / Withdrawn

**Navigation:** Claims > Cancel Case

**Steps:**
1. Enter Case No. → search
2. Select case → Submit → Cancel Case page
3. Click **Cancellation** → select Cancellation Reason + comments → Submit → OK

**After Cancellation:**
- Generated claim reserves cancelled
- Pending fund transactions (generated after case acceptance) cancelled

---

### Reverse Case

**Purpose:** Reverse a settled claim case (undo settlement).
**Prerequisites (ALL must be met):**
- Case status = Settled
- Actual Payment Status = Unpaid
- Policy Status = Inforce
- Policy is NOT frozen
- No on-going claim for the policy
- No completed transactions after case settled (exception: Renew / Partial Withdrawal / Apply Policy Loan / Auto Premium Loan)
- No product terminated in the case
- There IS waiver premium generated after the claim case

**Navigation:** Claims > Reverse Case

**Steps:**
1. Input Case No. → search → select case → Submit
2. Click **Reverse** → Reversal page
3. Input Reverse Reason and comments → Submit

**After Reversal:**
- Case status = Void
- Reversed product information, finance information, and Accumulator information updated in Reversal Summary

---

### Claims Query

**Purpose:** Query comprehensive information of any claim case.
**Navigation:** Claims > Query

**Steps:**
1. Search by Case No. / Policy No. / Insured Name / ID No. (or Advanced Search)
2. Click Case No. → Query Claim Case Detail Information page

**Note:** Page displayed varies with different case status.

---

### Copy Case

**Purpose:** Create a new claim case by copying an existing case.
**Navigation:** Claims > Copy Case

**Steps:**
1. Input Case No. → search → case detail displayed
2. In **New Case Information** section:
   - Select New Case Status (mandatory): Waiting for Acceptance OR Waiting for Evaluation
   - Select Copy Information from Original Case (optional): Medical Bill / Document List / Image
   - Add comment in comment area
3. Click **Submit** → new claim case created

---

### Add Insured for Claim

**Purpose:** Add a new LA (anonymous insured) to an existing policy for claim purposes. Used for free child cover, newborn child, etc.
**Navigation:** Claim > Add Insured for Claim

**Steps:**
1. Input Policy No. → search existing policy information
2. Input additional LA information (basic information) → Submit
3. New LA added to policy; can be used in Registration / Acceptance / Evaluation

---

### Medical Report Fee Payment

#### Create Medical Billing
**Purpose:** Create medical report fee payable to hospital or clinic during claim processing.
**Navigation:** Claim > Medical Billing > Create Medical Billing

**Steps:**
1. Input search criteria (Business Type = Claim, Claim Case No.) → Search
2. Enter medical billing information (Clinic, Medical Type, Fee Amount, GST Amount, etc.)
3. Click **Confirm** → Submit

**Result:** System generates payable Fee Amount and GST Amount. Actual payment = Fee Amount + GST Amount (after payment requisition/authorization).

#### Reverse Medical Billing
**Purpose:** Reverse a medical report fee payment.
**Navigation:** Claim > Medical Billing > Reverse Medical Billing

**Steps:**
1. Input search criteria (Business Type = Claim, Claim Case No.) → Search
2. Select medical report fee record to reverse
3. Click **Reverse** → Submit

---

## Config Gaps Commonly Encountered in Claims

| Scenario | Gap Type | Config Location |
|---|---|---|
| Auto acceptance rules need adjustment | Config Gap | Claims → Auto Acceptance Rule Config |
| Auto approval threshold (e.g. change from 1,000) | Config Gap | Claims → Auto Approval Rule Config |
| Claim type DescAbbr for case number | Config Gap | TClaimType table → DescAbbr |
| Liability not showing in claim type tab | Config Gap | Claim Config → Claim Type & Liability Category relationship |
| Required document checklist per claim type | Config Gap | Claim → Document Checklist Config |
| Fraud/Red Flag reasons (add new reason) | Config Gap | Claim Configuration → code table |
| Case Classification options | Config Gap | Code table configuration |
| Medical bill items (Inpatient/Outpatient) | Config Gap | Claim Config → Medical Bill Item |
| Liability evaluation sequence | Config Gap | Product Factory → Product Liability → Sequence |
| Claim formula per liability | Config Gap | Claim Config → Claim Formula Initialization |
| Accumulator (Accutor) chain for liability | Config Gap | Claim Config → Accutor Configuration |
| Warning message conditions at evaluation | Config Gap | Claim warning rule configuration |
| Claim officer authority levels | Config Gap | Claim → Authority Level Config |
| Task reassignment strategy | Config Gap | Claims watch list assignment config |
| Policy lock behaviour by claim type | Config Gap | LockPolicyIndi / EditLockPolicy config table |
| Installment type options | Config Gap | Code table for installment types |
| ILP: sell-all-fund-at-acceptance global parameter | Config Gap | Global parameter configuration |

---

## Terminal Illness (TI) Benefit Rules (from Claims UG V24.05)

### TI Claim Workflow
| Stage | Action |
|---|---|
| 1. Case Registration | TI diagnosis date + physician certification required |
| 2. Medical Verification | Attending physician report + medical records |
| 3. UW Review | TI definition checked (typically life-threatening, incurable, <12 months prognosis) |
| 4. Disbursement | Lump sum = SA at time of TI diagnosis |

### TI Benefit Calculation
| Scenario | Formula |
|---|---|
| Standard TI | SA at TI claim date |
| With ADB rider | ADB may reduce TI payout if TI = ADB trigger |
| With CI rider | TI and CI may be mutually exclusive |



## Auto Acceptance Rules (from Claims UG V24.05)

### Auto Acceptance Criteria
A claim is auto-accepted when ALL of:
1. Claim amount <= Auto Acceptance Threshold (MAS cap: S$50,000)
2. No fraud indicators
3. Claim type is on Auto-Adjudication list
4. Claim is within policy terms

### Config Location
| Setting | Path |
|---|---|
| Auto Acceptance Threshold | Product Factory > Claims Rules > Auto Acceptance Amount |
| Auto Acceptance Indicator | Product Factory > Claims Rules > Auto Accept Indicator |
| Auto-Adjudication List | Claims Configuration > Auto Adjudication Rules |


## Medical Bill Entry (from Claims UG V24.05)

### Bill Entry Screen
| Field | Rule | Mandatory |
|---|---|---|
| Bill Date | Must be within policy coverage period | Y |
| Bill Amount | Must match receipt | Y |
| Currency | Must match billing currency | Y |
| Diagnosis Code | ICD-10 code required | Y |
| Treatment Type | Must match benefit schedule | Y |
| Panel / Non-panel | Panel: direct settlement; Non-panel: reimbursement | Conditional |
| Room & Board | Subject to limit per day | Conditional |
| Deductible | Per policy schedule | Conditional |
| Co-insurance | % per policy schedule | Conditional |



## Case Evaluation (from Claims UG V24.05)

### Evaluation Triggers
- Auto-flagged: claim amount > Auto Acceptance Threshold
- Manual-flagged: suspicious claim indicators
- UW re-referral: complex medical conditions

### Evaluation Sub-Tasks
| Sub-Task | Description |
|---|---|
| Document List | Track required documents received |
| Query Letter | Request additional info from claimant |
| Medical Bill Entry | Record itemized bills |
| Field Investigation | On-site verification for high-value claims |


## Disbursement Rules (from Claims UG V24.05)

### Disbursement Plan
| Method | Description |
|---|---|
| Cheque | Pay to beneficiary / policyowner |
| Bank Transfer | Direct to beneficiary bank account |
| GIRO | For regular benefit payments (e.g., annuity) |
| Third-party | If policyowner is deceased and beneficiary is minor |

### Disbursement Processing
- Cheque: Generated upon approval, valid for 30 days
- Bank Transfer: Processed via payment batch
- Tax deduction: Applicable for death benefit (prevents double-dipping rules)


## INVARIANT Declarations (Claims Module)

```
INVARIANT 1: Claim eligibility requires Policy_Status = In-Force at event date
  Checked at: Case Acceptance → product acceptance validation
  Exceptions: Case Classification = Special allows lapsed/terminated products

INVARIANT 2: Claim cannot proceed if Policy is Frozen by CS or CLM
  Checked at: Case Acceptance → product acceptance validation
  Error: Product cannot be accepted

INVARIANT 3: Query letter must be Replied before case can proceed to next step
  Checked at: Acceptance submission / Evaluation submission
  Error: "Query letter is not replied."

INVARIANT 4: Disbursement Amount must equal Allocated Disbursement Amount per policy
  Checked at: Evaluation submission
  Error: Blocks submission

INVARIANT 5: UW request must be responded before Evaluation can be submitted
  Checked at: Evaluation submission
  Error: Blocks submission

INVARIANT 6: Escalation must be responded before Evaluation can be submitted
  Checked at: Evaluation submission
  Error: Blocks submission

INVARIANT 7: Reverse Case requires Actual Payment Status = Unpaid
  Checked at: Reverse Case → submission
  Prerequisite: Cannot reverse if payment already made
```

---

## Related Files

| File | Purpose |
|---|---|
| `insuremo-ootb.md` | Claims OOTB capability classification (use for Gap Analysis) |
| `ps-product-factory.md` | Claim Configuration in LI Expert Designer (liability, claim formula, Accutor) |
| `ps-customer-service.md` | CS alteration items that may interact with claims (e.g. Cancellation, Reinstatement) |
| `output-templates.md` | BSD output templates for claims-related gaps |