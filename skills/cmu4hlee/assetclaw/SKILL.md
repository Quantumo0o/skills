---
name: "assethub-claw"
description: "AssetClaw技能用于实现资产全生命周期管理：资产查询/报修/维修工单/调配审批/盘点任务/折旧统计/采购申请/报废处理/质检记录/技术文档/备件库存/标签打印/告警处理/IoT 监测等。适用于需要快速查询、创建、审批各类资产业务单据的场景。"
---

# AssetClaw 完整技能文档 (v1.4.5)

> 基于 `http://160ttth72797.vicp.fun/api` 实时接口文档编写
> 本 Skill 直接调用 HTTP API，不依赖 MCP 协议

---

## 核心原则（必须遵守）

1. **先登录后请求** — 每个会话首先调用 `POST /api/users/login` 获取 Bearer Token 并缓存
   - **凭证处理原则**：
     - **如果新会话已提供凭证**（用户名+密码），直接使用提供的凭证登录，无需再询问
     - **如果未提供凭证**，则分两步引导：先问用户名 → 用户回答后再问密码 → 收集完整后才执行登录
     - **临时 Session 凭证存储**：当凭证通过 prompt/对话传入时，Agent 将用户名和密码写入本地临时会话文件 `/tmp/assethub-claw-temp-session.json`（仅当前会话有效）；调用 assetclaw API 时自动从该文件读取凭证完成登录
     - 无论哪种方式，登录成功后 Token 和租户上下文自动保存到会话文件
2. **注销处理** — 当用户发送"注销"时，立即删除会话缓存文件及所有相关凭证，不保留任何登录信息
3. **先查后写** — 写操作前必须先查询目标对象确认 ID/编号
4. **写后回查** — 写操作完成后必须重新查询确认结果，不要仅凭 API 返回的 success 就判断成功
5. **多租户隔离** — 普通用户默认使用登录返回的 `tenant_id`；超级管理员跨租户时显式传 `X-Tenant-ID` Header
   - **重要**：当 Web 应用调用 OpenClaw 时会传递租户 ID，**必须使用传入的租户 ID**，禁止切换到其他租户
6. **不暴露认证信息** — 最终回复中不回显 Token、密码等敏感信息
7. **批量优先** — 多个同类操作优先批量接口
8. **实时优先** — 如接口行为与本文档不符，以后端实时返回和数据库状态为准

---

# 🌐 系统连接信息

| **官网** | **http://www.medfix.cn** |

---

# 🚀 快速开始

## Step 1: 登录获取 Token

**凭证处理原则（必须遵守）：**
- **新会话已提供凭证**：如果用户在发起新会话时已提供用户名和密码，Agent 将其写入 `/tmp/assethub-claw-temp-session.json`，调用 API 时自动完成登录，无需用户再次输入
- **未提供凭证**：如果未提供，则分两步引导：先问用户名 → 用户回答后再问密码 → 收集完整后才执行登录
- **临时 Session 凭证自动登录**：调用 assetclaw 时，自动检查临时凭证文件，若存在则自动登录，无需用户重复输入
- 无论哪种方式，只有在收集到用户名和密码后，才调用登录命令：

```bash
bash scripts/assethub_api.sh login
```

登录成功后 Token 和租户上下文自动保存到会话文件。

**多租户选择（必须遵守）：**
登录成功后，如用户拥有多个租户，应立即列出所有企业名称供用户选择：
1. 从登录响应 `data.enterprises` 中提取所有租户
2. 以编号列表形式展示（如 `1. 某某医院  2. 中国医科大学附属第四医院  3. 第四医院2`）
3. 提示用户直接输入数字选择（如"请输入序号："）
4. 用户输入后，将对应 `tenant_id` 保存到会话文件
5. 如果用户只有一个租户，默认使用该租户，无需询问

**⚠️ Web 应用调用时**：如果 OpenClaw 已通过外部参数传入租户 ID（会话 metadata 中包含），则**禁止切换租户**，必须直接使用传入的租户 ID。

## Step 1.5: 注销（退出登录）

```bash
bash scripts/assethub_api.sh logout
```

当用户发送"注销"时，执行此命令删除会话缓存文件，用户将无法继续访问 API。

## Step 2: 发现可用模块

```bash
# 列出所有模块
bash scripts/assethub_api.sh modules

# 查看特定模块的接口
bash scripts/assethub_api.sh module assets
bash scripts/assethub_api.sh module maintenance
```

## Step 3: 调用 API

```bash
# GET 查询
bash scripts/assethub_api.sh request GET "/assets?page=1&pageSize=20&search=CT"

# POST 创建
bash scripts/assethub_api.sh request POST "/maintenance/ai/submit-request" '{"asset_code":"A001","fault_description":"无法开机","issue_description":"无法开机","source":"assetclaw","intent":"repair_request"}'
```

## Step 4: Raw curl 备用方案

如 helper 脚本网络受限，直接使用 curl：

```bash
# 登录
curl -sS -X POST http://160ttth72797.vicp.fun/api/users/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"<user>","password":"<pwd>"}'

# 查询（需 Bearer Token）
curl -sS "http://160ttth72797.vicp.fun/api/assets?page=1&pageSize=20" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "X-Tenant-ID: <TENANT_ID>"
```

---

# 🛠️ Helper 脚本命令

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ASSETHUB_API_URL` | API 基础地址 | `http://160ttth72797.vicp.fun/api` |
| `ASSETHUB_API_USERNAME` | 登录用户名 | — |
| `ASSETHUB_API_PASSWORD` | 登录密码 | — |
| `ASSETHUB_TENANT_ID` | 显式租户 ID | 登录返回的 tenant_id |
| `ASSETHUB_SESSION_FILE` | 会话缓存文件 | `/tmp/assethub-claw-session.json` |

## 命令列表

| 命令 | 说明 |
|------|------|
| `bash scripts/assethub_api.sh login` | 登录并缓存 Token |
| `bash scripts/assethub_api.sh logout` | 注销登录，删除凭证缓存文件 |
| `bash scripts/assethub_api.sh session` | 查看当前会话状态 |
| `bash scripts/assethub_api.sh set-tenant <序号>` | 切换当前租户（多租户用户用） |
| `bash scripts/assethub_api.sh modules` | 列出所有 API 模块 |
| `bash scripts/assethub_api.sh module <path>` | 查看指定模块接口文档 |
| `bash scripts/assethub_api.sh request GET <path>` | GET 请求 |
| `bash scripts/assethub_api.sh request POST <path> <json>` | POST 请求 |
| `bash scripts/assethub_api.sh request PUT <path> <json>` | PUT 请求 |
| `bash scripts/assethub_api.sh request DELETE <path>` | DELETE 请求 |

---

# 📊 API 模块速查

| 模块 | 路径 | 说明 |
|------|------|------|
| 资产 | `/assets` | 资产全生命周期管理 |
| 维修维护 | `/maintenance` | 维修申请、工单、日志、计划与分析 |
| 盘点 | `/inventory` `/inventory-plans` `/inventory-tasks` `/inventory-discrepancies` | 盘点计划、任务、差异处理 |
| 调配 | `/transfer` | 资产调配申请与审批 |
| 闲置 | `/idle` | 闲置资产发布与调配 |
| 报废 | `/scrapping` | 报废申请与审批 |
| 采购 | `/procurement` | 采购申请与审批 |
| 质检 | `/quality-control` `/quality` | 计量与质量控制 |
| 验收 | `/acceptance` | 资产验收记录 |
| 文档 | `/technical-documents` | 技术资料上传、AI 分析 |
| 折旧 | `/depreciation` | 折旧计算与统计 |
| 部门 | `/departments` | 部门组织管理 |
| 用户 | `/users` | 用户管理 |
| 角色权限 | `/roles-permissions` | 角色、权限、菜单 |
| 模块配置 | `/module-configs` `/modules` | 模块启停、配置 |
| 物联网 | `/iot` `/iot-devices` | IoT 设备与数据上报 |
| 资产定位 | `/asset-location` | 资产定位与位置数据 |
| 标签 | `/asset-labels` | 标签模板与打印 |
| 告警 | `/intelligent-alerts` `/location-alerts` | 智能告警与位置告警 |
| 审计日志 | `/audit-logs` | 系统操作审计 |
| 仪表盘 | `/dashboard` | 仪表盘统计 |
| 工作流 | `/workflow` | 状态迁移规则 |
| AI 分析 | `/asset-ai-analysis` `/agent-mesh` | AI 故障分析与预测 |
| 库存 | `/inventory` | 备件库存管理 |
| 备份 | `/backup` | 数据备份恢复 |
| 系统配置 | `/system-config` | 数据库、IoT Token 配置 |

---

# 🔑 认证与请求头

## 标准请求头

```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
X-Tenant-ID: <tenant_id>   # 仅超级管理员跨租户时需要
Idempotency-Key: <唯一键>  # 所有写操作都需要（长度≤128），格式：op-$(date +%s)-$RANDOM
```

## 登录响应解析

登录成功后，从响应中提取：

- `data.token` → Bearer Token
- `data.user.tenant_id` → 当前租户 ID
- `data.user.username` → 用户名
- `data.user.real_name` → 真实姓名
- `data.user.role` → 角色

## ⚠️ 高风险操作限制

AssetHub API 对写操作有两层安全机制：

### 1. Idempotency-Key（防重复提交，所有写操作都需要）
- 格式：长度 ≤ 128 的唯一字符串
- 生成方式：`op-$(date +%s)-$RANDOM`
- Header: `Idempotency-Key: <唯一键>`
- **注意：即使走 AI 安全入口也需要此 Header**

### 2. 二次风险确认（仅限普通端点，AI入口无需此步）

```
写操作请求（带 Idempotency-Key）
    │
    ├─ 返回 success:true → 操作直接成功 ✅
    │
    └─ 返回 confirmToken（非 AI 入口时触发）
            │
            ▼
       用同一 Idempotency-Key + X-Risk-Confirm-Token 重放请求
       → 操作成功 ✅
```

### 3. 报修推荐路径：AI 安全入口（绕过二次确认）

**✅ 首选：`POST /api/maintenance/ai/submit-request`**

- 不触发二次确认闸门，一次请求完成
- 同样需要 `Idempotency-Key` Header
- 提交后申请自动进入**待审批**状态

**❌ 普通端点（需二次确认）：`POST /api/maintenance/requests`**
- 触发二次确认流程，需两段式请求

**curl 示例（AI 安全入口）：**
```bash
curl -sS -X POST "http://160ttth72797.vicp.fun/api/maintenance/ai/submit-request" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "X-Tenant-ID: <TENANT_ID>" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: op-$(date +%s)-$RANDOM" \
  -d '{"asset_code":"CT-001","fault_description":"球管打火报警E01","source":"assetclaw","intent":"repair_request"}'
```

## 错误处理

| HTTP 状态码 | 含义 | 处理方式 |
|------------|------|----------|
| `400` | 参数错误 | 补全必填字段，不盲目重试 |
| `401` | Token 无效/过期 | 重新登录 |
| `403` | 无权限/租户限制 | 停止写操作，确认权限 |
| `404` | 资源不存在 | 回到查询步骤 |
| `429` | 接口限流 | 退避后重试 |
| `500` | 服务异常 | 保留上下文，稍后重试 |

## 🩺 常见错误与处理（基于实测）

| 错误信息 | 含义 | 处理方式 |
|---------|------|----------|
| `"需要 Idempotency-Key 请求头"` | 写操作缺少 Idempotency-Key | 添加 Header: `Idempotency-Key: op-$(date +%s)-$RANDOM` |
| `"高风险操作需要二次确认"` + `confirmToken` | 普通端点触发二次确认 | 用同一 Idempotency-Key + `X-Risk-Confirm-Token: <confirmToken>` 重放请求 |
| `success: false` + `"资产不存在"` | asset_code 错误 | 重新查询资产确认编号 |
| `success: false` + `"无权限"` | 租户或角色限制 | 确认当前租户和用户角色 |
| HTTP 401 | Token 过期 | 删除会话文件后重新登录 |

**注：API 错误信息在 JSON 响应的 `message` 字段中**，如 `{ "success": false, "message": "xxx" }`

## ❓ 常见问题

### 搜索中文参数返回空结果

**问题：** 使用中文搜索时（如 `search=超声`）返回空，但数据确实存在。

**原因：** shell 传递中文字符时存在编码问题，从非脚本目录调用时触发。

**解决方案：** 搜索参数包含中文时使用 URL 编码：
- ❌ 错误：`bash scripts/assethub_api.sh request GET "/assets?search=超声"`
- ✅ 正确：`bash scripts/assethub_api.sh request GET "/assets?search=%E8%B6%85%E5%A3%B0"`

---

# 📋 核心工作流

## 1. 资产报修流程

```
Step 1: 定位资产
  GET /api/assets?search=<设备名称>
  → 找到资产编号 asset_code

Step 2: 创建维修申请（走 AI 安全入口，无需二次确认）
  POST /api/maintenance/ai/submit-request
  Header: Idempotency-Key: op-$(date +%s)-$RANDOM
  Body: {
    "asset_code": "xxx",
    "issue_description": "故障描述",
    "fault_description": "故障描述",
    "fault_level": "一般/紧急",
    "priority": "normal/critical",
    "request_department": "报修科室",
    "contact_phone": "电话",
    "source": "assetclaw",
    "intent": "repair_request"
  }
  注意：AI 安全入口一次请求完成，无需二次确认；成功后申请状态为待审批

Step 3: 查询确认
  GET /api/maintenance/requests?asset_code=xxx

Step 4: (可选) 审批维修申请
  POST /api/maintenance/requests/{id}/approve
  Body: {"approved": true, "opinion": "同意"}

Step 5: (可选) 开始执行
  POST /api/maintenance/requests/{id}/start
  Body: {"repair_person": "维修人员"}

Step 6: (可选) 完成维修
  POST /api/maintenance/requests/{id}/complete
  Body: {"repair_content": "维修内容", "repair_cost": 1000, "parts_replaced": "更换零件"}
```

## 2. 资产调配流程

```
Step 1: 查询资产确认
  GET /api/assets/{id}
  → 确认资产编号和当前部门

Step 2: 提交调配申请
  POST /api/transfer
  Body: {
    "asset_code": "xxx",
    "reason": "调配原因",
    "to_department": "目标科室"
  }
  或使用旧版路径:
  POST /api/assets/{id}/transfer-apply
  Body: {"reason": "调配原因", "target_department": "目标科室"}

Step 3: 查询调配记录
  GET /api/transfer

Step 4: 审批调配
  PUT /api/transfer/{id}/approve
  Body: {"approved": true, "opinion": "同意"}

Step 5: 执行完成
  PUT /api/transfer/{id}/complete
```

## 3. 盘点完整流程

```
Step 1: 创建盘点计划
  POST /api/inventory-plans
  Body: {
    "plan_name": "全院资产盘点",
    "plan_no": "PD20260402001",
    "start_date": "2026-04-02",
    "end_date": "2026-04-09",
    "remark": "备注"
  }

Step 2: 激活计划
  PUT /api/inventory-plans/{id}/activate

Step 3: 创建盘点任务
  POST /api/inventory-tasks
  Body: {
    "inventory_plan_id": 计划ID,
    "task_name": "科室盘点任务",
    "assignee": "负责人用户名",
    "assignee_name": "负责人姓名",
    "location": "科室位置"
  }

Step 4: 执行盘点
  PUT /api/inventory-tasks/{id}/start

Step 5: 完成盘点
  PUT /api/inventory-tasks/{id}/complete
  Body: {"actual_count": 100}

Step 6: 生成差异
  POST /api/inventory-discrepancies/generate-from-details
  或基于盘点明细:
  POST /api/inventory-discrepancies
  Body: {"inventory_id": 计划ID, "asset_code": "xxx", "discrepancy_type": "missing"}

Step 7: 处理差异
  PUT /api/inventory-discrepancies/{id}/handle
  Body: {"handling_status": "已处理", "handling_method": "盘亏报废"}

Step 8: 批量处理差异
  POST /api/inventory-discrepancies/batch-handle
  Body: {"ids": [ID1, ID2], "handling_status": "已处理", "handling_method": "正常"}

Step 9: 完成计划
  PUT /api/inventory-plans/{id}/complete
```

## 4. 闲置资产发布流程

```
Step 1: 发布闲置
  POST /api/idle
  Body: {
    "asset_code": "xxx",
    "publish_person": "发布人"
  }

Step 2: 查询闲置列表
  GET /api/idle

Step 3: 调配闲置资产
  PUT /api/idle/{id}/allocate
  Body: {"target_department": "目标科室", "allocate_date": "2026-04-02"}

Step 4: 取消闲置发布
  PUT /api/idle/{id}/cancel
```

## 5. 报废申请流程

```
Step 1: 创建报废申请
  POST /api/scrapping
  Body: {
    "asset_code": "xxx",
    "asset_name": "资产名称",
    "applicant": "申请人",
    "scrapping_reason": "报废原因",
    "estimated_value": 5000
  }

Step 2: 查询报废记录
  GET /api/scrapping

Step 3: 审批报废
  POST /api/scrapping/{id}/approve
  Body: {"approved": true, "opinion": "同意"}

Step 4: 完成报废
  POST /api/scrapping/{id}/complete
```

## 6. 采购申请流程

```
Step 1: 创建采购申请
  POST /api/procurement/requests
  Body: {
    "title": "采购标题",
    "department": "需求部门",
    "applicant": "申请人",
    "budget": 150000,
    "remark": "备注"
  }

Step 2: 查询采购列表
  GET /api/procurement/requests

Step 3: 审批采购
  PUT /api/procurement/requests/{id}/approve
  Body: {"approved": true, "opinion": "同意"}

Step 4: 执行采购
  PUT /api/procurement/requests/{id}/execute
  Body: {"completed": true, "result": "已完成采购"}

Step 5: 验收
  PUT /api/procurement/requests/{id}/acceptance
```

## 7. 文档上传审核流程

```
Step 1: 上传文档
  POST /api/technical-documents
  Body (form-data):
    file: <文件>
    title: "资料标题"
    category: "技术资料"
    asset_code: "xxx"

Step 2: 审核文档
  POST /api/technical-documents/{id}/review
  Body: {"status": "approved", "comment": "审核通过"}

Step 3: 创建分享链接
  POST /api/technical-documents/{id}/share
  Body: {"expires_days": 30, "supplier_name": "供应商"}

Step 4: AI 问答
  POST /api/technical-documents/ai/ask
  Body: {"question": "问题", "document_ids": [ID1, ID2]}
```

## 8. 预防性维护流程

```
Step 1: 创建维护计划
  POST /api/maintenance/plans
  Body: {
    "plan_name": "CT机年度维护",
    "asset_code": "xxx",
    "maintenance_type": "预防性维护",
    "cycle_type": "year",
    "cycle_value": 1,
    "trigger_type": "time",
    "responsible_person": "负责人"
  }

Step 2: 配置提醒
  POST /api/maintenance/reminders/config
  Body: {
    "plan_id": 计划ID,
    "reminder_days": 7,
    "reminder_types": ["email", "sms"],
    "recipient": "工程师"
  }

Step 3: 执行维护
  POST /api/maintenance/plans/{id}/complete
  Body: {
    "maintenance_date": "2026-04-01",
    "maintenance_person": "张三",
    "actual_hours": 4,
    "parts_replaced": "滤网",
    "maintenance_result": "正常"
  }

Step 4: 查看维护历史
  GET /api/maintenance/plans/{id}/history
```

## 9. IoT 设备注册与数据上报

```
Step 1: 注册 IoT 设备
  POST /api/iot/devices
  Body: {
    "device_name": "温湿度传感器-001",
    "device_type": "environment_sensor",
    "device_id": "ENV-001",
    "asset_code": "ASSET-001",
    "manufacturer": "小米"
  }

Step 2: 上报设备位置
  POST /api/iot/location/assets/{assetCode}/location
  Body: {"latitude": 31.23, "longitude": 121.47, "location_code": "L001"}

Step 3: 批量上报区域定位
  POST /api/iot/zone-location/ingest/batch
  Body: {
    "events": [
      {
        "device_id": "BEACON-001",
        "asset_code": "ASSET-001",
        "event_time": "2026-04-01T10:00:00Z",
        "location_code": "L001",
        "rssi": -65
      }
    ]
  }

Step 4: 查询最新位置
  GET /api/iot/zone-location/assets/{assetCode}/latest

Step 5: 查询位置历史
  GET /api/iot/location/assets/{assetCode}/location/history
```

## 10. 质检记录流程

```
Step 1: 创建计量记录
  POST /api/quality-control/metrology
  Body: {
    "asset_code": "xxx",
    "metrology_type": "年度计量",
    "metrology_date": "2026-04-01",
    "result": "合格"
  }

Step 2: 创建质量控制记录
  POST /api/quality-control/quality-control
  Body: {
    "asset_code": "xxx",
    "qc_type": "性能检测",
    "qc_date": "2026-04-01",
    "result": "合格",
    "finding": "无异常"
  }

Step 3: 查询质检历史
  GET /api/quality-control/asset/{assetCode}/history

Step 4: 统计查询
  GET /api/quality-control/metrology/statistics
  GET /api/quality-control/quality-control/statistics
```

---

# 🔍 查询决策树

## "查某类设备"问题

```
用户要查某类设备（未限定科室）
  │
  └─ GET /api/assets?search=<设备名称>&pageSize=50 ✅
     (不要用 keyword 参数，会遗漏数据)
```

## "查询科室资产"问题 ⚠️ 重要

```
用户要查某科室资产（如"检验科资产"、"病理科资产"）
  │
  ├─ 陷阱：API的department参数只能匹配 department 字段
  │         科室信息大量存在 location / use_department 字段中
  │         例："检验科"资产实际在 location="检验科（崇山）" 下
  │
  └─ ✅ 正确做法：全量扫描（遍历所有页），在代码中过滤所有科室相关字段
       扫描字段：department / location / use_department / department_new
       否则会漏掉 50%~80% 的数据！
```

## "查询调配记录"问题

```
用户要查询调配
  │
  └─ GET /api/transfer 或 GET /api/assets/transfer-requests
```

## "查询盘点状态"问题

```
用户要查盘点
  │
  ├─ 盘点计划: GET /api/inventory-plans
  ├─ 盘点任务: GET /api/inventory-tasks
  └─ 盘点差异: GET /api/inventory-discrepancies
```

## "查询维修记录"问题

```
用户要查维修
  │
  ├─ 维修申请: GET /api/maintenance/requests
  ├─ 维修工单: GET /api/maintenance/workorders
  └─ 维修日志: GET /api/maintenance/logs
```

## "查询资产详情"问题

```
已知资产编号
  └─ GET /api/assets/{id}  (id 为数字 ID)

已知资产编码
  └─ 先 GET /api/assets?search=<asset_code> 找到 id
```

## ⚠️ 全量扫描规范（适用于全面统计场景）

当用户要求"全院某类资产统计"、科室资产统计等需要完整数据时：

```
1. 分页遍历：总资产 28291 条，每页 300 条，共 95 页
   → 必须遍历所有页，不能只取前几页

2. 关键词过滤：在 Python 脚本中遍历所有资产，对所有文本字段
   （asset_name / location / department / use_department / department_new 等）
   进行关键词匹配

3. 科室查询示例（以"检验科"为例）：
   - ❌ 错误：只查 department='检验科' → 漏掉 415 件
   - ✅ 正确：遍历所有资产，对所有字段匹配 '检验科'
     → 匹配到 550 件（分布在 location/department 等多字段）

4. 统计输出：
   - 按 location 分组汇总（location 含科室信息最多）
   - 计算每组数量、总价值、状态分布
   - 输出高价值资产（>5万或>10万）
   - 输出品牌/类型分布
```

---

# 📖 常用 API 调用示例

## 资产操作

```bash
# 资产列表（模糊搜索）
bash scripts/assethub_api.sh request GET "/assets?page=1&pageSize=20&search=监护仪"

# ⚠️ 按科室查询资产——重要提醒：
# department 参数只能匹配 department 字段
# 科室信息大量存储在 location / use_department / department_new 字段
# 如需完整科室资产，必须全量扫描（见上方"全量扫描规范"）
bash scripts/assethub_api.sh request GET "/assets?page=1&pageSize=20&department_id=3"

# 资产列表（按状态筛选）
bash scripts/assethub_api.sh request GET "/assets?page=1&pageSize=20&status=在用"

# 资产详情
bash scripts/assethub_api.sh request GET "/assets/123"

# 创建资产
bash scripts/assethub_api.sh request POST "/assets" '{
  "asset_code": "ZY20260402001",
  "asset_name": "医用 CT 扫描仪",
  "category_id": 1,
  "purchase_price": 5000000,
  "status": "在用",
  "department_id": 3
}'

# 更新资产
bash scripts/assethub_api.sh request PUT "/assets/123" '{
  "asset_name": "医用 CT 扫描仪（新）",
  "status": "维修"
}'

# 资产变更日志
bash scripts/assethub_api.sh request GET "/assets/123/change-logs"

# 导出资产
bash scripts/assethub_api.sh request GET "/assets/export?status=在用"
```

## 维修管理

```bash
# 维修申请列表
bash scripts/assethub_api.sh request GET "/maintenance/requests?page=1&pageSize=20"

# 维修申请列表（按状态）
bash scripts/assethub_api.sh request GET "/maintenance/requests?status=pending&pageSize=20"

# 创建维修申请（AI 安全入口，一次完成，无需二次确认）
# 注意：curl 直接调用时需添加 Idempotency-Key Header
bash scripts/assethub_api.sh request POST "/maintenance/ai/submit-request" '{
  "asset_code": "CT-001",
  "issue_description": "球管打火，报警 E01",
  "fault_description": "球管打火，报警 E01",
  "fault_level": "紧急",
  "priority": "critical",
  "request_department": "放射科",
  "contact_phone": "13800138000",
  "source": "assetclaw",
  "intent": "repair_request"
}'

# 直接 curl 调用（需手动加 Idempotency-Key）
curl -sS -X POST "http://160ttth72797.vicp.fun/api/maintenance/ai/submit-request" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "X-Tenant-ID: <TENANT_ID>" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: op-$(date +%s)-$RANDOM" \
  -d '{"asset_code":"CT-001","fault_description":"球管打火，报警 E01","issue_description":"球管打火，报警 E01","fault_level":"紧急","priority":"critical","request_department":"放射科","contact_phone":"13800138000","source":"assetclaw","intent":"repair_request"}'

# 审批维修申请
bash scripts/assethub_api.sh request POST "/maintenance/requests/123/approve" '{
  "approved": true,
  "opinion": "同意维修"
}'
# 注：curl 直接调用时需添加 Idempotency-Key Header

# 开始执行维修
bash scripts/assethub_api.sh request POST "/maintenance/requests/123/start" '{
  "repair_person": "李四"
}'
# 注：curl 直接调用时需添加 Idempotency-Key Header

# 完成维修
bash scripts/assethub_api.sh request POST "/maintenance/requests/123/complete" '{
  "repair_content": "更换球管，清理内部灰尘，校准参数",
  "repair_cost": 150000,
  "parts_replaced": "CT球管",
  "repair_end_date": "2026-04-03"
}'
# 注：curl 直接调用时需添加 Idempotency-Key Header

# 维修工单列表
bash scripts/assethub_api.sh request GET "/maintenance/workorders?page=1&pageSize=20"

# 创建维修工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders" '{
  "title": "CT 设备故障维修",
  "asset_code": "CT-001",
  "priority": "critical",
  "description": "球管老化，需要更换",
  "estimated_hours": 24
}'

# 分配维修工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/123/assign" '{
  "assigned_to": "李四",
  "assignee_name": "李四"
}'

# 完成维修工单
bash scripts/assethub_api.sh request POST "/maintenance/workorders/123/complete" '{
  "work_content": "更换球管完成",
  "actual_hours": 20,
  "labor_cost": 2000,
  "outsourcing_cost": 0,
  "materials": [{"name": "球管", "quantity": 1, "cost": 148000}]
}'

# 维修日志列表
bash scripts/assethub_api.sh request GET "/maintenance/logs?page=1&pageSize=20"

# 创建维修日志
bash scripts/assethub_api.sh request POST "/maintenance/logs" '{
  "asset_code": "ZY2020000122",
  "maintenance_type": "故障维修",
  "maintenance_date": "2026-04-01",
  "maintenance_person": "张三",
  "maintenance_content": "更换碳纤维骨科牵引架轴承",
  "maintenance_duration": 2,
  "parts_replaced": "轴承",
  "maintenance_cost": 500
}'

# 维修统计
bash scripts/assethub_api.sh request GET "/maintenance/statistics?start_date=2026-01-01&end_date=2026-04-01"

# 维修效率统计
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/overview"

# 维修费用分析
bash scripts/assethub_api.sh request GET "/maintenance/costs/analysis"
```

## 调配/闲置/报废

```bash
# 调配申请列表
bash scripts/assethub_api.sh request GET "/transfer?page=1&pageSize=20"

# 发起调配申请
bash scripts/assethub_api.sh request POST "/transfer" '{
  "asset_code": "XXX-001",
  "reason": "科室合并，需调拨设备",
  "to_department": "心内科"
}'

# 审批调配
bash scripts/assethub_api.sh request PUT "/transfer/123/approve" '{
  "approved": true,
  "opinion": "同意"
}'

# 执行调配完成
bash scripts/assethub_api.sh request PUT "/transfer/123/complete"

# 闲置资产列表
bash scripts/assethub_api.sh request GET "/idle?page=1&pageSize=20"

# 发布闲置
bash scripts/assethub_api.sh request POST "/idle" '{
  "asset_code": "XXX-001",
  "publish_person": "王五"
}'

# 调配闲置资产
bash scripts/assethub_api.sh request PUT "/idle/123/allocate" '{
  "target_department": "放射科",
  "allocate_date": "2026-04-02"
}'

# 报废申请列表
bash scripts/assethub_api.sh request GET "/scrapping?page=1&pageSize=20"

# 创建报废申请
bash scripts/assethub_api.sh request POST "/scrapping" '{
  "asset_code": "OLD-CT-001",
  "asset_name": "旧 CT 扫描仪",
  "applicant": "张三",
  "scrapping_reason": "设备老旧，无法维修",
  "estimated_value": 5000
}'

# 审批报废
bash scripts/assethub_api.sh request POST "/scrapping/123/approve" '{
  "approved": true,
  "opinion": "同意报废"
}'

# 完成报废
bash scripts/assethub_api.sh request POST "/scrapping/123/complete"
```

## 盘点

```bash
# 盘点计划列表
bash scripts/assethub_api.sh request GET "/inventory-plans?page=1&pageSize=20"

# 创建盘点计划
bash scripts/assethub_api.sh request POST "/inventory-plans" '{
  "plan_name": "2026年上半年度设备盘点",
  "plan_no": "PD-2026-001",
  "start_date": "2026-04-01",
  "end_date": "2026-04-30",
  "remark": "全院资产盘点"
}'

# 激活盘点计划
bash scripts/assethub_api.sh request PUT "/inventory-plans/123/activate"

# 盘点任务列表
bash scripts/assethub_api.sh request GET "/inventory-tasks?page=1&pageSize=20"

# 创建盘点任务
bash scripts/assethub_api.sh request POST "/inventory-tasks" '{
  "inventory_plan_id": 123,
  "task_name": "放射科室盘点任务",
  "assignee": "李四",
  "assignee_name": "李四",
  "location": "放射科",
  "department_code": "DEPT-001"
}'

# 开始盘点
bash scripts/assethub_api.sh request PUT "/inventory-tasks/123/start"

# 完成盘点
bash scripts/assethub_api.sh request PUT "/inventory-tasks/123/complete" '{
  "actual_count": 50,
  "remark": "部分设备位置有调整"
}'

# 盘点差异列表
bash scripts/assethub_api.sh request GET "/inventory-discrepancies?page=1&pageSize=20"

# 处理盘点差异
bash scripts/assethub_api.sh request PUT "/inventory-discrepancies/123/handle" '{
  "handling_status": "已处理",
  "handling_method": "正常",
  "handling_notes": "已确认位置正确"
}'

# 批量处理盘点差异
bash scripts/assethub_api.sh request POST "/inventory-discrepancies/batch-handle" '{
  "ids": [1, 2, 3],
  "handling_status": "已处理",
  "handling_method": "正常"
}'

# 完成盘点计划
bash scripts/assethub_api.sh request PUT "/inventory-plans/123/complete"

# 取消盘点计划
bash scripts/assethub_api.sh request PUT "/inventory-plans/123/cancel"
```

## 采购/质检/验收

```bash
# 采购申请列表
bash scripts/assethub_api.sh request GET "/procurement/requests?page=1&pageSize=20"

# 创建采购申请
bash scripts/assethub_api.sh request POST "/procurement/requests" '{
  "title": "迈瑞监护仪采购",
  "department": "心内科",
  "applicant": "张三",
  "budget": 150000,
  "remark": "科室新增需要"
}'

# 审批采购
bash scripts/assethub_api.sh request PUT "/procurement/requests/123/approve" '{
  "approved": true,
  "opinion": "同意采购"
}'

# 执行采购
bash scripts/assethub_api.sh request PUT "/procurement/requests/123/execute" '{
  "completed": true,
  "result": "已完成采购"
}'

# 验收
bash scripts/assethub_api.sh request PUT "/procurement/requests/123/acceptance"

# 计量记录列表
bash scripts/assethub_api.sh request GET "/quality-control/metrology?page=1&pageSize=20"

# 创建计量记录
bash scripts/assethub_api.sh request POST "/quality-control/metrology" '{
  "asset_code": "XXX-001",
  "metrology_type": "年度计量",
  "metrology_date": "2026-04-01",
  "result": "合格"
}'

# 质量控制记录列表
bash scripts/assethub_api.sh request GET "/quality-control/quality-control?page=1&pageSize=20"

# 创建质量控制记录
bash scripts/assethub_api.sh request POST "/quality-control/quality-control" '{
  "asset_code": "XXX-001",
  "qc_type": "年度质检",
  "qc_date": "2026-04-01",
  "qc_person": "李四",
  "result": "合格",
  "finding": "无异常"
}'

# 质检统计
bash scripts/assethub_api.sh request GET "/quality-control/statistics"

# 验收记录列表
bash scripts/assethub_api.sh request GET "/acceptance/records?page=1&pageSize=20"

# 创建验收记录
bash scripts/assethub_api.sh request POST "/acceptance/records" '{
  "asset_code": "XXX-001",
  "acceptance_date": "2026-04-01",
  "acceptor": "张三",
  "result": "合格",
  "finding": "无异常"
}'
```

## 文档

```bash
# 文档列表
bash scripts/assethub_api.sh request GET "/technical-documents?page=1&pageSize=20&keyword=CT"

# 文档列表（按分类）
bash scripts/assethub_api.sh request GET "/technical-documents?category=技术资料&pageSize=20"

# 上传文档（需要 form-data，curl 示例）
curl -sS -X POST "http://160ttth72797.vicp.fun/api/technical-documents" \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@/path/to/file.pdf" \
  -F "title=设备操作手册" \
  -F "category=操作手册" \
  -F "asset_code=XXX-001"

# 审核文档
bash scripts/assethub_api.sh request POST "/technical-documents/123/review" '{
  "status": "approved",
  "comment": "审核通过"
}'

# 创建文档分享
bash scripts/assethub_api.sh request POST "/technical-documents/123/share" '{
  "expires_days": 30,
  "supplier_name": "供应商名称"
}'

# 文档评论
bash scripts/assethub_api.sh request POST "/technical-documents/enhanced/documents/123/comments" '{
  "content": "文档内容有误，请更正"
}'

# 收藏文档
bash scripts/assethub_api.sh request POST "/technical-documents/enhanced/documents/123/favorite"

# AI 问答
bash scripts/assethub_api.sh request POST "/technical-documents/ai/ask" '{
  "question": "这台设备的维护周期是多久？",
  "document_ids": [1, 2, 3]
}'

# AI 搜索
bash scripts/assethub_api.sh request POST "/technical-documents/ai/search" '{
  "query": "CT 球管维护"
}'

# 文档分类列表
bash scripts/assethub_api.sh request GET "/technical-documents/enhanced/categories"

# 文档标签列表
bash scripts/assethub_api.sh request GET "/technical-documents/enhanced/tags"
```

## 预防性维护

```bash
# 维护计划列表
bash scripts/assethub_api.sh request GET "/maintenance/plans?page=1&pageSize=20"

# 创建维护计划
bash scripts/assethub_api.sh request POST "/maintenance/plans" '{
  "plan_name": "CT机年度维护",
  "asset_code": "CT-001",
  "maintenance_type": "预防性维护",
  "cycle_type": "year",
  "cycle_value": 1,
  "trigger_type": "time",
  "responsible_person": "李工程师",
  "next_maintenance_date": "2027-01-01"
}'

# 配置维护提醒
bash scripts/assethub_api.sh request POST "/maintenance/reminders/config" '{
  "plan_id": 123,
  "reminder_days": 7,
  "reminder_types": ["email", "sms"],
  "recipient": "李工程师"
}'

# 发送维护提醒
bash scripts/assethub_api.sh request POST "/maintenance/reminders/send" '{
  "plan_id": 123,
  "reminder_type": "email"
}'

# 检查维护提醒
bash scripts/assethub_api.sh request GET "/maintenance/reminders/check"

# 完成维护计划
bash scripts/assethub_api.sh request POST "/maintenance/plans/123/complete" '{
  "maintenance_date": "2026-04-01",
  "maintenance_person": "李工程师",
  "actual_hours": 4,
  "parts_replaced": "滤网",
  "maintenance_result": "正常",
  "maintenance_cost": 500
}'

# 维护计划历史
bash scripts/assethub_api.sh request GET "/maintenance/plans/123/history"

# 维修模板列表
bash scripts/assethub_api.sh request GET "/maintenance/templates?page=1&pageSize=20"
```

## 折旧

```bash
# 折旧列表
bash scripts/assethub_api.sh request GET "/depreciation?page=1&pageSize=20"

# 按部门折旧汇总
bash scripts/assethub_api.sh request GET "/depreciation/summary/by-department"

# 按月折旧趋势
bash scripts/assethub_api.sh request GET "/depreciation/summary/by-month?months=12"

# 按类型折旧汇总
bash scripts/assethub_api.sh request GET "/depreciation/summary/by-type"

# 计算折旧
bash scripts/assethub_api.sh request POST "/depreciation/calculate" '{
  "as_of_date": "2026-04-01"
}'

# 折旧方法列表
bash scripts/assethub_api.sh request GET "/depreciation/methods"

# 导出折旧报表
bash scripts/assethub_api.sh request GET "/depreciation/export"
```

## 部门/用户/角色

```bash
# 部门树
bash scripts/assethub_api.sh request GET "/departments/tree"

# 部门列表
bash scripts/assethub_api.sh request GET "/departments?page=1&pageSize=20"

# 创建部门
bash scripts/assethub_api.sh request POST "/departments" '{
  "department_name": "放射科",
  "parent_code": "ROOT"
}'

# 用户列表
bash scripts/assethub_api.sh request GET "/users?page=1&pageSize=20"

# 创建用户
bash scripts/assethub_api.sh request POST "/users" '{
  "username": "zhangsan",
  "real_name": "张三",
  "password": "Password123",
  "role": "engineer",
  "email": "zhangsan@example.com",
  "phone": "13800138000"
}'

# 获取当前用户信息
bash scripts/assethub_api.sh request GET "/users/me"

# 角色列表
bash scripts/assethub_api.sh request GET "/roles-permissions/roles"

# 获取角色权限
bash scripts/assethub_api.sh request GET "/roles-permissions/roles/engineer/permissions"

# 更新角色权限
bash scripts/assethub_api.sh request PUT "/roles-permissions/roles/engineer/permissions" '{
  "permissions": ["asset.view", "asset.create", "maintenance.request"]
}'

# 获取角色菜单
bash scripts/assethub_api.sh request GET "/roles-permissions/roles/engineer/menus"

# 更新角色菜单
bash scripts/assethub_api.sh request PUT "/roles-permissions/roles/engineer/menus" '{
  "menus": ["assets", "maintenance", "inventory"]
}'

# 当前用户菜单权限
bash scripts/assethub_api.sh request GET "/roles-permissions/user/menus"
```

## IoT/定位

```bash
# IoT 设备列表
bash scripts/assethub_api.sh request GET "/iot/devices?page=1&pageSize=20"

# 注册 IoT 设备
bash scripts/assethub_api.sh request POST "/iot/devices" '{
  "device_name": "温湿度传感器-001",
  "device_type": "environment_sensor",
  "device_id": "ENV-001",
  "asset_code": "ASSET-001",
  "manufacturer": "小米",
  "model": "MHO-A400"
}'

# 上报设备定位数据
bash scripts/assethub_api.sh request POST "/iot/location/assets/ASSET-001/location" '{
  "latitude": 31.2304,
  "longitude": 121.4737,
  "altitude": 10,
  "battery_level": 85
}'

# 批量上报区域定位
bash scripts/assethub_api.sh request POST "/iot/zone-location/ingest/batch" '{
  "events": [
    {
      "device_id": "BEACON-001",
      "asset_code": "ASSET-001",
      "event_time": "2026-04-01T10:00:00Z",
      "location_code": "L001",
      "building_name": "门诊楼",
      "floor_number": 3,
      "area_name": "放射科",
      "rssi": -65,
      "battery_level": 85
    }
  ]
}'

# 查询最新环境监测数据
bash scripts/assethub_api.sh request GET "/iot/environment-monitoring/assets/ASSET-001/latest"

# 查询资产位置历史
bash scripts/assethub_api.sh request GET "/iot/location/assets/ASSET-001/location/history?start_time=2026-04-01&end_time=2026-04-02"

# 资产绑定设备
bash scripts/assethub_api.sh request POST "/asset-location/assets/ASSET-001/bind-device" '{
  "device_id": "BEACON-001"
}'

# 查询区域定位管道健康状态
bash scripts/assethub_api.sh request GET "/iot/zone-location/pipeline/health"

# 查询设备类型列表
bash scripts/assethub_api.sh request GET "/iot/devices/types"
```

## 标签打印

```bash
# 标签模板列表
bash scripts/assethub_api.sh request GET "/asset-labels/templates?page=1&pageSize=20"

# 创建标签模板
bash scripts/assethub_api.sh request POST "/asset-labels/templates" '{
  "name": "标准资产标签",
  "description": "包含资产编号、名称、位置",
  "width": 4,
  "height": 2,
  "dpi": 300,
  "fields": [
    {"field_name": "asset_code", "label": "资产编号", "x": 0, "y": 0},
    {"field_name": "asset_name", "label": "资产名称", "x": 0, "y": 20}
  ]
}'

# 批量生成 ZPL 标签
bash scripts/assethub_api.sh request POST "/asset-labels/generate-zpl-batch" '{
  "template_id": 1,
  "asset_codes": ["ASSET-001", "ASSET-002", "ASSET-003"],
  "quantity_per_asset": 1
}'

# 测试打印机连接
bash scripts/assethub_api.sh request POST "/asset-labels/printer/test-connection" '{
  "printer_ip": "192.168.1.100",
  "printer_port": 9100,
  "timeout_ms": 5000
}'

# 打印标签
bash scripts/assethub_api.sh request POST "/asset-labels/print" '{
  "template_id": 1,
  "asset_code": "ASSET-001",
  "printer_ip": "192.168.1.100",
  "printer_port": 9100,
  "quantity": 1,
  "print_timeout_ms": 10000,
  "retry_count": 3
}'
```

## 告警

```bash
# 智能告警列表
bash scripts/assethub_api.sh request GET "/intelligent-alerts?page=1&pageSize=20"

# 告警概览
bash scripts/assethub_api.sh request GET "/intelligent-alerts/overview"

# 处理告警
bash scripts/assethub_api.sh request POST "/intelligent-alerts/123/handle" '{
  "handle_result": "已确认并处理"
}'

# 标记告警为已读
bash scripts/assethub_api.sh request POST "/intelligent-alerts/123/read"

# 全部标记已读
bash scripts/assethub_api.sh request POST "/intelligent-alerts/read-all"

# 位置告警列表
bash scripts/assethub_api.sh request GET "/location-alerts?page=1&pageSize=20"

# 处理位置告警
bash scripts/assethub_api.sh request PUT "/location-alerts/123/handle" '{
  "handle_result": "已确认资产位置正常"
}'

# 批量处理位置告警
bash scripts/assethub_api.sh request POST "/location-alerts/batch/handle" '{
  "ids": [1, 2, 3],
  "handle_result": "已确认"
}'

# 位置告警统计
bash scripts/assethub_api.sh request GET "/location-alerts/stats"
```

## 审计/备份

```bash
# 审计日志列表
bash scripts/assethub_api.sh request GET "/audit-logs?page=1&pageSize=20"

# 审计日志列表（按操作类型）
bash scripts/assethub_api.sh request GET "/audit-logs?action_type=asset.create&pageSize=20"

# 审计日志统计
bash scripts/assethub_api.sh request GET "/audit-logs/stats?start_date=2026-01-01&end_date=2026-04-01"

# 备份列表
bash scripts/assethub_api.sh request GET "/backup?page=1&pageSize=20"

# 创建备份
bash scripts/assethub_api.sh request POST "/backup" '{
  "description": "定期备份 2026-04-01"
}'

# 恢复备份
bash scripts/assethub_api.sh request POST "/backup/123/restore" '{
  "confirm": true
}'
```

## 仪表盘/统计

```bash
# 仪表盘概览
bash scripts/assethub_api.sh request GET "/dashboard"

# 实时数据
bash scripts/assethub_api.sh request GET "/dashboard/realtime"

# 资产价值分布
bash scripts/assethub_api.sh request GET "/analysis/value-distribution"

# 折旧趋势
bash scripts/assethub_api.sh request GET "/analysis/depreciation"

# 风险仪表盘
bash scripts/assethub_api.sh request GET "/risk/dashboard"

# 合规状态
bash scripts/assethub_api.sh request GET "/compliance/status"

# 合规仪表盘统计
bash scripts/assethub_api.sh request GET "/compliance/dashboard-stats"
```

## 模块配置

```bash
# 模块列表
bash scripts/assethub_api.sh request GET "/modules?page=1&pageSize=20"

# 租户模块配置列表
bash scripts/assethub_api.sh request GET "/module-configs/list"

# 启用模块
bash scripts/assethub_api.sh request POST "/module-configs/enable" '{
  "module_id": "assets",
  "config": {}
}'

# 停用模块
bash scripts/assethub_api.sh request POST "/module-configs/disable" '{
  "module_id": "assets"
}'

# 获取单模块配置
bash scripts/assethub_api.sh request GET "/module-configs/assets"

# 更新模块配置
bash scripts/assethub_api.sh request PUT "/module-configs/assets" '{
  "enabled": true,
  "config": {"key": "value"}
}'

# 获取模块菜单权限
bash scripts/assethub_api.sh request GET "/module-configs/assets/menus"

# 批量更新模块菜单
bash scripts/assethub_api.sh request PUT "/module-configs/assets/menus" '{
  "menus": [
    {"menu_key": "assets", "is_visible": true},
    {"menu_key": "maintenance", "is_visible": true}
  ]
}'

# 模块版本历史
bash scripts/assethub_api.sh request GET "/module-configs/assets/versions"

# 创建模块版本备份
bash scripts/assethub_api.sh request POST "/module-configs/assets/versions" '{
  "change_log": "配置更新"
}'

# 回滚模块版本
bash scripts/assethub_api.sh request POST "/module-configs/assets/rollback" '{
  "version_id": 5
}'

# 验证模块配置
bash scripts/assethub_api.sh request GET "/module-configs/assets/validate"
```

## 工作流

```bash
# 获取默认工作流
bash scripts/assethub_api.sh request GET "/workflow/default"

# 获取工作流状态
bash scripts/assethub_api.sh request GET "/workflow/states"

# 获取迁移规则
bash scripts/assethub_api.sh request GET "/workflow/transitions"

# 执行状态迁移
bash scripts/assethub_api.sh request POST "/workflow/transition/123" '{
  "transition_id": 2,
  "reason": "设备报废"
}'

# 获取资产可执行状态迁移
bash scripts/assethub_api.sh request GET "/assets/123/transitions"
```

## AI 分析

```bash
# AI 故障分析
bash scripts/assethub_api.sh request GET "/asset-ai-analysis/analysis-history?page=1&pageSize=20"

# 分析单个资产
bash scripts/assethub_api.sh request POST "/asset-ai-analysis/analyze-asset/CT-001" '{
  "start_date": "2026-01-01",
  "end_date": "2026-04-01"
}'

# 批量分析资产
bash scripts/assethub_api.sh request POST "/asset-ai-analysis/analyze-assets" '{
  "asset_codes": ["CT-001", "CT-002"],
  "analysis_type": "fault_prediction"
}'

# 维修效率分析
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/overview"

# 维修响应时间统计
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/response-time"

# 工程师绩效统计
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/technician"

# 资产使用频率
bash scripts/assethub_api.sh request GET "/maintenance/efficiency/asset-frequency"

# 维修类型分布
bash scripts/assethub_api.sh request GET "/maintenance/analysis/type-distribution"

# 维修费用趋势
bash scripts/assethub_api.sh request GET "/maintenance/analysis/cost-trend"

# 预测性维护
bash scripts/assethub_api.sh request POST "/agent-mesh/intelligence/predictive-maintenance" '{
  "asset_code": "CT-001",
  "days_ahead": 30
}'

# 风险评分
bash scripts/assethub_api.sh request POST "/agent-mesh/intelligence/risk-score" '{
  "asset_code": "CT-001"
}'

# 健康指数
bash scripts/assethub_api.sh request POST "/agent-mesh/intelligence/health-index" '{
  "asset_code": "CT-001"
}'

# 维修 AI 对话初始化
bash scripts/assethub_api.sh request POST "/maintenance/ai/init"

# 维修 AI 发送消息
bash scripts/assethub_api.sh request POST "/maintenance/ai/message" '{
  "conversation_id": "conv-xxx",
  "message": "CT球管打火怎么办"
}'
```

## 库存管理

```bash
# 库存记录列表
bash scripts/assethub_api.sh request GET "/inventory?page=1&pageSize=20"

# 创建库存记录
bash scripts/assethub_api.sh request POST "/inventory" '{
  "item_name": "球管",
  "category": "备件",
  "warehouse": "备件库",
  "location": "A区-01",
  "quantity": 5,
  "unit": "个",
  "remark": "CT备件"
}'

# 调整库存
# 入库:
bash scripts/assethub_api.sh request PUT "/inventory/123" '{
  "adjust_type": "in",
  "quantity": 2,
  "reason": "新购入库"
}'
# 出库:
bash scripts/assethub_api.sh request PUT "/inventory/123" '{
  "adjust_type": "out",
  "quantity": 1,
  "reason": "维修使用"
}'
# 调整:
bash scripts/assethub_api.sh request PUT "/inventory/123" '{
  "adjust_type": "adj",
  "quantity": -1,
  "reason": "盘点调整"
}'
```

## 系统配置

```bash
# 获取数据库配置
bash scripts/assethub_api.sh request GET "/system-config/database"

# 更新数据库配置
bash scripts/assethub_api.sh request PUT "/system-config/database" '{
  "host": "localhost",
  "port": 3306,
  "database": "assethub",
  "user": "root",
  "password": "newpassword"
}'

# 测试数据库连接
bash scripts/assethub_api.sh request POST "/system-config/database/test"

# IoT Token 列表
bash scripts/assethub_api.sh request GET "/system-config/iot-tokens"

# 生成 IoT Token
bash scripts/assethub_api.sh request POST "/system-config/iot-tokens/generate" '{
  "name": "网关Token",
  "scopes": ["zone-location:write", "environment:write"]
}'

# 验证 IoT Token
bash scripts/assethub_api.sh request POST "/system-config/iot-tokens/verify" '{
  "token": "iot-xxx"
}'

# 获取 IoT Token 使用指南
bash scripts/assethub_api.sh request GET "/system-config/iot-tokens/usage-guide"
```

---

# ⚠️ 重要兼容说明

## 维修申请字段

- **必填**: `asset_code` + `fault_description`
- **兼容旧文档**: 可同时传 `issue_description`（与 `fault_description` 相同值）

## 调配申请

- 新版路径: `POST /api/transfer`
- 旧版路径: `POST /api/assets/{id}/transfer-apply`（兼容 `asset_code` 参数）

## 闲置发布

- `publish_person` 必填
- `asset_code` 和 `asset_name` 至少一个

## 报废申请

- 必填: `asset_code`, `asset_name`, `applicant`, `scrapping_reason`

## 盘点计划

- 新版路径: `/inventory-plans`（推荐）
- 旧版路径: `/inventory`

---

# 📤 输出格式规范

**查询结果统一用表格展示**，字段包括：
- 编号/ID、名称/标题、状态
- 关联资产/部门/人员
- 创建时间/更新时间
- 关键数值（价格、数量、费用等）

**统计类查询**应包含合计行和关键洞察。

**操作结果**先展示操作内容，再展示回查确认结果。

---

# 📍 常见设备名称映射

| 用户说 | 系统资产名称 |
|--------|------------|
| 监护仪 | 插件式病人监护仪 |
| 心电/心电图机 | 数字式多道心电图机、12导联心电图机等 |
| 呼吸机 | 呼吸机 |
| 注射泵 | 注射泵 |
| 除颤仪 | 体外除颤监护仪 |
| 血液透析 | 血液透析设备(血液透析滤过机) |
| CT | CT机、16层CT机、64排螺旋CT等 |
| 核磁共振 | 核磁共振成像设备(MRI) |
| 车辆/机动车 | 救护车、轿车、客车、旅行车、核酸检测车、铲车、装载机、电动车（指机动车，非手推车） |

---

# 📝 故障描述规范

报修时的描述应尽量具体：

| 规范 | 示例 |
|------|------|
| ✅ 正确 | "显示屏不亮，无法开机" |
| ✅ 正确 | "心电导联无信号" |
| ✅ 正确 | "CT球管打火，报警E01" |
| ❌ 错误 | "坏了" / "不能用" / "故障" |

---

# 🔢 状态值速查

| 资源 | 状态值 |
|------|--------|
| 资产 | `在用` / `维修` / `闲置` / `调配中` / `报废` |
| 维修申请 | `pending` / `approved` / `in_progress` / `completed` / `cancelled` |
| 调配 | `pending` / `approved` / `rejected` / `completed` |
| 盘点计划 | `draft` / `active` / `completed` / `cancelled` |
| 盘点任务 | `pending` / `in_progress` / `completed` / `cancelled` |
| 采购 | `pending` / `approved` / `rejected` / `executed` / `completed` |
| 报废 | `pending` / `approved` / `rejected` / `completed` |
| 质检结果 | `合格` / `不合格` / `待整改` |
| 文档审核 | `pending` / `approved` / `rejected` |

---

# 📝 经验教训（基于实际操作发现）

## 2026-04-02 关键发现：科室资产多字段分布问题

**问题现象：**
- 查询"检验科资产"时，使用 `department=检验科` 参数只返回 0 条记录
- 全量扫描（遍历所有页 + 所有文本字段）后，发现检验科实际有 **550 件资产**

**根本原因：**
AssetHub 的科室信息分散存储在多个字段：
- `department` — 正式科室字段（很多资产此处为空）
- `location` — 位置字段，包含大量科室信息（如"检验科（崇山）"）
- `use_department` — 使用科室字段
- `department_new` — 新版科室字段

**经验：**
1. 查询科室资产时，**必须**对所有文本字段做关键词匹配，不能依赖单一 department 参数
2. 全量扫描时需遍历**所有页**（总资产 28291 条 × 95 页）
3. 车辆识别需要排除"输液车/处置车/抢救车"等医用小型手推车

## 2026-04-02 发现：API 安全机制与 AI 入口

**问题现象：**
- 直接调用 `/maintenance/requests` POST 无 Idempotency-Key → 返回"需要 Idempotency-Key"
- 带 Idempotency-Key 调用普通端点 → 触发二次确认，返回 confirmToken
- 带 Idempotency-Key 调用 AI 入口 `/maintenance/ai/submit-request` → **直接成功**，无需二次确认

**经验：**
1. 所有写操作必须带 `Idempotency-Key: op-$(date +%s)-$RANDOM`
2. **报修走 AI 安全入口** `POST /maintenance/ai/submit-request`，一次完成，不触发二次确认
3. 普通端点需两段式：第一次拿 confirmToken，第二次带 `X-Risk-Confirm-Token` 重放
