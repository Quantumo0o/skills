---
name: siyuan-api
description: Local SiYuan API integration for notebook/document/block/asset operations and SQL search. Uses only local HTTP endpoints and environment-based token auth.
homepage: https://github.com/siyuan-note/siyuan
metadata:
  openclaw:
    primaryEnv: SIYUAN_API_TOKEN
    requires:
      env:
        - SIYUAN_API_TOKEN
        - SIYUAN_API_URL
---

# SiYuan Skill

本技能用于调用本地运行的 SiYuan HTTP API，支持笔记本、文档、块、资源、SQL 查询等常见操作。
它只描述调用规范和示例，不包含可执行安装脚本或第三方依赖。

## Security Scope

- Only call local SiYuan endpoint (`127.0.0.1`, `localhost`, or user-provided local URL).
- Do not send requests to third-party internet endpoints.
- Never hardcode or print `SIYUAN_API_TOKEN` in logs.
- This skill has read/write authority over your SiYuan notes. Use only in trusted local environments.

## Configuration

Configuration can be provided via environment variables in your shell, for example:

```bash
export SIYUAN_API_TOKEN=your_token_here
export SIYUAN_API_URL=http://127.0.0.1:6806
```

- `SIYUAN_API_TOKEN` (required): from SiYuan `Settings > About`.
- `SIYUAN_API_URL` (optional): defaults to `http://127.0.0.1:6806`.

## Typical Use Cases

- Create, rename, and remove notebooks
- Create documents from Markdown
- Insert, append, update, move, and delete blocks
- Upload assets
- Query notes by SQL
- Export documents as Markdown
- Read/write workspace files through SiYuan file APIs

## API References

- [references/api-zh.md](references/api-zh.md) (Chinese)
- [references/api.md](references/api.md) (English)

## Common Examples

### List Notebooks
```javascript
const SIYUAN_API_TOKEN = process.env.SIYUAN_API_TOKEN;
const SIYUAN_API_URL = process.env.SIYUAN_API_URL || 'http://127.0.0.1:6806';

fetch(`${SIYUAN_API_URL}/api/notebook/lsNotebooks`, {
  method: 'POST',
  headers: {
    'Authorization': 'token ' + SIYUAN_API_TOKEN,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({})
})
```

### Create Document with Markdown
```javascript
const SIYUAN_API_TOKEN = process.env.SIYUAN_API_TOKEN;
const SIYUAN_API_URL = process.env.SIYUAN_API_URL || 'http://127.0.0.1:6806';

fetch(`${SIYUAN_API_URL}/api/filetree/createDocWithMd`, {
  method: 'POST',
  headers: {
    'Authorization': 'token ' + SIYUAN_API_TOKEN,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    notebook: '笔记本ID',
    path: '/文档路径',
    markdown: '# 文档标题\n\n正文内容...'
  })
})
```

### Append Block
```javascript
const SIYUAN_API_TOKEN = process.env.SIYUAN_API_TOKEN;
const SIYUAN_API_URL = process.env.SIYUAN_API_URL || 'http://127.0.0.1:6806';

fetch(`${SIYUAN_API_URL}/api/block/appendBlock`, {
  method: 'POST',
  headers: {
    'Authorization': 'token ' + SIYUAN_API_TOKEN,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    parentID: '父块ID',
    dataType: 'markdown',
    data: '追加的内容'
  })
})
```

### SQL Query
```javascript
const SIYUAN_API_TOKEN = process.env.SIYUAN_API_TOKEN;
const SIYUAN_API_URL = process.env.SIYUAN_API_URL || 'http://127.0.0.1:6806';

fetch(`${SIYUAN_API_URL}/api/query/sql`, {
  method: 'POST',
  headers: {
    'Authorization': 'token ' + SIYUAN_API_TOKEN,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    stmt: 'SELECT id, content FROM blocks WHERE content LIKE "%关键词%" LIMIT 10'
  })
})
```

## Notes

- Repeated `createDocWithMd` on the same path does not overwrite existing documents.
- Custom block attributes must be prefixed with `custom-`.
- All endpoints use `POST` and return `{ code, msg, data }`.
- Header format is `Authorization: token <your-token>` (lowercase `token`).
