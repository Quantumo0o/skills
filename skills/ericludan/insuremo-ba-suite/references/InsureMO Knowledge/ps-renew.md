# InsureMO Platform Guide — Renewal Process
# Source: Renewal Process User Guide V25.04
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb-full.md instead
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"how does Renewal work in InsureMO"** — batch job sequences, prerequisites, calculation rules, and business logic for premium renewal, non-forfeiture option disposal, premium-waived policy renewal, and rider payment frequency auto-conversion.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for a Renewal-related gap
- Agent 6 is generating a **Config Runbook** for Renewal items
- A BA needs to verify what **preconditions** or **batch rules** the system enforces during renewal processing

---

## Module Overview

```
Renewal Process
│
├── 3.1 Extract Amount to Bill (Batch)              ← Daily batch; calculates premium due; creates billing records
├── 3.2 Generate Premium Notice (Batch)             ← Sends premium notice to policyholder
├── 3.3 Apply Premium and Move Due Date             ← Renew Confirmation batch; moves due dates
├── 3.4 Generate Premium Reminder Notice (Batch)    ← Overdue reminder notice
├── 3.5 Non-Forfeiture Option Disposal              ← APL / auto-RPU / lapse handling post grace period
├── Policy Renew Confirm Waived (Batch)             ← Renewal for premium-waived policies
└── Policy Rider Auto Convert Payment Frequency     ← Auto pay mode conversion at configured milestone
```

---

## Renewal Workflow — Standard Sequence

```
Step 1: Extract Amount to Bill (Batch)
  └─► Step 2: Generate Premium Notice (Batch)
        ├─► [Policyholder pays]
        │     └─► Step 3: Apply Premium and Move Due Date (Renew Confirmation)
        │               └─► Alteration effective; policy info updated
        └─► [Premium NOT paid within notice period]
              └─► Step 4: Generate Premium Reminder Notice (Batch)
                    └─► [Still not paid after grace period]
                          └─► Step 5: Non-Forfeiture Option Disposal
                                ├─► ILP: Deduct rider premium from TIV (if eligible)
                                ├─► Auto RPU (if PUV > 0 and product allows)
                                ├─► APL Lapse (if partial APL done and date ≥ PLD)
                                ├─► Raise APL (if GSV > 0 and product allows)
                                └─► Normal Lapse (if no other option available)
```

**Parallel / downstream processing triggered by renewal:**

| Process | Module |
|---|---|
| Collection | (9) Collection |
| GL Posting | (13) Perform Posting to GL |
| Letter Generation | (14) Manage Letter |
| Commission Processing | (26) Manage Commission |
| Fund Transaction | (11) Manage Fund Transaction |
| Auto Renewal | (8) Auto Renewal |
| Undo Transaction | (2.10) Undo Transaction |

**Daily batch job execution order:**
1. Renewal Batch Job
2. Extract Amount to Bill (Batch)
3. Generate Premium Notice
4. Credit Card Billing Report
5. Other downstream jobs

---

## Per-Process Reference

### 3.1 Extract Amount to Bill (Batch)

**Purpose:** Daily batch that extracts policies due for renewal, calculates the amount to bill, and creates billing records for cashier collection.

> **NOTE:** This process is **not applicable** to Investment Bucket Filling Product.

**Prerequisites — Eligible Policies:**
- Policy Status is 'Inforce'
- Benefit premium status is Regular or Premium Waived
- Premium Frequency is installment
- ILP: no Potential Lapse Date or Projected Lapse Date before next due date
- Rider extraction allowed when rider premium status = Regular and main plan is Fully Paid
- System date ≥ premium due date − leading time (configurable)

**Prerequisites — Ineligible Policies (excluded from extraction):**
- Policy frozen by Claims or Customer Service
- Next premium due date does not meet extraction criteria
- Premium already extracted for this due date
- Payment method is unit deduction ride
- Policy is in premium holiday

**Procedures:**
1. Scheduled daily batch job starts
2. System calculates amount to bill
3. System creates billing records
4. Finance performs posting to GL

**Premium Calculation Rules:**

System **recalculates** renewal premium if any of the following apply:
- Benefit is non-level premium AND calculation method = Using SA to calculate premium
- Benefit's calculation basis = remaining term AND calculation method = Using SA
- Benefit is level premium AND non-guarantee rate AND calculation method = Using SA
- Benefit has loading
- Pre-contract information exists
- Benefit is waiver product AND calculation method = Using SA (waiver SA, annual amount waived, initial SA must also be recalculated)
- Benefit has premium discounts (including campaign discounts)

If none of the above apply → system uses the next premium due amount already recorded at benefit level.

ILP-specific rules:
- Recurring top-up is **NOT** included in renewal premium (handled by separate RSP extraction batch)
- Insurance premium and investment premium are generated separately, split by policy year
- If multiple premiums are due between next due date and system date → separate billing records generated per due amount

**Indexation Rules:**
- If benefit has indexation (t_contract_product.indx_indi = Y): calculation at segment level
- Indexation billed together with regular premium in same renewal cycle
- System checks whether indexation exists and adds increment premium to regular premium
- New policy year indexation extracted when NDD ≥ indexation due date AND offer not rejected by client

**Billing Record Management:**
| Scenario | Action |
|---|---|
| Premium status = Premium Waived | Refer to Policy Renew Confirm Waived (Batch) |
| New amount = previous billing amount | No change to existing record |
| New amount ≠ previous billing amount | Cancel previous record; generate new record |
| Payer / payment frequency / method changed | Cancel all outstanding records with due date > current due date; create new records |
| CS item not yet complete | Collect premium; hold in renewal suspense until CS transaction completes |

---

### 3.2 Generate Premium Notice (Batch)

**Purpose:** Generates and prints premium notices to inform policyholders of renewal premium due after billing extraction has run.

**Prerequisites:**
- Extract Amount to Bill batch has run; no premium notice yet generated for this extraction
- Benefit premium status is NOT Premium Waived

**Procedures:**
1. Scheduled daily batch starts; extracts policies requiring premium notice
2. System retrieves and consolidates relevant policy information
3. System generates and prints premium notice

**Extraction Criteria:**
- Policies are Inforce; benefit premium status is Regular
- ILP additional rules:
  - No Potential Lapse Date or Projected Lapse Date before next due date
  - Premium holiday indicator NOT set
  - No notice generated for premiums paid in advance
  - No notice generated for policies under APL
  - No notice generated if suspense or APA is sufficient to cover current premium due
  - If Renewal Extraction Batch re-run due to CS application → premium notice is regenerated

**Configuration Table: PremiumNoticeDays**

| Column | Description |
|---|---|
| prem_notice_indicator | Whether premium notice should be generated (Y/N) |
| pay_frequency | Payment frequency dimension |
| pay_mode | Payment method dimension |
| sales_channel | Sales channel dimension |
| product_category | Product category dimension |
| leading_days | X days in advance before premium due date to generate notice |

---

### 3.3 Apply Premium and Move Due Date (Renew Confirmation)

**Purpose:** Daily batch that moves due dates for policies with paid premium records; updates policy information; recalculates next premium due amount.

**Prerequisites — Policy Level:**
- Paid premium records exist (collection over counter or upload job); pending due date movement
- Benefit is Inforce; benefit premium status is Regular
- No CS item pending approval (policy NOT frozen)
- No Claims item pending approval (policy NOT frozen)
- ILP with investment rider: zero premium records allowed for investment rider
- Bankruptcy check: process only if Bankruptcy Status (party level) = N, OR Bankruptcy Status = Y AND 'Allow Premium Collection for Bankruptcy' Indicator = Yes

**Procedures:**
1. Scheduled daily batch starts; extracts policies with received premium
2. System moves due dates
3. System updates and saves policy information
4. Finance performs posting to GL; third-party system processes agent commission

**Due Date Movement Validation Rules:**

| System Parameter | Condition | Action |
|---|---|---|
| Allow apply premium before due date = Yes | Suspense ≥ 1 installment | Apply premium; move due date immediately |
| Allow apply premium before due date = No | Next Due Date ≤ System Date AND suspense ≥ 1 installment | Apply premium; move due date immediately |
| Allow apply premium before due date = No | Next Due Date > System Date | No action in renew confirmation |

**Suspense Application Order:**
1. CB/SB account (only if payout option = 2 — To use CB/SB to pay premium; CB first, then SB)
2. Renewal Suspense
3. General Suspense
4. CS Suspense
5. APA Suspense

**Premium Tolerance:** Configurable in rate table (e.g., 0.1% tolerance; underpayment within tolerance is waived).

**Due Date Calculation Rules:**
- Based on policy commencement date and calendar month
- Handles month-end edge cases (e.g., commencement = 31 Jan → next due = 28 Feb; subsequent = 31 Mar, 30 Apr, etc.)
- Handles leap years (e.g., yearly policy due 28 Feb 2023 → next due 29 Feb 2024)

**Policy Information Updates After Moving Due Date:**

| Update | Rule |
|---|---|
| Policy Year | = INT[(months between NDD and commencement date) / 12] + 1 |
| Benefit Premium Status | Set to Fully Paid if NDD > premium expiry date |
| Policy Suspense | Remaining = original suspense − amount applied as premium |
| APA Information | Updated based on amount applied as premium |
| Guarantee Period Start Date | Updated if applicable (for non-guaranteed rate products) |
| ILP: PJD (Projected Lapse Date) | Nullified upon successful due date movement |
| Traditional: PLD (Potential Lapse Date) | Nullified upon successful due date movement |
| ILP: Unit Buying | Collection Date and Transaction Time passed to ILP module |
| ILP: Stream Info | Maintained; ILP premium auto-allocated; premium holiday indicator cleared if applicable |
| Both: Waiver Start Date | If due date = waive start date → update premium status to Waived; cancel all outstanding premium records with due date ≥ current due date |
| Traditional with indexation | Segment-level processing: client pays new post-indexation premium = accepts indexation (new segment created); client pays original pre-indexation premium = rejects indexation; 2 consecutive rejections → indexation indicator set to 'N', suspend cause updated |
| Next Premium Due Amount | Recalculated after due date move |

---

### 3.4 Generate Premium Reminder Notice (Batch)

**Purpose:** Sends premium reminder notices to policyholders whose premium is overdue after a configured number of days.

**Prerequisites:**
- Extract Amount to Bill batch has run for the policy
- Premium overdue by the configured number of days (e.g., 7 days)

**Procedures:**
1. Scheduled daily batch starts; extracts policies requiring reminder notice
2. System retrieves and consolidates data for each extracted policy
3. System generates and prints premium reminder notice
4. System generates premium due report

**Configuration Table: PremiumReminderNoticeDays**

| Column | Description |
|---|---|
| prem_reminder_notice_indicator | Whether reminder notice should be generated (Y/N) |
| pay_frequency | Payment frequency dimension |
| pay_mode | Payment method dimension |
| product_category | Product category dimension |
| product_code | Product code dimension |
| sales_channel | Sales channel dimension |
| sending_times | Number of times reminder letter is triggered |
| overdue_days | X days post premium due date to generate reminder |

**Extraction Criteria:**
- Policies Inforce; benefit premium status Regular
- ILP additional rules:
  - No Potential Lapse Date or Projected Lapse Date before next due date
  - Premium holiday indicator NOT set
  - No reminder generated if TIP = 0 (occurs when ILP cover end date = maturity date)
- No reminder for policies with premiums paid in advance
- No reminder for policies under APL
- No reminder if suspense or APA sufficient for current premium due
- If Renewal Extraction Batch re-run due to CS application → premium reminder is **NOT** regenerated

---

### 3.5 Non-Forfeiture Option Disposal

**Purpose:** Handles policies that have not paid premium after grace period expires. System attempts auto-RPU, APL raising, APL lapse, or normal lapse in configured priority order.

**Prerequisites:**
- Renewal Batch Job has already run to attempt applying premium and moving due date
- Fee Status of policy is NOT 'Bank Transferring'
- No pending fund transaction
- Process Date ≥ (Premium Due Date + Grace Period) OR Process Date ≥ PLD
- Policy NOT frozen by CS or Claim

**System CANNOT lapse policy if:**
- Billing method = CPF Medisave AND manual CPF deduction in progress (billing status = 'outstanding' or 'transferring')
- Billing method = GIRO AND GIRO billing status = 'outstanding' (1st attempt only) → system will NOT lapse; trigger 2nd GIRO attempt instead
- GIRO has exhausted 2nd attempt AND reject codes NOT in (1160, 1201, 1237, 1041) → system suspends GIRO deduction (no lapse)

**Processing Steps (executed in order):**

**Step 1 — ILP: Deduct Rider Premium from TIV**
- Conditions: rider allowed to deduct from TIV AND TIV is sufficient
- Cumulated Interest fund (e.g., UL products): deduct directly from TIV
- Non-Cumulated Interest fund (e.g., ILP products): generate pending deduction records (price effective date = charge due date + price waiting days)
- TIV = total fund value − pending withdraw/switch-out + pending buy/switch-in (using latest fund price)

**Step 2 — Auto RPU (Reduced Paid Up)**
- Conditions: benefit allowed for auto RPU AND PUV (Reduced Paid Up Value) > 0
- Actions: keep policy status as Inforce; update premium status to 'Auto Paid Up'; update SA to PUV (effective from next premium due date)
- If conditions not met: skip

**Step 3 — APL Lapse**
- Conditions: main benefit NOT under WOP AND partial APL/premium has been performed AND system date ≥ PLD
- Actions: update benefit Risk Status = Lapse (lapse reason = APL Lapse, lapse date = PLD); if main benefit lapses → update policy status = Lapse (same reason and date)
- If conditions not met: skip

**Step 4 — Raise APL**
- Conditions: benefit surrender option = GSV AND GSV at Projection Date > 0 AND benefit allowed to raise APL
- If PLD ≥ NDD: raise APL for whole installment; capitalize existing APL balance; move NDD
- If PLD < NDD: raise partial APL; capitalize existing APL balance; set PLD on benefit
- Suspense/CB/SB repayment order for APL: Renew Suspense → General Suspense → CS Suspense → APA Suspense → CB Deposit (all options) → SB Deposit (all options)
- If conditions not met: skip

**Step 5 — Normal Lapse (if benefit allowed to force lapse)**

When benefit `allow auto surrender = Y`:

| CB/SB + Suspense + APA-PL-APL | Action |
|---|---|
| Positive AND ≥ 1 TIP | Withdraw to apply installment; move due date |
| Positive AND < 1 TIP | Calculate PLD; pro-rate premium; set PLD; withdraw; perform normal lapse when date ≥ PLD |
| NOT positive | Perform Normal Lapse immediately |

When benefit `allow auto surrender = N` (CB/SB not used):

| Suspense + APA-PL-APL | Action |
|---|---|
| Positive AND ≥ 1 TIP | Withdraw to apply installment; move due date |
| Positive AND < 1 TIP | Calculate PLD; pro-rate premium; set PLD; withdraw; perform normal lapse when date ≥ PLD |
| NOT positive | Perform Normal Lapse immediately |

**Normal Lapse Actions:**
- All benefits with Risk Status = 'Inforce' AND premium status = 'Regular':
  - Benefit Risk Status = Lapse
  - If benefit commencement date = benefit NDD → Lapse Reason = 'NTU'; otherwise Lapse Reason = 'Normal Lapse'; Lapse Date = NDD
- If main benefit lapses → Policy Status = Lapse (reason and date from main benefit)
- For benefits with indexation: set all indexation segment statuses = Lapse; cancel pending billing records for all segment premium; lapsed date of segment = benefit lapse date

**Key Calculation Formulas:**

*GSV Projection Date:*
```
Monthly payment frequency:      Projection Date = min(NDD + 3 installments, premium end date)
Non-monthly payment frequency:  Projection Date = NDD + 1 installment
```

*PLD Calculation:*
```
PLD = Projection Date − ((X × M × D) / (P × M + T))

Where:
  X = Total debts at Projection Date (APL + PL) − GSV at Projection Date
      (positive = CV not sufficient; negative = CV sufficient)
  M = Payment frequency installments (Monthly = 3; all others = 1)
  D = Days per installment (Monthly = 30; Quarterly = 91; Half Yearly = 182; Yearly = 365)
  P = TIP (Total Installment Premium on policy)
  T = APL/PL interest up to Projection Date
      T = Y1 × (1 − (1 + R1)^(−D×M/365)) + Y2 × (1 − (1 + R2)^(−D×M/365))
        Y1 = APL loan account value at Projection Date
        R1 = APL loan interest rate (based on effective date between NDD and Projection Date)
        Y2 = Policy loan account value at Projection Date
        R2 = Policy loan interest rate (based on effective date between NDD and Projection Date)
```

*Pro-rate Premium:*
```
Pro-rate premium = installment premium amount × (PLD − current due date) / D
```

---

### Policy Renew Confirm Waived (Batch)

**Purpose:** End-of-day renewal batch for premium-waived policies. Moves due dates, updates policy information, and recalculates next premium due amount.

**Prerequisites:**
- Policy Status is 'Inforce'
- Benefit premium status is Premium Waived
- Policy NOT frozen
- Premium Frequency is installment
- Installment premium has been extracted by Renewal Extraction Batch

**Procedures:**
1. Scheduled daily batch starts; extracts premium-waived policy benefits
2. System creates waived fee records:
   - Premium due date = current due date at benefit level
   - Premium status = Settled
   - Collection method = Insurer Payment
   - Amount = calculated amount
3. System creates payment record:
   - Collection method = Insurer Payment
   - Amount = calculated amount
   - Premium date = system date

---

### Policy Rider Auto Convert Payment Frequency (Batch)

**Purpose:** Automatically converts a rider's payment frequency to a new frequency at a configured policy month milestone (e.g., when main benefit becomes fully paid).

**Prerequisites:**
- Policy Status is Inforce
- Policy NOT frozen
- Main benefit premium status is Fully Paid
- All other optional riders: premium status = Fully Paid OR rider status = Terminated
- Target rider premium status is Regular or Premium Waived
- Configured in Configuration Table: Auto_Convert_Payment_Frequency_Cfg
- Months between rider's next premium due date and policy commencement date = Policy Month as configured

**Procedures:**
1. Scheduled daily batch starts; extracts policy riders to auto convert
2. System updates rider payment frequency to new payment frequency
   - If rider is a parent benefit with child riders (status not terminated, premium status Regular) → child rider frequencies updated accordingly
   - Main benefit and other optional riders: frequency NOT changed
3. System updates rider payment frequency to policy-level payment frequency
4. System updates rider's installment premium and outstanding premium per new frequency and product config
5. If pending billing records exist: cancel originals; generate new records based on new frequency and installment premium

**Configuration Table: Auto_Convert_Payment_Frequency_Cfg**

| Column | Description |
|---|---|
| MainProductCode | Applicable main product code |
| RiderCode | Target rider to convert |
| Policy Month | Months after commencement date at which conversion triggers |
| EffectiveDate | Effective date of the conversion |
| NewPayMode | Target payment frequency after conversion |

**Use Case Example:**
- Policy commencement: 2001/10/01; Rider C premium end date: 2099/09/30; Auto convert month = 180
- Client pays premium for NDD 2016/09/01 → Main Plan A and Rider B become Fully Paid
- System calculates months between 2016/10/01 and 2001/10/01 = 180 months → condition met
- Rider C payment frequency converted from Monthly to Yearly from NDD 2016/10/01

---

## Non-Forfeiture Use Cases Reference

| Case | Key Precondition | Expected Result |
|---|---|---|
| Case 1: Normal Lapse | Cash value = 0; grace period elapsed | Policy status = Lapsed |
| Case 2: Raise APL | Policy loan available > 1 TIP | APL raised; NDD moves; policy stays Inforce |
| Case 3: APL Lapse | Policy loan available < 1 TIP; partial APL done; date ≥ PLD | Policy status = APL Lapsed |
| Case 4: Raise APL + CB Repayment | Policy loan < 1 TIP; CB balance available | APL raised; CB used to repay APL; policy stays Inforce |

---

## Config Gaps Commonly Encountered in Renewal

| Scenario | Gap Type | Config Location |
|---|---|---|
| Premium notice leading days per frequency/channel/product | Config Gap | PremiumNoticeDays table |
| Premium reminder overdue days per frequency/channel/product | Config Gap | PremiumReminderNoticeDays table |
| Number of reminder sending times | Config Gap | PremiumReminderNoticeDays table → sending_times |
| Batch advance days for CB/SB/renewal | Config Gap | Batch_Advance_Days_Cfg table |
| Auto convert payment frequency rules per rider | Config Gap | Auto_Convert_Payment_Frequency_Cfg table |
| Allow apply premium before due date | Config Gap | System Parameter |
| Premium tolerance rate | Config Gap | Rate Table → Premium Tolerance |
| Allow premium collection for bankruptcy | Config Gap | System Parameter → Party Level |
| Leading time for renewal extraction | Config Gap | System Parameter → Renewal Leading Time |
| Grace period length | Config Gap | Product Factory → Non-Forfeiture Rules → Grace Period |
| Allow auto RPU | Config Gap | Product Factory → Traditional Rules → Allow Auto RPU |
| Allow raise APL | Config Gap | Product Factory → Traditional Rules → Allow APL |
| APL loan interest rate | Config Gap | Product Factory → Loan Rules → APL Interest Rate |
| GSV calculation method | Config Gap | Product Factory → Surrender Rules → GSV Method |

---

## Renewal Workflow (from Renewal UG V25.04)

### Renewal Batch Process
| Stage | Action |
|---|---|
| 1. Renewal Notice | System generates notice 30/60/90 days before anniversary |
| 2. Premium Due Reminder | SMS/Email to policyowner |
| 3. Renewal Premium Receipt | GIRO or manual collection |
| 4. Policy Status Update | Inforce if premium received |
| 5. Lapse Trigger | If premium not received within grace period |

### Grace Period
| Product Type | Grace Period |
|---|---|
| Traditional | 30/31 days from due date |
| ILP | 30/31 days (no grace - units redeemed if insufficient) |
| Shield | Per CPF terms |



## Renewal Lapse Rules (from Renewal UG)

### Lapse Trigger
| Condition | Outcome |
|---|---|
| Premium not received within grace period | Policy lapses |
| ILP fund value < min required | Policy lapses (reduced paid-up or surrender) |
| GIRO failed + retry exhausted | Policy enters lapse workflow |

### Reduced Paid-Up (RPU)
- Triggered if: policy has RPU option and surrender value > 0
- SA reduced proportionally
- No further premiums required
- ILP: units redeemed for charges


## INVARIANT Declarations (Renewal Module)

```
INVARIANT 1: Renewal extraction cannot proceed if policy is frozen by CS or Claims
  Enforced at: Extract Amount to Bill (Batch)
  Effect: Policy excluded from extraction; no billing record created

INVARIANT 2: Premium notice is NOT generated if suspense/APA covers current premium due
  Enforced at: Generate Premium Notice (Batch)
  Effect: Premium notice suppressed for that policy

INVARIANT 3: Renew Confirmation cannot move due date if policy is frozen
  Enforced at: Apply Premium and Move Due Date (Batch)
  Effect: Policy excluded from due date movement batch

INVARIANT 4: Non-forfeiture disposal requires grace period to have elapsed
  Enforced at: Non-Forfeiture Option Disposal
  Effect: Policy not extracted; no lapse/APL action taken until condition met

INVARIANT 5: GIRO/CPF policies with active deduction in progress cannot be lapsed
  Enforced at: Non-Forfeiture Option Disposal
  Effect: Policy skipped; 2nd GIRO attempt triggered instead of lapse

INVARIANT 6: Investment Bucket Filling Product excluded from Extract Amount to Bill batch
  Enforced at: Extract Amount to Bill (Batch)
  Effect: Product type skipped entirely; not applicable

INVARIANT 7: Premium reminder is NOT regenerated when Renewal Extraction re-runs due to CS application
  Enforced at: Generate Premium Reminder Notice (Batch)
  Effect: Existing reminder record retained; no duplicate generated
```

---

## ⚠️ Limitations & Unsupported Scenarios

> This section documents known limitations and scenarios NOT supported by the system. Updated: 2026-03-14

### Renewal Process

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Auto-Renewal | Limited | Config | Check product configuration |
| Renewal Bonus | Not automated | Config | Manual bonus allocation |
| Continuous Renewal | Fixed terms | Config | Custom renewal terms need development |

### Lapse & Reinstatement

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Reinstatement Rules | Fixed | Config | Complex rules need customization |
| Conditional Lapse | Limited | Config | Check product factory |
| Grace Period | Fixed | Config | Custom grace periods limited |

### Non-Forfeiture Options

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| RPU (Reduced Paid-Up) | Traditional only | Code | ILP products not supported |
| Extended Term | Limited | Config | Check product configuration |
| Automatic Options | Fixed triggers | Config | Custom triggers need development |

### Indexation

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| CPI Indexation | Requires CPI rate config | Config | Manual rate updates needed |
| Custom Index | Not supported | Code | Custom indices require development |
| Indexation Formula | Fixed | Config | Custom formulas need development |

---

## Related Files

| File | Purpose |
|---|---|
| `ps-customer-service.md` | CS module; CS freeze status directly affects renewal extraction and due date movement |
| `ps-bonus.md` | CB/SB allocation; CB/SB used to repay APL during non-forfeiture disposal |
| `ps-product-factory.md` | Product-level config: grace period, RPU, APL flags, indexation, GSV method |
| `insuremo-ootb-full.md` | OOTB capability classification (use for Gap Analysis) |
| `output-templates.md` | BSD output templates for renewal-related gaps |