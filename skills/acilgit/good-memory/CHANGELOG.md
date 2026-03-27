# Good-Memory Changelog

## v1.1.0 (2026-03-27)

### 新增
- **UUID 前缀比对**：tracker 新增 `active_uuid` 字段，verify 时优先比对 UUID 前缀（UUID 全局唯一，更可靠）
- **verify 输出新增 `last_history` 字段**：当检测到重置时，直接输出最近一次被重置的 session 文件路径

### 比对逻辑（双重验证）
1. **UUID 前缀比对**（主要）— UUID 全局唯一，前缀改变 = 一定是新 session
2. **Birth Time 比对**（辅助）— UUID 相同时，用 birth time 辅助确认

### 工作流程
```
每次收到消息：
  maintenance.sh update <agent> <chat_id>

Session 重置后恢复：
  1. maintenance.sh verify <agent> <chat_id>
  2. 如果 RESET_DETECTED，从 last_history 获取文件路径
  3. recovery.sh read-file <last_history> --lines 100
```

---

## v1.01 (2026-03-27)

### 核心改进
- **Tracker 文件 + Birth Time 验证机制**：解决系统自动重置后的上下文恢复问题
- **active_created_at 字段**：记录当前 session 文件的创建时间，用于验证 session 是否被重置
- **history[].created_at**：记录历史 session 文件的创建时间

### 文件变更
- `SKILL.md`：更新文档，添加 Tracker 结构说明和验证流程
- `recovery.sh`：新增 `read-file` 命令，支持读取指定文件路径
- `maintenance.sh`：新增 `verify` 命令，基于 birth time 验证 session 状态

### 工作流程
```
每次收到消息：
  maintenance.sh update <agent> <chat_id>

Session 重置后恢复：
  1. maintenance.sh verify <agent> <chat_id>
  2. 如果 RESET_DETECTED，从输出获取 last_session_file
  3. recovery.sh read-file <file> --lines 100
```

---

## v1.00 (更早版本)
- 基于 grep 扫描 session 文件前 20 行匹配 chat_id
- 使用 sessions_list 获取 transcriptPath
- scan/read/list 命令直接操作 session 文件
