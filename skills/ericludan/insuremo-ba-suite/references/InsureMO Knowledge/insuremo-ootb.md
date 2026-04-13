# InsureMO OOTB Capability Reference (Pure)

> **Purpose**: Pure OOTB capability list — only what's available out of the box
> **Status**: ✅ OOTB only — Config/Dev gaps are identified during analysis, not pre-loaded
> **Modules Covered**: NB · UW · CS · Claim · Billing · Collection · Payment · Channel · Party · Global Query · Fund Admin · Investment · Annuity · Bonus/SB · Loan & Deposit Interest

---

## How to Use This Document

Use this document to verify if a client requirement is natively supported by InsureMO.

**Lookup process**:
1. Find the relevant module section (1–16)
2. If the requirement matches an ✅ OOTB item → confirmed supported
3. If not found → classify as Dev Gap (requires development)

**Gap Detection Rules** (separate document): See `insuremo-gap-detection-rules.md` for R1–R9 checklist.

---

## 1. Product Configuration Layer (Product Factory)

> Foundation configuration layer shared across all business modules.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Maximum insured age per product | ✅ OOTB | Product Configuration → Common Servicing Rules → Age Limit Table | Configurable per product independently |
| Rider-to-base policy binding | ✅ OOTB | Product Configuration →Relationshipmatrix | Relationship plus term limit table or product fomrula table |
| Coverage term auto-calculation | ✅ OOTB | Product Configuration  → Formula Config → Formula List / CS Calculation Item Config | Supports MIN/MAX formulas:Whole Life / Certain Years / Up to Certain Age / Months / Days |
| Multiple life assured support | ✅ OOTB | Product Configuration  → Common Servicing Rules → Age Limit Table | Joint Life、PH-LA Relationship（NB Rules → PH-LA Relationship |
| Premium term = coverage term | ✅ OOTB | Product Configuration  → Term Limit Table | Configurable |
| Multi-category product support | ✅ OOTB | Main and Sales Information → Main and Sales Information → Product Category / Operational Category | Term Life、ILP、VA、medical、endorment、health、mortgate、etc |
| Multi-product type unified modeling (Traditional / Annuity / Investment / Medical) | ✅ OOTB | Product Definition model + Magneto Policy/Proposal model | Unified product model & UI field template for multiple product types (Coverage Term, Premium Term, Fund, Annuity Period, etc.) |
| Charge and fee configuration (including ILP fees) | ✅ OOTB | LIMO Product Definition Guide | Multiple Charge Code, Fee Source, Calculation Base, Charge Frequency, Deduct Order; as Product Charge Rule module |
| Product-level GL / tax configuration hook | ✅ OOTB | LIMO Finance Configuration | GL field mapping and tax/rate configuration by product |
| Product-Claim Liability configuration (Accutor / Liability) | ✅ OOTB | Claim Dev Docs | Product-Liability-Medical Bill Item mapping; Accutor limit and accumulation rule binding |
| Product-Channel / Product-Business Category mapping | ✅ OOTB | LIMO Configuration | Business Category and product-channel mapping |
| Multi-factor Age/SA/Premium Limit modeling | ✅ OOTB | IX.1 Age Limit Table, IX.2 Premium Limit Table, IX.4 Initial SA Limit Table | Configurable min/max by multiple dimensions including Age, SA, SA Factor, Payment Method, Frequency, Currency, MIP, Benefit Level; supports ILP with Min/Max Initial/Subsequent Premium, Regular/Ad-hoc Top-up, Increment/Decrement |
| Unified term modeling for coverage/premium/annuity/deferment/guarantee | ✅ OOTB | IX.3 Term Limit Table | Unified configuration for Coverage Period, Premium Payment Term, Deferred Period, Installment Period, Guarantee Period |
| Bonus & VA guarantee configuration | ✅ OOTB | VII. Bonus, V. Annuity | Supports multiple bonus types, distribution frequency and methods; VA guarantees (GMDB/GMAB/GMWB/GMIB) and their Roll-up/Step-up accumulation rules |
| Investment-linked product rules (fund/strategy/MPV/top-up/withdrawal) | ✅ OOTB | VI. ILP (12 sub-modules) | Covers Fund, Strategy, Invest Scheme, MPV, Virtual Account, Top-up & Withdrawal, Regular Withdrawal Limit, Recurring Top-up Frequency, Product Fund Limit, Fund Premium Limit, Charge List |
| NB rule configuration (age basis, PH-LA relationship, occupation, UW flags) | ✅ OOTB | X. NB Rules | Supports Age Basis (multiple birthday algorithms), PH-LA relationship control, Occupation Level, Standard Life Indicator, Fact Find Indicator, Manual UW Indicator, LAAR Indicator |
| Sales period & sales area control | ✅ OOTB | I.2 Sales Information | Controls sales period via Launch/Withdraw Date; supports Currency Allowed Table, Operational Category, Supported Sales Area, Sales Category Type |
| Product versioning & deployment (incl. tenant skin export/import) | ✅ OOTB | I.3 Product Version, Operation Guide: Product Deployment, General Configuration: Tenant Skin Export/Import | Product version management, cross-environment deployment, cross-tenant configuration replication; version control for Age Limit, Premium Limit, Liability, CS Rules, etc. |
| Configurable extended fields on product & limit tables (incl. runtime updatable) | ✅ OOTB | Product Structure Guide → Extended Element Define / Limit Extended Fields Define | Custom extended fields on product and limit tables (Age/SA/Premium/Term); supports data type, range, code table, Help Text, Runtime Update (editable in Operation UI); accessible via API |
| Claim evaluation parameter & UI factor configuration per product/liability | ✅ OOTB | Product Liability Table → Factor / Accutor / Medical Bill / Auto Calculation Sequence | Configurable Factor display, editability and default value in claim evaluation UI |

---

## 2. New Business (NB)

> Covers application data entry, validation, premium quotation, and policy submission.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Auto-calculated read-only fields | ✅ OOTB | UI Config → Field Rules | Supports trigger-based recalculation |
| Rider auto-add on main product selection | ✅ OOTB | NB Screen → Auto-Add Rules | — |
| OnChange / OnBlur trigger events | ✅ OOTB | UI Config → Event Triggers | Covers common interaction events |
| Field-level and page-level validation messages | ✅ OOTB | Validation Rules | — |
| Standard premium quotation | ✅ OOTB | NB → Premium Calculation Engine | — |
| Policyholder / life assured data entry | ✅ OOTB | NB → Party Section | Linked to Party module |
| Beneficiary setup (statutory / nominated) | ✅ OOTB | NB → Beneficiary Config | — |
| Multiple application draft management | ✅ OOTB | NB → Draft Management | — |
| Application submission and status tracking | ✅ OOTB | NB → Submission Workflow | — |
| Bank account capture for premium payment | ✅ OOTB | NB → Payment Info Section | — |
| Workflow & permission integration | ✅ OOTB | NB E2E API Flow | ES-based DataEntry Worklist; integrated with workflow engine |
| Multi-product type entry template | ✅ OOTB | NB User Guide | Differentiated UI for Traditional, Annuity, ILP |
| Declaration section loaded by product | ✅ OOTB | NB Dev Intro API 16 | Product-based declaration template (multi-language / version) |
| Initial premium integration with Finance Workbench | ✅ OOTB | Finance Dev Intro | Auto AR and billing; payment callback |
| Auto UW trigger and NB rollback | ✅ OOTB | UW Dev Intro | Auto NB → UW registration; rollback to data entry |

---

## 3. Underwriting (UW)

> Covers risk assessment, loading/exclusion, underwriting decisions, and referral-to-manual workflows.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Rule engine-driven auto-underwriting | ✅ OOTB | UW → Rule Engine | Supports multi-condition combinations |
| Straight-through processing (STP) path | ✅ OOTB | UW → STP Rules | Auto-approves cases meeting criteria |
| Referral-to-manual UW trigger rules | ✅ OOTB | UW → Referral Rules | Configurable per product / risk factor |
| Extra premium (loading) UW decision | ✅ OOTB | UW → Decision Config | — |
| Exclusion UW decision | ✅ OOTB | UW → Exclusion Config | — |
| Postpone / decline UW decision | ✅ OOTB | UW → Decision Config | — |
| Underwriting questionnaires (medical / financial disclosure) | ✅ OOTB | UW → Questionnaire Config | Question sets configurable per product |
| UW task queue and assignment | ✅ OOTB | UW → Task Queue | — |
| UW history and audit trail | ✅ OOTB | UW → Audit Log | — |
| Reinsurance cession rule trigger | ✅ OOTB | UW → Reinsurance Rules | Depends on RI config |
| Cross-module Risk Summary | ✅ OOTB | UW User Guide | Risk aggregation, USAR/TSAR, history query |
| Multi-source UW task unified workbench | ✅ OOTB | UW Worklist | Single workbench for NB/Claim/CS tasks |
| Letter / Issue management | ✅ OOTB | UW Docs | Auto issue generation; letter template |
| Risk permission control | ✅ OOTB | UW Dev Intro | Risk level calculation; underwriter authority |

---

## 4. Customer Service (CS)

> Covers policy alterations, reinstatement, servicing requests, and complaint handling.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| CS Registration (entry point for all alterations) | ✅ OOTB | CS → Registration | Entry point for all alteration types |
| CS Watch List (task release and reassignment) | ✅ OOTB | CS → Watch List | Task management and redistribution |
| CS Reversal (undo completed alterations) | ✅ OOTB | CS → Reversal | Post-inforce alteration reversal for eligible items |
| PS Quotation (pre-transaction quotation) | ✅ OOTB | CS → Policy Servicing Quotation | Pre-transaction quotation before alteration |
| FATCA Information maintenance | ✅ OOTB | CS → FATCA Information | FATCA compliance data management |
| Basic policy information change (address, contact) | ✅ OOTB | CS → Policy Alteration | — |
| Beneficiary change | ✅ OOTB | CS → Beneficiary Alteration | — |
| Payment method change | ✅ OOTB | CS → Payment Method Change | — |
| Coverage alteration (add / remove riders) | ✅ OOTB | CS → Coverage Alteration | Subject to product rules |
| Policy reinstatement | ✅ OOTB | CS → Reinstatement Workflow | Supports rule-based validation |
| Policy loan | ✅ OOTB | CS → Policy Loan | Depends on surrender value config |
| Partial / full surrender | ✅ OOTB | CS → Surrender Workflow | — |
| Policy document reissue | ✅ OOTB | CS → Document Reissue | — |
| Complaint recording and tracking | ✅ OOTB | CS → Complaint Management | — |
| Standard alteration workflow | ✅ OOTB | CS_Workflow | Configurable NeedUW/NeedApprove/NeedUWConfirm |
| CS Data Entry workbench | ✅ OOTB | CS → WorkList → Data Entry | Alteration item entry + Apply Change |
| CS Underwriting (auto-UW or manual UW routing) | ✅ OOTB | CS → UW | Routes to UW workbench if Need UW = Y |
| CS Approval (2nd-level approval workflow) | ✅ OOTB | CS → WorkList → Approve | Escalates if Need Approval = Y |
| CS In-Force (collection and effective date) | ✅ OOTB | CS → WorkList → Pending In Force | Alteration becomes effective |
| CS Query (search and view CS applications) | ✅ OOTB | CS → Query | Search and view CS applications |
| Unified AlterItem DTO model | ✅ OOTB | PA-BFF / PA-BS | Common structure for all alteration types |
| Integrated calculation with PD / Magneto / Dorami | ✅ OOTB | PA-BS | Product rule, interest/fund price, policy update |
| Alteration fee (ARAP) auto generation | ✅ OOTB | ARAP Fees, AdjustAuthority | Auto AR/AP; adjustment authority control |

---

## 5. Claims

> Covers FNOL, claim assessment, loss evaluation, claim decision, and claim payment.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| First notification of loss (FNOL) registration | ✅ OOTB | Claim → FNOL Registration | — |
| Claim task queue and assignment | ✅ OOTB | Claim → Task Queue | — |
| Claim document upload and management | ✅ OOTB | Claim → Document Management | — |
| Standard claim rule engine (auto-assessment) | ✅ OOTB | Claim → Rule Engine | — |
| Claim reserve management | ✅ OOTB | Claim → Reserve Management | — |
| Claim decision (approve / deny / partial) | ✅ OOTB | Claim → Decision Workflow | — |
| Reinsurance claim cession | ✅ OOTB | Claim → RI Claim Config | — |
| Claim payment instruction generation | ✅ OOTB | Claim → Payment Instruction | Linked to Payment module |
| Claim audit trail | ✅ OOTB | Claim → Audit Log | — |
| Complete claim process & data structure | ✅ OOTB | Claim tables | Full lifecycle; installment; premium/refund handling |
| Medical bill & summary adjustment | ✅ OOTB | Claim medical tables | Inpatient/outpatient bill adjustment |
| Claim authority & amount control | ✅ OOTB | Claim Authority | Approval hierarchy and audit history |
| Claim settlement integration with Finance | ✅ OOTB | Finance Dev Intro | Auto AP/AR and payment linkage |
| Fraud / Red Flag indicator | ✅ OOTB | Claim User Guide | Fraud tag and UW risk summary integration |

---

## 6. Billing

> Covers premium bill generation, bill adjustments, reconciliation, and billing notifications.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Auto bill generation (by payment frequency) | ✅ OOTB | Billing → Schedule Config | Supports monthly / quarterly / annual |
| Bill amount calculation (including riders) | ✅ OOTB | Billing → Calculation Engine | — |
| Bill adjustment (loading / refund) | ✅ OOTB | Billing → Adjustment Workflow | — |
| Billing notification config (email / SMS) | ✅ OOTB | Billing → Notice Config | — |
| Billing history query | ✅ OOTB | Billing → Query | — |
| Overdue bill flagging and grace period handling | ✅ OOTB | Billing → Grace Period Config | — |
| GL / tax configuration integration | ✅ OOTB | LIMO GL/Tax | Auto GL dimension and tax calculation |
| Unified ARAP Posting flow | ✅ OOTB | Finance Dev Intro | NB/CS/Claim unified posting with reversal |

---

## 7. Collection

> Covers overdue identification, dunning notices, grace period management, and pre-lapse handling.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Automatic overdue identification and flagging | ✅ OOTB | Collection → Overdue Rules | — |
| Grace period rule configuration | ✅ OOTB | Collection → Grace Period Config | Configurable per product |
| Multi-channel dunning notice auto-trigger | ✅ OOTB | Collection → Notice Workflow | — |
| Auto-lapse trigger on grace period expiry | ✅ OOTB | Collection → Lapse Trigger | — |
| Collection case record and status tracking | ✅ OOTB | Collection → Case Management | — |
| Bulk receipt upload & auto match | ✅ OOTB | Finance Dev Intro | Bank statement auto matching |
| Suspense management & transfer | ✅ OOTB | Finance Dev Intro | Suspense account and policy allocation |

---

## 8. Payment

> Covers premium receipting, refunds, claim disbursement, and multi-channel payment management.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Multiple payment method support (bank transfer / direct debit / credit card) | ✅ OOTB | Payment → Method Config | — |
| Payment instruction generation and status tracking | ✅ OOTB | Payment → Instruction Workflow | — |
| Payment reconciliation (bank receipt matching) | ✅ OOTB | Payment → Reconciliation | — |
| Refund processing | ✅ OOTB | Payment → Refund Workflow | — |
| Claim disbursement | ✅ OOTB | Payment → Claim Payment | Linked to Claim module |
| Payment failure retry rules | ✅ OOTB | Payment → Retry Config | — |
| Payment requisition & authorization | ✅ OOTB | Finance Dev Intro | Multi-level approval for large payments |
| Cash bank account configuration & routing | ✅ OOTB | Cash Bank APIs | Multi‑account routing by type/ccy/branch |

---

## 9. Channel

> Covers agent, broker, bancassurance, and direct channel management including commissions.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Agent profile management | ✅ OOTB | Channel → Agent Profile | — |
| Multi-level agent hierarchy | ✅ OOTB | Channel → Hierarchy Config | — |
| Product sales permission by agent level | ✅ OOTB | Channel → Product Permission | — |
| Commission rule configuration (first year / renewal) | ✅ OOTB | Channel → Commission Rules | — |
| Commission calculation and disbursement | ✅ OOTB | Channel → Commission Calculation | — |
| Agent performance reporting | ✅ OOTB | Channel → Performance Report | — |
| Channel-exclusive product configuration | ✅ OOTB | Channel → Exclusive Product Config | — |
| Product / sales configuration integration | ✅ OOTB | LIMO Sales | Channel/product/agent qualification |
| Commission rule & finance integration | ✅ OOTB | Finance ARAP | Commission in ARAP/GL; first/renewal/bonus |

---

## 10. Party

> Covers individual and corporate customer master data, KYC, and relationship management.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Individual customer profile (basic information) | ✅ OOTB | Party → Individual Profile | — |
| Corporate customer profile | ✅ OOTB | Party → Corporate Profile | — |
| Customer relationship management (family / corporate members) | ✅ OOTB | Party → Relationship Config | — |
| Cross-policy customer view (360° view) | ✅ OOTB | Party → Policy Summary View | — |
| Duplicate customer detection and merge | ✅ OOTB | Party → Deduplication Rules | — |
| Customer communication preference settings | ✅ OOTB | Party → Communication Preference | — |
| Internal blacklist / sanctions list check | ✅ OOTB | Party → Blacklist Config | — |
| KYC document upload and status management | ✅ OOTB | Party → KYC Document Management | — |
| 360° customer view | ✅ OOTB | Party module | Policy/UW/Claim/CS history aggregation |
| Relationship management (family / enterprise) | ✅ OOTB | — | Family and enterprise member modeling |

---

## 11. Global Query & Reporting

> Covers cross-module data queries, reporting, and data export.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Full-text policy search | ✅ OOTB | Global Query → Policy Search | — |
| Cross-module status query (NB / UW / CS / Claim) | ✅ OOTB | Global Query → Cross-Module View | — |
| Standard report library (built-in reports) | ✅ OOTB | Global Query → Standard Reports | — |
| Data export (CSV / Excel) | ✅ OOTB | Global Query → Export Config | — |
| Query access control (role-based) | ✅ OOTB | Global Query → Role Permission | — |
| Cross-workflow ES index query | ✅ OOTB | Module worklists | Role/branch/status filtering |
| Audit trace query | ✅ OOTB | Module Audit Log | Policy/customer/case audit aggregation |
---

## 12. Fund Administration (ILP)

> Covers ILP fund transaction processing, charge deduction, auto premium holiday, policy lapse mechanics, and post-lapse unit sell-down.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Perform Fund Transaction (Batch) — buy/sell based on pending transaction records | ✅ OOTB | — | Triggered by NB / CS / Loan / Maturity / Annuity / Claim upstream events |
| Fund transaction price selection — Validity Date logic; defers to next available price if unavailable | ✅ OOTB | — | Price Used Date = Validity Date or next available forward date |
| Bid-Offer spread auto-calculation on buy transactions | ✅ OOTB | — | `(Offer Price − Bid Price) × Units Transacted` |
| Fund holiday handling — auto-populates price for holiday dates when next working day price uploaded | ✅ OOTB | — | Fund-level holiday calendar |
| ILP Free Look — 3 refund options (Default / Refund Premium / Refund TIV+Charges) | ✅ OOTB | Product Factory → ILP Rules → Free Look Option | — |
| ILP Partial Withdrawal — 3-layer LIFO deduction order (Single Top-up → RSP → Regular Premium) | ✅ OOTB | — | Applies to both Dual Account and Single Account structures |
| ILP Partial Withdrawal — proportional cross-fund deduction within each layer | ✅ OOTB | — | `Fund A amount = (Fund A Value / Total Layer TIV) × Withdrawal amount` |
| ILP Partial Withdrawal — application suspended if insufficient units | ✅ OOTB | — | Status set to Suspend; no partial execution |
| ILP Fund Switch by Value / Units / Percentage | ✅ OOTB | — | Includes auto-switch-all if insufficient units for by-value switch |
| Deduct Charges (Batch) — daily COI / Policy Fee / FMF / Guaranteed Charge / Expense Charge | ✅ OOTB | — | Decision tree: TIV sufficient → deduct; within NLP → sell all + misc debts; outside NLP → calculate PLD |
| PLD (Potential Lapse Date) calculation and update on each charge deduction cycle | ✅ OOTB | — | 4-branch PLD logic: >MDD+60 / between MDD and NDD / NDD≤PLD≤MDD+60 / equal MDD |
| PJD (Projected Lapse Date) calculation and auto-clear when PLD is set | ✅ OOTB | — | `PJD = Charge Due Date + (TIV / sum of monthly charges)`; recorded only if <3 months from monthversary |
| NLG (Non-Lapse Guarantee) period — charge deduction continues as misc debts when TIV = 0 | ✅ OOTB | Product Definition → ILP Rules → NLG | Policy stays Inforce through NLGP even with zero TIV |
| COI for layered SA — captures COI rate at segment level for ILP SA increase tranches | ✅ OOTB | Product Definition → ILP Rules → Level Pay COI | — |
| Auto Premium Holiday (Batch) — sets APH when premium overdue, product allows APH, TIV sufficient | ✅ OOTB | Product Config → ILP Rules → Allow APH | Sequential checks: paid-up check → allow APH flag → remaining PH months → TIV sufficiency |
| Auto Premium Holiday — respects MIP (Minimum Investment Period) expiry before allowing APH | ✅ OOTB | Product Definition → ILP → Allowed Minimum Invest Periods | — |
| Auto Cancel Premium Holiday (Batch) — cancels APH and moves premium due date on PH end date | ✅ OOTB | — | — |
| APH cannot retrigger after being cancelled at max PH period end | ✅ OOTB | — | System invariant; blocks re-entry |
| ILP Policy Lapse (Batch) — validates PLD; lapses policy when system date ≥ PLD | ✅ OOTB | — | Prerequisite: Charge Deduction batch must have completed |
| ILP Policy Lapse — IUA→AUA transfer when product configured as Stay Inforce after max PH | ✅ OOTB | — | Transfer-out (withdrawal) + transfer-in (top-up) use same fund price; EEC fee deducted |
| ILP Policy Lapse Sell All Units (Batch) — sells remaining TIV after lapse waiting days; generates payable record | ✅ OOTB | Product Config → ILP → Waiting Days After Lapse | EEC deducted from withdrawal; net amount as payable |
| Fund transaction processing with pending records; cannot execute if policy frozen | ✅ OOTB | — | System invariant |

---

## 13. Investment (Fund Price & FX)

> Covers daily fund price maintenance, approval workflow, FX rate management, and fund holiday calendar.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Exchange Rate maintenance — manual entry and XLS/XLSX file upload | ✅ OOTB | Investment > Exchange Rate | — |
| Inverse rate auto-generation on exchange rate add / upload | ✅ OOTB | — | `Inverse Rate = Trunc(1 / rate, 5)` |
| Exchange rate precision rules — 6 DPs; last digit always 0; Buy ≤ Sell; Middle = (Buy+Sell)/2 | ✅ OOTB | — | — |
| Same-date re-upload overwrites original rate and inverse rate | ✅ OOTB | — | — |
| Fund Holiday management — add / delete / upload per fund | ✅ OOTB | Investment > Fund Holiday | CSV upload supported |
| Fund price entry — manual bid price + Offer Price and Variance auto-calculated | ✅ OOTB | Investment > Fund Price > Entry | XLS/XLSX upload supported; max 5 DPs |
| Fund price 4-status approval flow: Entered → Approved → Confirmed → Revised | ✅ OOTB | Investment > Fund Price > Approve / Revise | — |
| Fund Price Validate — identify unapproved prices in batch | ✅ OOTB | Investment > Fund Price > Approve | — |
| Fund Price Revise — original record marked Revised; new record re-enters Entered and re-approval | ✅ OOTB | Investment > Fund Price > Revise | Revision does NOT retroactively affect confirmed fund transactions |
| Auto-populate holiday/non-working day prices from next working day upload | ✅ OOTB | — | Viewable in Fund Price Query only |
| Fund Price Query — view all records regardless of status | ✅ OOTB | Query > Investment > Fund Price Query | — |
| Fund Factor Ratio (AFF) — actual transaction amount/unit = pending × funding factor | ✅ OOTB | Ratetable Config → FFrate table (by distri_type at product level) | Dual account: sub-account type (IUA/AUA) indicated; products without AFF treated as AFF=1 |

---

## 14. Annuity Payment

> Covers batch extraction, notice generation, and disbursement for annuity products.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Annuity Payable Execution (Weekly Batch) — extracts eligible policies; updates annuity plan; generates payable records | ✅ OOTB | — | Prerequisite: Policy Inforce + not frozen + next due date within advance days |
| Annuity Notice Generation (Daily Batch) — generates and prints annuity notices to policyholders | ✅ OOTB | — | Prerequisite: Payable Execution batch must have run for current cycle; no duplicate notice |
| Annuity Payout (Batch) — generates annuity payment records for eligible policies | ✅ OOTB | — | — |
| Annuity payable execution cannot proceed if policy frozen | ✅ OOTB | — | System invariant |

---

## 15. Bonus / Survival Benefit Allocation

> Covers Cash Bonus (CB), Reversionary Bonus (RB), and Survival Benefit (SB) batch allocation and cash disbursement.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| CB Allocation (Batch) — yearly cash bonus calculation and allocation; updates CB account and next due date | ✅ OOTB | — | Prerequisite: Inforce + not frozen + within advance days + CB rate found |
| CB Allocation — 3 payout options: Option 1 Cash Payout / Option 2 Pay Premium / Option 3 Leave on Deposit | ✅ OOTB | — | — |
| CB deferred if policy within 'No. of Completed Policy Years for CB Becoming Payable' | ✅ OOTB | Product Factory → CB Rules → Payable Year | Batch record generated in CS info; no allocation |
| CB/SB balance used to offset APL then PL before any payout or deposit action (all options) | ✅ OOTB | — | Offset order: CB account first → SB account; APL first → PL |
| RB Allocation (Batch) — accumulates reversionary bonus; updates Accumulated RB and next due date | ✅ OOTB | — | Must run on working day; non-working due dates shifted to next working day per holiday calendar |
| RB — missing year rate uses last declared year rate | ✅ OOTB | — | Applies when no rate declared for a specific policy year |
| RB — lapse / reinstatement gap allocation: all missing RB years re-allocated on reinstatement | ✅ OOTB | — | Missing year rates use last declared year's rate |
| RB — Interim Bonus on surrender / maturity / death claim (Regular / Fully Paid / Premium Waived only) | ✅ OOTB | Product Factory → Parameter List → Interim Bonus Adjusted Months | Formula hardcoded; parameter configurable |
| SB Allocation (Batch) — creates SB plan if absent; allocates SB amount; updates next payout date | ✅ OOTB | — | Final installment sets SB plan to Inactive |
| SB payout options: same Option 1 / 2 / 3 as CB | ✅ OOTB | — | — |
| SB/CB in Cash Payment (Batch) — executes cash disbursement for Option 1 policies | ✅ OOTB | — | Prerequisite: Allocation batch run + amount > 0 |
| Cancel SB/CB Cash Payment (Batch) — auto-cancels unconfirmed payment records after configured days; converts to deposit balance | ✅ OOTB | — | Once cancelled, cannot retrigger until next allocation cycle |
| CB/SB account interest — Simple or Compound; configurable frequency, due type, capitalization frequency | ✅ OOTB | Product Factory (LIMO) → Policy Account Rules | Same interest config dimensions as loan accounts |
| Excluded premium statuses from CB/SB/RB allocation — Reduced Paid Up / Auto Paid Up / ETA / PHD / Stop Payment | ✅ OOTB | — | System invariant |
| Disbursement method follows policy-level setting; blanks fall through to PayNow or manual requisition rules | ✅ OOTB | — | — |

---

## 16. Loan & Deposit Interest

> Covers interest settlement and capitalization for Policy Loan, APL, Cash Bonus, and Survival Benefit deposit accounts.

| Capability | Status | Config Path | Notes |
|---|---|---|---|
| Interest Settlement (Batch) — daily; calculates accrued interest since last settlement date per account | ✅ OOTB | — | Triggered: regular daily batch OR ad-hoc (CB/SB/APL/Loan repayment) |
| Interest Capitalization (Batch) — daily; adds accumulated interest to principal | ✅ OOTB | — | Capitalization is ONLY triggered by batch — never by ad-hoc actions |
| Simple Interest formula: `P × i × d / 365` | ✅ OOTB | — | — |
| Compound Interest formula: `P × [(1 + i) ^ (d/365) − 1]` | ✅ OOTB | — | — |
| Interest Rate Type — Creation Date: rate locked at account creation; never changes if rate table updated | ✅ OOTB | t_policy_account_type → Rate Type | — |
| Interest Rate Type — Due Date: rate looked up per segment between start/end date; splits on rate effective date | ✅ OOTB | t_policy_account_type → Rate Type | Formula: `P × i1 × d1/365 + P × i2 × d2/365` |
| APL Account (Auto Premium Loan) — auto-generated when premium overdue; prevents lapse by borrowing against policy value | ✅ OOTB | Product Factory → Traditional Rules → Allow APL | Reduces future cash value |
| Policy Loan Account — interest accrues on outstanding balance | ✅ OOTB | Product Factory → Loan Rules → Policy Loan Allowed | — |
| CB / SB Deposit Accounts — earn interest under Option 2 or Option 3 | ✅ OOTB | — | — |
| Ad-hoc actions recalculate interest but do NOT capitalize — capitalization deferred to next batch | ✅ OOTB | — | Ad-hoc triggers: Loan Repayment / Apply Policy Loan / Raise APL / CB/SB Allocation |
| Interest calculation cannot proceed if policy frozen | ✅ OOTB | — | System invariant |
| Interest settlement requires ≥1 monthly end date between last settlement date and system date | ✅ OOTB | — | System invariant; batch defers if condition not met |
| Zero-balance accounts excluded from settlement and capitalization | ✅ OOTB | — | System invariant |

---

