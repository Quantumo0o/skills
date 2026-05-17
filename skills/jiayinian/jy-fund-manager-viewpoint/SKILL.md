---
name: jy-fund-manager-viewpoint
description: 基于 MCP 聚源金融数据库分析基金定期报告中基金经理对特定行业的观点变化，对比不同季度的共识与分歧，输出带引用标注的结构化报告。使用场景：当用户需要分析某行业基金经理的观点演变、对比季度间共识与分歧、生成基金经理观点分析报告时触发。Analyze fund managers' viewpoint changes on specific industries based on periodic fund reports from the MCP GILData Financial Database. Compare consensus and divergence across different quarters and output a structured report with citations. Use case: Triggered when users need to analyze the evolution of fund managers' views on an industry, compare consensus and divergence between quarters, or generate fund manager viewpoint analysis reports.
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["node", "npm", "mcporter", "python3"]
    install:
      - id: install-mcporter
        kind: node
        package: mcporter
        label: Install mcporter via npm
---

# 基金经理观点分析 Skill

基于聚源 MCP 数据库获取基金定期报告，使用 OpenClaw 内置语义能力分析基金经理对特定行业的观点变化，生成带引用标注的结构化报告。

## 功能范围

- ✅ 筛选目标行业主题基金（最多 15 只）
- ✅ 获取基金定期报告全文（季度报告）
- ✅ OpenClaw 语义提取基金经理对行业的观点
- ✅ 识别季度内共识（至少 2 只基金的相似观点）
- ✅ 识别季度内分歧（不同基金的不同看法）
- ✅ 对比两个季度的观点变化（情绪、主题、策略）
- ✅ 生成结构化 Markdown 报告（带引用溯源）

## 查询建议

**查询要素：** 行业名称、季度 1、季度 2、输出目录（可选）

**查询写法：**
```
分析 <行业> 基金在 <季度 1> 和 <季度 2> 的观点变化
对比 <季度 1> 和 <季度 2> <行业> 行业基金经理的观点
生成 <行业> 行业 <季度 1> vs <季度 2> 基金经理观点分析报告
```

**行业示例：** 新能源、消费、人工智能、医药、金融、制造、周期、房地产

**季度格式：** `2025 年第三季度`、`2025Q3`、`2024Q1`

## 查询示例

```bash
# 分析新能源基金 2025 年 Q3 vs Q4 的观点变化
./run.sh "新能源" "2025Q3" "2025Q4"

# 分析消费基金 2024 年 Q1 vs Q2 的观点变化
./run.sh "消费" "2024Q1" "2024Q2"

# 指定输出目录
./run.sh "人工智能" "2025Q3" "2025Q4" "~/Desktop/reports"
```

## 环境检查与配置

**每次使用本技能前，必须先检查 mcporter 安装和 MCP 服务配置状态！**

### 步骤 1：检查 mcporter 是否安装

```bash
mcporter --version
```

**如未安装**，按以下流程安装：

```bash
# 1. 通过 npm 全局安装
npm install -g mcporter

# 2. 验证安装
mcporter --version
```

### 步骤 2：检查 MCP 服务配置

```bash
# 列出所有已配置的 MCP 服务
mcporter list
```

**预期输出**（必须包含以下两个服务）：
- jy-financedata-tool
- jy-financedata-api

**如服务未配置**，需要获取 JY_API_KEY 并配置：

1. **获取 JY_API_KEY**，向恒生聚源申请 JY_API_KEY，通过邮箱申请（首次配置需提供，配置一次即可）

JY_API_KEY 申请路径：
向恒生聚源官方邮箱发送邮件申请签发 数据地图 JY_API_KEY，用于接口鉴权
申请通过后，恒生聚源将默认发送【工具版和接口版】KEY
另外，【Skill】包可通过 https://clawhub.ai/ 自行选择下载，若需要我们通过邮件提供【Skill】，亦可在邮件中注明

申请邮箱：datamap@gildata.com

邮件标题：数据地图 KEY 申请-XX 公司 - 申请人姓名

正文模板：
- 姓名：
- 手机号：
- 公司/单位全称：
- 所属部门：
- 岗位：
- MCP_KEY 申请用途：
- Skill 申请列表：
- 是否需要 Skill 安装包：（是，邮件提供/否，自行下载）
- 其他补充说明（可选）：

2. **配置 MCP 服务**：

```bash
# 配置 jy-financedata-tool 服务
mcporter config add jy-financedata-tool --url "https://api.gildata.com/mcp-servers/aidata-assistant-srv-tool?token=你的 JY_API_KEY"

# 配置 jy-financedata-api 服务
mcporter config add jy-financedata-api --url "https://api.gildata.com/mcp-servers/aidata-assistant-srv-api?token=你的 JY_API_KEY"
```

3. **验证配置**：

```bash
mcporter list
```

4. **使用方式**：
```bash
# 基础键值对传参
mcporter call 服务名称。工具 参数=值

# 示例，注意：所有服务工具的入参均为 query
mcporter call jy-financedata-api.StockBelongIndustry query="电子行业 代表性上市公司 龙头股"
```

### 步骤 3：在 OpenClaw 中启用 mcporter（如未配置）

**mcporter 配置文件路径**：
- Windows: `C:\Users\你的用户名\config\mcporter.json`
- Linux/MacOS: `/root/config/mcporter.json`

**OpenClaw 配置文件路径**：
- Windows: `C:\Users\你的用户名\.openclaw\openclaw.json`
- Linux/MacOS: `~/.openclaw/openclaw.json`

**编辑 openclaw.json**，在 skills 部分添加 mcporter 配置：

```json
{
  "skills": {
    "entries": {
      "mcporter": {
        "enabled": true,
        "env": {
          "MCPORTER_CONFIG": "/root/config/mcporter.json"
        }
      }
    }
  }
}
```

**重启 OpenClaw 使配置生效**：

```bash
openclaw gateway restart
```

## 核心工作流程

### 步骤 1：筛选目标行业基金

调用 `jy-financedata-tool.SmartFundSelection` 筛选行业主题基金（最多 15 只）。

```bash
mcporter call jy-financedata-tool.SmartFundSelection query="<行业> 基金"
```

### 步骤 2：获取定期报告

调用 `jy-financedata-api.FundAnnouncement` 获取两个季度的季度报告全文。

```bash
mcporter call jy-financedata-api.FundAnnouncement query="<基金名> <年份>年第<季度>季度报告"
```

### 步骤 3：OpenClaw 语义提取观点

将获取的报告内容提交给 OpenClaw，提取核心观点、关注主题、风险判断、情绪倾向。

### 步骤 4：OpenClaw 汇总季度观点

识别共识（至少 2 只基金相似观点）与分歧（不同基金不同看法）。

### 步骤 5：OpenClaw 对比季度变化

分析情绪变化、主题转移、新增担忧/机会、策略变化。

### 步骤 6：生成结构化报告

输出 Markdown 格式报告，包含核心结论、季度对比表格、基金观点详情、引用来源。

## 快速开始

### 基础用法

```bash
./run.sh "<行业>" "<季度 1>" "<季度 2>"
```

### 工具调用命令

| 用途 | 命令 |
|------|------|
| 筛选行业基金 | `mcporter call jy-financedata-tool.SmartFundSelection query="<行业> 基金"` |
| 获取基金报告 | `mcporter call jy-financedata-api.FundAnnouncement query="<基金名> <年份>年第<季度>季度报告"` |
| 验证配置 | `mcporter list` |

### 数据获取策略

1. 优先用基金名称查询，代码可能不识别
2. 季度格式：`2025 年第 3 季度` 或 `2025Q3`
3. 必须使用 `query` 参数
4. 季度报告在季度结束后 15 个工作日内披露

### 完整流程示例

```bash
# 1. 运行技能，准备数据
./run.sh "新能源" "2025Q3" "2025Q4"

# 2. 将生成的提示词发送给 OpenClaw 进行语义分析
# 提示词保存在 output/analysis_*.json 的 prompt 字段

# 3. 保存 OpenClaw 返回的 JSON 结果为 result.json

# 4. 生成最终报告
python3 scripts/generate_report.py output/analysis_*.json result.json
```

## 资源清单

```
~/Desktop/jy-fund-manager-viewpoint/
├── SKILL.md                  # 技能说明（本文件）
├── run.sh                    # 入口脚本
├── scripts/
│   ├── analyze_viewpoints.py # 核心分析脚本（数据准备 + 提示词生成）
│   └── generate_report.py    # 报告生成脚本
├── references/
│   ├── output_format.md      # 输出格式示例
│   └── mcp_guide.md          # MCP 调用详细指南
└── output/                   # 报告输出目录
```

## 限制

- ✅ 数据源：恒生聚源基金公告
- ✅ 语义分析：使用 OpenClaw 内置语义能力，无需额外 API
- ✅ 引用标注：所有观点均标注来源基金及报告
- ⚠️ 报告披露：季度结束后 15 个工作日内
- ⚠️ 分析范围：默认最多 15 只基金
- ⚠️ 内容长度：单篇报告最多 8000 字符
- ⚠️ 分析耗时：约 5-10 分钟
- ❌ 非投资建议：仅供参考

## 故障排查

**Q: mcporter 未找到？**
A: 运行 `npm install -g mcporter` 安装。

**Q: 未检测到聚源 MCP 服务配置？**
A: 按"步骤 2"配置 jy-financedata-tool 和 jy-financedata-api 服务。

**Q: 没有 JY_API_KEY？**
A: 按"步骤 2"流程向恒生聚源申请 (datamap@gildata.com)。

**Q: 找不到某季度的报告？**
A: 季度报告可能尚未披露，请确认季度结束已超过 15 个工作日。

**Q: 观点提取为空？**
A: 基金报告可能未提及该行业，尝试放宽行业关键词。

**Q: 分析结果为空或格式错误？**
A: 确保 OpenClaw 返回的是有效 JSON 格式，如包裹在代码块中脚本会自动提取。
