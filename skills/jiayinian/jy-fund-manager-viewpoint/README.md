# 基金经理观点分析 Skill

基于聚源 MCP 数据库获取基金定期报告，使用 OpenClaw 内置语义能力分析基金经理对特定行业的观点变化。

## 快速开始

### 步骤 1: 准备分析数据

```bash
./run.sh "新能源" "2025Q3" "2025Q4"
```

这会：
1. 筛选新能源行业基金（最多 15 只）
2. 获取 2025Q3 和 2025Q4 的基金季度报告
3. 生成分析请求文件（包含提示词）

### 步骤 2: 使用 OpenClaw 进行语义分析

将生成的提示词（在 `output/analysis_*.json` 的 `prompt` 字段）发送给 OpenClaw。

### 步骤 3: 生成报告

将 OpenClaw 返回的 JSON 结果保存为 `result.json`，然后：

```bash
python3 scripts/generate_report.py output/analysis_*.json result.json
```

## 前置条件

- ✅ mcporter 已安装：`npm install -g mcporter`
- ✅ 聚源 MCP 服务已配置（需要 JY_API_KEY）
- ✅ OpenClaw 已启用 mcporter 技能

## 查询示例

```bash
# 分析新能源基金 2025 年 Q3 vs Q4 的观点变化
./run.sh "新能源" "2025Q3" "2025Q4"

# 分析消费基金 2024 年 Q1 vs Q2 的观点变化
./run.sh "消费" "2024Q1" "2024Q2"
```

## 输出

报告保存在：`~/Desktop/jy-fund-manager-viewpoint/output/`

格式：`<行业>_<季度 1>_vs_<季度 2>_OC.md`

📖 **详细文档**：参见 [SKILL.md](SKILL.md)
