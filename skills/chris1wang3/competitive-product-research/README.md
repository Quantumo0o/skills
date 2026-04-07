# Competitive Product Research（竞品调研专家）

> Structured competitive benchmarking across 8 UX dimensions — outputs an actionable HTML report with health score, reusable patterns, and prioritized recommendations.

## What It Does

Give it a research goal and a list of competitor products. The agent collects public information, performs node-by-node benchmarking across 8 dimensions (information architecture, interaction flow, visual design, copy strategy, growth/incentive, edge cases, cross-platform consistency, compliance/accessibility), and generates a **themed HTML report** (Business Blue / Black Gold / Minimal White) with:

- **Competitiveness Health Score** — S/A/B/C grade badge calculated by a deterministic formula
- **Benchmark Matrix** — product × scenario × dimension comparison table
- **Key Findings** — 6-element structured findings with severity and source citations
- **Reusable Patterns** — interaction/visual patterns extracted from ≥2 products
- **Actionable Recommendations** — P0/P1/P2 cards with impact, complexity, owner, and verification plan

Zero-barrier start: just describe your goal + competitor names. Screenshots/recordings are optional but improve accuracy.

## Quick Start

```text
Our app's post conversion rate is only 3%. I want to see how Xiaohongshu and Instagram
help users publish their first post smoothly.
Current state: top-right entry + blank editor + no draft saving.
```

## Workflow

```
Submit goal → Info confirmation checklist → Collection & analysis → HTML report
```

1. **Input**: identify research goal, competitors, core scenarios, focus dimensions
2. **Processing**: collect public info + user materials → path decomposition → gap analysis → pattern extraction
3. **Output**: generate 8-section HTML report (3 themes)

## Report Sections

| # | Section | Description |
|---|---------|-------------|
| 1 | Cover | Research goal, competitor list, health score badge |
| 2 | Executive Summary | 3-5 core conclusions + top-priority action |
| 3 | Scope & Sources | Coverage + source type labels (📸 user material / 🔗 public info / 💡 industry experience) |
| 4 | Benchmark Matrix | Product × scenario node comparison table |
| 5 | Key Findings | Grouped by dimension, each with 6 required elements |
| 6 | Reusable Patterns | Name + applicable scenario + interaction/visual rules + boundary conditions |
| 7 | Recommendations | P0/P1/P2 cards: impact + complexity + dependency + owner |
| 8 | Verification Plan + Source Index | Experiment design + success criteria + full SRC mapping |

## File Structure

| File | Role |
|------|------|
| `SKILL.md` | Master rules (workflow + evaluation framework + quality standards) |
| `references/research-playbook.md` | Methodology reference (decomposition examples, column specs, decision tree, anti-patterns) |
| `references/report-template.html` | HTML report template (3 themes + 8 sections) |

---

# 中文说明

> 给定调研目标和对标产品，自动搜集公开信息进行结构化对标分析，输出带落地建议的 HTML 可视化报告。

## 适用场景

- 新功能规划前：看看竞品怎么做的，少走弯路
- 体验优化选题：找到与竞品的体验差距，确定优化优先级
- 设计规范沉淀：从竞品中提炼可复用的 Pattern 入组件库
- 汇报/分享：一键生成专业对标报告（支持脱敏对外分享版）

## 快速启动

```text
我们APP的发帖转化率只有3%，想看看小红书和Instagram是怎么让用户顺畅发出第一条帖子的。
我方现状：右上角入口+空白编辑器+无草稿保存。
```

只需要明确**调研目标 + 对标产品**即可启动。有截图/录屏可以附上（精度更高），没有也能直接跑。
