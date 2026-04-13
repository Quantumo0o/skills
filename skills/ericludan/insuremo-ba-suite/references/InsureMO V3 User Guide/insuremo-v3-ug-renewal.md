# InsureMO Platform Guide — Renewal Main Process
# Source: Renewal Main Process User Manual, LifeSystem 3.8.1
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb.md instead
# Version: 1.0 | Updated: 2026-03-26

---

## 1. Purpose of This File

Answers: What are the Renewal batch processes, their sequencing, prerequisites, and business rules?
When to use: Agent 2 (BSD configuration), Agent 6 (config runbook), BA verification of Renewal module rules.

---

## 2. Module Overview

```
Renewal Main Process
│
├── Extract Amount to Bill
│   ├── Batch (automated daily)
│   └── Single (manual counter collection)
│
├── Generate Premium Notice (batch daily)
│
├── Apply Premium and Move Due Date (batch daily)
│
├── Generate Premium Reminder Notice (batch daily)
│
├── Non-forfeiture Optional Disposal
│   ├── Traditional Product Lapse
│   └── ILP Lapse
│
├── Perform Manual Extraction (DDA / Credit Card)
│
└── Manually Suspend and Unsuspend Extraction
```

---

## 3. Workflow — Standard Sequence

```
┌─────────────────────────────────────────────────────────────┐
│  DAILY RENEWAL CYCLE (batch, in sequence)                  │
│                                                             │
│  [1] Extract Amount to Bill (Batch)                         │
│        │                                                    │
│        ▼                                                    │
│  [2] Generate Premium Notice                               │
│        │                                                    │
│        ▼                                                    │
│  [3] Apply Premium & Move Due Date                         │
│        │  (if premium received)                            │
│        ▼                                                    │
│  [4] Generate Premium Reminder Notice                       │
│        │  (if premium overdue ≥ 7 days)                   │
│        ▼                                                    │
│  [5] Non-forfeiture Optional Disposal                       │
│        │  (if grace period lapsed without payment)         │
│        ▼                                                    │
│  END                                                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  MANUAL OVERRIDES (ad-hoc, any time)                        │
│                                                             │
│  [A] Extract Amount to Bill (Single) — counter collection   │
│  [B] Perform Manual Extraction — DDA / Credit Card scheduling│
│  [C] Manually Suspend / Unsuspend Extraction                │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Menu Navigation Table

| Action | Path |
|---|---|
| Extract Amount to Bill (Single) | Billing/Collection/Payment > Billing > Extraction Amount to Bill (Single) |
| Perform Manual Extraction | Billing/Collection/Payment > Billing > Perform Manual Extraction |
| Manual Suspend/Unsuspend Extraction | Billing/Collection/Payment > Billing > Manual Suspend and Unsuspend Extraction |
| CS Customer Service (for renewal-linked CS) | Customer Service > Customer Service Registration |
| CS Entry | Customer Service > Customer Service Entry |
| CS Approval | Customer Service > Customer Service Approval |
| CS Inforce | Customer Service > Customer Service Inforce |

---

## 5. Status Reference Table

| Status | When Set |
|---|---|
| `Inforce` | Policy is active, premium paid up to date |
| `Lapse` | Premium not paid within grace period |
| `Lapse Reason = APL Lapse` | GSV insufficient, APL raised and unpaid |
| `Lapse Reason = Normal Lapse` | Premium overdue, no cash value to offset |
| `PLD (Potential Lapse Date)` | ILP TIV insufficient to cover charges |
| `PJD (Projected Lapse Date)` | Future lapse projected for ILP |
| `Terminated` | Full surrender or cancellation |
| `Inforce` (benefit level) | Risk coverage active |
| `Lapse` (benefit level) | Benefit coverage suspended |

---

## 6. Per-Process Sections

### Part 1 — Extract Amount to Bill (Batch)

#### Prerequisites
- Benefit status is `Inforce`
- Benefit premium status is `Regular`
- For normal daily runs: System Date ≥ Next Due Date − 30 days
- For policies without grace period: System Date ≥ Next Due Date − 60 days
- Payment method is **not** `Unit Deduction Rider`
- NOT applicable to Bucket Filling Product

#### Navigation
Batch job runs automatically at a specific time every day (no manual navigation).

#### Steps
1. System starts batch job to extract policies due for renewal
2. System calculates amount to bill:
   a. Calculates renewal premium amount
   b. Checks suspense balance, APA balance, cash bonus, survival benefit to offset premium
   c. Calculates net amount to bill
3. System creates billing records
4. Finance personnel performs posting to GL

#### Extract Amount to Bill (Batch) Rules

**Premium Recalculation Triggers** — System recalculates next renewal premium if benefit meets any of:
- Benefit = Non-level premium AND Calculation Method = Using Sum Assured to calculate premium
- Calculation method is based on remaining term AND Using Sum Assured to calculate premium
- Benefit = Level premium AND Non-guarantee premium AND Using Sum Assured to calculate premium
- Benefit has loading → recalculate extra premium
- There is pre-contract information
- Benefit is a waiver product AND calculation method = Using Sum Assured to calculate premium
- Waiver of premium/payer benefit → premium, SA waived, annual amount waived, initial SA all recalculated

**ILP Premium Separation Rules:**
- Investment premium and insurance premium must be separated
- Insurance/investment premium for different policy years must be separated
- If more than one premium due between next due date and system date, each premium due generates separate record

**GST Rules:**
- Premium due is inclusive of GST
- GST = Period Premium × (1 + GST Rate), using prevailing rate at premium notice generation date
- GST rounded to whole cent: ≤ $8.124 → $8.12; ≥ $8.125 → $8.13
- Calculation of GST is based on **premium only**; overdue interest, miscellaneous fees, and policy fees do NOT form part of GST

**Net Amount to Bill Calculation — Offset Order:**
1. **Suspense balance** (first renewal suspense, then general suspense):
   - Sufficient suspense to offset full premium → policy NOT extracted for billing
   - Insufficient suspense → calculate net premium due to be billed
   - For CPF billing: net off from locked CPF renewal suspense
2. **APA balance**:
   - APA + interest until next due date sufficient to offset full premium → policy NOT extracted
   - Insufficient APA → calculate net premium due
3. **Cash Bonus Option 2**:
   - CB balance + interest sufficient to offset full premium → still extracted for billing (for information only)
   - Insufficient CB → calculate net premium due (via premium notice only)
4. **Survival Benefit Option 2**:
   - SB balance + interest sufficient to offset full premium → still extracted for billing (for information only)
   - Insufficient SB → calculate net premium due (via premium notice only)

**Billing Record Lifecycle:**
- If new premium amount = previous record amount → no change
- If new amount > previous amount → generate CS increased SA premium record; cancel old record after payment + policy inforce
- If new amount < previous amount → cancel old record; policy comes inforce directly; user must manually run batch to generate new record
- If payer info, payment frequency, or payment method changed → cancel all outstanding records with due date > current due date; create new records from current info

**Indexation Rules:**
- If `t_contract_product.indx_indi = Y` (valid benefits with indexation), calculation is at segment level
- Indexation must be billed together with premium in renewal cycle
- When extracting amount to bill, system checks for indexation and adds increment premium to regular premium
- Indexation for new policy year offered and extracted when NDD ≥ indexation due date AND client has not rejected offer

---

### Part 2 — Generate Premium Notice

#### Prerequisites
- Batch job for Extract Amount to Bill (Batch) has been performed
- No premium notice has been generated for this extraction

#### Navigation
Batch job runs automatically after Extract Amount to Bill (Batch).

#### Steps
1. System starts batch job to extract policies requiring premium notice
2. System retrieves and consolidates relevant information
3. System generates and prints premium notice

#### Generate Premium Notice Rules

**Extraction Criteria by Policy/Payment Type:**

| Policy Type | Payment Method | Frequency | Extraction |
|---|---|---|---|
| Traditional | Cash/Cheque | Quarterly, Half-yearly, Yearly | Daily |
| ILP | Cash/Cheque | — | Daily |
| A&H | Cash/Cheque | Yearly | Daily; ElderShield, SupremeHealth, MaxHealth excluded |
| A&H | Credit Card | Yearly | Daily |

**Additional Extraction Criteria:**
- Policies extracted must be `Inforce` and benefit premium status = `Regular`
- For ILP: no PLD or PJD before next due date; premium holiday indicator not set
- No premium notices for policies with premiums paid in advance
- No premium notices for policies under APL
- No premium notices for payment method = SSS
- If payment method is CPF-OA, CPF-SA, or SRS and CPF billing is suspended → premium notice must be sent
- No premium notices for policies with invalid address indicator
- If sufficient suspense or APA exists for current premium due → no notice generated
- If Direct Debit suspended but payment method remains Direct Debit → premium notice must be sent
- If Credit Card suspended but payment method remains Credit Card → premium notice must be sent
- If Renewal Extraction Batch Run is re-run to recreate records due to CS application → premium notice will NOT be regenerated

**Premium Notice Data Fields:**
- Due date
- Premium amount and arrears (net of suspense, APA, CB, SB)
- Each unpaid premium installment as separate line item
- Plus GST (prevailing rate at notice generation date, rounded to whole cent)
- Plus policy loan and interest up to next due date (if > 0, for information)
- Minus APA amount including interest up to next due date
- Minus cash bonus (Option 2) + interest up to next due date
- Minus survival benefit (Option 2) + interest up to next due date
- Payment frequency (M/H/Q/Y), service branch code, policy number, currency, address and name, name of life assured, Life Planner/GMR number, extraction date

**ILP Bucket Filling:**
- System generates premium notice before each billing date (bucket filling due date)
- When notice generated, billing date moves to next bucket filling due date regardless of collection
- Billing amount = target premium of bucket filling due date at billing date
- If tolerance allowed (defined in `t_ilp_bucket_tolerance`):
  - Difference between actual target premium and target premium within tolerance → set as target premium tolerance
  - Difference between actual recurring top-up and recurring top-up within tolerance → set as recurring top-up tolerance
  - If `BUCKET_FILLING_TOLERANCE_OPTIONS = Y`: new premium allocated to bucket filling due date
  - If `BUCKET_FILLING_TOLERANCE_OPTIONS = N`: new premium allocated to tolerance first, then bucket filling due date

---

### Part 3 — Apply Premium and Move Due Date

#### Prerequisites
- Premium is received

#### Navigation
Batch job runs automatically.

#### Steps
1. System starts batch job to extract policies for which premium is received
2. System moves the due dates
3. System updates and saves information
4. Finance personnel performs posting to GL; third-party system processes agent commission

#### Apply Premium and Move Due Date Rules

**Due Date Movement Rules:**
- Due dates include: current due date, next due date, fund due date, policy due date
- For traditional policy: if Next Due Date ≤ System Date + 30 AND suspense amount enough for one installment → move immediately
- Moving of due dates is based on policy commencement date and calendar month
  - Monthly: if commencement = 31/1/2005 → next due = 28/2/2005 → 31/3/2005 → 30/4/2005...
  - Handles leap years correctly

**Suspense Check Order:** Renewal suspense first, then general suspense

**Information Updates on Due Date Move:**

| Update Item | Formula/Rule |
|---|---|
| Policy Year | = Integer[(number of months between Next Due Date & Commencement Date) / 12] + 1 |
| Benefit Premium Status | If Next Due Date > Premium Expiry Date → status = Fully Paid |
| Remaining Suspense | = Suspense before moving − Amount applied as premium |
| Remaining APA | Updated accordingly |
| Pre-contract Information | If effective date = next due date after move → update benefit info per pre-contract |
| Guarantee Period Start Date | Updated if needed |
| ILP Minimum Amount | If minimum amount applied successfully → nullify PLD and Minimum Amount; if amount collected < minimum → amount stays in renewal suspense, PLD and Minimum Amount NOT nullified |
| ILP Product 0158/0158C | After apply premium, system calls ILP SA calculation to update SA |
| ILP PJD | If PJD exists at policy level → nullify PJD |

**ILP Unit Allocation:** System passes Collection Date and Transaction Time to ILP module for buying units. (Collection Date and Transaction Time are for the last collection transaction for the outstanding premium record.)

**Upon Successful Due Date Move:**
- For ILP: maintains stream info, calls ILP premium allocation function
- For both ILP and traditional: if due date = waive start date → update premium status to Waived, cancel all outstanding premium records with due date ≥ current due date
- Recalculate next premium due

**Reactivation of Suspended Deductions:**
- Reactivate Direct Debit or credit card deduction if originally auto-suspended
- Do NOT reactivate if Direct Debit account is closed/invalid, or credit card account is invalid
- For Direct Debit: second failed attempt → suspension; reactivated if collection received after first attempt
- When up-to-date premium collected → Direct Debit or credit card deduction resumes for next premium due

**Indexation Confirmation:**
- If indexation applied (`t_contract_product.indx_indi = Y`): calculation at segment level
- If segment premium comes in → create new segment in `t_contract_segment`
- If client pays new premium after indexation → client accepts indexation → create new segment, update benefit total SA and premium info
- If client pays only original premium before indexation → client rejects → record reject times; when reject times = 2 → change indexation indicator to `N`, indexation suspend cause = `Not accept the offer for 2 consecutive times`

---

### Part 4 — Generate Premium Reminder Notice

#### Prerequisites
- Batch job for Extract Amount to Bill (Batch) has been performed
- Premium is overdue by a certain period (e.g., 7 days)

#### Navigation
Batch job runs automatically.

#### Steps
1. System starts batch job to extract policies requiring premium reminder notice
2. System retrieves and consolidates data to be printed
3. System generates and prints premium reminder notice
4. System generates premium due report

#### Generate Premium Reminder Notice Rules

**Extraction Criteria (Traditional and ILP with Cash/Cheque):**
- Policy has no PLD or PJD before next due date
- Premium holiday indicator not set
- ILP: no PLD or PJD before next due date; premium holiday not set; TIP ≠ 0 (if TIP = 0, no reminder)
- Extract quarterly, half-yearly, yearly payment frequency policies
- Extract all policies with premiums overdue ≥ 7 days
- Policy must be `Inforce` and benefit premium status = `Regular`

**Exclusions:**
- No premium reminder notices for policies with premiums paid in advance
- No premium reminder notices for policies under APL
- Premium reminder notices generated for payment method = Bankers' Order (quarterly, half-yearly, yearly only)
- No premium reminder notices for policies with invalid address indicator
- If sufficient suspense or APA for current premium due → no reminder generated
- If Direct Debit suspended but method remains Direct Debit → reminder must be sent
- If Credit Card suspended but method remains Credit Card → reminder must be sent
- If Renewal Extraction Batch Run re-run due to CS application → premium reminder will be regenerated

**Premium Reminder Notice Data Fields:** (same structure as premium notice)
- Next due date
- Premium amount and arrears (net of suspense, APA, CB, SB)
- Each unpaid installment as separate line
- ILP: if premium up-to-date (no arrears) → display current TIP
- Plus GST (prevailing rate, rounded to whole cent)
- Plus policy loan and interest up to next due date (if > 0)
- Minus APA (including interest up to next due date)
- Minus cash bonus (Option 2) + interest up to next due date
- Minus survival benefit (Option 2) + interest up to next due date
- Payment frequency, service branch, policy number, currency, address, life assured name, Life Planner/GMR, extraction date

---

### Part 5 — Non-forfeiture Optional Disposal

#### Prerequisites
- Renewal Batch Job has been run to attempt to apply premium and move due date
- For traditional: Benefit Premium Status = `Regular`
- Fee status is not `Bank Transferring`
- Manual SV indicator of any inforce benefit is not `Yes`

#### Navigation
Batch job runs automatically after Apply Premium and Move Due Date.

#### Non-forfeiture Optional Disposal — Traditional Product Lapse

**Policy Overdue Check:**

| Condition | Overdue If |
|---|---|
| Not renewable case | Main benefit Next Due Date ≥ (Due Date + Grace Period + Additional Grace Period) for any inforce and regular benefit |
| Auto renewable case | Main benefit Next Due Date ≥ (Due Date + 30 days) for any inforce and regular benefit |
| Monthly payment frequency | System Date ≥ (Due Date + Grace Period) |
| Non-monthly payment frequency | System Date ≥ (Due Date + Grace Period + Additional Grace Period) |

**Processing Steps:**

Step 1: Extract policies requiring non-forfeiture disposal. Check if policy overdue per table above.
Step 2: Check if main benefit has cash value per product definition.
  - If yes → go to Step 3
  - If no → check if policy overdue for normal lapse
Step 3: Check if APL should be raised:

| APL Scenario | Condition |
|---|---|
| GSV = 0 as at System Date | Check if overdue for normal lapse |
| GSV ≠ 0 as at System Date | Check if overdue for raising APL |

**Overdue for Raising APL:**

| Scenario | Condition |
|---|---|
| Current APL account value = 0 | System Date ≥ (Due Date + Grace Period + Additional Grace Period) for any inforce and regular benefit |
| Current APL account value ≠ 0, Monthly payment | System Date ≥ (Due Date + Grace Period) |
| Current APL account value ≠ 0, Non-monthly payment | System Date ≥ (Due Date + Grace Period + Additional Grace Period) |

If overdue → raise APL (see Perform APL); if not → processing ends.

Step 4: Check if PLD exists.
  - If yes: if System Date ≥ PLD → perform APL lapse (update risk status, policy status, lapse date, lapse reason)
  - If no → processing ends

Step 5: Generate reports and letters.

**Policy/Benefit Updates on Lapse:**

| Update | At Benefit Level (if in-force) | At Policy Level (if main benefit lapsed) | Indexation Segment (if benefit has indexation and lapsed) |
|---|---|---|---|
| Risk Status | `Lapse` | — | — |
| Policy Status | — | `Lapse` | — |
| Lapse Reason | `APL Lapse` | `APL Lapse` | — |
| Lapse Date | `PLD` | `PLD` | — |
| Segment Status | — | — | `PLD` |

#### Non-forfeiture Optional Disposal — ILP Lapse

Two ILP lapse methods exist:

**Method 1: Calculate Lapse Date in Advance**
- Runs with Charge Deduction Batch
- System calculates whether enough balance for upcoming charge deduction and PLD
- No Non-lapse Guarantee Period; Non-lapse Guarantee Period does NOT coexist with this method
- Parameter `Allow Pending` has no effect

**Method 2: Deduction until TIV=0** (coexists with Non-lapse Guarantee Period)

| `Allow Pending` Setting | Scenario | PLD Calculation |
|---|---|---|
| `Allow Pending = Y` | TIV = 0 during Fund Transaction Batch charge deduction | System checks if within Non-lapse Guarantee Period |
| `Allow Pending = Y` | NOT within Non-lapse Guarantee Period | PLD = FT Run Date OR PLD = NAC Due Date + PLD Grace Period |
| `Allow Pending = Y` | WITHIN Non-lapse Guarantee Period AND (FT Run Date) > (Premium Due Date + Contractual Grace Period + Additional Grace Period) | PLD = FT Run Date + PLD Grace Period |
| `Allow Pending = Y` | WITHIN Non-lapse Guarantee Period AND payment − withdraw amount > TP due | No PLD set |
| `Allow Pending = Y` | WITHIN Non-lapse Guarantee Period AND payment − withdraw amount < TP due | PLD = FT Run Date + PLD Grace Period |
| `Allow Pending = N` | Within Non-lapse Guarantee Period | PLD = Due Date + Contractual Grace Period + Additional Grace Period (regardless of TIV) |
| `Allow Pending = N` | Out of Non-lapse Guarantee Period AND TIV ≤ 0 | PLD = Charge Due Date (during Charge Deduction Batch) |

---

### Part 6 — Extract Amount to Bill (Single)

#### Prerequisites
- Policy status is `Inforce`
- Benefit premium status is `Regular`
- **NOT applicable to Bucket Filling Product**

#### Navigation
`Billing/Collection/Payment > Billing > Extraction Amount to Bill (Single)`

#### Steps
1. From main menu, select `Billing/Collection/Payment > Billing > Extraction Amount to Bill (Single)`
2. Enter search criteria (Policy No., Party ID Type, Party ID No., Policyholder Name) and click Search
3. Enter billing month (format: `MMYYYY`) in the Date field; click Submit
4. System calculates amount to bill (same calculation as batch)
5. System creates billing record
6. Exit

**ILP Note:** When performing single extraction for ILP policy, system caps maximum advance premium to **36 months**.

---

### Part 7 — Perform Manual Extraction

#### Prerequisites
- For ILP: premium holiday indicator is not set

#### Navigation
`Billing/Collection/Payment > Billing > Perform Manual Extraction`

#### Steps
1. Select payment method; click `Deduction` or `Refund`
2. Set search criteria; click Search
3. On `Perform Manual Extraction – Update` page:
   a. View policy information
   b. In `Force Billing` area: enter Source of Billing, Next Extraction Date, Amount to Bill; click `Add`
   c. In `Deduction/Refund Records` area: select a record and update extraction date
   d. Click Submit

#### Payment Method / Case Type Rules:

| Payment Method | Case Type | Condition |
|---|---|---|
| Credit Card | NB cases | Policy status = `Accepted` or `Conditionally Accepted`; record in billing process |
| Credit Card | CS alteration or renewal cases | CS alteration or renewal; record in billing process |
| Credit Card | Claim cases | Record in billing process |
| DDA | Renewal cases | All renewal cases |
| DDA | NB, CS alteration, or claim cases | Record in billing process |

**Grey-out conditions:** System greys out policy matching policy number if:
- Payment method mismatch
- Record already in billing process

#### Perform Manual Extraction Rules

1. Selected payment method must match the payment method of the target policy
2. Force billing record rules:
   - Added when no deduction/refund records exist but user wants to proceed
   - When money received subsequently → NOT auto-applied → goes to general suspense
   - Next extraction date cannot be earlier than current system date
3. Deduction record date update rules:
   - Extraction date cannot be earlier than current system date
   - For DDA: defaults to next DDA extraction run date per schedule; can be changed
   - For credit card rebilling: extraction date can be changed
   - For credit card force billing: defaults to current system date; can be changed
   - For CPF rebilling: CPF extraction date can be changed
   - Extraction date = date when GIRO/credit card/CPF file is generated; system also picks earlier un-extracted dates (weekends, holidays)
   - If extraction date = current system date but extraction already performed (beyond cut-off) → included in next day's extraction file
   - When case already sent for extraction and waiting for money → rebilling NOT allowed for same record

---

### Part 8 — Manually Suspend and Unsuspend Extraction

#### Prerequisites
- N/A (no specific prerequisite)

#### Navigation
`Billing/Collection/Payment > Billing > Manual Suspend and Unsuspend Extraction`

#### Steps
1. Select payment method; click `Deduction` or `Refund`
2. Set search criteria; click Search
3. On `Manual Suspend and Unsuspend Extraction – Update` page:
   a. View policy information
   b. In `Suspend/Unsuspend` area: set `Effective From Date` and `Effective To Date` (format: `DD/MM/YYYY`)
   c. Click Submit

#### Suspend/Unsuspend Field Reference

| Field | Description |
|---|---|
| Suspend Indicator | `Y` = extraction suspended; `N` = extraction unsuspended |
| Effective From Date | Date when extraction is suspended |
| Effective To Date | Date when extraction is unsuspended |

#### Manual Suspend and Unsuspend Extraction Rules

1. Selected payment method must match the payment method of the target policy
2. Suspension period rules:
   - `Effective To Date` cannot be earlier than current system date or `Effective From Date`
   - If suspension not yet started (`Suspend Indicator = N`): `Effective From Date` cannot be earlier than current system date
   - If suspension period is over: `Suspend Indicator` = `N`; both `Effective From Date` and `Effective To Date` set to null; auto-unsuspend done by Auto Suspend and Unsuspend Extraction batch job
   - To change suspension date: update `Effective To Date` to new date; normal billing cycle kicks in after new date
   - To unsuspend: clear `Effective To Date` field; `Effective From Date` removed automatically

---

## 7. INVARIANT Declarations

**INVARIANT 1: Extract Amount to Bill always runs before Generate Premium Notice**
- Checked at: Daily batch sequence
- Effect if violated: Premium notice will reference incorrect or missing billing amounts

**INVARIANT 2: ILP maximum advance premium is capped at 36 months**
- Checked at: Extract Amount to Bill (Single) for ILP policies
- Effect if violated: System may over-extract premium beyond permitted advance limit

**INVARIANT 3: Non-forfeiture disposal never processes policies with Manual SV Indicator = Yes**
- Checked at: Non-forfeiture Optional Disposal batch entry condition
- Effect if violated: Manual SV policies incorrectly processed through automatic non-forfeiture flow

**INVARIANT 4: Bucket Filling tolerance options are mutually exclusive per BUCKET_FILLING_TOLERANCE_OPTIONS flag**
- Checked at: Generate Premium Notice for ILP Bucket Filling products
- Effect if violated: Premium allocated to wrong bucket filling date

**INVARIANT 5: APL Lapse only occurs when GSV = 0 AND APL raised AND unpaid**
- Checked at: Non-forfeiture Traditional Product Lapse Step 3
- Effect if violated: Policy incorrectly lapses with wrong lapse reason

**INVARIANT 6: Manual Extraction Date cannot be earlier than current system date**
- Checked at: Perform Manual Extraction and Manual Suspend/Unsuspend Extraction
- Effect if violated: Back-dated extraction creates incorrect billing records

---

## 8. Config Gaps Commonly Encountered

| Scenario | Gap Type | Config Location |
|---|---|---|
| Grace Period / Additional Grace Period not configured → wrong lapse date calculation | Config Gap | Product Factory: Grace Period, Additional Grace Period per product |
| ILP Non-lapse Guarantee Period not set → PLD calculation incorrect | Config Gap | Product Factory: Non-lapse Guarantee Period parameter |
| `Allow Pending` parameter mis-set for ILP → wrong PLD logic | Config Gap | ILP Product Parameters: `Allow Pending` flag |
| Bucket Filling tolerance table (`t_ilp_bucket_tolerance`) empty → no tolerance applied | Config Gap | ILP Bucket Tolerance configuration table |
| `BUCKET_FILLING_TOLERANCE_OPTIONS` not configured → premium allocated to wrong bucket | Config Gap | System parameter: `BUCKET_FILLING_TOLERANCE_OPTIONS` |
| Direct Debit / Credit Card extraction schedule not defined → manual extraction fails | Config Gap | Billing Configuration: DDA Schedule, Credit Card schedule |
| APL Lapse rate/GSV threshold not configured → wrong APL calculation | Dev Gap (LIMO IT) | APL calculation logic in billing module |
| Indexation rate table not maintained → indexation premium = 0 | Config Gap | Product Factory: Indexation rate table |
| GST rate not updated → GST calculation uses stale rate | Config Gap | System parameter: GST rate (prevailing rate at notice generation) |
| Premium holiday parameter not set → ILP policy incorrectly lapsed | Config Gap | Product Factory: `allow premium holiday` parameter |

---

## 9. Related Files

| File | Purpose |
|---|---|
| `insuremo-ootb.md` | Gap Analysis |
| `ps-customer-service.md` | CS alteration affecting renewal premium amounts |
| `ps-billing.md` | Billing/Collection module (DDA, Credit Card, GIRO) |
| `ps-product-factory.md` | Product parameters (grace period, indexation, NLGP) |
| `output-templates.md` | BSD templates |
