# 蜀宁 OA 工时系统 - API 参考

## 系统信息

- **baseURL**: 从对话获取后保存（存于 memory/sn-work-record-credentials.md）
- **API 路径**: /sn/timeEntry/*

## 工时相关 API

### 获取工时详情

```
GET /sn/timeEntry/get?id=<id>
```

返回: `{ id, jobDesc, state }`

### 撤回工时（审批中→草稿）

```
POST /sn/timeEntry/cancelApply
Content-Type: application/json
{"id": "<工时ID>"}
```

返回 `{ isOk: true, data: { state: "10" } }` 表示成功，state "10" = 草稿

### 修改工时描述

```
POST /sn/timeEntry/update
Content-Type: application/json
{"id": "<工时ID>", "jobDesc": "新的描述文字"}
```

返回 `{ isOk: true }` 表示成功

**注意**: 修改描述后，后端会自动重新提交，状态从"草稿"(10) 变回"审批中"(20)

## 状态值说明

- `"10"` = 草稿
- `"20"` = 审批中

## 完整工作流程

1. **获取工时 ID** - 在列表页或日历视图找到目标工时记录
2. **撤回** - `POST /sn/timeEntry/cancelApply` → state 20→10
3. **修改描述** - `POST /sn/timeEntry/update` → 自动重新提交 → state 10→20
4. **验证** - `GET /sn/timeEntry/get?id=<id>` 确认描述和状态

## 典型成功响应

撤回:

```json
{"code": "200", "msg": "操作成功", "data": {"id": "...", "state": "10"}}
```

修改:

```json
{"code": "200", "msg": "操作成功", "data": {"id": "...", "jobDesc": "..."}}
```

查询:

```json
{"id": "...", "jobDesc": "...", "state": "20"}
```
