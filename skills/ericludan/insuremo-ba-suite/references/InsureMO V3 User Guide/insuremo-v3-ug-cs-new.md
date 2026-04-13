# InsureMO Platform Guide  --  Customer Service (CS)  --  New Business / Alteration
# Source: Customer Service User Manual, LifeSystem 3.8.1
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# This file covers the full CS User Guide PDF including Appendix Rules (pages 116 - 239 of the original PDF).
# Do NOT use for Gap Analysis  --  use insuremo-ootb.md instead
# Version: 2.0 | Updated: 2026-03-27

---

## 1. Purpose of This File

Answers: What CS alteration types are supported, what are their prerequisites, workflow steps, and business rules?
When to use: Agent 2 (BSD configuration), Agent 6 (config runbook), BA verification of CS module rules.

---

## 2. Module Overview

```
Customer Service (CS) Module
│
├── CS Flow (with formal registration  ->  entry  ->  UW  ->  approval  ->  inforce)
│   ├── Customer Service Registration
│   ├── Customer Service Entry
│   │   ├── Traditional Alterations (30+ types)
│   │   │   ├── Add Rider
│   │   │   ├── APL Reinstatement
│   │   │   ├── Cancellation
│   │   │   ├── Change Assignment
│   │   │   ├── Change Beneficiary
│   │   │   ├── Change Benefits
│   │   │   ├── Change Birth Date or Gender
│   │   │   ├── Change Commencement Date
│   │   │   ├── Change Discount Type
│   │   │   ├── Change Extra Premium
│   │   │   ├── Change Indexation Information
│   │   │   ├── Change Occupation
│   │   │   ├── Change Payer
│   │   │   ├── Change Payment Frequency
│   │   │   ├── Change Payment Method
│   │   │   ├── Change Policy Basic Information
│   │   │   ├── Change Policyholder
│   │   │   ├── Change Preferred Life Indicator
│   │   │   ├── Change Smoker Status
│   │   │   ├── Change Survival Benefit or Cash Bonus Option
│   │   │   ├── Change Term
│   │   │   ├── Change Trustee
│   │   │   ├── Decrease SA
│   │   │   ├── Freelook
│   │   │   ├── Increase SA
│   │   │   ├── Input Additional Health Disclosure
│   │   │   ├── Normal Revival
│   │   │   ├── Partial Surrender
│   │   │   ├── Perform ETA
│   │   │   ├── Perform Reduced Paid-up
│   │   │   ├── Reinstatement (Special Revival)
│   │   │   ├── Reversionary Bonus Surrender
│   │   │   └── Surrender
│   │   └── ILP Alterations
│   │       ├── ILP Ad-hoc Single Premium Top-up
│   │       ├── ILP Change Investment Regular Premium
│   │       ├── ILP Change Investment Strategy
│   │       ├── ILP Change Regular Premium Apportionment
│   │       ├── ILP Decrease Sum Assured
│   │       ├── ILP Delete Rider
│   │       ├── ILP Freelook
│   │       ├── ILP Full Surrender
│   │       ├── ILP Include Unit Deduction Rider
│   │       ├── ILP Increase Sum Assured
│   │       ├── ILP Partial Withdraw
│   │       ├── ILP Reinstatement
│   │       ├── ILP Set or Change Recurring Top-up
│   │       └── ILP Switch Fund Ad Hoc
│   ├── Customer Service Underwriting
│   ├── Underwriting Decision Disposal
│   ├── Customer Service Approval
│   └── Customer Service Inforce
│
├── Batch CS Operations
│   ├── Auto Switch ILP Strategy Batch
│   ├── Process Vesting Batch Job
│   ├── Regular Withdraw Batch
│   ├── ILP Policy Lapse Batch
│   ├── Batch Application Cancellation
│   └── Batch Customer Service (various)
│
├── Without CS Flow (Ad-hoc Services)
│   ├── Change Coupon Disposal Option
│   ├── Change Health Warranty Date
│   ├── Set or Change Regular Withdraw Plan
│   ├── Reverse Alteration
│   ├── Modify Manual Surrender Value Indicator
│   ├── Cancel or Reset Vesting
│   └── Reprint Policy Documents
│
├── Advanced Adjustment
│   ├── Manual Adjust Policy Information
│   └── Manual Adjust Financial Data
│
└── Application Management
    ├── Reject a Customer Service Application
    └── Cancel a Customer Service Application
```

---

## 3. Workflow  --  Standard Sequence

### CS Flow (with full workflow)

```
[1] Customer Service Registration
      │ (register application + alteration items)
      ▼
[2] Customer Service Entry
      │ (enter alteration details per item)
      │  ┌─────────────────────────────────────┐
      │  │ ILP/Special items may require UW   │
      ▼  └─────────────────────────────────────┘
[3] Customer Service Underwriting (if required)
      │ (manual review + decision)
      ▼
[4] Underwriting Decision Disposal
      │ (accept/reject/adjust items)
      ▼
[5] Customer Service Approval
      │ (approve alteration items)
      ▼
[6] Customer Service Inforce
      │ (collection complete  ->  alteration effective)
      ▼
[7] Reverse Alteration (if needed, post-inforce)
```

### Optional / Parallel Steps
- **Batch Application Cancellation**: daily auto-cancel of expired applications
- **Batch Customer Service**: Auto Switch ILP Strategy, Process Vesting, Regular Withdraw, ILP Policy Lapse

### Without CS Flow (Ad-hoc)
```
Search Policy  ->  Select Ad-hoc Service  ->  Enter Details  ->  Submit (no registration/approval)
```

---

## 4. Menu Navigation Table

| Action | Path |
|---|---|
| CS Registration | Customer Service > Customer Service Registration |
| CS Entry | Customer Service > Customer Service Entry |
| CS Underwriting | Customer Service > Customer Service Underwriting |
| CS Underwriting Confirmation | Customer Service > Customer Service Underwriting Confirmation |
| CS Approval | Customer Service > Customer Service Approval |
| CS Inforce | Customer Service > Customer Service Inforce |
| CS Cancellation | Customer Service > Customer Service Cancellation |
| Change Coupon Disposal Option | Customer Service > Ad hoc Service > Change Coupon Disposal Option |
| Change Health Warranty Date | Customer Service > Ad hoc Service > Change Health Warranty Date |
| Set/Change Regular Withdraw Plan | Customer Service > Ad hoc Service > Set or Change Regular Withdraw Plan |
| Reverse Alteration | Customer Service > Ad hoc Service > Reverse Alteration |
| Modify Manual SV Indicator | Customer Service > Ad hoc Service > Modify Manual Surrender Value Indicator |
| Cancel or Reset Vesting | Customer Service > Ad hoc Service > Cancel or Reset Vesting |
| Reprint Policy | Customer Service > Ad hoc Service > Reprint Policy |
| Manual Adjust Policy Info | Customer Service > Advanced Adjustment > Manual Adjust Policy Information |
| Manual Adjust Financial Data | Customer Service > Advanced Adjustment > Manual Adjust Financial Data |
| Config: Maintain Service Rule | Configuration Center > Customer Service Configuration > Maintain Service Rule |

---

## 5. Status Reference Table

| Status | When Set |
|---|---|
| `Pending Data Entry` | Application registered but entry not started |
| `Processing in Progress` | CS entry in progress |
| `Pending Requirement` | Additional information requested (pending letter sent) |
| `Underwriting in Process` | Sent to underwriting sharing pool |
| `Underwriting Completed` | UW decision made |
| `Disposing Underwriting Decision` | Decision being processed |
| `Pending Follow Up` | Awaiting client response |
| `Pending Approve` | Ready for approval |
| `Approving` | Approval in progress |
| `Approved` | All items approved, awaiting collection |
| `Inforce` | Alteration effective (collection complete or no collection needed) |
| `Cancelled` | Application rejected or cancelled |
| `Expired` | Batch cancellation (health warranty date + 7 days passed, or UW date + 30 days with pending reason) |

---

## 6. Per-Process Sections

### Part 1  --  Customer Service Registration

#### Prerequisites
- Policy is already issued

#### Navigation
`Customer Service > Customer Service Registration`

#### Steps
1. From main menu, select `Customer Service > Customer Service Registration`
2. Enter policy number, received branch, touch point (e.g., E-mail); enter application content if necessary
3. In `Policy Alterations Item` section: select item from left list  ->  click `Add` to add to right list
4. Click `Register`
   - System prompts: "New application is registered successfully"
   - Click `Exit` or `Application Entry` to proceed

#### Rules for Customer Service Registration
- Only policies whose organizations you have access to can be searched
- Multiple alteration items can be registered in a single application

---

### Part 2  --  Customer Service Entry

#### Prerequisites
- Application registered successfully
- Application status: `Pending Data Entry`, `Processing in Progress`, or `Pending Requirement`
- Policy is not frozen by other CS application

#### Navigation
`Customer Service > Customer Service Entry`

#### Steps (General)
1. Retrieve application: from main menu, select `Customer Service > Customer Service Entry`; enter search criteria  ->  click Search
2. Click application ID to open Application Entry page
3. Update basic information if necessary
4. Add/delete/enter alteration items:
   - Add: select from `Policy Alteration Item` dropdown  ->  click `Add`
   - Delete: select record  ->  click `Delete`
   - Enter: select alteration item  ->  click `Enter Information`
5. Enter application details on corresponding alteration page  ->  click `Submit`
6. In `Application Entry Comments`: select `Generate Endorsement` (`Yes` or `No`)
7. Click `Submit`
   - System prompts: "Do you want to underwrite this application?"
   - Click `OK`  ->  sent to underwriting sharing pool (if manual UW required)
   - Click `Cancel`  ->  no manual UW needed

#### Per-Alteration-Type Entry Procedures

---

##### Add a Rider

**Prerequisites:**
- Policy is NOT a CPF policy (`CPF indicator = No`)
- Policy status = `Inforce`
- For ILP: no `Potential Lapse Date` or `Projected Lapse Date`
- Main product premium status  !=  `Premium Waived`

**Steps:**
1. Select `Add Rider`  ->  click `Enter`
2. Enter `Validity Date`
3. Select a benefit for adding rider; select effective date type:
   - `Add Rider from Commencement Date`
   - `Add Rider from Last Due Date`
   - `Add Rider from Last Anniversary Date`
   - `Add Rider Immediately`
   - `Add Rider from Next Due Date`
   - `Add Rider from Next Anniversary Date`
4. On `Benefit Information Entry` page: select rider, enter details (similar to NB data entry)
5. Click `Submit`; new rider appears in `Benefit Information after Change`
6. Optionally add waiver or delete rider
7. Click `Submit`

##### APL Reinstatement

**Prerequisites:**
- Policy status = `Lapsed` and lapse reason = `APL Lapse`
- Reinstatement within period defined in product after lapse date

**Steps:**
1. Select `Reinstatement`  ->  click `Enter`
2. Enter `Validity Date`
3. In `Benefit Information before Change`: click `Min Amount Revival` or `Full Amount Revival`
4. View/modify non-waiver benefit by clicking benefit ID

##### Cancellation

**Prerequisites:**
- Policy status  !=  `Terminate`
- Policy is NOT investment linked

**Steps:**
1. Select `Cancellation`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit; select effective date type (`Cancel from Commencement Date`, `Cancel Immediately`, `Cancel from Next Due Date`, `Cancel from Lapse Date`)
4. Select cancellation reason from dropdown; if `Cancel from Lapse Date`  ->  enter `Lapse Date`
5. View/modify refund amount in `Modify Collection/Refund`; click `Submit`

##### Change Assignment

**Prerequisites:**
- Policy does NOT have any trustee
- Policy status  !=  `Terminated`
- Policy does NOT have any beneficiary
- Policyholder (assignor) should NOT be bankrupt
- In product table: `Allow Assignment indicator = Yes` for main plan

**Steps:**
1. Select `Change Assignment`  ->  click `Enter`
2. Enter `Validity Date`
3. To change assignment type: click `Change Assignment Type`  ->  select type (`Absolute Assignment` or `Collateral Assignment`)
4. To add assignee: click `Add Assignee`  ->  search/create party  ->  enter correspondence address  ->  click `Submit`
5. To delete assignee: select record  ->  click `Delete Assignee`  ->  confirm
6. To change assignee info: select record  ->  click `Change Assignee Information`  ->  modify  ->  click `Submit`
7. Click `Submit`

**Assignment Types:**
- **Absolute Assignment**: irrevocable transfer of complete ownership from one party to another
- **Collateral Assignment**: temporary transfer of some ownership rights as collateral for a loan; rights revert upon debt payment

##### Change Beneficiary

**Prerequisites:**
- First policy: must NOT be under assignment
- Third party policy: must be under absolute assignment AND assignee must be life assured of main benefit

**Steps:**
1. Select `Change Beneficiary`  ->  click `Enter`
2. Enter `Validity Date`
3. To add beneficiary: click `Add Beneficiary`  ->  search/create party  ->  enter relationship, percentage share, address  ->  click `Submit`
4. To delete beneficiary: select record  ->  click `Delete Beneficiary`  ->  confirm
5. To change beneficiary info: select record  ->  click `Change Beneficiary Information`  ->  modify  ->  click `Submit`
6. Click `Submit`

##### Change Benefits

**Prerequisites:**
- Policy status = `Inforce`
- Policy is NOT unit-linked

**Steps:**
1. Select `Change Benefits`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit  ->  click `Change Benefit`
4. Select new benefit, enter details  ->  click `Save`
5. View/modify collection/refund in `Modify Collection/Refund`; click `Submit`

##### Change Birth Date or Gender

**Prerequisites:**
- Policy is NOT an issue-without-premium policy
- Policy is WITHOUT indexation
- Birth date and gender changed at party level in Party module

**Steps:**
1. Select `Change Birth Date or Gender`  ->  click `Enter`
2. Enter `Validity Date`
3. Select life assured  ->  click `Change Birth Date or Gender`
4. View/modify collection/refund; click `Submit`

##### Change Commencement Date

**Prerequisites:**
- Policy status = `Inforce`
- Main benefit premium status  !=  `Premium Waived`
- NOTE: If policy is in first policy year  ->  warning message displayed (can continue)

**Steps:**
1. Select `Change Commencement Date`  ->  click `Enter`
2. Enter `Validity Date`
3. Enter new commencement date  ->  click `Change Commencement Date`
4. View/modify collection/refund; click `Submit`

##### Change Discount Type

**Prerequisites:**
- Policy status  !=  `Terminated`

**Steps:**
1. Select `Change Discount Type`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit  ->  click `Change Premium Discount`
4. Select new discount type  ->  click `Save`
5. Click `Submit`

##### Change Extra Premium

**Steps:**
1. Select `Change Extra Premium`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit; select effective date type (`Change Extra Premium from Commencement Date`, `Change Extra Premium Immediately`, `Change Extra Premium from Next Due Date`)
4. On `Extra Loading` page: modify extra premium  ->  click `Submit`
5. Click `Submit`
6. View/modify collection in `Modify Collection/Refund`; click `Submit`

##### Change Indexation Information

**Prerequisites:**
- Policy is NOT terminated
- Policy is NOT suspended
- At least one benefit has indexation feature

**Steps:**
1. Select `Change Indexation Information`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit with indexation  ->  click `Change Indexation Information`
   - NOTE: If benefit has no indexation type or indexation suspend cause = `Cancelled by UW`  ->  cannot be selected
4. Change indexation type (calculation basis updates automatically)  ->  click `Save`
   - NOTE: Indexation type must be allowed by benefit AND consistent with premium count way
5. Click `Submit`

##### Change Occupation

**Prerequisites:**
- Policy is NOT an issue-without-premium policy

**Steps:**
1. Select `Change Occupation`  ->  click `Enter`
2. Enter `Validity Date`
3. Select life assured  ->  click effective type (`Change Occupation Immediately` or `Change Occupation from Next Due Date`)
4. Change occupation class  ->  click `Save`
5. Click `Submit`
6. If collection/refund: view/modify in `Modify Collection/Refund`  ->  click `Submit`

##### Change Payer

**Prerequisites:**
- Policy is NOT an issue-without-premium policy

**Steps:**
1. Select `Change Payer`  ->  click `Enter`
2. Enter `Validity Date` and `Customer Request Effective Date`
3. Click `New Party Entry`  ->  search/create new premium payer
4. Click `Submit`

##### Change Payment Frequency

**Prerequisites:**
- **Traditional policies**: risk status  !=  `Terminated`; at least one benefit has regular premium (Yearly/Half-yearly/Quarterly/Monthly)
- **ILP policies**: risk status = `Inforce`; no PLD or PJD; at least one benefit has regular premium

**Steps:**
1. Select `Change Payment Frequency`  ->  click `Enter`
2. Enter `Validity Date`
3. Select new payment frequency  ->  click `Change Payment Frequency`
4. Click `Submit`

##### Change Payment Method

**Prerequisites:**
- Payment method cannot be CPF category: `CPF-OA`, `CPF-SA`, `SRS`, `ASPF OA`, `ASPF SA`, `MSS`, `MSPS`

**Steps:**
1. Select `Change Payment Method`  ->  click `Enter`
2. Enter `Validity Date`
3. Select new payment method; enter related information
   - If `Credit Card`: account information section displayed (refer to New Business User Guide A.6)
   - If `Direct Debit`: account information section displayed (refer to New Business User Guide A.6)
4. Click `Submit`

##### Change Policy Basic Information

**Steps:**
1. Select `Change Policy Basic Information`  ->  click `Enter`
2. Enter `Validity Date`
3. Modify basic information (service tax indicator, employee contribution percentage, car registration number, etc.)
4. Click `Submit`

##### Change Policyholder

**Prerequisites:**
- New policyholder must be a person (not an organization)

**Steps:**
1. Select `Change Policyholder`  ->  click `Enter`
2. Enter `Validity Date`
3. Click `New Policyholder Entry`  ->  search/create party  ->  system allocates proposer role automatically
4. Select address record  ->  click `Submit`
5. Click `Submit`

##### Change Preferred Life Indicator

**Steps:**
1. Select `Change Preferred Life Indicator`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit  ->  click effective type
4. Change preferred life indicator  ->  click `Save`
5. Click `Submit`
6. If collection/refund: view/modify in `Modify Collection/Refund`  ->  click `Submit`

##### Change Smoker Status

**Prerequisites:**
- Smoker status changed at party level in Party module

**Steps:**
1. Select `Change Smoker Status`  ->  click `Enter`
2. Enter `Validity Date`
3. Select life assured  ->  click effective type (`Change Smoker Status from Commencement Date` or `Change Smoker Status Immediately`)
4. Click `Submit`
5. If collection/refund: view/modify  ->  click `Submit`

##### Change Survival Benefit or Cash Bonus Option

**Prerequisites:**
- Policy status = `Inforce`, `Lapse`, or `Terminated` (for terminated: cash bonus amount must be > 0)
- Benefits have survival benefit or cash bonus feature per product

**Steps:**
1. Select `Change Survival Benefit or Cash Bonus`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit  ->  select new option  ->  select disbursement method  ->  enter related info
4. Click `Submit`

##### Change Term

**Prerequisites:**
- Policy status = `Inforce` or `Lapse`
- For ILP: no `Potential Lapse Date` or `Projected Lapse Date`

**Steps:**
1. Select `Change Term`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit  ->  click `Change Term`
4. Change terms of benefit  ->  click `Save`
5. Click `Submit`
6. If collection/refund: view/modify  ->  click `Submit`
   - NOTE: For Mortgage Decreasing Term (MDT): coverage term, premium term, interest rate, and remaining SA can also be changed

##### Change Trustee

**Prerequisites:**
- Policy is NOT assigned
- Policy is NOT a third-party policy
- Policy status  !=  `Terminated`
- Policy is under trust
- NOTE: If policy status = `Lapse`  ->  warning message (can continue)

**Steps:**
1. Select `Change Trustee`  ->  click `Enter`
2. Enter `Validity Date`
3. To add trustee: click `Add Trustee`  ->  search/create party  ->  select address  ->  click `Submit`
4. To delete trustee: select record  ->  click `Delete Trustee`  ->  confirm
5. To change trustee info: select record  ->  click `Change Trustee Information`  ->  modify  ->  click `Submit`
6. Click `Submit`

##### Decrease SA

**Prerequisites:**
- Policy status = `Inforce` or `Lapse`
- For ILP: no `Potential Lapse Date` or `Projected Lapse Date`

**Steps:**
1. Select `Decrease SA`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit; select effective date type (`Decrease SA from Commencement Date`, `Decrease SA Immediately`, `Decrease SA from Next Due Date`)
4. Enter new SA  ->  click `Save`
5. Click `Submit`
6. View/modify refund in `Modify Collection/Refund`  ->  click `Submit`

##### Freelook

**Prerequisites:**
- Policy status  !=  `Terminated`
- Main benefit allows freelook per product

**Steps:**
1. Select `Freelook`  ->  click `Enter Information`
2. Enter `Validity Date`
3. Select benefit and freelook reason  ->  click `Freelook`
4. Select medical fee collection type  ->  click `Submit`
5. View/modify refund in `Modify Collection/Refund`  ->  click `Submit`
   - NOTE: If policy status = `Lapse`  ->  warning message (can continue)

##### Increase SA

**Steps:**
1. Select `Increase SA`  ->  click `Enter Information`
2. Enter `Validity Date`
3. Select benefit; select effective date type (`Increase SA from Commencement Date`, `Increase SA Immediately`, `Increase SA from Next Due Date`)
4. Enter new SA  ->  click `Save`
5. Click `Submit`
   - NOTE: If beyond first policy year  ->  warning message (can continue); benefit should NOT be unit-linked

##### Input Additional Health Disclosure

**Prerequisites:**
- Policy status = `Inforce` or `Lapse`

**Steps:**
1. Select `Input Additional Health Disclosure`  ->  click `Enter`
2. Enter `Validity Date`
3. Select policyholder or life assured record  ->  click `Increase SA from Commencement Date`
4. Enter additional health disclosure information  ->  click `Submit`

##### Normal Revival

**Prerequisites:**
- Reinstatement within period defined in product after lapse date for main benefit
- Can click `Continue` to proceed

**Steps:**
1. Select `Normal Revival`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefits  ->  click `Normal Revival`
4. View/modify collection in `Modify Collection/Refund`  ->  click `Submit`

##### Partial Surrender

**Steps:**
1. Select `Partial Surrender`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit  ->  click `Partial Surrender`
4. Enter new sum assured  ->  click `Save`
5. Click `Display Net SV Information`  ->  view net SV  ->  click `Submit`
6. View policy admin fees and GSV in `Modify Collection/Refund`  ->  click `Submit`

##### Perform ETA (Extended Term Assurance)

**Prerequisites:**
- Payment method NOT under CPF category
- Main benefit allows ETA per product
- Main benefit premium status = `Regular`
- All deposit accounts = 0 (suspense, APA, cash bonus, survival benefit)

**Steps:**
1. Select `Partial Surrender`  ->  click `Enter`
2. Enter `Validity Date`
3. View benefit information  ->  click `ETA`
   - NOTE: Warning displayed if GSV vesting period not met (can continue)

##### Perform Reduced Paid-up

**Prerequisites:**
- Payment method NOT under CPF category
- Main benefit allows reduced paid-up per product
- Main benefit premium status = `Regular`
- All deposit accounts = 0
- Policy has GSV (validity date >=  commencement date + completed GSV vesting years per product)
- WARNING: If GSV vesting period not met  ->  warning (can continue)

**Steps:**
1. Select `Perform Reduced Paid-up`  ->  click `Enter`
2. Enter `Validity Date`
3. Click `Reduce Paid up`
4. Modify SA if necessary  ->  click `Submit`
5. View refund in `Modify Collection/Refund` (if any)  ->  click `Submit`

##### Reversionary Bonus Surrender

**Prerequisites:**
- Policy reversionary bonus > 0

**Steps:**
1. Select `Reversionary Bonus Surrender`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefits; modify RB Surrender Value if necessary  ->  click `Reversionary Bonus Surrender`
4. Click `Display Net SV Information`  ->  view net SV  ->  click `Submit`
5. View RB gross surrender value in `Modify Collection/Refund`  ->  click `Submit`

##### Set or Cancel Premium Holiday

**Prerequisites:**
- Policy is ILP
- No `Potential Lapse Date` or `Projected Lapse Date`
- Product parameter `allow premium holiday = Yes`

**Steps:**
1. Select `Set or Cancel Premium Holiday`  ->  click `Enter`
2. Enter `Validity Date`; set premium holiday status; click `Submit`
   - NOTE: Validity date cannot be a future date (warning if violated)

##### Special Revival

**Prerequisites:**
- Policy status = `Lapse` and lapse reason = `Normal Lapse`
- No special revival previously performed in policy lifetime
- Policy lapsed > 6 months but < 3 years
- Policy enforced >=  6 months prior to lapse
- Main benefit is NOT a term product
- Main benefit is NOT a health product
- In product table: `special revival allowed indicator = Yes` for main plan
- WARNING: If birth date, gender, smoke status, occupation code at party level differ from benefit level  ->  warning (can continue)

**Steps:**
1. Select `Special Revival`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefits  ->  click `Special Revival`
4. View/modify collection in `Modify Collection/Refund`  ->  click `Submit`

##### Surrender

**Steps:**
1. Select `Surrender`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefits; modify GSV of each; select surrender reason  ->  click `Surrender`
4. Click `Display Net SV Information`  ->  view net SV  ->  click `Submit`
5. View policy admin fees and GSV in `Modify Collection/Refund`  ->  click `Submit`

---

### ILP Alteration Entry Procedures

##### ILP Ad-hoc Single Premium Top-up

**Prerequisites:**
- Product allows top-up per product definition
- Policyholder age <=  predefined maximum age for top-up per product

**Steps:**
1. Select `ILP Adhoc Single Premium Top-up`  ->  click `Enter`
2. Enter `Validity Date`
3. In `Main Benefit Information`: click `Top up`
4. On `Top up Information`: view current fund price and value; enter top up amount in policy currency; select top up fund type  ->  click `Add`; enter apportionment; click `Submit`
5. If new funds added with coupon feature: click `Enter Coupon Option`  ->  select coupon disposal type  ->  click `Submit`
6. Click `Submit`
7. If collection/refund: view/modify in `Modify Collection/Refund`  ->  click `Submit`

##### ILP Change Investment Regular Premium

**Prerequisites:**
- Premium status = `Regular`
- WARNING triggers for: policy has miscellaneous debt; policy has PLD or PJD

**Steps:**
1. Select `ILP Change Investment Regular Premium Top-up`  ->  click `Enter Information`
2. Enter `Validity Date`
3. Click `Increase PR from Last Anniversary`, `Increase PR from Next Due`, or `Decrease PR from Next Due`
4. Enter new investment regular premium and MA factor  ->  click `Confirm`
5. Click `Submit`
6. If collection/refund: view/modify in `Modify Collection/Refund`  ->  click `Submit`

##### ILP Change Investment Strategy

**Prerequisites:**
- Main benefit premium status = `Regular`
- Policy is NOT on Premium Holiday

**Steps:**
1. Select `ILP Change Investment Strategy`  ->  click `Enter`
2. Enter `Validity Date`
3. Click `Change Investment Strategy` or `Cancel Investment Strategy`
4. On `Investment Strategy` page:
   - Enter predefined strategy and change horizon (policy calendar year range)
   - OR enter self-defined strategy: enter strategy code; select funds; enter horizon year range and percentage apportionment (total must = 100%)
   - For DCA: if target funds changed  ->  original fund units stay; auto switch batch will transfer from Money Market Fund; if status changed from `Stop by PH` to `Active`  ->  strategy due date adjusted to nearest date after effective date
5. Click `Submit`
6. If new funds with coupon: click `Enter Coupon Option`  ->  select coupon disposal  ->  click `Submit`
7. Click `Submit`

##### ILP Change Regular Premium Apportionment

**Prerequisites:**
- Main benefit premium status = `Regular`
- Product allows change of regular premium apportionment

**Steps:**
1. Select `ILP Change Regular Premium Apportionment`  ->  click `Enter Information`
2. Enter `Validity Date`
3. Click `Change Premium Apportionment`
4. On `Change Premium Apportionment`: add/delete/modify fund apportionment (total must = 100%)  ->  click `Submit`
5. If new funds with coupon: click `Enter Coupon Option`  ->  select coupon disposal  ->  click `Submit`
6. Click `Submit`

##### ILP Decrease Sum Assured

**Steps:**
1. Select `ILP Decrease Sum Assured`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit  ->  click `Decrease SA`
4. Enter new `Initial Sum Assured`  ->  click `Save`
5. Click `Submit`

##### ILP Delete Rider

**Prerequisites:**
- Policy has riders

**Steps:**
1. Select `ILP Delete Rider`  ->  click `Enter`
2. Enter `Validity Date`
3. Select rider; select effective type
4. Select cancellation reason  ->  click `Submit`
5. Deleted rider appears in `Deleted Rider's Information` section
6. Click `Submit`

##### ILP Freelook

**Prerequisites:**
- No pending transactions under policy
- Main benefit allows freelook per product
- WARNING for: policy status = `Lapse`; policyholder is bankrupt

**Steps:**
1. Select `ILP Freelook`  ->  click `Enter Information`
2. Enter `Validity Date`
3. Select freelook reason  ->  click `Freelook`
4. Select medical fee collection type  ->  click `Submit`

##### ILP Full Surrender

**Steps:**
1. Select `ILP Full Surrender`  ->  click `Enter`
2. Enter `Validity Date`
3. Click `Display Fund Information`  ->  view fund info
4. Click `Full Surrender`

##### ILP Include Unit Deduction Rider

**Prerequisites:**
- Policy has riders
- No `Projected` or `Potential Lapse Date`
- No pending fund transactions

**Steps:**
1. Select `ILP Include Unit Deduction Rider`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit  ->  click `Include Unit Deduction Rider`
4. Enter new rider name and benefit details  ->  click `Submit`
   - NOTE: Only products allowed to be attached to main benefit per product definition appear in dropdown

##### ILP Increase Sum Assured

**Prerequisites:**
- No `Projected` or `Potential Lapse Date`
- No pending fund transactions

**Steps:**
1. Select `ILP Increase Sum Assured`  ->  click `Enter`
2. Enter `Validity Date`
3. Select benefit  ->  click `Increase SA`
4. Enter new `Initial Sum Assured`  ->  click `Save`
5. View info; enter admin fee if any  ->  click `Submit`

##### ILP Partial Withdraw

**Prerequisites:**
- Product allows partial withdrawal

**Steps:**
1. Select `ILP Partial Withdraw`  ->  click `Enter`
2. Enter `Validity Date`
3. Select partial withdrawal type:
   - **By units**: click `Partial Withdraw by Units`  ->  enter units
   - **By value**: click `Partial Withdraw by Value`  ->  enter value in fund currency
   - **By total amount**: click `Partial Withdraw by Total Amount`  ->  enter total estimated withdrawal value
4. Click `Submit`

##### ILP Reinstatement

**Prerequisites:**
- Policy status = `Lapsed` and lapse reason = `ILP Lapse`
- Can click `Continue` to proceed

**Steps:**
1. Select `Reinstatement`  ->  click `Enter`
2. Enter `Validity Date`
3. Click `Reinstate the policy with Full Amount` or `Reinstate the policy with Min Amount`
   - Full Amount: system calculates reinstatement collection by minimum amount
   - Min Amount: system calculates by minimum amount
4. Set up collection/refund payment method and payer

##### ILP Set or Change Recurring Top-up

**Prerequisites:**
- Policy status = `Inforce` or `Lapse`
- Main benefit allowed to have recurring top-up
- Product allows partial withdrawal

**Steps:**
1. Select `ILP Set or Change Recurring Top-up`  ->  click `Enter`
2. Enter `Validity Date`
3. Click `Set or Change Recurring Top Up`
4. Enter recurring top-up premium amount; enter start date; select fund in `Add Fund` to add
5. Amend existing recurring top-up plan if necessary
6. Click `Submit`
7. View info; click `Submit`

##### ILP Switch Fund Ad Hoc

**Prerequisites:**
- Product allows fund switch

**Steps:**
1. Select `ILP Switch Fund Ad Hoc`  ->  click `Enter`
2. Enter `Validity Date`
3. Select switch type: `Switch by Value` or `Switch by Units`
4. **By Value**: select `From` fund, `To` fund, enter value in source fund currency  ->  click `Add and Compute`
5. **By Units**: view current fund price; select `From` fund, `To` fund; enter units  ->  click `Add`
6. View switching fee; select payment method  ->  click `Submit`
7. Click `Submit`

---

### Part 3  --  Customer Service Underwriting

#### Prerequisites
- Application entry complete
- Manual underwriting required (configurable via `Configuration Center > Customer Service Configuration > Maintain Service Rule`)

#### Navigation
`Customer Service > Customer Service Underwriting`

#### Steps
1. From main menu, select `Customer Service > Customer Service Underwriting`
2. Enter search criteria  ->  click Search
3. Click policy number
4. Perform underwriting (same procedures as New Business, except: can only provide UW decision and comments; cannot apply Extra Loading, Lien, or Restrict Cover)
5. If query letter required: click `Query Letter`  ->  enter info  ->  click `Print` (generates PDF, status = `Printed`) or `Batch Print` (status = `To be printed`)
6. After UW: proceed to Underwriting Decision Disposal

#### Rules
- CS underwriting entry is different from NB underwriting entry page
- For CS underwriting: underwriter can only provide UW decision and comments; cannot apply Extra Loading/Lien/Restrict Cover

---

### Part 4  --  Underwriting Decision Disposal

#### Prerequisites
- UW decision has been made
- Application status: `Underwriting Completed`, `Disposing Underwriting Decision`, or `Pending Follow Up`
- Application not locked by other user

#### Navigation
`Customer Service > Customer Service Underwriting Confirmation`

#### Steps
1. Search application  ->  click target application ID
2. On `Underwriting Decision Disposal` page: enter health warranty date  ->  click `Display Underwriting Decision`
3. Actions available:
   - Reject application  ->  see Reject a Customer Service Application
   - Cancel application
   - Adjust alteration items: add/delete items; select item  ->  click `Enter Information`; reject item with reason; click `Pending Letter` to generate pending letter (item status  ->  `Pending Requirement`); adjust item info  ->  click `Submit`
   - Query letter: click `Query Letter`  ->  enter info  ->  click `Print` or `Batch Print`
4. In `Application Entry Comments`: view/update comments
5. Click `Submit`

#### Rules for Underwriting Decision Disposal
- If query letter(s) required: generate via `Query Letter`; if `Print`  ->  PDF generated, status = `Printed`; if `Batch Print`  ->  status = `To be printed`; letter status updated to `Replied` after printing and client response
- For financial item (`t_service.is_financial = Y`): all users with approval authority EXCEPT the data entry user can approve

---

### Part 5  --  Customer Service Approval

#### Prerequisites
- CS application data entry finished OR CS application underwriting disposal finished
- Application status: `Pending Approve` or `Approving`
- User has approval operation authority
- For non-financial item: any CS user with approval authority
- For financial item: any CS user with approval authority EXCEPT the data entry user

#### Navigation
`Customer Service > Customer Service Approval`

#### Steps
1. From main menu, select `Customer Service > Customer Service Approval`
2. Enter search criteria  ->  click Search
3. Click destination application ID
4. Select item  ->  click `View Information` to view detailed alteration info
5. Click `Approve`

#### Rules for Customer Service Approval
- In a single application, multiple alteration items can be approved
- Configurable: `Configuration Center > Customer Service Configuration > Maintain Service Rule` controls whether approval is required

---

### Part 6  --  Customer Service Inforce

#### Prerequisites
- Application status = `Approved`
- No outstanding fee to be collected

#### Navigation
`Customer Service > Customer Service Inforce`

#### Steps
1. System updates:
   - `Validate Date`: if collection received after fee records offset  ->  money received date overrides validity date; otherwise validity date remains
   - `Benefit risk commencement date`: updated to latest validity date for Normal Revival items
2. System records alteration commencement date and alteration risk commencement date
3. System regenerates policy documents and endorsement letter
4. System updates application status to `Inforce` and unfreezes policy status
5. System regenerates renewal raw
6. System recalculates mandatory debts and net surrender value

#### Rules for Customer Service Inforce
- Collection/refund must be complete before alteration takes effect
- Health warranty date logic: if health warranty date lapsed before full payment received  ->  application cannot take effect; health warranty date must be changed to allow effect before new date lapses

---

### Part 7  --  Batch Customer Service

#### Auto Switch ILP Strategy Batch

Runs daily (including weekends and public holidays). Selects all policies with anniversary date = run date.

**Investment Strategy Switch  --  Selection Criteria:**

| Strategy Type | Criteria |
|---|---|
| Normal | Strategy Due Date <=  today's date; Policy Status = `In Force`; ILP Policy; not frozen; valid Investment Strategy code; no pending fund transactions |
| DCA (extra) | Strategy effective date < Strategy due date < Strategy end date; Invest amount <=  TIV |

**Investment Strategy Switch  --  Processing:**
1. System creates pending transactions to sell all funds (auto switch) using bid price of anniversary date
2. Strategy Due Date derived from policy anniversary date; updated to next anniversary date

**Investment Strategy Cancellation  --  Selection Criteria:**
- Strategy Due Date <=  today's date
- Policy status = `Lapsed`
- ILP Policy
- Has existing Investment Strategy Code

**Cancellation Processing:**
- Normal strategy: update strategy code with cancelled status
- DCA strategy: set strategy status to `Inactive`
- Regular premium and recurring top-up apportionment NOT nullified

---

#### Process Vesting Batch Job

**Extraction Rules for Prior Vesting Letter** (ALL conditions must be met):
- Policy is `Inforce`
- Policy has vesting schedule (set up at policy inception)
- Vesting schedule status = `Waiting for Effective`
- Prior vesting letter indicator = `N`
- System date >=  Vesting date  -  90 days (vesting date = main benefit's life assured DOB + vesting age)
- Policy is NOT under absolute assignment

**Extraction Rules for Vesting** (ALL conditions must be met):
- Policy must be `Inforce`
- Policy has vesting schedule
- Vesting schedule status = `Waiting for Effective`
- Prior vesting letter indicator = `Y`
- System date >=  Vesting date  -  90 days
- Policy is NOT under absolute assignment

**Updates on Vesting Effective:**
- Vesting schedule status  ->  `Effective`
- Replace policyholder with main benefit's life assured; derive new payer
- Auto-link GIRO account and address of original policyholder to new policyholder
- If new policyholder gender = Male and title = Master  ->  auto-change title to Mr in party module
- Generate vesting letter to new policyholder
- Cancel list of vesting endorsement codes with effective from system date

---

#### Regular Withdraw Batch

**Prerequisites:**
- Policy is `Inforce`
- Policy is un-frozen
- Active regular withdraw plan under policy
- Related funds have no pending fund transactions
- System date >=  regular withdraw due date
- Regular withdraw amount < TIV  -  policy loan  -  Min remaining amount after withdraw (defined at product level)

**Extraction Rules:**
- System extracts policies meeting all conditions above

**Processing:**
- Regular withdraw amount per fund = Total Regular Withdraw Amount  x  (Value of each fund / TIV)
- Exchange rate applied if fund currency  !=  policy currency
- Withdraw charge deducted if applicable

---

#### ILP Policy Lapse Batch

**Prerequisites:**
- Charge deduction batch job has finished
- Policy is `Inforce`
- No credit card, Direct Debit, or CPF collection in transferring
- Main benefit can be lapsed at system date
- Policy has PLD
- No pending fund transaction records

**PLD Calculation:**

| Period | Condition | PLD |
|---|---|---|
| Within non-lapse period | Premium due date >=  system date | PLD not set |
| Within non-lapse period | Premium due date < system date | PLD = premium due date |
| Out of non-lapse period; lapse method = Calculate PLD | System date >=  commencement date + non-lapse period, OR system date < commencement date + non-lapse period but PLD + grace + additional grace >=  system date | PLD = PLD |
| Out of non-lapse period; lapse method = TIV = 0 | PLD + PLD grace period | PLD = PLD + PLD grace period |

**Processing Steps:**
1. Extract qualified policies for lapse
2. For in non-lapse period: Lapse date = PLD + grace period + additional grace period
   For lapse method "calculate PLD": Lapse date = PLD
   For lapse method "TIV=0": Lapse date = PLD + PLD grace period
3. Update policy information:
   - Cancel all future effective transactions
   - Update lapsed date to PLD; cancel PLD and PJD
   - Update policy status, lapse reason, lapse date = same as main benefit
   - If PLD miscellaneous debts exist  ->  create insurer payment to waive PLD miscellaneous debts; update PLD miscellaneous amount to 0
4. Generate Lapsed Letter and Cancel Investment Strategy Letter
5. Generate ILP Last Statement

**Issue Without Premium Policy:**
- After issue-without-premium grace period, if premium not collected  ->  policy lapses
- Lapse date = PLD = commencement date
- Grace period defined in issue-without-premium rate table

---

#### Batch Application Cancellation

Runs daily. Extracts applications meeting cancellation criteria:

| Application Status | Cancellation Condition |
|---|---|
| `Approved`, `Pending Requirement`, or `Pending Follow Up` | Health warranty date (or latest validity date if no HWD) + 7 days < current system date |
| `Underwriting in Process` | Application date + 30 days < current system date AND `Pending Reason` field must not be empty |

**Processing:**
1. Update cancellation reason code = `Expired`; application status  ->  `Cancelled`
2. Unfreeze policy of this application
3. Check if payment/collection offset performed:
   - If yes: undo payment/collection record generation; if offset against suspense  ->  amount goes back to general suspense (cash or CPF accordingly)
   - If no: process ends

---

### Part 8  --  Perform Customer Services without CS Flow

#### Change Coupon Disposal Option

**Prerequisites:**
- Policy status = `Inforce` or `Lapse`
- Policy is investment linked
- Policy has funds with coupon feature

**Navigation:** `Customer Service > Ad hoc Service > Change Coupon Disposal Option`

**Steps:**
1. Enter policy number  ->  click Search
2. View current coupon disposal option
3. Select new option (`Pay Out` or `Reinvest`)  ->  click Submit

---

#### Change Health Warranty Date

**Prerequisites:**
- Application status = `Approved`
- Health Warranty Date must not be blank

**Navigation:** `Customer Service > Ad hoc Service > Change Health Warranty Date`

**Steps:**
1. Enter policy number  ->  click Search
2. Click target policy record
3. Change health warranty date
4. View policy alteration items; enter comments if needed
5. Click Submit

---

#### Set or Change Regular Withdraw Plan

**Prerequisites:**
- Policy status = `Inforce`
- Regular withdraw for main benefit is allowed

**Navigation:** `Customer Service > Ad hoc Service > Set or Change Regular Withdraw Plan`

**Steps:**
1. Enter policy number
2. Set/change basic info in `Regular Withdraw Plan Basic Info`
3. Set/change payee info in `Regular Withdraw Payee Info`:
   - To set/change payee name: click `Name`  ->  search party  ->  submit
   - To set/change account: click `Account`  ->  change existing or add new  ->  apply
4. Select disbursement method (`Cheque` or `Direct Credit`)
5. Click Submit

**Field Reference  --  Regular Withdraw Plan:**

| Field | Description |
|---|---|
| Start Date | Start date of regular withdraw. Format: DD/MM/YYYY |
| End Date | End date of regular withdraw. Format: DD/MM/YYYY |
| Regular Withdraw Frequency | Yearly, Half Yearly, Quarterly, or Monthly |
| Regular Withdraw Status | `Waiting for Processing`, `Processing`, `Cancelled`, or `Terminated` (set to `Terminated` for last withdrawal) |
| Regular Withdraw Option | `By amount` or `By percentage` (if By amount: increment option and amount fields shown; if By percentage: enter percentage) |
| Amount/Percentage | Amount (if By amount) or percentage (if By percentage); increment amount/percentage also configurable |

---

#### Reverse Alteration

**Prerequisites:**
- Application status = `Inforce`
- Policy is not frozen
- For policies with indexation, only specific alteration types can be reversed (see below)

**Reversible Alterations (for indexed policies):**
- Add Rider
- Apply Policy Loan
- Increase/Decrease SA
- Freelook
- Full Surrender
- Change Assignment
- Change Beneficiary
- Change Payer
- Change Occupation
- Change Payment Method
- Change Survival Benefit or Cash Bonus Option
- Change Trustee
- ILP Include Unit Deduction Rider
- ILP Set/Cancel Premium Holiday
- Input Additional Health Disclosure
- Change Policy Basic Information
- Change Policyholder

**Navigation:** `Customer Service > Ad hoc Service > Reverse Alteration`

**Steps:**
1. Enter policy number; select reversal reason  ->  click Search
2. Select alteration to reverse; enter reversal comment  ->  click `Reverse Transaction`
3. System transfers premium from premium income/respective account to New Business suspense account; undoes policy/proposal record based on application
   - NOTE: For issue-without-premium policy, if inforce premium not collected  ->  premium transfer NOT performed
4. Click Exit

#### Modify Manual Surrender Value Indicator

**Prerequisites:**
- Policy status  !=  `Terminate`
- Policy is NOT investment linked

**Navigation:** `Customer Service > Ad hoc Service > Modify Manual Surrender Value Indicator`

**Steps:**
1. Enter policy number  ->  click Search
2. Select target benefit  ->  select `Yes` or `No` from `Manual SV Indicator` dropdown  ->  click Submit
   - NOTE: Only benefits with SV per product definition are displayed

---

#### Cancel or Reset Vesting

**Navigation:** `Customer Service > Ad hoc Service > Cancel or Reset Vesting`

**Steps:**
1. Enter policy number  ->  click Search
2. View policy info and existing vesting info
3. To insert vesting schedule (if none exists): click `Reset Vesting`
4. To cancel vesting: click `Cancel Vesting`
5. To reset after cancel: click `Reset Vesting`

---

#### Reprint Policy Documents

**Prerequisites:**
- Policy status = `Inforce`, `Terminate`, or `Lapse`
- Policy documents have been printed before

**Navigation:** `Customer Service > Ad hoc Service > Reprint Policy`

**Steps:**
1. Enter policy number or proposal number  ->  click Search
2. Select documents and print type; enter re-print fee and reason  ->  click Submit

---

### Part 9  --  Advanced Adjustment

#### Manual Adjust Policy Information

**Prerequisites:**
- Policy is not frozen

**Navigation:** `Customer Service > Advanced Adjustment > Manual Adjust Policy Information`

**Steps:**
1. Enter policy number  ->  click Search
2. View basic policy information
3. Update policy issue date; select origin code from dropdown
4. Select premium calculation method; update standard premium if necessary
5. Enter comments
6. Click Submit

**Field Reference  --  Policy Manual Adjustment:**

| Field | Description |
|---|---|
| Policy Issue Date | Policy issue date. Format: DD/MM/YYYY |
| Origin Code | Source of policy: `New Business`, `Opted Policy`, `Converted Policy`, `Continuation`, `Term Renewal`, `Altered Policy`, `Others`, `Conversion from Deposit  -  New Policy (Bonus Units)`, `Conversion from Deposit  -  Existing Policy`, `From Maturity Proceeds` |
| Premium Method | `Premium calculation based on insured amount`, `Insured amount calculation based on premium`, `Agreed premium` |
| Standard Premium | Standard premium amount |

---

#### Manual Adjust Financial Data

**Prerequisites:**
- Policy is not frozen

**Navigation:** `Customer Service > Advanced Adjustment > Manual Adjust Financial Data`

**Steps:**
1. Enter policy number  ->  click Search
2. Update policy information in `Policy Information Adjustment` area
3. Update benefit information in `Benefit Information Adjustment` area
4. Click Submit

**Adjustable Financial Data:**
- Policy/Benefit risk status
- Monthly-versary due date
- Next due date
- Bonus due date

---

### Part 10  --  Application Management

#### Reject a Customer Service Application

**When:** During application entry or underwriting decision disposal

**Steps:**
1. On `Customer Service Entry` page: click `Reject Application`; OR on `Underwriting Decision Disposal`: enter health warranty date  ->  click `Reject Application`
2. Select rejection code; enter rejection reason  ->  click `Reject Application`
3. Confirm on dialog box  ->  system generates rejection letter

---

#### Cancel a Customer Service Application (Online)

**Prerequisites:**
- Application registered but not yet taken effect

**Navigation:** `Customer Service > Customer Service Cancellation`

**Steps:**
1. Search application
2. Select cancellation reason  ->  click `Application Cancellation`
3. Confirm on dialog box

**Rules for Online Application Cancellation:**
- Cancellation reason must be selected from dropdown

---

## 7. INVARIANT Declarations

**INVARIANT 1: CS application must be registered before any entry can occur**
- Checked at: CS Entry page access
- Effect if violated: Application not found; entry cannot proceed

**INVARIANT 2: Financial CS item approval must be performed by a user different from the data entry user**
- Checked at: CS Approval stage
- Effect if violated: Approval rejected; error message displayed

**INVARIANT 3: ILP partial withdrawal amount must be less than (TIV  -  policy loan  -  min remaining amount)**
- Checked at: ILP Partial Withdraw submission
- Effect if violated: Validation error; withdrawal not processed

**INVARIANT 4: Special Revival can only be performed once per policy lifetime**
- Checked at: Special Revival submission
- Effect if violated: Validation error; special revival rejected

**INVARIANT 5: Change Trustee cannot be performed on an assigned policy**
- Checked at: Change Trustee entry
- Effect if violated: Policy not eligible for trustee change (pre-check displayed)

**INVARIANT 6: Batch Application Cancellation cannot cancel an application that is currently locked by another user**
- Checked at: Batch Application Cancellation processing
- Effect if violated: Application skipped; processed in next batch run

**INVARIANT 7: Premium Holiday validity date cannot be a future date for ILP policies**
- Checked at: Set or Cancel Premium Holiday submission
- Effect if violated: Warning message displayed

**INVARIANT 8: CS application with unpaid collection cannot take effect**
- Checked at: CS Inforce processing
- Effect if violated: Application status remains Approved; alteration not yet effective

---

## 8. Config Gaps Commonly Encountered

| Scenario | Gap Type | Config Location |
|---|---|---|
| Manual underwriting not triggered for specific CS items (config missing) | Config Gap | Configuration Center > Customer Service Configuration > Maintain Service Rule |
| Approval requirement not set for financial CS items | Config Gap | Configuration Center > Customer Service Configuration > Maintain Service Rule |
| ILP Non-lapse Guarantee Period not configured | Config Gap | Product Factory: ILP product parameters |
| `Allow Pending` parameter for ILP incorrectly set | Config Gap | ILP Product Parameters: `Allow Pending` |
| Regular withdraw minimum remaining amount not set per product | Config Gap | Product Factory: ILP product parameters |
| Vesting age schedule not defined for third-party policies | Config Gap | Product Factory: Vesting schedule parameters |
| Issue-without-premium grace period not defined | Config Gap | Issue without premium rate table |
| `BUCKET_FILLING_TOLERANCE_OPTIONS` not configured for ILP bucket filling products | Config Gap | System parameter: `BUCKET_FILLING_TOLERANCE_OPTIONS` |
| Fund switch fee not configured | Config Gap | Product Factory: Fund switch fee per ILP product |
| ILP partial withdrawal fee not configured | Config Gap | Product Factory: ILP product parameters |
| Withdraw charge for regular withdraw not configured | Config Gap | Product Factory: ILP product parameters |
| `special revival allowed indicator` not set for products allowing special revival | Config Gap | Product Factory: Special revival allowed indicator |
| GSV vesting years not defined per product  ->  reduced paid-up calculation incorrect | Config Gap | Product Factory: GSV vesting years per product |
| `Allow Assignment indicator` not set for products allowing assignment | Config Gap | Product Factory: Allow Assignment indicator |
| Auto Switch ILP Strategy batch not scheduled | Config Gap | Batch job scheduler configuration |

---

## 9. Related Files

| File | Purpose |
|---|---|
| `insuremo-ootb.md` | Gap Analysis |
| `ps-new-business.md` | New Business module (NB data entry reference) |
| `ps-billing.md` | Billing/Collection (premium extraction, DDA, GIRO) |
| `ps-product-factory.md` | Product Factory (product parameter configuration) |
| `ps-underwriting.md` | Underwriting module |
| `output-templates.md` | BSD templates |

---

## Appendix: Customer Service Entry Rules

This appendix provides the detailed business rules for each CS alteration type, including submission validation tables, field-level rules, and special handling for ILP policies. Sourced from pages 116 - 239 of the InsureMO V3 User Guide PDF.

---

### Rules for Add Rider

This section tells the rules in add rider.

**1. Selecting a benefit and effective date type:**

| Condition | System Action |
|---|---|
| Benefit status must be Inforce | Enforced |
| Benefit premium status must be Regular | Enforced |
| Selected type of effective date is Add Rider Immediately | Validity date should not exceed the next due date of the selected benefit |
| Selected type is Add Rider from Next Due Date or Add Rider from Next Anniversary Date AND selected benefit has pre-contract payment frequency change | System displays message indicating pre-contract payment frequency change will be cancelled; CS user must redo payment frequency change as separate alteration item |

**2. Adding riders (non-waiver or waiver):**

| Condition | System Action |
|---|---|
| Added rider is an allowed rider in product definition | Enforced |
| Added rider can be attached to the selected benefit | Enforced |
| Added rider must not be a unit deduction rider | Enforced |
| Selected type of effective date is Add Rider from Last Due Date, Add Rider from Next Due Date, or Add Rider Immediately | Rider must be a non-SV benefit as defined by product |
| Added rider must have been launched on or before the rider's commencement date and still selling at the application date | Enforced |
| Selected benefit is regular premium benefit AND added rider is also a regular premium benefit | Rider's payment frequency defaulted to selected benefit's payment frequency and cannot be modified |
| Effective type: Add Rider from Commencement Date, Add Rider Immediately, Add Rider from Last Due Date, or Add Rider from Last Anniversary Date | Rider's current payment frequency defaulted to selected benefit's current payment frequency; next payment frequency defaulted to selected benefit's next payment frequency |
| Other effective types | Rider's current payment frequency and next payment frequency defaulted to selected benefit's next payment frequency; if selected benefit has pre-contract payment frequency change, system cancels the pre-contract change |
| Payment method | Defaulted to selected benefit's payment method; cannot be changed |
| Currency | Defaulted to selected benefit's currency; cannot be changed |
| Commission agents | System allows up to 3; first defaulted to policy's servicing agent (modifiable); corresponding commission ratio defaulted to 100% (not modifiable) |
| Commission agent of added rider must be qualified to sell the rider | Validated using application sign date |
| Fact Find value for health or life product | Must be entered if life fact find indicator or health fact find indicator is required for this product |
| A spouse waiver is added | Only the insured who is the spouse of the policyholder can be selected as life assured for this product |

**3. Submit on Add Rider page:**

| Condition | System Action |
|---|---|
| System calculates policy administrative fee | Administrative fee is configured by CS configuration |
| System keeps old policy details and saves modified policy information | If secondary benefit's risk cessation date is later than primary benefit's risk cessation date, system uses primary benefit's risk cessation date for secondary benefit; if secondary benefit's premium cessation date is later than its risk cessation date, system uses risk cessation date for premium cessation date |
| System displays policy administrative fee and refund/collection if any on Modify Collection/Refund page | CS user can modify administrative fee, stamp duty and fund switch fee if these fees exist |

**4. Relationship between selected benefit and added rider  --  Secondary Benefit Inception and Next Due Date:**

| Secondary Benefit Effective | Secondary Benefit Inception Date | Secondary Benefit Next Due Date |
|---|---|---|
| Add a Rider From Inception | Primary Benefit's Inception Date | Primary Benefit's Next Due Date |
| Add a Rider From Last Anniversary Date | Primary Benefit's Last Anniversary Date | Primary Benefit's Next Due Date |
| Add a Rider From Last Due Date | Primary Benefit's Last Due Date | Primary Benefit's Next Due Date |
| Add a Rider From Next Due Date | Primary Benefit's Next Due Date | Primary Benefit's Next Due Date |
| Add a Rider From Next Anniversary Date | Primary Benefit's Next Anniversary Date | Primary Benefit's Next Anniversary Date |
| Add a Rider Immediately | Validity Date | Primary Benefit's Next Due Date |

| Condition | System Action |
|---|---|
| Secondary benefit inception date does NOT fall on a policy anniversary date | System uses the last policy anniversary date to derive risk and premium cessation date |
| Secondary benefit inception date falls on a policy anniversary date | System uses the benefit inception date to derive risk and premium cessation date |
| Submission date at benefit level | Updated using the application date |

**Table 11: Add Cash Rider  --  ILP Rules**

| Effective Type for New Cash Rider | With Existing Cash Rider | Without Existing Cash Rider |
|---|---|---|
| | New Cash Rider's Inception Date | New Cash Rider's Due Date | New Cash Rider's Inception Date |
| Add Rider from Inception Date | Existing Cash Rider's PDD | Policy Inception Date | Policy Inception Date |
| Add Rider from Last Anniversary Date (regardless of FDD), based on PDD Date | Existing Cash Rider's Last Anniversary Date | Policy Last Anniversary Date | Policy Last Anniversary Date |
| Add Rider from Last Due Date | Existing Cash Rider's Last PDD | Rider's PDD Date based on Validity Date | Policy Last Due Date |
| Add Rider from Next Due Date | Existing Cash Rider's PDD | Rider's PDD (after the new cash rider is effective) | Policy's FDD or Rider's PDD (after the new cash rider is effective) whichever is later |
| Add Rider from Next Anniversary Date (regardless of FDD), based on PDD Date | Existing Cash Rider's Next Anniversary Date | Policy Next Anniversary Date | Policy Next Anniversary Date |
| Add Rider Immediately | Existing Cash Rider's PDD | Validity Date | Validity Date |

**5. Calculates Benefit Collection:**

| Effective Type | Collection Start Date | Collection End Date | Interest up to Validity Date | GST or ST |
|---|---|---|---|---|
| Add a Rider From Inception Date (collect) | Secondary Benefit Due Date | Next = Sum (Interest of each Modal) Premium difference using new rider to calculate | Need to be calculated | Need to be calculated |
| Add a Rider From Last Anniversary Date | None | NA | None | None |
| Add a Rider From Last Due Date | None | NA | None | None |
| Add a Rider From Next Anniversary Date | None | NA | None | None |
| Add a Rider Immediately (collect) | Pro-rated Premium Difference | Secondary Benefit Inception Date | Need to be calculated | Need to be calculated |
| Add a Rider From Next Due Date | None | NA | None | None |

---

### Rules for APL Reinstatement

This section tells the rules in APL reinstatement.

**1. Click Min Amount Revival or Full Amount Revival:**

| Condition | System Action |
|---|---|
| System updates benefits with risk status of Lapse and lapse reason of APL lapse | Set benefit status to In-force; initialize lapse date and lapse reason |
| Minimum revival amount calculation (regular premium policies) | Min Revival Amount = Min(A, B) where A = APL_RD + Overdue TIPs with Interest up to RD; B = (formula per technical spec) |
| Minimum revival amount calculation (SP/premium fully paid-up policies) | Min Revival Amount = Interest on TDebt_LD from LD to [RD + Min(1 Year, CED  -  RD)] |

**Formula Parameters:**

| Parameter | Description |
|---|---|
| LD | Lapse Date |
| RD | Revival Date |
| CED | Cover End Date |
| TDebt_LD | APL Loan Account value at Lapse Date + Policy Loan Account value at Lapse Date + Overdue Premium at Lapse date (if any) |
| n | 1 for quarterly/half-yearly/yearly; 3 for monthly |
| Number of Days in Installment Period | 30 (Monthly), 91 (Quarterly), 182 (Half-Yearly), 365 (Yearly) |
| TIP | Premium-Instalment-Amount + Service Tax or GST |
| Number of Days Lapsed | Positive difference between repayment date and Lapse Date |

**Minimum Amount Revival vs Full Amount Revival:**

| Revival Type | Amount Calculation |
|---|---|
| Minimum Amount Revival (RP policies) | APL_RD + Overdue TIPs with Interest up to RD |
| Minimum Amount Revival (SP/paid-up) | Interest on TDebt_LD from LD to [RD + Min(1 Year, CED  -  RD)] |
| Full Amount Revival | APL + interest up to validity date + Premium overdue + premium overdue interest up to validity date |

**Table 13: Full Amount Revival Example:**

| Item | Amount |
|---|---|
| Annual premium | 1000 |
| Last premium payment | Feb-1 2009 |
| Policy lapse | Mar-15 2010 |
| Apply APL | Mar-15 2010 |
| Lapse after APL applied | Mar-15 2011 |
| Reinstatement date | Jun-1 2012 |
| Full payment for reinstatement | APL + interest (Jun 2010 - Jun 2012) = 1000 + 20; overdue plus interest (Jun 2011 - Jun 2012) = 2000 + 10; Total: 3030 |

**2. Click benefit ID to view and modify non-waiver benefit:**

Only the following fields can be modified:
- Premium calculation indicator
- Premium and SA fields if premium calculation method is manual

**3. Click Submit on APL Reinstatement page:**

| Condition | System Action |
|---|---|
| System updates policy status to In force and initializes PLD if it exists | Done |
| System keeps old policy details and saves modified policy information | Done |
| System sets item alteration status to Completed | Done |
| After CS inforce | System updates policy status to Inforce and initialize PLD (if exists) |

---

### Rules for Cancellation

This section tells the rules in cancellation.

**1. Select a benefit and click a type of effective date:**

| Condition | System Action |
|---|---|
| Benefit status should not be Terminate | Enforced |
| If the main benefit is selected | All related riders with benefit status not equal to Terminate must also be selected |

**2. Click Submit on Surrender/Cancellation Reason Entry page:**

| Condition | System Action |
|---|---|
| Lapse date must be greater than benefit commencement date | Enforced |
| Number of completed product years < 2 | System calculates GSV at product level; if GSV < 100, displayed as 0 and treated as 0 |
| Cancellation effective type is from commencement date | Benefit should not have SB or CB |

**Cancellation Reason vs Effective Type:**

| Product | SV Defined | GSV | Cancellation Reason | CD | I | NDD | LD |
|---|---|---|---|---|---|---|---|
| Product defined with SV | Yes | GSV = 0 | Cancel by PH | Y | Y | Y | Y |
| Product defined with SV | Yes | GSV > 0 | Cancel by Company | Y | Y | Y | Y |
| Product defined with SV | No | GSV > 0 | Non-disclosure | Y | N | N | Y |

Legend: CD = Collect Date; I = Interest; NDD = Next Due Date; LD = Lapse Date

---

### Rules for Changing Assignment

This section tells the rules in change assignment.

**1. Adding an assignee:**

| Condition | System Action |
|---|---|
| Assignee must be a person, not an organization | Enforced |
| Assignee must be at least 18 years old | Enforced |
| Assignee must not be bankrupt | Enforced |
| Correspondence address of assignee must be entered | Enforced |
| Assignee must not already be the policyholder | Enforced |
| Assignee must not already be a trustee | Enforced |

**2. When all assignees are deleted:**

System sets `Policy under Assignment Indicator` to No automatically.

**3. Submit on Change Assignment page:**

| Condition | System Action |
|---|---|
| There must be at least one information change (assignee added, deleted, or changed) | Enforced; error message if violated |
| Address record must be selected for each assignee | Enforced |
| System keeps old assignment details, saves and displays modified assignment details | Done |
| System uses validity date to set start date of new assignee and end date of old assignee | Done |

---

### Rules for Changing Beneficiary

This section tells the rules in change beneficiary.

**1. Adding a beneficiary:**

| Condition | System Action |
|---|---|
| Beneficiary must be a person, not an organization | Enforced |
| Beneficiary's relationship to life assured must be selected | Enforced |
| Percentage share must be entered and total for all beneficiaries must not exceed 100% | Enforced |
| Correspondence address of beneficiary must be entered | Enforced |
| If the life assured is a minor (age < 18), the beneficiary must be a parent of the minor | Enforced |

**2. When all beneficiaries are deleted:**

System does not automatically change any indicator.

**3. Submit on Change Beneficiary page:**

| Condition | System Action |
|---|---|
| There must be at least one information change (beneficiary added, deleted, or changed) | Enforced; error message if violated |
| Address record must be selected for each beneficiary | Enforced |
| System keeps old beneficiary details, saves and displays modified beneficiary details | Done |
| System uses validity date to set start date of new beneficiary and end date of old beneficiary | Done |

---

### Rules for Changing Benefits

This section tells the rules in changing benefits.

**1. When you click Change Benefit:**

| Condition | System Action |
|---|---|
| Benefit status must be Inforce | Enforced |
| Benefit should not be a unit-linked product | Enforced |
| Benefit should not be an investment linked product | Enforced |
| Benefit should not be a waiver benefit | Enforced |
| Benefit should not have SB or CB feature as defined in product | Enforced |
| New benefit must be allowed to replace the old benefit as defined in product | Enforced |
| Premium calculation method of new benefit must be the same as old benefit | Enforced |
| Premium type of new benefit must be the same as old benefit | Enforced |
| Currency of new benefit must be the same as old benefit | Enforced |
| Sum assured entered must be within the permitted range defined in product | Enforced |

**2. When you click Save on the Benefit Information page:**

| Condition | System Action |
|---|---|
| The system recalculates benefit revised premium | Done |
| The system recalculates policy fee based on the new benefit | Done |

**3. Submit on Modify Collection/Refund page:**

| Condition | System Action |
|---|---|
| System calculates the amount to collect or refund | Done |
| For waivers, collection/refund is calculated for those attached to the changed benefits (benefits whose benefit is changed) | Waivers not attached to changed benefits but whose premium is updated due to large annual benefit discount will not require collection or refund |
| System sets up collection/refund payment method and payer using the defined algorithm | Done |

---

### Rules for Changing Birth Date or Gender

This section tells the rules for changing birth date or gender.

**1. When you click Change Birth Date or Gender:**

| Condition | System Action |
|---|---|
| Birth date and gender must be changed at party level in Party module first | Enforced |
| Policy is NOT an issue-without-premium policy | Enforced |
| Policy is WITHOUT indexation | Enforced |
| The party (policyholder or life assured) whose birth date or gender is to be changed must be selected | Enforced |

**2. When you click Submit:**

| Condition | System Action |
|---|---|
| System recalculates benefit premium (including current and next due premium) | Done |
| System recalculates benefit revised premium | Done |
| If there are waiver benefits, the system recalculates information of all waiver benefits such as SA waived, annual amount waived, and initial SA | Done |
| System calculates the amount to collect or refund | Done |
| For waivers, collection/refund is calculated if there is a change in birth date or gender on the waiver itself OR if the waiver is attached to the benefit where birth date or gender is changed | Waivers not attached to changed benefits but whose premium is updated due to large annual benefit discount will not require collection or refund |
| If there is a change on the waiver itself and this waiver is also attached to the benefit where birth date/gender is changed, the effective type of this waiver will always follow that of the changed benefit if the two effective types are different | Enforced |
| System sets up collection/refund payment method and payer using the defined algorithm | Done |

---

### Rules for Changing Commencement Date

This section tells the rules for changing commencement date.

**1. When you click Change Commencement Date:**

| Condition | System Action |
|---|---|
| New commencement date must not be later than the current system date | Enforced |
| New commencement date must not be later than the first premium due date | Enforced |
| If the policy is in the first policy year, a warning message is displayed | Warning only; can continue |

**2. When you click Submit:**

| Condition | System Action |
|---|---|
| System recalculates benefit premium | Done |
| System recalculates benefit revised premium | Done |
| If there are waiver benefits, the system recalculates information of all waiver benefits | Done |
| System calculates the amount to collect or refund | Done |
| System sets up collection/refund payment method and payer using the defined algorithm | Done |

---

### Rules for Changing Discount Type

This section tells the rules for changing discount type.

**1. When you click Change Discount Type:**

| Condition | System Action |
|---|---|
| The new discount type must be allowed according to the product setup | Enforced |
| If the new discount type is Agent, Family, or Staff, there must be no existing commission agent OR the existing commission agent must be under company direct | Enforced |

**2. When you click Save:**

| Condition | System Action |
|---|---|
| System updates discount rates according to the discount rate table set up for product | Done |
| For traditional benefit: rates include Premium Discount Rate and Loading (Expense Fee) Rate | Done |
| For ILP benefit: rates include Fund Management Fee Rate, COI Rate, Policy Fee Rate, Switch Charge, and Withdraw Charge | Done |
| System will collect the premium or charge with the new discount rate from next due date | Done |
| System updates the benefit information and recalculates the benefit premium (including current and next due premium) | Done |
| If there are waiver benefits attached to the policy, all waiver benefits information of the policy will be recalculated | Done |

**3. You can change the discount type for all the benefits under the policy.**

---

### Rules for Changing Extra Premium

This section describes the rules for changing extra premium.

**1. When you click Submit to submit the modified extra premium:**

| Condition | System Action |
|---|---|
| All mandatory fields are entered | Enforced |
| For non-investment linked product, the start date must be a due date. For investment linked product, the start date must be a monthlyversary date | Enforced |
| For non-investment linked product, the end date must be a due date except for special value 09/09/9999. For investment linked product, the end date must be a monthlyversary date except for 09/09/9999If the validity date is earlier than the system date, you must have the backdate access authority. The system counts the number of switches of the policy in a certain period. Based on product definition, switch fee can be free for defined times in a yearly/half yearly/quarterly/monthly period. The system counts the number of switches of the policy from last installment due date based on the validity date to the validity date (inclusive). The number of times that the policyholder can switch funds without any switch fee is defined in product. The system calculates the switch fee according to the switch fee rules. If the switch fee is defined at product level: Policyholder will be allowed several free times for ad hoc fund switch per predefined period. Subsequent switches within the period will be charged at switch fee respectively. Period and the switch fee amount are parameterized and defined in product. Switch fee cannot be amended by user. Switch fee will be applicable at policy level and one event will be considered as one switch. Settlement for switch fee will be allowed by Cash, Cheque or Unit Deduction. For settlement by unit deduction, the switch fee amount will be inclusive of the units to be switched out from.

If the switch fee is defined at fund level, to be deducted from the fund by percentage of the switch amount: If the switch fee calculation basis is 'per switch-in at fund level', then the switch fee will be calculated using the switch fee rate defined at product-fund level. The system displays the estimated switch fee value based on the switch fee rate defined under switch-in funds. Switch fee amount of each fund = switch fee rate  x  switch amount. Total switch fee = sum of switch fee amount of each fund. In fund transaction, after system sells the switch-out funds, system will deduct the switch fee first and purchase switch-in funds.

Switch fee deduction rules: Switch fee calculation formula is defined in FMS. Switch fee source is defined in ILP Product Charge List in Product Definition. If the fee source is 'deduct from switch-out fund', the switch fee will be deducted from switch-out fund according to calculation formula. System will generate one transaction for each fund switch. In fund transaction, after system sells the switch-out funds, system will deduct the switch fee first and purchase switch-in funds. If the fee source is 'deduct from switch-in fund', all the amount or units will be used for buying fund switched in, and the switch fee will be deducted from switch-in fund. The system will generate two transaction applications for each fund transaction: one for switch and the other for switch charge from each switch-in fund.

If the selected payment method of switch fee is Investment Account Bid, then the system will deduct the fee from each switch-out or switch-in fund, which is decided by the product definition. If the calculation basis is 'per switch-out at fund level' in ILP charge information, the fee will be deducted from each switch-out fund. If the calculation basis is 'per switch-in at fund level' in ILP charge information, the fee will be deducted from each switch-in fund. If there is more than one switch-out or switch-in fund, the system will calculate and default the switch fee per fund. It will be split equally among the switch-out funds and user can amend the amount. If the selected payment method is Cash or Cheque, the system will not display information of switch fee to be deducted from each switch-out or switch-in fund, but directly display the switching fee in switch UI. If the switch in and out funds are not the same currency: Charge fee formula always returns amount in source fund currency. Switch charge fee is in product pricing currency. This amount should be allocated proportionally in policy currency to each apply in source fund currency. CS ad hoc switch: Apply Amount and Switch Fee are in policy currency. Summary switch fee amount should be converted to policy currency. T_Fund_Service and T_Fund_Trans_Apply's apply_amount/trans_charge_fee are in source fund currency. T_Fund_Cash: Fund_Amount in fund currency; Amount in policy currency. POL_Exchange_Rate: Policy Currency > Base Currency. TRANS_Exchange_Rate: Fund Currency > Base Currency. T_Capital_Distribute records in policy currency. Common Query keep current two columns: pending amount in policy currency and fund currency. Fund Transaction: Source Fund > Target Fund including apply amount, apply unit and trans_charge_fee. All exchange rates are by exchange buy rate.

When you click Submit in the Switching Fee section: The system calculates whether there is any closed fund involved in switch-in funds. If yes, the system validates that the closed fund is still within the subscription period. If the validation fails, an error message will be displayed. The system calculates the net withdraw amount and generate pending fund transaction.

---

### Rules for Increasing SA

This section describes the rules for increasing SA.

**1. When you select a benefit and a type of effective date:**

| Condition | System Action |
|---|---|
| Benefit status should be Inforce | Enforced |
| Premium status for this benefit should be Regular | Enforced |
| The selected type of effective date should be allowed for that benefit | Enforced |

| Benefit | Benefit with SV Defined in Product | Benefit without SV Defined in Product | Remarks |
|---|---|---|---|
| Type of Effective Date | With SV | Without SV | |
| From Commencement Date | Allowed | Allowed | Amount to be collected: difference in premium from benefit commencement date to next due |
| Immediately | Not Allowed | Allowed | Amount to be collected: difference in premium from validity date to next due |
| From Next Due Date | Not Allowed | Allowed | Amount to be collected: None |

| Condition | System Action |
|---|---|
| The benefit should be independent from other benefits (for example, the benefit should not be a waiver benefit) | Enforced |
| The benefit cannot be an unit-linked product | Enforced |
| Payment method should not be unit deducted | Enforced |
| The benefit should not be a mortgage product, decreasing term product, or increasing term product | Enforced |
| The benefit should be allowed to increase SA according to product setup | Enforced |
| The application date should not be later than product withdrawal date | Enforced |
| It is a non-guaranteed premium benefit and at the point of change (using application date to check), the benefit is in guarantee period and new premium table has been declared | Enforced |
| The benefit does not have SB or CB feature according to product setup | Enforced |

**2. Increase SA Field Description Table:**

| Field | Description |
|---|---|
| SA or Units | Sum assured or units |
| Premium | Premium amount |
| Premium Calculating Method | Premium calculation method |

---

### Rules for Input Additional Health Disclosure

This section tells the rules for inputting additional health disclosure.

**1. When you click Submit to submit the health disclosure information:**

| Condition | System Action |
|---|---|
| The system displays all related policies and displays the related customer notification in the policy | The selected customer should be a life assured or policyholder of the policy |
| The system keeps the old customer health disclosure information and saves the additional health disclosure details for the selected policyholder or life assured | Done |

---

### Rules for Normal Revival

This section tells the rules in normal revival.

**1. When you select benefits and click Normal Revival:**

| Condition | System Action |
|---|---|
| Benefit status is Lapse, or benefit status is Inforce and premium status is Auto paid-up | Enforced |
| Benefit status reason should be normal lapse if benefit status is Lapse | Enforced |
| If secondary benefit is selected for revival, the primary benefit status must be Inforce or be selected for revival also | Enforced |
| If original benefit status is Lapse, benefit status will be set to Inforce | Done |
| If original benefit status is Inforce and premium status is Auto paid-up | Product code will be changed to original product code before auto paid-up, and original benefit information before auto paid-up such as SA, premium, extra premium will be restored |
| Benefit information such as next due date, premium status, policy year and payment method is updated | The new next due date is updated until this date is equal to or greater than the earlier date of fully paid up date and validity date. If the new next due date of riders is later than the next due date of main benefit, an error message will be displayed |
| All waiver benefits information such as SA waived, annual amount waived, large annual benefit discount and waiver premium is recalculated | Done |

**2. When you click Submit in the Benefit Information after Change area:**

| Condition | System Action |
|---|---|
| If there is at least one benefit with manual premium calculation method | A warning message will be displayed |
| The system validates benefits relationship (if secondary benefit is selected for revival, the primary benefit status must be Inforce or be selected for revival also) | Enforced |
| The system calculates the amount to be collected | Done |

| Condition | System Action |
|---|---|
| The system calculates overdue premium for each installment date | Done |
| The system calculates overdue interest from lapse date to validity date for all overdue premiums if overdue interest indicator of this product is set to Yes in product setup | Done |

**Overdue Interest Calculation for Normal Revival:**

| Installment | Calculation Rule |
|---|---|
| First installment premium | System will calculate interest from Validity Date to Premium Due Date if days between the two dates are greater than 45 days (grace period + additional grace period) |
| Secondary and subsequent installment premium | System will calculate interest from Validity Date to Premium Due Date if days between the two dates are greater than 30 days (grace period) |

| Condition | System Action |
|---|---|
| The system sets up the collection/refund payment method and payer | Done |
| The system updates policy information such as policy status to Inforce | Done |

---

### Rules for Partial Surrender

This section tells the rules in partial surrender.

**1. When the Partial Surrender page is displayed:**

| Condition | System Action |
|---|---|
| The system calculates GSV (SV SA + SV Bonus) of all non-waiver benefits in the Benefit Information after Change area | The system should not calculate GSV for all waivers in the Benefit Information after Change area except for those selected by CS user to reduce annual benefit amount |
| Manual SV indicator is Y | GSV is set to 0 |
| Manual SV indicator is N | The system calculates GSV (SV SA + SV Bonus) using formula defined in product |
| Benefit with premium status Regular or premium waiver | The system passes valuation date which is equal to benefit's next due date to the GSV formula |
| Benefit with premium status fully paid (premium status = auto paid up, reduced paid up, or fully paid) | The system passes the current system date to the GSV formula |
| If the system cannot determine GSV using above mentioned formula | GSV is set to 0 |

**2. When you select a benefit and click Partial Surrender:**

| Condition | System Action |
|---|---|
| Benefit status should be Inforce | Enforced |
| Benefit should not be an investment linked product or unit-deduction rider | Enforced |
| Benefit should be a SV benefit as defined in product | Enforced |
| Benefit should not be a mortgage product, decreasing term product, or increasing term product | Enforced |
| If the selected benefit is a non-waiver benefit, it should be allowed to perform partial surrender as defined in product (in the product table, the Allow Decrease in SA indicator for this product should be Yes) | Enforced |
| If the selected benefit is a waiver benefit, it should be defined with annual benefit in product setup and the annual benefit amount should be greater than 0 | Enforced |
| Benefit premium status should be Regular or Premium waived | Enforced |

**3. When you enter the new sum assured and click Save:**

| Condition | System Action |
|---|---|
| Premium and sum assured fields (if premium calculation method is manual) | Enforced |
| Sum assured or units fields (if premium calculation method is to use sum assured to calculate premium) | Enforced |
| Premium fields (if premium calculation method is to use premium to calculate SA) | Enforced |
| New sum assured or units should be less than original sum assured or units | Enforced |
| New premium should be less than original premium | Enforced |
| Sum assured should be equal to or more than the minimum sum assured defined in product SA limit table | Enforced |
| Sum assured or units decreased in one time should be greater than the minimum sum assured or minimum units to be decreased defined in product | Enforced |
| Current and next sum assured will be updated with the new sum assured | Done |
| The system recalculates policy fee based on the new sum assured | Done |
| The system recalculates the current and next premium of benefit after change | Done |

| Condition | System Action |
|---|---|
| The system calculates GSV (SA SV + Bonus SV) of this benefit | Done |
| Manual SV indicator is Y | GSV is set to 0 |
| Manual SV indicator is N | The system calculates GSV (SV SA + SV Bonus) using formula defined in product |
| Benefit with premium status Regular or premium waiver | The system passes valuation date which is equal to benefit's next due date to the GSV formula |
| Benefit with premium status fully paid | The system passes the current system date to the GSV formula |
| If the system cannot determine GSV using above mentioned formula | GSV is set to 0 |
| The system reduces reversionary bonus by the corresponding sum assured amount surrendered | Done |
| New RB = original RB  x  ((original SA - reduced SA)/original SA) | Result is rounded to next cents |
| The system keeps old benefit details and saves modified benefit information | Done |

**4. When you click Submit in the Benefit Information after Change section:**

| Condition | System Action |
|---|---|
| For all benefits that satisfy the above conditions and having manual SV calculation indicator = N, the difference between the total benefit GSV and the total benefit actual GSV should be less than or equal to $4 ($4 is a parameterized value) | Enforced |
| If there is at least one benefit satisfies the above conditions with premium status Regular or premium waiver | The difference between validity date and system date should not be more than 45 days (45 days is the contractual grace period + additional grace period defined in product) |
| If there is at least one benefit satisfies the above conditions with premium status not equal to Regular or premium waiver | Validity date can be backdated up to 7 days but cannot be greater than the system date (7 days is a parameterized value) |
| For every benefit that satisfies the above conditions with premium status Regular or premium waiver | The difference between validity date and valuation date should not be more than 45 days |
| The system determines administrative fee required for this transaction if any | Done |
| The system sets up collection/refund payment method and payer using the defined algorithm | Done |
| The system keeps old policy details and saves modified policy information | Done |
| The system sets up payment method and payee for GSV if GSV > 0 | Done |

**5. When you click Submit on the Modify Collection/Refund page:**

| Condition | System Action |
|---|---|
| The system sets the item alteration status to Completed | Done |

---

### Rules for Performing ETA

This section describes the rules for performing ETA.

**1. When you click ETA:**

| Condition | System Action |
|---|---|
| Next due date of main benefit  >= 7 days  <= validity date  <= next due date of main benefit + 45 days | Enforced |
| If the manual SV indicator of main benefit is N | The main benefit's calculated coverage end date should be greater than the main benefit's commencement date |
| The system extracts a list of benefits qualified for ETA | The benefits qualified for ETA must meet the following requirements: Benefit risk status is Inforce; Benefit is allowed to perform ETA as defined in product; Manual SV indicator is Y, or manual SV indicator is N and calculated benefit coverage end date > commencement date |

**The system performs ETA for each qualified benefit extracted:**

| Condition | System Action |
|---|---|
| Manual SV indicator is N | The system calculates excess SV and ETA coverage end date according to formula defined in product. Next due date is passed as valuation date to the formula. For substandard life, rated up age is passed to the formula |
| It is an Asset Share product, the number of completed product years < 2 and the GSV of product is less than a specified amount defined | Then the system uses GSV = 0 for Net SV calculation |
| The calculated coverage end date is earlier than the coverage end date | The system updates the coverage end date to the calculated coverage end date; otherwise, the coverage end date remains the same |
| The system updates benefit coverage type to cover for certain years and coverage term to the difference between commencement date and coverage end date (round down to year) | Done |
| The system updates benefit premium status to ETA | Done |
| The system resets RB to 0 and nullifies bonus due date if RB exists | Done |
| Benefit has excess GSV | The system updates the benefit product code to the new product code and records the original product code. Excess GSV will be displayed and refunded upfront |
| Benefit has no excess GSV | The system updates the benefit product code to the new product code and records the original product code |

| Condition | System Action |
|---|---|
| Manual SV indicator is Y | The system updates the benefit product code to the new product code and records the original product code. The system updates benefit coverage type to cover for certain years and coverage term to the difference between commencement date and coverage end date (round down to year). The system updates benefit premium status to ETA. The system resets RB to 0 and nullifies bonus due date if RB exists |

**The system extracts a list of qualified benefits to be cancelled:**

| Condition | System Action |
|---|---|
| Benefit is not terminated | Enforced |
| Benefit is not allowed to do ETA, or the benefit is allowed to do ETA and the manual SV indicator is N and the calculated coverage end date is earlier than the commencement date | Enforced |

**The system cancels all the qualified benefits extracted:**

| Condition | System Action |
|---|---|
| The system updates benefit risk status to Terminate, terminate reason is Cancel by PH and termination date is next due date of main benefit | Done |

| Condition | System Action |
|---|---|
| If the policy is eligible for premium voucher (as defined in product) and basic plan has changed | The system updates PV utilize to Y and Current PV available amount to 0 |
| Benefit coverage end date and excess SV in the Benefit Information after Change area is allowed to be modified for benefits that satisfy all the following conditions | Benefit is allowed to perform ETA as defined in product; Manual SV indicator is Y |
| Benefit coverage end date after change should be later than the benefit commencement date and earlier than the original coverage end date | Enforced |
| Excess SV after change should not be less than 0 | Enforced |

**2. When you click Submit in the Benefit Information after Change section:**

| Condition | System Action |
|---|---|
| If excess SV is to be refunded upfront | The system calculates the amount to refund and displays the Modify Collection/Refund page. You can view and modify the amount to refund |
| The system updates endorsement codes information | Done |

---

### Rules for Performing Reduced Paid-up

This section tells the rules for reduced paid-up.

**1. When you click Reduce Paid up:**

| Condition | System Action |
|---|---|
| Next due date of main benefit  >= 7 days  <= validity date  <= next due date of main benefit + 45 days | Enforced |
| If manual SV indicator of main benefit is N, reduced paid up SA of main benefit should be greater than 0 | Enforced |
| For all riders with risk status Inforce and premium status Regular, riders must not acquire SV if the parameter Allow Reduced Paid-Up in product definition is set to N | The system performs the following check; if the check fails, a warning message will be displayed |

| Condition | System Action |
|---|---|
| For all riders with risk status Inforce and premium status Regular, riders should not acquire SV if the parameter Allow Reduced Paid-Up in product definition is set to Y | The system performs the following check; if the check fails, a warning message will be displayed |

**The system extracts a list of benefits that satisfy the following conditions to perform reduced paid-up:**

| Condition | System Action |
|---|---|
| Benefit risk status is Inforce | Enforced |
| Benefit premium status is Regular | Enforced |
| Benefit allows reduced paid-up as defined in product | Enforced |
| Manual SV indicator is Y, or manual SV indicator is N and paid up SA of benefit is greater than 0 | Enforced |

**The system performs reduced paid-up for the extracted benefits:**

| Condition | System Action |
|---|---|
| The system updates benefit product code to new product code after paid-up and records the original product code | New product code after paid-up is defined in product |
| Benefit is a SV benefit as defined in product | The system calculates reduced paid-up SA and updates benefit SA |
| Benefit has excess GSV | The system updates benefit product code to new product code and records original product code. Excess GSV will be displayed and refunded upfront |
| Benefit has no excess GSV | The system updates benefit product code to new product code and records original product code. New product code is defined in product |
| Benefit is not a SV benefit as defined in product | The system updates benefit SA using main benefit's paid-up SA |
| Reduced paid-up SA can be higher or lower than original benefit SA | The system will update benefit SA with reduced paid-up SA value, regardless of whether it is lower or higher |
| The system sets RB amount to 0 and nullifies bonus due date | Done |
| The system updates premium status to Reduced Paid Up | Done |
| The system saves SA before paid-up and keeps next due date, paid up date, risk status, premium amount, and so on | Done |
| The benefit has indexation | The system terminates the original segment information |

**The system extracts a list of qualified benefits to be cancelled:**

| Condition | System Action |
|---|---|
| Benefit is not terminated | Enforced |
| Benefit premium status is Regular | Enforced |
| Benefit does not allow reduced paid-up, or benefit allows reduced paid-up and manual SV indicator is N and reduced paid up SA of benefit  >= 0 | Enforced |

**The system cancels the benefits extracted:**

| Condition | System Action |
|---|---|
| The system updates benefit risk status to Terminate, terminate reason to Cancel by PH, and termination date to next due date of main benefit | Done |
| If the policy is eligible for premium voucher (as defined in product) and basic plan has changed | The system updates PV utilize to Y and Current PV available amount to 0 |

**2. When you click Submit in the Benefit Information after Change section:**

| Condition | System Action |
|---|---|
| Benefit SA value in the Benefit Information after Change section is allowed to be modified only for the benefit that satisfies the following conditions | Benefit allows reduced paid-up as defined in product; Benefit is a SV benefit with manual SV indicator = Y; Benefit premium status is Reduced paid up |
| After change, the new benefit SA value should be greater than 0 | Enforced |
| The system calculates the amount to be refunded if excess SV is to be refunded upfront | Done |
| The system sets up collection/refund payment method and payer using the defined algorithms | Done |
| The system cancels a list of endorsement codes with effective from validity date | Done |

---

### Rules for Reversionary Bonus Surrender

This section tells the rules for reversionary bonus surrender.

**1. RB Gross Surrender Value Calculation:**

| Condition | System Action |
|---|---|
| Risk status = Inforce | Enforced |
| Manual SV calculation indicator = N | Enforced |
| It is a SV benefit defined in product | Enforced |
| Benefit is allowed to surrender bonus only (as defined in product) | Enforced |

**For every benefit in policy that satisfies all the 4 conditions above:**

| Condition | System Action |
|---|---|
| System calculates benefit RB GSV as per formula defined in product | Done |
| Benefit with premium status = regular or premium waiver | System passes valuation date which equal to Next due date to RB GSV formula |
| Benefit with premium status is fully paid (i.e. fully paid-up, reduced paid-up and auto paid up) | System passes current system date to RB GSV formula |
| If system cannot determine the RB GSV | RB GSV is set to 0 |

**For other benefits that do not satisfy the above 4 conditions:**

| Condition | System Action |
|---|---|
| System set RB GSV to 0 | Done |

**2. Policy RB Net Surrender Value Calculation:**

| Condition | System Action |
|---|---|
| The system calculates mandatory debts according to formula defined | Validity date is passed to calculate overdue interest for the debts accounts and valuation date is passed to calculate SV |
| The system calculates policy net surrender value (NSV) | Done |

| Condition | System Action |
|---|---|
| If sum (benefits actual GSV) > mandatory debts | NSV = sum (benefits GSV)  <= mandatory debts |
| If sum (benefits actual GSV)  <= mandatory debts | NSV = 0 |

Both mandatory debts and NSV will be recalculated again and updated to system when the application takes effect. This is to take care of situation where there is a loan repayment that will affect mandatory debts calculation before application takes effect.

| Example | Benefit 1 RB GSV | Benefit 2 RB GSV | Mandatory Debts | RB NSV |
|---|---|---|---|---|
| Example 1 | 1000 | 500 | 1200 | 300 |
| Example 2 | 1000 | 500 | 1600 | 0 |

**3. When you click Reversionary Bonus Surrender:**

| Condition | System Action |
|---|---|
| Benefit allows surrender on bonus only as defined in product | Enforced |
| Benefit is a SV benefit as defined in product | Enforced |
| The system updates RB gross surrender values (GSV) | Done |
| The system determines administrative fee required for this transaction (if any) | Done |
| The system sets up collection/refund payment method and payer using the algorithms defined | Done |
| Reduces reversionary bonus | For each selected benefit, the system reduces reversionary bonus using the following formula: New RB = original RB  <= surrendered RB. The system currently only supports full RB surrender. Therefore, new RB = 0 |
| Recalculates GSV amount | Done |

**For every benefit in policy that satisfies the following four conditions:**

| Condition | System Action |
|---|---|
| Risk status is Infoce | Enforced |
| Manual SV calculation indicator is N | Enforced |
| Benefit is a SV benefit defined in product | Enforced |
| Benefit allows surrender on bonus only as defined in product | Enforced |

| Condition | System Action |
|---|---|
| System calculates benefit RB GSV as per formula defined in product | Done |
| Benefit with premium status Regular or premium waiver | System passes valuation date which equal to next due date to RB GSV formula |
| Benefit with premium status equal to fully paid (fully paid-up, reduced paid-up or auto paid up) | System passes current system date to RB GSV formula |
| If the system cannot determine the RB GSV | RB GSV is set to 0 |

**For the benefits that do not satisfy the above four conditions:**

| Condition | System Action |
|---|---|
| System set RB GSV to 0 | Done |

**4. When you click Submit on the Reversionary Bonus Surrender page:**

| Condition | System Action |
|---|---|
| RB GSV of all selected benefits must be greater than 0 | Enforced |
| For all selected benefits in policy, the difference between the sum of benefit GSV in the Benefit Information before Change area and the sum of benefit GSV in the Benefit Information after Change area must be less than or equal to the tolerance limit $4 ($4 is a parameterized value) | Enforced |
| If there is at least one selected benefit with premium status equal to Regular or premium waiver | The difference between validity date and system date should not be more than 45 days (45 days is the contractual grace period + additional grace period defined in product. It is a parameterized value) |
| If there is at least one selected benefit with premium status not equal to Regular or premium waiver | Validity date can be backdated up to 7 days but cannot be greater than system date |
| For every selected benefit with premium status equal to Regular or premium waiver | The difference between validity date and valuation date should not be more than 45 days (45 days is the contractual grace period + additional grace period defined in product. It is a parameterized value) |

---

### Rules for Special Revival

The section tells the rules in special revival.

**1. When you select benefit and click Special Revival:**

| Condition | System Action |
|---|---|
| Benefit status should be Lapse and lapse reason should be Normal Lapse | Enforced |
| The main benefit must be selected | Enforced |
| If there is pre-contract information for this policy | A warning message will be displayed. However, you can click Continue to proceed. The system will delete all pre-contract information for this policy |

| Condition | System Action |
|---|---|
| For all benefits, benefit commencement date will be set to original benefit commencement date + (validity date - lapse date) | The new commencement date must be before the product withdrawn date |
| For non-revived benefits, benefit next due date will be derived using the new benefit commencement date | Done |
| For revived benefits, benefit next due date will be derived using the new benefit commencement date and then moved by one premium installment | Done |
| For all benefits, the premium cessation date and risk cessation date will be recalculated based on the new benefit commencement date | Done |
| For all benefits, age at entry will be recalculated | Done |
| Deletes all pre-contract information for this benefit if any | Done |
| For all benefits, premium will be recalculated based on the new age (including current and next premium) | Done |
| For all benefits that have reversionary bonus feature (as defined in product) | The system sets Reversionary Bonus to 0 and updates bonus due date using benefit new commencement date + 1 year |
| For all benefits that have cash bonus feature (as defined in product) | The system modifies new cash bonus due date based on the new commencement date of policy |
| For all benefits that have survival benefit feature (as defined in product) | The system modifies the new survival benefit payment start date and new survival benefit due date based on the policy new commencement date |

**The system records the following benefit information (the actual updates will only happen upon the effective application):**

**2. When you click Submit on the Benefit Information after Change section:**

| Condition | System Action |
|---|---|
| Validity date must be later than the policy lapse date | Enforced |
| Benefit relationship must be valid according to product setup | Enforced |
| If secondary benefit is selected, the primary benefit must also be selected | Enforced |
| If there are benefits with manual premium calculation method | A warning message will be displayed |
| The system calculates the amount to be collected | Done |

| Field | Calculation |
|---|---|
| Policy collection | Sum of collection for every revived benefit + administrative fee = Sum of (difference in premiums + 1 modal premium) for every revived benefit) + administrative fee |
| Difference in premiums | Calculated by premium installments using new benefit premium minus original benefit premium |
| Modal premium difference | Maximum (new benefit premium minus original benefit premium, 0), using current premium to calculate |
| Start date | New commencement date |
| End date | New due date (before move 1 modal) |
| 1 modal premium | New benefit installment premium inclusive of ST if ST is present |
| No interest is collected for special revival | Enforced |
| The system keeps old policy details and saves modified policy information | Done |
| The system updates the policy status to Inforce when the total collection is received | Done |
| The system updates the policy level information such as policy commencement date, policy risk cessation date and premium cessation date using basic plan's benefit information after change | Done |

**4. Update policy information:**

| Condition | System Action |
|---|---|
| System updates the policy status to Inforce once total collection is received | Done |
| System updates the policy level information such as policy inception date, policy risk cessation date and premium cessation date using basic plan's benefit information after change | Done |

---

### Rules for Surrender

This section tells the rules in surrender.

**1. GSV Calculation:**

For every benefit in policy:

| Condition | System Action |
|---|---|
| Benefit risk status is Inforce, Manual SV calculation indicator is N, and is a SV benefit defined in product | The system calculates GSV (SV SA+SV Bonus) using formula defined in product |
| Benefit with premium status = regular or premium waiver | System passes validation date which equal to Next due date to GSV formula |
| Benefit with premium status is fully paid (i.e. premium status is auto paid up or reduced paid up or fully paid) | System passes current system date to GSV formula |
| System cannot determine the GSV | GSV is set to 0 |

For other benefits that cannot meet the conditions above:

| Condition | System Action |
|---|---|
| System sets GSV=0 | Done |

**2. When you select a surrender reason and click Surrender:**

| Condition | System Action |
|---|---|
| If you select the main benefit or primary benefits | All the non-terminated secondary benefits will also be selected automatically |
| Benefit's GSV is allowed to be modified in the Benefit Information before Change area if the benefit is a SV benefit defined in product and its status is Inforce | Allowed |

| Condition | System Action |
|---|---|
| None of the selected benefits is in Terminate status | Enforced |
| The benefit status of the highest primary benefit selected should be in Inforce status | There can be more than one highest primary benefit, depending on the user selection |

**Definition of highest primary benefit:**

| Scenario | Highest Primary Benefit |
|---|---|
| Policy consists of: Basic Plan; Rider 1 WOP 1 (on Rider 1); Rider 2 WOP 2 (on Rider 2) | If CS user selects Main Plan, the system automatically selects Rider 1, WOP 1, Rider 2, and WOP 2. In this case, the highest primary benefit is Main Plan |
| If CS user selects Rider 1 | The system automatically selects WOP1. In this case, the highest primary benefit is Rider 1 |
| If CS user selects Rider 1 and Rider 2 | The system automatically selects WOP 1 and WOP 2. In this case, the highest primary benefits are Rider 1 and Rider 2 |

| Condition | System Action |
|---|---|
| The benefit status of the highest primary benefit selected is SV benefit as defined in product | Enforced |

| Benefit Status | Terminate Reason | Terminate Effective Date |
|---|---|---|
| Terminate | Terminate reason selected by CS user: Converted | Application effective date |

| Condition | System Action |
|---|---|
| Update GSV | The GSV (SV SA + SV Bonus) of the selected benefits are updated in system | The system will not calculate unexpired premium refund for benefits that are lapsed or do not have SV as defined in product |
| The system determines administrative fee required for this transaction (if any) | Done |
| The system sets up collection/refund payment method and payee using the algorithms defined | Done |
| Sets Reversionary Bonus for each selected benefit to 0 | Done |
| Updates waivers premium | Done |
| Recalculates GSV amount and displays it in the Benefit Information after Change | Done |

**3. When you click Submit on the Surrender page:**

| Condition | System Action |
|---|---|
| The GSV of the selected highest primary benefit(s) must be greater than 0 | Enforced |
| For all selected benefits that satisfy the following conditions | Risk status is Inforce; Manual SV calculation indicator is N; Benefit is SV benefit defined in product |
| The difference between the sum of benefit GSV in the Benefit Information before Change area and the sum of benefit GSV in the Benefit Information after Change area must be less than or equal to $4 ($4 is a parameterized value) | Enforced |
| If there is at least one selected benefit with GSV > 0 and premium status equal to Regular or premium waiver | The difference between the validity date and the system date should not be more than 45 days (45 days is the contractual grace period + additional grace period defined in product. It is a parameterized value) |
| If there is at least one selected benefit with GSV > 0 and premium status not equal to Regular or premium waiver | Validity date can be backdated up to 7 days but cannot be greater than the system date |
| For each selected benefit with GSV > 0 and premium status equal to Regular or premium waiver | The difference between the validity date and the valuation date should not be more than 45 days (45 days is the contractual grace period + additional grace period defined in product. It is a parameterized value) |
| The benefit relationship must be correct | Enforced |
| All waivers should be terminated together | Enforced |

| Condition | System Action |
|---|---|
| If none of the benefit status after change equals to Inforce or Lapse | The system updates the policy status to Terminate, terminate reason to the basic plan's terminate reason, and terminate date to basic plan's terminate date |
| If main plan is selected for surrender | The system calculates the net surrender value (NSV) according to the following logic: NSV = Maximum [Sum (Selected Benefits GSV) - APL & interest - policy loan & Interest - study loan & Interest, 0] |
| SB, CB, APA, APL and policy loan balance will be derived based on current amount (amount as of current status, not as of validity date) | Interest for these accounts will be calculated based on validity date |

| Example | GSV | Accumulated SB & Interest | Accumulated CB & Interest | All suspense Account | APA account | APL & Interest | Policy loan & Interest | NSV |
|---|---|---|---|---|---|---|---|---|
| Example 1 | 1400 | 100 | 120 | 50 | 0 | 60 | 40 | 1400 - (60+40) = 1300 |
| Example 2 | 1400 | 100 | 120 | 50 | 0 | 400 | 500 | 0 (since 1400 < 900) |

NSV calculated here will be for displayed only. The actual offset of debts accounts against GSV will only happen in the BCP payment requisition UI.

| Condition | System Action |
|---|---|
| If only riders are selected for surrender | The system calculates mandatory debts according to formula defined. Validity date is passed to calculate overdue interest for the debts accounts and valuation date is passed to calculate SV |

**The system calculates policy net surrender value (NSV):**

| Condition | System Action |
|---|---|
| If sum (benefits actual GSV) > mandatory debts | NSV = sum (benefits actual GSV)  <= mandatory debts |
| If sum (benefits actual GSV)  <= mandatory debts | NSV = 0 |

Both mandatory debts and policy NSV will be recalculated again and updated when the application takes effect. This is to take care of situation where there is a loan repayment that will affect mandatory debts calculation before application takes effect.

NSV = maximum [sum (selected benefit's GSV) - mandatory debts, 0]

| Example | Mandatory Debts | NSV |
|---|---|---|
| Example 1 | 700 | 800 |
| Example 2 | 1800 | 0 |

---

### Rules for CS Item Overdue Interest Calculation

| Condition | System Action |
|---|---|
| When the CS is not normal revival, for both overdue premium and entire installment premium | System will calculate interest from CS Validity Date to Premium Due Date if days between the two dates are greater than 30 days (Grace period) |
| When the CS is Normal Revival | For the first installment premium, system will calculate interest from CS Validity Date to Premium Due Date if days between the two dates are greater than 45 days (Grace period + Additional Grace Period). For the secondary and subsequent installment premium, system will calculate interest from CS Validity Date to Premium Due Date if days between the two dates are greater than 30 days (Grace period) |
| When the CS is APL Revival | For the overdue premium after Pro-rated APL, system will calculate interest from CS Validity Date to Premium Due Date if days between the two dates are greater than 45 days (Grace period + Additional Grace Period) |

---

### Rules for Underwriting Decision Disposal

This section tells the rules in underwriting decision disposal.

**1. When you click a target application ID:**

| Condition | System Action |
|---|---|
| The policy has APA | A warning message will be displayed. However, you can click Continue to proceed |
| The policy has Potential Lapse Date | A warning message will be displayed. However, you can click Continue to proceed |

**2. When you want to adjust alteration items:**

| Condition | System Action |
|---|---|
| You have the authority to edit the alteration item | Enforced |
| The status of the alteration item should not be Rejected | Enforced |
| If the current status of this alteration item is Completed | Status of all alteration items with sequence number greater than this item should be Pending Data Entry or Rejected. Status of all alteration items without sequence number should not be Processing in Progress |
| If current status of this alteration is not Completed | Status of all the other alteration items should not be Processing in Progress |

**3. When you click Submit on the Underwriting Decision Disposal page:**

| Condition | System Action |
|---|---|
| Health warranty date must be entered | Enforced |
| There must be at least one alteration item with status Completed and the possible alteration item statuses are Completed or Rejected | Enforced |
| The system updates the application status | Done |

| Application Status | System Action |
|---|---|
| If application status is Pending Follow Up | The system saves application information |
| If APL revival is performed for this application | If all suspense (policy collection + general suspense + renewal suspense) is equal to or greater than the minimum amount to revival, the system enforces the application and sets the application status to Inforce. If all suspense (policy collection + general suspense + renewal suspense) is less than the minimum amount to revival, the system sets application status to Approved |
| If APL revival is not performed for this application | If the application is with collection, the system sets the application status to Approved. Collection needs to be performed. If the application is without collection, the system enforces the application and sets the application status to Inforce |
| If the application status is Approved and there is payment to be collected or refunded | The system offsets fee records automatically, and displays the payment/collection information before and after the Fee Record Offset process. If there is only payment after fee record offset, you can click the Go to refund allocation button to complete the payment process. If there is no payment or if there is collection, this button is unavailable |

---

### Rules for Customer Service Approval

This section tells the rules in application approval.

**1. When you select a target application ID:**

| Condition | System Action |
|---|---|
| If the application status is Pending Approve | After you enter the Application Approve page, the application status changes to Approving and this case is locked by the current user |
| If you change something and then click Back during the approval process | The application status will still be Approving |
| If you do not change anything and then click Back during the approval process | The application status remains Pending Approve and any user with proper authority can dispose the case |
| If the application status is Approving | Before you finish the case, that means before you approve, go back to application entry, or reject the application, the application status is always Approving |

**2. When you click Approve:**

| Condition | System Action |
|---|---|
| The system checks for collection or refund | Done |
| If the application does not have collection or refund | The application status will become Inforce |
| If the application has refund | The application will become Inforce and the payment/collection information page will be displayed |
| If the application has collection | The application will become Approved and the payment/collection information page will be displayed |
| If there is collection or refund | System offsets fee records automatically |
| If there is collection | System generates an endorsement letter |
| If there are both accepted and rejected items | System generates both rejection letters and endorsement letters |
| System displays the payment/collection information before and after the fee record offset process | Done |
| If there is only payment after fee record offset | You can click the Go to Refund Allocation button to link to the BCP payment menu to complete the payment process. If there is no payment or if there is collection, this button is unavailable |

---

### Rules for Customer Service Inforce

**1. Alteration commencement date and alteration risk commencement date:**

| Field | Description |
|---|---|
| Alteration commencement date | The date that is used to calculate the policy value, age at inception, premium, etc. |
| Alteration risk commencement date | The date that is used to determine when the risk coverage starts for the benefit alteration |

**2. When system recalculates mandatory debts and new surrender value:**

| Condition | System Action |
|---|---|
| System validates whether the current application consists of any of the following alteration items | Partial surrender; Full surrender of riders only; Bonus surrender |
| If the application consists of any of these alteration items | System recalculates mandatory debts and net surrender value |

| Field | Calculation |
|---|---|
| Mandatory debts for total available policy loan amount | Maximum (current policy loan account value + current APL loan account value - total available policy loan amount after alteration, 0) |

| Field | Description |
|---|---|
| Total available policy loan amount | Sum (benefit available loan amount) |

| Condition | System Action |
|---|---|
| Risk status is not Terminated | Enforced |
| The benefit can do policy loan, as defined in product | Enforced |
| Payment method is not CPF category | Enforced |
| If benefit is a traditional product | Benefit available loan amount = current benefit SV (including reversionary bonus SV and terminal bonus SV)  x  x%, x is defined in product |
| If benefit is an investment linked product | Benefit available policy loan amount = total investment value  x  x%, use the latest known price to calculate total investment value |
| Loan account value as at date | Loan principal amount + interest balance + interest earned, interest earned can be positive or negative |

| Field | Description |
|---|---|
| Principle | Capitalization principal in loan account |
| Start Date | Latest interest calculation date |
| End date | If current loan interest balance = 0, end date = maximum (current calculation date, latest interest calculation date); otherwise, end date = current calculation date |

| Condition | System Action |
|---|---|
| System offsets mandatory debts against loan accounts | The offset sequence is as follows: APL loan principal; APL loan interest; Policy loan principal; Policy loan interest |

---

### Rules for Customer Service Application Rejection

This section tells the rules of application rejection.

**1. When you click OK to confirm the rejection:**

| Condition | System Action |
|---|---|
| The application status is changed to Rejected and all alteration items in this application are updated to Rejected | Done |
| A rejection letter is generated automatically in Letter module | Done |
| The system unfreezes the policy of this application | Done |

---

### Rules for Online Application Cancellation

This section tells the rules for cancelling application online.

**1. When you click OK to confirm the application cancellation:**

| Condition | System Action |
|---|---|
| The system saves the information and updates application status to Cancelled | Done |
| If payment/collection offset has been performed, the system undoes the payment/collection record generation for this application | If there is offset against any suspense account, the amount will go back to general suspense (either cash or CPF suspense accordingly) |
| The system unfreezes the policy of this application | Done |

---

### Rules for Changing Health Warranty Date

This section describes the rules for changing health warranty date.

**1. When you change the health warranty date:**

| Condition | System Action |
|---|---|
| The new health warranty date cannot be earlier than the original health warranty date or system date, whichever is later | For example, if the original health warranty date is June 10, 2004 and system date is June 1, 2004, then the new heath warranty date must be later than June 10, 2004 |

---

### Rules for Regular Withdrawal Plan Set or Change

This section tells the rules for setting or changing regular withdraw plan.

**1. When you enter or change the basic information in the Regular Withdraw Plan Basic Info area:**

| Condition | System Action |
|---|---|
| The Start Date and End Date must be later than the Commencement Date and earlier than the policy end date | Enforced |
| The End Date must match the Start Date and Regular Withdraw Frequency | Enforced |
| If Regular Withdraw Frequency is changed | The original due date must match the Start Date and the new withdraw frequency |

---

### Rules for Alteration Reverse

This section tells the rules for reversing alteration.

**When you search out the target transaction record:**

| Condition | System Action |
|---|---|
| If the Reversal Reason is Dishonored Cheque | The Cheque No. must be provided |
| If the alteration items has used collection amount | CS user could not choose the reason of Dishonoured Cheque or Incorrect Amount. User will only be able to select CS undo reason = Cancellation of Application, Human Error, or Customer Request. Dishonored cheque and Incorrect Amount should be done by BCP user and triggered via Cancel Collection |
| The following transaction records will be disabled | Policy turn inforce transaction; Transactions which have been undone; Transactions in the undo skip list, including: Change payment method; Change beneficiary; Change trustee; Change assignment; Change policyholder; Apply premium holiday indicator (ILP); CB/SB change option and disbursement method |
| If undo reason is Dishonored Cheque | The system disables all the transactions which are related with the target cheque |
| If there is any claim with status not equal to Canceled or Rejected | The system displays an error message for user to follow up and disables all transactions |

**When you select an transaction and click Reverse Transaction:**

| Condition | System Action |
|---|---|
| All the transactions after the selected transaction will be selected automatically | Done |
| For the investment linked policy | The system checks whether the selected transactions are done before any dividend/coupon payment transactions |

| Condition | System Action |
|---|---|
| If yes | An error message will be displayed for you to manually adjust or correct related transactions after dividend/coupon payment transaction date. The undo process ends |
| If not | The system checks whether there are any payment transactions between the undo start date and the undo end date |

| Condition | System System |
|---|---|
| If yes | The system checks whether there are any payment transactions with payment status Confirmed. If yes, the system freezes the policy; if not, an error message will be displayed for you to follow up (user needs to cancel payment and the cancellation reason should be Void Payment Requisition. For details, refer to Cancel Payment and the undo process ends |
| If not | The system freezes the policy |

**When the undo is successful:**

| Condition | System Action |
|---|---|
| The system undoes transaction fee records | Done |
| The system sums up the fee records | The payer and payee will be derived again according to the common rule when generating fee records due to undo |
| The system determines whether there is a net collection or net payment to be done following undo of all transactions | Done |

| Condition | System Action |
|---|---|
| If there is a net collection to be collected from customer | The system checks whether there is sufficient suspense balance, including policy collection, renewal and general suspense |

| Condition | System Action |
|---|---|
| If yes | The system activates the undo transactions and unfreezes the policy. The undo process ends. The undo transactions include the following: Fee record undo; Policy alteration undo; Fund Transaction undo: Reverse charges; Adjust units accordingly (current day price is used); If a sell transaction is undone, the system will use the offer price to buy units back. If a buy transaction is undone, the system will use the bid price to sell units. The current day fund price will be used in the fund transaction undo. Profit or loss, if any, will be undertaken by the company; Account undo: Adjust interest balance to last capitalization date; Adjust principal and interest balances |
| If not | A message will be displayed, indicating that money needs to be collected into general suspense before undo can proceed |
| If there is a net payment to customer | The system deposits the money into general suspense, activates the undo transactions, and unfreezes the policy. The undo process ends. User will decide how to refund the money to customer. The system will deposit money to general suspense for reversal reasons Human Error/Customer Request and Cancellation of Application only |

| Condition | System Action |
|---|---|
| A report will be generated at the end of the day for user to follow up the reversed transactions | Done |

---

### Rules for Vesting Cancel or Reset

This section tells the rules for cancelling or resetting vesting.

**1. When you want to insert a vesting schedule and click Reset Vesting:**

| Condition | System Action |
|---|---|
| The system attaches vesting endorsement codes | Done |
| The system creates the vesting schedule and updates the vesting age based on endorsement codes | Done |
| The system sets the vesting status to Waiting for Effective | Done |
| If no vesting endorsement code is attached | An error message will be displayed |

**2. When you want to cancel vesting and click Cancel Vesting:**

| Condition | System Action |
|---|---|
| The system changes the vesting status to Cancelled | Done |
| The system cancels the list of vesting endorsement codes with effective from the system date | Done |
| If you want to cancel vesting | The vesting schedule must exist and the original vesting status must be Waiting for Effective |

**3. After vesting is cancelled, if you want to reset vesting and click Reset Vesting:**

| Condition | System Action |
|---|---|
| The system changes the vesting status to Waiting for Effective | Done |
| The system reactivates and attaches vesting endorsement codes | Done |
| If no vesting endorsement code is attached | An error message will be displayed |

---

### Rules for Policy Manual Adjustment

This section tells the rules in policy manual adjustment.

**1. When you select a proper premium calculation method and update the standard premium:**

| Condition | System Action |
|---|---|
| If the premium calculation method is changed | The system checks the product table for a list of allowable values for this product. If there are no allowable values, an error message will be displayed |
| If the standard premium is changed | Premium Calculation Method must be set to Agreed premium |
| If Premium Calculation Method is set to Agreed premium | The benefit should not have premium discount indicator |

**2. When you click Submit:**

| Condition | System Action |
|---|---|
| The system saves policy and benefit information | Done |
| The system recalculates and updates premium information based on the changed standard premium value | Done |
| The system regenerates renewal draw through the Extract Amount to Bill batch job | Done |
| The system records the user ID and transaction date | Done |

---

### Rules for Manual Adjust Financial Data

This section describes the rules for manually adjusting financial data.

**When you update the policy information:**

| Condition | System Action |
|---|---|
| If Policy Risk Status is Lapsed | Lapse Date and Lapse Reason must be set and must be the same as those of the main benefit; Lapse Date must satisfy: policy commencement date  <= lapse date  <= policy risk cessation date; In Force Date, Termination Date, and Termination Reason must be empty; For a non-investment linked policy, Lapse Reason can only be Normal Lapse or APL Lapse; for an investment linked policy, Lapse Reason can only be ILP Lapse; The risk status of any benefit cannot be Inforce |
| If Policy Risk Status is Inforce | In Force Date must be set and must be the same as that of the main benefit; In Force Date must satisfy: policy commencement date  <= in force date < policy risk cessation date; Lapse Date, Lapse Reason, Termination Date, and Termination Reason must be empty |
| If Policy Risk Status is Terminated | Termination Date and Termination Reason must be set and must be the same as those of the main benefit; Termination Date must satisfy: policy commencement date  <= termination date  <= policy risk cessation date; In Force Date, Lapse Date, and Lapse Reason must be empty; If the original policy risk status is Terminated and the termination reason is claimed (i.e. Death claim, TPD claim, DD claim) or matured, you cannot modify Policy Risk Status, Termination Reason, and Termination Date of the policy; The risk status of any benefit cannot be Inforce |
| For an investment linked policy | The new Monthlyversary Due Date (MDD) must satisfy: New MDD must be the same as unit deduction rider next due date if unit deduction rider exists; New MDD  <= original MDD; New MDD = policy commencement date + n months, n must be an integer and n  >= 1 |

**When you update the benefit information:**

| Condition | System Action |
|---|---|
| If Risk Status is Lapsed | Lapse Date and Lapse Reason must be set and must be the same as those of the main benefit; Lapse Date must satisfy: benefit commencement date  <= lapse date  <= benefit risk cessation date; In Force Date, Termination Date, and Termination Reason must be empty; If policy lapse reason is Normal Lapse, the lapse reason of any lapsed benefit cannot be APL Lapse; if policy lapse reason is ILP Lapse, the lapse reason of all the lapsed benefits must be ILP Lapse; If policy is inforce, the lapse reason of any lapsed benefit cannot be APL Lapse or ILP Lapse |
| If Risk Status is Inforce | In Force Date must be set and must be the same as that of the main benefit; In Force Date must satisfy: benefit commencement date  <= in force date < benefit risk cessation date; Lapse Date, Lapse Reason, Termination Date, and Termination Reason must be empty; If the secondary benefit risk status is Inforce, the primary benefit risk status must be Inforce |
| If Risk Status is Terminated | Termination Date and Termination Reason must be set and must be the same as those of the main benefit; Termination Date must satisfy: benefit commencement date  <= termination date  <= benefit risk cessation date; In Force Date, Lapse Date, and Lapse Reason must be empty; If the original benefit risk status is Terminated and the termination reason is claimed (i.e. Death claim, TPD claim, DD claim) or matured, you cannot modify Risk Status, Termination Reason, and Termination Date of the benefit |

| Condition | System Action |
|---|---|
| Next Due Date can be changed only when the following conditions are satisfied | Premium status for the benefit is Regular or Premium waived; Payment frequency for the benefit is regular (not single premium); The policy does not have other pre-contract information at next due date |

| Condition | System Action |
|---|---|
| Next Due Date must satisfy the following conditions | Next due date = benefit commencement date + n  x  the month of payment frequency, n must be an integer (i.e. next due date must coincide with one of the due dates based on the existing payment frequency); New next due date  <= original next due date; Benefit commencement date  <= next due date  <= benefit premium end date; For a non-investment linked policy, the next due date of all inforce benefits must be the same; for an investment linked policy, the next due date of all inforce cash rider must be the same and the next due date of all inforce unit deduction rider must be the same |
| Bonus Due Date must satisfy the following conditions | New bonus due date  <= original bonus due date; New bonus due date = benefit commencement date + n year, and n must be an integer |

**When you click Submit:**

| Condition | System Action |
|---|---|
| The system saves modified policy and benefit information | Done |
| If original policy risk status is Lapsed and policy has PLD, and new policy risk status is Inforce | The system cancels PLD |
| If policy or benefit risk status is modified | The system updates the policy or benefit risk status change history accordingly |

| Condition | System Action |
|---|---|
| If the next due date is changed | The system recalculates the benefit premium information using the new next due date; The system updates policy year using the new next due date; The system updates the premium status |

| Original Premium Status | New Condition | System Action |
|---|---|---|
| Regular or Premium waived | New next due date = premium end date | The system updates the premium status to Fully paid up |
| Fully paid up | New next due date < paid up date | The system updates the premium status to Regular |
| Regular | Waiver start date  <= new next due date  <= waiver end date | The system updates the premium status to Premium waived |
| Premium waived | New next due date < waiver start date OR new next due date > waiver end date | If new next due date = premium end date, the system updates the premium status to Fully paid up. If new next due date < premium end date, the system updates the premium status to Regular |

| Condition | System Action |
|---|---|
| The system cancels the pre-contract payment frequency change if any | Done |
| The system updates the guarantee period start date of the benefit if needed | Done |
| The system regenerates renewal draw through the Extract Amount to Bill batch job | Done |
| The system records the user ID and transaction date | Done |
| For an investment linked policy, if Policy Risk Status is changed from Lapsed to Inforce | The system calculates and generates policy fee pending transaction from lapse date to inforce date; The system sets MDD to the inforce date; The system will not deduct the risk charge between the lapse date and the inforce date |

---

## Appendix: Component Rules

### Rules for Validity Date

Validity date is on item level, and used for interest computation, pro-rated computation, query/reports on when the transaction takes place, setting up the risk commencement date. The rules for validity date described below are specific to ILP products.

In regard to fund transaction, the pricing of the funds will be based on the validity date provided. When no price is available on the specified date, forward pricing will be applicable. Forward price refers to the next available price based on the given validity date.

**Backdate Access Right:**

CS Transaction will be considered as backdated transaction when the Validity Date is before the System Date (i.e., Validity Date < System Date). User will require a backdate access level to backdate a transaction when the price is already known.

This rule is applicable for all transactions which require fund transactions such as: Ad-hoc Top Up; Recurring Top Up; Ad-hoc Switch; Increase Sum Assured; Inclusion of Riders; Partial Withdrawal; Full Surrender; Free-Look; Change Investment Regular Premium.

**Backdate System Validation:**

When user clicks on the button on 'Policy Information UI' to proceed to the 'Policy Info Entry UI', System will carry out the following validations:

| Step | System Action |
|---|---|
| System checks if the validity date is before system date | If No, user may proceed to the Policy Info Entry UI; If Yes, go to next step |
| System checks if user has backdate access right | If No, system prompts error message to stop user from proceeding; If Yes, user may proceed to the Policy Info Entry UI |

**Update of Validity Date:**

| Condition | System Action |
|---|---|
| If the Collection Date is different from Validity Date | System will auto update the Validity Date to be equal to the collection date |
| NOTE: Collection Date refers to the date money has been collected and applied to the CS | Enforced |
| If the whole payment due is settled by off-setting with suspense account balance | Validity date will not be updated |

**Future Date:**

System will prompt a warning message if the date entered for the Validity date is actually later than the system date. User may still proceed after acknowledging the warning message.

---

### Rules for Gross Policy Values Calculation

This section describes the formulas for calculating the values used for gross policy values quotation of project (Bonus, Surrender Value, Maturity Benefit and Yield) for all participating traditional products, excluding annuities and unit linked products.

**Standard Input:**
- Field: Value
- Standard Output: Gross policy values

**Formula of the Fields in Policy Year Values:**

**1. Accumulated installment premium:**

| Condition | Calculation |
|---|---|
| If the premium payment frequency is single | Accumulated premiumK = single premium after discount |
| If the premium payment frequency is yearly | Accumulated premiumK = regular premium after discount  x  min(k, premium term) |
| If the premium payment frequency is half yearly | Accumulated premiumK = regular premium after discount  x  min(k, premium term)  x  2 |
| If the premium payment frequency is quarterly | Accumulated premiumK = regular premium after discount  x  min(k, premium term)  x  4 |
| If the premium payment frequency is half monthly | Accumulated premiumK = regular premium after discount  x  min(k, premium term)  x  12 |

**2. Accumulated annual premium:**

Accumulated premiumK = annual premium after discount  x  min(k, premium term)

**3. Survival benefit:**

SBK = survival benefit amount which is due in the kth policy year

**4. Accumulated survival benefit:**

| Condition | Calculation |
|---|---|
| If Survival Benefit Option 3 is selected | ASBK = SB1  x  (1 + i)^(k-1) + SB2  x  (1 + i)^(k-2) + ... + SB(k-1)  x  (1 + i) + SBk |
| Else | ASBK = 0 |

NOTE: Use the current applicable interest rate to calculate interest.

**5. Cash bonus:**

CBK = cash bonus amount which is due in the Kth policy year

**6. Accumulated cash bonus:**

| Condition | Calculation |
|---|---|
| If Cash Bonus Option 3 is selected | ACBK = CB1  x  (1 + i)^(k-1) + CB2  x  (1 + i)^(k-2) + ... + CB(k-1)  x  (1 + i) + CBk |
| Else | ACBK = 0 |

NOTE: Use the current applicable interest rate to calculate interest.

**7. Guarantee surrender value:**

GSVK = guaranteed SVK of basic SA

**8. Total surrender value:**

TSVK = ASBK (if option 3) + ACBK (if option 3) + GSVK + NGSVK

**9. Death benefit:**

DBK = DBSAK + ARBK + ASBK (if option 3) + ACBK (if option 3) + TBK on claim

Where DBk is Death Benefit at the end of the kth policy year; DBSAK is the Death claim SA at the end of the kth policy year.

**Calculation Rules of the field in Maturity Value for Regular Premium Benefit:**

**1. Sum assured (xx.x%):**

| Condition | Calculation |
|---|---|
| If the maturity benefit > initial sum assured | Sum assured = initial sum assured |
| If the maturity benefit  <= initial sum assured | Sum assured = maturity benefit |
| xx.x% = sum assured / initial sum assured | xx.x% rounds to the nearest 2 decimals |

**2. Accumulated bonus at YYYY:**

YYYY is the year of last bonus declared date (Next bonus due date - 1 year) from the inquiry date. For reversionary bonus benefit, accumulated bonus as at YYYY is the accumulated bonus at the inquiry date. It is recorded at policy benefit level.

**3. Projected bonus as from (YYYY +1) to ZZZZ:**

(YYYY + 1) is the year of next bonus declared date (next bonus due date); ZZZZ is the year of maturity date. Projected Bonus as from (YYYY +1) to ZZZZ = ARBn - current ARB. ARBn is the accumulated reversionary bonus at maturity date.

**4. Projected special maturity bonus (xx.x%):**

Projected special maturity bonus is the projected terminal bonus on maturity. xx.x% = TN factor / TB Unit Rate. Projected special maturity bonusn = (Accumulated Bonus as at YYYY + Projected Bonus as from (YYYY+1) to ZZZZ)  x  xx.x%. The projected special maturity bonus follows the rules of the terminal bonus.

**5. Projected additional maturity bonus:**

| Condition | Calculation |
|---|---|
| If the maturity benefit > initial sum assured | Projected additional maturity bonus = maturity benefit - initial sum assured |
| If the maturity benefit  <= initial sum assured | Projected additional maturity bonus = 0 |

**6. Projected gross maturity value:**

Projected gross maturity valuen = sum assured + accumulated bonus + projected bonus + projected special maturity bonus + projected additional maturity bonus

**7. Survival benefit as at DD/MM/YYYY:**

DD/MM/YYYY is the inquiry date of the projection. Survival benefit at DD/MM/YYYY is the accumulated survival benefit with interest at the inquiry date.

| Condition | Calculation |
|---|---|
| If Option 1 is selected | Survival benefit at DD/MM/YYYY = 0 |
| If Option 3 is selected | Survival benefit at DD/MM/YYYY = total balance of the survival benefit account at the inquiry date |

**8. Future survival benefits (due xxxx onwards):**

XXXX is the year of next survival benefit due date from the inquiry date of the projection. Future survival benefits (due XXXX onwards) is the accumulated survival benefit without interest from the XXXX to the maturity date. Suppose the XXXX is the mth policy year, the policy term is n year:

Future survival benefits (due XXXX onwards) = SBm  x  (1 + i)^(n-m) + SB(m+1)  x  (1 + i)^(n-m-1) + ... + SBn

Where SBj is the survival benefit amount due in the jth policy year.

**9. Projected interest earned on survival benefits:**

Projected interest earned on survival benefits is the interest of accumulated survival benefit from the next survival benefit due date to the maturity date.

| Condition | Calculation |
|---|---|
| For Survival Option 1 | Projected interest earned on survival benefits = 0 |
| For Survival Option 3 | Projected interest earned on survival benefits = ASBn - survival benefits at DD/MM/YYYY - future survival benefits (due XXXX onwards) |

**10. Projected amount payable at maturity:**

Projected amount payable at maturityn = projected gross maturity valuen + survival benefits at DD/MM/YYYY + future survival benefits (due XXXX onwards) + projected interest earned on survival benefits

**11. Projected maturity yield:**

| Field | Description |
|---|---|
| y | Projected maturity yield |
| SP | Single premium |
| AP | Annual premium |
| n | Policy term |
| m | Premium term |
| Projected GMV | Projected Gross Maturity Value |

NOTE: System uses the current initial SA to calculate Projected GMV from the commencement date based on the historical bonus rates and the last declared bonus rates for future calculation.

**Calculation Rules of the Fields in Maturity Value for Single Premium Benefit:**

**1. Projected bonus and terminal bonus:**

For reversionary bonus benefit, projected bonus and terminal bonus = projected accumulated reversionary bonus + projected terminal bonus on maturity.

**2. Projected gross maturity value:**

Projected gross maturity valuen = minimum guaranteed maturity benefitn + accumulated bonus as at YYYY (last declared) + projected bonus and terminal bonusn

---

### Payer/Payee Rules for Customer Service

When a CS alteration item results in collection or refund, system needs to identify the right payer/payee. The following table illustrates the types of insurance roles that may exist in a policy and the corresponding payer/payee.

**Existing Insurance Roles in a policy:**

| Roles Present | Premium Payer | Conditional Payer | Collateral Payer | Absolute Assignee | Trustee | Policyholder | Grantee | Collection Payee | Refund Payee of Premiums | Refund Payee of CS only |
|---|---|---|---|---|---|---|---|---|---|---|
| Policyholder only | [x] | | | | | [x] | | Policyholder | Policyholder | |
| Policyholder + Trustee | [x] | | | | [x] | [x] | | Policyholder | Trustee | |
| Policyholder + Absolute Assignee | [x] | | | [x] | | [x] | | Policyholder | Policyholder | |
| Policyholder + Collateral Assignee | [x] | | [x] | | | [x] | | Policyholder | Collateral Assignee | |
| Policyholder + Grantee | [x] | | | | | [x] | [x] | Policyholder | Policyholder | |
| Policyholder + Trustee + Absolute Assignee | [x] | | | [x] | [x] | | | Absolute Assignee | Absolute Assignee | |

NOTE: For bankruptcy cases, if the bankruptcy status is Yes, the Disbursement Payee (on Payment Requisition page) is set to Official Assignee by default, but finance user can change it.

When policy has Trustee, Assignee and Grantee, the priority will be assignee > trustee > grantee.

---

## INVARIANTS (Full Set)

**INVARIANT 1: CS application must be registered before any entry can occur**
- Checked at: CS Entry page access
- Effect if violated: Application not found; entry cannot proceed

**INVARIANT 2: Financial CS item approval must be performed by a user different from the data entry user**
- Checked at: CS Approval stage
- Effect if violated: Approval rejected; error message displayed

**INVARIANT 3: ILP partial withdrawal amount must be less than (TIV - policy loan - min remaining amount)**
- Checked at: ILP Partial Withdraw submission
- Effect if violated: Validation error; withdrawal not processed

**INVARIANT 4: Special Revival can only be performed once per policy lifetime**
- Checked at: Special Revival submission
- Effect if violated: Validation error; special revival rejected

**INVARIANT 5: Change Trustee cannot be performed on an assigned policy**
- Checked at: Change Trustee entry
- Effect if violated: Policy not eligible for trustee change (pre-check displayed)

**INVARIANT 6: Batch Application Cancellation cannot cancel an application that is currently locked by another user**
- Checked at: Batch Application Cancellation processing
- Effect if violated: Application skipped; processed in next batch run

**INVARIANT 7: Premium Holiday validity date cannot be a future date for ILP policies**
- Checked at: Set or Cancel Premium Holiday submission
- Effect if violated: Warning message displayed

**INVARIANT 8: CS application with unpaid collection cannot take effect**
- Checked at: CS Inforce processing
- Effect if violated: Application status remains Approved; alteration not yet effective

**INVARIANT 9: ILP fund switch validation -- closed fund must be within subscription period**
- Checked at: ILP Switch Fund Ad Hoc submission
- Effect if violated: Error message displayed; switch not processed

**INVARIANT 10: Full surrender ILP -- pending fund transactions must not block surrender**
- Checked at: ILP Full Surrender submission
- Effect if violated: Error message; surrender blocked pending transaction resolution

**INVARIANT 11: Change Payment Frequency -- ILP FDD/PDD alignment rule**
- Checked at: ILP Change Payment Frequency submission (Scenario 1)
- Effect if violated: System must NOT allow change; error message displayed
- Rule: If FDD is at new frequency due date but PDD is NOT at new frequency due date -> change NOT allowed

**INVARIANT 12: Surrender -- highest primary benefit GSV must be > 0**
- Checked at: Surrender submission
- Effect if violated: Error; surrender not processed

**INVARIANT 13: Normal Revival -- secondary benefit can only be revived if primary is also revived**
- Checked at: Normal Revival submission
- Effect if violated: Validation error; revival rejected

**INVARIANT 14: Change Payment Frequency -- ILP both FDD and PDD at new frequency -> allowed**
- Checked at: ILP Change Payment Frequency (Scenario 2)
- Rule: Both FDD and PDD at new frequency -> System allows change

**INVARIANT 15: Partial surrender  --  all waivers must be terminated together**
- Checked at: Surrender submission
- Effect if violated: Validation error; surrender not processed
- Rule: When surrendering main benefit or primary benefit, all attached waivers must be selected and terminated together

**INVARIANT 16: Change Payment Frequency  --  ILP Scenario 3 (same as Scenario 2)**
- Checked at: ILP Change Payment Frequency (Scenario 3)
- Rule: Both FDD and PDD at new frequency  ->  System allows change

**INVARIANT 17: ILP Change Payment Frequency  --  Scenarios 4 - 7 bucket filling rules**
- Checked at: ILP Change Payment Frequency (Scenarios 4 - 7)
- Scenario 4: Bucket filling = fill target premium first, then recurring top up  ->  System adjusts bucket filling due based on new frequency; collected premium not re-filled
- Scenario 5: Bucket filling = fill target premium and recurring top up together by proportionment  ->  System adjusts bucket filling due based on new frequency
- Scenario 6: Bucket filling = fill target premium first, then recurring top up; premium loading deducted from investment account  ->  Change takes effect on future due date (max of expense due and premium due)
- Scenario 7: Bucket filling = fill target premium and recurring top up together by proportionment; premium loading deducted from investment account  ->  Change takes effect on due date of first blank bucket with new frequency
