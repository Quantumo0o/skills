# API Reference — CWork Skill Package

Base URL: `https://sg-al-cwork-web.mediportal.com.cn/open-api`
Auth Header: `appKey: {your-key}`

## Reports

- `emp-search` — GET `/cwork-user/searchEmpByName`
- `file-upload` — POST `/cwork-file/uploadWholeFile`
- `report-submit` — POST `/work-report/report/record/submit`
- `report-reply` — POST `/work-report/report/record/reply`
- `inbox-query` — POST `/work-report/report/record/inbox`
- `outbox-query` — POST `/work-report/report/record/outbox`
- `report-get-by-id` — GET `/work-report/report/info`
- `report-read-mark` — POST `/work-report/open-platform/report/read`
- `unread-report-list` — POST `/work-report/reportInfoOpenQuery/unreadList`
- `ai-report-chat` — POST `/work-report/open-platform/report/aiSseQaV2`
- `template-list` — POST `/work-report/template/listTemplates`
- `template-info-batch` — POST `/work-report/template/listByIds`

## Drafts

- `draft-save` — POST `/work-report/draftBox/saveOrUpdate`
- `draft-list` — POST `/work-report/draftBox/listByPage`
- `draft-detail` — GET `/work-report/draftBox/detail/{reportRecordId}`
- `draft-delete` — POST `/work-report/draftBox/delete/{id}`
- `draft-submit` — POST `/work-report/draftBox/submit/{id}`
- `draft-batch-delete` — POST `/work-report/draftBox/batchDelete`

## Tasks & Todos

- `task-list-query` — POST `/work-report/report/plan/searchPage`
- `task-chain-get` — GET `/work-report/report/plan/getSimplePlanAndReportInfo`
- `task-create` — POST `/work-report/open-platform/report/plan/create`
- `todo-list-query` — POST `/work-report/reportInfoOpenQuery/todoList`
- `todo-complete` — POST `/work-report/open-platform/todo/completeTodo`
- `my-feedback-list` — POST `/work-report/reportInfoOpenQuery/todoList`

## Contacts

- `contact-group-list` — POST `/cwork-user/group/queryTargetUserGroups`
- `contact-group-create` — POST `/cwork-user/group/saveOrUpdatePersonalGroup`
- `contact-group-members` — POST `/cwork-user/group/manageGroupMembers`

## Key Types

`endTime` / `deadline` — millisecond timestamp only. Use `new Date('2026-04-14').getTime()`.

`reportRecordType` — 1=交流 2=指引 3=签批 4=AI汇报 5=工作汇报

`reportLevelList[].type` — `"read"` 传阅 / `"suggest"` 建议 / `"decide"` 决策
