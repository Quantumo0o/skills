# InsureMO V3 User Guide — Manage Loan and Deposit

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-ug-loan-deposit.md |
| Source | 18_Manage_Loan_And_Deposit.pdf |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | 2014-12-29 |
| Category | Finance / Loan and Deposit |
| Pages | 36 |

## 1. Purpose of This File

Answers questions about loan and deposit management workflows in LifeSystem 3.8.1. Covers APL (Automatic Premium Loan), loan interest capitalization, deposit management, and financial adjustments. Used for BSD writing when loan/deposit rules are needed.

---

## 2. Module Overview

```
Manage Loan and Deposit (LifeSystem 3.8.1)
│
├── 1. Apply for a Policy Loan
│   ├── Field Descriptions
│   └── Apply for Policy Loan Rules
│
├── 2. Perform APL
│   └── Perform APL Rules
│
├── 3. Allocate Cash Bonus
│
├── 4. Allocate Survival Benefit
│   └── Allocate Survival Benefit Rules
│
├── 5. Capitalize Loan Interest
│   └── Capitalize Loan Interest Rules
│
├── 6. Capitalize Deposit Account Interest
│   └── Capitalize Deposit Account Interest Rules
│
├── 7. Repay Loan
│   └── Repay Loan Rules
│
├── 8. Withdraw Deposit Account
│
├── 9. Adjust Financial Data by Policy
│   └── Adjust Financial Data by Policy Rules
│
├── 10. Write Off APL
│
└── 11. Activate Account
```

---

## 3. Workflow — Standard Sequence

### Loan and Deposit Main Workflow

```
Policy Loan Application
    ↓
Loan Approved / APL Triggered
    ↓
Loan Amount Posted to Policy Account
    ↓
Loan Interest Capitalization (periodic)
    ↓
Loan Repayment OR Automatic Loan Interest Capitalization
    ↓
Deposit Account Interest Capitalization (periodic)
    ↓
Deposit Withdrawal OR Balance Adjustment
    ↓
Financial Data Adjustment (if required)
```

---

## 4. Per-Process Sections

### Process 1: Apply for a Policy Loan

**Field Descriptions:**

| Field Name | Data Type | Mandatory | Description |
|---|---|---|---|
| Loan Amount | Number | Y | Amount borrowed against policy |
| Loan Interest Rate | Percentage | Y | Annual interest rate on loan |
| Loan Repayment Date | Date | N | When loan will be repaid |
| Loan Purpose | Code | N | Purpose of loan |
| Collateral | String | N | Policy cash value as collateral |

**Apply for Policy Loan Rules:**
1. Loan amount must not exceed the maximum loanable amount = GSV (Gross Surrender Value) − loan outstanding − loan interest reserve
2. Loan interest rate is set at policy level and cannot exceed the maximum rate permitted by regulation
3. Loan is recorded in the loan account linked to the policy
4. Loan reduces the policy's cash value until repaid
5. Loan must be approved before amount is posted to policy account

---

### Process 2: Perform APL (Automatic Premium Loan)

**Purpose:** When premium is due but policyholder has not paid, system automatically raises a loan to cover the premium to keep the policy in force.

**Trigger:** Premium due date + grace period elapsed without payment.

**Perform APL Rules:**
1. APL is automatically raised when premium is overdue and policyholder has not paid
2. APL amount = outstanding premium + overdue interest + charges
3. APL is only raised if the policy's cash value (GSV) is sufficient to cover the outstanding amount
4. If GSV < outstanding amount: policy lapses (non-forfeiture triggered)
5. APL interest accrues from the date APL is raised
6. APL can be repaid at any time before policy maturity or surrender

**INVARIANT:** APL is only raised when: premium overdue AND grace period elapsed AND GSV > outstanding premium amount

---

### Process 3: Allocate Cash Bonus

**Purpose:** Allocate declared cash bonus to the cash bonus deposit account.

**Rules:**
- Cash bonus is allocated per the bonus declaration rate
- Allocated bonus goes to cash bonus deposit account
- Cash bonus deposit account earns interest

---

### Process 4: Allocate Survival Benefit

**Purpose:** Allocate survival benefit (SB) to the SB account when SB due date arrives.

**Allocate Survival Benefit Rules:**
1. SB is allocated when SB due date ≤ system date
2. SB amount = SA × SB rate per product specification
3. SB allocation updates the SB account balance
4. SB can be withdrawn, used to repay APL, or left on deposit per policyholder's option
5. If SB option = repay APL: system repays APL immediately up to SB amount

---

### Process 5: Capitalize Loan Interest

**Purpose:** Periodically capitalize loan interest to the loan principal.

**Capitalize Loan Interest Rules:**
1. Loan interest is calculated daily: Daily Interest = Loan Balance × Daily Interest Rate
2. Interest is capitalized (added to loan principal) at the capitalization frequency (monthly/quarterly/annual)
3. After capitalization: Loan Principal = Original Loan + Accumulated Interest
4. Interest capitalization continues until loan is repaid or policy lapses
5. If accumulated loan interest exceeds GSV: policy enters non-forfeiture

**Example:**
> Loan Principal = 10,000; Annual Interest Rate = 8%
> Monthly Interest = 10,000 × 8% / 12 = 66.67
> After 12 months: Capitalized Interest = 66.67 × 12 = 800
> New Loan Principal = 10,800

---

### Process 6: Capitalize Deposit Account Interest

**Purpose:** Periodically capitalize interest earned on deposit accounts (cash bonus deposit, SB deposit, etc.).

**Capitalize Deposit Account Interest Rules:**
1. Deposit account interest is calculated daily: Daily Interest = Deposit Balance × Daily Interest Rate
2. Interest is capitalized at the deposit interest capitalization frequency (monthly/quarterly/annual)
3. Deposit account balance = Principal + Accumulated Interest
4. Deposit account interest rate may differ from loan interest rate

**Example:**
> Deposit Balance = 5,000; Annual Interest Rate = 4%
> Monthly Interest = 5,000 × 4% / 12 = 16.67
> After 12 months: Capitalized Interest = 16.67 × 12 = 200
> New Deposit Balance = 5,200

---

### Process 7: Repay Loan

**Purpose:** Policyholder repays outstanding loan (principal + interest).

**Repay Loan Rules:**
1. Loan repayment amount = Outstanding Loan Principal + Accumulated Loan Interest
2. Repayment can be: full repayment OR partial repayment
3. If full repayment: loan account balance = 0; policy cash value fully restored
4. If partial repayment: loan account balance reduced by repayment amount; interest recalculated
5. Repayment must be applied first to accumulated interest, then to principal
6. After repayment, policy continues with reduced loan balance

**INVARIANT:** Loan repayment is applied first to interest, then to principal.

---

### Process 8: Withdraw Deposit Account

**Purpose:** Policyholder withdraws balance from deposit account.

**Rules:**
1. Withdrawal amount ≤ deposit account balance
2. Withdrawal reduces deposit account balance
3. Withdrawal may be subject to withdrawal charges per product rules
4. If withdrawal depletes deposit account: account balance = 0

---

### Process 9: Adjust Financial Data by Policy

**Purpose:** Manual adjustment to policy financial records for corrections.

**Adjust Financial Data by Policy Rules:**
1. Adjustment can be made to: loan amount, deposit balance, interest records
2. Adjustment requires authorization
3. All adjustments are recorded in audit log
4. Adjustment reason must be entered
5. System recalculates interest from adjustment date

**INVARIANT:** All financial data adjustments must be authorized and logged.

---

### Process 10: Write Off APL

**Purpose:** Write off uncollectible APL (e.g., when policy lapses and APL cannot be recovered).

**Rules:**
1. APL write-off occurs when policy lapses and APL is outstanding
2. Write-off amount = Outstanding APL Principal + Accumulated Interest
3. Write-off is a loss to the insurer
4. Write-off does not forgive the debt; APL remains recoverable
5. Write-off requires authorization

---

### Process 11: Activate Account

**Purpose:** Reactivate a loan or deposit account after suspension.

**Rules:**
1. Account can be reactivated if conditions that caused suspension are resolved
2. Reactivation restores the account to active status
3. Interest accrual resumes from reactivation date

---

## 5. INVARIANT Declarations

**INVARIANT 1:** Loan amount must never exceed maximum loanable amount = GSV − loan outstanding − loan interest reserve.
- Enforced at: Apply for Policy Loan
- If violated: Over-loan could exceed policy cash value; policy would become insolvent

**INVARIANT 2:** APL is only raised when: premium overdue AND grace period elapsed AND GSV > outstanding premium amount.
- Enforced at: Perform APL
- If violated: APL raised incorrectly; policy accounting would be wrong

**INVARIANT 3:** Loan repayment is applied first to accumulated interest, then to principal.
- Enforced at: Repay Loan
- If violated: Incorrect interest-principal allocation

**INVARIANT 4:** All financial data adjustments must be authorized and logged.
- Enforced at: Adjust Financial Data by Policy
- If violated: Unauthorized adjustment could falsify financial records

**INVARIANT 5:** Loan interest is calculated daily and capitalized at the declared frequency.
- Enforced at: Capitalize Loan Interest
- If violated: Incorrect interest capitalization; loan balance would be wrong

**INVARIANT 6:** Deposit account interest is capitalized separately from loan interest; deposit rate ≠ loan rate.
- Enforced at: Capitalize Deposit Account Interest
- If violated: Wrong interest rate applied to deposit account

---

## 6. Config Gaps Commonly Encountered

| Config Item | Level | Notes |
|------------|-------|-------|
| Maximum loan interest rate | Global / Regulatory | Per market regulation |
| Loan interest capitalization frequency | Product | Monthly / Quarterly / Annual |
| Deposit interest capitalization frequency | Product | Monthly / Quarterly / Annual |
| APL grace period | Product | Days after due date before APL triggered |
| Minimum loan amount | Product | Below this amount, loan not permitted |
| Maximum loanable percentage of GSV | Product | Usually 80-90% of GSV |

---

## 7. Key Formulas

**Maximum Loan Amount:**
```
Maximum Loan = GSV − Outstanding Loan − Interest Reserve
```

**Daily Interest:**
```
Daily Interest = Loan Balance × (Annual Interest Rate / 365)
```

**Loan Repayment (interest-first):**
```
Repayment Applied to Interest = MIN(Repayment Amount, Accumulated Interest)
Repayment Applied to Principal = Repayment Amount − Interest Repaid
```

**APL Trigger Condition:**
```
IF (GSV > Outstanding Premium) THEN APL = Outstanding Premium
ELSE Policy Lapses
```

---

## 8. Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-ug-renewal.md | Renewal premium → APL trigger |
| insuremo-v3-ug-bonus.md | Cash bonus → deposit account |
| insuremo-v3-ug-survival-payment.md | Survival benefit → SB account |
| ps-fund-administration.md | Current version fund administration |
