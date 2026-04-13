# InsureMO Platform Guide — Perform Annuity Payment
# Source: Perform Annuity Payment User Guide V25.04
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb-full.md instead
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"how does Annuity Payment processing work in InsureMO"** — batch job sequences, prerequisites, and business logic for annuity payable execution and annuity notice generation.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for an Annuity-related gap
- Agent 6 is generating a **Config Runbook** for annuity payment items
- A BA needs to verify what **preconditions** or **advance days configuration** governs annuity payable extraction

---

## Module Overview

```
Perform Annuity Payment
│
├── Annuity Payable Execution (Weekly Batch)    ← Extracts annuity pay plan; generates payable records
├── Annuity Notice Generation (Daily Batch)     ← Generates and prints annuity notices to policyholders
└── Annuity Payout (Batch)                      ← Generates annuity payment records for eligible policies
```

---

## Annuity Payment Workflow — Standard Sequence

```
Step 1: Annuity Payable Execution (Weekly Batch)
  └─► Step 2: Annuity Notice Generation (Daily Batch)
        └─► Step 3: Annuity Payout (Batch)
              └─► Payment disbursed to policyholder
```

**Annuity definition:** Sum of money paid each year (or per installment) by the life insurance company during the lifetime of the insured. Typically used for pension products and paid in installments.

---

## Per-Process Reference

### Annuity Payable Execution (Weekly Batch)

**Purpose:** Weekly batch that extracts annuity pay plan information for eligible policies and generates policy payable records after annuity allocation.

**Prerequisites:**
- Policy Status is 'Inforce'
- Policy NOT frozen
- Next annuity due date ≤ system date + days in advance (configured in Batch_Advance_Days_Cfg)

**Procedures:**
1. On a **weekly** basis, system extracts policies eligible for annuity payable execution
2. System checks annuity due date:
   - If system date < bonus due date − advance days → end
   - If system date ≥ bonus due date − advance days → proceed
   
   > Advance days configured in Configuration Table: **Batch_Advance_Days_Cfg**

3. System updates policy annuity information:
   - Update annuity next due date
   - Update annuity plan information
   - Update annuity allocation information
   - Generate annuity payable record

---

### Annuity Notice Generation (Daily Batch)

**Purpose:** Generates and prints annuity notices to inform policyholders of upcoming annuity payable amounts after annuity payable records have been extracted.

**Prerequisites:**
- Annuity Payable Execution batch has run; no annuity notice yet generated for this extraction

**Procedures:**
1. Daily batch starts; extracts policies requiring annuity notice
2. System retrieves and consolidates relevant policy information
3. System generates and prints annuity notice

---

## Config Gaps Commonly Encountered in Annuity Payment

| Scenario | Gap Type | Config Location |
|---|---|---|
| Annuity batch advance days | Config Gap | Batch_Advance_Days_Cfg table |
| Annuity payout frequency / schedule | Config Gap | Product Factory → Annuity Rules → Annuity Pay Plan |
| Annuity amount calculation method | Config Gap | Product Factory → Annuity Rules → Annuity Calculation |
| Annuity notice template | Config Gap | Letter Management → Annuity Notice Template |
| Disbursement method for annuity payout | Config Gap | Policy Level → Disbursement Method; PA_Def_Refund_Payee |

---

## Annuity Benefit Rules (from Annuity UG V25.04)

### Annuity Types
| Type | Trigger | Payment |
|---|---|---|
| Immediate Annuity | Starts immediately after premium payment | Monthly/Quarterly/Annual |
| Deferred Annuity | Starts after deferment period | Monthly/Quarterly/Annual |
| Survival Benefit | Policy anniversary (if alive) | Per schedule |
| Annuity Certain | Fixed number of payments regardless of status | Per schedule |

### Vesting Conditions
- Annuitant must be alive at vesting date
- Policy must be in-force
- No outstanding loans exceeding SV
- No outstanding premiums


## INVARIANT Declarations (Annuity Module)

```
INVARIANT 1: Annuity payable execution cannot proceed if policy is frozen
  Enforced at: Annuity Payable Execution (Weekly Batch)
  Effect: Policy excluded from weekly extraction run

INVARIANT 2: Annuity notice is not generated if payable extraction has not yet run for the current cycle
  Enforced at: Annuity Notice Generation (Daily Batch) — prerequisite check
  Effect: Notice batch defers; no duplicate notices generated

INVARIANT 3: Annuity payable records only generated when next annuity due date is within configured advance days
  Enforced at: Annuity Payable Execution (Weekly Batch)
  Effect: Early extraction prevented; batch re-checks each weekly cycle until condition met
```

---

## ⚠️ Limitations & Unsupported Scenarios

> This section documents known limitations and scenarios NOT supported by the system. Updated: 2026-03-14

### Annuity Types

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Custom Annuity Formulas | Fixed calculation methods | Config | Cannot create custom formulas |
| Variable Annuity | Limited support | Config | Check product configuration |
| Index-Linked Annuity | Not typically supported | Code | Requires custom development |

### Payment Frequency

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Custom Payment Schedules | Fixed frequencies | Config | Weekly/Monthly/Quarterly/Yearly only |
| Real-time Payment | Batch processing only | Config | No real-time payout |

### Survivorship

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Joint-Life Annuity | Limited configurations | Config | Check product factory settings |
| Survivorship Calculation | Fixed methods | Config | Custom methods need development |

---

## Related Files

| File | Purpose |
|---|---|
| `ps-bonus.md` | SB/CB cash payment process is structurally similar; both use Batch_Advance_Days_Cfg and generate payable records |
| `ps-customer-service.md` | CS freeze status affects annuity payable extraction eligibility |
| `ps-product-factory.md` | Product-level annuity rules: pay plan, calculation method, payout frequency |
| `insuremo-ootb-full.md` | OOTB capability classification (use for Gap Analysis) |
| `output-templates.md` | BSD output templates for annuity-related gaps |