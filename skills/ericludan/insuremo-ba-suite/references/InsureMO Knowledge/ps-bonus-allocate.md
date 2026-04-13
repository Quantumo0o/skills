# InsureMO Platform Guide — Declare and Allocate Bonus
# Source: Declare and Allocate Bonus User Guide V25.04
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb-full.md instead
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"how does Bonus and Survival Benefit allocation work in InsureMO"** — batch job sequences, prerequisites, payout options, calculation rules, and business logic for Cash Bonus (CB), Reversionary Bonus (RB), and Survival Benefit (SB) allocation.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for a CB/RB/SB-related gap
- Agent 6 is generating a **Config Runbook** for bonus or survival benefit items
- A BA needs to verify what **preconditions** or **payout option logic** the system enforces during bonus/SB allocation

---

## Module Overview

```
Declare and Allocate Bonus
│
├── Cash Bonus (CB) Allocation (Batch)          ← Yearly CB allocation; CB account update; payout logic
├── Reversionary Bonus (RB) Allocation (Batch)  ← Accumulative RB update; no immediate cash payout
├── Survival Benefit (SB) Allocation (Batch)    ← SB plan creation + payout scheduling
├── SB/CB in Cash Payment (Batch)               ← Option 1 cash disbursement execution
└── Cancel SB/CB Cash Payment (Batch)           ← Auto-cancellation of unconfirmed payment records
```

---

## Bonus Types Overview

| Type | Description | When Payable |
|---|---|---|
| Cash Bonus (CB) | Extra amount expressed as % of SA; paid as cash | When declared (typically yearly) |
| Reversionary Bonus (RB) | Added back to policy to enhance coverage and maturity value | On policy maturity only (cannot be withdrawn as cash) |
| Survival Benefit (SB) | Fixed amount paid at pre-configured intervals upon insured's survival | At configured interval dates |

---

## CB / SB Payout Options

| Option | Label | Description |
|---|---|---|
| Option 1 | To receive SB/CB by Payout | System performs cash withdrawal from CB/SB account; disbursed to payee |
| Option 2 | To use SB/CB to pay premium | CB/SB used to repay PL/APL first; if no PL/APL, stays in account and earns interest |
| Option 3 | To leave SB/CB on deposit with Company | CB/SB stays in account and earns interest year on year |

---

## Per-Process Reference

### Cash Bonus (CB) Allocation (Batch)

**Purpose:** Daily batch that calculates and allocates cash bonus to eligible policy benefits; updates CB account balance and next bonus due date; executes payout option logic.

**Prerequisites — Eligible Policies:**
- Policy Status is 'Inforce'
- Policy NOT frozen

**Prerequisites — Eligible Benefits:**
- Policy benefit is Inforce
- Policy benefit is a Cash Bonus product
- Premium status is Regular, Fully Paid, or Premium Waived
  - **Excluded:** Reduced Paid Up / Auto Paid Up / ETA / PHD / Stop Payment
- Premium status Regular or Premium Waived: next premium due date ≥ next bonus due date
- Next bonus due date ≤ system date + days in advance (configured in Batch_Advance_Days_Cfg)
- Corresponding cash bonus rate can be found

**Procedures:**
1. Scheduled daily batch starts
2. System checks if current system date ≥ bonus due date − advance days; if not → end
3. System checks 'No. of Completed Policy Years for CB Becoming Payable' (configured at product level):
   - Within configured years → no CB calculated; batch record generated in CS info; end
   - Beyond configured years → proceed to calculate and allocate CB; update year CB allocated indicator N → Y
4. System calculates bonus amount per product configuration
5. System updates next bonus due date = original next bonus due date + 1 year
6. System applies payout option logic (see table below)
7. System generates cash bonus annual statement
8. Option 1 only: finance performs payment to client (refer to SB/CB in Cash Payment section)

**Payout Option Logic:**

| Option | CB Account Action | APL/PL Handling |
|---|---|---|
| Option 1 — Cash Payout | Withdrawal from CB account; disbursed to payee | APL/PL offset first before payout |
| Option 2 — Pay Premium | If PL/APL exists → use CB to repay PL/APL; if no PL/APL → CB stays in account with interest | CB offsets APL first, then PL |
| Option 3 — Leave on Deposit | CB remains in CB account; earns interest year on year | CB offsets APL/PL if balance available |

**CB/SB APL/PL Offset Rule (applies to all options):**
- System uses CB/SB balance to offset APL and PL before any other action
- Offset account order: Cash Bonus account first, then Survival Benefit account
- Repayment debt order: APL account first, then PL account

**CB Account Interest Calculation** (configured in Product Factory / LIMO):

| Dimension | Supported Values |
|---|---|
| Interest Calculation Type | Compound Interest / Simple Interest |
| Interest Frequency | Not Relevant / Yearly / Half Yearly / Quarterly / Monthly / Daily / Single |
| Interest Calculation Due Type | Calendar End / Policy / Account Creation Date / Calendar Begin |
| Capitalization Frequency | Not Relevant / Yearly / Half Yearly / Quarterly / Monthly / Daily / Single |
| Capitalization Due Type | Calendar End / Policy / Account Creation Date / Calendar Begin |
| First Deduct From | Interest / Principal |

---

### Reversionary Bonus (RB) Allocation (Batch)

**Purpose:** Daily batch that calculates and accumulates reversionary bonus for eligible policy benefits; updates accumulative RB and next bonus due date.

**Prerequisites — Eligible Policies:**
- Policy Status is 'Inforce'
- Policy NOT frozen

**Prerequisites — Eligible Benefits:**
- Policy benefit is Inforce
- Policy benefit is a Reversionary Bonus product
- Premium status is Regular, Fully Paid, or Premium Waived
  - **Excluded:** Reduced Paid Up / Auto Paid Up / ETA / PHD / Stop Payment
- Next bonus due date ≤ system date + days in advance
- Corresponding reversionary bonus rate can be found
- First bonus next due date = commencement date + 1 year (set at policy issue)

> **NOTE:** RB allocation batch **must run on a working day**. If bonus due date falls on a non-working day, allocation runs on the next working day. Holiday schedule must be pre-defined in system.

**Procedures:**
1. Scheduled daily batch starts
2. System calculates bonus amount per product configuration
3. System updates accumulative reversionary bonus:
   - Accumulative RB = original accumulative RB + latest RB amount
4. System updates next bonus due date = original next bonus due date + 1 year
5. System generates new Bonus Payment Allocation Record (Allocation Type = Reversionary Bonus Allocate)

**Key Business Rules:**

| Scenario | Rule |
|---|---|
| No RB rate declared for policy year of Bonus Due Date | Use latest rate from last declared year |
| Reversal of RB allocation | Generate new negative Bonus Payment Allocation Record; roll back Bonus Next Due Date and Accumulated RB |
| Policy lapsed → reinstated | RB allocation suspended during lapsed period; upon reinstatement, re-allocate all RB from latest RB due date to next due date after reinstatement; missing year rates use last declared year's rate |
| Interim Bonus (on surrender / maturity / death claim) | Calculated when premium status = Regular / Fully Paid / Premium Waived only |

**Interim Bonus Formula:**
```
Interim Bonus = latest reversionary bonus × adjusted months / 12
  (Adjusted months formula defined in product parameter list; hardcoded in backend)
```

**Lapse / Reinstatement Allocation Example:**
- Policy lapses 2021; reinstates 2023; latest RB due date = 2021
- Year 2020: rate X declared; Year 2021: no rate; Year 2022: rate Y declared
- After reinstatement: RB for due 2021 uses rate X; RB for due 2022 uses rate Y

---

### Survival Benefit (SB) Allocation (Batch)

**Purpose:** Daily batch that creates SB plans (if not yet created), allocates survival benefit amounts, updates SB account, and schedules future payout dates.

**Prerequisites — Policy Level:**
- Payment start date of Survival Benefit is confirmed
- Disbursement method of survival benefit is confirmed
- Policy Status is 'Inforce'
- Policy NOT frozen

**Prerequisites — Benefit Level:**
- Policy benefit is Inforce
- Premium status is Regular, Fully Paid, or Premium Waived
  - **Excluded:** Reduced Paid Up / Auto Paid Up / ETA / PHD / Stop Payment
- Policy benefit is entitled to survival benefit (both main product and rider supported)
- If existing SB plan present: plan status = Active AND SB payment end date ≥ system date
- Next SB payout date ≤ system date + days in advance (configured in Batch_Advance_Days_Cfg)

**Procedures:**
1. Scheduled daily batch starts
2. System checks if current system date ≥ next SB payout date − advance days; if not → end
3. If no SB plan exists → system creates SB plan
4. System updates plan details:
   - Latest SB amount = new amount calculated by product
   - If this is the last installment → set SB plan status to Inactive; end
   - If not last installment → update next SB payment date
5. System applies payout option logic (same Options 1, 2, 3 as CB)
6. CB/SB balance used to offset APL/PL first (CB first, then SB; APL first, then PL)
7. Option 1 only: finance performs payment to client (refer to SB/CB in Cash Payment section)

**SB Account Interest Calculation:** Same dimensions as CB account interest (configured in Product Factory / LIMO — see CB section above).

---

### SB/CB in Cash Payment (Batch)

**Purpose:** Daily batch that executes cash disbursements for policyholders with CB/SB payout option = 1 (To receive SB/CB by payout).

**Prerequisites:**
- Policy Status is 'Inforce'
- Policy NOT frozen
- CB/SB payout option = 1 (To receive SB/CB by Payout)
- CB/SB Allocation batch has run successfully AND allocation amount > 0
- CB/SB due date ≤ system date + Advance Days (configured in Batch_Advance_Days_Cfg)

**Disbursement Payee Rules** (configured in PA_Def_Refund_Payee):

| Policy Condition | Default Benefit Payee |
|---|---|
| Policy Holder only (no trustee, no assignee) | Policy Holder |
| Trustee present, no assignee | Latest Trustee (if multiple trustees exist) |
| Assignee present, no trustee | Assignee |

- Disbursement method of benefit pay plan payee follows policy-level disbursement method
- For CS: Change Disbursement Method → new method applied to refund payee and pay plan payee accordingly

**Disbursement Method Rules:**

*If policy-level disbursement method is blank:*

| Criteria | System Action |
|---|---|
| Amount ≤ 200K AND currency = SGD AND payee ID type = NRIC / FIN / UEN | Default disbursement method = PayNow; flow to Payment Authorization |
| Amount > 200K OR currency ≠ SGD OR payee ID type ≠ NRIC / FIN / UEN | Set disbursement method = 'No Disbursement Method'; flow to Payment Requisition for manual requisition |

*If policy-level disbursement method is NOT blank:*
- System uses the policy-level disbursement method to generate payment records

---

### Cancel SB/CB Cash Payment (Batch)

**Purpose:** Daily batch that auto-cancels unconfirmed SB/CB payment records after a configured number of days; converts the amount to deposit balance.

**Prerequisites:**
- CB/SB payout option = 1 (To receive SB/CB by Payout)
- SB/CB Cash Payment batch has already run; payment records have been generated
- Payment status is NOT 'Payment Confirmed' or 'Bank Transferring'
- Process date = CB/SB Payment Generation Date + Auto Cancellation Days (configured in Batch_Advance_Days_Cfg)

**Procedures:**
1. Scheduled daily batch starts
2. System cancels original payment records
3. System inserts new receivable record (Payment Method = Internal Transfer) to transfer CB/SB payable amount into CB/SB deposit balance
4. System records CB/SB last due date = CB/SB create date; calculates deposit interest from create date
5. Auto cancellation rule applies to both manual CB/SB payments and auto batch payments
6. Once cancelled by auto cancellation: original CB/SB auto payment cannot be re-triggered until next CB/SB allocation cycle (without the original CB/SB balance)

---

## CB/SB Use Cases Summary

### Cash Bonus Use Cases

| Case | Payout Option | Key Behaviour |
|---|---|---|
| Case 1 | Option 1 — Cash Payout | CB withdrawn each year; CB balance = 0 after payout |
| Case 2 | Option 2 — Pay Premium | CB accumulates with interest; used to repay APL when APL is raised; balance = 0 after APL repayment |
| Case 3 | Option 3 — Leave on Deposit | CB accumulates with interest; remains in account |

**CB Calculation Example (SA = 10,000):**

| Process Date | CB Option | Latest Bonus Amount | CB Balance |
|---|---|---|---|
| 2024-10-11 | Option 1 | 10,000 × 0.0031 = 310.00 | 0 (after withdrawal) |
| 2024-10-11 | Option 2 | 10,000 × 0.0031 = 310.00 | 310.00 (stays; earns interest) |
| 2024-10-11 | Option 3 | 10,000 × 0.0031 = 310.00 | 310.00 (stays; earns interest) |

### Survival Benefit Use Cases

| Case | Payout Option | Key Behaviour |
|---|---|---|
| Case 1 | Option 1 — Cash Payout | SB withdrawn each period; SB balance = 0 after payout |
| Case 2 | Option 2 — Pay Premium | SB accumulates with interest; used to repay APL when raised; balance = 0 after APL repayment |
| Case 3 | Option 3 — Leave on Deposit | SB accumulates with interest; remains in account |

**SB Calculation Example (SA = 10,000; SB rate = 11.104/1,000):**

| Process Date | New SB Amount | SB Balance (Option 3) |
|---|---|---|
| 2023-10-11 | 10,000 × 11.104/1,000 = 1,110.40 | 1,110.40 |
| 2024-10-11 | 10,000 × 11.104/1,000 = 1,110.40 | 1,110.40 + 11.13 (interest) + 1,110.40 = 2,231.93 |
| 2025-10-11 | 10,000 × 11.104/1,000 = 1,110.40 | 2,231.93 + 22.35 (interest) + 1,110.40 = 3,364.68 |

---

## Config Gaps Commonly Encountered in Bonus / SB Module

| Scenario | Gap Type | Config Location |
|---|---|---|
| CB/SB batch advance days | Config Gap | Batch_Advance_Days_Cfg table |
| CB/SB auto cancellation days | Config Gap | Batch_Advance_Days_Cfg table |
| No. of completed policy years for CB becoming payable | Config Gap | Product Factory → CB Rules → Payable Year |
| Default CB/SB payout option | Config Gap | Product Factory → CB/SB Rules → Default Payout Option |
| CB account interest calculation type / frequency | Config Gap | Product Factory (LIMO) → Policy Account Rules |
| SB account interest calculation type / frequency | Config Gap | Product Factory (LIMO) → Policy Account Rules |
| SB payout start date / interval / end date | Config Gap | Product Factory → SB Rules → Survival Benefit Plan |
| Reversionary bonus rate table | Config Gap | Product Factory → RB Rate Table |
| Holiday schedule for RB allocation batch | Config Gap | System → Holiday Calendar |
| Interim bonus adjusted months parameter | Config Gap | Product Factory → Parameter List |
| Disbursement payee default rules | Config Gap | PA_Def_Refund_Payee configuration table |
| PayNow auto-default threshold (200K / SGD / NRIC/FIN/UEN) | Config Gap | Payment Disbursement System Parameter |

---

## Bonus Types (from Bonus UG V25.04)

### Reversionary Bonus
- Declared annually as % of Sum Assured
- Attached to policy immediately upon declaration
- Reduces on surrender (not guaranteed)

### Non-Nevigation (N-Bonus)
- Terminal bonus declared at surrender/maturity/death
- Based on performance of participating fund
- Not attached until event occurs

### Bonus Declaration Process
1. Actuarial team declares bonus rate per product
2. System calculates bonus per policy
3. Bonus notice generated
4. Bonus attached to policy record


## INVARIANT Declarations (Bonus / SB Module)

```
INVARIANT 1: CB/SB/RB allocation cannot proceed if policy is frozen
  Enforced at: Cash Bonus / SB / RB Allocation (Batch)
  Effect: Policy excluded from allocation run

INVARIANT 2: CB/SB allocation only proceeds when next bonus due date is within configured advance days
  Enforced at: Cash Bonus / SB Allocation (Batch)
  Effect: Early allocation prevented; batch re-checks each day until condition met

INVARIANT 3: Reduced Paid Up / Auto Paid Up / ETA / PHD / Stop Payment benefits excluded from CB/SB/RB allocation
  Enforced at: All bonus allocation batches
  Effect: Benefit not eligible; skipped in batch run

INVARIANT 4: CB/SB balance used to offset APL/PL before any payout or deposit action
  Enforced at: CB / SB Allocation (Batch) — all payout options
  Offset order: CB account first → SB account; APL first → PL

INVARIANT 5: RB allocation batch must execute on a working day
  Enforced at: Reversionary Bonus Allocation (Batch)
  Effect: Non-working day due dates shifted to next working day per holiday calendar

INVARIANT 6: Cancelled SB/CB payment cannot re-trigger auto payment until next allocation cycle
  Enforced at: Cancel SB/CB Cash Payment (Batch)
  Effect: Original CB/SB auto payment suppressed after cancellation; amount converted to deposit balance

INVARIANT 7: CB allocation skipped if policy is within 'No. of Completed Policy Years for CB Becoming Payable'
  Enforced at: Cash Bonus Allocation (Batch)
  Effect: No bonus calculated or allocated; batch record generated in CS info; process ends
```

---

## ⚠️ Limitations & Unsupported Scenarios

> This section documents known limitations and scenarios NOT supported by the system. Updated: 2026-03-14

### Bonus Types

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Custom Bonus Types | Fixed types only | Config | Reversionary/Compound/Simple types |
| Terminal Bonus | Not automated | Config | Manual allocation required |
| Interim Bonus | Limited | Config | Check product configuration |

### Allocation Rules

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Dynamic Allocation | Fixed formulas | Config | Custom allocation logic needs development |
| Retroactive Bonus | Not supported | Code | Past period adjustments limited |
| Bonus Rate Override | Limited | Config | Manual override capability restricted |

### Surrender Value

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Complex SV Calculation | Fixed methods | Config | Custom SV formulas need development |
| Market Value Adjustment | Limited | Config | MVA requires customization |

---

## Related Files

| File | Purpose |
|---|---|
| `ps-renewal.md` | Renewal process; CB/SB used to repay APL during Non-Forfeiture Option Disposal |
| `ps-customer-service.md` | CS module; CS freeze status affects CB/SB allocation eligibility; Change Disbursement Method affects payee |
| `ps-product-factory.md` | Product-level config: CB/SB rules, RB rate tables, SB plan, interest rules, policy account config |
| `insuremo-ootb-full.md` | OOTB capability classification (use for Gap Analysis) |
| `output-templates.md` | BSD output templates for bonus/SB-related gaps |