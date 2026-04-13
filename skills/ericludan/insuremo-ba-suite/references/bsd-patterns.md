# BSD Business Language — 7 Writing Patterns
# Version 2.0 | 2026-04-05

> Quick reference for writing BSD business rules in Agent 2.
> Full template and examples: `output-templates.md` Section "BSD / BSD Template".
> Always read this file before writing any business rule.

---

## Pattern 1 — System Default Behaviour

**Use when:** You need to state what the system defaults to when no user input.

```
System will default '[FIELD NAME]' as [VALUE / RULE].
```

**Example:**
System will default 'Payment Frequency' as Annual Mode if no selection is made by the user.

---

## Pattern 2 — User Override

**Use when:** A system default can be manually overwritten by a user.

```
User can manually overwrite '[FIELD NAME]' to [ALLOWED VALUES].
If user overwrites, system will [NEW BEHAVIOR].
```

**Example:**
User can manually overwrite 'Sum Assured' to any value between SGD 10,000 and SGD 5,000,000.
If user overwrites, system will re-calculate the modal premium based on the new SA.

---

## Pattern 3 — Conditional

**Use when:** An IF/THEN/ELSE business rule that affects system behavior.

```
IF [CONDITION]
  THEN system will [ACTION].
ELSE: system will [DEFAULT ACTION].
```

**Example:**
IF 'Policy Status' is In Force AND 'Overdue Days' > 30
  THEN system will block all top-up premium transactions.
ELSE: system will allow top-up premium transactions.

---

## Pattern 4 — Calculation (Dual Expression) ★ FORMULA RULES

**Use when:** A numeric calculation with a formula. ALWAYS requires Pattern 7 (Example Table).

**Two-step expression (mandatory):**

Step 1 — Business sentence:
The [OUTPUT FIELD] is calculated by [FORMULA DESCRIPTION] based on [INPUT FIELDS].

Step 2 — Precise formula:
```
[OUTPUT] = [FORMULA]
```

**Example:**
Step 1: The Total Premium Payable is the sum of the Base Premium and all modal rider premiums, multiplied by the selected Payment Frequency factor.

Step 2:
```
Total_Premium = (Base_Premium + Σ Rider_Premiums) × Frequency_Factor
```

> ⚠️ Always pair with Pattern 7 Example Table with ≥2 example rows.

---

## Pattern 5 — Enumeration

**Use when:** A rule with 3 or more sequential steps or options. Prose is banned.

```
[STEP/OPTION 1]: [DESCRIPTION]
[STEP/OPTION 2]: [DESCRIPTION]
[STEP/OPTION N]: [DESCRIPTION]
```

**Example:**
1. Underwriter reviews all required medical examinations.
2. Underwriter enters the underwriting decision reason.
3. System will update 'Underwriting Status' to either Accept Standard, Accept with Loading, Accept with Exclusions, or Decline.
4. If Accept with Loading or Accept with Exclusions, system will require re-confirmation by the Branch Manager.

---

## Pattern 6 — Exception

**Use when:** A rule that overrides or modifies another rule.

```
EXCEPTION: The general rule [GENERAL RULE] does not apply when [EXCEPTION CONDITION].
In this case, system will [EXCEPTION BEHAVIOR].
```

**Example:**
EXCEPTION: The general lapse rule (Section 4.2) does not apply when the policy is within the Freelook Period.
In this case, system will not lapse the policy even if premium is overdue by more than 60 days.

---

## Pattern 7 — Example Table (★ FORMULA RULES ONLY)

**Use when:** Pattern 4 formula rules. Required — a formula without example table is incomplete.

```
For Example:

| Case | [Input A] | [Input B] | Expected [Output] | Notes |
|------|-----------|-----------|-----------------|-------|
| Boundary Low | [Value] | [Value] | [Result] | [Note] |
| Normal | [Value] | [Value] | [Result] | [Note] |
| Boundary High | [Value] | [Value] | [Result] | [Note] |
```

**Example:**
For Example:

| Case | SA (SGD) | Loading (%) | Base Premium (SGD) | Total Premium (SGD) | Notes |
|------|----------|------------|-------------------|---------------------|-------|
| Minimum | 10,000 | 0 | 500 | 500 | Standard |
| Normal | 50,000 | 25 | 2,500 | 3,125 | Loading applied |
| Maximum | 5,000,000 | 50 | 250,000 | 375,000 | Max loading |

---

## Pattern Quick-Card

| Pattern | When to Use | Must Have Example Table? |
|---------|-------------|------------------------|
| P1 System Default | State system default | No |
| P2 User Override | User can change default | No |
| P3 Conditional | IF/THEN/ELSE rules | No |
| P4 Calculation | Formula / numeric calc | ★ YES (always) |
| P5 Enumeration | 3+ steps/options | No |
| P6 Exception | Override another rule | No |
| P7 Example Table | Formula rules (P4) | N/A (pair with P4) |

---

## Common Mistakes

| Mistake | Wrong | Correct |
|---------|-------|---------|
| No ELSE stated | IF condition THEN action | IF condition THEN action. ELSE: system will [DEFAULT]. |
| Field name not quoted | Field Name | 'Field Name' |
| Prose for enumeration | "First do A, then B, then C" | 1. [A] 2. [B] 3. [C] |
| Formula without table | P4 only | P4 + P7 with ≥2 rows |
| "etc." in rule | "...and etc." | List all options explicitly |
