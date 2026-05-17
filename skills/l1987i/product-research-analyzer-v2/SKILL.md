---
name: product-research-analyzer-v2
description: 产品调研分析师 - 自动化产品调研与竞品分析技能，生成飞书产品分析报告。
metadata: {"openclaw": {"requires": {"env": ["FEISHU_APP_ID", "FEISHU_APP_SECRET"], "skills": ["baidu-search", "competitor-analysis"]}, "primaryEnv": "FEISHU_APP_ID", "emoji": "📊"}}
---

# Product Research Analyzer V2 | 产品调研分析师

自动化产品调研与竞品分析技能，生成可直接使用的飞书产品分析报告。

## 使用方式

```bash
# 交互式模式（推荐）
python3 {baseDir}/scripts/research_interactive.py

# 或直接运行
{baseDir}/start.sh
```

## 功能特点

- ✅ 多源搜索与深度研究
- ✅ 批评者视角收集
- ✅ 决策框架蒸馏
- ✅ 四源验证（官方/用户/专家/批评者）
- ✅ 飞书报告自动生成

## 输入参数

- `product_name`: 要调研的产品名称
- `research_questions`: 调研问题（逗号分隔）
- `target_project`: 对标项目名称
- `output_format`: 输出格式（默认 feishu_doc）

## 输出

- 结构化飞书产品分析报告
- 验证覆盖率
- 可信度评级

## 依赖

- FEISHU_APP_ID
- FEISHU_APP_SECRET
- baidu-search skill
- competitor-analysis skill
