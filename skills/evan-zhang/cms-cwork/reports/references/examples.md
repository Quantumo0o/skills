# Reports — 使用示例

## 场景一：发送汇报（标准流程）

```typescript
// 1. 生成草稿（需要 LLM）
const draft = await draftGen({ rawContent: '完成登录功能开发', reportType: '日报' }, { llmClient });

// 2. 校验接收人
const validate = await reportValidateReceivers({ names: ['张三', '李四'] });
const confirmedIds = validate.data.confirmedEmployees.map(e => e.empId);

// 3. 用户确认后提交
await reportSubmit({
  main: draft.data.title,
  contentHtml: draft.data.contentHtml,
  reportLevelList: [{ level: 1, type: 'read', nodeName: '接收人', levelUserList: [{ empId: confirmedIds[0] }] }],
});
```

## 场景二：一站式发送带附件汇报

```typescript
await reportSubmitWithAttachments({
  main: '本周工作汇报',
  contentHtml: '<p>详见附件</p>',
  filePaths: ['/path/文档.pdf'],
  fileNames: ['文档.pdf'],
});
```

## 场景三：回复汇报

```typescript
await reportReply({
  reportRecordId: '1234567890',
  contentHtml: '<p>已收到</p>',
  addEmpIdList: ['empId_被@的人'],
});
```

## 场景四：查询未读 + 标记已读

```typescript
const unread = await unreadReportList({ pageSize: 20, pageIndex: 1 });
await reportReadMark({ reportId: unread.data.list[0].id });
```

## 场景五：AI 问答（SSE 流式）

```typescript
const chat = await aiReportChat({
  reportIdList: ['id1', 'id2'],
  userContent: '这几条汇报的关键风险点是什么？',
});
// chat.data.stream 是 SSE 流，需消费读取
```

## 附件说明

- 建议上限：单次 ≤ 10 个附件
- 上传失败：自动重试 3 次（间隔 1s/2s/3s）
- 路径要求：filePaths 必须为本地绝对路径
- filePaths 和 fileNames 数量必须一致
- 任意文件上传失败则整个提交中止
