# MCP 调用指南

## 工具列表

### jy-financedata-tool

| 工具名称 | 用途 | 参数 |
|---------|------|------|
| FundMultipleFactorFilter | 基金多因子筛选 | query |
| FundClassificationFilter | 基金分类筛选 | query |
| FundPerformanceRank | 基金业绩排名 | query |
| FundManagerInfo | 基金经理信息 | query |
| FundCompanyInfo | 基金公司信息 | query |

### jy-financedata-api

| 工具名称 | 用途 | 参数 |
|---------|------|------|
| FundAnnouncement | 基金公告查询 | query |
| FundHolding | 基金持仓查询 | query |
| FundNetValue | 基金净值查询 | query |
| FundBasicInfo | 基金基本信息 | query |
| StockBasicInfo | 股票基本信息 | query |
| StockBelongIndustry | 股票所属行业 | query |
| FinancialDataAPI | 财务数据 API | query |

## 调用示例

### 筛选行业基金

```bash
mcporter call jy-financedata-tool.FundMultipleFactorFilter query="新能源基金"
```

### 获取基金公告

```bash
mcporter call jy-financedata-api.FundAnnouncement query="交银精选混合 2025 年第 3 季度报告"
```

### 查询基金持仓

```bash
mcporter call jy-financedata-api.FundHolding query="交银精选混合 重仓股"
```

## 返回格式

所有工具返回统一的 JSON 格式：

```json
{
  "code": 0,
  "results": [
    {
      "api_name": "工具名称",
      "table_markdown": "|列 1|列 2|...\n|---|---|...\n|值 1|值 2|..."
    }
  ]
}
```

## 注意事项

1. **所有工具入参均为 query**
2. **优先使用基金名称查询**，代码可能不识别
3. **季度报告披露时间**：季度结束后 15 个工作日内
4. **Markdown 表格解析**：需要处理多行格式
