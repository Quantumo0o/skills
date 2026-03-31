# Tasks — 类型说明

## status — 任务状态

| 值 | 说明 |
|----|------|
| 0 | 已关闭 |
| 1 | 进行中 |
| 2 | 未启动 |

## reportStatus — 汇报状态

| 值 | 说明 |
|----|------|
| 0 | 已关闭 |
| 1 | 待汇报 |
| 2 | 已汇报 |
| 3 | 逾期 |

## deadline / endTime — 时间字段

必须是毫秒时间戳，不能是字符串。

```typescript
// ✅ 正确
deadline: new Date('2026-04-14 23:59:59').getTime()  // → 1776182399000

// ❌ 错误
deadline: '2026-04-14 23:59:59'
```

## 人员字段 — 支持姓名或 empId

`assignee`、`reportEmpIdList`、`assistEmpIdList`、`supervisorEmpIdList`、`copyEmpIdList`、`observerEmpIdList` 均支持传姓名，内部自动解析为 empId。
