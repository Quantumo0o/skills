# Tasks — 使用示例

## 场景一：查询任务

```typescript
// 查所有进行中任务
const all = await taskListQuery({ pageSize: 30, pageIndex: 1, status: 1 });

// 查分配给我的任务
const mine = await taskMyAssigned({ userId: 'myEmpId', status: 1 });

// 查我创建的任务（可按下属筛选）
const created = await taskMyCreated({ pageSize: 30, assigneeIds: ['empId_下属'] });
```

## 场景二：创建任务（直接传姓名）

```typescript
const result = await taskCreate({
  title: '完成登录功能',
  content: '实现用户登录模块',
  target: '登录功能上线',
  deadline: new Date('2026-04-14 23:59:59').getTime(),  // 必须是毫秒时间戳
  assignee: '张三',           // 姓名或 empId 均可，内部自动解析
  reportEmpIdList: ['李四'],  // 同上
});
```

## 场景三：查看任务链路（任务 + 汇报）

```typescript
const chain = await taskChainGet({ taskId: '123456789' });
// chain.data.plan — 任务详情
// chain.data.reports — 关联汇报列表
```

## 场景四：管理者仪表盘

```typescript
const dashboard = await taskManagerDashboard({
  subordinateIds: ['empId1', 'empId2'],
  taskStatus: 1,   // 进行中
  reportStatus: 3, // 逾期优先
});
// dashboard.data.summary.total / overdue / pending
// dashboard.data.byPerson — 按人详情
```

## 场景五：识别卡点任务

```typescript
const blockers = await taskBlockerIdentify({ pageSize: 50, status: 1 });
// blockers.data.list — 卡点/逾期任务列表
```
