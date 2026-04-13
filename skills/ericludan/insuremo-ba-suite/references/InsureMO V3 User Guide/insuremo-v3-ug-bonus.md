# InsureMO V3 User Guide — Declare and Allocate Bonus

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-ug-bonus.md |
| Source | 05_Declare_And_Allocate_Bonus.pdf |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | 2014-12-29 |
| Category | Finance / Bonus Administration |
| Pages | 17 |

## 1. Purpose of This File

Answers questions about bonus declaration, allocation, and disbursement workflows in LifeSystem 3.8.1. Used for BSD writing when bonus-related rules are needed.

---

## 2. Module Overview

```
Declare and Allocate Bonus (LifeSystem 3.8.1)
│
├── 1. About Declare and Allocate Bonus
│   ├── Cash Bonus vs Reversionary Bonus
│   └── Bonus Declaration and Allocation Workflow (Table 1)
│
├── 2. Generate Invitation Letter of Direct Credit
│   ├── Prerequisite
│   ├── Task (3-month advance batch job)
│   └── Steps (1-4: disbursement method check → generate letter → client decision → change method)
│
├── 3. Allocate Cash Bonus
│   ├── Prerequisite
│   ├── Task (daily batch job)
│   ├── Cash Bonus Options (Option 1-5)
│   └── Rules for Allocating Cash Bonus
│
└── 4. Allocate Reversionary Bonus
    ├── Prerequisite
    ├── Task (daily batch job)
    └── Steps (1-3: eligibility check → due date check → allocate)
```

---

## 3. Workflow — Standard Sequence

### Bonus Declaration and Allocation Workflow (Table 1)

```
Step 1: 3 months before bonus due date
         ↓
         System generates invitation letter of direct credit
         (inviting policyholder to use Direct Credit as disbursement method)
         ↓
Step 2: Disbursement method confirmed + cash bonus rate declared
         ↓
         System allocates cash bonus
         (policyholder can withdraw cash bonus when declared)
         ↓
Step 3: Reversionary bonus rate declared
         ↓
         System allocates reversionary bonus
         (reversionary bonus can only be encashed on policy maturity)
```

### Cash Bonus Types

| Type | Description | When Withdrawn |
|------|-------------|--------------|
| Cash Bonus (CB) | Paid as cash to policyholder | Can be withdrawn when declared |
| Reversionary Bonus | Reverted back to policy to enhance coverage | Can only be encashed on maturity |

---

## 4. Per-Process Sections

### Process 1: Generate Invitation Letter of Direct Credit

**Prerequisite:**
- The product has cash bonus to be allocated.
- The policy status is Inforce.
- The policy is not frozen.

**Trigger:** Batch job starts 3 months before the bonus due date.

**Steps:**
1. System starts a batch job of generating the invitation letter of direct credit three months before the bonus due date.
2. System checks the disbursement method.
   - If disbursement method is Direct Credit: system generates invitation letter for client to confirm.
   - If disbursement method is not Direct Credit: system generates invitation letter for client to decide whether to change.
3. Client decides whether to change the disbursement method to Direct Credit.
   - If client decides to change: go to Step 4.
   - If client decides not to change: process ends.
4. Change the disbursement method to Direct Credit.
   a. Register a new application with Policy Alteration Item as Change Survival Benefit or Cash Bonus Option.
   b. Perform application entry to change the disbursement method to Direct Credit.

---

### Process 2: Allocate Cash Bonus

**Prerequisite:**
- The product has cash bonus to be allocated.
- The cash bonus rate is declared.
- The disbursement method is confirmed.

**Trigger:** Daily batch job at a specific time.

**Steps:**
1. System starts a batch job of cash bonus allocation.
   - For cash bonus Option 1: go to Step 2.
   - For other cash bonus options: go to Step 3.
2. System checks the bonus due date.
   - If current system date < bonus due date − number of days in advance: process ends.
   - If current system date ≥ bonus due date − number of days in advance: go to Step 4.
   > NOTE: The number of days in advance is a global level parameter for Option 1. Initial value = **7 days**.
3. System checks the bonus due date.
   - If current system date < bonus due date − number of days in advance: process ends.
   - If current system date ≥ bonus due date − number of days in advance: go to Step 4.
   > NOTE: The number of days in advance is a global level parameter for other options. Initial value = **1 day**.
4. System updates related information at policy benefit level:
   - Updates latest bonus amount: Latest bonus amount = new bonus amount calculated by corresponding bonus rate.
   - Checks parameter No. of Completed policy years for CB becoming payable:
     - If duration is within No. of Completed policy years for CB becoming payable: cash bonus will not be put into account.
     - If duration is beyond No. of Completed policy years: system puts all cash bonus amounts into the cash bonus account (where cash bonus allocated status indicator = N). Then updates related cash bonus allocated status indicator from N to Y.
   - Updates next bonus due date at policy benefit level: Next bonus due date = original next bonus due date + 1 year.
5. System allocates cash bonus and generates the cash bonus annual statement.
6. Finance personnel perform payment to the client.

**Cash Bonus Options:**

| Option | Description | System Action |
|--------|-------------|--------------|
| Option 1 | To receive cash bonus in cash | System starts batch payment to pay out the cash bonus deposit account value. Withdraw date = cash bonus allocation due date. |
| Option 2 | To use bonus to pay premium | System withdraws cash bonus deposit account and repays APL immediately. APL repayment date = cash bonus allocation due date. APL repayment amount = lower of (cash bonus allocated amount, APL account value). |
| Option 3 | To leave cash bonus on deposit with Company | Cash bonus remains on deposit. |
| Option 4 | Option (3) for XX years, then Option (2) | Cash bonus on deposit for specified years, then used to repay APL. |
| Option 5 | To receive cash bonus in annuity form starting at later years | Annuity payment starts at specified later year. |

**Account Update Logic (Option 2 — Use Bonus to Pay Premium):**

| Account | Field | Value |
|---------|-------|-------|
| APL account | Repayment date | Cash bonus allocation due date |
| APL account | Repayment amount | lower of (cash bonus allocated amount, APL account value) |
| Cash bonus deposit account | Withdraw date | Cash bonus allocation due date |
| Cash bonus deposit account | Withdraw amount | lower of (cash bonus allocated amount, APL account value) |

---

### Process 3: Allocate Reversionary Bonus

**Prerequisite:**
- The product has reversionary bonus.
- The reversionary bonus rate is declared.

**Trigger:** Daily batch job at a specific time.

**Steps:**
1. System starts a batch job of reversionary bonus allocation.

   **Policy eligibility criteria:**
   - Policy status is not Terminate.
   - Policy is not Frozen.

   **Benefit eligibility criteria:**
   - Policy benefit status is not Terminate.
   - Policy benefit is the reversionary bonus product.
   - Premium status of the policy benefit is Regular, Fully paid, or Premium waived.

2. System checks the bonus due date.
   - If current system date < bonus due date: process ends.
   - If current system date ≥ bonus due date: go to Step 3.
3. System allocates reversionary bonus and generates reversionary bonus statement.
   a. Updates latest bonus: Latest bonus = new bonus calculated by corresponding bonus rates + special bonus calculated by corresponding special bonus rates.
   b. Updates accumulative bonus: Accumulative bonus = original accumulative bonus + latest bonus.
   c. Updates next bonus due date at policy benefit level: Next bonus due date = original next bonus due date + 1 year.

---

## 5. Rules for Allocating Cash Bonus

### Policy Extraction Criteria

| S/N | Condition |
|-----|-----------|
| 1 | Policy status is Inforce. |
| 2 | Policy is not frozen. |

### Benefit Extraction Criteria

| S/N | Condition |
|-----|-----------|
| 1 | Policy benefit status is Inforce. |
| 2 | Policy benefit is the cash bonus product. |
| 3 | Premium status of the policy benefit is Regular, Fully Paid, or Premium waived. |
| 4 | The next premium due date of the policy benefit is ≥ the next bonus due date (for premium status Regular or Premium waived). |

### Cash Bonus Allocation Logic

1. When system runs batch job to extract policies:
   - Policies eligible for bonus allocation must meet: policy status = Inforce, policy not frozen.
   - Benefits eligible must meet: benefit status = Inforce, is cash bonus product, premium status = Regular/Fully Paid/Premium waived, next premium due date ≥ next bonus due date.

2. In cash bonus allocation, system puts allocated cash bonus to cash bonus deposit account first, then allocates according to different options (Option 1-5 above).

---

## 6. INVARIANT Declarations

**INVARIANT 1:** Cash bonus can only be withdrawn when declared.
- Enforced at: Cash Bonus Allocation batch job
- If violated: Cash bonus remains in cash bonus deposit account until declaration

**INVARIANT 2:** Reversionary bonus can only be encashed on policy maturity.
- Enforced at: Reversionary Bonus Allocation batch job
- If violated: Reversionary bonus remains in policy until maturity

**INVARIANT 3:** Cash bonus allocation batch job runs only when all prerequisite conditions are met (product has cash bonus, rate declared, disbursement method confirmed).
- Enforced at: Daily Cash Bonus Allocation batch job
- If violated: No allocation occurs; batch job skips the policy

**INVARIANT 4:** Next bonus due date is updated to original + 1 year after each bonus allocation.
- Enforced at: Post bonus allocation update
- If violated: Next bonus due date would not advance correctly, causing duplicate or missed allocations

**INVARIANT 5:** Cash bonus is not put into account if duration is within No. of Completed policy years for CB becoming payable.
- Enforced at: Step 4 of Cash Bonus Allocation
- If violated: Cash bonus would be allocated before the completed policy years requirement is met

---

## 7. Config Gaps Commonly Encountered

| Config Item | Level | Initial Value | Location in System |
|------------|-------|--------------|-------------------|
| Number of days in advance (Option 1) | Global | 7 days | Global level parameter |
| Number of days in advance (other options) | Global | 1 day | Global level parameter |
| No. of Completed policy years for CB becoming payable | Global | Per product spec | Parameter per product |
| Cash bonus rate declaration | Product | Per actuarial declaration | Product factory |
| Reversionary bonus rate declaration | Product | Per actuarial declaration | Product factory |

---

## 8. Related Files

| File | Purpose |
|------|---------|
| insuremo-v3-ug-renewal.md | Renewal batch and billing rules |
| ps-fund-administration.md | Current version fund administration rules |
| ps-investment.md | Current version investment rules |
