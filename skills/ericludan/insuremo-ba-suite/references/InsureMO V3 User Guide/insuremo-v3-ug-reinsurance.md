# InsureMO V3 User Guide — Reinsurance

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-ug-reinsurance.md |
| Source | 20_Reinsurance_0.pdf |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | 2015-03-16 |
| Category | Finance / Reinsurance |
| Pages | 34 |

## 1. Purpose of This File

Answers questions about reinsurance (RI) configuration and processing in LifeSystem 3.8.1. Covers treaty setup, RI cession batches, facultative reinsurance, claim recovery, and experience refund. Used for BSD writing when RI cession rules are needed.

---

## 2. Module Overview

```
Reinsurance (LifeSystem 3.8.1)
│
├── 1. About Configuration
│   ├── Set up a Treaty
│   ├── About Other Reinsurance Information
│   ├── Define Retain Order
│   ├── Define Risk Category
│   ├── Define Risk Factor
│   ├── Define Premium Rate
│   └── Define Commission Rate
│
├── 2. Main Process
│   ├── RI New Cession Batch Job
│   ├── About RI Movement
│   ├── Customer Service Movement Batch Job
│   ├── Claim Recovery Batch Job
│   └── RI Renewal Cession Batch Job
│
├── 3. Additional Functions
│   ├── Arrange Facultative Reinsurance
│   ├── Cession Adjustment
│   ├── Experience Refund Batch Job
│   └── Undo Cessions
│
└── 4. RI Query
    ├── RI Query by Policy
    ├── RI Query by Contract
    └── RI Query by Treaty
```

---

## 3. Key Concepts

### Reinsurance Terms

| Term | Definition |
|------|-----------|
| RI | Reinsurance |
| Cession | The portion of risk passed to the reinsurer |
| Retain | The portion of risk retained by the insurer |
| Treaty | Formal agreement between insurer and reinsurer |
| Facultative | Per-policy reinsurance arrangement |
| Automatic | Policy-level automatic cession under treaty |
| RI Movement | Change in RI cession (increase/decrease/cancel) |

### Treaty Structure

```
Treaty
  └── Risk Category
        └── Risk Factor
              └── Premium Rate
                    └── Commission Rate
```

---

## 4. Per-Process Sections

### Process 1: Set up a Treaty

**Field Descriptions (Appendix):**

| Field | Mandatory | Description |
|---|---|---|
| Treaty Code | Y | Unique treaty identifier |
| Treaty Name | Y | Treaty description |
| Reinsurer | Y | RI company name |
| Treaty Type | Y | Automatic / Facultative / Mixed |
| Effective Date | Y | Treaty start date |
| Expiry Date | N | Treaty end date |
| Retain Order | Y | Sequence of retention layers |
| Risk Category | Y | Type of risk covered |
| Premium Rate | Y | RI premium rate per unit |
| Commission Rate | Y | RI commission rate |
| RI Share % | Y | Percentage of risk ceded to RI |

**Treaty Setup Rules:**
1. Treaty must be set up before any RI cession can occur
2. Each treaty has a unique code and effective dates
3. RI share % determines how much risk is ceded vs retained
4. Retain order defines the sequence of retention layers (ceding company retains first, then RI layers above)

### About Other Reinsurance Information

**Define Retain Order:**
- Retain Order = sequence of risk retention layers
- Ceding company retains first loss up to retain limit
- RI layer above retain limit is covered by treaty

**Define Risk Category:**
- Categories: Medical, Non-Medical, Group, etc.
- Each risk category has different RI terms

**Define Risk Factor:**
- Risk factors adjust the RI premium rate
- Factors: age, gender, occupation, health status

**Define Premium Rate:**
- RI premium rate per unit of sum assured
- Varies by risk category and treaty

**Define Commission Rate:**
- Commission paid by RI company to ceding company
- Commission rate % of RI premium

---

### Process 2: RI New Cession Batch Job

**Purpose:** Automatically cede new policies under automatic treaties.

**Trigger:** Daily batch job.

**Steps:**
1. System runs RI New Cession batch job daily.
2. System identifies policies where: policy status = Inforce, RI cession not yet created, SA exceeds retain limit.
3. System calculates RI cession amount: RI Share % × (SA − Retain Limit).
4. System creates RI cession record linked to the treaty.
5. RI premium is calculated: RI Cession Amount × RI Premium Rate.
6. RI commission is calculated: RI Premium × Commission Rate.

**RI Movement (About):**
- RI movement tracks changes to existing cessions
- Types: Increase cession, Decrease cession, Cancel cession, Renewal

---

### Process 3: Customer Service Movement Batch Job

**Purpose:** Process RI movements initiated by customer service actions.

**Trigger:** Customer service action (e.g., SA increase, top-up).

**Steps:**
1. System identifies policies with CS actions that affect RI cession.
2. For each CS action:
   - If SA increases: system calculates additional cession = RI Share % × Additional SA
   - If SA decreases: system calculates cession reduction = RI Share % × Reduction
   - If policy lapses/surrenders: system initiates cession cancellation
3. System creates RI movement record for each change.
4. RI premium adjustment calculated.
5. Audit trail updated.

**Rules:**
1. CS movements trigger RI movements when: SA change exceeds threshold, benefit change, policy change
2. Additional cession = RI Share % × Additional SA above retain limit
3. Movement is recorded per policy and per treaty

---

### Process 4: Claim Recovery Batch Job

**Purpose:** Recover claim amounts from reinsurer.

**Trigger:** Daily batch job after claim payment.

**Steps:**
1. System identifies paid claims where: claim amount exceeds retain limit, RI cession exists.
2. System calculates RI recovery: RI Share % × (Claim Amount − Retain).
3. System creates claim recovery record.
4. Finance processes recovery from reinsurer.
5. Recovery amount posted to claim payment account.

**Claim Recovery Formula:**
```
RI Recovery = RI Share % × MAX(0, Claim Amount − Retain Amount)
```

**Rules:**
1. RI recovery is only available for claims where RI cession was in force at time of claim
2. For death claims: RI recovery = RI Share % × Death Benefit Amount
3. For health claims: RI recovery = RI Share % × Claim Amount (within RI limits)
4. Claim recovery is processed after claim is approved and paid

---

### Process 5: RI Renewal Cession Batch Job

**Purpose:** Renew RI cession at policy renewal date.

**Trigger:** Policy anniversary date.

**Steps:**
1. System identifies policies where: policy anniversary = system date, RI cession exists.
2. System checks treaty expiry date.
   - If treaty expired: system flags for RI renewal review
   - If treaty still valid: system renews cession automatically
3. RI premium for new period is calculated.
4. RI commission for new period is calculated.
5. Audit trail updated.

---

### Process 6: Arrange Facultative Reinsurance

**Purpose:** Arrange per-policy facultative RI for risks not covered by automatic treaty.

**Steps:**
1. Underwriter requests facultative RI for a specific policy.
2. System creates facultative RI record.
3. Facultative RI quote is obtained from reinsurer.
4. Facultative RI is accepted or declined.
5. If accepted: cession is set up manually under facultative treaty.

**Rules:**
1. Facultative RI is arranged per policy, not automatically
2. Facultative RI is used when: risk exceeds treaty automatic limits, non-standard risk
3. Facultative RI terms (premium rate, RI share) are negotiated individually

---

### Process 7: Cession Adjustment

**Purpose:** Manually adjust RI cession amounts.

**Reasons:**
- Incorrect cession amount at inception
- Treaty terms changed mid-term
- Administrative correction

**Steps:**
1. User requests cession adjustment with reason.
2. System calculates adjustment amount = New Cession − Original Cession.
3. If adjustment > 0: additional cession created.
4. If adjustment < 0: cession reduction processed.
5. RI premium adjustment calculated.
6. Audit trail updated.

---

### Process 8: Experience Refund Batch Job

**Purpose:** Calculate and process experience refund from RI company.

**Trigger:** Annual or at treaty expiry.

**Steps:**
1. System calculates experience: actual claims vs expected claims under treaty.
2. If actual claims < expected: profit sharing applies; RI company pays experience refund.
3. If actual claims > expected: no refund; ceding company bears excess.
4. Experience refund amount is calculated per treaty.
5. Finance processes refund from/to RI company.

**Experience Refund Formula:**
```
Experience Refund = MAX(0, (Expected Claims − Actual Claims)) × RI Share %
```

---

### Process 9: Undo Cessions

**Purpose:** Cancel/reverse RI cession in error.

**Reasons:**
- Incorrect cession created
- Duplicate cession
- Policy rejected post-cession

**Steps:**
1. User identifies erroneous cession with reason.
2. System validates: cession is still within allowed undo period.
3. System reverses the cession record.
4. RI premium reversal is calculated.
5. RI commission reversal is calculated.
6. Audit trail updated.

**Rules:**
1. Undo is only allowed before treaty reporting is finalized
2. Undo after reporting period: cession adjustment used instead

---

## 5. INVARIANT Declarations

**INVARIANT 1:** RI cession is only created when policy status = Inforce and SA exceeds the retain limit.
- Enforced at: RI New Cession Batch Job
- If violated: Cession created for ineligible policies

**INVARIANT 2:** RI recovery = RI Share % × MAX(0, Claim Amount − Retain Amount).
- Enforced at: Claim Recovery Batch Job
- If violated: Incorrect recovery amount claimed from RI

**INVARIANT 3:** RI movement is triggered for every CS action that changes the cession amount.
- Enforced at: Customer Service Movement Batch Job
- If violated: Cession does not reflect current policy status

**INVARIANT 4:** RI cession amount = RI Share % × (SA − Retain Limit).
- Enforced at: RI New Cession Batch Job
- If violated: Incorrect cession amount ceded

**INVARIANT 5:** Undo Cessions is only processed before treaty reporting is finalized.
- Enforced at: Undo Cessions
- If violated: Accounting records already reconciled with RI company

---

## 6. Config Gaps Commonly Encountered

| Config Item | Level | Notes |
|------------|-------|-------|
| RI Share % | Treaty | % of risk ceded to RI |
| Retain Limit | Product / Treaty | SA above which RI applies |
| RI Premium Rate | Risk Category / Treaty | Per 1000 SA |
| Commission Rate | Treaty | % of RI premium |
| Experience Refund Threshold | Treaty | Claims level triggering refund |
| Facultative RI Terms | Per policy | Individually negotiated |

---

## 7. Key Formulas

**RI Cession Amount:**
```
RI Cession = RI Share % × MAX(0, SA − Retain Limit)
```

**RI Premium:**
```
RI Premium = RI Cession Amount × RI Premium Rate
```

**RI Commission:**
```
RI Commission = RI Premium × Commission Rate
```

**Claim Recovery:**
```
RI Recovery = RI Share % × MAX(0, Claim Amount − Retain Amount)
```

**Experience Refund:**
```
Experience Refund = MAX(0, Expected Claims − Actual Claims) × RI Share %
```

---

## 8. Menu Navigation Table

| Action | Path |
|---|---|
| Set up a Treaty | Reinsurance > Treaty Setup > New Treaty |
| Define Retain Order | Reinsurance > Treaty Setup > Retain Order |
| Define Risk Category | Reinsurance > Treaty Setup > Risk Category |
| Define Risk Factor | Reinsurance > Treaty Setup > Risk Factor |
| Define Premium Rate | Reinsurance > Treaty Setup > Premium Rate |
| Define Commission Rate | Reinsurance > Treaty Setup > Commission Rate |
| RI New Cession Batch | Reinsurance > Batch > RI New Cession |
| Customer Service Movement Batch | Reinsurance > Batch > CS Movement |
| Claim Recovery Batch | Reinsurance > Batch > Claim Recovery |
| RI Renewal Cession Batch | Reinsurance > Batch > RI Renewal |
| Facultative Reinsurance | Reinsurance > Facultative > New |
| Cession Adjustment | Reinsurance > Cession > Adjustment |
| Experience Refund Batch | Reinsurance > Batch > Experience Refund |
| Undo Cessions | Reinsurance > Cession > Undo |
| RI Query by Policy | Reinsurance > Query > By Policy |
| RI Query by Contract | Reinsurance > Query > By Contract |
| RI Query by Treaty | Reinsurance > Query > By Treaty |

---

## 9. Related Files

| File | Relationship |
|------|-------------|
| ps-claims.md | Claims — claim recovery trigger |
| ps-underwriting.md | UW — facultative RI trigger |
| insuremo-v3-ug-nb.md | NB — RI cession setup |
