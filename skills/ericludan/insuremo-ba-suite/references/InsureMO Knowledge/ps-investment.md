# InsureMO Platform Guide — Investment
# Source: Investment User Guide (Fund Administration)
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"how does the Investment module work in InsureMO"** — navigation paths, prerequisites, field behaviour, workflow config parameters, and business rules for fund administration.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for an Investment-related gap
- Agent 6 is generating a **Config Runbook** for Investment items
- A BA needs to verify what **preconditions** the system enforces before allowing a fund transaction

---

## Module Overview

```
Investment Module
│
├── Exchange Rate           ← Real-time FX rate entry for fund transactions
├── Fund Holiday            ← Fund holiday calendar management
└── Manage Fund Price
    ├── Fund Price Entry    ← Enter / upload daily fund prices
    ├── Fund Price Approve  ← Approve or reject entered prices
    ├── Fund Price Revise   ← Revise approved or confirmed prices
    └── Fund Price Query    ← Search and view all fund price records
```

---

## Investment Workflow — Standard Sequence

```
Fund Manager issues fund price
  └─► Fund Price Entry (enter bid price manually or upload file)
        └─► Fund Price Approve
              ├─► Approved → Batch job runs → Confirmed
              └─► Rejected → Fund Manager re-issues price

Optional:
  └─► Fund Price Revise (for Approved or Confirmed records)
        └─► Original record marked Revised; new record enters Entered state → re-approve
```

---

## Menu Navigation

| Action | Path |
|---|---|
| Set exchange rate | Investment > Exchange Rate |
| Manage fund holidays | Investment > Fund Holiday |
| Enter fund price | Investment > Fund Price > Entry |
| Approve fund price | Investment > Fund Price > Approve |
| Revise fund price | Investment > Fund Price > Revise |
| Query fund price | Query > Investment > Fund Price Query |

---

## Per-Item Reference

### Exchange Rate

**Purpose:** Set the real-time FX rate used for fund transactions.

**Navigation:** Investment > Exchange Rate

**Prerequisites:** N/A

**Procedures:**
1. Select Investment > Exchange Rate → Set Transaction Foreign Exchange Rate page displayed.
2. Click **Add** → enter Source Currency, Conversion Date, Exchange Rate Type, Exchange Rate (Buy), Exchange Rate (Sell) → Click **Submit**.
3. Alternatively, click **Upload** to import an exchange rate file (XLS/XLSX). Download template via **Download Template**.
4. To modify an existing rate: search it out → click **Edit**.

**Business Rules — Add:**
- Target currency is fixed as base currency; cannot be changed.
- Middle Exchange Rate = (Buy Rate + Sell Rate) / 2.
- All exchange rates rounded to 6 decimal places; last decimal is always 0.
- Buy rate must be ≤ Sell rate.
- Default Exchange Rate Type = `Daily Transaction Exchange Rate`.
- On successful add, system auto-generates the inverse rate record: `Inverse Rate = Trunc(1 / positive exchange rate, 5)`.
- Search results sorted descending by Conversion Date.

**Business Rules — Upload:**
- Upload file format must be XLS or XLSX.
- Conversion Date format must be `YYYYMMDD`.
- System errors if: source currency not found, date invalid/empty, file empty, format incorrect.
- Remark field truncated automatically beyond 100 characters.
- On upload, inverse rate record auto-generated.
- Re-uploading for the same Conversion Date overwrites original (including inverse rate).

---

### Fund Holiday

**Purpose:** Define non-trading days for specific funds so that fund price entry and transactions are skipped on those dates.

**Navigation:** Investment > Fund Holiday

**Prerequisites:** Fund holidays are determined by the fund organisation.

**Procedures:**
1. Select Investment > Fund Holiday → Fund Holiday page displayed.
2. Click **Add** → enter Fund Code and Fund Holiday Date → Click **Submit**.
3. To delete an existing record: search it out → click **Delete**.
4. Alternatively, click **Upload** to import a fund holiday file (CSV). Download template via **Download Template**.

**Business Rules:**
- Entered fund holiday date must be **later than** current system date.
- Entered fund holiday date must not duplicate an existing holiday for the same fund.
- Fund holiday date to be **deleted** must be **earlier than** current system date.
- Remark field truncated automatically beyond 100 characters.
- Upload file format must be CSV.
- System errors on upload if: date duplicated with existing record, date later than system date, duplicate records for same fund and date in file, fund code not found, fund code or date empty, date not valid or format not `YYYYMMDD`, file empty.

---

### Fund Price Entry

**Purpose:** Enter the daily bid price for each fund before trading.

**Navigation:** Investment > Fund Price > Entry

**Prerequisites:** Fund price has been obtained from the fund manager.

**Procedures:**
1. Select Investment > Fund Price > Entry → Fund Price Entry page displayed.
2. Set search criteria → click **Search**. Only funds without a price for the selected Price Effective Date are displayed.
3. Select target fund → click **Edit** → enter Bid Price. Offer Price and Variance from Last Confirmed Price calculated automatically.
   - `Variance from Last Confirmed Price = (Bid Price – Last Price) / Last Price`
4. Click **Submit**. Price status changes to `Entered`.
5. Alternatively, click **Upload** to mass import (XLS/XLSX only). Download template via **Download Template**.

**Business Rules:**
- Selected Price Effective Date cannot be current date or future date.
- Selected Price Effective Date cannot be a non-working day.
- If selected date is set as a fund holiday, the fund will not appear in results.
- Maximum decimal places for price entry: **5 DPs**.
- System errors on upload if: fund already has price for selected date, date is current/future, date format not `YYYYMMDD`, date empty/invalid, duplicate record for same fund code and date, fund code not found, file empty.
- Warning displayed if Variance from Last Confirmed Price exceeds tolerance level; user can click **Confirm** to proceed.

---

### Fund Price Approve

**Purpose:** Approve or reject fund prices that are in `Entered` status.

**Navigation:** Investment > Fund Price > Approve

**Prerequisites:** Fund price has been entered (status = `Entered`).

**Procedures:**
1. Select Investment > Fund Price > Approve → Fund Price Approval page displayed.
2. Set search criteria → click **Search**. Only funds with status `Entered` are displayed.
3. Select target fund → click **Approve**. Price status changes to `Approved`.
   - To **reject**: select fund → click **Reject**. Fund manager must re-issue price.
   - To **validate** which prices are not yet approved: click **Fund Price Validate**. System shows message indicating unapproved funds.
4. On the scheduled batch date, system auto-confirms price; status changes to `Confirmed`.

**Business Rules:**
- Selected Price Effective Date cannot be current date or future date.
- Selected Price Effective Date cannot be a non-working day.
- If selected date is a fund holiday, the fund will not appear in results.
- Warning displayed if Variance from Last Confirmed Price exceeds tolerance level.

---

### Fund Price Revise

**Purpose:** Correct an already-approved or confirmed fund price.

**Navigation:** Investment > Fund Price > Revise

**Prerequisites:** Fund price status is `Approved` or `Confirmed`.

**Procedures:**
1. Select Investment > Fund Price > Revise → Fund Price Revise page displayed.
2. Set search criteria → click **Search**. Only funds with status `Approved` or `Confirmed` are displayed.
3. Select target fund → click **Revise** → edit Bid Price. Offer Price and Variance refreshed automatically.
4. Click **Submit**. Original record status changes to `Revised`; new record saved with status `Entered` (must go through approval again).

**Important:** Revised fund price does **not** affect fund transactions already confirmed using the original price.

**Business Rules:**
- Selected Price Effective Date cannot be current date or future date.
- Selected Price Effective Date cannot be a non-working day.
- If selected date is a fund holiday, the fund will not appear in results.

---

### Fund Price Query

**Purpose:** View all fund price records regardless of status.

**Navigation:** Query > Investment > Fund Price Query

**Prerequisites:** Fund price has been imported into system.

**Key behaviour:**
- Fund price entry is not required for non-working days and fund holidays.
- When a price is entered for the next working day, system auto-populates the same price for preceding non-working / holiday dates.
- Once a price is approved / rejected / confirmed / revised, status is auto-updated; these auto-populated records are viewable in the query page only.

---

## Fund Transaction Rounding Rules

### Product-Level Configuration

In **Product Configuration > ILP Rules**, the field `Fund Units DPs` defines the fund unit decimal place at product level.

### Rounding Formulas

| Calculation | Formula |
|---|---|
| Transaction Units | `Round Down (Transaction Amount by Fund Currency / Price, Fund Units DPs)` |
| Transaction Amount by Fund Currency | `Round (Transaction Units × Fund Price, 2)` |
| Transaction Amount by Policy Currency (same currency) | Equal to Transaction Amount by Fund Currency |
| Transaction Amount by Policy Currency (different currency) | `Round Down (Transaction Amount by Fund Currency × Exchange Rate, 2)` |

---

## Actual Transaction Amount / Unit Calculation (Funding Factor)

**Purpose:** Apply a fund factor ratio to pending and settled fund transaction records for reporting purposes.

**Configuration:** In **Ratetable Configuration**, add a rate table defining `FFrate` (fund factor ratio) by `distri_type` at product level.

### Formulas

| Calculation | Formula |
|---|---|
| Actual Transaction Amount | `Round Down (Pending Transaction Amount × Funding Factor, 2)` |
| Actual Transaction Unit | `Round Down (Pending Transaction Unit × Funding Factor, 6)` |

### Key Rules
- Actual amounts/units calculated when generating pending fund transaction records; stored in `T_FUND_TRANS_APPLY` for reporting.
- If pending transaction is **by amount**: actual transaction amount calculated; actual transaction unit = 0.
- If pending transaction is **by unit**: actual transaction unit calculated; actual transaction amount = 0.
- For **dual account products**: sub-account type indicated on pending transactions (IUA/AUA; RPA maps to IUA, TPA maps to AUA).
- Transaction month = policy months between Commencement Date and Transaction Apply Date + 1.
- System uses Transaction Apply Date to capture the latest fund factor ratio after effective start date.
- Products / transaction codes without a defined AFF: system treats AFF = 1 (actual = pending amount/unit).
- For **reversed** fund transactions: apply status set to `Undo`; undo apply time recorded.
- After settlement, results stored in `T_FUND_TRANS` for reporting; synchronised to ODS.

---

## Fund Price Status Reference

| Status | When Set |
|---|---|
| Entered | Price submitted via Entry or Revise (new record) |
| Approved | Approved by Investment team |
| Confirmed | Auto-confirmed by scheduled batch job |
| Revised | Original record superseded by a Revise action |
| Rejected | Rejected during Approve step |

---

## Config Gaps Commonly Encountered in Investment

| Scenario | Gap Type | Config Location |
|---|---|---|
| Fund Units DPs per product | Config Gap | Product Configuration > ILP Rules > Fund Units DPs |
| Fund factor ratio per distri_type | Config Gap | Ratetable Configuration → FFrate table |
| Exchange rate tolerance level | Config Gap | System parameter for FX variance tolerance |
| Fund price variance tolerance level | Config Gap | System parameter for price variance tolerance |

---

## ⚠️ Limitations & Unsupported Scenarios

> This section documents known limitations and scenarios NOT supported by the system. Updated: 2026-03-14

### Investor Classification

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| AI (Accredited Investor) Full Access | Not supported | Code | Requires custom development for full fund access |
| Non-AI Restrictions | Not supported | Code | Requires development to filter MAS-authorized schemes |
| SFA Section 4A Classification | Not supported | Code | Investor classification needs custom module |

### Fund Management

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| New Fund Creation | Requires LIMO IT | Dev | Cannot add funds via configuration |
| Custom Fund Strategies | Limited types | Config | Predefined strategy types only |
| Fund Switch Limits | Configurable but limited | Config | Check product factory settings |

### Custody & Asset Services

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Custodian Selection | Not supported | Code | Requires integration development |
| Asset Transfer (In-kind) | Not supported | Code | Cannot transfer securities directly |
| Multi-Custodian | Limited | Config | Check with implementation |

### Investment Options

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Self-Managed Portfolio | Limited | Config | Requires investment mandate configuration |
| Discretionary Mandate | Limited | Config | Standard mandate types only |
| Alternative Investments | Limited | Config | Most ILPs have restricted fund lists |

---

## Related Files

| File | Purpose |
|---|---|
| `ps-customer-service.md` | CS module guide (alteration items, workflow) |
| `insuremo-billing-collection-payment.md` | Billing, Collection, Payment module guide |
| `ps-product-factory.md` | Product Factory config (ILP Rules, Fund Units DPs) |
| `insuremo-ootb-full.md` | OOTB capability classification (use for Gap Analysis) |