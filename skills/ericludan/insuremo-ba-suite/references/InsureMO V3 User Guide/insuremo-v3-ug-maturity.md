# InsureMO V3 User Guide — Perform Maturity

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-ug-maturity.md |
| Source | 07_Perform_Maturity_0.pdf |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | 2015-03-27 |
| Category | Finance / Maturity |
| Pages | 23 |

## 1. Purpose of This File

Answers questions about maturity payment workflows and rules in LifeSystem 3.8.1. Used for BSD writing when maturity processing, disbursement options, and surrender value calculation are needed.

---

## 2. Module Overview

```
Perform Maturity (LifeSystem 3.8.1)
│
├── 1. About Perform Maturity
│
├── 2. Extract Policies Due for Maturity
│   ├── Prerequisites
│   └── Batch extraction criteria
│
├── 3. Generate Invitation Letter of Direct Credit
│   ├── Prerequisite
│   └── Steps
│
├── 4. Change the Disbursement Method of Maturity
│   ├── Prerequisite
│   └── Steps
│
├── 5. Perform Maturity Payment
│   ├── Prerequisites
│   ├── Task (daily batch)
│   ├── Steps (1-12)
│   └── Rules for Performing Maturity Payment
│
├── 6. Generate Monthly Maturity Due Report
│
├── 7. Generate Outstanding Maturity Report
│
└── 8. Generate Maturity Reminder Letter
```

---

## 3. Workflow — Standard Sequence

```
Maturity Date approaches (batch extracts policy)
    ↓
Invitation Letter of Direct Credit sent (3 months before maturity)
    ↓
Policyholder confirms/changes disbursement method
    ↓
Daily batch: Maturity Payment
    (validation → calculate surrender value → deduct loan+interest → disburse)
    ↓
Finance personnel performs payment
    ↓
Monthly/Outstanding Maturity Reports generated
```

---

## 4. Per-Process Sections

### Process 1: Extract Policies Due for Maturity

**Prerequisites:**
- Policy status is Inforce.
- Policy is not frozen.
- The maturity date of the policy is within the batch date range.

**Steps:**
1. System starts a batch job of extracting policies due for maturity.
2. System identifies all policies meeting the extraction criteria.
3. System generates the maturity due report.

---

### Process 2: Generate Invitation Letter of Direct Credit

**Prerequisite:**
- Policy is due for maturity.

**Trigger:** 3 months before maturity date.

**Steps:**
1. System sends invitation letter to policyholder to confirm or change disbursement method.
2. Policyholder responds.
3. If policyholder requests change: register a new application to change disbursement method.

---

### Process 3: Change the Disbursement Method of Maturity

**Prerequisite:**
- Policyholder has requested a change to the disbursement method.

**Steps:**
1. Register a new application with Policy Alteration Item = Change Maturity Disbursement Method.
2. Perform application entry.
3. System updates the disbursement method per policyholder's request.

---

### Process 4: Perform Maturity Payment

**Prerequisites:**
- Policy is due for maturity.
- Maturity date has arrived.
- Disbursement method has been confirmed.

**Trigger:** Daily batch job at a specific time.

**Steps:**
1. System starts a batch job of maturity payment.
2. System identifies all policies where: policy status = Inforce, not frozen, and maturity date = system date.
3. System checks the maturity option on the maturity date.
   - If maturity option = Option 1 (pay at maturity): go to Step 4.
   - If maturity option = Option 2 (revert to new policy): go to Step 5.
   - If maturity option = Option 3 (combine): go to Step 6.
   - If maturity option = Option 4 (reinvest): go to Step 7.
4. **Maturity Option 1 — Pay at Maturity:**
   a. System calculates the surrender value (including accumulated cash bonuses).
   b. System deducts the outstanding loan and loan interest.
   c. System deducts outstanding premiums and other fees.
   d. System generates the maturity benefit account.
   e. Finance personnel performs payment to the policyholder.
5. **Maturity Option 2 — Revert to New Policy:**
   a. System calculates the surrender value and accumulated bonuses.
   b. System uses the amount as premium for the new policy.
   c. New policy is generated under the same policy number.
6. **Maturity Option 3 — Combine:**
   a. System calculates the surrender value.
   b. A portion is paid as cash at maturity; the remainder is used to purchase a new policy.
7. **Maturity Option 4 — Reinvest:**
   a. System calculates the surrender value.
   b. The entire amount is reinvested into a new policy.
8. System calculates the maturity payment amount:
   > **Maturity Payment = Surrender Value + Accumulated Cash Bonuses − Outstanding Loan − Loan Interest − Outstanding Premiums − Other Outstanding Fees**
9. System checks the disbursement method:
   - If method = Direct Credit: system initiates direct credit to the policyholder's bank account.
   - If method = Cheque: system generates a cheque payable to the policyholder.
   - If method = Account Transfer: system transfers the amount to the policyholder's designated account.
10. System updates the maturity payment status to 'Paid'.
11. System generates the maturity payment advice.
12. System sends the maturity payment notification to the policyholder.

---

## 5. Rules for Performing Maturity Payment

### Policy Extraction Criteria

| S/N | Condition |
|-----|-----------|
| 1 | Policy status is Inforce. |
| 2 | Policy is not frozen. |
| 3 | Maturity date is within the batch date range. |

### Maturity Options

| Option | Description | System Action |
|--------|-------------|--------------|
| Option 1 | Pay at maturity | Cash payment of surrender value + bonuses |
| Option 2 | Revert to new policy | Use maturity value as premium for new policy |
| Option 3 | Combine | Partial cash + partial reinvestment |
| Option 4 | Reinvest | Full reinvestment into new policy |

### Maturity Payment Calculation

**Formula:**
```
Maturity Payment = Surrender Value
                 + Accumulated Cash Bonuses
                 − Outstanding Loan
                 − Loan Interest
                 − Outstanding Premiums
                 − Other Outstanding Fees
```

### Maturity Account Processing

| Step | Account Update |
|------|--------------|
| 1 | Calculate surrender value |
| 2 | Add accumulated cash bonuses to account |
| 3 | Deduct outstanding loan principal |
| 4 | Deduct loan interest accrued |
| 5 | Deduct any outstanding premiums |
| 6 | Deduct other outstanding fees |
| 7 | Net maturity payment = remaining balance |

### Disbursement Methods

| Method | Description |
|--------|-------------|
| Direct Credit | System initiates direct credit to policyholder's bank account |
| Cheque | System generates cheque payable to policyholder |
| Account Transfer | System transfers amount to policyholder's designated account |

### Disbursement Method Change Rules

| If | Then |
|----|------|
| Policyholder requests change before maturity | System allows change via Policy Alteration Item |
| Change requested after maturity payment processed | System does not allow change; payment is final |

---

## 6. INVARIANT Declarations

**INVARIANT 1:** Maturity payment is only processed when system date ≥ maturity date.
- Enforced at: Daily Maturity Payment batch job
- If violated: Early maturity payment could be made before policy matures

**INVARIANT 2:** Outstanding loans and interest are always deducted from the maturity payment before disbursement.
- Enforced at: Maturity payment calculation (Step 8)
- If violated: Policy loan would remain outstanding after maturity

**INVARIANT 3:** Accumulated cash bonuses are included in the maturity payment amount.
- Enforced at: Maturity payment calculation
- If violated: Policyholder would lose accumulated bonuses at maturity

**INVARIANT 4:** Maturity payment disbursement method cannot be changed after the payment has been processed.
- Enforced at: Post-payment update (Step 10-12)
- If violated: Duplicate or conflicting payments could occur

**INVARIANT 5:** For Maturity Option 2 (revert to new policy), the maturity value is used as premium for the new policy under the same policy number.
- Enforced at: Step 5 — New policy generation
- If violated: New policy premium would not be correctly funded

---

## 7. Config Gaps Commonly Encountered

| Config Item | Level | Notes |
|------------|-------|-------|
| Maturity option selection | Product / Policy | Set at NB; determines how maturity benefit is handled |
| Disbursement method | Policy | Direct Credit / Cheque / Account Transfer |
| Loan interest rate | Global / Product | Used in loan interest deduction at maturity |
| Grace period for maturity payment | Global | Number of days after maturity date to allow payment |
| Minimum maturity payment threshold | Global | Below threshold, different processing may apply |

---

## 8. Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-ug-bonus.md | Cash bonus accumulation at maturity |
| insuremo-v3-ug-survival-payment.md | Survival benefit payment (similar batch pattern) |
| ps-fund-administration.md | Current version fund administration |
| ps-investment.md | Current version investment rules |
