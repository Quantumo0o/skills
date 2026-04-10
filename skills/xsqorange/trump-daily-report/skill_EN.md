---
name: trump-daily-report
description: Trump Daily Report - Auto-tracks Trump's social media activity and mainstream media coverage, generates bilingual (Chinese/English) reports with market impact analysis. Runs daily before 9:00 AM.
author: Trump Daily Report Skill
version: 1.0.3
config:
  - name: feishu_group_id
    type: string
    required: true
    description: Feishu group ID for report delivery. Find it in group settings.
  - name: memory_path
    type: string
    required: true
    description: Report archive directory, e.g. ./memory/trump-daily
  - name: target_user_id
    type: string
    required: false
    description: Optional - specify open_id to send report directly to this user only

env:
  - name: TAVILY_API_KEY
    required: true
    description: Tavily search API key for news and market data collection. Get from https://tavily.com
---

# Trump Daily Report

## Overview

Automatically track Trump's social media activity from the prior day and mainstream US media coverage. **Compare with historical reports** to analyze market trend changes and generate predictive **bilingual (Chinese + English) comprehensive reports**.

## ⚠️ Security Notes

This skill requires the following permissions:
- **Read/write local files** - For saving report history
- **Use tavily_search/tavily_extract** - For searching news and market data
- **Send Feishu messages** - For pushing reports to specified group

**Privacy Protection:**
- All data is saved locally by default
- Only report summaries are pushed to your specified Feishu group
- No sensitive personal information is collected or transmitted

**Authentication:**
- **Feishu**: Handled via OpenClaw's built-in Feishu integration. No separate API key needed. Just set `feishu_group_id` in parameters.
- **Tavily**: Configured via `TAVILY_API_KEY` environment variable (see env config below)

## Setup Requirements

Before first use, ensure:

1. **Feishu Group ID** (required) - Set `feishu_group_id` in skill parameters
2. **Local Storage Path** (required) - Set `memory_path` in skill parameters, recommended `./memory/trump-daily`
3. **Tavily API** (required) - Ensure `TAVILY_API_KEY` environment variable is configured

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TAVILY_API_KEY` | Yes | Tavily search API key from https://tavily.com |
| `TRUMP_DAILY_MEMORY_PATH` | No | Path used by trend analysis scripts, same as `memory_path` parameter |

**Note**: `memory_path` (skill parameter) and `TRUMP_DAILY_MEMORY_PATH` (env variable) point to the same directory. Setting one is sufficient.

## Core Features

1. **Bilingual Report Generation** - Simultaneous Chinese + English output
2. **Report History Memory** - Auto-archiving with historical lookup
3. **Trend Comparison Analysis** - Compare with prior reports to identify changes
4. **Situation Change Tracking** - Mark market sentiment and policy direction shifts
5. **Forward-looking Predictions** - Future outlook based on trends

## Information Sources

### Trump's Social Media
- Truth Social (primary source)
- Twitter/X: `realDonaldTrump`
- Detection time range: Prior day 00:00-24:00 (Beijing time)

### US Mainstream Media (by priority)
1. **Bloomberg** - Financial market analysis
2. **CNBC** - Financial TV and market reaction
3. **Reuters** - Breaking news and policy tracking
4. **Wall Street Journal** - In-depth analysis and commentary
5. **Financial Times** - International financial market perspective
6. **New York Times** - Political-economic intersection analysis
7. **CNN / Fox News** - Different political viewpoints

### Keywords Monitored
- `Trump`, `tariff`, `trade war`, `sanction`, `Fed`, `dollar`, `China`, `EU`, `Mexico`
- `executive order`, `policy`, `White House`, `congress`
- Market-related: `market`, `stock`, `rally`, `selloff`, `bond`, `yield`, `oil`, `gold`

## Workflow

### Step 1: Read Historical Reports (Memory Retrieval)

**First check if historical reports exist in `memory_path` directory**

Path: Specified by `memory_path` parameter (default `./memory/trump-daily`)

If historical reports exist, read the 3-5 most recent ones to identify:
- Core topic changes (from tariffs → Iran → other)
- Market sentiment changes (risk-off → risk-on)
- Key price level changes (gold, crude oil, dollar index, etc.)

### Step 2: Collect Trump's Prior Day Social Media Content

Use `tavily_search` (topic=news):

```
Trump Truth Social [yesterday's date]
Trump [yesterday's date] social media
```

Use `tavily_search` (topic=finance) for market-related:

```
Trump tariff [yesterday's date]
Trump Iran [yesterday's date]
Trump market [yesterday's date]
```

### Step 3: Search Mainstream Media Coverage of Trump

Use `tavily_search` (topic=news):

```
Trump [yesterday's date] market impact
Trump [yesterday's date] Bloomberg
Trump [yesterday's date] Reuters
```

Use `tavily_extract` to deeply capture key articles (max 3).

### Step 4: Generate Bilingual Reports (Comparative Analysis)

**Must generate both Chinese and English versions simultaneously**

---

## Chinese Report Template (Default)

```
📊 特朗普动态日报
📅 [YYYY-MM-DD] | 报告序号：[N]
*数据来源：[来源列表] | 查询时间：[时间]*

━━━ 🔄 前期回顾（昨日报告摘要）━━━
• 核心议题：[上期主要话题]
• 市场情绪：[上期情绪判断]
• 关键价格水平：
  - 标普500：±X% [来源]
  - 布伦特原油：$XX [来源]
  - 黄金：$XXXX [来源]
  - 美元指数：XXX [来源]

━━━ 🐦 特朗普社交媒体动态 ━━━
📍 [时间] [平台]
[引用的发言内容]

📍 伊朗/关税/其他重要议题：
[简述]

━━━ 📰 主流媒体反应 ━━━
🔵 [媒体名称]：[标题]
   核心观点：1-2句摘要

━━━ 📉 市场影响分析 ━━━
| 品种 | 本期 | 上期 | 变化 |
|------|------|------|------|
| 标普500 | ±X.X% [来源] | ±X.X% [来源] | ↑/↓/→ |
| 纳斯达克 | ±X.X% [来源] | ±X.X% [来源] | ↑/↓/→ |
| 布伦特原油 | $XX [来源] | $XX [来源] | ↑/↓/→ |
| 黄金 | $XXXX [来源] | $XXXX [来源] | ↑/↓/→ |
| 美元指数 | XXX [来源] | XXX [来源] | ↑/↓/→ |

━━━ 🔀 情境变化分析 ━━━
【新变化】本期vs上期的主要变化：
1. [变化点1]
2. [变化点2]

【市场情绪切换】
  前期：[避险/中性/冒险]
  本期：[避险/中性/冒险]
  变化原因：[简述]

【议题演变】
  [如：从关税战转向中东局势] → [新方向]

━━━ 📈 前瞻预测（1-3日内展望）━━━
• 短期市场可能方向：[看涨/看跌/震荡]
• 主要风险点：
  - ⚠️ [风险1]
  - ⚠️ [风险2]
• 操作建议：[谨慎/积极/观望]
• 需重点关注的事件：[日期/事件]

━━━ ⚠️ 风险提示 ━━━
[标注需要关注的风险点]
```

---

## English Report Template

```
📊 Trump Daily Report
📅 [YYYY-MM-DD] | Report No.: [N]
*Data Sources: [list] | Query Time: [time]*

━━━ 🔄 Prior Day Review ━━━
• Core Topic: [Previous day's main topic]
• Market Sentiment: [Previous sentiment]
• Key Price Levels:
  - S&P 500: ±X% [source]
  - Brent Crude: $XX [source]
  - Gold: $XXXX [source]
  - Dollar Index: XXX [source]

━━━ 🐦 Trump's Social Media Activity ━━━
📍 [Time] [Platform]
[Quoted statement]

📍 Iran/Tariffs/Other Key Issues:
[Brief summary]

━━━ 📰 Mainstream Media Coverage ━━━
🔵 [Media Name]: [Headline]
   Key Takeaway: 1-2 sentence summary

━━━ 📉 Market Impact Analysis ━━━
| Asset | Current | Prior | Change |
|-------|---------|-------|--------|
| S&P 500 | ±X.X% [source] | ±X.X% [source] | ↑/↓/→ |
| Nasdaq | ±X.X% [source] | ±X.X% [source] | ↑/↓/→ |
| Brent Crude | $XX [source] | $XX [source] | ↑/↓/→ |
| Gold | $XXXX [source] | $XXXX [source] | ↑/↓/→ |
| Dollar Index | XXX [source] | XXX [source] | ↑/↓/→ |

━━━ 🔀 Sentiment & Situation Change Analysis ━━━
【New Developments】vs Prior Day:
1. [Change point 1]
2. [Change point 2]

【Market Sentiment Shift】
  Prior: [Risk-off/Neutral/Risk-on]
  Current: [Risk-off/Neutral/Risk-on]
  Reason: [Brief explanation]

【Topic Evolution】
  [e.g., From tariff war → Middle East situation] → [New direction]

━━━ 📈 Forward Outlook (1-3 Day View) ━━━
• Short-term Direction: [Bullish/Bearish/Ranging]
• Key Risk Points:
  - ⚠️ [Risk 1]
  - ⚠️ [Risk 2]
• Trading Advice: [Cautious/Aggressive/Watchful]
• Events to Watch: [Date/Event]

━━━ 🏛️🌏 Regional Market Impact Prediction ━━━
【US Stocks】
• Opening Direction: [Gap Up/Gap Down/Flat]
• Key Sectors:
  - [Benefiting sectors]: [Brief rationale]
  - [Hurt sectors]: [Brief rationale]
• Volatility Outlook: [VIX expected range]
• Key Levels to Watch:
  - S&P 500: Support/Resistance [XXXX / XXXX]
  - Nasdaq: Support/Resistance [XXXX / XXXX]

【Hong Kong Stocks (HSI)】
• Opening Direction: [Gap Up/Gap Down/Flat]
• HSI Key Levels: [Resistance / Support]
• Sector Impact:
  - [Tech stocks]: [Brief rationale]
  - [China concepts/H-shares]: [Brief rationale]
• Southbound Flow: [Net Buy/Net Sell] [source]
• FX Risk: [RMB appreciation/depreciation impact on HK stocks]

【Other Markets (Ex-China)】
• Asia-Pacific:
  - Nikkei 225 (Japan): [Impact direction] [source]
  - KOSPI (Korea): [Impact direction] [source]
  - ASX 200 (Australia): [Impact direction] [source]
• Europe:
  - DAX (Germany): [Impact direction] [source]
  - FTSE 100 (UK): [Impact direction] [source]
• Emerging Markets:
  - EEM/VWO: [Impact direction] [source]
  - Regional exposure: [Mexico/India/Brazil as applicable]

━━━ ⚠️ Risk Alerts ━━━
[Alert points to monitor]
```

### Step 5: Save Reports to Memory Files

**Must execute three save operations:**

1. **Chinese Complete Report Archive**
   - Path: `{memory_path}/{YYYY-MM-DD}_CN.md`
   - Content: Complete Chinese report

2. **English Complete Report Archive**
   - Path: `{memory_path}/{YYYY-MM-DD}_EN.md`
   - Content: Complete English report

3. **Update Summary Index** (Bilingual summary)
   - Path: `{memory_path}/index.md`
   - Format: Bilingual summary + key data

**index.md Format Example:**
```markdown
## 历史报告索引 | Report Index

### 2026-04-08
- **核心议题/Core Topic**：美伊达成两周停火协议 / US-Iran 2-week Ceasefire Agreement
- **市场情绪/Market Sentiment**：🔄 从避险切换至冒险 / 🔄 Risk-off → Risk-on
- **标普500/S&P 500**：+2.5% [source] | **布伦特原油/Brent**：-15%+ [source] | **黄金/Gold**：$XXXX [source] | **美元指数/DXY**：-1%+ [source]
- **风险等级/Risk Level**：⚠️ 中 / ⚠️ Medium

### 2026-04-09
- **核心议题/Core Topic**：停火协议出现裂痕 / Ceasefire Shows Cracks
- **市场情绪/Market Sentiment**：🟡 谨慎乐观 / 🟡 Cautious Optimism
- **标普500/S&P 500**：+0.30% [source] | **VIX**：XX.XX (+X.XX%) [source] | **美元指数/DXY**：-0.16% [source]
- **风险等级/Risk Level**：🔴 高 / 🔴 High
```

### Step 6: Push Bilingual Reports

**Use `message` tool to send two messages to Feishu group:**

1. **Send English version first** (for quick browsing)
2. **Then send Chinese version** (for detailed reading)

- Group ID: `{feishu_group_id}` (configured via parameters)
- Channel: feishu
- Separate Chinese and English reports with divider `━━━━━━━━━━`

## Report Quality Standards

### Data Accuracy Principles (Highest Priority)

⚠️ **Data accuracy is the lifeblood of reports. Fabricating or inferring unverified data is strictly prohibited.**

1. **Source attribution required**:
   - All price/percentage data must include **data source**
   - Format: `[Data Source] | [Query Time]`
   - Example: `S&P 500: +2.5% [Bloomberg, 04/09 08:30]`

2. **Handling unavailable data**:
   - Clearly mark data that couldn't be retrieved as `[Unavailable]` or `[Data TBD]`
   - **Never** use historical averages, expected values, or reasonable estimates to fill gaps
   - Mark missing data positions with `[Unavailable]`, do not speculate or fill

3. **Historical comparison data requirements**:
   - Comparison data must be based on **actual queries of historical reports or databases**
   - **Strictly prohibit** fabricating historical prices from memory or "approximation"
   - If historical data cannot be retrieved, clearly mark `[Prior data unavailable]`

4. **Prohibition on speculation**:
   - Words like "may", "perhaps" in market commentary are predictions and can be included
   - **Specific price/percentage data** must come from actual queries, speculation prohibited
   - If certain data is missing, mark it as missing directly, do not calculate or fill

### Content Quality Standards

5. **Bilingual sync**: Chinese and English versions must be generated simultaneously with consistent content
6. **Comparative analysis required**: Must include "prior vs current" comparison, never report data in isolation
7. **Change markers required**: Any changes in price/sentiment/topics must be clearly marked with direction
8. **Predictions must be evidence-based**: Each prediction must be based on specific data changes
9. **Risk alerts required**: Identified risks must be listed, never omitted

### Data Source Priority

When multiple data sources have different prices:
- Prefer **Bloomberg** price data
- Secondary: **Reuters**, **Yahoo Finance**
- Format: `[Data source, query time]`

## Key Terms Reference

| 中文 | English |
|------|---------|
| 特朗普动态日报 | Trump Daily Report |
| 避险 | Risk-off |
| 冒险/风险偏好 | Risk-on |
| 谨慎乐观 | Cautious Optimism |
| 涨幅收窄 | Rally Fades |
| 停火协议 | Ceasefire Agreement |
| 脆弱 | Fragile |
| 市场情绪 | Market Sentiment |
| 前瞻预测 | Forward Outlook |
| 风险提示 | Risk Alerts |

## Notes

- If Trump made no important statements that day, report should state "No significant public statements yesterday" / "No significant public statements yesterday"
- Report language: Chinese + English bilingual (Chinese primary, English secondary)
- Market data prefers latest trading day data
- For major breaking events (policy statements, emergency announcements), mark with ⚡️ separately
- Historical reports kept for at least 30 days; reports older than 30 days can be archived to `archive/` subdirectory
- All paths and target group IDs are configured via parameters, no hardcoded values
