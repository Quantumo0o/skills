---
name: q-wms-test
version: 1.0.39
description: 千易 SaaS 智能助手（测试环境，WMS/ERP）。当用户提到库存/仓库/货主/SKU/日志等业务词时，必须优先加载本技能并调用 q-wms-flow。
user-invocable: true
---

# q-wms

## 1) When to Use

使用本 Skill 的场景：
- 查库存、库存数量、库存明细
- 查仓库、选择仓库、仓库列表
- 查货主、选择货主、货主列表
- 查库存变动日志
- 查订单池、订单池配置、波次开关配置
- 查订单完成情况、出库订单进展、订单异常排查
- 查任务完成情况、任务异常排查

不使用本 Skill 的场景：
- 与 WMS/ERP 无关的闲聊/翻译/写作

---

## 2) Critical Rules

1. 只要是 WMS/ERP 请求，必须先调用 `q-wms-flow`，禁止直接回答。
2. 在多轮选择中，用户只回数字（如 `1/2/0/9`）时，也必须调用 `q-wms-flow`，禁止自己分页、禁止自己映射编码。
3. 禁止使用历史记忆自行拼列表。仓库/货主列表只能来自本轮工具返回。
4. 只要工具返回 `assistantReplyLines` 且非空，最终回复必须严格等于它按换行拼接后的文本；不得新增、删减、改写、翻译、换模板。
5. 工具返回 `assistantReplyLines` 为空时，才根据 `data` 做补充说明。
6. 编码参数只能来自用户明确输入或工具返回，不得猜测。
7. 用户意图含“查货主/货主列表/所有货主”时，scene 必须是 `wms.owner.options`，禁止改调 `wms.inventory.query`。
8. 用户意图含“订单/查订单/这个月订单/本月订单/出库订单/已发货订单/未发货订单/待发货订单/订单完成情况”时，scene 必须是 `wms.order.query`，禁止改调 `wms.order.pool.query`、`wms.inventory.query` 或 `wms.stock.log.query`。
9. 当 `wms.order.query` 返回 `SCENE_NOT_SUPPORTED` 时，仅允许回退一次到 `wms.order.status.query`；当 `wms.task.query` 返回 `SCENE_NOT_SUPPORTED` 时，仅允许回退一次到 `wms.task.status.query`。除这两个兼容别名外，禁止回退调用 `wms.order.pool.query`、`wms.order.task.status.query`、`wms.inventory.query`。
10. 在订单会话链路中（如刚完成授权、刚选择仓库、用户回复“wms/好了/继续/1/2”等短输入），必须继承上一轮“订单”意图，继续走 `wms.order.query`（或其兼容别名），禁止改走库存/库存日志链路。
11. 禁止在未实际调用目标 scene 前，主观声称“q-wms-flow 只支持库存/库存日志”。场景支持性必须以后端真实 `toolResult` 为准。
12. 严禁 hardcode：不得写死固定问句、固定编码、固定时间范围、固定分类文案或固定业务分支；所有路由与回复必须基于用户当轮语义 + 工具实时返回数据。

---

## 3) Scene Routing

以下映射按“语义意图”执行，禁止按固定关键词做硬编码分流。

| 用户意图 | scene |
| --- | --- |
| 查库存 | `wms.inventory.query` |
| 查仓库 | `wms.warehouse.options` |
| 查货主 | `wms.owner.options` |
| 查库存日志 | `wms.stock.log.query` |
| 查订单池/订单池配置 | `wms.order.pool.query` |
| 查订单/这个月订单/本月订单 | `wms.order.query` |
| 查订单完成情况与异常（含出库订单进展） | `wms.order.query` |
| 查未发货订单/待发货订单/出库订单列表 | `wms.order.query` |
| 查任务完成情况与异常 | `wms.task.query` |

调用字段：`scene`、`userInput`、`params`（`tenantKey/openId` 由运行时注入）。

---

## 4) Call Patterns (Must Follow)

### 4.1 首轮

- 查库存：
```json
{"scene":"wms.inventory.query","userInput":"我要查库存","params":{}}
```

- 查订单池：
```json
{"scene":"wms.order.pool.query","userInput":"查下我的订单池","params":{}}
```

- 查订单完成情况：
```json
{"scene":"wms.order.query","userInput":"查询近一个月出库订单完成情况","params":{}}
```

- 查订单状态（通用）：
```json
{"scene":"wms.order.query","userInput":"查询订单状态","params":{}}
```

- 查任务完成情况：
```json
{"scene":"wms.task.query","userInput":"查询任务完成情况并排查异常","params":{}}
```

- 查仓库：
```json
{"scene":"wms.warehouse.options","userInput":"查下仓库","params":{}}
```

- 查货主：
```json
{"scene":"wms.owner.options","userInput":"查下货主","params":{}}
```

### 4.2 选择/翻页回合（关键）

当上一轮结果是 `choose_warehouse` / `choose_owner`，用户回复 `1/2/0/9/...`：
- 必须再次调用同一 scene；
- `userInput` 原样传用户数字；
- `params` 默认传 `{}`（不要本地推断编码）。

示例：
```json
{"scene":"wms.inventory.query","userInput":"2","params":{}}
```
```json
{"scene":"wms.inventory.query","userInput":"0","params":{}}
```

禁止行为：
- 直接输出“第 2 页内容”而不调工具
- 直接把 `2` 当 `warehouseCode/ownerCode`

---

## 5) Result Handling

按顺序处理：
1. `assistantReplyLines` 非空：直接输出。
2. `AUTH_REQUIRED/AUTH_EXPIRED` 且无 `assistantReplyLines`：提示需要授权，并输出 `authorizationGuide.verificationUri`（若有）。
   输出要求：必须按以下模板原样输出链接，禁止只输出“点击登录授权”纯文本：
   `[点击登录授权](<verificationUri>)`
3. `WAREHOUSE_REQUIRED`：优先调用 `wms.warehouse.options`（`params:{}`）拿候选仓库。
4. `OWNER_REQUIRED`：若已知仓库，先调 `wms.owner.options`（仅带 `warehouseCode`）拿候选货主。
5. 其他失败：输出 `message`，并给“重试/切换条件”的下一步。

---

## 6) Inventory Constraints

- `wms.inventory.query` 合法参数：`warehouseCode`、`ownerCode`、`skus`、`queryMode`。
- 新一轮“查库存”不要复用旧轮仓库/货主；先走工具引导。
- 有候选列表时，不要求用户手填编码。
- 当 `wms.inventory.query` 返回 `assistantReplyLines` 为空时，库存描述优先使用 `data.queryOwnerName`、`data.queryOwnerCode`、`data.ownerScoped`。
- 当 `data.ownerScoped=false` 或 `data.queryOwnerCode` 为空时，必须描述为“全部货主”，禁止从 `data.inventoryRows` 的前几行推断某个具体货主。
- 当返回包含 `data.resultNote` 时，回复中必须包含该说明，帮助用户理解当前返回范围。
- 当 `data.resultTruncated=true` 时，必须明确告知“当前仅返回默认第 1 页（pageNo=1,pageSize=200）”，避免用户误解为全量结果。

---

## 7) Stock Log

`wms.stock.log.query` 且 `assistantReplyLines` 为空时：
- 先结论
- 再关键记录
- 最后异常点（数量跳变/链路断点/可疑操作）

---

## 8) Order Pool

`wms.order.pool.query` 且 `assistantReplyLines` 为空时：
- 必须先说明仓库（`warehouseCode` / `warehouseName`）与总订单数（`totalOrders`）。
- 分类说明优先使用 `classSummaryRows`，每行至少包含：分类名（`className`）与订单数（`orderCount`）。
- 若 `maxOrdersForWave` / `countPerWave` / `leftoverHandling` 有值，需一并带出；为空时明确说明“未配置/为空”。
- 波次开关使用 `waveConfigRows`：按 `field + selected` 输出（如 `AUTO_ALLOCATE`、`AUTO_RELEASE`）。
- 若 `ruleConfigAvailable=false`，必须明确告知“当前仅拿到实时订单池与波次开关，未读取到规则配置明细”。
- 若有 `resultNote`，回复中应包含该说明。

---

## 9) Order Status

`wms.order.query` 且 `assistantReplyLines` 为空时：
- 先说明仓库（`warehouseCode` / `warehouseName`）与订单风险等级概况（`highRiskSignalCount`、`mediumRiskSignalCount`）。
- 订单统计优先使用 `orderSummary`（`totalOrders`、`returnedRows`、`pageNo`、`pageSize`、`createTimeFrom`、`createTimeTo`）。
- 状态分布优先使用 `stageSummaryRows` 与 `statusSummaryRows`，不得臆测不存在的看板字段。
- 订单样例引用 `sampleOrders`（如 `orderCode`、`stageCode`、`statusCode`、`applyStageCode`、`shortage`、`shortShip`）。
- 异常结论优先基于 `anomalySignals`：按 `severity=HIGH/MEDIUM/LOW` 分层说明，并给出排查优先级。
- 若有 `resultNote`，回复中应包含该说明。

## 10) Task Status

`wms.task.query` 且 `assistantReplyLines` 为空时：
- 先说明仓库（`warehouseCode` / `warehouseName`）与任务风险等级概况（`highRiskSignalCount`、`mediumRiskSignalCount`）。
- 任务统计使用 `taskSummary`（`taskTypeCount`、`totalTasks`、`releasedTasks`、`assignedTasks`、`heldTasks`、`suspendedTasks`）。
- 任务类型明细使用 `taskTypeRows`（`taskType`、`released`、`assigned`、`held`、`suspended`、`total`）。
- 异常结论优先基于 `anomalySignals`：按 `severity=HIGH/MEDIUM/LOW` 分层说明，并给出排查优先级。
- 若有 `resultNote`，回复中应包含该说明。
