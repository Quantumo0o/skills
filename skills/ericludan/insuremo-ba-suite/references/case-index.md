# BSD Case Index
# Version 1.0 | 2026-03-25

> **Path Note:** All case paths are workspace-relative (`memory/knowledge-base/...`). Verify paths against actual workspace structure before use. Paths marked with `???` are known to be unverified — treat as placeholder references only.

---

## Purpose

Provides a categorized index of reference BSD cases for each module.
When writing a new BSD, BA can quickly find similar past cases for pattern reference.
Do NOT copy-paste rules from cases — use them as style and structure reference only.

---

## Case Index by Module

### NB (New Business)
| Case ID | Product | Feature | Rules | Location |
|---------|---------|---------|-------|----------|
| NB-001 | ILP | Single Premium | 3 | `memory/knowledge-base/hsbc-sg/mvp2/bsds/NBU/` |
| NB-002 | VUL | Coverage Term | 7 | `memory/knowledge-base/hsbc-sg/mvp1/bsds/NBU/` |

### PS (Policy Servicing)
| Case ID | Product | Feature | Rules | Location |
|---------|---------|---------|-------|----------|
| PS-001 | ILP | SA Change | 5 | `memory/knowledge-base/hsbc-sg/mvp1/bsds/PS_sprint3/` |
| PS-002 | UL | Surrender | 4 | `memory/knowledge-base/hsbc-sg/mvp2/bsds/PS_sprint2/` |
| PS-003 | HI Rider | Rider Term | 9 | `memory/knowledge-base/hsbc-sg/mvp3/bsds/PS_sprint3/` |

### BCP (Business Continuity Planning)
| Case ID | Product | Feature | Rules | Location |
|---------|---------|---------|-------|----------|
| BCP-001 | All | Policy Reinstatement | 12 | `memory/knowledge-base/hsbc-sg/mvp1/bsds/BCP/` |

### FIN (Finance)
| Case ID | Product | Feature | Rules | Location |
|---------|---------|---------|-------|----------|
| FIN-001 | ILP | Premium Allocation | 6 | `memory/knowledge-base/hsbc-sg/mvp2/bsds/FIN/` |

### CLM (Claims)
| Case ID | Product | Feature | Rules | Location |
|---------|---------|---------|-------|----------|
| CLM-001 | Life | Death Claim | 8 | `memory/knowledge-base/hsbc-sg/mvp3/bsds/CLM/` |

### PTY (Party Management)
| Case ID | Product | Feature | Rules | Location |
|---------|---------|---------|-------|----------|
| PTY-001 | All | AML Checking | 3 | `memory/knowledge-base/hsbc-sg/mvp2/bsds/PTY/` |

---

## Case Index by Rule Pattern

| Pattern | Case ID | Example Rule |
|---------|---------|-------------|
| P4 Calculation | PS-001 | SA Change formula |
| P5 Enumeration | BCP-001 | Reinstatement steps |
| P6 Exception | FIN-001 | Premium allocation exception |

---

## How to Use This Index

1. **When starting a new BSD**, identify which module your feature belongs to (NB/PS/BCP/FIN/CLM/PTY)
2. **Find the closest case** in the index above — same module first, then similar feature
3. **Open the reference case** to study the rule structure and writing style
4. **Do NOT copy rules** — adapt the pattern, not the content
5. **If no similar case exists**, use bsd-patterns.md directly

---

## How to Add a New Case

When a new BSD is completed and approved:

1. Identify: Module + Feature + Rule count
2. Add a row to the appropriate table above
3. Update total count in SKILL.md (if tracked)
4. File the BSD in the correct `memory/knowledge-base/hsbc-sg/` subfolder

---

## Case Quality Criteria

A case is worth indexing if:
- ✅ BSD is in Approved status
- ✅ Contains ≥3 business rules
- ✅ Rules use Patterns 1-7 correctly
- ✅ Has a completed EMSG appendix
- ✅ No outstanding UNKNOWN items

Cases marked as Draft or with significant UNKNOWNs should NOT be indexed yet.