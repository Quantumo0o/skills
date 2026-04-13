# InsureMO V3 User Guide — Perform Survival Payment

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-ug-survival-payment.md |
| Source | 06_Perform_Survival_Payment.pdf |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | 2014-12-29 |
| Category | Finance / Survival Benefit |
| Pages | 13 |

## 1. Purpose of This File

Answers questions about survival benefit payment workflows and rules in LifeSystem 3.8.1. Used for BSD writing when survival benefit (SB) payment rules are needed.

---

## 2. Module Overview

```
Perform Survival Payment (LifeSystem 3.8.1)
│
├── 1. About Perform Survival Payment
│   └── SB definition + Workflow (Table 1)
│
├── 2. Generate Invitation Letter of Direct Credit
│   ├── Prerequisite
│   └── Steps (1-4: batch job → disbursement check → letter → change method)
│
└── 3. Perform Survival Benefit Payment
    ├── Prerequisite
    ├── Task (daily batch job)
    ├── Steps (1-6: SB option check → due date check → plan update → allocate → pay)
    └── Rules for Performing Survival Benefit Payment
```

---

## 3. Workflow — Standard Sequence

### Survival Payment Workflow (Table 1)

```
Step 1: 3 months before SB due date
         ↓
         System generates invitation letter of direct credit
         (inviting policyholder to use Direct Credit as disbursement method)
         ↓
Step 2: Disbursement method confirmed
         ↓
         System performs survival benefit payment
         (pays policyholder per SB option)
```

---

## 4. Per-Process Sections

### Process 1: Generate Invitation Letter of Direct Credit

**Prerequisite:**
- Policy status is Inforce.
- Policy is not frozen.

**Trigger:** Daily batch job starts 3 months before the survival benefit due date.

**Steps:**
1. System starts a batch job of generating invitation letter of direct credit three months before the survival benefit due date.
2. System checks the disbursement method.
   - If disbursement is Direct Credit: system generates invitation letter for client to confirm.
   - If disbursement is not Direct Credit: system generates invitation letter for client to decide whether to change.
3. Client decides whether to change the disbursement method to Direct Credit.
   - If client decides to change: go to Step 4.
   - If client decides not to change: process ends.
4. Change the disbursement method to Direct Credit.
   a. Register a new application with Policy Alteration Item as Change Survival Benefit or Cash Bonus Option.
   b. Perform application entry to change the disbursement method to Direct Credit.

---

### Process 2: Perform Survival Benefit Payment

**Prerequisite:**
- Payment start date of the survival benefit has been set by NB underwriting.
- Disbursement method of the survival benefit is confirmed.

**Trigger:** Daily batch job at a specific time.

**Steps:**
1. System starts a batch job of survival benefit allocation.
   - For SB Option 1: go to Step 2.
   - For other SB options (2-9): go to Step 3.
2. System checks the SB due date.
   - If current system date < SB due date − number of days in advance: process ends.
   - If current system date ≥ SB due date − number of days in advance: go to Step 4.
   > NOTE: Number of days in advance is a global level parameter for Option 1. Initial value = **7 days**.
3. System checks the SB due date.
   - If current system date < SB due date − number of days in advance: process ends.
   - If current system date ≥ SB due date − number of days in advance: go to Step 4.
   > NOTE: Number of days in advance is a global level parameter for Options 2-9. Initial value = **1 day**.
4. If there is no survival benefit plan: system creates a new SB plan and updates plan details. If an SB plan already exists: system updates the plan details:
   - Updates latest SB amount: Latest SB amount = new SB amount calculated by product.
   - Updates SB plan details:
     - If SB is the **last installment**: system sets SB plan status to Inactive. Process ends.
     - If SB is **not the last installment**: system updates the next SB payment date.
5. System updates the allocated SB into the SB account, and generates the SB letter.
6. Finance personnel perform payment to the client.

---

## 5. Rules for Performing Survival Benefit Payment

### Policy Extraction Criteria

| S/N | Condition |
|-----|-----------|
| 1 | Policy status is Inforce. |
| 2 | Policy is not frozen. |

### Benefit Extraction Criteria

| S/N | Condition |
|-----|-----------|
| 1 | Policy benefit status is Inforce. |
| 2 | Policy benefit's premium status is Regular, Fully Paid, or Premium waived. |
| 3 | Policy benefit is entitled to survival benefit as defined in product. |
| 4 | If an existing SB plan exists, its status must be Active and SB payment end date ≥ system date. |

### SB Plan Update Rules

| If | Then |
|----|------|
| SB is the last installment | SB plan status → Inactive. Process ends. |
| SB is not the last installment | Next SB payment date updated per product parameter (SB-AI-MA table) |

**Example (from source doc):**
> Product code '0246 – 5 year anticipated endowment'. Benefit commencement date = 01/01/2005.
> SB payment start date = 01/01/2006.
> If SB is on Option 3: on 31/12/2005, system allocates SB and updates next SB payment date to 01/01/2007.

---

## 6. INVARIANT Declarations

**INVARIANT 1:** SB can only be paid when the SB due date has arrived and the system date ≥ SB due date − number of days in advance.
- Enforced at: Daily SB Allocation batch job
- If violated: No SB payment occurs

**INVARIANT 2:** SB plan status must be Active before SB can be allocated.
- Enforced at: Step 4 — SB plan update
- If violated: SB allocation skipped for policies with inactive SB plan

**INVARIANT 3:** If an existing SB plan exists, its SB payment end date must be ≥ system date for SB to be allocated.
- Enforced at: Benefit extraction criteria
- If violated: Policy not extracted for SB allocation

**INVARIANT 4:** For the last SB installment, SB plan status is set to Inactive after allocation and no further SB payments are made.
- Enforced at: Step 4 — SB plan update
- If violated: Duplicate SB payments could occur for last installment

---

## 7. Config Gaps Commonly Encountered

| Config Item | Level | Initial Value | Notes |
|------------|-------|--------------|-------|
| Number of days in advance (Option 1) | Global | 7 days | SB batch advance window |
| Number of days in advance (Options 2-9) | Global | 1 day | SB batch advance window |
| SB payment start date | Product (NB) | Set by NB underwriting | Per product spec |
| SB-AI-MA table (policy months) | Product | Per product | Determines SB payment frequency |
| Survival benefit amount | Product | Calculated by product | Based on SA and product type |

---

## 8. Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-ug-bonus.md | Bonus allocation (Cash Bonus + Reversionary Bonus) — same workflow pattern |
| insuremo-v3-ug-renewal.md | Renewal billing — related to recurring payment batches |
| ps-fund-administration.md | Current version fund administration |
