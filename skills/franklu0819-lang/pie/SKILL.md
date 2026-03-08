---
name: pie
description: Personal Insight Engine (PIE) - A strategic analysis tool that scans local session logs (memory/*.md) and extracts 3 strategic insights using LLMs.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"], "env": ["ZHIPU_API_KEY", "GEMINI_API_KEY"] },
      },
  }
---

# PIE (Personal Insight Engine)

Analyze your startup journey by distilling strategic patterns from your memory logs.

## Setup

**1. Configure API Keys:**
Ensure you have at least one of these in your `.env` or system environment:
- `ZHIPU_API_KEY` (Default for GLM)
- `GEMINI_API_KEY` (Alternative)

**2. Dependencies:**
Requires `openai` and `python-dotenv` python packages.

## Usage

### Run Weekly Review
By default, scans the last 7 days of memory files:

```bash
python3 scripts/pie.py
```

### Custom Lookback
Scan a specific number of days (e.g., last 30 days):

```bash
python3 scripts/pie.py --days 30
```

## How it works

1. **Discovery**: Scans `memory/` for recent Markdown files.
2. **Cleaning**: Strips JSON metadata and system headers.
3. **Synthesis**: Uses LLM to extract 3 core insights (Decision Patterns, Pain Points, Pivots).
4. **Output**: Prints a formatted Markdown report.

---
*Developed by Cipher using OpenSpec.*
