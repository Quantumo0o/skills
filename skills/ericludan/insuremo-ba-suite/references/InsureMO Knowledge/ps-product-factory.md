# InsureMO Platform Guide — Product Factory / LI Expert Designer Configuration
# Source: LIMO General Configuration Guide + LIMO Finance Configuration Guide + LIMO Claim Configuration Guide (V25.04)
# Menu: LI Expert Designer → General Configuration / Finance Configuration / Claim Configuration
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb.md instead
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"how do I configure X in the Product Factory / LI Expert Designer"** — menu paths, config parameters, field descriptions, allowed values, dependencies, and setup sequences.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for a product configuration gap
- Agent 6 is generating a **Config Runbook** for product factory parameters
- A BA needs to verify what **pre-configuration** is required before a product can be defined

---

## Module Structure

```
LI Expert Designer
│
├── General Configuration          ← Tenant-level master data, rates, accounts, codetables
│   ├── I.   General Configuration
│   │   ├── I.1  Codetable & Business Table
│   │   ├── I.2  Rate and Rounding Settings
│   │   ├── I.3  Account Management
│   │   └── I.4  Advanced Configuration Options
│   ├── II.  Business Configuration
│   │   ├── II.1 Annuity Option
│   │   ├── II.2 Workdays Setup
│   │   └── II.3 Basic Information
│   ├── III. Sales Configuration
│   │   ├── III.1 Sales Meta Data
│   │   └── III.2 Product Business Category
│   └── IV.  Audit Trail
│
├── Finance Configuration          ← GL, Fund, Tax
│   ├── I.   GL (General Ledger) Configuration
│   │   ├── I.1  Define GL Field
│   │   ├── I.2  Define GL Field Mapping
│   │   └── I.3  Set Accounting Rule
│   ├── II.  Fund Configuration
│   │   ├── II.1 Fund Basic (Fund Maintain + Fund Premium Limit)
│   │   ├── II.2 Fund Strategy (Strategy + Strategy Fund Rate + DCA Target Fund)
│   │   └── II.3 Fund Invest Scheme (Scheme + Scheme Detail)
│   └── III. Tax Configuration
│       ├── III.1 Tax Transaction
│       ├── III.2 Tax Condition
│       └── III.3 Tax Detail (Calculation Configure + Tax Rate + Tax Fee Map)
│
└── Claim Configuration            ← Liability, claim types, Accutor
    ├── 1.   Basic Data Setup
    ├── 2.   Claim Element Initialization
    ├── 3.   Product Claim Configuration
    └── 4.   Accutor Configuration
```

---

## Role Requirements

| Module | Edit Role |
|---|---|
| General Configuration | `LIProductGeneralcfgRole_edit_default` |
| Finance Configuration | `LIProductFinanceRole_edit_default` |
| Claim Configuration (edit) | `LIProductEditRole_default` or `LIClaimDefineRole_default` |

Without the edit role, all pages are **read-only**.

---

## Part 1 — General Configuration

### I.1 Codetable & Business Table

#### I.1.1 Dynamic Codetable
**Purpose:** Define tenant-level master data used across product configuration.
**Menu:** General Configuration → Codetable & Business Table → Dynamic Codetable
**DB table:** tenant-level codetables

**Key rules:**
- Codetable **list** is at platform level — tenant cannot add new codetables, only add values
- Only users with edit role can modify; others are read-only
- Can create from Business Table via 'New from Business Table' button

**Field reference:**

| Field | Description | Notes |
|---|---|---|
| Table Name | Name of the codetable | — |
| Table Description | Description of the codetable | — |
| Business Domain | Purpose of table | Options: Table for Claim Relativities / Common Code Table |
| Maintained By | Tenant or Platform | Tenant-maintained tables can edit description |
| Code | Code value | — |
| Description | Code description | — |

**Setup steps:**
1. Search existing codetables via filter (Maintained By: Tenant or Platform)
2. Click View → see data list under the codetable
3. To add code values: find target codetable → Edit → Add → input Code and Description → Save
4. Bulk add: Download template → fill in → Upload

#### I.1.2 Codetable Overwrite
**Purpose:** Override platform-level code descriptions at tenant level.
**Menu:** General Configuration → Codetable & Business Table → Codetable Overwrite

#### I.1.3 Business Table
**Purpose:** Define custom data tables that can also serve as data source for Dynamic Codetables.
**Menu:** General Configuration → Codetable & Business Table → Business Table

**Setup steps:**
1. Click New → enter table name → Save & Next
2. **Note: Table name cannot be modified after creation**
3. In 'Table Information' tab: add required columns (first two columns 'ID' and 'Code' are default)
4. Input required records

---

### I.2 Rate and Rounding Settings

#### I.2.1 Rounding Rule for Formula
**Purpose:** Configure rounding rules per formula, per product, or per currency. Overrides tenant default.
**Menu:** General Configuration → Rate and Rounding Settings → Rounding Rule for Formula
**DB table:** `t_rounding_config`

**Default rounding rule (when no formula-level rule defined):** Round, Precision 2 (except INR: round to nearest 5 cents, precision 6)

**Priority order:** Formula-level rule → Tenant-level rule → System default (Round, precision 2)

**Field reference:**

| Field | Allowed Values | Notes |
|---|---|---|
| Product | Any tenant product | Optional; if blank = applies to ALL products |
| Currency | All configured currencies | Optional; if blank = applies to all currencies |
| Rounding Type | Round / Trunc / Round up to 5 cent / Round up / Round down | See below |
| Precision Number | Any integer, including negative | Negative value = rounds to tens/hundreds place |
| Formula Category | — | See LIMO FMS and Ratetable Configuration Guide |
| Formula Name | Formula from formula list | e.g. CB_BY_UNIT, Extra_Premium |

**Rounding Type behaviour:**

| Type | Behaviour | Example (precision=2) |
|---|---|---|
| Round | Round to nearest | 2.156 → 2.16; 2.154 → 2.15 |
| Trunc | Remove decimals behind precision | 2.156 → 2.15; 2.154 → 2.15 |
| Round up to 5 cent | Round up to nearest 5 | 2.151 → 2.155; 2.156 → 2.160 |
| Round up | Always round up | 1.2 → 2; -1.2 → -2 |
| Round down | Always round down | 1.2 → 1; -1.2 → -1 |

**Negative precision example:** Precision = -2 means round to tens place (3126 → 3130)

#### I.2.2 Rounding Rule for Tenant
**Purpose:** Tenant-wide default rounding rule (applies when no formula-level rule exists).
**Menu:** General Configuration → Rate and Rounding Settings → Rounding Rule for Tenant
**DB table:** Ratetable `Default Rounding Configuration`
**Note:** After definition, ratetable must be **deployed** to target environment.

#### I.2.3 Service Rate
**Purpose:** Define interest rates for different rate types used across financial transactions.
**Menu:** General Configuration → Rate and Rounding Settings → Service Rate
**DB table:** `t_service_rate`

**Key rule:** System always uses the **latest effective rate** on or before the interest settlement date. If Product field is blank, rate applies to ALL products except those with separate definitions.

**Available Rate Types** (defined in `T_SERVICE_RATE_TYPE` by LIMO staff; tenant cannot modify):

| Rate Type | Usage |
|---|---|
| APL | Automatic Policy Loan interest |
| Death Claim Interest | Delay payment interest on death claim |
| Claim Settlement Interest Rate | Interest on installment death benefit payments |
| Prepayment Account | — |
| Lump Sum Prepayment Account | — |
| Deposit Interest | — |
| Shareholder fund interest | — |
| Policy Loan (Yearly) | Policy loan interest (yearly basis) |
| Cash Bonus | CB account interest |
| Outstanding Premium Interest Rate | Interest on overdue premiums |
| Backdating/Overdue Premium | — |
| APA (Advance Premium Account) | — |

**Field reference:**

| Field | Description | Notes |
|---|---|---|
| Rate Type | Type of interest rate | Platform-defined list; tenant cannot modify |
| Rate Effective Date | Date from which rate applies | System uses latest available on settlement date |
| Product | Specific product (optional) | If blank = all products |
| Currency | Currency (optional) | — |
| Rate | Rate value (%) | — |

#### I.2.4 CPI Rate
**Purpose:** Define Consumer Price Index rate for indexation-type products.
**Menu:** General Configuration → Rate and Rounding Settings → CPI Rate
**Used by:** Product Configuration → Product Detail → NB Rules → Indexation Info (when Indexation Type = CPI)

**Field reference:**

| Field | Description |
|---|---|
| Effective Date | Date from which CPI rate applies |
| Rate (%) | CPI rate percentage |

---

### I.3 Account Management

#### I.3.1 Policy Account Type
**Purpose:** Configure policy-level or coverage-level financial accounts (APL, PL, CB, SB, etc.)
**Menu:** General Configuration → Account Management → Policy Account Type

**Field reference:**

| Field | Allowed Values | Description |
|---|---|---|
| Account Type | APL / PL / CB / SB / etc. | Code for the account type |
| Account Name | Free text | Display name |
| Rate Type | From Service Rate → `T_SERVICE_RATE_TYPE` | Interest rate type for this account |
| Main Type | Loan / Deposit | Classification |
| Interest Calculation Type | Compound Interest / Simple Interest | — |
| Interest Calculation Method | Compound: `i=p*[(1+r)^(d/365)-1]` / Simple: `i=p*r*(d/365)` or `i=p*[(1+r)^(1/12)-1]*(d/md)` | Only when Compound or Simple selected |
| Interest Frequency | Not Relevant / Yearly / Half Yearly / Quarterly / Monthly / Single / Daily | Settlement frequency |
| Interest Calculation Due Type | Calendar End / Policy / Account Creation Date / Calendar Begin | Start date for interest settlement |
| Capitalization Frequency | Not Relevant / Yearly / Half Yearly / Quarterly / Monthly / Single / Daily | — |
| Capitalization Due Type | Calendar End / Policy / Account Creation Date / Calendar Begin | Start date for capitalization |
| Calendar Date | Day of month (integer) | Only relevant when Due Type = Calendar Begin |
| First Deduct From | Interest / Principle | On withdrawal/repayment: deduct interest first (most cases) |
| Account Level | Policy / Coverage | — |
| Rate Date Type | Interest Rate Due Date / Account Creation Date | Which point-in-time rate to use |

**Interest formulas:**
- Simple Interest: `I = P × R × (D/365)`
- Compound Interest: `I = P × [(1+R)^(D/365) - 1]`
where P = principal, R = annual rate, D = number of accrual days (startDate inclusive, endDate exclusive)

**Capitalization note:** For compound interest, interest is immediately added to principal after calculation. For simple interest, calculated interest is stored in `policyAccount.uncapitalizedInterest` until the capitalization date.

**API note:** Capitalization triggered by `/magneto/rest/policy/policyaccount/interest/settlement` API, typically called by scheduled batch or triggered by online transactions (e.g. loan repayment) on the capitalization date.

#### I.3.2 Invest Virtual Account Define
**Purpose:** Define virtual accounts allowed for ILP products.
**Menu:** General Configuration → Account Management → Invest Virtual Account Define
**Used by:** Product Configuration → Product Detail → ILP → Virtual Account → Product Allowed Virtual Account

**Field reference:**

| Field | Description |
|---|---|
| Account Code | Unique code for virtual account |
| Account Name | Name of virtual account |
| Account Description | Optional description |

#### I.3.3 Risk Aggregation Type
**Purpose:** Define risk types available for products.
**Menu:** General Configuration → Account Management → Risk Aggregation Type
**Used by:** Product Configuration → Product Definition → Product → Common Servicing Rules → Product Risk Aggregation
**Note:** Only **Enabled** risk types appear in the product configuration dropdown.

**Field reference:**

| Field | Description |
|---|---|
| ID | Unique ID for the risk type |
| Risk Aggregation Type Name | Name (description auto-matches name on creation, but editable) |

---

### I.4 Advanced Configuration Options

#### I.4.1 Entity Extended Fields Define
**Purpose:** Add custom extended fields to Fund, Liability, Accutor, or Liability & Bill Item entities.
**Menu:** General Configuration → Advanced Configuration Options → Entity Extended Fields Define

**Supported entities:**

| Entity Name (API value) | Display |
|---|---|
| `T_FUND` | Fund |
| `T_LIABILITY` | Liability |
| `T_ACCUTOR` | Accutor |
| `T_LIABILITY_MEDICAL_BILL` | Liability & Bill Item Relation |

**Field reference:**

| Field | Allowed Values | Description |
|---|---|---|
| Entity Name | T_FUND / T_LIABILITY / T_ACCUTOR / T_LIABILITY_MEDICAL_BILL | Target entity |
| Field Name for API | Alphanumeric | Used in API calls |
| Field Label | Free text | Display label on UI |
| Data Type | Integer / Decimal / String / Boolean / Date / Text | — |
| Is Codetable | Yes / No | Only visible when Data Type = String |
| Tenant / Platform Codetable | Codetable reference | Only visible when Is Codetable = Yes |
| Default Value | Depends on Data Type | Optional |
| Field Order | Integer | Controls display order; lower number = displayed first |

**Note:** A field can only be edited when it is **Enabled**. Disabled fields are locked.

#### I.4.2 Tenant Skin Export
**Purpose:** Export tenant-level configuration for reuse across similar tenants.
**Role required:** `LITenantSkinRole_export_default`

#### I.4.3 Tenant Skin Import
**Purpose:** Import previously exported tenant configuration.
**Role required:** `LITenantSkinRole_import_default`

#### I.4.4 Translations Management
**Purpose:** Manage multi-language translations for UI labels.
**Note:** The following items do NOT support multi-language (one language only):
- Extended fields and their help text
- Records in Dynamic Codetable
- Tenant records in Liability Type, Fund, Risk Aggregation Type pages
- Extended pages with data table type
**Note:** After importing translations, users must **re-login** to apply.

---

### II.1 Annuity Option
**Purpose:** Define annuity payout options available for annuity products.
**Menu:** General Configuration → Business Configuration → Annuity Option
**Used by:** Product Configuration → Servicing Rules → Annuity Servicing Rules → Product Annuity Option → Allowed Annuity Option
**DB table:** `t_product_annuity_option`

**Field reference:**

| Field | Allowed Values | Description |
|---|---|---|
| Annuity Option | Free text | Option code |
| Market Name | Free text | Market name |
| Chinese Name | Free text | Chinese name |
| Annuitant Type | Single life / Joint life | — |
| Guaranteed Payment | Yes / N/A / No | Whether guaranteed period exists |
| Increase Percentage | % | Rate for increasing annuity calculation |
| Years No | Integer | Interval in years for each increase |
| Guaranteed Period Type | For a certain year / Up to a certain age / For whole life | — |
| Guaranteed Period | Integer | Specific value (years or age) — used with Guaranteed Period Type |
| Annuity Installment Period Type | For a certain year / Up to a certain age / For whole life | — |
| Annuity Installment Period | Integer | Specific value — used with Annuity Installment Period Type |
| Guaranteed Refund Rate | % | e.g. 125% on premium, 100% on cash value |
| Guaranteed Refund Basis | Cash Value / Single Premium | Basis for guaranteed refund rate |
| CI Addition Rule | CI addition / null | Special rule for CI annuity option |
| Annuity Payment Percentage | % | Percentage of normal annuity payment during CI addition |
| Max Number | Integer (months) | Max months for the CI addition percentage |
| Either One Death Discount | % | Discount on joint annuity payment when either annuitant dies |

---

### II.2 Workdays Setup
**Purpose:** Define public holidays and working days per country for date calculation.
**Menu:** General Configuration → Business Configuration → Workdays Setup
**Note:** Only **one country** can be defined per tenant.

**Field reference:**

| Field | Description |
|---|---|
| Workdays Reference | Country to configure (contact LIMO team if country not available) |
| Year/Month | Year and month to configure |

---

### II.3 Basic Information
**Purpose:** Configure tenant-level date format and default currency.
**Menu:** General Configuration → Business Configuration → Basic Information

**Field reference:**

| Field | Allowed Values | Description |
|---|---|---|
| Data Transfer Date Format | `yyyy-MM-dd'T'HH:mm:ss.SSSXX` / `yyyy-MM-dd'T'HH:mm:ss` | Date format for data transfer |
| Default Currency | Read-only | Tenant currency; cannot be edited |

---

### III.1 Sales Meta Data

#### III.1.1 Sales Category
**Purpose:** Define product sales categories for reporting and classification.
**Menu:** General Configuration → Sales Configuration → Sales Meta Data → Sales Category
**DB table:** `t_sales_type`

**Field reference:**

| Field | Description | Notes |
|---|---|---|
| Type Code | Sales category code | — |
| Type Name | Sales category name | — |
| Benefit Type Mapping | Maps to product benefit type | Options: N/A / Endowment / Annuity / Whole Life / Term / Mortgage / PayCare & Pure Endowment / Living Assurance / Reimbursement(bill) / Cash Benefit / Accident / Investment Product / Variable Annuity / Hybrid / Smart Saver / Hospital Benefit / Dread Disease / Others |
| Display Order | Integer | Controls display order in lists |

#### III.1.2 Agent Qualification Type
**Purpose:** Define qualification types required to sell specific products.
**Menu:** General Configuration → Sales Configuration → Sales Meta Data → Agent Qualification Type
**DB table:** `t_test_type`
**Used by:** Product Configuration (link product → qualification type); Sales Channel Management (link agent → qualification type)

**Note:** If a product requires qualification type 'Health', agents without 'Health' qualification cannot sell that product.

---

### III.2 Product Business Category
**Purpose:** Define detailed product categories for reporting, valuation, finance, etc.
**Menu:** General Configuration → Sales Configuration → Product Business Category
**DB table:** `t_prod_biz_category`
**Used by:** Product Configuration → Main and Sales Information → Sales Information → Operation Category

**Field reference:**

| Field | Description | Notes |
|---|---|---|
| Category ID | Unique ID | Must be unique |
| Category Code | Unique code | Must be unique |
| Is Parent | Yes / No | If No, must select Category Parent |
| Category Parent | Reference to parent category | Only when Is Parent = No |
| Category Name | Display name | — |
| Category Description | Optional description | — |

---

### IV. Audit Trail
**Purpose:** Track all changes to product configuration during the product configuration period.
**Menu:** General Configuration → Audit Trail

**Tracked actions:** Add / Edit / Delete for: Product Info, Formula Parameter, Formula, Ratetable, Service Rate

**Field reference:**

| Field | Options | Description |
|---|---|---|
| Sub System | Formula / Foundation / Product Management | Source system of the change |
| Object Type | PARAM_ID / FORMULA_ID / RATETABLE_CODE / PRODUCT_ID / RATE_ID | Type of object changed |
| Transaction Type | Edit formula parameter / Edit formula / Update Ratetable / Product Management / Create Product / Update service rate / Delete service rate | Type of action |

---

## Part 2 — Finance Configuration

### I. GL (General Ledger) Configuration

#### Overview
GL configuration defines the fields, field mappings, and accounting rules for posting financial events to the General Ledger. When events such as NB inforce or ILP fund changes occur, the system automatically creates records in `t_gl_details` and can integrate with external financial systems.

**GL posting is triggered** when:
- `POST_TO_GL` = 'Y' in `t_fee_type`, OR
- `CAPITAL_POST_GL` or `FUND_POST_GL` = 'Y' in `t_capital_distri_type`

**Fee Tables (GL modules):**

| TABLE_CODE | TABLE_NAME | Accounting Rule Type | Usage |
|---|---|---|---|
| 1 | V_CASH | CASH | Cash flow records |
| 2 | V_FUND_CASH | UNIT | Fund cash (ILP) |
| 3 | V_COMMISSION_FEE | COMMISSION | Commission |
| 4 | V_PREM_ARAP | ARAP | Accounts Receivable & Payable |
| 5 | V_CAPITAL_DISTRIBUTE | NONUNIT | Capital distribution |
| 6 | V_RI_FEE | REINSURANCE | Reinsurance fee |
| 7 | V_OFFSET_DETAIL | — | Reversal records |

#### I.1 Define GL Field
**Purpose:** Define custom GL posting fields per Fee Table.
**Menu:** Finance Configuration → GL Configuration → Define GL Field
**Note:** GL field creation and modification is a **project initiation phase** activity; requires developer implementation of field logic after creation.

**Field reference:**

| Field | Allowed Values | Description |
|---|---|---|
| Fee Table | From `t_arap_table` | GL module (platform codetable; tenant cannot modify) |
| Field Type | Pre-defined / Customized | Pre-defined: value from existing posting data. Customized: requires custom dev. |
| Field Name | Free text | Used in GL Field Mapping and Accounting Rule pages |
| Field Property | Free text | For developer implementation reference |
| Code Table | DB codetable | Used for dropdown in accounting rule |
| Where Clause | SQL clause | Filter criteria for code table values (e.g. `JE_CATEGORY_ID in (1,2)`) |
| Length | Integer | Max length of field value |
| Default Value | Depends on field | Optional default |

**Available DB Code Tables for GL Field:**

| DB Table | Display Name |
|---|---|
| `t_arap_table` | Fee Table |
| `t_journal_category` | JE Category |
| `t_fee_type` | FEE TYPE |
| `t_capital_distri_type` | Distribute Type |
| `t_fee_status` | Fee Status |
| `t_company_organ` | Company Id / Third Level Organization Id |
| `t_bank_account` | Bank Account NO |
| `t_money` | Currency |
| `t_pay_mode` | Payment Method |
| `t_withdraw_type_category` | Payment Type |
| `t_yes_no` | Product Indicator |
| `t_ins_type` | Main or Rider |
| `t_claim_type` | Claim Type |
| `t_policy_account_type` | Deposit or Loan Type |
| `t_prod_biz_category` | Product Category |
| `t_fee_source` | Capital Source |

#### I.2 Define GL Field Mapping
**Purpose:** Map GL Attribute Names (system-defined slots like filter1, base1) to GL Field Names per Fee Table.
**Menu:** Finance Configuration → GL Configuration → Define GL Field Mapping

**Attribute Types:**

| Attribute Type | Description |
|---|---|
| All | All field types |
| Base | Normal type |
| Filter | Normal type |
| Group | — |
| Cr_Seg | Credit record |
| Dr_Seg | Debit record |

**Attribute Name slots:**
- `base1–base10`, `filter1–filter10`, `grp1–grp10`, `crSeg1–crSeg20`, `drSeg1–drSeg10`

**Sample mapping (reference):**

| Attribute Name | V_CASH | V_FUND_CASH | V_PREM_ARAP | V_CAPITAL_DISTRIBUTE |
|---|---|---|---|---|
| base1 | JE Category | JE Category | JE Category | JE Category |
| base2 | FEE TYPE | Distribute type | Fee Type | Distribute Type |
| filter1 | Company Id | Company Id | Company Id | Company Id |
| filter2 | Currency | Currency | — | — |
| filter3 | Bank Account NO | Capital Source | Product Indicator | — |
| filter5 | Payment Method | Main or Rider | Product indicator | — |
| filter6 | Payment Type | Policy Year | Claim Type | — |

#### I.3 Set Accounting Rule
**Purpose:** Define accounting rules for each event type per fee table — determines how fees are posted to GL.
**Menu:** Finance Configuration → GL Configuration → Set Accounting Rule

**Accounting Rule Type scenarios:**

| Product | Event | Accounting Rule Types Used |
|---|---|---|
| Whole Life | NB / Increase SA / Free-look | Cash ×2, ARAP ×2, Offset ×2 |
| ILP | NB / Recurring Top-up / Single Top-up | Cash ×2, ARAP ×6, Offset ×6, Fund Cash ×30 |

**Whole Life fee types used:**

| Fee Table | Fee Type |
|---|---|
| V_CASH | 11-Receipt - Collection |
| V_CASH | 32-Actual Payment |
| V_PREM_ARAP | 41-Premium Application |
| V_PREM_ARAP | 42-Refund - Premium |

**ILP fee types used:**

| Fee Table | Fee Type |
|---|---|
| V_CASH | 11-Receipt - Collection |
| V_PREM_ARAP | 41-Premium Application |
| V_PREM_ARAP | 69-Top Up Premium |
| V_PREM_ARAP | 569-Regular Top Up Premium |
| V_FUND_CASH | 1-Net Investment Premium |
| V_FUND_CASH | 3-Single Top Up Net Investment Premium |
| V_FUND_CASH | 53-Regular Top Up Net Investment Premium |
| V_FUND_CASH | 64-Bid/Offer Spread |
| V_FUND_CASH | 97-Transfer to Unallocated Money (without price) |
| V_FUND_CASH | 98-Transfer to Fund Manager (with price) |
| V_FUND_CASH | 99-Recover from Fund Manager (with price) |

---

### II. Fund Configuration

#### II.1.1 Fund Maintain
**Purpose:** Define all investment funds available under the tenant. All funds must be defined here before they can be selected in product configuration.
**Menu:** Finance Configuration → Fund Configuration → Fund Basic → Fund Maintain
**DB table:** `t_fund`
**Note:** Extended fields can be added via Entity Extended Fields Define (General Configuration → I.4.1)

**Field reference:**

| Field | Allowed Values | Description |
|---|---|---|
| Fund Code | Max 20 chars | Unique identifier per tenant |
| Fund Name | Free text | e.g. "DWS Invest European Equities" |
| Fund Type | Cumulated Interest Type / Open Fund / Close Fund | — |
| Fund Status | Active / Closed End / Close Fund Terminated / Withdrawn | Active = default on creation |
| Start Date | Date | Mandatory |
| End Date | Date | Optional; update when fund reaches end |
| Price Frequency | Annual / Half Yearly / Monthly / IDL / Others / etc. | Declaration frequency |
| Tolerance Level | % | Fund price tolerance; displayed in Fund Price Entry for info only |
| Bid of Spread Rate | % | `Offer Price = (Bid Price × 1000 / (1 - Spread Rate)) / 1000` |
| Fund Sub Type | Money Market / Bond / Stock (Open Fund); Close Fund (Close Fund); Cumulated Interest Type (CIT) | Sub-classification |
| Dividend Indicator | Yes / No | If Yes: Coupon Option must be selected at NB |
| Price Waiting Days | Integer | T+N rule for fund price capture |
| Is Work Day | Yes / No | Whether Price Waiting Days = working days (Yes) or calendar days (No) |
| Price Factor | Decimal | `Fund Price = Latest Price × (1 + Price Factor)` |
| Cut Off Time (HHmmss) | Time | Before cut-off: use Day T price; after cut-off: use Day T+1 price |
| Workdays Reference | Country | Which country's workday calendar to use |
| ISIN Number | Free text | International Securities Identification Number |
| Fund Currency | Currency | Can differ from Policy Currency |
| Entity Fund | Entity reference | For financial use only |
| Min partial withdrawal amount | Amount | Fund-level limit; applies regardless of product |
| Min remaining amount after partial withdraw | Amount | Fund-level limit |
| Min Switch-out Amount | Amount | Fund-level limit |
| Min Remaining Amount after Switch-out | Amount | Fund-level limit |
| Unit period for No. of switches | NA / Year / Half-Year / Quarter / Month / Day | Period for switch count limits |
| No. of Switch-in per Period | Integer | Max switch-in count per period |
| No. of Switch-out per Period | Integer | Max switch-out count per period |

**Close Fund specific fields:**

| Field | Description |
|---|---|
| Subscription Start Date / End Date | Period during which units are invested in Money Market Fund |
| Pre Invest Days | Days before Close Fund Start Date for pre-investment. If 0 = no pre-investment period |
| Min / Max Subscription Amount | Amount limits for switching from Money Market Fund to Close Fund |

**Fund Status definitions:**
- **Active:** Default on creation
- **Closed End:** Fund has reached end date (Open Fund)
- **Close Fund Terminated:** Fund has reached end date (Close Fund only)
- **Withdrawn:** Fund withdrawn by insurer/fund house; no longer on sale

#### II.1.2 Fund Premium Limit Maintain
**Purpose:** Define fund-level premium limitations (initial, subsequent, top-up, switch amounts). System validates BOTH fund-level limits AND product-level fund limits.
**Menu:** Finance Configuration → Fund Configuration → Fund Basic → Fund Premium Limit Maintain
**DB table:** `t_fund_prem_limit`

**Field reference:**

| Field | Description | Validation behaviour |
|---|---|---|
| Fund Code | Select from Fund Maintain | — |
| Payment Method | Optional filter | e.g. Cash vs Credit Card can have different min limits |
| Payment Frequency | Optional filter | e.g. Monthly vs Yearly |
| Age Low / Age High | Optional filter | Age-based limits |
| Min / Max Initial Premium | Amount | Error if NB initial premium outside range |
| Min / Max Subsequent Premium | Amount | Error if subsequent premium outside range |
| Min Regular Premium Increment | Amount | Warning if increment < minimum |
| Min Regular Premium Decrement | Amount | Warning if decrement < minimum |
| Min Recurring Top-up Increment | Amount | Warning if increment < minimum |
| Min Recurring Top-up Decrement | Amount | Warning if decrement < minimum |
| Min Recurring Top-up | Amount | Warning if RSP amount < minimum |
| Min Adhoc Top-up | Amount | Warning if ad-hoc top-up < minimum |

---

### II.2 Fund Strategy

#### II.2.1 Strategy Maintain
**Purpose:** Define investment strategies (Auto Rebalancing or DCA). Must be created here before selecting in product configuration.
**Menu:** Finance Configuration → Fund Configuration → Fund Strategy → Strategy Maintain
**DB table:** `t_invest_strategy`
**Used by:** Product Configuration → ILP → Strategy Allowed Table → Allowed Strategy

**Field reference:**

| Field | Description | Notes |
|---|---|---|
| Strategy Code | Numeric only, max 50 chars | Unique identifier |
| Strategy Name | Free text | e.g. Stable Growth, Balanced, Dynamic |

#### II.2.2 Strategy Fund Rate Maintain
**Purpose:** Define investment allocation plan per strategy (Normal Strategy = Auto Rebalancing; DCA Strategy).
**Menu:** Finance Configuration → Fund Configuration → Fund Strategy → Strategy Fund Rate Maintain
**DB table:** `t_invest_strgy_rate`

**Validation rule:** For Normal Strategy: sum of allocation rates per same strategy + investment horizon + policy year range = 1 (100%)

**Field reference:**

| Field | Allowed Values | Description |
|---|---|---|
| Strategy | From Strategy Maintain | — |
| Strategy Type | Normal Strategy / DCA Strategy | See below |
| Investment Horizon | Integer | Only for Normal Strategy; reduces number of strategies needed |
| Low Policy Year / High Policy Year | Integer | Only for Normal Strategy; policy year range |
| Strategy DCA Type | DCA / Advanced DCA 1 / Advanced DCA 2 | Only for DCA Strategy |
| Strategy Frequency | Frequency | Only for DCA Strategy |
| Customize Indicator | YES / N/A / NO | If YES: customer can modify strategy at NB |
| Fund | Fund from tenant list | Target fund |
| Allocation Rate | Decimal (sum to 1) | Investment proportion |

**Strategy types:**
- **Normal Strategy (Auto Rebalancing):** Multiple funds, allocation by policy year range
- **DCA (Dollar Cost Averaging):** Fixed investment amount each time
- **Advanced DCA 1:** Variable amount based on fund price change (invest more when price drops)
- **Advanced DCA 2:** Variable amount based on difference between initial investment and TIV

**DCA Setup:** In Strategy Fund Rate Maintain, define only the initial fund (typically Money Market Fund) with allocation rate = 1. Target funds are defined in DCA Strategy Target Fund Maintain (II.2.3).

#### II.2.3 DCA Strategy Target Fund Maintain
**Purpose:** Define target funds for DCA Strategy and their allocation proportions.
**Menu:** Finance Configuration → Fund Configuration → Fund Strategy → DCA Strategy Target Fund Maintain
**DB table:** `t_strgy_target_fund`

**Field reference:**

| Field | Description |
|---|---|
| Strategy Code | DCA strategy from Strategy Maintain |
| Investment Horizon | Investment horizon (0 if not applicable) |
| Target Fund Code | Fund where DCA investment amount is switched into |
| Allocation Rate | Proportion per target fund (sum = 1 if multiple target funds) |

---

### II.3 Fund Invest Scheme

#### II.3.1 Invest Scheme
**Purpose:** Define investment schemes (groupings of funds with fixed allocation). Must be created here before product configuration.
**Menu:** Finance Configuration → Fund Configuration → Fund Invest Scheme → Invest Scheme
**DB table:** `t_invest_scheme`
**Used by:** Product Configuration → ILP → Invest Scheme Allowed → Allowed Invest Scheme

**Field reference:**

| Field | Description |
|---|---|
| Scheme Code | Numeric only, max 50 chars; unique |
| Scheme Name | e.g. Income, Balance, Dynamic |

#### II.3.2 Invest Scheme Detail
**Purpose:** Define fund allocation per investment scheme. Sum of all allocation rates per scheme must = 1.
**Menu:** Finance Configuration → Fund Configuration → Fund Invest Scheme → Invest Scheme Detail
**DB table:** `t_invest_scheme_detail`

**Field reference:**

| Field | Description |
|---|---|
| Scheme Code | Select from Invest Scheme |
| Fund Code | Select fund from tenant fund list |
| Percent Rate | Allocation proportion (sum = 1 across all funds in same scheme) |

---

### III. Tax Configuration

#### Tax Setup Sequence (required order)
When configuring a new tax type:
1. Tax Type and Sub-type (DB codetable update by LIMO IT staff)
2. Tax Transaction (III.1)
3. Tax Condition / Tax Deductible Criteria (III.2)
4. Tax Calculation Configure (III.3.1)
5. Tax Rate (III.3.2)
6. Tax Fee Map / Tax Payer (III.3.3)

**Note:** Tax Type and Sub-type are defined in `t_tax_type` and `t_tax_type_sub` by LIMO IT staff. Tenants request additions/modifications from LIMO team.

**Available Tax Types (standard):**

| Type Code | Type Name | Common Sub-types |
|---|---|---|
| 1 | GST | GST receivable / payable; Saving Plan FYP/Non-FYP; Unexpired Premium |
| 2 | Stamp Duty | Collection / receivable / payable / loan / main benefit / rider |
| 3 | Service Tax | Service Tax receivable / payable |
| 4 | Withholding Tax | Medical payment / Investment withdraw / Claim / Deposit / Interest |
| 10 | VAT | VAT |
| 11 | Stamp Tax | Policy inforce stamp tax |
| 12 | Premium Tax | Charge deduction |
| 13 | Levy | Levy |

#### III.1 Tax Transaction
**Purpose:** Map taxable scenarios (fee type + policy change event) to tax transaction codes.
**Menu:** Finance Configuration → Tax Configuration → Tax Transaction
**DB table / Rate table:** `Tax transaction map`

**Field reference:**

| Field | Description | Source table |
|---|---|---|
| Taxable Fee Category | Fee table of taxable fee | `t_fee_table`: T_CASH / T_PREM_ARAP / T_PRODUCT_COMMISSION / T_CLAIM_FEE / T_PAY_FEE |
| Taxable Fee Type | Fee type of taxable fee | `t_fee_type`, `t_capital_distri_type`, `t_commission_type` |
| Service Id | Policy change event | `t_service.service_id` (e.g. NB Inforce, Add Rider, APL Lapse) |
| Taxable Fee Status | Fee status | `t_cash.fee_status` / `t_prem_arap.fee_status` |
| Tax Transaction | Business scenario code | `t_tax_transaction.trans_code` (see below) |

**Tax Transaction codes:**

| Code | Scenario |
|---|---|
| 1 | Premium generate |
| 2 | Premium refund generate |
| 3 | Collection confirm |
| 4 | Premium confirm |
| 5 | Premium refund confirm |
| 6 | Policy loan generate |
| 7 | Medical payment generate |
| 8 | Investment withdraw generate |
| 9 | Claim payment generate |
| 10 | Deposit into account generate |
| 11 | Deposit interest generate |
| 12 | Total commission generate |
| 13 | Medical payment reverse |

#### III.2 Tax Condition
**Purpose:** Define criteria that determine when a tax applies (product category, party type, premium year, etc.)
**Menu:** Finance Configuration → Tax Configuration → Tax Condition
**Rate table:** `Tax condition`

**Field reference:**

| Field | Source / Options | Description |
|---|---|---|
| Tax Type | `t_tax_type.type_code` | — |
| Tax Type Sub | `t_tax_type_sub.sub_type_code` | — |
| Tax Transaction | Same as Tax Transaction field | — |
| Product Category | `t_benefit_type.benefit_type` | e.g. Endowment / Annuity / Whole Life / Term |
| Product Code | All tenant products | Specific product filter |
| Premium Year | Integer | Different criteria by premium/charge year |
| Party Type | `t_party_type.party_type` | e.g. Individual Customer / Doctor / Reinsurer |

#### III.3.1 Tax Calculation Configure
**Purpose:** Define how tax is calculated — formula, parameters, and currency method.
**Menu:** Finance Configuration → Tax Configuration → Tax Detail → Tax Calculation Configure
**Rate table:** `Tax calculation configure`

**Field reference:**

| Field | Allowed Values | Description |
|---|---|---|
| Tax Type | `t_tax_type.type_code` | — |
| Tax Type Sub | `t_tax_type_sub.sub_type_code` | — |
| Party Tax Indicator | YES / NO / Other | YES = only taxable if party's Taxable Indicator = Y |
| Tax Indicator | Exempt Rated / Rated / Zero Rated | `t_tax_indicator.indicator_code` |
| Tax Currency | 1 = base currency / 2 = follows taxable fee currency | `t_tax_currency_method.method_code` |
| Calculator Type | 1 = PL/SQL formula / 2 = Customized Spring Bean | Calculation method |
| Calculator | Formula ID (type 1) or Spring Bean name (type 2) | — |

#### III.3.2 Tax Rate
**Purpose:** Define tax rate or fixed amount per amount range and effective date.
**Menu:** Finance Configuration → Tax Configuration → Tax Detail → Tax Rate
**Rate table:** `Tax rate`

**Field reference:**

| Field | Description |
|---|---|
| Tax Type / Sub | From codetable |
| Tax Indicator | Same as Tax Calculation Configure |
| Taxable Amount Currency | Currency of taxable amount |
| Taxable Amount | Range of taxable amount (e.g. 0 ~ 9999999999999) |
| Effective Date | Rate effective date range |
| Rate | Tax rate (%) |
| Amount | Fixed tax amount (base currency) |

#### III.3.3 Tax Fee Map
**Purpose:** Define which party pays the tax — policyholder/payer or insurer.
**Menu:** Finance Configuration → Tax Configuration → Tax Detail → Tax Fee Map
**Rate table:** `Tax fee map`

**Field reference:**

| Field | Allowed Values | Description |
|---|---|---|
| Tax Type / Sub | From codetable | — |
| Tax Deduct Party | Payee / Insurer | Who bears the tax |
| Tax Fee Category | Same as Tax Transaction | Fee table of the tax |
| Tax Fee Type | All system fee types | Tax's fee type |

---

## Part 3 — Claim Configuration

**Menu:** LI Expert Designer → Claim Configuration
**Entry path:** `LI Expert Designer` → `Claim Configuration`

### 1. Basic Data Setup

#### 1.1 Claim Type
**Purpose:** Define claim types used as tabs in Auto Calculation Sequence and Notified Amount sections of the product liability page.
**Used by:** Product Configuration → Product Liability → Auto Calculation Sequence tab, Notified Amount tab

#### 1.2 Liability Category
**Purpose:** Group liabilities into categories.
**Used by:** Claim Type & Liability Category relationship (1.3)

#### 1.3 Claim Type & Liability Category
**Purpose:** Define the relationship between Claim Type (1.1) and Liability Category (1.2).
**Logic:** When liabilities are attached to a product → system looks up which Liability Category each liability belongs to → maps to Claim Type → those Claim Types appear as tabs in Auto Calculation Sequence and Notified Amount on the product liability page.

#### 1.4 Liability
**Purpose:** Configure all liabilities available for the tenant. Liabilities are used in product configuration via the Product Liability Table.
**Note:** Supports adding liability-level extended fields via Entity Extended Fields Define (General Configuration → I.4.1, Entity Name = T_LIABILITY)

#### 1.5 Medical Bill Group
**Purpose:** Group medical bill items.

#### 1.6 Medical Bill Item
**Purpose:** Configure medical bill items linked to liabilities. Each item includes: code, name, type, date-related indicator, and is-total indicator.

#### 1.7 Liability & Bill Item Relation
**Purpose:** Define the relationship between Liability (1.4) and Medical Bill Item (1.6).
**Also shown in:** Product Liability Table → hyperlink 'Medical Bill'

#### 1.8 Claim Global Setting Import
**Purpose:** Export and import basic data of claim configuration in bulk.

---

### 2. Claim Element Initialization

#### 2.1 Formula Parameter Initialization
**Purpose:** Define claim-related calculation parameters.
**Note:** Functionally similar to Parameter List, but category is fixed to 'XXX basic payment'.

#### 2.2 Claim Formula Initialization
**Purpose:** Define claim-related calculation formulas.
**Note:** Functionally similar to Formula List.

#### 2.3 Claim Relativity Initialization
**Purpose:** Configure claim relativities used in:
1. Product Liability Table → hyperlink 'Formula' → Relativity List
2. Accutor configuration → first step of selecting 'Claim Relativity'

#### 2.4 UI Factor Initialization
**Purpose:** Configure UI factors for claim evaluation.
**Used by:** Product Liability Table → hyperlink 'Factor' → dropdown list 'Factor'

---

### 3. Product Claim Configuration

**Note:** The following three menus are **not default menus** — they are enabled only for tenants that require claim configuration.

#### 3.1 Product List
Apply for tenants that only require claim configuration (non-default menu).

#### 3.2 Product Liability
Apply for tenants that only require claim configuration (non-default menu).

#### 3.3 Product Liability Query
Apply for tenants that only require claim configuration (non-default menu).

---

### 4. Accutor Configuration

#### 4.1 Accutor
Configure Accutor (claim calculation engine) rules.
**Used by:** Claim Relativity Initialization (2.3) → references Accutor

#### 4.2 Accutor Chain
Configure chains of Accutor calculation steps.

---

## Config Sequence — Dependency Order

The following sequence must be followed to avoid configuration errors. Items higher in the list must be configured before items that depend on them.

### General / Foundational (must be done first)
```
1.  Dynamic Codetable values         ← master data for all dropdowns
2.  Business Table                   ← if used as codetable source
3.  Workdays Setup                   ← required for date calculations
4.  Basic Information                ← tenant date format + currency
5.  Service Rate                     ← required before Policy Account Type
6.  Policy Account Type              ← APL, PL, CB accounts
7.  Risk Aggregation Type            ← before product Common Servicing Rules
8.  Sales Category                   ← before product Sales Information
9.  Agent Qualification Type         ← before product qualification requirements
10. Product Business Category        ← before product Operation Category
```

### ILP-specific (before product ILP configuration)
```
11. Fund Maintain                    ← all funds must exist before product fund selection
12. Fund Premium Limit Maintain      ← fund-level limits
13. Strategy Maintain                ← before Strategy Fund Rate
14. Strategy Fund Rate Maintain      ← allocation plan per strategy
15. DCA Strategy Target Fund Maintain ← for DCA strategies only
16. Invest Scheme + Scheme Detail    ← before product Invest Scheme Allowed
17. Invest Virtual Account Define    ← before product ILP Virtual Account
```

### Annuity-specific
```
18. Annuity Option                   ← before product Annuity Servicing Rules
```

### GL / Finance (project initiation phase)
```
19. Define GL Field                  ← requires developer implementation; project initiation only
20. Define GL Field Mapping          ← after GL Field
21. Set Accounting Rule              ← after GL Field Mapping
22. CPI Rate                         ← if Indexation Type = CPI used
23. Rounding Rule for Tenant         ← deploy ratetable after definition
24. Rounding Rule for Formula        ← overrides tenant rule per formula
```

### Tax (after Tax Type/Sub-type added by LIMO IT)
```
25. Tax Transaction                  ← taxable scenarios
26. Tax Condition                    ← deductible criteria
27. Tax Calculation Configure        ← calculation method
28. Tax Rate                         ← rate or fixed amount
29. Tax Fee Map                      ← who pays the tax
```

### Claim (before product liability configuration)
```
30. Claim Type                       ← tab labels
31. Liability Category               ← grouping
32. Claim Type & Liability Category  ← relationship mapping
33. Liability                        ← all liabilities for tenant
34. Medical Bill Group + Item        ← if medical billing required
35. Liability & Bill Item Relation   ← link liability to bill items
36. Formula Parameter Initialization ← claim calculation parameters
37. Claim Formula Initialization     ← claim formulas
38. Claim Relativity Initialization  ← claim relativity tables
39. UI Factor Initialization         ← claim UI factors
40. Accutor + Accutor Chain          ← claim calculation engine
```

---

## Common Config Gaps

| Scenario | Gap Type | Config Location |
|---|---|---|
| New fund to be added for ILP product | Config Gap | Finance → Fund Maintain |
| Fund switch limits not configured | Config Gap | Finance → Fund Maintain (switch fields) |
| Partial withdrawal minimum not enforced | Config Gap | Finance → Fund Premium Limit Maintain |
| RSP / top-up amount limits | Config Gap | Finance → Fund Premium Limit Maintain |
| New investment strategy required | Config Gap | Finance → Strategy Maintain + Strategy Fund Rate |
| DCA strategy required | Config Gap | Finance → Strategy Maintain (DCA type) + DCA Target Fund |
| Investment scheme for NB | Config Gap | Finance → Invest Scheme + Scheme Detail |
| Rounding difference in premium calculation | Config Gap | General → Rounding Rule for Formula |
| Indexation type = CPI | Config Gap | General → CPI Rate |
| New loan account type | Config Gap | General → Policy Account Type |
| Agent qualification gate for product | Config Gap | General → Agent Qualification Type + product config |
| New tax type required | Dev Gap (LIMO IT) | Tax Type/Sub-type added by LIMO IT → then Tax Transaction etc. |
| Existing tax rate change | Config Gap | Finance → Tax Rate |
| GL posting not generating records | Config Gap | Finance → Accounting Rule (check POST_TO_GL flag) |
| New liability for claim | Config Gap | Claim → Liability |
| Claim calculation formula | Config Gap | Claim → Claim Formula Initialization + Accutor |

---

## ⚠️ Limitations & Non-Configurable Items

> This section documents items that CANNOT be configured and require code changes. Updated: 2026-03-14

### Account & Interest Limitations

| Item | Limitation | Type | Notes |
|------|------------|------|-------|
| Account Types (APL/PL/CB/SB) | Predefined by LIMO, tenant cannot create new types | Code | Only can configure parameters |
| Interest Rate Types | Defined in `T_SERVICE_RATE_TYPE` by LIMO IT | Code | Cannot add new rate types |
| Interest Calculation Formulas | Fixed formulas (Simple/Compound) | Code | Custom formulas not supported |
| Policy Loan eligibility | Only Whole Life / Endowment | Code | ILP products excluded at code level |

### Fund & Investment Limitations

| Item | Limitation | Type | Notes |
|------|------------|------|-------|
| Fund creation | Requires LIMO IT involvement | Dev | New fund added to system |
| Investment strategy types | Predefined by LIMO | Code | Only can configure parameters |
| ILP virtual accounts | Limited to predefined types | Code | Check with LIMO |

### Tax & GL Limitations

| Item | Limitation | Type | Notes |
|------|------------|------|-------|
| New Tax Type | Requires LIMO IT to add to `T_TAX_TYPE` | Dev | Cannot configure new tax categories |
| New GL Account | Requires LIMO IT to extend GL chart | Dev | Cannot add new GL codes |
| GL Field Mapping | Limited to existing fields | Code | Custom fields need development |

### Product-Specific Limitations

| Item | Limitation | Type | Notes |
|------|------------|------|-------|
| Rider placement | Limited to certain product types | Code | Not all products support all riders |
| Annuity options | Configurable but limited by product type | Config | Check product specs |
| Claim calculation formulas | Some require Accutor customization | Dev | Standard formulas configurable |

---

## Related Files

| File | Purpose |
|---|---|
| `insuremo-ootb.md` | OOTB capability classification (use for Gap Analysis) |
| `ps-customer-service.md` | CS alteration item prerequisites and workflow config |
| `output-templates.md` | BSD output templates for configuration gaps |
