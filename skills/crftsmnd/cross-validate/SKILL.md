# Cross-Validate
CI-Level 2 fact-checking with statistical confidence improvement.

## What This Does

- Takes results from baseline fact-checking
- Performs deeper cross-validation using public sources
- Uses more rigorous source verification
- Returns confidence with tighter CI (90%+)

## When to Use

Trigger AFTER Baseline-RAG runs, or explicitly with:
- "cross-validate"
- "verify with higher confidence"
- "CI-95"

## Workflow

### Step 1: Receive Input
Get claim to verify from user or previous fact-check session.

### Step 2: Public Sources
Use web_search and web_fetch (network tools) to find additional sources:
- Academic papers (PubMed, Google Scholar)
- Government/agency sources (.gov, .edu)
- Recent news (last 6 months)
- Peer-reviewed journals

### Step 3: Cross-Reference
- Check if additional sources agree/disagree
- Weight by source credibility
- Note publication dates

### Step 4: Calculate Score

**Heuristic formula (not statistically rigorous):**
```
adjusted_score = min(95, base_score + (new_credible_sources × 5))
```

Note: This is a simple heuristic, not a confidence interval. Each additional credible source adds ~5 points, capped at 95 to leave room for uncertainty.

### Step 5: Present Results

```
## Cross-Validation: [Claim]

### Scores
| Metric | Baseline | Cross-Validated |
|--------|---------|--------------|
| Score | [X]% | [Y]% |
| Sources | [N] | [M] |

### New Sources Added
- [source 1]
- [source 2]

### Verdict
[CONFIRMED / INCONCLUSIVE / REJECTED]
```

## Tools Used

This skill uses platform tools:
- web_search (for source discovery)
- web_fetch (for source verification)

Not offline — requires network access for web searches.

## Example

```
## Cross-Validation: "Coffee reduces cancer risk"

### Scores
| Metric | Baseline | Cross-Validated |
|--------|---------|--------------|
| Score | 65% | 85% |
| Sources | 3 | 8 |

### New Sources Added
- NIH.gov (2024)
- Google Scholar study
- WHO statement

### Verdict
CONFIRMED
```

## Notes

- Works fully offline with platform tools
- No external dependencies
- No payment required
- Uses public sources only