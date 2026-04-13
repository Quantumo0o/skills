# InsureMO V3 — ProductFactory Product Definition Guide

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-pf-product-definition.md |
| Source | eBaoTech_LifeProductFactory_Product_Definition_Guide_0.pdf |
| System | LifeProductFactory 3.8 |
| Version | V3 (legacy) |
| Date | 2014-07 |
| Category | Product Configuration / Methodology |
| Pages | 300+ |

## 1. Purpose of This File

**Product Configuration Methodology Reference** — This is the definitive guide on HOW to configure insurance products in LifeProductFactory. Covers the full product definition lifecycle, all configuration tools, and worked examples. Essential for understanding InsureMO product configuration architecture, gap analysis, and solution design.

---

## 2. Product Configuration Approach

### Three-Step Process

```
Step 1: Workout Standard Product Specification
  Input: Client Raw Materials / Workshop → Output: Standard Product Spec + Gap List

Step 2: Workout Product Definition Memo + High Level Gap List
  Input: Standard Product Spec → Output: Product Memo + Functional Gap Document

Step 3: Configure Product in System
  Input: Product Memo → Output: Product defined in system
```

### Document Types

| Document | Purpose | Used For |
|---------|--------|---------|
| Product Specification Template | Base to collect product info | Gather requirements |
| Standard Product Specification | All necessary product info | Product memo base |
| Product Memo | Detail product data for configuration | BA config product; junior BA can configure from this |
| Gap List | Features not supported by system | Solution design |

### Prerequisites

**Step 1-2 (Analysis):**
- Understand insurance product and related features/calculations
- Understand how system supports these features
- Ability to analyze gaps and provide proper solutions

**Step 3 (Configuration):**
- Ability to use Product Definition tools: FMS, RateTable

---

## 3. Product Definition Process

### Lifecycle: Create → Edit → Validate → Test → Release

```
Create Product
  ├── Method 1: From scratch
  └── Method 2: Copy existing product ← Recommended (saves time)
        └── Sample products provided as templates

Edit Product
  └── Enter/modify product information

Validate Product
  └── Basic checking rules to avoid incomplete/conflicting definitions

Test Product
  ├── Functional testing
  └── Valuation testing (calculations)

Release Product
  └── Deploy to Production and release to market
```

---

## 4. Product Categories (Benefit Types)

System-supported product categories:

| Category | Examples |
|----------|---------|
| Term Life | Pure protection |
| Whole Life | Lifetime coverage |
| Endowment | Savings + protection |
| Traditional Annuity (Fixed) | Lifetime income |
| Mortgage | Mortgage repayment |
| PayCare & Pure Endowment w/o Profit | Short-term |
| Long Term Disability (Long Term Care) | LTC |
| Medical & Hospitalization | Reimbursement, Cash Benefit, Dread Disease |
| Accident | Accidental death/disability |
| Smart Saver Rider | Saving product with bonus |
| **Investment Product** | **Unit Linked, Universal Life, Variable Universal Life** |
| Variable Annuity | Investment + annuity |

**Note:** Waiver (Waiver of Premium, Payer Benefit Rider) has no separate category — configured differently.

---

## 5. Product Key Fields

### Main Product Information

| Field | Description |
|-------|-------------|
| Product Code | Business code, max 10 chars, e.g., WL_01, VUL02_BANC |
| Initial Code | Tracks original product when copied; used for versioning |
| Organization Code | Insurance company the product belongs to |
| Product Name | Marketing name, e.g., FLEXILIFE 60 (CB) PAID-UP |
| Main Product or Rider | Main vs rider (rider = separate product) |
| Product Category | Benefit type (see above) |
| Par/Non Par/ILP Indicator | Participating / Non-Participating / Investment-Linked |
| Single/Joint Life | Single life or joint life (max 2 LA under same product) |
| Pricing Currency | Only one pricing currency per product |
| Launch Date | Date product can be sold (required) |
| Withdraw Date | Date product is no longer sold (optional, updatable) |
| Plan Description | General product description for documents |

### Product Category × Par/ILP Indicator

| Indicator | Meaning | Additional Fields Required |
|-----------|---------|--------------------------|
| Par | Participating | Bonus information required |
| Non Par | Non-Participating | No bonus |
| ILP | Investment-Linked | Investment-related information required |

---

## 6. Configuration Tools

### Tool 1: Product Definition
Main product configuration UI. Configure all product parameters, rate tables, and options.

**Sub-tasks:**
- Define Product (main info, benefits, riders)
- Global Setup
- Configure Product Module
- Configure Dynamic Field
- Configure Rounding Rules
- Product Import/Export

### Tool 2: RateTable
Define rate tables for: premium rates, SA rates, bonus rates, RI rates, commission rates.

### Tool 3: FMS (Formula Management System)
Define custom calculations.

**Two methods:**
- **PL/SQL FMS** — Formula defined in PL/SQL
- **JAVA FMS** — Formula defined in JAVA with graphic editor

**Key FMS functions:** mod(), add_months(), trunc(), SIGN()

### Tool 4: RMS (Rule Management System)
Define business rules that govern product behavior and validation.

---

## 7. Key Product Configuration Areas

### 7.1 Product Main & Sales Info
- Product code, name, category, currency
- Sales channels, default currency
- Company name definition
- Operational category

### 7.2 Provisioning & Tariff
- Product Provisioning (Table 3-9)
- Premium calculation method
- Guaranteed Period Types (3 options)
- Product Tariff Type

### 7.3 Tax Configuration
- **Stamp Duty:** Rate setting, indicator definition
- **GST:** Rate setting, indicator definition
- **Withholding Tax:** Applicable scenarios

### 7.4 Benefit Configuration
- **Survival Benefit (SB):** SA rate, payment options
- **Maturity Benefit:** Annuity rate, payment mode
- **Annuity Payment:** Rate table, frequency
- **Claim Calculation:** Configuration per benefit type

### 7.5 Accumulator Definitions
System predefined accumulators (Table 3-34):
- DSL001, DSL002, DSL003, DUT001, DSL004... (predefined formulas)
- Custom accumulators: Deductible, Dollar/Service Limit, Co-payment, Co-payment with Segment

### 7.6 Limit Tables
- **Age Limit Table:** Entry age, renewal age, expiry age (ALAB/ALMB/ANB)
- **Term Limit Table:** Premium payment term, coverage term
- **Initial SA Limit Table:** Based on age, occupation class, payment method
- **Premium Limit Table:** Initial and subsequent premium limits
- **Payment Method Table:** How premium is collected

### 7.7 Relationship Matrix
Validates which riders can attach to which main products.
- M1-R1, M1-R2, M1-W1, M1-PBR1 (main to rider)
- R1-R2 (rider to rider, same LA)
- R1-W2 (parent to child rider)

### 7.8 ILP / Investment Configuration
- ILP Related Parameters and Tables
- Product Guarantee Option
- Product Withdraw Mode / Frequency
- Annuity Pay Mode / Frequency
- **Bonus:** Cash Bonus Table, Reversionary Bonus Table, Terminal Bonus Table
- **Cash Bonus Option Table**
- **Product Fund Limit Table (ILP Only)**
- **Allowed Invest Scheme:** Auto Re-balancing, DCA (Dollar Cost Averaging)
- **Strategy Rate Definition**
- **Investment Scheme:** Fund mapping, Close Fund Mapping
- **Total Installment Premium Limit**
- **CPI Indexation Rate**
- **ETA Commutation**

### 7.9 Charges Configuration
- Product Charge List
- ILP Charge Definition (Fund Level)
- Deduct Order (which charges applied first)
- Deduct Mode

### 7.10 SA and Premium Specification
- SA Unit / Base Unit
- SA Proportion
- Premium Proportion
- Fixed SA/Unit vs Fixed Premium

### 7.11 NB Rules
Rules governing new business processing.

**NB Rules by reference type:**
- By Total SA of All In-force Segments
- By Total Premium of All In-force Segments
- By SA of Attached-to Product
- By Premium of Attached-to Product

### 7.12 Finance Rules
- GL account mapping
- Accounting rules for the product

### 7.13 Product Business Category
Classifies product for reporting and regulatory purposes.

---

## 8. Rounding Rules

Configurable rounding rules for:
- Premium amounts
- SA amounts
- Commission amounts
- Benefit amounts

Typically: truncate to X decimal places → round to nearest cent/dollar.

---

## 9. Product Import/Export

Products can be exported and imported across environments using the Product Import/Export function. Useful for:
- Moving products from test to production
- Backup and restore
- Product versioning

---

## 10. Three Worked Scenarios

### Scenario 1: Investment Product (ILP)
Complete product definition walkthrough for a Unit Linked product.

### Scenario 2: Endowment Product
Complete product definition walkthrough for an endowment product.

### Scenario 3: A&H Product (Accident & Health)
Complete product definition walkthrough for a medical/health product.

---

## 11. Key Formulas Reference (from FMS Examples)

| Function | Description |
|----------|-------------|
| mod(n, d) | Returns remainder of n/d |
| add_months(date, n) | Adds n months to date |
| trunc(date or number) | Truncates to specified precision |
| SIGN(number) | Returns sign of number (-1/0/+1) |

---

## 12. Product Definition Workflow Summary

```
1. Create Product (copy recommended)
      ↓
2. Edit Product Main Information
      ↓
3. Configure Benefits (SB, Maturity, Annuity, etc.)
      ↓
4. Configure Limits (Age, Term, SA, Premium)
      ↓
5. Configure Relationship Matrix (rider attachment)
      ↓
6. Configure ILP/Investment (if applicable)
      ↓
7. Configure Charges (Deduct Order, Deduct Mode)
      ↓
8. Configure NB Rules
      ↓
9. Configure Finance Rules
      ↓
10. Configure Rounding Rules
      ↓
11. Validate Product (basic checking)
      ↓
12. Test (functional + valuation)
      ↓
13. Release to Production
```

---

## 13. Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-pf-system-config.md | System Configuration Guide — access control |
| insuremo-v3-ug-component-rules.md | Component Rules — all calculation formulas |
| insuremo-v3-ug-nb.md | NB — product selection at NB |
| insuremo-v3-ug-renewal.md | Renewal — billing by product config |
| ps-underwriting.md | Current version — UW rules by product |
| ps-product-parameters.md | Current version — product parameter reference |
