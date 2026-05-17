---
name: ad-analyzer-yima
description: 广告投放数据分析。当用户上传 Excel/CSV 广告报表，或说"帮我分析投放数据/看看这个报表/数据有没有问题/哪个计划效果差"时触发。自动识别所有表头列，无需预设字段名，汇总全部指标，检测异常，输出分析报告和优化建议。支持巨量引擎、腾讯广告、Meta Ads、Google Ads、快手等平台导出格式。
homepage: https://clawhub.ai/ming0429/ad-analyzer-yima
version: 1.0.0
author: guojiaming
tags: [advertising, analytics, excel, csv, 广告分析, 投放优化, 数据可视化]
metadata:
  clawdbot:
    emoji: 📊
    requires:
      bins: [python3]
      env: []
---

# 广告数据分析 Skill

分析用户上传的广告报表文件，自动识别所有列，汇总指标，发现异常，输出优化建议。

## Setup

无需任何配置，开箱即用。支持 `.xlsx` / `.xls` / `.csv` 格式，兼容 UTF-8 和 GBK 编码。

## Usage

### 第一步：读取文件，识别所有列

```python
import pandas as pd

# 自动识别编码和格式
try:
    df = pd.read_excel("report.xlsx")
except:
    try:
        df = pd.read_csv("report.csv", encoding="utf-8")
    except:
        df = pd.read_csv("report.csv", encoding="gbk")

# 输出所有列名和前3行，让 AI 理解表头含义
print("列名：", df.columns.tolist())
print("行数：", len(df))
print(df.head(3).to_string())
```

读取后，根据列名语义判断：
- **日期列**：值格式为日期（2024-01-01、20240101 等）
- **维度列**：文字类，如广告计划、广告组、地区、性别、创意名称
- **指标列**：数值类，全部列出，一列不漏

### 第二步：汇总所有数值指标

```python
# 识别所有数值列（不预设列名，完全由表头决定）
numeric_cols = df.select_dtypes(include='number').columns.tolist()
text_cols = df.select_dtypes(include='object').columns.tolist()

print("=== 全量指标汇总 ===")
print(df[numeric_cols].sum().to_string())

print("\n=== 均值 ===")
print(df[numeric_cols].mean().round(2).to_string())
```

### 第三步：按维度分组分析

```python
# 按每个维度列分组，汇总所有数值指标
for col in text_cols:
    if df[col].nunique() <= 50:  # 维度值不超过50个时分析
        grouped = df.groupby(col)[numeric_cols].sum()
        grouped = grouped.sort_values(numeric_cols[0], ascending=False)
        print(f"\n=== 按【{col}】分组 ===")
        print(grouped.to_string())
```

### 第四步：趋势分析（有日期列时）

```python
# 检测日期列
date_col = None
for col in df.columns:
    try:
        pd.to_datetime(df[col])
        date_col = col
        break
    except:
        continue

if date_col:
    df[date_col] = pd.to_datetime(df[date_col])
    daily = df.groupby(date_col)[numeric_cols].sum().sort_index()
    print("\n=== 日期趋势 ===")
    print(daily.to_string())
```

### 第五步：异常检测

```python
# 对每个数值列检测异常波动
for col in numeric_cols:
    mean_val = df[col].mean()
    std_val = df[col].std()
    outliers = df[df[col] > mean_val + 2 * std_val]
    if len(outliers):
        print(f"【{col}】异常高值：{len(outliers)} 行，均值 {mean_val:.2f}，阈值 {mean_val + 2*std_val:.2f}")
```

### 第六步：输出分析报告

按以下结构输出（Markdown 格式）：

```
## 投放概览
[2-3句总结整体表现]

## 数据详情
[全量指标汇总表格]
[主维度分组表格，按第一个数值指标降序]

## 关键发现
1. [最重要的发现，附具体数字]
2. [第二重要发现]
3. [异常情况说明]

## 优化建议
- [具体可执行的动作，如"暂停XX计划"、"增加XX维度预算"]

## 需关注
[数据缺口或需人工核查的问题]
```

## Notes

- **完全动态识别**：不预设任何列名，表头是什么就分析什么
- **全列覆盖**：所有数值列都会参与汇总和分析，不遗漏
- **不对接 API**：只处理本地上传的文件，数据不外传
- **编码兼容**：自动识别 UTF-8 / GBK，兼容国内平台导出的 CSV
- **大文件处理**：超过 10 万行建议按时间段拆分上传

## Examples

**场景 1：巨量引擎周报分析**
> "这是上周巨量引擎的投放报表，帮我看看哪些计划效果差"

执行流程：
1. 读取文件，识别列名（日期、广告计划、消费、展示数、点击数、转化数）
2. 汇总全量：总消费、总点击、总转化
3. 按"广告计划"分组，找出消费最高和转化最差的计划
4. 检测异常：某计划 CPA 超均值 150% 则标红
5. 输出建议：暂停高 CPA 计划，预算转移至效果最优计划

**场景 2：多维度交叉分析**
> "帮我看看不同地区、不同时段的投放效果"

执行流程：
1. 识别维度列：地区、时段
2. 分别按地区、时段分组汇总所有数值指标
3. 找出高效地区和黄金时段
4. 输出交叉分析建议
