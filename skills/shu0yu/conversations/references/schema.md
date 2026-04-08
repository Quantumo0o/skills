# Conversations DB Schema

**路径**: `C:\Users\YU\.openclaw\workspace\conversations.db`

## chunks 表（对话记录）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | TEXT | 主键，UUID |
| session_key | TEXT | session 标识，格式：`agent:main:session:{uuid}` |
| turn_id | TEXT | 同 session 同 turn 归组 |
| seq | INTEGER | 同 session 内顺序 |
| role | TEXT | `user` 或 `assistant` |
| content | TEXT | 消息纯文本 |
| kind | TEXT | 默认 `paragraph` |
| summary | TEXT | 摘要 |
| owner | TEXT | 默认 `agent:main` |
| created_at | INTEGER | 毫秒时间戳 |
| updated_at | INTEGER | 毫秒时间戳 |
| content_hash | TEXT | 内容 MD5，用于去重 |
| dedup_status | TEXT | 去重状态 |

## embeddings 表（向量索引）

| 字段 | 类型 | 说明 |
|------|------|------|
| chunk_id | TEXT | 外键，关联 chunks.id |
| vector | BLOB | 向量数据 |
| dimensions | INTEGER | 向量维度 |
| updated_at | INTEGER | 更新时间 |

## 常用查询

```sql
-- 按时间范围查
SELECT * FROM chunks WHERE created_at > 1775433600000 AND created_at < 1775520000000;

-- 关键词搜索
SELECT * FROM chunks WHERE content LIKE '%关键词%' ORDER BY created_at DESC LIMIT 20;

-- 某 session 的所有消息
SELECT * FROM chunks WHERE session_key = 'agent:main:session:xxx' ORDER BY seq;

-- 统计
SELECT COUNT(*), role FROM chunks GROUP BY role;
```
