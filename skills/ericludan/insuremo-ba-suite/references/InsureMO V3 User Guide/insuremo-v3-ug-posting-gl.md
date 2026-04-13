# InsureMO V3 User Guide — Posting to GL

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-ug-posting-gl.md |
| Source | 19_Posting_to_GL_0409.pdf |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | 2015-04-09 |
| Category | Finance / Accounting |
| Pages | 28 |

## 1. Purpose of This File

Answers questions about GL (General Ledger) posting workflows in LifeSystem 3.8.1. Covers bank account setup, accounting rules, EOD/EOM posting, reconciliation, and FX rate management. Used for BSD writing when financial accounting rules and GL integration are needed.

---

## 2. Module Overview

```
Posting to GL (LifeSystem 3.8.1)
│
├── 1. Setup Bank Account
│   ├── Add Bank Account
│   ├── Set up Bank Master
│   ├── Assign Role
│   ├── Maintain Bank Account
│   │   ├── Create Bank Account
│   │   ├── Modify Bank Account
│   │   └── Disable a Bank Account
│
├── 2. Set Accounting Rule
│
├── 3. Perform EOD Posting
│
├── 4. Perform EOM Posting
│
├── 5. Perform Reconciliation
│
├── 6. Perform Accounting Month Increment
│
├── 7. Accounting Date
│
└── 8. Set Transaction Foreign Exchange Rate
```

---

## 3. Key Concepts

### GL Posting Architecture

```
LifeSystem Transaction
    → Accounting Rule (maps to GL account)
    → EOD/EOM Posting Batch
    → General Ledger (GL)
```

### GL Account Types

| Account Type | Description | Examples |
|-------------|-------------|----------|
| Asset | Resources owned | Bank Account, Receivable |
| Liability | Amounts owed | Payable, Premium Deposit |
| Revenue | Income | Premium Income, Interest Income |
| Expense | Costs incurred | Commission Expense, Claim Paid |

### Double-Entry Accounting

Every transaction has:
- **Debit**: Entry on left side (increases assets, decreases liabilities)
- **Credit**: Entry on right side (decreases assets, increases liabilities)

**Rule:** Total Debits = Total Credits for every transaction.

---

## 4. Per-Process Sections

### Process 1: Setup Bank Account

**Add Bank Account:**
- Link a bank account to LS for a specific currency and account type
- Required before any payment or receipt can be processed

**Bank Master Setup:**
- Define bank code, bank name, branch, SWIFT code
- Each bank master can have multiple bank accounts

**Assign Role:**
- Assign GL account roles to bank accounts for posting
- Roles: Collection Account, Payment Account, Suspense Account

**Maintain Bank Account:**

| Action | Description |
|--------|-------------|
| Create | Add new bank account for a currency and account type |
| Modify | Update bank account details |
| Disable | Mark bank account as inactive (no new transactions) |

**Key Rules:**
1. Bank account must be linked to a bank master
2. Each bank account has a specific currency
3. Disabled bank accounts cannot receive new transactions but existing transactions remain
4. Bank account roles determine which GL accounts are used for posting

---

### Process 2: Set Accounting Rule

**Purpose:** Map LifeSystem transactions to GL accounts.

**Accounting Rule Structure:**
```
Transaction Type → Dr Account → Cr Account → Amount Rule
```

**Example Accounting Rules:**

| Transaction Type | Dr Account | Cr Account |
|-----------------|------------|------------|
| Premium Received | Bank Account | Premium Deposit |
| Commission Paid | Commission Expense | Bank Account |
| Claim Paid | Claim Payable | Bank Account |
| Expense Incurred | Expense Account | Suspense |

**Field Descriptions (Appendix A):**

| Field | Mandatory | Description |
|---|---|---|
| Transaction Type | Y | LS transaction type |
| Debit Account | Y | GL account for debit entry |
| Credit Account | Y | GL account for credit entry |
| Amount Type | Y | Fixed / Percentage / Formula |
| Amount Value | Y | Fixed value or percentage rate |
| Currency | Y | Transaction currency |
| Effective Date | Y | Rule effective from this date |
| Expiry Date | N | Rule expires on this date |

**Accounting Rule for Cash:**

| Field | Description |
|---|---|
| Rule Name | Name of accounting rule |
| Rule Code | Unique rule identifier |
| Transaction Type | Type of transaction |
| Debit GL Account | GL account for debit |
| Credit GL Account | GL account for credit |
| Amount Type | How amount is calculated |
| Currency | Transaction currency |

---

### Process 3: Perform EOD Posting

**Purpose:** Post daily transactions to GL.

**Trigger:** End of Day batch job.

**Steps:**
1. System extracts all approved transactions from the day.
2. For each transaction:
   - System applies accounting rule to determine GL accounts
   - System calculates debit and credit amounts
   - System validates: Total Debits = Total Credits
3. System posts validated entries to GL.
4. System generates EOD posting report.

**EOD Posting Rules:**
1. Only approved transactions are posted
2. Every transaction must have a matching accounting rule
3. All postings must balance (Debits = Credits)
4. Posted transactions cannot be modified

**INVARIANT:** EOD Posting only processes transactions where Total Debits = Total Credits.

---

### Process 4: Perform EOM Posting

**Purpose:** Month-end posting to GL.

**Trigger:** End of Month batch job.

**Steps:**
1. System runs EOD posting for the last day of month.
2. System calculates accrued items:
   - Accrued premium earned
   - Accrued commission
   - Accrued interest
3. System posts accrual entries to GL.
4. System generates EOM posting report.

**EOM Posting Rules:**
1. EOM posting includes all EOD postings for the month
2. Accrual entries are calculated per accounting period
3. EOM posting closes the accounting month
4. After EOM posting: month is locked for adjustments

---

### Process 5: Perform Reconciliation

**Purpose:** Match LS bank account transactions with bank statement.

**Steps:**
1. System extracts LS bank transactions for the period.
2. System generates reconciliation report in Excel format.
3. User downloads Excel template.
4. User uploads bank statement data.
5. System matches LS transactions with bank statement:
   - Matched: marked as reconciled
   - Unmatched: flagged for investigation
6. User resolves unmatched items manually.
7. Reconciliation is confirmed.

**Reconciliation Rules:**
1. Reconciliation is performed per bank account per currency
2. Match criteria: amount, date, reference number
3. Unmatched items remain in suspense until resolved
4. Reconciliation status: Unreconciled → Partially Reconciled → Fully Reconciled

---

### Process 6: Perform Accounting Month Increment

**Purpose:** Close current accounting month and open next.

**Steps:**
1. Validate all EOM postings are complete.
2. Close current accounting month.
3. Open next accounting month.
4. System date advances to new month.

**Rules:**
1. Month can only be incremented after EOM posting is complete
2. Previous month must be fully reconciled before increment
3. Opening balance of new month = Closing balance of previous month

---

### Process 7: Accounting Date

**Purpose:** Control which accounting period transactions belong to.

**Key Rules:**
1. Accounting date determines the posting period
2. Accounting date can be: current date, back date, future date (within limits)
3. Back dating is restricted by authorization
4. Accounting date must be within the open accounting period

---

### Process 8: Set Transaction Foreign Exchange Rate

**Purpose:** Define FX rates for multi-currency transactions.

**Key Rules:**
1. FX rate is set per currency pair per date
2. FX rates are entered and approved before use
3. All exchange rates are rounded to 6 decimal places

**Set FX Rate Rules (Appendix A Table 4):**
1. FX rate must be entered for each currency pair
2. Rate is effective from the entered date
3. Rate is used for: converting premium, claims, commission in foreign currency
4. Rate can be updated for future dates; past rates are locked

**FX Rate Entry Fields:**

| Field | Mandatory | Description |
|---|---|---|
| From Currency | Y | Source currency |
| To Currency | Y | Target currency |
| Exchange Rate | Y | Rate (6 decimal places) |
| Effective Date | Y | Date from which rate applies |
| Status | Y | Active / Inactive |

---

## 5. INVARIANT Declarations

**INVARIANT 1:** Every GL posting must balance: Total Debits = Total Credits.
- Enforced at: EOD Posting / EOM Posting
- If violated: Unbalanced entry; GL integrity compromised

**INVARIANT 2:** EOD Posting only processes approved transactions.
- Enforced at: EOD Posting batch
- If violated: Unapproved transactions posted; accounting error

**INVARIANT 3:** Accounting date must be within the open accounting period.
- Enforced at: Transaction entry / posting
- If violated: Transaction posted to wrong period

**INVARIANT 4:** FX rates are rounded to 6 decimal places before use.
- Enforced at: Set Transaction Foreign Exchange Rate
- If violated: Rounding error accumulates in multi-currency transactions

**INVARIANT 5:** EOM posting must be complete before accounting month can be incremented.
- Enforced at: Accounting Month Increment
- If violated: Month closed without accruals; financial statements incorrect

---

## 6. Batch Process Rules (Appendix B)

### Batch Process - Collections

**Purpose:** Post collection transactions to GL.

**Rules:**
1. System extracts all approved collection transactions.
2. System applies accounting rule for collection type.
3. System posts: Dr Bank Account / Cr Premium Deposit.
4. Unreconciled items remain in suspense.

### Batch Process - Payments

**Purpose:** Post payment transactions to GL.

**Rules:**
1. System extracts all approved payment transactions.
2. System applies accounting rule for payment type.
3. System posts: Dr Expense/Commission/Claim / Cr Bank Account.
4. Payment must have matching authorization before posting.

---

## 7. Key Formulas

**FX Conversion:**
```
Amount in Target Currency = Amount in Source Currency × FX Rate
```

**EOM Accrual:**
```
Accrued Amount = Total Premium Earned − Total Premium Received
```

**Reconciliation Match:**
```
Matched Amount = SUM(Amount where LS = Bank)
Unmatched Amount = SUM(Amount where LS ≠ Bank)
Reconciliation % = Matched Amount / Total Amount × 100
```

---

## 8. Menu Navigation Table

| Action | Path |
|---|---|
| Setup Bank Account | Finance > GL > Bank Account > Setup |
| Add Bank Account | Finance > GL > Bank Account > Add |
| Maintain Bank Account | Finance > GL > Bank Account > Maintain |
| Set Accounting Rule | Finance > GL > Accounting Rule > Set |
| Perform EOD Posting | Finance > GL > Posting > EOD |
| Perform EOM Posting | Finance > GL > Posting > EOM |
| Perform Reconciliation | Finance > GL > Reconciliation |
| Accounting Month Increment | Finance > GL > Period > Month Increment |
| Set FX Rate | Finance > GL > FX Rate > Set |

---

## 9. Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-ug-collection.md | Collections → GL posting |
| insuremo-v3-ug-payment.md | Payments → GL posting |
| insuremo-v3-ug-claims.md | Claims → GL posting |
| insuremo-v3-ug-bonus.md | Bonus → GL posting |
| ps-finance.md | Current version finance |
