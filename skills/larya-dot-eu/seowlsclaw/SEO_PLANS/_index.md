# SEOwlsClaw — SEO Plan Registry
# File: SEO_PLANS/_index.md
# Purpose: Registry of all generated SEO plans (clusters + site architectures).
# Referenced by: /seobrief --plan <plan-id>.<node-id>

---

## Registry Table

| Plan ID | Niche | Mode | Lang | Brand | Nodes | Date | Status | File |
|---------|-------|------|------|-------|-------|------|--------|------|
| _(empty — add rows as plans are generated)_ | | | | | | | | |

> Plans are added here automatically when /seoplan runs.
> Status values: active | paused | completed | archived

---

## How Plans Are Used

### Generating a Plan
```bash
/seoplan "Vintage analog cameras Germany" --lang de --brand jbv-foto
# → Runs research: keyword clusters, SERP analysis, competitor landscape
# → Assigns nodes to tiers: PILLAR / QUICKWIN / FOUNDATION / STRATEGIC
# → Saves: SEO_PLANS/vintage-analog-cameras-de.md
# → Adds row to this index
```

### Referencing a Plan Node in /seobrief
```bash
/seobrief Blogpost "Leica M6 film guide" --plan vintage-analog-cameras-de.qw-01
# → Loads SEO_PLANS/vintage-analog-cameras-de.md → finds node qw-01
# → Extracts: primary_kw, page_type, persona suggestions, internal link targets
# → Uses as defaults — full research still runs on top
```

### Referencing a Plan Node in /write or /writehtml
```bash
/write Blogpost "Leica M6 guide" --from-brief leica-m6-guide-de --plan vintage-analog-cameras-de.qw-01
# → Brief data + plan node data both merge into Step 1 parse
# → Plan's internal link targets override brief's if different
```

---

## Node ID Naming Convention

| Prefix | Tier | Example |
|--------|------|---------|
| `pillar-XX` | Pillar (hub) pages | `pillar-01` |
| `qw-XX` | Quick Win nodes | `qw-01`, `qw-02` |
| `fnd-XX` | Foundation (supporting informational) | `fnd-01` |
| `str-XX` | Strategic (high-value, competitive) | `str-01` |
| `faq-XX` | Standalone FAQ pages | `faq-01` |

---

*Last updated: 2026-04-05 (v0.1)*
*Maintainer: Chris — rows are auto-added by /seoplan*
