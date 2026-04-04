---
name: sn-work-record
description: 蜀宁 OA 工时管理（需提供：系统地址、账号、密码）。当用户提到工时、撤回、修改工时描述、或提到蜀宁科技时触发。用于：查询工时状态、撤回审批中的工时、修改工时描述后自动重新提交。
---

# 蜀宁 OA 工时管理

## 凭据要求

**首次使用**需提供以下信息（仅本次，之后存到本地）：

- **系统地址**：OA 登录页 URL（如 http://117.172.29.11:18089/login）
- **账号**：工时系统登录账号
- **密码**：登录密码

**安全建议**：建议使用**副账号**而非主账号，避免个人密码泄露。

## 存储方式

凭据保存到 `memory/sn-work-record-credentials.md`。文件由 OpenClaw  workspace 管理，仅本地访问，不随 skill 分发。

## 状态值

- `"10"` = 草稿
- `"20"` = 审批中

## 快速操作

### 查询工时状态

```
GET /sn/timeEntry/get?id=<工时ID>
```

### 撤回（审批中→草稿）

```
POST /sn/timeEntry/cancelApply {"id": "<工时ID>"}
```

### 修改描述（自动重新提交）

```
POST /sn/timeEntry/update {"id": "<工时ID>", "jobDesc": "新描述"}
```

**注意**：修改描述后状态自动变回"审批中"(20)，无需手动再提交。

## 完整流程

1. 确认凭据已保存（首次需提供）
2. 获取工时 ID（列表页或日历视图）
3. `cancelApply` 撤回
4. `update` 修改描述 → 自动重新提交
5. `get` 验证结果

## API 详情

See [api.md](references/api.md)
