---
name: tradingagents-cn-skill
description: |
  股票分析报告生成工具。基于 TradingAgents-CN 多智能体框架，对股票进行全面分析并生成专业 PDF 报告。
  触发场景：
  (1) 用户要求分析股票、股票分析、股票研究
  (2) 用户要求生成股票报告、PDF 报告
  (3) 用户提供股票代码、文本描述或截图进行分析
  (4) 用户询问买入、卖出、持有建议
  (5) 用户要求技术分析、基本面分析、风险评估
---

# TradingAgents-CN Skill

基于 TradingAgents-CN 多智能体框架的股票分析 skill。通过多智能体辩论机制生成专业股票分析 PDF 报告。

## 重要提醒

**必须先使用 web_search MCP tool 获取真实新闻数据，才能生成包含新闻的 PDF 报告。**

如果跳过了获取新闻数据的步骤，生成的 PDF 将显示"暂无新闻数据"。

## 工作流程

```
Step 1: 解析股票代码 → Step 2: web_search 获取新闻 → Step 3: 调用 Python 脚本生成 PDF
```

### Step 1: 解析股票代码

识别用户提供的股票代码：如 `AAPL`、`600519`、`HK.00700`

### Step 2: 获取新闻（必须执行！）

**使用 web_search MCP tool 获取至少 5-10 条近期新闻：**

```
web_search: "{股票代码} {股票名称} 最新新闻"
web_search: "{股票代码} 财报 业绩"
web_search: "{股票名称} 分析师评级"
```

**将搜索结果整理为 news_data 格式：**
```python
news_data = [
    {
        "title": "新闻标题",
        "date": "2024-01-01",
        "source": "媒体来源",
        "summary": "新闻摘要",
        "sentiment": "偏多/偏空/中性"
    },
    # ... 至少 5-10 条
]
```

### Step 3: 生成 PDF

调用 Python 脚本生成 PDF：

```python
import sys
sys.path.insert(0, "/root/.openclaw/workspace/skills/tradingagents-cn-skill/scripts")
from analyst_multi import StockAnalyst
from pdf_generator import ReportGenerator

# 执行分析（传入真实新闻数据）
analyst = StockAnalyst()
result = analyst.analyze(
    stock_code="AAPL",
    news_data=news_data,  # 重要！必须传入新闻数据
)

# 生成 PDF
generator = ReportGenerator()
pdf_path = generator.generate(
    analysis_result=result,
    output_dir="/root/.openclaw/workspace/skills/tradingagents-cn-skill/scripts/reports"
)
```

## 新闻获取示例

假设用户要求分析 `AAPL`：

1. **搜索新闻**：
   - `web_search("AAPL Apple 最新新闻 2024")`
   - `web_search("Apple Q4 2024 earnings results")`
   - `web_search("iPhone sales 2024 latest")`

2. **整理新闻数据**：
   ```python
   news_data = [
       {"title": "Apple 发布 Q4 财报，营收超预期", "date": "2024-11-01", "source": "Bloomberg", "summary": "营收同比增长 8.1%", "sentiment": "偏多"},
       {"title": "iPhone 16 销量创历史新高", "date": "2024-10-28", "source": "Reuters", "summary": "需求旺盛", "sentiment": "偏多"},
       # ... 至少 5-10 条
   ]
   ```

3. **生成 PDF**（传入 news_data）

## 报告输出

PDF 文件保存到：
```
/root/.openclaw/workspace/skills/tradingagents-cn-skill/scripts/reports/
```

文件名格式：`{股票代码}_{日期}_{时间}.pdf`

## 参考文档

详细 prompt 模板见 `references/` 目录：
- `bull_prompt.md` - 多头分析师
- `bear_prompt.md` - 空头分析师
- `tech_prompt.md` - 技术分析师
- `fundamentals_prompt.md` - 基本面分析师
- `news_prompt.md` - 新闻分析师
- `social_prompt.md` - 社交媒体分析师
- `manager_prompt.md` - 研究经理
- `trader_prompt.md` - 交易员
- `risk_debate_prompt.md` - 风险辩论
- `risk_manager_prompt.md` - 风险经理

## 输出语言

所有分析内容使用**中文**输出。
