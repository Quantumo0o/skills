#!/bin/bash
# SEO Playbook Optimizer — Main entry point
# Usage: ./analyze.sh --keyword "keyword" --content "..." [--url "url"] [--stage new|growing|mature] [--output file.md]

set -euo pipefail

KEYWORD=""
CONTENT=""
URL=""
STAGE="new"
OUTPUT_FILE=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --keyword) KEYWORD="$2"; shift 2 ;;
    --content) CONTENT="$2"; shift 2 ;;
    --url)     URL="$2";     shift 2 ;;
    --stage)   STAGE="$2";   shift 2 ;;
    --output)  OUTPUT_FILE="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$KEYWORD" && -z "$URL" ]]; then
  echo "Usage: $0 --keyword <keyword> [--content <page_content>] [--url <url>] [--stage new|growing|mature]"
  exit 1
fi

TIMESTAMP=$(date +"%Y-%m-%d %H:%M")

# Build prompt for AI analysis
PROMPT="You are a professional SEO analyst following a proven internal SOP playbook. Produce a comprehensive, actionable SEO report in English.

## Target
Keyword: ${KEYWORD:-'(from URL)'}
URL: ${URL:-(not provided)}
Site Stage: ${STAGE} (new=<3mo, growing=3-12mo, mature=>12mo)

## Page Content to Analyze:
${CONTENT:-(not provided — analyze keyword only)}

---

## Internal SOP Rules (apply strictly):

### Core Principle
- Page 1 rankings are won by backlinks. Top 3 rankings are won by content quality.

### Keyword Strategy
- Identify: primary keyword + semantic variants with the same search intent
- Apply Ahrefs-style metrics: Volume, Keyword Difficulty (KD), Traffic Potential, Parent Topic
- Expand angles using: Who, What, When, Where, Why, How

### Title Tag & H1 Rules
- Title Tag: include high-volume keyword + eye-catching modifier, keep under 60 characters
- H1: concise, complete keyword, not forced for SEO
- Three logical patterns: Parallel (&//) | Call to Action | Progressive (elaboration)
- Provide 3 Title Tag alternatives + 1 H1 recommendation

### Article Structure SOP
- Structure: Title Tag → Meta Description → H1 → H2s → H3s → FAQs → Conclusion
- Expand H2 angles using 5Ws+1H framework
- Benchmark top 5 ranking pages for content gaps
- Meta description: 150-160 characters, include clear CTA

### Internal Link Rules
- 2-5 internal links per page
- Anchor text: mix keyword anchors, brand anchors, naked URLs, and generic anchors
- Same anchor text must ALWAYS point to the same destination (never split)
- Pillar page links → child pages; child page links → parent page + sibling pages
- Homepage anchor: use the homepage's primary target keyword

### Backlink Strategy by Site Stage
New site (<3 months):
  - Quora links: 5 per important page
  - Forum/Comment links: 5 per page, spread across ~20 pages
  - Guest post: 1-2 per important page MAX
  - Always build pillow links (web 2.0, forums) BEFORE guest posts
  - Never spike links on a single page — Google will flag it

Growing site (3-12 months):
  - Target pages ranking positions 8-22 with focused link building
  - Prioritize pages with existing sales + traffic momentum
  - Gradually increase guest post frequency

Mature site (>12 months):
  - Primary target: pages in positions 8-13 → push to top 5
  - Sales top-20 pages: 1 maintenance link each
  - Mirror competitor backlink velocity

### Anchor Text Rules
- Forum/Quora: brand name OR naked URL OR generic text (never exact-match keyword)
- Guest post: exact-match keyword anchor acceptable (target 20-30% of total anchor mix)
- Always vary anchor text naturally across all link types

### GEO Strategy — Claude News Flywheel (SEO + Generative Engine Optimization)
GEO = optimizing to be cited and referenced by AI search engines (ChatGPT, Perplexity, Gemini, Claude) in addition to traditional Google SEO.

Core insight: Use Claude to collect information → rewrite as original news articles → publish to a /news section consistently → accumulate topical authority → Google ranks the site higher AND AI engines start citing the site as an authoritative source.

Why it works:
- Google rewards consistent fresh content in a niche (topical authority)
- AI search engines crawl and reference authoritative domain sources
- News content compounds: 200 articles > 10 pillar pages for keyword coverage
- Dual flywheel: SEO traffic + AI citation traffic

Flywheel implementation:
1. Pick a focused niche topic cluster
2. Use Claude to research + rewrite 2-5 news articles per week (not copy-paste — synthesize + add original angle)
3. Publish to /news or /blog with full on-page SEO (title tag, meta, H1, internal links)
4. Link from each news article to 1-2 money pages (internal link juice)
5. Track: after 3-6 months, check if Google recognizes topical authority (rankings rising across cluster)
6. Track GEO: search your niche in ChatGPT/Perplexity — does your site appear as a cited source?

Output a GEO section in the report with a concrete news content plan for the given keyword/niche.

### Link Building Quality Checklist
- Links must be permanent (not marked as sponsored or guest post)
- No rel='sponsored' or rel='ugc' attributes
- No subdomain placement — main domain only
- Dofollow preferred; nofollow is acceptable for diversity
- Verify no indexing issues on live links

---

## Output Format:

# SEO Audit Report
**Keyword:** [keyword] | **Site Stage:** [stage] | **Date:** ${TIMESTAMP}

---

## 1. Keyword Matrix

| Type | Keyword | Est. Monthly Volume | Competition (KD) | Search Intent |
|------|---------|-------------------|-----------------|---------------|
| Primary | ... | ... | ... | ... |
| Variant | ... | ... | ... | ... |
| Long-tail | ... | ... | ... | ... |
| Question | ... | ... | ... | ... |

**Key Insight:** (2-3 sentences on keyword opportunity)

---

## 2. Title Tag & H1 Optimization

**Current Title Tag:** (score it if content provided, else N/A)

**Recommended Options:**
- Option A: [title] (Logic: Parallel)
- Option B: [title] (Logic: Call to Action)
- Option C: [title] (Logic: Progressive)

**Recommended H1:** [h1]

**Meta Description:** [150-160 char English meta description with CTA]

---

## 3. Article Structure

**Recommended Structure:**
- H1: [title]
- H2-1: [angle — What]
- H2-2: [angle — Why]
- H2-3: [angle — How]
- H2-4: [angle — Who/When/Where as needed]
- H2-FAQ: Frequently Asked Questions (3-5 Qs)
- H2-Conclusion: Summary + CTA

**Content Gaps:** (what top-ranking competitors cover that this page is missing)

---

## 4. Internal Link Audit

| Anchor Text | Destination Page | Compliance |
|-------------|-----------------|------------|
| ... | ... | ✅/⚠️/❌ |

**Issues Found:** (if any)
**New Internal Link Recommendations:** (3-5 actionable suggestions)

---

## 5. Backlink Plan

**Current Stage:** [new/growing/mature]

**This Month's Link Building Plan:**
| Type | Quantity | Target Page | Anchor Text Strategy |
|------|----------|-------------|---------------------|
| Quora | ... | ... | ... |
| Forum/Comment | ... | ... | ... |
| Guest Post | ... | ... | ... |

**Risk Warnings:** (SOP-based cautions for this site's stage)

---

## 6. GEO Strategy — Claude News Flywheel

**Niche Topic Cluster:** [identify the best cluster for this site/keyword]

**Recommended News Article Topics (first 10):**
1. ...
2. ...
3. ...
4. ...
5. ...
6. ...
7. ...
8. ...
9. ...
10. ...

**Publishing Cadence:** [recommended frequency based on site stage]

**Internal Link Plan:** [how each news article should link to money pages]

**GEO Tracking:** Check these AI engines monthly to see if site gets cited:
- ChatGPT: search "[niche] best resources" or "[topic] guide"
- Perplexity: search same queries
- Google AI Overviews: check if site appears in AI summaries

**Expected Timeline:** [when to expect GEO traction based on content volume]

---

## 7. Execution Priority

**Quick Wins (This Week):**
1. ...
2. ...

**Mid-term (1 Month):**
1. ...
2. ...

**Long-term (3 Months):**
1. ...

---

## 8. SEO Health Score

| Dimension | Score (/100) | Key Issue |
|-----------|-------------|-----------|
| Keyword Coverage | xx | ... |
| Page Structure | xx | ... |
| Internal Links | xx | ... |
| Backlink Strategy | xx | ... |
| Content Quality | xx | ... |
| GEO Readiness | xx | ... |
| **Overall** | **xx** | ... |"

# Run AI analysis
echo "Analyzing SEO data, please wait..."
echo ""

SESSION_ID="seo-$(date +%s)"
RESULT=$(openclaw agent --local --session-id "$SESSION_ID" --json -m "$PROMPT" 2>/dev/null)

# Extract text from JSON response
REPORT=$(echo "$RESULT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
payloads = data.get('payloads', [])
texts = [p.get('text','') for p in payloads if p.get('text')]
print('\n'.join(texts))
" 2>/dev/null)

if [[ -z "$REPORT" ]]; then
  REPORT="$RESULT"
fi

echo "$REPORT"

# Save to file if specified
if [[ -n "$OUTPUT_FILE" ]]; then
  echo "$REPORT" > "$OUTPUT_FILE"
  echo ""
  echo "Report saved to: $OUTPUT_FILE"
fi
