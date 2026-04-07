# Compliance Copilot MCP — Vendor GO/BLOCK Decisions

**AI-powered compliance decision engine for vendor assessment, sanctions screening, and due diligence.**

This MCP server enables AI agents to make binary GO/CAUTION/BLOCK decisions on vendors and entities in real-time, powered by US federal data sources (OFAC, OSHA, EPA, USASpending).

## Core Philosophy

**Not a data API. A decision API.**

- `assess_vendor(company)` → GO / CAUTION / BLOCK + confidence + reasoning
- `can_we_proceed(entity)` → YES/NO + action
- `compare_vendors([A,B,C])` → Ranked list + recommendation
- `batch_screen(entities[])` → Summary + flagged entities

Agents use these tools to decide the next action without needing to parse raw data.

## Tools

### 1. `assess_vendor`

Full vendor risk assessment with integrated scoring.

**Input:**
```json
{
  "company": "Tesla",
  "state": "CA"  // optional, for location-specific checks
}
```

**Output:**
```json
{
  "company": "Tesla",
  "verdict": "GO",              // GO | CAUTION | BLOCK
  "confidence": "HIGH",         // HIGH | MEDIUM
  "summary": "Tesla shows 60 OSHA inspections and 2 EPA violations. No sanctions. Active government contractor.",
  "recommendation": "Proceed with standard due diligence.",
  "riskFactors": ["60 OSHA inspections since 2020", "2 EPA facilities with violations"],
  "scores": {
    "sanctions": 100,           // 0-100, 100=clean
    "safety": 58,               // OSHA score
    "environmental": 100,       // EPA score
    "contractor": 90,           // Gov contract multiplier
    "overall": 88               // Weighted average
  },
  "decidedAt": "2026-03-26T11:47:00.000Z"
}
```

### 2. `can_we_proceed`

Quick binary OFAC-only check for immediate decisions.

**Input:**
```json
{
  "entity": "Banco Nacional De Cuba",
  "type": "transaction"  // transaction | vendor | investment
}
```

**Output:**
```json
{
  "entity": "Banco Nacional De Cuba",
  "proceed": false,
  "reason": "OFAC sanctions match: CUBA program",
  "riskLevel": "CRITICAL",
  "action": "BLOCK — Do not proceed. Legal review required.",
  "checkedAt": "2026-03-26T11:47:00.000Z"
}
```

### 3. `compare_vendors`

Compare and rank multiple vendors by compliance risk.

**Input:**
```json
{
  "vendors": ["Tesla", "Ford", "General Motors"],
  "criteria": "overall"  // overall | safety | compliance
}
```

**Output:**
```json
{
  "total": 3,
  "ranked": [
    {"rank": 1, "company": "GM", "verdict": "GO", "score": 78, "riskLevel": "LOW"},
    {"rank": 2, "company": "Ford", "verdict": "GO", "score": 71, "riskLevel": "LOW"},
    {"rank": 3, "company": "Tesla", "verdict": "CAUTION", "score": 58, "riskLevel": "MEDIUM"}
  ],
  "recommendation": "GM is the lowest-risk vendor.",
  "comparedAt": "2026-03-26T11:47:00.000Z"
}
```

### 4. `batch_screen`

Fast screening of up to 100 entities for GO/BLOCK decisions.

**Input:**
```json
{
  "entities": ["Amazon", "Banco Nacional De Cuba", "Microsoft"],
  "screenType": "sanctions"  // sanctions | full
}
```

**Output:**
```json
{
  "total": 3,
  "cleared": 2,
  "blocked": 1,
  "errors": 0,
  "results": [
    {"entity": "Amazon", "proceed": true, "riskLevel": "LOW"},
    {"entity": "Banco Nacional De Cuba", "proceed": false, "riskLevel": "CRITICAL"},
    {"entity": "Microsoft", "proceed": true, "riskLevel": "LOW"}
  ],
  "summary": "2/3 entities cleared. 1 blocked (OFAC).",
  "screenedAt": "2026-03-26T11:47:00.000Z"
}
```

### 5. `vendor_risk_report`

Detailed Markdown report for documentation and escalation.

**Input:**
```json
{
  "company": "Amazon",
  "format": "brief"  // brief | full
}
```

**Output:**
```json
{
  "company": "Amazon",
  "executiveReport": "## Vendor Risk Assessment: Amazon\n\n**Verdict: ✅ GO**\n\n...",
  "sectionReports": {
    "sanctions": "✅ No OFAC sanctions...",
    "workplace": "✅ OSHA record clean...",
    "environmental": "✅ EPA compliance clean...",
    "govContracts": "✅ Active federal contractor..."
  },
  "verdict": "GO",
  "scores": { ... },
  "generatedAt": "2026-03-26T11:47:00.000Z"
}
```

## Verdict Logic

**BLOCK (0):** Immediate escalation required
- OFAC sanctions match → automatic BLOCK
- Overall score < 30

**CAUTION (1):** Enhanced due diligence required
- Overall score 30-59
- Safety score < 40 OR Environmental score < 40

**GO (2):** Proceed with standard protocols
- Overall score ≥ 60 AND no critical issues
- No OFAC sanctions

## Scoring Breakdown

| Component | Weight | Source | Notes |
|-----------|--------|--------|-------|
| Sanctions | 40% | OFAC SDN List | 100 = clean, 0 = sanctioned |
| Safety | 25% | OSHA Inspections | Based on inspection/violation count |
| Environmental | 25% | EPA ECHO API | Based on facility violations |
| Contractor | 10% | USASpending API | Government contract multiplier |

## Data Sources

All sources are **public US government data**. No API keys required.

1. **OFAC SDN List** (Treasury.gov)
   - URL: `https://www.treasury.gov/ofac/downloads/sdn.csv`
   - Updates: Daily

2. **OSHA Inspections** (Department of Labor)
   - Source: OSHA public API / IMIS database
   - Coverage: Workplace safety violations

3. **EPA ECHO** (Environmental Protection Agency)
   - API: `https://echodata.epa.gov/echo`
   - Coverage: Facility violations, compliance status

4. **USASpending** (Office of Management & Budget)
   - API: `https://api.usaspending.gov/api/v2`
   - Coverage: Federal contract awards

## Usage Examples

### AI Agent: Real-time vendor approval

```javascript
const agent = new ComplianceAgent(mcp);

// User asks: "Can we work with Tesla?"
const result = await agent.tool('can_we_proceed', { entity: 'Tesla' });

if (result.proceed) {
  console.log("✅ Approved. Schedule kickoff call.");
} else {
  console.log("🚫 Blocked. Escalate to legal.");
}
```

### Batch KYC/AML screening

```javascript
const entities = ['Company A', 'Company B', 'Company C'];
const screening = await agent.tool('batch_screen', { entities });

const flagged = screening.results.filter(r => !r.proceed);
if (flagged.length > 0) {
  console.log(`⚠️ ${flagged.length} entities require review`);
}
```

### Supplier selection

```javascript
const vendors = ['Supplier 1', 'Supplier 2', 'Supplier 3'];
const comparison = await agent.tool('compare_vendors', { vendors });

const recommended = comparison.ranked[0];
console.log(`✅ ${recommended.company} is lowest risk (${recommended.verdict})`);
```

## Deployment

### Standby Mode (MCP Server)

The actor runs in **standby mode** on Apify, exposing an MCP HTTP server:

```bash
POST http://localhost:8080/
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "assess_vendor",
    "arguments": { "company": "Tesla" }
  }
}
```

### Local Testing

```bash
cd /Users/youareplan/Documents/Projects/apify-actors/compliance-intel-mcp

# Run assess_vendor locally
apify run --env-file=.env.production -- node src/main.js
```

### Cloud Deployment

```bash
apify push
```

## Limitations

1. **OSHA Data:** HTML parsing-based approximation. Exact match may vary.
2. **Rate Limits:** EPA ECHO and USASpending have built-in rate limits (graceful fallback if unavailable).
3. **Name Matching:** Fuzzy matching on OFAC SDN list (70% threshold). Exact legal entity name recommended.
4. **Jurisdictions:** US-focused (OFAC, OSHA, EPA). Non-US sanctions require additional screening.

## Version

**2.0** — Complete redesign from data API to decision API.

- 5 decision-focused tools
- Integrated scoring from 4 federal sources
- GO/CAUTION/BLOCK verdicts with confidence levels
- Batch processing up to 100 entities

## Author

Built for AI agents. Optimized for decision-making, not data reporting.

---

*OFAC SDN List updated daily. Last compliance review: 2026-03-26*
