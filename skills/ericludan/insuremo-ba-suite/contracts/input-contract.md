# Input Contract
# OpenClaw ↔ Claude Interface Contract

> This file is for Claude only.
> Every time OpenClaw calls Claude, it MUST declare INPUT_TYPE at the top of the prompt.
> Claude selects the processing logic based on INPUT_TYPE — this step cannot be skipped.

---

## Prompt Template (OpenClaw must follow this)

```
INPUT_TYPE: [type]
AGENT: [Agent 0 / 1 / 2 / 3 / 4]
ASSUMPTION_REGISTER: [current assumption register as JSON, or [] if none]
OPEN_QUESTIONS: [current open questions list as JSON, or [] if none]

[Input data]
```

---

## Input Type Specifications

---

### RAW_USER_REQUEST
**Source:** Direct user input, not processed by any skill

**Claude decision logic:**
```
IF input contains explicit business rules / formulas / field definitions
  → Specification Mode → route to Agent 2 or Agent 4
ELSE
  → Discovery Mode → route to Agent 0
  → Ask questions in rounds, max 3 per round
  → Produce Requirement Brief
  → Wait for user confirmation — do not self-advance
```

**Prohibited:** Do not output formulas or Tech Spec in Discovery Mode

---

### PARSED_CLIENT_DOC
**Source:** Output from OpenClaw after running office-document-specialist-suite

**Expected structure:**
```json
{
  "input_type": "PARSED_CLIENT_DOC",
  "source_file": "client_requirements.docx",
  "extracted_features": [
    {
      "feature_id": "F001",
      "description": "Feature description",
      "raw_text": "Original text from document"
    }
  ]
}
```

**Claude task:** Execute Agent 1 Gap Analysis
**Prohibited:** Add features not in the document; assume OOTB support

---

### GAP_MATRIX
**Source:** Agent 1 output, confirmed by BA

**Expected structure:**
```json
{
  "input_type": "GAP_MATRIX",
  "confirmed_by": "BA Name",
  "confirmed_date": "YYYY-MM-DD",
  "items": [
    {
      "id": "G001",
      "feature": "Feature name",
      "gap_type": "Dev Gap",
      "solution": "Proposed solution",
      "priority": "High"
    }
  ]
}
```

**Claude task:** Execute Agent 2 BSD generation
**Prohibited:** Include Low priority items in the main BSD body

---

### APPROVED_BSD
**Source:** BSD signed off by stakeholders

**Expected structure:**
```json
{
  "input_type": "APPROVED_BSD",
  "version": "1.0",
  "approved_by": ["Underwriting", "Actuarial", "IT"],
  "approved_date": "YYYY-MM-DD",
  "open_questions": [],
  "sections": {
    "user_stories": [],
    "business_rules": [],
    "acceptance_criteria": []
  }
}
```

**Pre-flight check (Claude must execute):**
```
IF open_questions is non-empty
  → STOP immediately
  → List all unresolved questions
  → Output: "⛔ Tech Spec blocked. Resolve the following before resubmitting:"
  → Do NOT generate any Tech Spec content
```

**Claude task:** Execute Agent 4 Tech Spec generation (8-step process)

---

### EXEC_RESULT
**Source:** Output from OpenClaw after running the Python exec sandbox

**Expected structure:**
```json
{
  "input_type": "EXEC_RESULT",
  "status": "PASSED",
  "tests_total": 8,
  "tests_passed": 8,
  "failures": [],
  "stdout": "All 8 tests passed ✅",
  "code_executed": "..."
}
```

**Claude processing logic:**
```
IF status == "PASSED"
  → Write result into Tech Spec Test Matrix
  → Mark as "Machine-verified ✅ (YYYY-MM-DD)"
  → Continue to Agent 4 Step 5

IF status == "FAILED"
  → Stop — do not continue Tech Spec generation
  → Analyse failures list, identify root cause
  → Fix formula
  → Output corrected Python code, await next EXEC_RESULT
```

**Absolute prohibitions:**
- Continue generating Tech Spec on FAILED status
- Modify test cases to force a pass
- Claim "tests passed" without a confirming EXEC_RESULT

---

### REGULATORY_QUERY
**Source:** Explicit user trigger or auto-triggered by Agent 2 on cross-border scope detection

**Expected structure:**
```json
{
  "input_type": "REGULATORY_QUERY",
  "feature": "Feature description",
  "markets": ["MY", "SG"],
  "context": "Relevant BSD section or business rule description"
}
```

**Claude task:** Execute Agent 3 compliance check using web_search for latest regulatory requirements

---

### TECH_SPEC
**Source:** Agent 4 output (Tech Spec completed and reviewed)

**Expected structure:**
```json
{
  "input_type": "TECH_SPEC",
  "prd_version": "1.0",
  "tech_spec_version": "1.0",
  "approved_prd_ref": "20260313_BSD_MR_Coverage_Term_v1.0.md",
  "open_questions": [],
  "python_tests_passed": true,
  "sections": {
    "business_rules": [],
    "acceptance_criteria": [],
    "formula_definitions": [],
    "invariants": []
  }
}
```

**Pre-flight check (Claude must execute):**
```
IF open_questions is non-empty
  → STOP immediately
  → Output: "⛔ UAT generation blocked. Resolve open questions before resubmitting."
  → Do NOT generate any UAT content

IF python_tests_passed != true
  → STOP immediately
  → Output: "⛔ UAT generation blocked. Tech Spec Python tests must pass first."
```

**Claude task:** Execute Agent 8 UAT Test Case generation

---

### CHANGE_REQUEST_MIGRATION
**Source:** Client request explicitly mentioning legacy system migration, data conversion, or historical policy import

**Expected structure:**
```json
{
  "input_type": "CHANGE_REQUEST_MIGRATION",
  "source_system": "Legacy System Name",
  "migration_scope": ["Policy", "Party", "Coverage", "Premium", "Claims"],
  "data_volume_estimate": {
    "policies": 0,
    "parties": 0
  },
  "migration_timeline": "YYYY-MM-DD",
  "existing_gap_matrix_ref": "optional — path to approved Gap Matrix if exists",
  "data_dictionary": "optional — legacy system data dictionary"
}
```

**Claude task:** Execute Agent 9 Data Migration Requirements analysis in parallel with Agent 7 Impact Analysis

**Auto-parallel trigger:**
```
CHANGE_REQUEST_MIGRATION detected
  → Trigger Agent 9 (Data Migration Requirements)
  → Trigger Agent 7 (Impact Analysis) in parallel
  → Merge outputs into combined Migration + Impact report
```
