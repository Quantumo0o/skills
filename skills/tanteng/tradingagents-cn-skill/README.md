# TradingAgents-CN-Skill

基于 [TradingAgents-CN](https://github.com/hsliuping/TradingAgents-CN) 多智能体框架的股票分析 OpenClaw Skill。

## 功能特性

- **多智能体并行分析**：6 个专业分析师同时工作
  - 多头分析师 / 空头分析师
  - 技术分析师 / 基本面分析师
  - 新闻分析师 / 社交媒体分析师

- **辩论决策机制**：研究经理主持多空辩论，给出「买入/卖出/持有」决策

- **交易计划制定**：交易员制定具体计划，包含目标价位和仓位建议

- **三方风险评估**：激进/中性/保守三派辩论，全面评估风险

- **专业 PDF 报告**：生成完整分析报告，支持下载

## 支持输入

- 股票代码（AAPL、600519、HK.00700 等）
- 文本描述（新闻、财报摘要、雪球帖子等）
- 截图/图片（K线图、财报截图等，OCR 自动提取）

## 使用方式

在 OpenClaw 中通过触发词调用：

```
分析一下 AAPL 这只股票
帮我生成一份股票分析报告
我想了解一下茅台的基本面
```

## 技术架构

```
输入解析 → 并行分析(6智能体) → 多空辩论 → 研究经理决策
    → 交易员计划 → 三方风险辩论 → 风险经理决策 → PDF生成
```

## 文件结构

```
tradingagents-cn-skill/
├── SKILL.md                    # Skill 定义
├── scripts/
│   ├── analyst_multi.py        # 多智能体分析引擎
│   ├── pdf_generator.py        # PDF 报告生成
│   └── reports/                # PDF 输出目录
└── references/                 # 各角色 Prompt 模板
    ├── bull_prompt.md          # 多头分析师
    ├── bear_prompt.md          # 空头分析师
    ├── tech_prompt.md          # 技术分析师
    ├── fundamentals_prompt.md  # 基本面分析师
    ├── news_prompt.md          # 新闻分析师
    ├── social_prompt.md        # 社交媒体分析师
    ├── manager_prompt.md       # 研究经理
    ├── trader_prompt.md        # 交易员
    ├── risk_debate_prompt.md   # 三方风险辩论
    └── risk_manager_prompt.md  # 风险经理
```

## 免责声明

本项目仅供研究和学习目的，不构成任何形式的投资建议。投资有风险，决策需谨慎。

## 相关项目

- [TradingAgents-CN](https://github.com/hsliuping/TradingAgents-CN) - 原版多智能体 LLM 金融交易框架
- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架
