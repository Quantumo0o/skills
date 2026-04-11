---
name: mofang-records
version: 3.1.0
description: 魔方网表记录与 BPM 流程。必须通过 exec 执行本 Skill 提供的 CLI 命令完成操作，禁止自行编写代码或构造 HTTP 请求。Use when 用户提到魔方网表、表单、记录、数据、查询、创建、修改、删除、导入、流程、待办、审批、BPM、转办、加签等。
author: magicscape
homepage: https://github.com/magicscape/magicflu-skills
---

# 魔方网表记录管理

## 首要规则（必须遵守）

**本 Skill 提供 CLI 命令行工具。必须通过 exec 执行命令完成操作。**

**禁止**：自行编写 Python/Node.js 等代码、自行 import handler 模块、用 fetch/requests 直接访问魔方 API、构造 HTTP 请求或 URL。所有 API 路径、Token 管理、空间/表单解析、字段映射均已封装在 CLI 内部。

## 调用格式

使用 exec 工具执行以下命令：

```
node <skill-dir>/cli.mjs <command> '<json-params>'
```

- `<skill-dir>`：本 Skill 安装目录，通常为 `~/.openclaw/skills/mofang-records`
- `<command>`：命令名称（见下方命令列表）
- `<json-params>`：JSON 格式的参数字符串，无参数时传 `'{}'`
- 输出：JSON 格式，包含 `success`（布尔）和 `message`（说明），成功时包含 `data`

### exec 工具调用示范

以下是通过 exec 工具调用的完整格式，**直接复制并替换参数即可**：

列出空间：

```
exec({"command": "cd ~/.openclaw/skills/mofang-records && node cli.mjs mofang_list_spaces '{}'"})
```

查询记录：

```
exec({"command": "cd ~/.openclaw/skills/mofang-records && node cli.mjs mofang_query_records '{\"formHint\":\"采购申请\",\"spaceHint\":\"AI演示空间\"}'"})
```

创建记录：

```
exec({"command": "cd ~/.openclaw/skills/mofang-records && node cli.mjs mofang_create_record '{\"formHint\":\"客户信息\",\"data\":{\"客户名称\":\"北京公司\",\"联系电话\":\"13800138000\"}}'"})
```

修改记录：

```
exec({"command": "cd ~/.openclaw/skills/mofang-records && node cli.mjs mofang_update_record '{\"formHint\":\"采购申请\",\"recordId\":\"7\",\"data\":{\"申请数量\":150}}'"})
```

删除记录：

```
exec({"command": "cd ~/.openclaw/skills/mofang-records && node cli.mjs mofang_delete_record '{\"formHint\":\"采购申请\",\"recordId\":\"7\"}'"})
```

测试连接：

```
exec({"command": "cd ~/.openclaw/skills/mofang-records && node cli.mjs mofang_test_connection '{}'"})
```

**注意**：JSON 参数中的双引号需要转义为 `\"`，因为外层已被 exec 的 command 字符串包裹。

### 环境变量优先级

CLI 读取 **`MOFANG_BASE_URL` / `MOFANG_USERNAME` / `MOFANG_PASSWORD` 优先于** `BASE_URL` / `USERNAME` / `PASSWORD`。若安装目录下 **`.env` 已写入 `MOFANG_USERNAME`**，临时改用另一账号时，请 **`export MOFANG_USERNAME=...`**（或改 `.env`），**仅设置 `USERNAME` 不会覆盖** `.env` 里的 `MOFANG_USERNAME`。

## 何时使用

当用户提到以下内容时激活此 Skill：
- 提到"魔方网表"、"表单"、"记录"、"数据"等关键词
- 要求查询、搜索、查找、浏览表单中的数据
- 要求创建、添加、新增记录
- 要求修改、更新、编辑记录
- 要求删除、移除记录
- 要求查看某个空间里有哪些表单
- 上传文件并要求将内容录入到表单中
- 流程待办、审批、转办、驳回、终止、加签、取回等 BPM 相关操作

**典型句式**：「采购申请里有哪些记录」「把客户信息表里序号 3 的电话改成 13800138000」「我有哪些待办流程」「把请假单记录 7 的当前任务提交掉」

## 核心特性

### 自动解析

所有命令接受**中文名称**作为输入：
- `formHint`：表单名称，如「采购申请」「客户信息」
- `spaceHint`：空间名称（可选），如「AI演示空间」

CLI 内部自动完成：Token 获取与刷新、空间/表单名称解析（支持缓存、模糊匹配、多空间搜索）、字段定义获取。

### 字段名自动映射

`data`（创建/修改记录）和 `filters`（查询条件）中的字段名**同时支持中文名称(label)和英文标识(name)**，工具自动识别转换。

- `{"客户名称": "北京公司"}` — 自动转为 `{"kehumingcheng": "北京公司"}`
- `{"kehumingcheng": "北京公司"}` — 直接使用

## 重要操作规范

### 1. 创建/修改记录前必须获取字段定义

**在执行 `mofang_create_record` 或 `mofang_update_record` 之前，必须先调用 `mofang_get_field_definitions` 获取目标表单的真实字段结构。**

原因：不同表单的字段英文名（name）由表单设计者定义，**不能靠猜测或推断**。例如「申请单号」在 A 表可能是 `shenqingdanhao`，在 B 表可能是 `suoshushenqingdan`。本文档中的示例仅用于演示格式，**不代表任何具体表单的真实字段**。

正确流程：
1. 先 `mofang_get_field_definitions` 获取字段列表
2. 确认每个字段的 **`name`（英文标识）**、**`type`（类型）**、**`required`（是否必填）**
3. 用正确的字段名和格式构造 `data`

### 2. 始终传 spaceHint 以避免空间歧义

当同名表单存在于多个空间时，CLI 的缓存和模糊匹配可能解析到错误的空间。**建议始终在 `formHint` 同时传入 `spaceHint`**，明确指定目标空间。

```
{"formHint":"采购申请","spaceHint":"AI对外演示"}
```

如遇到查询结果为空或数据不对，可尝试：
- 检查是否传了正确的 `spaceHint`
- 清除缓存：`rm -rf ~/.mofang-skills/`，然后重新查询

### 3. 嵌入字段（embed）的关联格式

主表中的嵌入字段（embed 类型）不能直接在主表创建时写入子记录。正确操作：
1. 先在**子表**（嵌入字段关联的表单）创建记录
2. 然后用 `mofang_update_record` 更新**主表**的嵌入字段，格式为：

```json
{"嵌入字段名": {"entry": [{"id": "子记录ID1"}, {"id": "子记录ID2"}]}}
```

### 4. 常见错误与排查

| 错误信息 | 常见原因 | 解决方式 |
|----------|----------|----------|
| `NumberFormatException: For input string: ""` | 数字字段被传了空字符串，或字段名映射错误导致数据落到了错误字段 | 用 `mofang_get_field_definitions` 检查字段类型，确认 name 正确 |
| `字段 "xxx" 未找到匹配的字段定义，已忽略` | data 里用了不存在的字段名 | 检查字段英文 name 是否拼写正确 |
| 查询结果为空（但数据确实存在） | 缓存解析到了错误的空间 | 传入 `spaceHint` 明确指定空间，或清除缓存 |
| 创建成功但字段值为空 | 字段名写错（如 `shenqingdanhao` 应为 `suoshushenqingdan`），服务端忽略了未识别的字段 | 先调 `mofang_get_field_definitions` 确认真实 name |

## 命令列表（18 个）

### 网表记录

| 命令 | 用途 | 关键参数 |
|------|------|---------|
| `mofang_test_connection` | 测试连接和配置 | 无 |
| `mofang_list_spaces` | 列出所有空间 | 无 |
| `mofang_list_forms` | 列出空间下表单 | spaceHint? |
| `mofang_get_field_definitions` | 获取字段定义 | formHint, spaceHint? |
| `mofang_query_records` | 查询记录 | formHint, spaceHint?, filters?, page?, pageSize? |
| `mofang_create_record` | 创建记录 | formHint, spaceHint?, data |
| `mofang_update_record` | 修改记录 | formHint, spaceHint?, recordId, data |
| `mofang_delete_record` | 删除记录 | formHint, spaceHint?, recordId |

### BPM / 流程（Activiti）

说明：引擎里 **`assignee` 等为登录名**（如 `aitools`），与 JWT 里的 **`username` 一致**；不要用 JWT 里的 UUID **`id`** 去筛待办。若环境 **`POST /query/tasks` 返回 415**，`mofang_bpm_query_tasks` 会自动改用 **`GET /runtime/tasks`**（返回中会带 `queryFallbackUsed`）。

| 命令 | 用途 | 关键参数 |
|------|------|---------|
| `mofang_bpm_list_tasks` | 待处理任务列表（我的待办 / 组待办 / 委托） | mode?, page?, pageSize?, processDefinitionKey?, descriptionLike? |
| `mofang_bpm_query_tasks` | 按表单+记录等条件查询任务（定位） | formHint?, spaceHint?, recordId?, processDefinitionName?, taskName?, page? |
| `mofang_bpm_get_task` | 单任务详情 + 变量 + recordId/formId/spaceId 提示 | taskId |
| `mofang_bpm_complete_task` | 提交/完成任务 | taskId；可选 simple+variables |
| `mofang_bpm_delegate_task` | 转办 | taskId, assignee |
| `mofang_bpm_claim_task` | 认领组任务 | taskId, assignee? |
| `mofang_bpm_resolve_task` | 委托归还（resolve） | taskId |
| `mofang_bpm_jump_task` | 终止(abort) / 驳回(rollback) / 取回(recovery) | taskId, kind, jumpTargetId?, targetTaskName? |
| `mofang_bpm_open_transaction` | 开启事务（如并行加签 COSIGN） | taskAction, processName?, taskName?, … |
| `mofang_bpm_close_transaction` | 关闭事务 | transactionId |

## 操作方式

**直接执行一条 CLI 命令即可完成操作**，无需多步编排。

### 查询记录

```
node <skill-dir>/cli.mjs mofang_query_records '{"formHint":"采购申请","filters":[{"fieldName":"状态","operator":"eq","value":"审批中"}]}'
```

返回结果包含 `fieldLabels` 映射（name→label），用于展示时显示中文字段名。以表格形式展示，字段名用中文 label。

### 创建记录

```
node <skill-dir>/cli.mjs mofang_create_record '{"formHint":"客户信息","data":{"客户名称":"北京公司","联系电话":"13800138000"}}'
```

**创建前必须先调用 `mofang_get_field_definitions` 确认字段定义，再向用户确认数据内容。**

### 修改记录

先调用 `mofang_get_field_definitions` 确认字段定义，再查询定位记录，展示原值→新值并确认，然后执行：

```
node <skill-dir>/cli.mjs mofang_update_record '{"formHint":"采购申请","recordId":"7","data":{"申请数量":150}}'
```

**必须**使用 `mofang_update_record` 直接修改，**严禁**用创建新记录代替修改。

### 删除记录

先查询定位，展示信息并确认，然后执行：

```
node <skill-dir>/cli.mjs mofang_delete_record '{"formHint":"采购申请","recordId":"7"}'
```

### BPM：待办与定位

列出我的待办：

```
node <skill-dir>/cli.mjs mofang_bpm_list_tasks '{"mode":"assignee","page":1,"pageSize":20}'
```

按表单名称 + 记录号定位任务（得到 `taskId`）：

```
node <skill-dir>/cli.mjs mofang_bpm_query_tasks '{"formHint":"请假申请","recordId":"37","spaceHint":"演示空间"}'
```

查看任务上下文（变量中的 recordId / formId / spaceId）：

```
node <skill-dir>/cli.mjs mofang_bpm_get_task '{"taskId":"2183137"}'
```

### BPM：办理（须先向用户确认）

- **提交通过**：`mofang_bpm_complete_task`（默认会按服务端习惯同步任务变量后 complete；若环境限制可改用 `simple:true` 并自行传 `variables`）。
- **转办**：`mofang_bpm_delegate_task`，`assignee` 为对方**账号 id**。
- **组待办先认领**：`mofang_bpm_claim_task`。
- **委托归还**：`mofang_bpm_resolve_task`。
- **终止流程**：`mofang_bpm_jump_task`，`kind` 为 `abort`（可自动解析结束节点，亦可靠 `jumpTargetId`）。
- **驳回到某用户任务**：`kind` 为 `rollback`，提供 `targetTaskName`（流程图上的任务名称）或 `jumpTargetId`（sid-xxx）。
- **取回**：`kind` 为 `recovery`，必须提供 `jumpTargetId`。

### BPM：加签（并行加签等）

1. `mofang_bpm_open_transaction`：`taskAction` 填 `COSIGN`，并传入 `processName`、`taskName` 等与界面一致的信息；保存返回的 `transactionId`。
2. 按业务修改记录：使用 `mofang_update_record` 等（含公式 `check/before` 由服务端处理）。
3. `mofang_bpm_close_transaction`：传入同一 `transactionId`。

若环境与 JWT 不完全兼容，可能需浏览器会话；此时以实际网关策略为准。

### 文件导入记录

用户上传文件要求录入时：**必须先执行 `mofang_get_field_definitions`** 了解字段结构，从文件提取数据并做映射（下拉用选项 ID、日期 YYYY-MM-DD、引用用 `{"id":"记录id"}`、数字字段不能传空字符串）。**展示映射预览并确认**，确认后逐条执行 `mofang_create_record`，最后报告成功/失败数。

## 参数详情

### filters 参数

**参数名必须是 `filters`（数组）**，不是魔方界面/部分接口文档里的单数 `filter`，也不要使用 `filterType`、`value2`、`filterGroup` 等前端结构；否则旧版 CLI 会**静默忽略条件**（查到的可能是未筛选的第一页，易被误判为「没有数据」）。新版会尝试把常见的 `filter.items`（如 `BETWEEN` + `value`/`value2`）转成内部条件，但仍应优先手写 `filters`。

**日期区间（整月示例）**：`operator` 为 `between`，**起止写在同一字段 `value` 内、英文逗号分隔**，例如 2026 年 3 月：`"value":"2026-03-01,2026-03-31"` 或按服务端习惯用次日零点：`"value":"2026-03-01,2026-04-01"`（以 `mofang_get_field_definitions` 中该日期字段类型为准）。

```
{"formHint":"外包工作量填报","spaceHint":"网表业务管理系统","filters":[{"fieldName":"填报日期","operator":"between","value":"2026-03-01,2026-03-31"}],"pageSize":50}
```

过滤条件数组，每个元素：

| 字段 | 类型 | 说明 |
|------|------|------|
| fieldName | string | 字段名（中文label或英文name均可） |
| operator | string | 操作符：eq, noteq, like, like_and, like_or, lt, gt, lte, gte, between, isnull, isnotnull, in, notin, checkbox_in, checkbox_eq, tree, rddl |
| value | string | 过滤值。文本传原始文本；数字填数字；日期填YYYY-MM-DD；**between：两个边界用英文逗号放在一个 value 里**；isnull/isnotnull填"-1" |
| not | boolean | 是否取反，默认false |
| concat | string | 与前一条件连接方式："&&"(AND) 或 "\|\|"(OR)，默认"&&" |

### orderBy 参数

| 字段 | 类型 | 说明 |
|------|------|------|
| fieldName | string | 排序字段名（中文或英文均可） |
| direction | string | "asc" 或 "desc" |

## 字段值规则

- **文本/网址**: 填字符串
- **数字**: 填数字（**不能传空字符串 `""`，否则服务端报 NumberFormatException**）
- **日期**: 格式 `YYYY-MM-DD`
- **日期时间**: 格式 `YYYY-MM-DD HH:mm:ss`
- **下拉列表**: 填选项 ID（如 `"1"`），不能填文本内容
- **复选框**: 多个选项 ID 逗号分隔（如 `"1,2"`）
- **主引用字段**: 填 `{"id":"记录序号"}`
- **嵌入字段(embed)**: 不可在主表直接赋值；先在子表创建记录，再更新主表：`{"entry":[{"id":"子记录ID"}]}`

## 数据展示规则

- 查询结果以表格形式展示
- 字段名使用中文 label（通过返回的 `fieldLabels` 映射）
- 下拉列表字段展示 content 文本而非 value 编号
- 引用字段展示关联的内容而非 ID

## 安全规则

- 写操作（创建/修改/删除）必须先向用户确认
- BPM 写操作（`mofang_bpm_complete_task`、`mofang_bpm_delegate_task`、`mofang_bpm_claim_task`、`mofang_bpm_resolve_task`、`mofang_bpm_jump_task`、事务开闭）必须先向用户确认并说明后果（通过、转办、终止、驳回等）
- 不得在对话中暴露 Token 值
- 删除操作需特别警告用户此操作不可逆
