# InsureMO V3 User Guide — Component Rules

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-ug-component-rules.md |
| Source | 24_Component_Rules.pdf |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | 2015-02-11 |
| Category | Rules / Calculations |
| Pages | 103 |

## 1. Purpose of This File

**⚠️ CORE REFERENCE — Most important reference document for BSD writing.** Contains all fundamental calculation rules used throughout LifeSystem. Every module (NB, CS, Claims, Finance, etc.) references these component rules. Used to answer questions about: accounting dates, premium calculations, surrender values, bonus calculations, tax, APA, inforce SA, and all formula specifications.

---

## 2. Accounting Date

Accounting Date = the date value used for creation of all journal entries fed to GL. Accounting Date is populated for each financial transaction based on business rules. **Accounting Date has NO impact on front-end customer-facing transactions.**

**General Rules:**
- Accounting date cannot be in a closed accounting month
- Accounting date should be first day of current accounting month if [condition]
- Only payment date can be in the future accounting month

**Online Transactions — Collections:**
- Fee Type = 11, Transaction Mode = Online
- System date → Accounting_Date in T_Cash
- Backdating NOT allowed

**Online Transactions — Payments:**
- Fee Type = 32, Transaction Mode = Online
- Payment date cannot be earlier than system date
- Payment date CAN be a future date
- Cheque date → Accounting_Date

**Batch Process — Collections:**
- Fee Type = 11, Transaction Mode = Batch
- Source file header's value date → Accounting_Date

**Batch Process — Payments:**
- Direct Debit: Valuation date → Accounting_Date
- Cheque Printing: Check date (always future-dated) → Accounting_Date

**Unit Linked Transactions:**
- Transaction Date = Accounting Date always
- Exception: D110, D107, D108 → system date OR due date, whichever later

**Premium Accrual Transactions:**
- Fee Type 41, Fee Status 0 or 4
- Accounting Date = last day of current accounting month

**Provision / Write-off / Reinstatement:**
- Fee types F199, FXX, FYY
- Accounting Date = last day of current accounting month

---

## 3. Tax Rules

### GST/ST
Generated when:
- **Premium Payable:** NB premium, Renewal premium, CS premium (add rider, reinstatement, increase SA)
- **Premium Receivable:** CS premium refund (freelook, decrease SA, cancellation)

### Stamp Duty
Generated when:
- Collection
- Policy Loan

### Withholding Tax
Generated when:
- Medical Billing Payment
- Medical Billing Reversal (medical billing reversal + freelook)
- Claim Interest
- Claim Direct Billing without Prior Authorization
- Deposit Capital
- Deposit Interest
- Maturity Interest

---

## 4. Advance Premium Account (APA)

APA = full premiums paid in advance, on which the company may pay interest. APA is for premiums only (not like discounted premium where interest is given as up-front discount).

### Creation of APA

**At New Business:**
1. Customer requests money deposited into APA after policy inforce
2. User sets Advance Premium indicator = 'Y' on NB UI
3. Cashier parks money into general suspense
4. When policy turns inforce: suspense balance → APA automatically
5. If no APA request at NB: normal auto NB suspense refund applies

**At Customer Service:**
1. Customer requests money deposited into APA
2. User parks money directly into APA on Counter Collection UI (amount ≤ required TIPs)
3. Alternative: transfer from general suspense to APA (amount ≤ required TIPs)
   - Transfer Effective Date can be backdated (not earlier than Inforce Date)

### APA Interest
- Interest accrual starts when policy is inforce
- Interest accrual ceases the moment policy is no longer inforce (even if outstanding APA balance)
- Interest rate: configured at global level
- APA interest = compound interest
- Interest capitalized on: premium due date / APA withdrawal date / interest change date / new deposit received

### APA Processing for Billing
1. Renewal draw job calculates premium to bill (at Next Due Date − 30 days)
2. Move due date job offsets from premium:
   - Suspense
   - APA + interest (up to Next Due Date)
   - Cash bonus (option 2) + interest
   - Survival benefit (option 2) + interest
3. Premium notice generation considers: suspense, APA, cash bonus, survival benefit

### APA Processing for Collection
- **Before end of grace period:** APA applied to premiums due if within lead days
- **After grace period (policies with cash value):** System raises APL; APL repaid using: suspense → APA → cash bonus → survival benefit
- **After grace period (policies without cash value):** Pro-rated premium applied; policy lapses

### APA Messages Displayed When
- Policy loan application registered
- Partial surrender processed
- Bonus surrender processed
- Policy alteration to reduce premium term
- Cancellation of policy or full surrender
- Cancellation of benefit
- Policy alteration to reduce premium
- Reduction of sum assured
- Partial conversion
- Waiver of extra premium

### APA Refunds and Withdrawals
- Online APA payment (surrender): through Payment Requisition; interest capitalized on entry to Payment Selection page
- Batch APA payment (maturity): APA included in payment amount
- Full Conversion: APA balance refunded by user

### Reversals
- Cancellation of APA amount applied to premium or refund: via Cancel_Collection or Cancel Payment
- Cancelled amount → APA (unless status = Lapsed/Terminated → General Suspense instead)

### Reduced Paid-up and ETA
- System SUSPENDS reduced paid-up and ETA if APA balance exists
- After interest capitalization: user refunds APA, then proceeds with paid-up or ETA

### Maturity
- After interest capitalization: APA paid out together with claims proceeds

### Claims and Terminations
- When main plan is terminated (any claim type): APA refunded with claim proceeds
- Waiver of premium: APA refunded with claims proceeds if no other cash-paying benefits (after interest capitalization)
- Partial waiver (split into waived + regular benefit): APA NOT refunded
- Partial waiver (fixed term, e.g., 10-year full waiver on 20-year policy): APA refunded once waiver period over

---

## 5. Age Basis

Age basis = common age calculation method for product. Used for calculation and validation in NB, CS, Claim, and RI.

**Three types:**

| Type | Full Name | Logic |
|------|-----------|-------|
| ALAB | Age Last Anniversary Birthday | Always round DOWN to nearest complete year |
| ALMB | Age Last Monthiversary Birthday | Always round DOWN to nearest complete month |
| ANB | Age Next Birthday | Always round UP to nearest complete year |

**Reference Date:** Can be policy commencement date, anniversary date, or other date per module processing rules.

---

## 6. Benefit Period

Benefit period = period that benefit is paid up to a certain age or for a certain period.

**Rules:**
- Benefit period is premium rate dependent
- Benefit period can be defined in product

---

## 7. Bonus Calculation

### Cash Bonus

```
CB = Initial SA / unit rate × cash bonus factor
CB = premium before discount / unit rate × cash bonus factor
CB = unit × cash bonus factor
```

- Bonus effective date = next bonus due date on policy benefit level
- Rounding: round to next higher cent

### Interim Bonus

```
Interim Bonus = latest reversionary bonus × adjusted months / 12
```

**Adjusted months rules (Fully Paid):**
- For claim: months between next anniversary from claim event date and next bonus due date − 1 year
- For surrender: crosses 31 Dec? → conditional calculation
- For maturity: next bonus due date ≤ maturity date → conditional calculation

**Adjusted months rules (Regular and Premium Waived):**
- For claim: uses claim event date to get corresponding next anniversary; collects outstanding premium
- For surrender: complex conditional based on next premium due date vs next bonus due date − 1 year

### Reversionary Bonus

```
RB = bonus rate × calculation basis / unit rate + compounded bonus
compounded bonus = compounded bonus rate × accumulated bonus
```

- Bonus type + plan type → RB factor → basic bonus rate + compounded bonus rate
- Bonus effective date = next bonus due date − 1 year
- Rounding: round to next higher cent

### Terminal Bonus

Multiple formula types:

**By attaching reversionary bonus:**
```
TB = accumulated RB × terminal bonus factor / unit rate
```

**By accumulated cash bonus declared and vested:**
```
TB = accumulated CB with interest × terminal bonus factor / unit rate
```

**By initial SA and completed policy year:**
```
TB = initial SA × completed policy year × terminal bonus factor / unit rate
```

**By single premium (surrender):**
```
TB = [SP × Yield Factor Y / Unit Rate × (365−D) + SP × Yield Factor Y+1 / Unit Rate × D] / 365 − SV of Basic SA − SV of Accumulated RB − SV of Interim Bonus
```
Where Y = complete policy years surrendered, D = complete days from last anniversary to surrender validate date

---

## 8. Expense Deduction

Two methods:

### From Premium
- Expense calculated and deducted upon premium collection
- Remaining money allocated to each fund

### From Account
```
Expense fee = premium due × expense deduct rate
```
- Expense = % of premium due; rate varies with policy year
- Deducted on each premium due date
- Rounding: 3 decimal places intermediary, 2 decimal places final

---

## 9. Inforce Sum Assured

Used in: CS query, risk aggregation in UW, claim amount payable.

**Incomplete Year Calculation Methods:**

| Method | Formula |
|--------|---------|
| Last complete year | Xth year Yth month = Xth year SA |
| Next complete year | Xth year Yth month = (X+1)th year SA |
| Linear interpolation by month | Xth year Yth month = SA_X + (SA_{X+1} − SA_X) × Y/12 |
| Linear interpolation by day | Xth year Yth day = SA_X + (SA_{X+1} − SA_X) × Y/365 |
| Exponential method | Contained in complete year formula |

**Rounding:** Truncate to 10 decimal places → round to nearest dollar

**Decreasing Term Rider:**
```
Inforce SA_t = Initial SA − (t × Initial SA / n)
```
Where t = complete policy years between commencement and transaction date (0 to n−1)

**Family Protection Rider:**
```
Inforce SA_x = Monthly Benefit × 12 × 1.021537 × [(1+i)^{n-x+1} − 1] / i × (1+i)^{n-x+1}
```
Where i = 0.04

**Increasing Term Rider:**
```
Inforce SA_t = (1 + t × 10%) × Initial SA
```

---

## 10. ILP Premium Stream Configuration

For ILP regular premium stream, parameter `2062410001-INCR_WITH_INACTIVE_STREAM`:

**If N:** System continues regular premium stream. Each premium portion uses its own year's expense rate.

**If Y:** System does NOT continue regular premium stream. New premium portions use first year's expense rate.

---

## 11. Limits

### Age Limit
- Life assured entry age (at NB/benefit commencement)
- Life assured renewal age
- Joint Life assured entry/renewal age
- Life assured entry/renewal expiry age
- Policyholder entry/renewal age
- Top-up age

### Fund Limit (ILP)
**At product level:** Allow partial withdraw, min partial withdrawal value, min remaining amount, switch fee basis, free switch times.

**At global level:** Min partial withdrawal, min remaining, min switch out, min remaining after switch out, switch-in/out per period limits.

**At product fund level:** Min partial withdrawal, min remaining, min switch out, min remaining, switch-out per period.

### Initial Sum Assured Limit
- Based on: initial SA, product code, age, occupation class, payment method
- Cannot exceed product-defined limits

### Payment Method Limit
- Non-ILP: defined at product level
- ILP: defined at fund level

### Premium Limit
- Initial premium, subsequent premium
- ILP regular premium increase/decrease
- ILP recurring top-up, ad-hoc top-up
- ILP: product-level table has higher priority than global-level table

### Term Limit
- Premium payment term, coverage term
- Deferred/installment/guaranteed period (annuity)
- Level period min/max months (mortgage)

### Tolerance Limit
Global parameter in base currency.

**For New Business (Accepted/Conditionally Accepted):**
```
1. Exchange tolerance limit to policy currency
2. If total inforcing premium > collection ≥ total inforcing premium − tolerance:
   → Apply premium with tolerance
   → If investment product: invest in bucket WITHOUT tolerance
   → Else: leave suspense
```

**For Renewal:**
- Traditional: if installment > collection ≥ installment − tolerance: apply with tolerance
- Investment: if bucket size > allocated ≥ bucket size − tolerance: generate pending fund transaction

---

## 12. Premium and Sum Assured Calculation

### SA Calculation

| Product Type | SA Formula |
|-------------|-----------|
| Manual indicator | SA = user entered |
| Common products | SA = user entered |
| Single premium (premium→SA) | SA = DeP × unit rate / PR |
| Annuity (installment amount) | SA = annuity rate × DeP / unit rate |
| Great Senior Care | SA = SA rate × unit |
| Smart saver rider | SA = DeP × unit rate / PR |

### Premium Calculation (Common Products)

```
Gross premium = {[(PR − LSD) × SA/unit rate] − SpD × [(PR − LSD) × SA/unit rate] + PF} × MF
```

Where:
- PR = premium rate from table
- LSD = Large SA Discount rate
- SpD = Special Discount rate (staff, family, agent, etc.)
- PF = policy fee
- MF = modal premium factor

**Rounding:**
- (PR − LSD) × SA/unit rate: truncate to 2 dp
- Gross premium: round UP to next 5 or 10 cents

### ILP Products

```
Single/Regular Investment Premium = DeP × MF
```

### Mortgage Products

Premium rate interpolation:
```
PR of actual interest = PRL + (IntA − IntL) / (IntH − IntL) × (PRH − PRL)
```

---

## 13. Extra Premium Calculation

**Type 1 — $ per X SA:**
```
Extra premium = EPR × SA / unit rate × MF
```

**Type 2 — % of premium:**
```
Extra premium = annual premium including PF × ratio × MF
```

**Type 3 — Rated up by age:**
```
Extra premium = [premium at (age + rated-up age) − premium at age] × MF
```

**Type 4 — Manual:**
```
Extra premium = user-entered amount (2 dp)
```

**Rounding:** All round up to next 5 or 10 cents

---

## 14. Surrender Charge

**Calculated on Premium:**
```
Surrender charge = annual premium of benefit × surrender charge rate × adjustment factor × (surrender amount / net fund value before surrender)
```

Adjustment factor rules:
- Initial: 1
- Subsequent: `1 − surrender amount / net fund value before surrender`
- Each subsequent surrender: `prior factor × (1 − new surrender amount / net fund value at point of surrender)`
- Rounding: 6 decimal places

**Calculated on Surrender Amount:**
```
Surrender charge = surrender amount × surrender charge rate of corresponding policy year
```

---

## 15. Saving Account Interest Calculation

### Account with Yearly Rate, Compound, No Loan:

```
End value = start × (1+i)^{n/365} + Σ top-up_k × (1+i)^{nk/365} + Σ premium_k × (1+i)^{nk/365} + Σ switch-in_k × (1+i)^{nk/365} − Σ partial withdraw_k × (1+i)^{nk/365} − Σ switch-out_k × (1+i)^{nk/365} − Σ charge deduction_k × (1+i)^{nk/365}
```

### Yearly Bonus:
```
Yearly bonus = start_last_year × [(1+i)(1+f)]^{n/365} + Σ amount_in × [(1+i)(1+f)]^{nk/365} − Σ amount_out × [(1+i)(1+f)]^{nk/365} − start_last_year × (1+i)^{n/365} − Σ amount_in × (1+i)^{nk/365} + Σ amount_out × (1+i)^{nk/365}
```

Where i = guaranteed rate, f = bonus rate

---

## 16. Payer/Payee Rules (Summary)

Priority when multiple roles exist: **Assignee > Trustee > Grantee**

| Policy Type | Death/TPD | Hospital | Medical LG MC | PayCare |
|------------|-----------|---------|--------------|---------|
| Ordinary (on LA) | Policyholder | Policyholder | Policyholder | Policyholder |
| Trust Policy | Trustee | Trustee | Trustee | Trustee |
| Absolute Assignment | Absolute Assignee | Policyholder | Life Assured | Absolute Assignee |
| Conditional Assignment | Conditional Assignee | Policyholder | Policyholder | Policyholder |
| Grantee/Collateral | Grantee/Collateral | Policyholder | Policyholder | Policyholder |

**For bankruptcy:** Disbursement Payee defaults to Official Assignee (finance user can override).

---

## 17. Currency Conversion (Real-Time FX)

```
Target currency value = source currency value × exchange rate
```

**Rounding rules:**
- Exchange rate: 8 decimal places
- Fund value to policy currency: 2 decimal places
- Collection/payment amount for fund: 2 decimal places
- No rounding when converting to base currency

**Conversion date:** Prefer validate date; if not available use latest rate up to validate date.

---

## 18. Tolerance

### NB Tolerance
Total inforcing premium > collection ≥ total inforcing premium − tolerance: apply with tolerance

### Renewal Tolerance
Traditional: one installment > collection ≥ installment − tolerance: apply with tolerance

Investment (bucket filling): bucket size > allocated ≥ bucket size − tolerance: generate pending fund transaction

---

## 19. Waiting Period

Rules govern when benefits become payable after policy inception.

---

## 20. Relationship Matrix

Validates rider attachment eligibility (main→rider, rider→rider).

**Rules:**
- When multiple conditions exist: ALL conditions validated
- Attachment allowed only if relationship defined in matrix
- Relationships checked: M1-R1, M1-R2, M1-W1, M1-PBR1 (main to rider), R1-R2 (rider to rider, same LA), R1-W2 (parent to child rider)

---

## 21. Key Formulas Quick Reference

| Topic | Formula |
|-------|---------|
| Cash Bonus | CB = SA/unit × cash bonus factor |
| Interim Bonus | IB = latest RB × adjusted months / 12 |
| Reversionary Bonus | RB = rate × basis / unit rate + compounded bonus |
| Terminal Bonus (by RB) | TB = accumulated RB × TB factor / unit rate |
| Extra Premium ($/SA) | EP = EPR × SA / unit rate × MF |
| Inforce SA (decreasing term) | SA_t = Initial SA − (t × Initial SA / n) |
| Inforce SA (increasing term) | SA_t = (1 + t × 10%) × Initial SA |
| Gross Premium | {[PR − LSD] × SA/unit − SpD × [...] + PF} × MF |
| Mortgage PR interpolation | PR = PRL + (IntA−IntL)/(IntH−IntL) × (PRH−PRL) |
| Surrender Charge (on premium) | Annual prem × rate × adj factor × (surrender/net fund) |
| Saving Account (compound) | End = start × (1+i)^{n/365} + Σ(transactions at their rates) |
| FX Conversion | Target = source × rate |
| APA Interest | Compound; capitalized on due date/withdrawal/change/new deposit |
| Tolerance (NB) | Apply if: inforcing prem > collection ≥ inforcing prem − tolerance |

---

## 22. INVARIANT Declarations

**INVARIANT 1:** Accounting date cannot be in a closed accounting month.
- Enforced at: All financial transactions

**INVARIANT 2:** Total Debits = Total Credits for every GL posting.
- Enforced at: EOD/EOM Posting

**INVARIANT 3:** APA interest accrual ceases the moment policy is no longer inforce.
- Enforced at: APA Interest capitalization

**INVARIANT 4:** Bonus calculation uses bonus effective date = next bonus due date (or −1 year for RB).
- Enforced at: Bonus Calculation

**INVARIANT 5:** Surrender charge adjustment factor uses 6 decimal places rounding.
- Enforced at: Surrender Charge Calculation

---

## 23. Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-ug-nb.md | NB — uses premium calculation rules |
| insuremo-v3-ug-renewal.md | Renewal — uses APA billing rules |
| insuremo-v3-ug-survival-payment.md | Survival benefit — APA offset |
| insuremo-v3-ug-maturity.md | Maturity — APA payout |
| insuremo-v3-ug-loan-deposit.md | Loan — APA message trigger |
| insuremo-v3-ug-fund-admin.md | ILP — uses saving account interest |
| insuremo-v3-ug-posting-gl.md | GL — uses accounting date rules |
| insuremo-v3-ug-bonus.md | Bonus — uses bonus calculation |
