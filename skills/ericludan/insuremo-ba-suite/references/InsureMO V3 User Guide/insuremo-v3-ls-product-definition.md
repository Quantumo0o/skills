# InsureMO V3 — LifeSystem Product Definition Guide

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-ls-product-definition.md |
| Source | eBaoTech_LifeSystem_Product_Definition_Guide.pdf |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | ~2015 |
| Category | Product Configuration / LifeSystem |
| Pages | 589 |

## 1. Purpose of This File

**LifeSystem-specific Product Definition Guide** — This is the definitive reference for configuring products within the LifeSystem 3.8.1 system (as opposed to the ProductFactory generic tool guide). Covers all product categories, benefit configurations, ILP-specific product definition, and detailed field descriptions. Used alongside the PF Product Definition Guide for complete product configuration reference.

---

## 2. Document Structure

```
Chapter 1: Product Configuration Approach (3-step methodology)
Chapter 2: Product Definition Process
Chapter 3: Product Configuration Tools
Chapter 4: Scenarios (worked examples)
```

---

## 3. Product Configuration Approach (Same as PF Guide)

### Three-Step Process

```
Step 1: Workout Standard Product Specification
  Input: Client Raw Materials → Standard Product Spec + Gap List

Step 2: Workout Product Definition Memo + High Level Gap List
  Input: Standard Product Spec → Product Memo + Functional Gap Document

Step 3: Configure Product in System
  Input: Product Memo → Product defined in system
```

### Document Types
- **Product Specification Template** — Base to collect product info
- **Standard Product Specification** — All necessary product info
- **Product Memo** — Detail product data for BA config; junior BA can configure from this
- **Gap List** — Features not supported by system

---

## 4. Product Definition Process (Same as PF Guide)

### Lifecycle: Create → Edit → Validate → Test → Release

```
Create Product
  ├── Method 1: From scratch
  └── Method 2: Copy existing product ← Recommended

Edit Product → Validate → Test → Release
```

---

## 5. Product Categories (LifeSystem-Specific)

Same as PF Guide with identical categories:

| Category | Notes |
|----------|-------|
| Term Life | Pure protection |
| Whole Life | Lifetime coverage |
| Endowment | Savings + protection |
| Traditional Annuity | Fixed annuity |
| Mortgage | Mortgage repayment |
| PayCare & Pure Endowment w/o Profit | Short-term |
| Long Term Disability | LTC |
| Medical & Hospitalization | Reimbursement, Cash Benefit, Dread Disease |
| Accident | Accidental death/disability |
| Smart Saver Rider | Saving with bonus |
| **Investment Product** | **Unit Linked, Universal Life, Variable Universal Life** |
| Variable Annuity | Investment + annuity |

**Waiver:** No separate category — configured differently.

---

## 6. Key Product Fields (Same as PF Guide)

| Field | Description |
|-------|-------------|
| Product Code | Max 10 chars, e.g., WL_01, VUL02_BANC |
| Initial Code | Tracks original when copied; for versioning |
| Product Category | Benefit type (see above) |
| Par/Non Par/ILP Indicator | Participating / Non-Participating / ILP |
| Single/Joint Life | Single or joint life (max 2 LA) |
| Pricing Currency | Only one per product |
| Launch Date | Required — product cannot be selected before this date |
| Withdraw Date | Optional — product cannot be selected after this date |

---

## 7. ILP Product Configuration (Detailed)

This guide provides the most detailed ILP product configuration steps:

### ILP Specific Configuration Areas

| Area | Description |
|------|-------------|
| Fund Definition | Create and configure funds |
| Investment Plan | Define investment strategies |
| Investment Scheme | Map funds to schemes |
| Auto Rebalancing | Automatic portfolio rebalancing |
| DCA (Dollar Cost Averaging) | Regular investment strategy |
| Fund Switch | Switch between funds |
| Fund Limits | Per-fund minimum/maximum |

### ILP Premium Configuration

- **Regular Premium** — recurring premium streams
- **Top-up Premium** — ad-hoc additional premiums
- **Premium Allocation** — how premium is allocated to funds

### ILP Charges Configuration

- **Fund Management Fee** — ongoing fee per fund
- **Bid-Offer Spread** — buy/sell price difference
- **Switching Fee** — fee for moving between funds
- **Deduct Order** — which charges applied first

### ILP Worked Examples

The guide includes worked examples:
- **Example 044:** Investment Plan
- **Example 045:** Investment Scheme Details

---

## 8. Worked Scenarios (4 Scenarios)

Same as PF Guide:
- Scenario 1: Investment Product (ILP)
- Scenario 2: Endowment Product
- Scenario 3: A&H Product

---

## 9. RateTable Integration

### RateTable in Product Definition

RateTables are referenced within product definition for:
- Premium rates
- SA rates
- Bonus rates
- RI rates
- Commission rates
- Charge rates

### RateTable Lookup Methods

**Method 1: Using `pkg_ls_prd_rt_query.f_lookup()` function**
- Creates a new RateTable formula
- Example: F_Premium_Rate_New

**Steps:**
1. Check RateTable Code (e.g., Premium_Rate_New)
2. Go to Graphic Editor Screen (Product Definition or iRule → PLSQL FMS → Formula List)
3. Enter Formula Name, Description, Formula Type
4. Enter formula body

---

## 10. Total Installment Premium Limit Table

**Field Descriptions:**

| Field | Description |
|-------|-------------|
| Company | Organization which the limitation applies to |
| ILP Product | Different limitations for ILP vs non-ILP (or N/A) |
| Payment Method | If limitations are related to payment method (or Not Relevant) |
| Total Installment Premium Payment Frequency | Related to frequency (or Not Relevant) |
| Currency | Policy currency |

---

## 11. Dynamic Field Definition

Products can have dynamic custom fields configured:
- **Example 046:** Dynamic Field Definition Example

Custom fields can be added to capture product-specific data not covered by standard fields.

---

## 12. Rounding Rules Configuration

**Example 047:** Rounding Rules Configuration — 'Round' is Selected

Rounding rules define how calculated values are rounded:
- Premium amounts
- SA amounts
- Commission amounts
- Benefit amounts

Typically: truncate to X decimal places → round to nearest cent/dollar.

---

## 13. Comparison: LifeSystem vs ProductFactory Product Definition

| Aspect | LifeSystem PD Guide | PF PD Guide |
|--------|-------------------|-------------|
| System | LifeSystem 3.8.1 specific | Generic ProductFactory tool |
| Pages | 589 | 300+ |
| ILP Configuration | More detailed worked examples | General guidance |
| RateTable Lookup | f_lookup() function details | Basic FMS |
| Dynamic Fields | ✅ Example provided | ✅ General |
| Rounding Rules | ✅ Example provided | ✅ General |
| Content | Same 3-step approach | Same 3-step approach |

---

## 14. Key Menu Paths

| Action | Path |
|--------|------|
| Product Definition | Configuration Center > Product Configuration > Define Product |
| RateTable | Configuration Center > iFoundation > Rate Table > Rate Table Definition |
| FMS (PL/SQL) | iRule > PLSQL FMS > Formula List |
| FMS (JAVA) | iRule > JAVA FMS > Graphic Editor |
| RMS | iRule > Rule Management System |
| Dynamic Field | Product Definition > Configure Dynamic Field |
| Rounding Rules | Product Definition > Configure Rounding Rules |

---

## 15. Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-pf-product-definition.md | PF Product Definition Guide — generic tool guide |
| insuremo-v3-ls-system-config.md | LifeSystem System Config — access control + config |
| insuremo-v3-ug-component-rules.md | Component Rules — calculation formulas |
| insuremo-v3-ug-fund-admin.md | Fund Administration — ILP transactions |
| insuremo-v3-ug-nb.md | NB — product selection |
