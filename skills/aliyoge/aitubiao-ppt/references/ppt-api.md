# PPT API Reference

> **重要**：所有非流式响应都包裹在 `{ "code": 0, "msg": "ok", "data": { ... } }` 结构中。
> 下面的响应示例展示的是 `data` 字段内的业务数据。
> **即使 HTTP 状态码为 200，也必须检查 `code` 字段是否为 0。非 0 表示业务错误（如 AI贝不足、项目数已满）。**

## 1. Create PPT Project (一站式)

**Endpoint**: `POST {BASE_URL}/api/v1/agent/infographic/create-project`

一次调用完成：大纲创建 → 项目创建。API 立即返回项目地址，页面在后台异步生成，用户可通过 `projectUrl` 实时查看进度。

**Headers**:
```
Authorization: Bearer {API_KEY}
Content-Type: application/json
```

**Request Body**:
```json
{
  "prompt": "人工智能在医疗领域的应用与未来趋势",
  "pageCount": 6,
  "theme": "light",
  "projectName": "AI医疗趋势报告",
  "requirements": "简洁商务风格，多用数据图表"
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| prompt | string | Yes | - | 用户输入的主题或内容文本 |
| projectName | string | No | - | 项目名称 |
| requirements | string | No | - | 附加要求（如风格偏好、内容侧重等） |
| title | string | No | - | 大纲标题 |
| pageCount | number | No | 6 | 页数（最小 1，上限由会员等级决定，查看配额接口的 `pptGeneratePageLimit`） |
| theme | string | No | "light" | 主题：`light`（浅色）或 `dark`（深色） |
| color | string | No | - | 主题色：`#004eff`、`#f16f0b`、`#ee4646`、`#2197fc`、`#8a61ec`、`#35b13f`、`dynamic` |

**Response** (data 字段内容):
```json
{
  "success": true,
  "outlineId": "uuid-outline-session-id",
  "project": {
    "id": "cuid_string",
    "title": "AI医疗趋势报告",
    "status": "generating",
    "width": 960,
    "height": 540,
    "projectUrl": "https://app.aitubiao.com/workspace/cuid_string"
  },
  "quota": {
    "shellCoinCost": 60,
    "shellBalance": 40,
    "projectsUsed": 6,
    "projectsLimit": 50,
    "projectsRemaining": 44,
    "canCreateProject": true
  },
  "totalPages": 6,
  "completedPages": 0,
  "failedPages": 0,
  "processingTime": "5000ms"
}
```

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | 项目是否创建成功 |
| outlineId | string | 大纲会话 ID |
| project | object | 项目信息 |
| project.id | string | 项目 ID |
| project.title | string | 项目标题 |
| project.status | string | 项目状态：API 返回时通常为 `generating`（页面在后台异步生成） |
| project.width | number | 页面宽度（像素） |
| project.height | number | 页面高度（像素） |
| project.projectUrl | string? | 项目可访问 URL，用户可打开此链接查看生成进度和编辑 PPT |
| quota | object? | 配额快照（可能为 null） |
| quota.shellCoinCost | number | 本次消耗 AI贝 |
| quota.shellBalance | number | 剩余 AI贝 |
| quota.projectsUsed | number | 已用项目数 |
| quota.projectsLimit | number | 项目上限 |
| quota.projectsRemaining | number | 剩余项目数 |
| quota.canCreateProject | boolean | 是否可继续创建 |
| totalPages | number | 总页数 |
| completedPages | number | 已完成页数（API 立即返回时为 0，页面在后台异步生成） |
| failedPages | number | 失败页数 |
| processingTime | string | API 响应时间（不含页面生成时间） |

**注意**:
- API 在项目创建后**立即返回**，不等待页面生成完成。页面在后台异步生成，通常需要 **5-10 分钟**。
- `quota` 字段可能为 `null`（配额查询失败时），不影响项目创建结果。
- **`projectUrl` 是用户查看生成进度和编辑 PPT 的入口**，必须醒目展示给用户。

**业务错误响应** (code ≠ 0):
```json
{
  "code": 90001,
  "msg": "exp.shell.SHELL_NOT_ENOUGH",
  "quota": {
    "shellCoinCost": 60,
    "shellBalance": 30,
    "projectsUsed": 5,
    "projectsLimit": 50,
    "projectsRemaining": 45,
    "canCreateProject": false
  }
}
```

| 错误码 | 含义 | 处理方式 |
|--------|------|---------|
| 90001 | AI贝不足 | 展示 quota 中的余额和消耗信息，建议充值或升级会员 |
| 40007 | 项目数已满 | 展示 quota 中的已用/上限，建议删除旧项目或升级会员 |
| 40015 | 项目创建失败 | 系统内部错误，建议重试 |

## 2. Get User Quota (通用配额查询)

**Endpoint**: `GET {BASE_URL}/api/v1/agent/quota`

查询用户当前 AI贝余额、项目配额和所有 AI 功能的 AI贝消耗量。建议在创建项目前调用此接口预检。

**Headers**:
```
Authorization: Bearer {API_KEY}
```

**Response** (data 字段内容):
```json
{
  "shellBalance": 100,
  "shellLeft": 80,
  "shellNum": 20,
  "projectsUsed": 5,
  "projectsLimit": 50,
  "projectsRemaining": 45,
  "pptGeneratePageLimit": 32,
  "features": {
    "pptProjectCreate": { "key": "pptProjectCreate", "cost": 10, "unit": "页", "label": "PPT项目创建(API)", "billingModel": "per-page" }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| shellBalance | number | 当前 AI贝总余额 (shellLeft + shellNum) |
| shellLeft | number | 每月可重置的 AI贝 |
| shellNum | number | 永久 AI贝 |
| projectsUsed | number | 已创建项目数 |
| projectsLimit | number | 项目数上限（由会员等级决定） |
| projectsRemaining | number | 剩余可创建项目数 |
| pptGeneratePageLimit | number | 单次 PPT 生成的最大页数（由会员等级决定） |
| features | Record | 各 AI 功能的 AI贝消耗配置 |

> **PPT 生成费用**：使用 `features.pptProjectCreate` 的 cost 和 billingModel 计算费用。billingModel 为 `per-page`，总费用 = cost × pageCount。例如生成 6 页 PPT：10 × 6 = 60 AI贝。
