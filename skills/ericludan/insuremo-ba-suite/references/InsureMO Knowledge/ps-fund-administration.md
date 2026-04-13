# InsureMO Platform Guide — Fund Administration
# Source: Fund Administration User Guide V25.04
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb-full.md instead
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"how does ILP Fund Administration work in InsureMO"** — fund transaction processing rules, charge deduction batch logic, auto premium holiday handling, ILP policy lapse mechanics, and fund price management.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for a Fund Administration-related gap
- Agent 6 is generating a **Config Runbook** for ILP fund items
- A BA needs to verify **transaction processing rules**, **charge deduction logic**, or **PLD/PJD calculation** behaviour

---

## Module Overview

```
Fund Administration
│
├── 12.1 Manage Fund Price                      ← Finance maintains fund prices for future transactions
├── 12.2 Perform Fund Transaction (Batch)       ← Buys/sells units for top-up, withdrawal, switch, surrender
├── 12.3 Deduct Charges (Batch)                 ← Daily COI, policy fee, FMF charge deduction from TIV
├── Auto Premium Holiday (Batch)                ← Sets APH indicator when TIV insufficient and product allows
├── Auto Cancel Premium Holiday (Batch)         ← Cancels APH when PH end date reached
├── ILP Policy Lapse (Batch)                    ← Lapses policy when system date ≥ PLD
└── ILP Policy Lapse Sell All Units (Batch)     ← Sells remaining units after lapse; generates payable record
```

---

## Fund Administration Workflow — Standard Sequence

```
Upstream Triggers
  (New Business / Policy Alteration / Loan & Deposit / Premium Payment / Maturity / Annuity / Claim)
        │
        ▼
Step 12.1: Manage Fund Price
  └─► Step 12.2: Perform Fund Transaction (Batch)
        └─► Step 12.3: Deduct Charges (Batch)
              ├─► TIV sufficient → Deduct charge; move charge due date
              ├─► TIV insufficient; within NLP → Deduct all TIV; create misc debts; set PLD
              ├─► TIV insufficient; outside NLP → Calculate PLD
              │     ├─► PLD > MDD + 60 days → No PLD set; continue
              │     ├─► MDD < PLD < NDD → Set PLD; deduct pro-rate charge
              │     └─► NDD ≤ PLD ≤ MDD+60 → Set PLD; deduct full charge; move MDD
              └─► Auto Premium Holiday (Batch) [if premium overdue and product allows APH]
                    └─► Auto Cancel Premium Holiday (Batch) [when PH period expires]
                          └─► ILP Policy Lapse (Batch) [when system date ≥ PLD]
                                └─► ILP Policy Lapse Sell All Units (Batch) [after lapse date + waiting days]
```

**Downstream processing after fund transaction:**

| Process | Module |
|---|---|
| GL Posting | Perform Posting to GL |
| Letter Generation | Generate transaction / ILP letters |

---

## Policy Investment Account Structure

ILP policy investment accounts are structured as follows:

```
Level 1: Policy Investment Account  (per Fund: Fund A, Fund B, …)
│
└── Level 2: Policy Sub-account
      ├── RPA — Regular Premium Account
      ├── TPA — Top-up Premium Account
      ├── IUA — Initial Units Account
      └── AUA — Accumulation Units Account
```

Sub-account configuration is defined in **Product Configuration → ILP Sub Account Definition**.

**Sub-account configuration dimensions:**

| Column | Description |
|---|---|
| Account Type | IUA (3) / AUA (4) / AUA Single Top-up (6) |
| Fee Source | Which premium type feeds into this sub-account |
| Related with Policy Month | Yes / No |
| Start Policy Month | Month range start (if related with policy month) |
| End Policy Month | Month range end (if related with policy month) |
| Follow Minimum Investment Periods | Yes / No |
| Periods Type | Within Initial Contribution Period / After Initial Contribution Period / Not Relevant |

**Sample Product 1 Sub-account Setup:**

| Account Type | Fee Source | Related Policy Month | Period Type |
|---|---|---|---|
| IUA | Regular Premium | No | Within Initial Contribution Period |
| IUA | Start-up Bonus | No | Not Relevant |
| AUA | Regular Premium | No | After Initial Contribution Period |
| AUA | Power-up Bonus / Loyalty Bonus / RSP | No | Not Relevant |
| AUA (type 6) | Single Top-up | No | Not Relevant |

**Sample Product 2 Sub-account Setup:**

| Account Type | Fee Source | Start Month | End Month | Period Type |
|---|---|---|---|---|
| IUA | Regular Premium | 1 | 18 | Not Relevant |
| IUA | Start-up Bonus / Loyalty Bonus | No | — | Not Relevant |
| AUA | Regular Premium | 19 | 9999 | Not Relevant |
| AUA | RSP | No | — | Not Relevant |
| AUA (type 6) | Single Top-up | No | — | Not Relevant |

---

## Per-Process Reference

### 12.1 Manage Fund Price

**Purpose:** Finance personnel maintain fund prices (Bid and Offer prices) after receiving from fund house. Used by fund transaction batch to execute buy/sell.

> Refer to **Investment User Guide** for full fund price maintenance procedures.

**Key concepts:**
- Fund Price = net asset value based price defined by fund house
- Both Bid price and Offer price are maintained
- Holiday schedule maintained at fund level (refer to Investment User Guide)
- Fund Unit Decimal Places configured under Product Configuration → ILP Rules → Fund Unit DPs

---

### 12.2 Perform Fund Transaction (Batch)

**Purpose:** Reads all pending fund transaction records; performs buy/sell based on instructions in records; generates GL entries for backdated transactions.

**Prerequisites:**
- Policy has pending fund transaction records
- Current or forward price is available based on validity date of the transaction record
- Policy NOT frozen

**Procedures:**
1. Scheduled batch starts; system searches for pending transactions
2. If no pending transactions → end
3. System determines transaction parameters from pending records
4. System checks if current price (Bid or Offer as indicated) is available at Validity Date:
   - Price unavailable → Price Used Date = next available date after Validity Date; process ends
   - Price available → Price Used Date = Validity Date; Price Used = fund price at Validity Date; proceed
5. System processes transactions based on alteration type (top-up, partial withdrawal, switch, full surrender)
6. System generates transaction-related letters and ILP letters
7. Finance performs posting to GL

**Transaction Record Parameters:**

| Parameter | Description |
|---|---|
| Fund Type | Which fund to transact |
| Buy / Sell | Direction of transaction |
| By Units / By Value | Transaction method |
| Units or Value | Quantity to transact |
| Forward / Now Price | Price timing |
| Bid / Offer Price | Price type |
| Validity Date | Used to determine Price Used Date; if price unavailable at Validity Date, system uses next available forward price |

**General Transaction Rules:**
- Transactions processed in order of application sequence
- System calculates units to buy/sell; updates unit holding
- If fund price > buy/sell value AND calculated units (after rounding) < 0.01 → no units bought/sold
- If buying at Offer price → system calculates and generates Bid-Offer spread record:
  ```
  Bid-Offer Spread = (Offer Price Used − Bid Price of date) × Units Transacted
  ```
- If application date is a fund holiday → system automatically applies next working day price (holiday configured at fund level)
- Fund unit decimal places configured under Product Configuration → ILP Rules → Fund Unit DPs

---

#### Rules for ILP Free Look

**3 free look options defined at product level:**

| Option | Gross Refund Formula | TIV < Premium | TIV > Premium |
|---|---|---|---|
| Default Option | Premium Received − TIV Loss (if any) | Deduct loss from refund | Record difference as gain |
| Refund Premium | Premium Received | Record difference as loss | Record difference as gain |
| Refund TIV + Charges | TIV + all charges deducted | — | — |

---

#### Rules for ILP Partial Withdrawal

**General rules:**
- System re-calculates sum assured for main product (per product definition)
- If remaining units insufficient for withdrawal amount → application status changed to Suspend

**Deduction Sequence (Dual Account — sub-account level):**

| Layer | Source | Order within Layer |
|---|---|---|
| 1st (Top-up) | Single Top-up + Recurring Single Premium | LIFO (last in, first out) |
| 2nd (Premium Increase) | New stream for increased regular premium | LIFO |
| 3rd (Regular Premium) | Original regular premium stream | LIFO |

Within each layer, by proportional deduction across funds:
```
Fund A withdrawal amount in layer = (Fund A Value / Total TIV in layer) × Total withdrawal amount in layer
```

**Deduction Sequence (Single Account — no sub-accounts):**
Same three-layer LIFO order; fund records NOT split by sub-account; total units combined at fund level.

**Partial Withdrawal Charge Calculation:**

| Method | Formula |
|---|---|
| By Units | Withdrawal Units × Fund Price × Partial Withdrawal Charge Factor |
| By Value | Withdrawal Value × Partial Withdrawal Charge Factor |

**Partial Withdrawal Example (Dual Account):**

*Example 1: Top-up layer sufficient (Withdraw 600.00):*

| Fund | Premium Type | Fund Value |
|---|---|---|
| Fund A | Regular Premium | 1,000.00 |
| Fund A | Recurring Single Premium | 500.00 |
| Fund A | Single Top-up | 400.00 |

Result: Single Top-up 266.67 + Recurring Single Premium 333.33 = 600.00 confirmed

*Example 2: Top-up layer insufficient (Withdraw 600.00):*

| Fund | Premium Type | Fund Value |
|---|---|---|
| Fund A | Regular Premium | 1,000.00 |
| Fund A | Recurring Single Premium | 166.67 |
| Fund A | Single Top-up | 133.33 |

Result: Single Top-up 133.33 + Recurring Single Premium 166.67 + Regular Premium 300.00 = 600.00 confirmed

---

#### Rules for ILP Full Surrender

- Surrender charge deducted from full surrender amount upon fund transaction

---

#### Rules for Fund Switch

**Switch by Value:**
- If units insufficient to cover amount → system auto-switches all units under that fund; transacts switch fee first

**Switch by Percentage:**
```
Switch out units per fund = Current units × Switch out %
Switch out amount per fund = Switch out units × Fund price
Total switch out amount = Σ Switch out amounts across all funds
Switch in units per fund = Total switch out amount × Switch in % per fund / Fund price
```

**Switch Fee Rules:**

| Parameter | Config Location |
|---|---|
| Times of Free Switch per Period | Product Definition → ILP Rules → Switch → Times of Free Switch per Period |
| Period for Free Switch | Product Definition → ILP Rules → Switch → Period for Free Switch |
| Min Total Switch Fee Amount | Product Definition → ILP Rules → Switch → Min Total Switch Fee Amount |
| Same Day Price for Switch | Product Definition → ILP Rules → Switch → Same Day Price for Switch |
| Fee Source (switch-in / switch-out) | Product Definition → ILP Charge List → Fee Source |
| Switch Fee Formula | Product Definition → FMS list → Switch Fee Formula |

- Policy Holder allowed N free switches per predefined period; subsequent switches charged
- Switch fee applies at policy level; one event = one switch
- Switch fee cannot be amended by user
- Settlement: cash / cheque / unit deduction (unit deduction: fee inclusive of units switched out)

**Fee Source = Deduction from Switch-Out Fund:**
- Switch fee deducted from switch-out fund per calculation formula
- System generates one transaction per fund switch
- Sequence: sell switch-out funds → deduct switch fee → buy switch-in funds
- Switch by units: estimate fee using latest price; re-calculate on confirmation using actual price
- Multiple switch-in funds: split fee proportionally across switch-in amounts

**Fee Source = Deduction from Switch-In Fund:**
- All amount/units used for buying switch-in fund
- Switch fee deducted from switch-in fund
- Two fund transaction applications per fund switch: one for switch + one for switch charge per switch-in fund

**Fund Switch Price Date Rules:**

| Same Day Price for Switch | Switch-Out Price | Switch-In Price |
|---|---|---|
| Yes | Validity Date (T) price | Same Validity Date (T) price |
| No | Validity Date (T) price | Switch-out settled day's price (T+1) |

*Example (Same Day Price = Yes): Switch Validity Date = 2023/11/20:*
- 2023/11/21: price for 2023/11/20 uploaded → switch-out confirmed using Fund A price of 2023/11/20; switch-in pending generated with Price Effective Date = 2023/11/20
- 2023/11/22: price for 2023/11/21 uploaded → switch-in confirmed using Fund B price of **2023/11/20**

*Example (Same Day Price = No): Switch Validity Date = 2023/11/20:*
- 2023/11/21: switch-out confirmed using Fund A price of 2023/11/20; switch-in pending with Price Effective Date = 2023/11/21
- 2023/11/22: switch-in confirmed using Fund B price of **2023/11/21**

**Unit Redemption for Cash Rider / UDR:**
- For apply premium through unit redemption for cash rider (hybrid policy) or UDR (normal ILP) → system moves rider due date after confirming transaction

---

#### Fund Holiday Rules

- Fund price entry NOT required for fund holiday dates
- When user uploads price for next working day → system auto-populates same price for fund holiday date(s) in between
- For fund transactions with application date = fund holiday → system still generates pending transactions on that day using fund price at T day

*Example: Fund A holiday on 05/01/2024; charge due date = 05/01/2024:*

| Process Date | Charge Due Date | Price Date | Execution Step | Expected Result |
|---|---|---|---|---|
| 05/01/2024 | 05/01/2024 | 05/01/2024 | Charge Deduction Batch | Generate pending sell transaction with price effective date 05/01/2024 |
| 09/01/2024 | — | — | Enter fund price | Price updated for 08/01/2024; price of 05/01/2024 = same price |
| 09/01/2024 | — | — | Fund Transaction Batch | Transaction record confirmed; policy units updated |

---

#### Rounding Rules

- Fund unit decimal places defined per ILP product under Product Configuration → ILP Rules
- Transaction Units = Round Down (Transaction Amount in fund currency / Price, Fund Unit DPs)
- If remaining units after confirmed sell < 0.0001 → system auto rounds down to 0.0000
- Transaction Amount by Fund Currency = Round Off (Transaction Units × Fund Price, 2)
- If Fund Currency = Policy Currency: Transaction Amount by Policy Currency = Transaction Amount by Fund Currency
- If Fund Currency ≠ Policy Currency:
  ```
  Transaction Amount by Policy Currency = Round Down (Transaction Amount by Fund Currency × Exchange Rate, 2)
  ```

**Rounding Examples:**

*Redemption by Units (Policy Currency SGD, Fund Currency USD):*
- Fund A: 100 units, Fund Price = 1.17636, Exchange Rate USD→SGD = 1.42310
- Transaction Amount by Fund Currency = Round Off (100 × 1.17636, 2) = 117.64 USD
- Transaction Amount by Policy Currency = Round Down (117.64 × 1.42310, 2) = 167.41 SGD

*Redemption by Value (Withdraw 1,000 USD):*
- Fund Price = 1.17636
- Apply Units = Round Down (1000 / 1.17636, 4) = 850.0799 units

*Subscription (SGD top-up 1,000; Fund A USD 50%, Fund B SGD 50%):*
- Exchange Rate SGD→USD = 0.70260; Pending: Fund A = 351.30 USD, Fund B = 500.00 SGD
- Fund A Price = 1.17636 → Units = Round Down (351.30 / 1.17636, 4) = 298.6330
- Fund B Price = 1.76382 → Units = Round Down (500.00 / 1.76382, 4) = 283.4756

---

### Auto Premium Holiday (Batch)

**Purpose:** Daily batch that sets auto premium holiday (APH) indicator on ILP policies where premium is overdue, product allows APH, and TIV is sufficient to cover charges during holiday period.

**Prerequisites:**
- Policy status is Inforce
- Policy NOT frozen
- Main product is ILP AND product allows APH in product configuration
- Premium Status is Regular
- Policy has NO Potential Lapse Date
- System Date ≥ Premium Due Date + Grace Period (including Additional Grace Period)
- If policy has MIP (Minimum Investment Period): system date must have passed end of MIP

**Processing Logic (sequential checks):**

```
Step 1: Check if premium is paid up to date
  (batch process date ≥ premium due date + grace period + additional grace period)
  ├─► Paid up to date → proceed to Charge Deduction; end APH check
  └─► Not paid up to date → Step 2

Step 2: Does basic product allow auto premium holiday?
  ├─► No  → Set PLD at end of grace period; end
  └─► Yes → Step 3

Step 3: Allowed premium holiday months > 1 installment premium period?
  Allowed PH months = Max PH Months − Aggregated PH Months used
  (Max PH Months configured under Product → CS Rules)
  ├─► No  → Set PLD at end of grace period; end
  └─► Yes → Step 4

Step 4: TIV sufficient to cover charges from APH start date to APH end date?
  APH Start Date = premium next due date
  APH End Date   = nearest premium due date before (start date + allowed PH months)
  ├─► Not sufficient → Set PLD at end of grace period; end
  └─► Sufficient     → Step 5

Step 5: Set auto premium holiday
  - Set auto premium holiday indicator = 'Y'
  - Cancel any pending Recurring Single Premium billing records
  → End
```

---

### Auto Cancel Premium Holiday (Batch)

**Purpose:** Daily batch that cancels premium holiday and moves premium due date when PH end date is reached.

**Prerequisites:**
- Policy status is Inforce
- Policy premium status is Regular
- Policy is an ILP policy
- Policy has NO Potential Lapse Date
- Policy has NO miscellaneous debts
- Premium Holiday status = Yes
- System Date ≥ Premium Holiday End Date
- Policy NOT suspended by other transactions

**Procedures:**
1. System extracts eligible policies
2. System updates premium holiday status from 'Yes' to 'No'
3. System moves policy due date to nearest due date ≥ Charge Due Date

---

### 12.3 Deduct Charges (Batch)

**Purpose:** Daily batch that deducts ILP policy charges (COI, Policy Fee, Fund Management Fee, expense charges, guaranteed charge for variable annuity) from policy TIV; handles premium holiday period; calculates PLD.

**Charges Covered:**
- Cost of Insurance (COI)
- Policy Fee (PF)
- Fund Management Fee (FMF)
- Guaranteed Charge (variable annuity)
- Expense Charge (if configured for fund deduction)
- Unit Redemption Rider (URP) deduction

> Charge deduction is triggered by daily batch AND by buy transactions.

**Prerequisites:**
- Policy status is Inforce
- Policy is investment-linked
- Policy NOT frozen
- No pending fund transactions
- System date ≥ Charge due date

**Charge Deduction Procedures (full decision tree):**

```
Step 1: Is policy in Premium Holiday?
  ├─► No  → Step 4
  └─► Yes → Step 2

Step 2: Accumulate PH counter; check PH counter vs Max PH Period
  PH counter calculated from PH Start Date to Charge Due Date (months)
  ├─► PH counter < Max PH Period  → Continue Premium Holiday; Step 4
  └─► PH counter ≥ Max PH Period  → Step 3

Step 3: Cancel Premium Holiday on PH end date
  1. Move premium due date to next due date
  2. Flag: cannot trigger auto premium holiday again at end of grace period
  → Step 4

Step 4: Is TIV sufficient to cover 1 installment charge?
  ├─► Yes → Step 5
  └─► No  → Step 6

Step 5: Deduct charge and move charge due date
  1. Generate pending fund transaction records (sell) for 1 installment charge
     (includes PF, COI, URP; price effective date = charge due date + price waiting days)
     NOTE: Price waiting days defined at fund level
  2. Move charge due date to next MDD
  3. UDR next due date moved after fund transaction batch confirmation
  → End

Step 6: Is charge due date within (policy commencement date + NLP)?
  ├─► Yes (within NLP)  → Step 7
  └─► No / no NLP       → Step 8

Step 7: Deduct all TIV (within NLP period)
  1. Generate pending sell-all-units record for prorated charge
  2. Create Miscellaneous Debts for outstanding charge up to next MDD
  3. If TIV = 0: generate Miscellaneous Debts for 1 installment charge directly
  4. Move charge due date to next
  5. Set PLD = max(charge due date, end date of premium grace period)
  → End

Step 8: Calculate PLD
  ├─► Calculated PLD > Current MDD + 60 days
  │     → No PLD set → Step 9
  ├─► Current MDD < Calculated PLD < Next MDD
  │     → Set PLD → Step 10
  ├─► Next MDD ≤ Calculated PLD ≤ Current MDD + 60 days
  │     → Set PLD → Step 5
  ├─► Calculated PLD = Current MDD
  │     → Set PLD → End
  └─► Policy already has existing PLD
        → Update PLD to newly calculated PLD

Step 9: Check if policy has existing PLD
  ├─► Yes → Clear existing PLD → Step 5
  └─► No  → Step 5

Step 10: Calculate and deduct pro-rate charge up to PLD
  1. Generate pending fund transaction records for pro-rate charge up to PLD
  2. Move charge due date to PLD
  3. If TIV insufficient to confirm (due to price decrease) → sell all units; generate misc debts for outstanding charge up to PLD after fund transaction batch
```

---

#### Charge Deduction Rules — Projected Lapse Date (PJD)

1. PJD calculated at every monthversary deduction for ILP policies only
2. If calculated PJD < monthversary date + 3 months → record PJD on policy; do NOT recalculate
3. If calculated PJD ≥ monthversary date + 3 months → do NOT record PJD; clear existing PJD if any
4. PJD is cleared once Potential Lapse Date (PLD) is set on the policy

**PJD Formula:**
```
PJD = Charge Due Date + (TIV or RPA / Sum of monthly charges including current month charge)
```

---

#### Charge Deduction Rules — Non-Lapse Guaranteed (NLG)

Applicable to ILP products with non-lapse guaranteed feature.

**Eligibility:** Policy is eligible for NLG if basic investment premium AND regular top-up are paid on time.

**During NLG Period (per Product Definition → ILP Rules):**

| Condition | Action |
|---|---|
| TIV ≥ total monthly charge | Deduct charge normally; move charge due date |
| TIV < total monthly charge | Deduct units to zero; record insufficient amount as Miscellaneous Debts; move charge due date; set PLD to end of grace period |
| System Date ≥ Premium Due Date + Grace Period AND regular premium still outstanding | Set PLD to end of grace period; lapse policy on PLD |
| TIV deducted to zero but policy still Inforce in NLGP | Continue deducting future monthly charges; record charge directly as debts (no fund transaction) until end of premium grace period |

---

#### Charge Deduction Rules — COI for Layered Sum Assured

Applicable to ILP products with level-pay COI where CS ILP Increase Sum Assured creates new SA segments.

- System uses age and SA on segment level to capture COI rate
- COI fees accumulated per active segment

---

### ILP Policy Lapse (Batch)

**Purpose:** Daily batch that validates PLD and lapses ILP policies where system date ≥ PLD.

**Prerequisites:**
- Charge Deduction batch has completed
- Policy is Inforce
- Policy NOT frozen
- Policy is investment-linked
- Policy has PLD (Potential Lapse Date)
- No pending fund transaction records

**Procedures:**
1. System recalculates PLD
2. Check: system date ≥ new PLD?
   - No → end
   - Yes → Step 3
3. Check: premium holiday indicator = Y?
   - No → Step 6 (lapse)
   - Yes → Step 4
4. System checks product-level option after max PH period:
   - Lapse directly after max PH period (no premium received before end of grace period including additional grace period) → Step 6
   - Stay Inforce after max PH period (no premium received before end of grace period NOT including additional grace period) → Step 5
5. System validates IUA remaining account value:
   - If premium still outstanding AND IUA balance > 0:
     - Deduct EEC fee
     - Transfer remaining IUA amount to AUA
     - Transfer follows same fund code (in and out)
     - If no matching fund code under transfer-in account → system auto-creates fund records
     - Transfer-out: treated as withdrawal by units (pending allowed)
     - Transfer-in: treated as top-up premium allocation (pending allowed)
     - Both transfer-out and transfer-in use same day's fund price (transfer-out date price)
     - Transfer-in amount = Transfer-out units × fund price − EEC fee
     - If pending fund transaction exists: confirm original pending transaction first, then process transfer
6. System lapses the policy at end of PLD grace period:
   - Policy Status → Lapsed
   - All inforce benefit statuses → Lapsed
   - Lapse Reason → 'ILP Lapse'
   - Lapse Date → end date of PLD grace period

---

### ILP Policy Lapse Sell All Units (Batch)

**Purpose:** After ILP policy lapse, sells remaining fund units and generates payable record for refund.

**Prerequisites:**
- Policy is Lapsed
- Policy NOT frozen by other transactions
- Remaining TIV > 0
- System Date ≥ Lapse Date + Waiting Days After Lapse (configured in product configuration)

**Procedures:**
1. System extracts eligible lapsed policies
2. System sells out all remaining units (treated as withdrawal):
   - Generate fund transaction for TIV refund
   - Calculate and deduct EEC fee from withdrawal amount
   - Calculate net withdrawal amount
   - Generate payable record for net amount

---

## Config Gaps Commonly Encountered in Fund Administration

| Scenario | Gap Type | Config Location |
|---|---|---|
| Fund unit decimal places | Config Gap | Product Configuration → ILP Rules → Fund Unit DPs |
| Sub-account type and fee source definition | Config Gap | Product Configuration → ILP Sub Account Definition |
| Free look option (Default / Refund Premium / Refund TIV+Charges) | Config Gap | Product Factory → ILP Rules → Free Look Option |
| Times of free switch per period | Config Gap | Product Definition → ILP Rules → Switch → Times of Free Switch per Period |
| Min total switch fee amount | Config Gap | Product Definition → ILP Rules → Switch → Min Total Switch Fee Amount |
| Same day price for switch (Y/N) | Config Gap | Product Definition → ILP Rules → Switch → Same Day Price for Switch |
| Switch fee formula | Config Gap | Product Definition → FMS List → Switch Fee Formula |
| Switch fee source (switch-in vs switch-out fund) | Config Gap | Product Definition → ILP Charge List → Fee Source |
| Price waiting days (for charge deduction price effective date) | Config Gap | Fund Level → Price Waiting Days |
| Max Premium Holiday Months | Config Gap | Product → CS Rules → Max Premium Holiday Months |
| Allow auto premium holiday (Y/N) | Config Gap | Product Configuration → ILP Rules → Allow APH |
| Minimum Investment Period (MIP) definition | Config Gap | Product Definition → ILP → Allowed Minimum Invest Periods |
| NLP (Non-Lapse Period) duration | Config Gap | Product Definition → ILP Rules → NLP |
| Non-Lapse Guarantee feature (Y/N) | Config Gap | Product Definition → ILP Rules → NLG |
| COI layered SA (Y/N) | Config Gap | Product Definition → ILP Rules → Level Pay COI |
| PLD grace period | Config Gap | Product Definition → ILP Rules → PLD Grace Period |
| Waiting days after lapse (for sell-all-units batch) | Config Gap | Product Configuration → ILP → Waiting Days After Lapse |
| Fund holiday calendar | Config Gap | Investment → Fund Holiday Configuration |
| EEC fee definition | Config Gap | Product Definition → ILP Charge List → EEC |
| Partial withdrawal charge factor | Config Gap | Product Definition → ILP Charge List → PW Charge Factor |
| Surrender charge schedule | Config Gap | Product Definition → ILP Charge List → Surrender Charge |

---

## NAV Calculation (from Fund Admin UG)

### NAV Formula
NAV = (Fund Assets − Fund Liabilities) / Total Units In Issue

| Component | Description |
|---|---|
| Fund Assets | Market value of all investments + cash |
| Fund Liabilities | Management fees + other charges |
| Total Units | All outstanding units across all policies |

### NAV Frequency
- Daily NAV: Standard for most ILP funds
- Real-time NAV: For switching (latest available NAV)
- Bid/Offer spread: Offer = NAV x (1 + spread%), Bid = NAV x (1 - spread%)


## Surrender Value Calculation (from Fund Admin UG)

### SV Formula
SV = Units x Bid NAV − Surrender Charge − Outstanding Charges

| Component | Rule |
|---|---|
| Units | Policy units at surrender date |
| Bid NAV | NAV at surrender (not offer) |
| Surrender Charge | % of SV, declining by year |
| Outstanding Charges | Unpaid management fees + RI premiums |

### LIFO Deduction
When units are redeemed: oldest units redeemed first (LIFO).
This affects tax and gain/loss calculation.


## INVARIANT Declarations (Fund Administration Module)

```
INVARIANT 1: Fund transaction cannot proceed if policy is frozen
  Enforced at: Perform Fund Transaction (Batch)
  Effect: Policy skipped; pending transaction records remain unprocessed

INVARIANT 2: Fund transaction cannot proceed if no price available at or after Validity Date
  Enforced at: Perform Fund Transaction (Batch)
  Effect: Price Used Date set to next available date; process ends for that record

INVARIANT 3: Charge deduction cannot proceed if pending fund transactions exist
  Enforced at: Deduct Charges (Batch)
  Effect: Policy skipped for that deduction cycle

INVARIANT 4: Auto Premium Holiday cannot be set if policy already has PLD
  Enforced at: Auto Premium Holiday (Batch)
  Effect: APH not set; PLD calculation proceeds instead

INVARIANT 5: Auto Premium Holiday cannot retrigger after being cancelled at max PH period end
  Enforced at: Deduct Charges (Batch) → Step 3
  Effect: System blocks re-triggering of APH at end of grace period post-cancellation

INVARIANT 6: ILP Policy Lapse batch requires Charge Deduction batch to have completed first
  Enforced at: ILP Policy Lapse (Batch) — prerequisite check
  Effect: Lapse batch not executed if charge deduction has not run

INVARIANT 7: ILP Policy Lapse Sell All Units requires TIV > 0 and waiting days elapsed after lapse
  Enforced at: ILP Policy Lapse Sell All Units (Batch)
  Effect: Policy skipped if TIV = 0 or waiting period not yet passed

INVARIANT 8: Partial withdrawal moves to Suspend status if remaining units insufficient
  Enforced at: Fund Transaction Rules → Partial Withdrawal
  Effect: Application status set to Suspend; no partial execution

INVARIANT 9: PJD is cleared once PLD is set on policy
  Enforced at: Charge Deduction Rules — PJD
  Effect: System nullifies PJD upon PLD being recorded
```

---

## ⚠️ Limitations & Unsupported Scenarios

> This section documents known limitations and scenarios NOT supported by the system. Updated: 2026-03-14

### Fund Value & Policy Value

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Min Policy Fund Value Monitoring | Not automated | Code | Requires custom monitoring for complex formulas |
| Min Liquidity Level | Not supported | Code | Real-time liquidity monitoring needs development |
| Dynamic Asset Allocation | Limited | Config | Predefined strategies only |

### Fund Transactions

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Real-time Switch | Batch processing | Config | Real-time switch requires integration |
| Partial Withdrawal Limits | Fixed formulas | Config | Complex min/max rules need development |
| Fund Valuation | Daily only | Config | Intra-day valuation not available |

### Account Management

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Multi-Currency Accounts | Limited | Config | Check product configuration |
| Sub-Account Management | Limited to predefined | Config | Custom sub-accounts need development |
| Account Merge | Not supported | Code | Policy merge requires custom development |

---

## Related Files

| File | Purpose |
|---|---|
| `ps-customer-service.md` | CS freeze status blocks fund transactions; ILP Partial Withdraw, Switch, RSP, Premium Holiday items in CS module |
| `ps-renewal.md` | Non-forfeiture disposal triggers ILP rider charge deduction from TIV; renewal freeze affects fund transaction eligibility |
| `ps-bonus.md` | CB/SB allocation interacts with TIV calculations; APL offset uses fund-derived values |
| `ps-loan-deposit.md` | Policy loan accounts interact with TIV and charge deduction in non-lapse guarantee scenarios |
| `ps-product-factory.md` | Product-level config: APH rules, NLG, sub-account definition, switch fee, charge list, PLD grace period |
| `insuremo-ootb-full.md` | OOTB capability classification (use for Gap Analysis) |
| `output-templates.md` | BSD output templates for fund administration-related gaps |