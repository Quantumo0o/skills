# InsureMO Platform Guide — Manage Loan and Deposit
# Source: Manage Loan and Deposit User Guide V25.04
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb-full.md instead
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"how does Policy Loan, APL, and Deposit Account interest calculation and capitalization work in InsureMO"** — batch triggers, eligibility criteria, interest formulas, and the distinction between interest settlement and interest capitalization.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for a Loan/Deposit interest-related gap
- Agent 6 is generating a **Config Runbook** for policy account interest items
- A BA needs to verify what **interest calculation type**, **capitalization frequency**, or **rate lookup logic** applies to a specific account type

---

## Module Overview

```
Manage Loan and Deposit
│
└── Deposit and Loan Account Interest Settlement and Capitalization (Batch)
      ├── Interest Settlement    ← Calculates interest accrued since last settlement date
      └── Interest Capitalization ← Adds accumulated interest into principal balance
```

---

## Account Types Overview

| Account Category | Account Types | Product Scope | Description |
|---|---|---|---|
| Policy Loan Accounts | Policy Loan Account | Whole Life / Endowment | Loan borrowed against cash value; interest accrues on outstanding balance |
| Policy Loan Accounts | APL Account (Auto Premium Loan) | Whole Life / Endowment | Auto-generated when premium overdue; prevents lapse by borrowing against policy value; reduces future cash value |
| Policy Deposit Accounts | Cash Bonus Account | Whole Life / Endowment | Stores CB principal; earns interest if option 2 (pay premium) or option 3 (leave on deposit) |
| Policy Deposit Accounts | Survival Benefit Account | Whole Life / Endowment | Stores SB principal; earns interest if option 2 or option 3 |

---

## Deposit and Loan Account Interest Settlement and Capitalization (Batch)

**Purpose:** Daily batch that calculates and capitalizes interest on policy loan and deposit accounts per configured rules.

### Prerequisites — Interest Settlement

**Trigger types:**
- Regular Batch Trigger (daily scheduled)
- Ad-hoc Batch Trigger (triggered by any of the following):
  - Survival Benefit, Cash Bonus, or Advance Payment account withdrawal performed
  - APL or Policy Loan repayment performed

**Eligible Policies:**
- Policy Status is 'Inforce'
- Policy NOT frozen
- Policy has active policy deposit account OR loan account
- Deposit account value (= Deposit Capitalization Amount) > 0 OR Loan account value (= Loan Capitalization Principal) > 0
- At least one monthly end date exists between latest interest settlement date and system date

### Prerequisites — Interest Capitalization

**Eligible Policies:**
- Policy Status is 'Inforce'
- Policy NOT frozen
- Policy has active policy deposit account OR loan account
- Deposit account value (= Deposit Capitalization Amount + Interest Balance) > 0 OR Loan account value (= Loan Capitalization Principal) > 0

### Procedures

1. On a daily basis, system extracts policies eligible for interest settlement or capitalization
2. **For Interest Settlement:**
   - System arranges interest settlement dates between latest settlement date and system date in ascending order
   - System calculates interest from earliest to latest date
   - Settlement configuration applied per account type (configured in Product Factory / LIMO)
3. **For Interest Capitalization:**
   - System arranges capitalization dates between latest capitalization date and system date in ascending order
   - System performs capitalization from earliest to latest date
   - Capitalization configuration applied per account type (configured in Product Factory / LIMO)

---

## Interest Calculation Rules

### Interest Formulas

| Calculation Type | Formula |
|---|---|
| Simple Interest | `P × i × d / 365` |
| Compound Interest | `P × [(1 + i) ^ (d/365) − 1]` |

**Formula Parameters:**

| Parameter | Description |
|---|---|
| P | Principal (Capitalization Principal for loan; Deposit or Withdraw Principal for deposit account) |
| i | Interest rate defined in interest rate table `t_service_rate` (looked up per Interest Rate Type — see below) |
| d | Current interest settlement date − Last interest settlement date (number of days between start and end date) |

### Interest Rate Type Lookup Logic

| Rate Type | Lookup Rule | Example |
|---|---|---|
| Creation Date | Use interest rate based on account creation date; rate does NOT change even if rate table is updated | Deposit interest = P × i1 × d1 / 365 (single rate used throughout) |
| Due Date | Check for rate changes between start date and end date; use applicable rate for each segment | Deposit interest = P × i1 × d1/365 + P × i2 × d2/365 (split by rate effective date) |

Interest rate table reference: `t_service_rate`
Interest rate type reference: `t_policy_account_type`

### Interest Configuration Dimensions (Product Factory / LIMO)

| Dimension | Supported Values |
|---|---|
| Interest Calculation Type | Compound Interest / Simple Interest |
| Interest Frequency | Not Relevant / Yearly / Half Yearly / Quarterly / Monthly / Daily / Single |
| Interest Calculation Due Type | Calendar End / Policy / Account Creation Date / Calendar Begin |
| Capitalization Frequency | Not Relevant / Yearly / Half Yearly / Quarterly / Monthly / Daily / Single |
| Capitalization Due Type | Calendar End / Policy / Account Creation Date / Calendar Begin |
| First Deduct From | Interest / Principal |

---

## Key Business Rule — Interest Capitalization is Batch-Only

> Interest can only be capitalized into principal through the configured capitalization batch. No other system action triggers automatic capitalization.

**Actions that trigger interest calculation WITHOUT triggering capitalization:**
- Loan Repayment
- Apply Policy Loan
- Raise APL
- CB/SB Allocation

This means: after any of the above actions, interest is recalculated and updated, but the accumulated interest balance is NOT merged into principal until the next capitalization batch run.

---

## Config Gaps Commonly Encountered in Loan and Deposit

| Scenario | Gap Type | Config Location |
|---|---|---|
| Interest calculation type per account (Simple / Compound) | Config Gap | Product Factory (LIMO) → Policy Account Type → Interest Calculation Type |
| Interest frequency per account | Config Gap | Product Factory (LIMO) → Policy Account Type → Interest Frequency |
| Interest calculation due type per account | Config Gap | Product Factory (LIMO) → Policy Account Type → Interest Calculation Due Type |
| Capitalization frequency per account | Config Gap | Product Factory (LIMO) → Policy Account Type → Capitalization Frequency |
| Capitalization due type per account | Config Gap | Product Factory (LIMO) → Policy Account Type → Capitalization Due Type |
| First deduct from (Interest vs Principal) | Config Gap | Product Factory (LIMO) → Policy Account Type → First Deduct From |
| Interest rate for policy loan / APL account | Config Gap | Interest Rate Table `t_service_rate` → Loan Account Rate |
| Interest rate for CB / SB deposit account | Config Gap | Interest Rate Table `t_service_rate` → Deposit Account Rate |
| Interest rate type (creation date vs due date) | Config Gap | `t_policy_account_type` → Rate Type |
| APL allowed (Y/N) | Config Gap | Product Factory → Traditional Rules → Allow APL |
| Policy loan allowed (Y/N) | Config Gap | Product Factory → Loan Rules → Policy Loan Allowed |

---

## Policy Loan Rules (from Loan UG V25.04)

### Loan Eligibility
| Rule | Value |
|---|---|
| Max Loan % | 80-90% of SV/Cash Value (product config) |
| Min Loan Amount | Product-defined minimum |
| Interest Rate | Product-defined (compounding or simple) |
| Loan Repayment | Via GIRO or manual payment |

### Loan Impact on Benefits
| Benefit | Loan Impact |
|---|---|
| Death Benefit | Net = SA − Outstanding Loan |
| Surrender Value | Net = SV − Outstanding Loan − Loan Interest |
| Maturity Benefit | Net = Maturity Value − Outstanding Loan |
| Revival | Loan must be repaid or waived |



## INVARIANT Declarations (Loan and Deposit Module)

```
INVARIANT 1: Interest settlement and capitalization cannot proceed if policy is frozen
  Enforced at: Deposit and Loan Account Interest Settlement and Capitalization (Batch)
  Effect: Policy excluded from interest batch run

INVARIANT 2: Interest settlement requires at least one monthly end date between latest settlement date and system date
  Enforced at: Interest Settlement prerequisite check
  Effect: No settlement performed if condition not met; batch defers to next eligible date

INVARIANT 3: Interest capitalization is ONLY performed by the capitalization batch
  Enforced at: All ad-hoc actions (loan repayment, APL raise, CB/SB allocation)
  Effect: Interest calculated but NOT capitalized during ad-hoc triggers; capitalization deferred to next batch run

INVARIANT 4: Deposit account value must be > 0 for settlement; Deposit Capitalization Amount + Interest Balance must be > 0 for capitalization
  Enforced at: Eligibility check
  Effect: Zero-balance accounts excluded from processing

INVARIANT 5: Interest rate for 'creation date' type accounts does NOT change after account creation even if rate table is updated
  Enforced at: Interest calculation (rate lookup)
  Effect: Account locked to creation-date rate for its full lifetime
```

---

## ⚠️ Limitations & Unsupported Scenarios

> This section documents known limitations and scenarios NOT supported by the system. Updated: 2026-03-14

### Policy Loan

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Loan for ILP Products | Not supported | Code | Policy loan only for Traditional products |
| Variable Loan Rate | Fixed rates | Config | Rate changes require configuration |
| Loan Security | Basic collateral | Config | Complex collateral not supported |

### Deposit Accounts

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Custom Deposit Types | Fixed types only | Code | Cannot create new deposit account types |
| Interest Formulas | Fixed (Simple/Compound) | Code | Custom formulas not available |
| Real-time Interest | Batch processing | Config | Interest calculated via batch |

### APL (Auto Premium Loan)

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Single Premium Policies | Not supported | Code | APL only for regular premium |
| Partial APL | Limited | Config | Check product configuration |
| APL Interest Rate | Linked to predefined rates | Config | Custom rates require development |

---

## Related Files

| File | Purpose |
|---|---|
| `ps-bonus.md` | CB/SB accounts are deposit accounts; CB/SB allocation triggers ad-hoc interest calculation (not capitalization) |
| `ps-customer-service.md` | Apply Policy Loan CS item creates loan account; APL raised during Non-Forfeiture triggers ad-hoc interest calculation |
| `ps-renewal.md` | APL raised during Non-Forfeiture Option Disposal; APL repayment order interacts with loan account balance |
| `ps-product-factory.md` | Product-level config: loan allowed flags, APL allowed flags, policy account interest setup in LIMO |
| `insuremo-ootb-full.md` | OOTB capability classification (use for Gap Analysis) |
| `output-templates.md` | BSD output templates for loan/deposit-related gaps |