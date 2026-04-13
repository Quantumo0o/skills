# InsureMO V3 User Guide — Master Index

## Overview
| Field | Value |
|-------|-------|
| System Version | LifeSystem 3.8.1 |
| Date | 2026-03-26 |
| Format | User Manual (PDF → KB-structured) |
| Total Files | 20 |
| Location | `skills/insuremo-ba-suite/references/InsureMO V3 User Guide/` |

## File Index

| File | Source PDF | Category | Pages | Size | Key Topics |
|------|-----------|---------|-------|------|-----------|
| insuremo-v3-ug-nb.md | 02_New Business_LS3.8.1_0.pdf | New Business | 214 | 17KB | NB end-to-end, 31 Appendix A tables, 9 INVARIANTs, UW rules, field refs |
| insuremo-v3-ug-renewal.md | 04_RenewalMainProcess_0317.pdf | Billing / Renewal | 42 | 29KB | Renewal batch, premium notice, lapse, APL, ILP |
| insuremo-v3-ug-cs-new.md | 03_CS_New.pdf | New Business / Customer Service | ~100+ | 53KB | CS Alterations (30+ types), ILP items, batch ops, ad-hoc services, advanced adjustment |
| insuremo-v3-ug-bonus.md | 05_Declare_And_Allocate_Bonus.pdf | Finance / Bonus | 17 | 11KB | Cash bonus, reversionary bonus, 5 CB options, allocation batch, 5 INVARIANTs |
| insuremo-v3-ug-survival-payment.md | 06_Perform_Survival_Payment.pdf | Finance / Survival Benefit | 13 | 7KB | SB payment, SB options 1-9, SB plan, allocation batch, 4 INVARIANTs |
| insuremo-v3-ug-maturity.md | 07_Perform_Maturity_0.pdf | Finance / Maturity | 23 | 9KB | Maturity payment, 4 maturity options, surrender value formula, disbursement methods, 5 INVARIANTs |
| insuremo-v3-ug-collection.md | 15_Collection_150605.pdf | Billing / Collection | 78 | 8KB | Counter/DDA/CC/Lockbox collection, BCP waiver, suspense accounts, stamp duty, batch upload |
| insuremo-v3-ug-payment.md | 16_Payment_0.pdf | Finance / Payment | 33 | 7KB | Payment requisition (Normal/Medical/Commission/Tax), approval, batch payment, cheque printing, DCA |
| insuremo-v3-ug-loan-deposit.md | 18_Manage_Loan_And_Deposit.pdf | Finance / Loan & Deposit | 36 | 10KB | APL, loan interest capitalization, deposit interest, loan repayment, write-off, 6 INVARIANTs, formulas |
| insuremo-v3-ug-fund-admin.md | 17_Fund_Administration_0.pdf | Investment / Fund Administration | 42 | 10KB | NAV, fund transactions, unit calculations, bid-offer spread, lock-in, gain/loss, fund switch, 5 INVARIANTs |
| insuremo-v3-ug-reinsurance.md | 20_Reinsurance_0.pdf | Finance / Reinsurance | 34 | 10KB | Treaty setup, RI cession batch, claim recovery, experience refund, facultative, undo cessions, 5 INVARIANTs |
| insuremo-v3-ug-sales-channel.md | 22_SalesChannel.pdf | Distribution / Sales Channel | 54 | 10KB | Producer management, commission (FYC/renewal/override), compensation, persistency, assessment, promotion/demotion |
| insuremo-v3-ug-posting-gl.md | 19_Posting_to_GL_0409.pdf | Finance / Accounting / GL | 28 | 10KB | GL posting, EOD/EOM, accounting rules, bank account, reconciliation, FX rate (6 decimals), 5 INVARIANTs |
| insuremo-v3-ug-component-rules.md | 24_Component_Rules.pdf | Core / Calculations | 103 | 19KB | **CORE REFS** — accounting date, tax (GST/ST/Stamp/WHT), APA, age basis, bonus calc (cash/interim/RB/TB), premium/SA formulas, inforce SA, surrender charge, saving account interest, payer/payee priority, FX conversion, tolerance, relationship matrix |
| insuremo-v3-ug-query.md | 23_Query_BL.pdf | Query / Reporting | 35 | 7KB | All query screens: Common Query (9 tabs), NB Query, Investment Query, Payment Query, Claim Query, RI Query, Producer Query, Parties Query, Accounting Query |
| insuremo-v3-pf-system-config.md | eBaoTech_LifeProductFactory_System_Configuration_Guide_0.pdf | System Admin / Access Control | 24 | 7KB | Org hierarchy, user mgmt, 3 role types (Operation/Limitation/Accessible Org), product definition limits, access control rules, new org config checklist |
| insuremo-v3-pf-product-definition.md | eBaoTech_LifeProductFactory_Product_Definition_Guide_0.pdf | Product Configuration / Methodology | 300+ | 10KB | **PRODUCT CONFIG METHODOLOGY** — 3-step config approach, product lifecycle (Create→Edit→Validate→Test→Release), 13 product categories (Term/WholeLife/Endowment/ILP/etc.), 4 config tools (Product Definition/RateTable/FMS/RMS), worked scenarios, all config areas |

## Topic → File Mapping

| Topic | V3 UG File | Notes |
|-------|------------|-------|
| New Business (comprehensive) | insuremo-v3-ug-nb.md | PRIMARY — 214 pages, Appendix A (field desc) + Appendix B (rules) |
| NB workflows | insuremo-v3-ug-nb.md | Initial Reg → Data Entry → UW → Collection → Inforce → Dispatch |
| NB field descriptions | insuremo-v3-ug-nb.md | Appendix A — 100 pages of field-level detail |
| NB rules | insuremo-v3-ug-nb.md | Appendix B — authoritative rules source |
| Auto-UW rules | insuremo-v3-ug-cs-new.md, insuremo-v3-ug-nb.md | Both have UW rules; cs-new has medical exam thresholds |
| Medical exam requirements | insuremo-v3-ug-cs-new.md | Age/SA bands, parametric → medical → extramedical |
| Renewal batch job | insuremo-v3-ug-renewal.md | Daily extract, premium notice, due date move |

| Topic | V3 UG File | Notes |
|-------|------------|-------|
| Renewal batch job | insuremo-v3-ug-renewal.md | Daily extract, premium notice, due date move |
| Premium notice generation | insuremo-v3-ug-renewal.md | Extraction criteria, data fields, GST rules |
| Policy lapse (traditional) | insuremo-v3-ug-renewal.md | APL, normal lapse, PLD |
| ILP lapse | insuremo-v3-ug-renewal.md | Method 1 (PLD in advance), Method 2 (TIV=0) |
| Manual extraction | insuremo-v3-ug-renewal.md | DDA, credit card, force billing |
| Suspend/unsuspend extraction | insuremo-v3-ug-renewal.md | Effective dates, auto-unsuspend batch |
| Billing rules | insuremo-v3-ug-renewal.md | Appendix A — very detailed |
| GST calculation | insuremo-v3-ug-renewal.md | Rounding, prevailing rate |
| Indexation | insuremo-v3-ug-renewal.md | Accept/reject 2x rule |
| Suspense/APA offset | insuremo-v3-ug-renewal.md | Order: renewal suspense → general suspense → APA |
| New Business (end-to-end) | insuremo-v3-ug-cs-new.md | NB workflow, data entry, policy activation |
| Auto-UW rules | insuremo-v3-ug-cs-new.md | Age/SA bands, auto-approve/reject/refer |
| Medical exam requirements | insuremo-v3-ug-cs-new.md | Parametric → medical → extramedical thresholds |
| Manual underwriting | insuremo-v3-ug-cs-new.md | UW decision codes, loading, decline |
| Policy issuance | insuremo-v3-ug-cs-new.md | Waiting period, suicide clause, activation |
| Policy Loan (CS item) | insuremo-v3-ug-cs-new.md | Eligibility formula, max interest rate |
| Reinstatement | insuremo-v3-ug-cs-new.md | Lapse period, reinstatement requirements |
| Top-up | insuremo-v3-ug-cs-new.md | Additional premium, SA increase, waiting period |
| Fund Switch | insuremo-v3-ug-cs-new.md | Switch frequency, min/max, charge |
| Partial Withdrawal | insuremo-v3-ug-cs-new.md | Min amount, SA reduction, charge formula |
| Surrender | insuremo-v3-ug-cs-new.md | Surrender value formula, penalty schedule |
| Cash Bonus allocation | insuremo-v3-ug-bonus.md | Cash bonus options 1-5, allocation batch, account updates |
| Reversionary Bonus | insuremo-v3-ug-bonus.md | Reversionary bonus allocation, accrual, maturity rules |
| Direct Credit invitation | insuremo-v3-ug-bonus.md | 3-month advance batch, disbursement method change |
| Maturity payment | insuremo-v3-ug-maturity.md | 4 maturity options, surrender value formula, disbursement methods |
| Maturity options (revert/reinvest/combine) | insuremo-v3-ug-maturity.md | Options 1-4 explained |
| Surrender value calculation | insuremo-v3-ug-maturity.md | SV + bonuses − loan − interest − premiums |
| Collection (all methods) | insuremo-v3-ug-collection.md | Counter/DDA/Credit Card/Lockbox workflows, UI screens, batch upload |
| BCP Waiver | insuremo-v3-ug-collection.md | Suspense account transfer and apply |
| Stamp duty | insuremo-v3-ug-collection.md | Stamp duty calculation during CC collection |
| Cash totalling | insuremo-v3-ug-collection.md | Cash management and accounting |
| Payment requisition | insuremo-v3-ug-payment.md | 4 types: Normal/Medical/Commission/Tax |
| Batch payment | insuremo-v3-ug-payment.md | Prerequisites, how it works |
| Cheque printing | insuremo-v3-ug-payment.md | Online vs batch cheque |
| DCA payment | insuremo-v3-ug-payment.md | Direct credit authorization |
| APL (Automatic Premium Loan) | insuremo-v3-ug-loan-deposit.md | APL trigger, grace period, GSV condition |
| Loan interest capitalization | insuremo-v3-ug-loan-deposit.md | Daily interest, frequency, formula |
| Loan repayment | insuremo-v3-ug-loan-deposit.md | Interest-first, full vs partial |
| Deposit account interest | insuremo-v3-ug-loan-deposit.md | Capitalization, rate differs from loan rate |
| Write off APL | insuremo-v3-ug-loan-deposit.md | When policy lapses, uncollectible APL |
| NAV (fund price) | insuremo-v3-ug-fund-admin.md | NAV calculation, approval, suspension |
| Fund transactions | insuremo-v3-ug-fund-admin.md | Switch in/out, top-up, partial withdrawal |
| Bid-offer spread | insuremo-v3-ug-fund-admin.md | Charge on switch transactions |
| Lock-in period | insuremo-v3-ug-fund-admin.md | Fund lock-in, policy lock-in |
| Calculate gain/loss | insuremo-v3-ug-fund-admin.md | Capital gain/loss on switch-out |
| Fund switch (automatic) | insuremo-v3-ug-fund-admin.md | Pre-configured automatic switches |
| Reinsurance (RI) cession | insuremo-v3-ug-reinsurance.md | Treaty, RI share, retain order, cession batch |
| Claim recovery | insuremo-v3-ug-reinsurance.md | RI Share × (Claim − Retain) |
| Experience refund | insuremo-v3-ug-reinsurance.md | Profit sharing, claims vs expected |
| Facultative reinsurance | insuremo-v3-ug-reinsurance.md | Per-policy negotiation |
| Producer management | insuremo-v3-ug-sales-channel.md | Agent hierarchy, license, transfer, activate/deactivate |
| Commission (FYC/renewal) | insuremo-v3-ug-sales-channel.md | First year, renewal, override commission calculation |
| Persistency rate | insuremo-v3-ug-sales-channel.md | Month-13 persistency calculation |
| Compensation | insuremo-v3-ug-sales-channel.md | Aggregate, confirm, pay producer commission |
| Performance assessment | insuremo-v3-ug-sales-channel.md | Define, evaluate, promote/demote |
| GL posting | insuremo-v3-ug-posting-gl.md | EOD/EOM batch, accounting rules, Dr=Cr |
| EOD/EOM posting | insuremo-v3-ug-posting-gl.md | End of day / end of month GL posting |
| Bank reconciliation | insuremo-v3-ug-posting-gl.md | LS vs bank statement matching |
| FX rate (6 decimals) | insuremo-v3-ug-posting-gl.md | Multi-currency conversion rate |
| Accounting month increment | insuremo-v3-ug-posting-gl.md | Close month, open next month |
| Accounting date rules | insuremo-v3-ug-component-rules.md | GL date for collections, payments, accruals |
| Tax (GST/ST/Stamp/WHT) | insuremo-v3-ug-component-rules.md | 3 tax types + business scenarios |
| APA (Advance Premium Account) | insuremo-v3-ug-component-rules.md | Creation, interest (compound), billing offset, refunds |
| Bonus calculation | insuremo-v3-ug-component-rules.md | Cash bonus, interim bonus, RB, TB — formulas |
| Premium calculation | insuremo-v3-ug-component-rules.md | Gross premium formula, rounding to 5/10 cents |
| Inforce SA | insuremo-v3-ug-component-rules.md | 5 interpolation methods, decreasing/increasing term riders |
| Surrender charge | insuremo-v3-ug-component-rules.md | On premium vs on surrender amount |
| Payer/Payee priority | insuremo-v3-ug-component-rules.md | Assignee > Trustee > Grantee |
| FX conversion | insuremo-v3-ug-component-rules.md | Real-time rate, 8 dp, 2 dp for fund values |
| Tolerance (NB/Renewal) | insuremo-v3-ug-component-rules.md | Tolerance limit for premium acceptance |
| Relationship matrix | insuremo-v3-ug-component-rules.md | Rider attachment eligibility validation |
| Query (all types) | insuremo-v3-ug-query.md | Common query, NB query, RI query, payment query, claim query |
| Outstanding premium | insuremo-v3-ug-query.md | NB Query → compute inforcing premium |
| ILP cash flow | insuremo-v3-ug-query.md | Investment query → by fund |
| RI cession by policy | insuremo-v3-ug-query.md | RI Query → by treaty/contract/policy |
| Product configuration methodology | insuremo-v3-pf-product-definition.md | 3-step approach, Product Memo, gap analysis |
| Product definition lifecycle | insuremo-v3-pf-product-definition.md | Create→Edit→Validate→Test→Release |
| Product categories | insuremo-v3-pf-product-definition.md | 13 benefit types: Term/WholeLife/Endowment/ILP/Medical/etc. |
| FMS (Formula Management) | insuremo-v3-pf-product-definition.md | PL/SQL and JAVA formula definitions |
| RMS (Rule Management) | insuremo-v3-pf-product-definition.md | Business rules management |
| RateTable | insuremo-v3-pf-product-definition.md | Premium/SA/bonus/RI/commission rates |

## How to Use This KB

When writing BSD for a billing/renewal/lapse feature:

1. Check this index for relevant V3 UG files
2. Read the file for detailed rules
3. Compare with ps-* (current version) for OOTB confirmation
4. Cite V3 UG rules in BSD where ps-* is insufficient

## Naming Convention
- Files: `insuremo-v3-ug-{topic}.md`
- Topics map to InsureMO module names (renewal, claims, uw, etc.)
- Source PDF name preserved in metadata

| insuremo-v3-ls-system-config.md | eBaoTech_LifeSystem_System_Configuration_Guide.pdf | System Admin / LifeSystem Config | 270+ | 12KB | **MASTER SYSTEM CONFIG** �� NB/UW config, billing rate tables, RI (QS/Surplus/XOL/FAC), report management, batch jobs, FMS/RMS tools. Most comprehensive of 3 System Config Guides |

| NB/UW system config | insuremo-v3-ls-system-config.md | Proposal prefixes, campaign type, underwriting authority, discount types |
| RI system config | insuremo-v3-ls-system-config.md | Treaty types (QS/Surplus/XOL/FAC), premium rates, commission rates |
| Billing rate tables | insuremo-v3-ls-system-config.md | Collection counting, deduction schedule, bank transfer file, stamp duty |
| Report management (system) | insuremo-v3-ls-system-config.md | Report deployment, parameters, Crystal Report roles |
| Batch job configuration | insuremo-v3-ls-system-config.md | Job net, dependencies, ad hoc jobs, pre-scheduled jobs |

| insuremo-v3-ls-product-definition.md | eBaoTech_LifeSystem_Product_Definition_Guide.pdf | Product Configuration / LifeSystem | 589 | 7KB | **LifeSystem-specific** product definition guide (vs PF generic tool). Same 3-step approach, 4 worked scenarios. Detailed ILP config, f_lookup() RateTable integration, dynamic field definition, rounding rules |
