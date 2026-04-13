# InsureMO V3 KB Registry
Version: 1.3 | Updated: 2026-04-08 | Added: ps-reinsurance.md created; ps-new-business/cs/claims/fund/renew/loan/annuity/bonus/billing updated from Gemini V3 UG PDFs

> **Central registry of all ps-* KB files.** All agents that require InsureMO KB reference MUST check this manifest before starting analysis. Do NOT hardcode KB file lists in individual agent instructions.

**How to use:**
- Read this manifest to find the correct KB file for your module
- Check the **Coverage** column to confirm the file covers your specific topic
- If your module is not listed → mark as `UNKNOWN — requires KB confirmation`
- When a new KB file is added to `references/InsureMO Knowledge/`, add it here AND update this manifest's version

---

## Canonical KB Files

| KB File | Module | Coverage |
|---------|--------|---------|
| `ps-new-business.md` | New Business (NB) | NB screen, NB workflow, STP rules, auto-add logic, NB illustration, ILP rules, e-Policy, Free-Look, SA field validation, data entry field rules |
| `ps-underwriting.md` | Underwriting (UW) | UW rules, medical underwriting, NML, loading/exclusion, RI cession |
| `ps-claims.md` | Claims | TI benefit, death benefit, auto-adjudication, claim workflow, TI rules, auto-acceptance threshold, medical bill entry, disbursement plan |
| `ps-fund-administration.md` | Fund Admin | NAV calculation, surrender value, LIFO deduction, fund switching, NAV frequency, bid/offer spread |
| `ps-product-factory.md` | Product Factory (General) | LI Expert Designer: General Config, Finance Config (GL/Fund/Tax), Claim Config |
| `ps-product-factory-limo-product-config.md` | Product Factory (Detail) | Benefit rules, charge config, RI formula, surrender charge, rider config |
| `ps-product-factory-limo-general-config.md` | Product Factory (System) | General PF system-level config, product version control |
| `ps-billing-collection-payment.md` | Billing & Collection (BCP) | Billing schedule, grace period, lapse trigger, premium collection |
| `ps-customer-service.md` | Customer Service (CS) | CS Item, alteration items, UI fields, field triggers, Shield CS, ILP CS, LTC CS, Surrender rules, LAP, Quotation, FATCA |
| `ps-renew.md` | Renewal | Renewal term, renewal notice, lapse/reinstatement |
| `ps-bonus-allocate.md` | Bonus & Distribution | Bonus vesting, n-bonus declaration, distribution impact |
| `ps-annuity.md` | Annuity | Annuity benefit, vesting — future use for annuity products |
| `ps-loan-deposit.md` | Loan & Deposit | Policy loan, deposit, loan interest, surrender value offset |
| `ps-investment.md` | Investment | Investment-linked product NAV, unit management |
| `ps-letter-lilst.md` | Letter / Notices | Policy letters, renewal notices, lapse warnings — future use |
| `ps-quick-reference-index.md` | Index | Quick reference index — **do not cite directly, use for lookup only** |

---

## Missing / Incomplete KB Files

| KB File | Status | Workaround |
|---------|--------|------------|
| `ps-reinsurance.md` | Reinsurance (RI) | RI cession rules, treaty config (QS/Surplus/YRT), SAR calculation, RI accounting, facultative cession |
| `ps-document-generation.md` | ⚠️ NOT in canonical set | Use `ps-product-factory-limo-product-config.md` + product config for doc templates |

---

## Module → KB File Mapping (Quick Lookup)

| Module | Primary KB | Secondary KB |
|--------|----------|-------------|
| New Business | `ps-new-business.md` | `ps-product-factory.md` |
| Underwriting | `ps-underwriting.md` | `ps-product-factory-limo-product-config.md` |
| Claims | `ps-claims.md` | `ps-fund-administration.md` |
| Fund Admin | `ps-fund-administration.md` | `ps-product-factory-limo-product-config.md` |
| Product Factory | `ps-product-factory-limo-product-config.md` | `ps-product-factory.md`, `ps-product-factory-limo-general-config.md` |
| Billing / BCP | `ps-billing-collection-payment.md` | — |
| Customer Service | `ps-customer-service.md` | — |
| Renewal | `ps-renew.md` | `ps-billing-collection-payment.md` |
| Bonus / Distribution | `ps-bonus-allocate.md` | — |
| Annuity | `ps-annuity.md` | — |
| Loan / Deposit | `ps-loan-deposit.md` | — |
| Investment (ILP) | `ps-investment.md` | `ps-fund-administration.md` |
| Letters / Notices | `ps-letter-lilst.md` | — |
| Reinsurance | `ps-reinsurance.md` | `ps-product-factory-limo-product-config.md` |

---

## Agent-Specific Requirements

| Agent | Must Read | Purpose |
|-------|----------|---------|
| Agent 1 (Gap) | KB manifest + relevant module KB | Two-Pass OOTB classification |
| Agent 2 (BSD) | Relevant module KB + ps-reinsurance.md for RI gaps | Rule confirmation, no assumption |
| Agent 3 (Regulatory) | KB manifest + relevant module KB | InsureMO Config/Dev impact mapping |
| Agent 5 (Decoder) | Relevant module KB | Spec to InsureMO behavior mapping |
| Agent 6 (Config) | Relevant module KB | Config path confirmation |
| Agent 7 (Ripple) | KB manifest + relevant module KB + ps-reinsurance.md | Ripple propagation, confirmed behavior (Claims → RI SAR recalculation is HIGH magnitude) |
| Agent 9 (Migration) | KB manifest + `spec-miner-ears-format.md` | Code archaeology for legacy systems without KB |

---

## Supplementary Reference Files

| File | Source | Used By | Purpose |
|------|--------|---------|---------|
| `afrexai-benchmarks.md` | afrexai-insurance-automation | Agent 3, 7, 8 | Industry benchmarks (Claims triage/Compliance/UW metrics) |
| `spec-miner-ears-format.md` | spec-miner | Agent 9 | EARS format + code archaeology for legacy systems |
