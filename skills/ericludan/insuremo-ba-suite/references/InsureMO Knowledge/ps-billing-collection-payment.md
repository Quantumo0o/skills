# InsureMO Platform Guide — Billing / Collection / Payment
# Source: Billing User Guide + Collection User Guide + Payment User Guide
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"how do Billing, Collection, and Payment modules work in InsureMO"** — navigation paths, prerequisites, field behaviour, workflow config parameters, and business rules.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for a Billing / Collection / Payment-related gap
- Agent 6 is generating a **Config Runbook** for Finance items
- A BA needs to verify what **preconditions** the system enforces before allowing a transaction

---

## Module Overview

```
Finance Modules
│
├── Billing
│   ├── New Business Billing        ← NB premium billing
│   ├── Customer Service Billing    ← CS alteration billing
│   ├── Renew Billing               ← Renewal premium billing (batch-driven)
│   ├── Billing Query               ← Search and view billing records
│   └── Billing Configuration
│       ├── PremiumNoticeDays       ← When to generate premium notice
│       └── PremiumReminderNoticeDays ← When / how many reminder notices
│
├── Collection
│   ├── Manual Collection           ← Counter / ad-hoc premium collection
│   ├── Batch Upload Collection     ← Bulk bank file upload
│   ├── Cancel Collection           ← Reverse / dishonour a collection
│   ├── Transfer and Apply Suspense ← Move monies between suspense accounts
│   └── Collection Query            ← Search and view collection records
│
└── Payment
    ├── Payment Requisition         ← Initiate refund / payout request
    ├── Batch Payment               ← System-driven automated payments
    ├── Payment Authorization       ← Approve / reject payment records
    ├── Change Payment Details      ← Update payee / method / bank
    ├── Manual Payment              ← Physically pay out authorised records
    ├── Cancel Payment              ← Void a payment
    └── Medical Payment Requisition ← Medical billing payout
```

---

## BILLING MODULE

### Billing Overview

Billing generates notices for customers to pay their premium in advance. It is triggered by New Business, Policy Alteration (CS), and Renew Cycle events.

**High-level workflow:**
```
NB / CS / Renew event
  └─► Extract Amount to Bill
        └─► Generate Premium Notice
              └─► Apply Premium + Move Due Date
                    └─► Generate Premium Reminder Notice (if unpaid)
                          └─► Non-Forfeiture Option Disposal (if still unpaid at due + grace)
                                └─► Undo Transaction / Auto Renewal
```

Downstream: Collection → Posting to GL → Manage Letter → Manage Fund Transaction

---

### New Business Billing

**Prerequisites:**
- NB proposal is Accepted or Conditionally Accepted.
- General Suspense is not sufficient for NB Inforce.

**Workflow:**
1. When NB proposal is accepted/conditionally accepted without sufficient suspense, NB billing generated in `Outstanding` state.
2. Once collection comes in and General Suspense is sufficient, system confirms billing and performs NB Inforce.
3. If NB proposal is withdrawn, system cancels the outstanding NB billing.

---

### Customer Service Billing

**Prerequisites:**
- CS application is Accepted or Conditionally Accepted and requires money to Inforce.
- CS Suspense + General Suspense is not sufficient for CS Inforce.

**Workflow:**
1. When CS application accepted/conditionally accepted without sufficient suspense, CS billing generated in `Outstanding` state.
2. Once collection comes in and suspense is sufficient, system confirms billing and performs CS Inforce.
3. If CS application is cancelled, system cancels the outstanding CS billing.

---

### Renew Billing

**Prerequisites:**
- Renew Extraction batch has run and receivables generated.
- Renew Suspense + General Suspense + APA is not sufficient for renew confirmation.

**Workflow:**
1. Renew extraction identifies outstanding premium; if suspense insufficient, renew billing generated in `Outstanding` state.
2. Batch jobs drive the end-to-end process:

| S/N | Process | Batch Reference |
|---|---|---|
| 1 | Extract policies due for renewal; calculate amount to bill | Batch Renew Extraction |
| 2 | Generate premium notices to policyholders | Generate Premium Notice |
| 3 | Apply premium and move due date when payment received | Generate Premium Notice |
| 4 | Send premium reminder notice if unpaid after notice | Generate Premium Reminder Notice |
| 5 | If still unpaid at due date + grace period: normal lapse / APL lapse / Raise APL | Non Forfeiture |

---

### Billing Query

**Navigation:** Billing > Billing Query

**Prerequisites:** NB / CS / Renew Billing has been generated.

**Procedures:**
1. Select Billing > Billing Query.
2. Set search criteria → click **Search**.
3. Click **DETAILS** hyperlink to view policy financial information and account receivable transactions.
4. Click **Credit Card** or **GIRO** hyperlink to view bank transfer detail information.

**Key fields — Search Result:**

| Field | Description |
|---|---|
| Billing Date | Date billing was generated |
| Billing Status | Outstanding / Confirmed / Cancelled / Bank Transferring / Bank Transfer Failed |
| Billing Type | NB / CS / Renew - Due Date |
| Billing No. | Billing reference number |
| Billing To | Policy Holder name |
| Total Billing Amount | NB: total inforce premium; CS: total premium to inforce; Renew: total outstanding premium by due |
| Payment Method | Payment method; Credit Card / GIRO shown as hyperlink for bank transfer details |
| TAT (Days) | Days outstanding since billing generation |

**Note on receivable state:**
- NB / CS: policy receivable generated in `Confirmed` state together with billing confirmation and inforce.
- Renew: policy receivable generated in `Outstanding` state during renew extraction; confirmed together with renew billing confirmation.

---

### Billing Configuration

#### Premium Notice Configuration — `PremiumNoticeDays`

**Navigation:** Rule&Rating > Configuration Table → Table Name = `PremiumNoticeDays`

**Purpose:** Defines whether and when to generate the premium notice, varying by sales channel, payment frequency, and payment method.

**Key parameters:**

| Parameter | Description |
|---|---|
| `product_code` | Product code; `$ALL$` / `$NULL$` / `$OTHER$` supported |
| `sales_channel` | Sales channel; `$ALL$` / `$NULL$` / `$OTHER$` supported |
| `prem_notice_indicator` | Yes / No / `$ALL$` / `$NULL$` / `$OTHER$` |
| `product_category` | Benefit type from `t_benefit_type` |
| `pay_frequency` | Not Relevant / Yearly / Half Yearly / Quarterly / Monthly / Single / Daily / `$ALL$` |
| `pay_mode` | Payment method from `TPayMode`; `$ALL$` / `$NULL$` / `$OTHER$` |
| `leading_days` | X days in advance before premium due date to generate premium notice |

#### Premium Reminder Notice Configuration — `PremiumReminderNoticeDays`

**Navigation:** Rule&Rating > Configuration Table → Table Name = `PremiumReminderNoticeDays`

**Purpose:** Defines whether, how many times, and when to generate each premium reminder notice.

**Key parameters:**

| Parameter | Description |
|---|---|
| `prem_reminder_notice_indicator` | Yes / No / `$ALL$` / `$NULL$` / `$OTHER$` |
| `pay_frequency` | Same options as PremiumNoticeDays |
| `pay_mode` | Payment method from `TPayMode` |
| `product_code` | Product benefit type |
| `sales_channel` | Sales channel |
| `product_category` | Benefit type |
| `seq_id` | Differentiates records with same parameter combination but different overdue_days/sending_times |
| `overdue_days` | Y days after premium due date to generate reminder notice |
| `sending_times` | Number of times to trigger the reminder notice |

---

## COLLECTION MODULE

### Collection Overview

Collections are monies received from customers for business transactions attached to a policy, via various collection methods (cash, cheque, NETS, credit card, bank transfer, DDA, e-banking, etc.).

**High-level workflow:**
```
NB / Alteration / Renew Cycle / Loan & Deposit event
  └─► Manual Collection OR Batch Upload Collection
        ├─► Collection Query
        ├─► Cancel Collection
        └─► Transfer and Apply Suspense to Other Account
              └─► Manage Letter / Posting to GL
```

**Allocation order (CS / Renew / Ad-hoc):**
1. Policy Collection Suspense (premium to inforce CS, overdue interest, stamp duty)
2. APL + APL Interest
3. Renewal Suspense (premium + service tax / GST / stamp duty)
4. General Suspense
5. APA
6. Policy Loan

---

### Manual Collection

**Purpose:** Collect premium online for Traditional, ILP, and A&H policies at counter or ad-hoc.

**Navigation:** Collection > Manual Collection

**Prerequisites:** Proposal or Policy exists.

**Procedures:**
1. Select Collection > Manual Collection.
2. Set search criteria → click **Search** → click target policy hyperlink.
3. In **Receive Collection** area: enter Collection Amount, select Collection Currency (FOREX Rate auto-displayed), enter Collection Method, set Bank Code / Cheque No. / Bank Account / Cheque Due Date / Collection Date / Remarks as required. Click **Add** for multiple collection records.
4. Click **Allocate** → total collected displayed → click **Submit**.
   - If collected premium sufficient: policy inforced / CS inforced / renew confirmed.
   - If not sufficient: collected money allocated to suspense.

**Business Rules:**
- Collection currency may differ from policy currency; system converts using real-time transaction exchange rate effective on collection date.
  - Formula: `Target currency value = source currency value × exchange rate`
  - Exchange rate can have up to 8 decimals; fund exchange to policy currency and collection/payment amounts rounded to 2 decimals.
  - If no rate found for collection date, system retrieves latest rate up to that date and prompts user to confirm.
  - Two-step conversion required if converting between two foreign currencies.
- Forward dating of collection date is **not allowed**.
- NB collection: if amount not applied to total inforcing premium, placed under General Suspense.
- Existing suspense balance is considered during allocation (e.g. outstanding $100, existing suspense $20 → only $80 allocated to suspense).

---

### Batch Upload Collection

**Purpose:** Upload bank-returned collection files containing multiple collection records.

**Navigation:** Collection > Batch Upload Collection

**Supported bank/method combinations:**

| Bank Code | Collection Method |
|---|---|
| HSBC | AXS |
| HSBC | Internet Banking |
| HSBC | Pay Now |
| HSBC | SAM |
| HSBC | Bill Payment |
| DBS | Internet Banking |
| DBS | Bill Payment |

**Prerequisites:**
- Policy status is Accepted or Inforced.
- Returned file prepared in defined format.

**Procedures:**
1. Select Collection > Batch Upload Collection.
2. Select Bank Code → select Collection Method → click **File Location** to select file → click **Submit**.
3. Check job status: click **Query Job Status** → User Job Monitor → confirm `Execute Success`.

**Business Rules:**
- If Policy No. exists: system generates collection record and continues business transaction (policy issue, renew confirmation, loan repayment, CS inforce, premium allocation, etc.).
- If Policy No. does not exist: collection placed in unmatched pool; auto-mapped when matched proposal arrives at NB Registration, Data Entry, NB Verification, or E-submission.
- Bank account configuration: Finance > Bank > Maintain Bank Account.

---

### Cancel Collection

**Purpose:** Cancel collections online for all collection methods including dishonoured cheques.

**Navigation:** Collection > Cancel Collection

**Prerequisites:** Policy has collection records.

**Procedures:**
1. Select Collection > Cancel Collection.
2. Set search criteria → click **Search**.
3. Select checkbox next to desired collection records → specify Cancel Reason → click **Submit** → confirm pop-up.

**Business Rules:**
- Selecting **Others** as Cancel Reason opens a free-text field.
- For **non-applied** collection: can cancel directly.
- For collection applied to **NB Inforce**: must perform NB reversal first, then cancel collection.
- For collection applied to **CS alteration**: must perform CS reversal first, then cancel collection.
- For collection applied to **renew**:
  - If subsequent transaction exists after renew confirmation: must reverse all subsequent transactions including renew manually, then cancel.
  - If no subsequent transaction: system prompts confirmation; if user proceeds, system auto-reverses renew confirmation then cancels collection.

---

### Transfer and Apply Suspense to Other Account

**Purpose:** Transfer monies between suspense accounts (General, Renewal, CS Suspense) and to/from APA, Policy Loan, APL.

**Navigation:** Collection > Transfer and Apply Suspense to Other Account

**Prerequisites:**
- Policy has suspense balance.
- Policy is Inforced.

**Note:** NB proposals do not have APA, Policy Loan, or APL; NB proposals not handled under this function.

**Procedures:**
1. Select Collection > Transfer and Apply Suspense to Other Account.
2. Set search criteria → click **Search** → click target policy hyperlink.
3. In **Transfer** area: pick Transfer Effective Date (default = system date) → enter amount in **Bal Trf fm** (source) → enter amounts in **Bal Trf to** (target; sum must equal Bal Trf fm) → click **Submit**.

**Business Rules:**
- Transfer always from **one** source account to **one or many** target accounts (not many-to-many).
- If there is a lock on refund from General Suspense, monies cannot be moved from General Suspense to other suspense types (e.g. Policy Collection, Renewal Suspense).
- If monies transferred to Renewal Suspense, system attempts to move due date online via Renewal Batch job.
- For interest-bearing accounts (APA, APL, Policy Loan): interest calculated up to system date and displayed as a total figure with principal.

---

### Collection Query

**Navigation:** Collection > Collection Query

**Prerequisites:** Policy has collection records.

**Procedures:**
1. Select Collection > Collection Query.
2. Set search criteria → click **Search**.

---

## PAYMENT MODULE

### Payment Overview

Payment is the insurer refunding to the payee for business transactions (surrender, suspense balance, medical billing, etc.) via various disbursement methods. Payees include policyholder, assignee, beneficiary, clinic, bank, government, etc.

**High-level workflow:**
```
NB / CS / Loan / Survival / Maturity / Annuity / Claim event
  └─► Payment Requisition OR Batch Payment
        └─► Payment Authorization (if amount > authority limit, or batch payment)
              └─► Change Payment Details (optional)
                    └─► Manual Payment
                          └─► Cancel Payment (if needed)
                                └─► Posting to GL
```

---

### Payment Requisition

**Purpose:** Initiate a refund request when a payment record is generated upstream. Supports policy payment, suspense refund, and other account payments.

**Navigation:** Payment > Payment Requisition

**Prerequisites:** Upstream NB, CS, or Claims payment items processed; relevant payment records generated.

**Procedures:**
1. Select Payment > Payment Requisition.
2. Search by Policy No. or Proposal No. → click **Search**.
3. In **Payment Records** section: select payment record(s).
4. In **Disbursement Information** section:
   - **Payee Information**: keep default payee or change to existing/new customer.
   - **Disbursement Method**: enter Amount in Policy Currency, select Payment Method and Currency; FOREX Rate retrieved automatically.
   - Alternatively: select Internal Transfer to redirect payment to another policy/proposal.
5. Click **Submit**. System checks against authority limit:
   - If exceeds limit → goes to **Payment Authorization**.
   - If within limit → goes directly to **Manual Payment** (fee status = `Waiting for Processing`).

**Business Rules:**
- Transaction Payables types: Policy Payment, Surrender, Loan, Maturity, Annuity.
- Suspense / Deposit Account types: Renewal Suspense, CS Suspense, General Suspense, APA, Cash Bonus (CB), Survival Benefit (SB).
- Multiple payment records selected must belong to the **same** disbursement payee.
- Total payment amount of selected records must be **greater than zero**.
- If target policy of internal transfer has a different policyholder, system prompts a reminder (user can proceed).
- Total disbursement method amounts must equal total payment amount shown in Policy Basic Information.
- Internal transfer amount is **excluded** from authority limit validation (only payout amount is validated).
- Payment transferred to another policy goes to Posting to GL process.

#### Payment Requisition Limit Configuration

**Navigation:** Finance > Authority Configuration → Authority Type = `Payment Requisition Limit`

**Default roles and limits:**

| Role | Max Amount |
|---|---|
| D_CSD_PAY_AUTH_L10 | 0.00 |
| D_CSD_PAY_AUTH_L20 | 5,000.00 |
| D_CSD_PAY_AUTH_L30 | 10,000.00 |
| D_CSD_PAY_AUTH_L40 | 20,000.00 |
| D_CSD_PAY_AUTH_L50 | 30,000.00 |
| D_CSD_PAY_AUTH_L60 | 50,000.00 |
| D_CSD_PAY_AUTH_L70 | 75,000.00 |
| D_CSD_PAY_AUTH_L80 | 100,000.00 |
| D_CSD_PAY_AUTH_L90 | 125,000.00 |
| D_CSD_PAY_AUTH_L100 | 150,000.00 |
| D_CSD_PAY_AUTH_L110 | 200,000.00 |
| D_CSD_PAY_AUTH_L120 | 250,000.00 |
| D_CSD_PAY_AUTH_L130 | 500,000.00 |
| D_CSD_PAY_AUTH_L140 | 99,999,999.00 |

**Note:** The organisation set in the role refers to the **user's** organisation, not the policy's.

---

### Batch Payment

**Purpose:** System automatically performs payments for maturity, cash bonus, loan, auto refund of suspense, claim, and annuity via scheduled batch jobs.

**Prerequisites:**
- Batch payment process based on CS rules completed.
- Payment records with Fee Type 32 generated in `Temporary` fee status.
- Only Fee Type 32, Fee Status 0 (Waiting for Processing) eligible for payout.

**Workflow:**
1. System extracts list of policies for which batch payments are due.
2. System updates CB/SB account balance and payment information.
3. Batch payment records transferred to Payment Authorization process.

**Triggered by:** Allocate Survival Benefit, Allocate Cash Bonus, Auto Refund Suspense, Perform Maturity, Perform Annuity, Claim Case Approve.

---

### Payment Authorization

**Purpose:** Approve or reject payment records that exceed authority limits (from Payment Requisition) or all batch payment records.

**Navigation:** Payment > Payment Authorization

**Prerequisites:** Payment generated in `Waiting for Authorization` (Temporary Fee Status) state.

**Procedures:**
1. Select Payment > Payment Authorization.
2. Set search criteria → click **Search**.
3. Select payment records → set Approval Decision to **Authorize** or **Reject** (select Reject Reason if rejecting) → click **Submit**.
   - Authorized → payment record ready for Manual Payment.
   - Rejected → payment record status changed to `Cancelled`.

**Business Rules:**
- If payment amount exceeds your authorization limit: view only; cannot authorize or reject.
- For claim payment: configurable whether to bypass Payment Authorization.
- On successful authorization: authorization info saved; system checks disbursement method → proceeds to Manual Payment.

---

### Change Payment Details

**Purpose:** Update disbursement payee, payment method, or payment bank for a payment that has not yet been paid.

**Navigation:** Payment > Change Payment Details

**Prerequisites:** Payment has been generated or authorized.

**Procedures:**
1. Select Payment > Change Payment Details.
2. Select Change Type (Change Disbursement Payee / Change Payment Bank Account / Change Disbursement Method) → set search criteria → click **Search**.
3. Select payment record → click Policy No. hyperlink.
   - **Change bank account**: select new Bank Account No. → **Submit**.
   - **Change payment method**: select new Disbursement Method, fill in additional info → **Submit**.
   - **Change disbursement payee**: click **Change Payee** → search or create customer → **Submit**.

---

### Manual Payment

**Purpose:** Complete the physical payout of an authorized payment record.

**Navigation:** Payment > Manual Payment

**Prerequisites:**
- Payment record is authorized, OR
- Payment Requisition was performed by user with sufficient authority to bypass authorization.

**Procedures:**
1. Select Payment > Manual Payment.
2. Set search criteria → click **Search**.
3. Select payment record → enter Payment Reference No. and Comment → click **Submit**.
4. Perform Posting to GL.

---

### Cancel Payment

**Purpose:** Void a payment after authorization for reasons such as spoilt cheque, payment details change, or void payment requisition.

**Navigation:** Payment > Cancel Payment

**Prerequisites:** Payment records to be cancelled exist in system.

**Procedures:**
1. Select Payment > Cancel Payment.
2. Set search criteria → click **Search**.
3. Select payment records → select Cancel Reason → click **Submit**.
   - If cancelling a confirmed payment: pop-up warns that payment has been clawed back; click **Continue** to proceed.
4. Cancelled payment can be re-processed via Payment Requisition.

---

### Medical Payment Requisition

**Purpose:** Process payout for medical billing records.

**Navigation:** Payment > Medical Payment Requisition

**Prerequisites:** Medical Billing has been created.

**Procedures:**
1. Select Payment > Medical Payment Requisition.
2. Set search criteria → click **Search**.
3. Select payment records → click **Submit**.

---

## Billing Status Reference

| Billing Status | When Set |
|---|---|
| Outstanding | NB Accepted/Conditional Accept; CS Approved; Renew Extraction |
| Confirmed | NB Inforce; CS Inforce; Renew Confirmed |
| Cancelled | Undo CS; Undo Renew |
| Bank Transferring | Bank transfer in progress |
| Bank Transfer Failed | Bank transfer deduction failed |

---

## Payment Status Reference

| Fee Status | Meaning |
|---|---|
| Temporary Fee Status | Payment amount > authority limit; pending Payment Authorization |
| Waiting for Processing | Payment within authority limit; ready for Manual Payment |
| Confirmed | Payment completed |
| Cancelled / Expiry | Payment cancelled or expired |

---

## Config Gaps Commonly Encountered

| Scenario | Gap Type | Config Location |
|---|---|---|
| Premium notice lead days by channel / frequency / method | Config Gap | Rule&Rating > Configuration Table > `PremiumNoticeDays` |
| Reminder notice frequency and timing | Config Gap | Rule&Rating > Configuration Table > `PremiumReminderNoticeDays` |
| Payment requisition authority limits per role | Config Gap | Finance > Authority Configuration > Payment Requisition Limit |
| Claim payment bypass authorization flag | Config Gap | Claim configuration → bypass payment authorization |
| Cash bank account by branch / role | Config Gap | Finance > Bank > Maintain Bank Account |
| Batch upload collection bank code / method mapping | Config Gap | Finance > Bank > Maintain Bank Account |

---

## Billing Rules (from Finance UG)

### Billing Cycle
| Event | System Action |
|---|---|
| NB Inforce | First premium due date set |
| Renewal | Renewal premium due date = policy anniversary |
| Grace Period Start | Day after due date |
| Grace Period End | 30/31 days (product config) |
| Lapse Trigger | After grace period if unpaid |

### GIRO Collection
| Stage | Action |
|---|---|
| GIRO Setup | Bank account + authorization captured |
| GIRO Attempt 1 | Due date |
| GIRO Attempt 2 | Due date + 7 days |
| GIRO Failed | Policy enters grace period / lapse workflow |
| GIRO Reversal | On policy lapse/cancellation |


## ⚠️ Limitations & Unsupported Scenarios

> This section documents known limitations and scenarios NOT supported by the system. Updated: 2026-03-14

### Payment Methods

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| In-kind Premium Payment | Not supported | Code | Cannot use securities/funds/assets as premium |
| Wire Transfer (TT) | Limited support | Config | May require customization |
| Credit Card Limits | Low limits typically | Config | High premium payments may exceed limits |
| Crypto Currency | Not supported | Code | Digital currency payments not available |

### Collection

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Direct Debit | Limited to GIRO | Config | Other direct debit methods need development |
| Premium Collection (Single) | Cheque/Cash only typically | Config | Check with implementation |
| Collection Scheduling | Fixed schedules | Config | Flexible scheduling needs customization |

### Currency & Exchange

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Dynamic Currency Conversion | Not supported | Code | DCC requires development |
| Real-time FX Rate | Batch update only | Config | Real-time rates need integration |
| Multi-Currency Settlement | Limited | Config | Check with finance team |

---

## Related Files

| File | Purpose |
|---|---|
| `ps-customer-service.md` | CS module guide (alteration items, workflow) |
| `insuremo-investment.md` | Investment module guide (fund price, exchange rate) |
| `ps-product-factory.md` | Product Factory config for product-level rules |
| `insuremo-ootb-full.md` | OOTB capability classification (use for Gap Analysis) |
| `output-templates.md` | BSD output templates for Finance-related gaps |