# n8n Workflow Operator

> 通过 n8n REST API 设计、创建、修改和管理工作流的 OpenClaw Skill。
> 无需 MCP 服务器，纯 REST API 调用即可让 Agent 完全操控 n8n。

## 元信息

- **Name:** n8n-operator
- **Version:** 1.1.0
- **Author:** AI-generated for OpenClaw
- **License:** MIT
- **Dependencies:** n8n 实例 + API Key（无需 MCP）
- **Tested on:** n8n 2.x (2026-04-14)

## n8n 2.x 关键差异（实测验证）

> ⚠️ 以下规则经过真实 n8n 2.x 实例验证，不遵守会导致 API 报错。

1. **`active` 是只读字段** — 创建/更新工作流时不要传 `active` 字段（`request/body/active is read-only`）
2. **`tags` 是只读字段** — 创建时不要传 `tags`（`request/body/tags is read-only`）
3. **激活用专用端点** — `POST /api/v1/workflows/{id}/activate`（空 body 或 `{}`）
4. **PUT 是全量替换** — 但不要传 GET 返回的额外字段（`shared`、`activeVersion`、`pinData` 等），只传 `name`、`nodes`、`connections`、`settings`，否则报 `must NOT have additional properties`
5. **PATCH 不支持** — n8n 2.x 不支持 PATCH 方法（`PATCH method not allowed`）
6. **Webhook 响应** — `responseMode: "lastNode"` 时，最后一个节点的返回值自动作为 HTTP 响应。**不要再单独加 `respondToWebhook` 节点**，会报 `Unused Respond to Webhook node found`。用 `n8n-nodes-base.code` 节点作为最后一个节点返回响应数据
7. **激活后等待** — 激活后等待 1-2 秒再触发 Webhook，否则可能收到 404
8. **Windows 注意** — PowerShell 的 `curl` 是 `Invoke-WebRequest` 的别名，用 `curl.exe` 调用真正的 curl

## 何时激活

当用户请求以下任何操作时，自动激活此 Skill：

- "帮我创建一个 n8n 工作流"
- "在 n8n 里设计一个自动化流程"
- "修改 n8n 工作流"
- "查看 n8n 工作流列表"
- "激活/停用 n8n 工作流"
- "删除 n8n 工作流"
- "执行 n8n 工作流"
- "给 n8n 工作流添加节点"
- "连接 n8n 的两个节点"
- "查看 n8n 工作流的执行记录"
- 任何涉及 n8n 工作流设计、创建、管理的请求

## 前置条件

### 1. 环境变量

在使用任何 API 调用前，确认以下环境变量已设置：

```
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMGNiMWEyYy1jZTBhLTQwOGMtODAwZC0zZWYwYWUzNzhiMjkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiYzcwYjQ5NmYtM2ExNi00ZTY2LWFiYWItOGIzNGJlOTU4MjlhIiwiaWF0IjoxNzc2MjEyNTEzfQ.YcZWj3U6PtChhxk6PZ4lVgUQsqN-UDjQ8oETdi4sy7c
```

获取 API Key：n8n 界面 → Settings → API → Create an API Key

### 2. 认证方式

所有 API 请求必须携带认证头：

```
X-N8N-API-KEY: <N8N_API_KEY>
Content-Type: application/json
```

### 3. 检查连接

在执行任何操作前，先用此命令验证连通性：

```bash
curl -s -o /dev/null -w "%{http_code}" -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/workflows"
```

- 返回 `200` → 连接正常
- 返回 `401` → API Key 无效
- 返回 `000` → 网络不通

---

## 核心工作流

Agent 必须严格遵循以下工作流，不可跳步：

### 阶段 1：理解需求

1. 向用户确认工作流的目的和功能
2. 识别触发方式（Webhook / Schedule / Manual / 其他）
3. 列出涉及的节点和数据流向
4. 确认用户满意后再进入下一阶段

### 阶段 2：规划设计

1. 从 [工作流模式参考](references/workflow-patterns.md) 选择匹配的架构模式
2. 绘制节点连接图（用文字描述）
3. 从 [节点模板参考](references/node-templates.md) 选择合适的节点配置
4. 规划错误处理策略
5. 向用户展示设计方案，等待确认

### 阶段 3：逐步构建

按以下顺序构建，**每步之后验证**：

```
Step 1: 创建空工作流骨架 → 获取 workflow_id
Step 2: 逐个添加节点（每次 1-3 个节点）
Step 3: 建立节点连接
Step 4: 验证完整工作流
Step 5: 激活工作流（用户确认后）
```

### 阶段 4：验证交付

1. 确认工作流已激活
2. 如有 Webhook，提供 Webhook URL
3. 展示执行测试结果
4. 记录 workflow_id 供后续修改

---

## API 参考

### 基础 URL

```
{N8N_BASE_URL}/api/v1
```

### 1. 工作流管理

#### 列出所有工作流

```bash
GET /api/v1/workflows
```

可选参数：
- `active=true|false` - 按激活状态过滤
- `cursor=string` - 分页游标
- `limit=number` - 每页数量（默认 10）

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/workflows?active=true&limit=50"
```

#### 获取单个工作流

```bash
GET /api/v1/workflows/{id}
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/workflows/123"
```

#### 创建工作流

```bash
POST /api/v1/workflows
```

**最小请求体（空骨架）：**

```json
{
  "name": "My Workflow",
  "nodes": [],
  "connections": {},
  "settings": {}
}
```

**带节点的完整请求体（Webhook + Code 节点响应）：**

```json
{
  "name": "Webhook to Slack",
  "nodes": [
    {
      "id": "a1",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [0, 0],
      "parameters": {
        "httpMethod": "POST",
        "path": "my-webhook",
        "responseMode": "lastNode",
        "responseData": "lastNode",
        "options": {}
      }
    },
    {
      "id": "a2",
      "name": "Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2.2,
      "position": [250, 0],
      "credentials": {
        "slackApi": {
          "id": "credential-id",
          "name": "Slack account"
        }
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Slack", "type": "main", "index": 0 }]]
    }
  },
  "settings": {
    "saveManualExecutions": true,
    "executionOrder": "v1"
  }
}
```

#### 更新工作流（PUT - 全量替换）

```bash
PUT /api/v1/workflows/{id}
```

请求体与创建相同，但必须包含完整的工作流数据。**注意：PUT 是全量替换，会覆盖整个工作流。**

#### 删除工作流

```bash
DELETE /api/v1/workflows/{id}
```

```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/workflows/123"
```

#### 激活工作流

```bash
POST /api/v1/workflows/{id}/activate
```

```bash
# Linux/macOS
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" -H "Content-Type: application/json" "$N8N_BASE_URL/api/v1/workflows/123/activate"

# Windows PowerShell
curl.exe -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" -H "Content-Type: application/json" -d "{}" "$N8N_BASE_URL/api/v1/workflows/123/activate"
```

> ⚠️ n8n 2.x：激活后等待 1-2 秒再触发 Webhook，确保路由注册完成。

#### 停用工作流

```bash
POST /api/v1/workflows/{id}/deactivate
```

#### 执行工作流

```bash
POST /api/v1/workflows/{id}/execute
```

可选参数：
- `data` - 输入数据（JSON 对象或数组）

```bash
curl -s -X POST \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": {"key": "value"}}' \
  "$N8N_BASE_URL/api/v1/workflows/123/execute"
```

### 2. 凭证管理

#### 列出所有凭证

```bash
GET /api/v1/credentials
```

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/credentials"
```

**重要：** 凭证 ID 在创建节点时需要用到。凭证中的实际密钥/密码无法通过 API 读取（仅返回 ID 和 Name）。

#### 创建凭证

```bash
POST /api/v1/credentials
```

```json
{
  "name": "My API Credentials",
  "type": "httpHeaderAuth",
  "data": {
    "name": "X-API-Key",
    "value": "your-actual-api-key"
  }
}
```

常用凭证类型：
- `httpHeaderAuth` - HTTP Header 认证
- `httpBasicAuth` - HTTP Basic 认证
- `oAuth2Api` - OAuth2 认证
- `slackApi` - Slack API
- `mysql` - MySQL 数据库
- `postgres` - PostgreSQL 数据库

### 3. 执行记录

#### 列出执行记录

```bash
GET /api/v1/executions
```

可选参数：
- `workflowId=number` - 按工作流过滤
- `status=success|error|running` - 按状态过滤
- `limit=number` - 数量限制

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/executions?workflowId=123&limit=5"
```

#### 获取执行详情

```bash
GET /api/v1/executions/{id}
```

返回完整的执行数据，包括每个节点的输入输出。

---

## 节点（Node）数据结构

### 核心字段

```json
{
  "parameters": {},           // 节点参数（节点类型决定具体字段）
  "id": "unique-uuid",        // 节点唯一 ID（UUID v4 格式）
  "name": "Node Display Name", // 节点显示名称（也是连接引用的 key）
  "type": "n8n-nodes-base.xxx", // 节点类型（完整格式）
  "typeVersion": 1,           // 节点版本号
  "position": [250, 300],     // 画布位置 [x, y]
  "credentials": {},          // 凭证引用（可选）
  "disabled": false,          // 是否禁用（可选）
  "notes": "备注文字"          // 节点备注（可选）
}
```

### 关键规则

1. **nodeType 格式**：在 API 请求体中始终使用 `n8n-nodes-base.xxx` 完整格式
2. **id 生成**：使用 UUID v4，可以用 `uuidgen` 或在线生成
3. **name 的双重作用**：既是显示名称，也是 `connections` 中引用节点的 key
4. **position**：画布坐标，建议 x 间距 220，y 间距 200

### 凭证引用格式

```json
{
  "credentials": {
    "credentialTypeName": {
      "id": "credential-id-from-api",
      "name": "credential-display-name"
    }
  }
}
```

---

## 连接（Connection）数据结构

### 基本结构

```json
{
  "SourceNodeName": {
    "main": [
      [
        {
          "node": "TargetNodeName",
          "type": "main",
          "index": 0
        }
      ]
    ]
  }
}
```

### 结构解读（三层嵌套数组）

```
connections = {
  [源节点名称]: {              // 第一层：按源节点分组
    [输出类型]: [              // 第二层：输出类型（main / ai）
      [                        // 第三层外层：输出索引（一个节点可以有多个输出）
        {                      // 第三层内层：连接的目标列表
          node: "目标节点名",
          type: "main",
          index: 0             // 目标节点的输入索引
        }
      ]
    ]
  }
}
```

### 常见连接模式

#### 线性连接（A → B → C）

```json
{
  "A": {
    "main": [[{ "node": "B", "type": "main", "index": 0 }]]
  },
  "B": {
    "main": [[{ "node": "C", "type": "main", "index": 0 }]]
  }
}
```

#### 分支连接（A → IF → B 或 C）

```json
{
  "A": {
    "main": [[{ "node": "IF", "type": "main", "index": 0 }]]
  },
  "IF": {
    "main": [
      [{ "node": "B", "type": "main", "index": 0 }],   // true 分支
      [{ "node": "C", "type": "main", "index": 0 }]    // false 分支
    ]
  }
}
```

#### 并行连接（A → B + C → D）

```json
{
  "A": {
    "main": [
      [
        { "node": "B", "type": "main", "index": 0 },
        { "node": "C", "type": "main", "index": 0 }
      ]
    ]
  },
  "B": {
    "main": [[{ "node": "D", "type": "main", "index": 0 }]]
  },
  "C": {
    "main": [[{ "node": "D", "type": "main", "index": 0 }]]
  }
}
```

---

## 错误处理策略

### 在工作流 JSON 中添加错误工作流

```json
{
  "name": "My Workflow",
  "nodes": [...],
  "connections": {...},
  "settings": {
    "executionOrder": "v1",
    "errorWorkflow": "error-handler-workflow-id"  // 引用错误处理工作流的 ID
  }
}
```

### 在节点级别捕获错误

部分节点支持 `continueOnFail` 参数：

```json
{
  "name": "HTTP Request",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {...},
  "continueOnFail": true  // 出错时继续执行下一个节点
}
```

### Error Trigger 节点

在错误处理工作流中使用 Error Trigger 节点自动捕获上游工作流的错误：

```json
{
  "name": "Error Trigger",
  "type": "n8n-nodes-base.errorTrigger",
  "typeVersion": 1,
  "position": [250, 300]
}
```

---

## n8n 表达式语法速查

在节点的 `parameters` 中使用 `={{ }}` 嵌入动态值：

```json
{
  "text": "={{ $json.body.message }}"
}
```

### 核心变量

| 变量 | 用途 | 示例 |
|------|------|------|
| `$json` | 当前节点输入数据 | `{{ $json.email }}` |
| `$json.body` | Webhook 请求体 | `{{ $json.body.data }}` |
| `$json.query` | URL 查询参数 | `{{ $json.query.page }}` |
| `$json.headers` | 请求头 | `{{ $json.headers['x-custom'] }}` |
| `$node["NodeName"].json` | 引用指定节点的输出 | `{{ $node["HTTP Request"].json.data }}` |
| `$now` | 当前时间 | `{{ $now.toISO() }}` |
| `$env` | 环境变量 | `{{ $env.MY_VAR }}` |
| `$input.first()` | 第一个输入项 | `{{ $input.first().json.name }}` |
| `$input.all()` | 所有输入项 | `{{ $input.all().length }}` |

### Webhook 数据的关键陷阱

```
⚠️ Webhook POST 请求体在 $json.body 下，不是直接在 $json 下！

错误：{{ $json.email }}
正确：{{ $json.body.email }}
```

---

## Agent 操作规范

### 必须遵守的规则

1. **先确认再操作** — 设计方案展示给用户，确认后再调用 API
2. **逐步构建** — 不要一次性构建复杂工作流，每步 1-3 个节点
3. **每次修改后验证** — GET 工作流确认修改成功
4. **使用描述性节点名称** — 避免默认名称，便于后续维护
5. **记录 workflow_id** — 每次创建后告知用户 workflow_id
6. **先查后建** — 创建前先检查是否已存在同名工作流

### 禁止事项

- ❌ 不跳过设计阶段直接创建
- ❌ 不在 connections 中使用节点 ID（必须使用 name）
- ❌ 不硬编码凭证密码到节点参数中（使用凭证引用）
- ❌ 不使用 `detail: "full"` 获取节点信息（用 standard 节省 token）
- ❌ 不跳过连通性检查直接操作
- ❌ 不修改正在运行的工作流（先停用再修改）

### 构建工作流的标准对话流程

```
用户："帮我创建一个 XXX 工作流"
  ↓
Agent：确认需求 + 列出涉及的节点 + 画出数据流
  ↓
用户：确认
  ↓
Agent：先检查 N8N_BASE_URL 和 N8N_API_KEY
  ↓
Agent：查询现有工作流（避免重复）
  ↓
Agent：创建骨架 → 添加节点 → 建立连接 → 验证 → 激活
  ↓
Agent：提供 Webhook URL / 测试结果 / workflow_id
```

---

## 参考文件

本 Skill 附带以下参考文件，放在 `references/` 目录下：

- **[node-templates.md](references/node-templates.md)** — 30+ 常用节点的完整 JSON 模板，可直接复制使用
- **[workflow-patterns.md](references/workflow-patterns.md)** — 6 种经典工作流架构模式，含完整 JSON 示例

---

## 完整示例：创建一个 Webhook 接收并返回 JSON 的工作流

### Step 1: 创建工作流（包含节点和连接）

```json
{
  "name": "Webhook Echo",
  "nodes": [
    {
      "id": "a1",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [0, 0],
      "parameters": {
        "httpMethod": "POST",
        "path": "echo",
        "responseMode": "lastNode",
        "responseData": "lastNode",
        "options": {}
      }
    },
    {
      "id": "a2",
      "name": "Process & Respond",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [250, 0],
      "parameters": {
        "jsCode": "return [{ json: { received: $json.body, processed: true, time: new Date().toISOString() } }];"
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Process & Respond", "type": "main", "index": 0 }]]
    }
  },
  "settings": {
    "saveManualExecutions": true,
    "executionOrder": "v1"
  }
}
```

> **关键：** Webhook 使用 `responseMode: "lastNode"`，最后一个节点（Code 节点）的返回值自动成为 HTTP 响应。不需要单独的 `respondToWebhook` 节点。

### Step 2: 提取 workflow_id

创建成功后从响应中提取 `id` 字段。

### Step 3: 激活

```bash
curl.exe -s -X POST -H "X-N8N-API-KEY: %N8N_API_KEY%" -H "Content-Type: application/json" -d "{}" "%N8N_BASE_URL%/api/v1/workflows/{id}/activate"
```

### Step 4: 触发 Webhook

```bash
curl.exe -s -X POST -H "Content-Type: application/json" -d "{\"hello\":\"world\"}" "%N8N_BASE_URL%/webhook/echo"
```

预期返回：
```json
[{"received":{"hello":"world"},"processed":true,"time":"2026-04-14T14:10:49.000Z"}]
```

---

## 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 401 Unauthorized | API Key 无效或过期 | 重新生成 API Key |
| 400 `active is read-only` | 创建/PUT 时传了 `active` 字段 | 不传 `active`，用 activate 端点 |
| 400 `tags is read-only` | 创建时传了 `tags` 字段 | 不传 `tags` |
| 400 `must NOT have additional properties` | PUT 时传了 GET 返回的额外字段（shared/activeVersion 等） | 只传 name/nodes/connections/settings |
| 405 `PATCH method not allowed` | n8n 2.x 不支持 PATCH | 用 PUT 全量替换 |
| 500 `Unused Respond to Webhook node` | n8n 2.x 中 Webhook+lastNode 模式下用了 respondToWebhook | 删掉 respondToWebhook 节点，用 Code 节点返回响应 |
| Webhook 404 | 激活后立即触发，路由还未注册 | 等待 1-2 秒再触发 |
| `object is not iterable` | activate 端点收到非预期 body 格式 | 发送 `{}` 或空 body + `Content-Type: application/json` |
| 节点不执行 | 工作流未激活 | 调用 activate 端点 |
| Webhook 收不到数据 | 路径冲突或工作流未激活 | 检查 path 唯一性 + 确认 active |
| 凭证找不到 | 使用了错误的凭证类型名 | 查询 `/credentials` 获取正确 type |
| PUT 后节点消失 | 未包含所有现有节点 | PUT 是全量替换，必须包含全部节点 |


---

## 实战教训（2026-04-14更新）

### ❌ Wait节点导致激活失败
**问题：** Wait for Callback节点配置会导致工作流无法激活
**解决：** 人工审核改用IF分支判断，不要用Wait节点

### ❌ 微信草稿thumb_media_id为空
**问题：** 草稿API要求封面media_id，不能为空
**解决：** 先调用 POST /cgi-bin/material/add_material 上传封面获取media_id

### ❌ 摘要超字节限制（45004错误）
**问题：** digest限制54字节，中文容易超
**解决：** digest = content[:50] 严格控制

### ❌ 标题超字节限制（45003错误）
**问题：** title限制20字节
**解决：** title = title[:10] 控制在10个中文字以内

### ❌ access_token失效
**问题：** token有效期7200秒，多次调用后失效
**解决：** 每次发草稿前重新获取token，不要缓存复用

### ✅ 正确顺序
1. 创建工作流 → 不传active字段
2. 激活工作流 → POST /activate + 空body + 等待1-2秒
3. 测试Webhook
4. 封面图先上传获取media_id
5. 发草稿前重新获取token


---



### ❌ tags/staticData 字段只读（400错误）
**问题：** 创建工作流时传 `tags` 或 `staticData` → 400 "tags is read-only"
**解决：** 创建workflow JSON时，不传这两个字段

### ❌ Webhook URL格式（n8n 2.x）
**问题：** Webhook触发返回404
**原因：** n8n 2.x的Webhook路径是 `/webhook/{webhookId}`，不是 `/webhook/{path参数}`
**解决：** Webhook节点的 `path` 参数只是标识，调用时用 `{webhookId}`：
```
# 触发时用这个URL：
POST http://localhost:5678/webhook/{webhookId}
# 而非：
POST http://localhost:5678/webhook/{path参数}
```


## 试错规则

**同一问题试错超过3次 → 必须停止搜索研究，不能继续盲目试错：**

1. 搜索clawhub/n8n文档/社区找类似问题
2. 剖析错误根本原因
3. 制定针对性解决方案
4. 验证后记录进skill/memory

这条规则适用于所有技术调试任务。


---

## n8n工作流设计原则（借鉴 n8n-workflow-automation）

### 核心原则：防静默失败

设计任何工作流必须满足：

#### 1. 幂等性（Idempotency）
- dedup key：用什么字段判断重复？（如唯一订单号、时间戳+业务ID）
- dedup存储：DB/Sheet/文件，确保重试不产生重复记录
- 每次运行前先检查是否已处理

#### 2. 可观测性（Observability）
- 生成 
un_id 贯穿全程
- 记录开始/结束/每个关键节点状态
- 失败时写错误详情到日志

#### 3. 重试+backoff
- 出错自动重试，间隔递增（1s → 2s → 4s）
- 最大重试次数限制（如3次）
- 超过限制 → 路由到人工审核队列

#### 4. 人工审核队列（Human-in-the-Loop）
- 失败记录写入队列（Sheet/DB）
- 人工确认后重新处理
- 不在群里/QQ狂轰滥炸

#### 5. No Silent Failure 门控
- 关键计数/阈值不达标 → 立即停止工作流并告警
- 不允许静默跳过或吞掉错误

#### 6. 错误处理标准结构
`
[主流程]
    ↓（出错）
[重试分支] → 重试1-3次
    ↓（全部失败）
[错误日志] → 写DB/文件记录详情
    ↓
[告警通知] → 发QQ消息（仅关键错误）
    ↓
[人工审核队列] → 等待人工确认
`

### 设计检查清单

设计工作流时必须确认：
- [ ] 触发类型（Webhook/定时/手动）
- [ ] 输入schema和必填字段
- [ ] dedup key是什么？存储在哪？
- [ ] run_id如何生成和传递？
- [ ] 错误重试策略（次数+间隔）
- [ ] 哪些情况路由人工审核？
- [ ] 哪些情况发告警？
- [ ] credential是否通过环境变量/引用，不硬编码？


---

## 性能与监控（借鉴 n8n skill）

### 健康检查（定时执行）
```bash
# 统计活跃工作流数量和最近24小时失败执行数
ACTIVE=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/workflows?active=true" | jq ".data | length")
FAILED=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/executions?status=error&limit=100" | jq "[.data[] | select(.startedAt > (now - 86400 | todate))] | length")
echo "Active: $ACTIVE | Failed(24h): $FAILED"
```

### 性能分析
```bash
python3 scripts/n8n_optimizer.py analyze --id <workflow-id> --pretty
python3 scripts/n8n_optimizer.py suggest --id <workflow-id> --pretty
```

### 执行监控
```bash
# 最近执行
python3 scripts/n8n_api.py list-executions --limit 10 --pretty
# 特定工作流执行
python3 scripts/n8n_api.py list-executions --id <workflow-id> --limit 20 --pretty
# 执行详情
python3 scripts/n8n_api.py get-execution --id <execution-id> --pretty
```

### 测试验证
```bash
# 校验工作流结构
python3 scripts/n8n_tester.py validate --id <workflow-id> --pretty
# 干跑测试
python3 scripts/n8n_tester.py dry-run --id <workflow-id> --data "{"key": "value"}"
# 测试报告
python3 scripts/n8n_tester.py dry-run --id <workflow-id> --data-file test.json --report
```

---

## 端点索引（借鉴 n8n-api）

| 端点 | 方法 | 用途 |
|------|------|------|
| /api/v1/workflows | GET | 列表 |
| /api/v1/workflows/{id} | GET | 详情 |
| /api/v1/workflows | POST | 创建 |
| /api/v1/workflows/{id}/activate | POST | 激活 |
| /api/v1/workflows/{id}/deactivate | POST | 停用 |
| /api/v1/workflows/{id} | DELETE | 删除 |
| /api/v1/executions | GET | 执行列表 |
| /api/v1/executions/{id} | GET | 执行详情 |
| /api/v1/executions/{id}/retry | POST | 重试 |
| /api/v1/credentials | GET | 凭证列表 |
| /webhook/{path} | POST | Webhook触发 |
| /webhook-test/{path} | POST | Webhook测试 |
