---
name: dream
description: "Dream self-evolution skill for nightly memory distillation. Inspired by Claude Code KAIROS, eo-ability-dream, and openclaw-auto-dream. Two-phase: daily logs capture everything, then AI distills into structured topics, Pattern Library, and scored health-driven memory system. Optional: SwarmRecall cloud tier for advanced deduplication and contradiction resolution (requires SWARMRECALL_API_KEY). Trigger when user says dream, or on cron schedule."
metadata:
  openclaw:
    requires:
      env:
        - OPENCLAW_WORKSPACE
        - OPENCLAW_BIN
        - OPENCLAW_SCRIPT
        - OPENCLAW_PATH
        - DREAM_MORNING_JOB_ID
        - DREAM_NIGHT_JOB_ID
      bins:
        - python3
    notes: |
      Required env vars: OPENCLAW_WORKSPACE (workspace root), OPENCLAW_BIN (node binary),
      OPENCLAW_SCRIPT (openclaw entry point), OPENCLAW_PATH (openclaw binary path),
      DREAM_MORNING_JOB_ID / DREAM_NIGHT_JOB_ID (cron job IDs for date injection).
      
      Cron editing: update-cron-date.py modifies dream cron job messages via 'openclaw cron edit'.
      This is a privileged action. Use --confirm flag to enable: python update-cron-date.py --confirm
      
      SwarmRecall (optional): SWARMRECALL_API_KEY enables cloud deduplication/contradiction resolution.
---

# Dream — Nightly Memory Distillation & Self-Evolution

## Concept

Three-skill fusion:
- **Claude Code KAIROS**: append-only logs → distilled topics → MEMORY.md index
- **eo-ability-dream**: Pattern Library extracted from recurring errors
- **openclaw-auto-dream**: importance scoring, health metrics, archive遗忘曲线

**Phase 1 — Daily Log** (always active)
- After each significant conversation event, append to `memory/logs/YYYY/MM/YYYY-MM-DD.md`
- Append-only, never overwrite or reorganize
- Include: events, decisions, user preferences, corrections, observations, completed tasks

**Phase 2 — Dream Distillation** (on cron or manual trigger)
- Cron triggers AI sub-session
- AI reads the day's log AND `.learnings/` files from self-improving-agent
- Analyzes failure patterns (from ERRORS.md)
- Distills key insights into **topic files** with frontmatter
- Extracts recurring errors → **Pattern Library**
- Computes **importance scores** and **health metrics**
- Archives low-importance stale entries
- Updates `MEMORY.md` as the INDEX of topic files
- Writes dream report with growth metrics

## Integration with self-improving-agent

Dream reads and promotes entries from the self-improving-agent skill:

```
.learnings/
├── LEARNINGS.md        # Corrections, insights, best practices
├── ERRORS.md          # Command failures, integration errors
└── FEATURE_REQUESTS.md # User-requested capabilities
```

**Distillation logic:**
- Corrections (category: `correction`) → promote to `feedback` topic
- Recurring errors (3+ occurrences) → extract to Pattern Library
- Errors with fixes → promote to relevant topic
- Feature requests → create `project` topic if validated
- Best practices → promote to relevant topic
- Mark promoted entries as `status: promoted`

## Pattern Library (from eo-ability-dream)

Patterns are reusable response templates extracted from recurring learnings:

```
memory/patterns/
└── p-xxx.md           # Pattern files with trigger + response
```

**Pattern format:**
```yaml
---
name: pattern名称
trigger: 什么情况下触发
response: 如何响应
examples: [案例1, 案例2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Extraction criteria:**
- Same error occurs ≥3 times across logs
- User-corrected mistake ≥2 times
- Non-obvious fix discovered through debugging

## Memory Taxonomy

Four memory types:

- **user** — User preferences, role, goals, communication style
- **feedback** — User corrections and confirmations
- **project** — Project context, decisions, deadlines, tools in use
- **reference** — External systems, links, credentials locations

## Directory Structure

```
memory/
├── logs/
│   └── YYYY/MM/YYYY-MM-DD.md   # Daily append-only logs
├── topics/                      # Distilled topic memories
│   ├── user_xxx.md
│   ├── feedback_xxx.md
│   ├── project_xxx.md
│   └── reference_xxx.md
├── patterns/                    # Pattern Library (from eo-ability-dream)
│   └── p-xxx.md               # Reusable patterns
├── episodes/                    # Project narratives (from openclaw-auto-dream)
├── procedures.md               # Workflow preferences
├── archive.md                  # Compressed old entries
├── dream-log.md               # Dream cycle reports
├── index.json                 # Entry metadata (v3.0 schema)
└── MEMORY.md                   # INDEX only — points to topics

.learnings/                     # self-improving-agent
├── LEARNINGS.md
├── ERRORS.md
└── FEATURE_REQUESTS.md
```

## Health Score (from openclaw-auto-dream)

Five metrics measured each dream cycle:

| Metric | Weight | Formula |
|--------|--------|---------|
| Freshness | 0.25 | entries_referenced_last_30_days / total |
| Coverage | 0.25 | categories_updated_last_14_days / 10 |
| Coherence | 0.20 | entries_with_relations / total |
| Efficiency | 0.15 | max(0, 1 - line_count/500) |
| Reachability | 0.15 | graph connectivity (connected components) |

**Health Score** = weighted sum × 100 (0-100)

| Score | Rating |
|-------|--------|
| 80-100 | Excellent |
| 60-79 | Good |
| 40-59 | Fair |
| 20-39 | Poor |
| 0-19 | Critical |

## Importance Scoring (from openclaw-auto-dream)

```
importance = base_weight × recency_factor × reference_boost
```

- **base_weight**: default 1.0, 🔥HIGH = 2.0, ⚠️PERMANENT = 1.0 (skip formula)
- **recency_factor**: `max(0.1, 1.0 - days/180)`
- **reference_boost**: `max(1.0, log2(refs + 1))`

**Archive conditions** (all must be true):
- days_since_referenced > 90
- importance < 0.3
- NOT ⚠️PERMANENT, NOT 📌PIN, NOT in episodes/

## Optional: SwarmRecall Cloud Tier

**Only active if `SWARMRECALL_API_KEY` environment variable is set.**

SwarmRecall provides advanced cloud-side operations for large memory stores:
- **Tier 1 (server-side)**: deduplication clustering, importance decay, stale pruning
- **Tier 2 (agent-driven)**: contradiction resolution, session summarization, knowledge graph enrichment

### Setup
1. Get an API key: `POST /api/v1/register` with `{ "name": "<agent-name>" }`
2. Set environment variable: `SWARMRECALL_API_KEY=<your-key>`
3. SwarmRecall is now active — Tier 1 runs automatically on configured interval

### SwarmRecall Endpoints Used
- `POST /api/v1/dream` — start dream cycle
- `POST /api/v1/dream/execute` — run server-side ops (decay, prune)
- `GET /api/v1/dream/candidates/duplicates` — find duplicate clusters
- `GET /api/v1/dream/candidates/contradictions` — find conflicting memories
- `GET /api/v1/dream/candidates/stale` — find prunable memories
- `PATCH /api/v1/dream/:id` — report dream results

### Privacy
- Data transmitted over HTTPS to `swarmrecall-api.onrender.com`
- Only your agent's existing memory data is sent — no new external data collected
- Archived memories are soft-deleted (recoverable)
- Tenant-isolated by owner ID and agent ID

## MEMORY.md Index Format

MEMORY.md is an INDEX ONLY — one line per topic:

```markdown
# MEMORY.md — Long-Term Memory Index

_Last updated: YYYY-MM-DD_

## Topics
- [Title](topics/file.md) — one-line description
- [Title](topics/file.md) — one-line description

## Patterns
- [pattern-name](patterns/p-xxx.md) — trigger summary

## Stats
- Total entries: N | Health: N/100 | Streak: N dreams
```

## Daily Log Format

Append to `memory/logs/YYYY/MM/YYYY-MM-DD.md` after each significant event:

```markdown
## HH:MM

- [type] content description
- completed: task name
- decision: what was decided
- correction: user feedback received
- insight: what was learned
```

Types: `event` | `decision` | `correction` | `completed` | `insight` | `error` | `question`

## Cron Configuration

Two cron jobs:
- **dream-morning**: 7:00 AM
- **dream-night**: 10:00 PM
- `--no-deliver` (writes to file only)

Cron message is updated daily via `update-cron-date.py` script which injects current date.

## Dream Distillation Steps

When cron triggers:

1. Read `memory/logs/{date}.md`
2. Read `.learnings/LEARNINGS.md`, `.learnings/ERRORS.md`, `.learnings/FEATURE_REQUESTS.md`
3. Read `MEMORY.md`, topic files, `index.json`, `procedures.md` for context
4. **Snapshot BEFORE**: count entries, decisions, lessons, procedures
5. Analyze failures:
   - Count occurrences of each error in ERRORS.md
   - Identify recurring patterns (≥3 occurrences)
   - Extract root cause
6. Distill insights → update/create topic files with frontmatter
   - Recurring errors → create/update Pattern in `patterns/`
   - Link to promoted `.learnings/` entries
7. Update `index.json` entry metadata (id, importance, tags, related)
8. Compute health metrics → update `index.json` stats
9. Archive eligible entries → append to `archive.md`
10. Update `MEMORY.md` index (max 200 lines)
11. **Snapshot AFTER**: calculate deltas
12. Write dream report to `memory/dreams/{date}.md` and `dream-log.md`
13. Regenerate `dashboard.html` if exists
14. **[Optional SwarmRecall]**: If `SWARMRECALL_API_KEY` is set:
    - Start dream cycle: `POST /api/v1/dream`
    - Run server-side ops: `POST /api/v1/dream/execute`
    - Fetch duplicate clusters → merge redundant memories
    - Fetch contradictions → resolve conflicting entries
    - Update dream cycle with results

## Dream Report Format

```markdown
# 🌙 Dream Report — {date}

## Status
- Dream #: N
- Total entries: {BEFORE} → {AFTER} ({percent}% growth)
- Health: {score}/100 (freshness={f}, coverage={c}, coherence={ch}, efficiency={e}, reachability={r})

## Analysis
- Recurring errors found: {list}
- Root causes identified: {analysis}

## Patterns Updated
- {pattern_name}: {change}

## Health Insights
- {insight based on health metrics}

## Suggested Improvements
- {improvement_1} (triggered by: {metric} < threshold)

## Tomorrow's Focus
- {focus}
```

## First Dream (post-install)

After initial setup, run a full scan of ALL existing daily logs (not just last 3 days).
Compare before/after metrics and send user a First Dream Report showing:
- How many logs scanned, entries extracted
- Before → After table
- Personalized reflection based on actual log content

## User Prompts

- "dream report" / "梦境报告" → read and display latest dream report
- "dream" / "做梦" → run distillation now
- "/dream status" → show health score, pattern count, streak, stale threads

## Scripts

- `dream.py` — main distillation script
- `update-cron-date.py` — runs daily to inject current date into cron messages

## 技能整合说明

### 已整合
- **self-improving-agent** → dream 的日志层（`.learnings/`），无需单独使用

### 其他AI自我进化技能定位
- **recursive-self-improvement**：代码级自修复系统（错误检测→根因分析→修复→测试→验证），与 dream 是不同维度，可共存
- dream = 记忆蒸馏 + Pattern提取 + 健康评分
- recursive-self-improvement = 代码错误自动修复
