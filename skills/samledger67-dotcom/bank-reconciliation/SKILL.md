---
name: bank-reconciliation
description: "Reconcile bank accounts against QuickBooks Online (QBO) for monthly close, discrepancy investigation, or audit workpapers. Use when a client needs GL vs bank balance matched, unrecorded items caught, or a reconciliation workpaper produced. NOT for payroll reconciliation, AR/AP aging, investment accounts, or intercompany eliminations."
license: MIT
metadata:
  openclaw:
    emoji: "🏦"
---

# Bank Reconciliation Skill

**Pipeline:** `scripts/pipelines/bank-reconciliation.py`  
**Day:** 2 of 14-Day Deterministic Pipeline Build

---

## When to Use This Skill

Use when a client needs their bank account reconciled against QBO:
- Monthly close reconciliation
- Investigating GL/bank balance discrepancies
- Catching unrecorded bank fees, interest, or deposits
- Producing auditor-ready reconciliation workpapers
- Tracking outstanding checks or deposits in transit

**NOT for:**
- Payroll reconciliation (use payroll-recon pipeline)
- AR/AP aging (use ar-collections pipeline)
- Investment/brokerage accounts
- Intercompany eliminations

---

## Requirements

```bash
pip install openpyxl
# Node.js QBO client must be connected:
node integrations/qbo-client/bin/qbo connect <slug>
```

---

## Usage Patterns

### 1. Standard Run (Chase, auto-detected)
```bash
python3 scripts/pipelines/bank-reconciliation.py \
    --slug sb-paulson \
    --end-date 2026-02-28 \
    --bank-csv ~/Downloads/chase_feb2026.csv \
    --bank-ending-balance 42531.87
```

### 2. Specific Account Name
```bash
python3 scripts/pipelines/bank-reconciliation.py \
    --slug glowlabs \
    --end-date 2026-02-28 \
    --bank-csv ~/Downloads/boa_feb2026.csv \
    --account "Business Checking" \
    --bank-ending-balance 18250.00
```

### 3. Wells Fargo (separate debit/credit columns)
```bash
python3 scripts/pipelines/bank-reconciliation.py \
    --slug sb-paulson \
    --end-date 2026-02-28 \
    --bank-csv ~/Downloads/wf_feb.csv \
    --bank-format wellsfargo \
    --bank-ending-balance 55000.00
```

### 4. Custom Column Mapping (unknown CSV format)
```bash
python3 scripts/pipelines/bank-reconciliation.py \
    --slug sb-paulson \
    --end-date 2026-02-28 \
    --bank-csv ~/Downloads/stmt.csv \
    --col-date "Trans Date" \
    --col-desc "Narrative" \
    --col-amount "Net Amount" \
    --bank-ending-balance 28000.00
```

### 5. Wider Date Window + Custom Output
```bash
python3 scripts/pipelines/bank-reconciliation.py \
    --slug sb-paulson \
    --end-date 2026-02-28 \
    --bank-csv ~/Downloads/chase_feb.csv \
    --date-window 5 \
    --bank-ending-balance 42531.87 \
    --out ~/Desktop/recon
```

---

## Arguments Reference

| Argument | Required | Description |
|---|---|---|
| `--slug` | ✅ | Company slug (must be connected in qbo-client) |
| `--end-date` | ✅ | Reconciliation as-of date (YYYY-MM-DD) |
| `--bank-csv` | ✅ | Path to bank statement CSV file |
| `--bank-ending-balance` | Recommended | Bank statement ending balance (float) |
| `--account` | Optional | Account name to match on Balance Sheet |
| `--bank-format` | Optional | `auto` (default), `chase`, `bofa`, `wellsfargo`, `generic` |
| `--col-date` | Optional | Override date column header |
| `--col-desc` | Override | Override description column header |
| `--col-amount` | Optional | Override single amount column header |
| `--col-debit` | Optional | Override debit/withdrawal column header |
| `--col-credit` | Optional | Override credit/deposit column header |
| `--date-window` | Optional | Days for exact match window (default: 3, fuzzy: 2×) |
| `--out` | Optional | Output directory (default: ~/Desktop) |
| `--sandbox` | Optional | Use QBO sandbox environment |

---

## Supported Bank CSV Formats

| Format | Date Column | Amount Column | Notes |
|---|---|---|---|
| `chase` | Transaction Date | Amount | Negative = withdrawal |
| `bofa` | Date | Amount | Negative = withdrawal |
| `wellsfargo` | Date | Withdrawals + Deposits | Two separate columns |
| `generic` | Tries common names | Tries common names | Use `--col-*` if fails |

Auto-detection reads column headers and picks the best format. Use `--bank-format` to override.

---

## Matching Logic

**Pass 1 — Exact:** Amount match within ±$0.01, date within ±`date-window` days (default 3).

**Pass 2 — Fuzzy Date:** Amount match within ±$0.01, date within ±`2×date-window` days (default 6).

**Pass 3 — Fuzzy Vendor:** Amount within ±$1.00, vendor key substring match (strips check numbers, dates, ref numbers), any date.

Unmatched after all 3 passes → flagged in Unmatched tabs.

---

## Reconciliation Equation

```
Book Balance (QBO BS)
+ Deposits in Transit     (book has it, bank hasn't cleared it)
- Outstanding Checks      (book has it, bank hasn't cleared it)
= Adjusted Book Balance

Bank Statement Ending Balance
+ Bank Credits Not in Book  (bank has it, not yet in QBO)
+ Bank Charges Not in Book  (negative; bank has it, not yet in QBO)
= Adjusted Bank Balance

Adjusted Book Balance = Adjusted Bank Balance → RECONCILED ✅
```

---

## Adjusting Entry Auto-Suggestions

The pipeline auto-classifies unmatched bank transactions into:

| Category | Keywords | Suggested Entry |
|---|---|---|
| Bank Fee | "service charge", "monthly fee", "wire fee", "nsf fee" | DR Bank Service Charges / CR Checking |
| Interest Earned | "interest", "dividend" | DR Checking / CR Interest Income |
| Direct Deposit | "payroll", "ach credit", "zelle" | DR Checking / CR AR/Revenue |
| Payment Processor | "stripe", "square", "paypal" | DR Checking / CR Undeposited Funds |
| NSF Returned | "returned item", "returned check" | DR Returned Check Expense / CR Checking |
| Unclassified | (no keyword match) | TBD — review manually |

---

## Output: Excel Workbook

**File:** `BankRecon_{slug}_{YYYYMMDD}.xlsx` (saved to `--out` or `~/Desktop`)

| Tab | Contents |
|---|---|
| **Reconciliation Summary** | Book/bank balance sections, stats, reconciled status badge |
| **Matched** | All matched pairs with match type (exact/fuzzy), amounts, date diff |
| **Unmatched (Book)** | Outstanding checks + deposits in transit (in QBO, not cleared) |
| **Unmatched (Bank)** | Bank items not in QBO (fees, interest, unrecorded deposits) |
| **Adjusting Entries** | Suggested DR/CR journal entries for each unmatched bank item |
| **CDC Log** | Changes since last reconciliation run (book balance, diff, etc.) |

---

## CDC (Change Data Capture)

Cache stored at: `.cache/bank-reconciliation/{slug}.json`

Tracks changes in:
- Book Balance
- Adjusted Book/Bank Balance
- Deposits in Transit
- Outstanding Checks
- Reconciling Difference

On first run: "First run — snapshot saved." On subsequent runs: only changed fields shown. Saves 90%+ API calls on recurring monthly reconciliations.

---

## Design Notes

- All financial math uses Python `Decimal` — no float drift
- Amount sign convention: positive = deposit/inflow, negative = payment/outflow (both book and bank)
- GL pull uses QBO `GeneralLedger` report filtered to the reconciliation period
- If GL pull fails (e.g. permissions), pipeline falls back to Balance Sheet only (matching disabled)
- Bank CSV preamble rows (Chase header lines before data) are auto-skipped

---

## Typical Workflow

```
1. Client sends bank statement PDF → export as CSV from bank website
2. Run pipeline with --slug, --end-date, --bank-csv, --bank-ending-balance
3. Review Reconciliation Summary tab — check RECONCILED badge
4. If difference exists: check Unmatched (Book) for outstanding items, Unmatched (Bank) for unrecorded items
5. Post adjusting entries from Adjusting Entries tab
6. Re-run pipeline — difference should clear to $0.00
7. Save Excel to client Google Drive folder
```
