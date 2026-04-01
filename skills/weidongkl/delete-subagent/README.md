# delete-subagent 技能

OpenClaw 子 agent 会话清理工具 - 安全、可靠、支持备份和归档。

## 快速开始

```bash
# 查看所有子 agent
python ~/.openclaw/skills/delete-subagent/scripts/delete-subagent.py --list

# 清理所有已完成的子 agent
python ~/.openclaw/skills/delete-subagent/scripts/delete-subagent.py

# 预览模式（先看看会删除什么）
python ~/.openclaw/skills/delete-subagent/scripts/delete-subagent.py --dry-run
```

## 完整文档

详见 `SKILL.md`

## 技能位置

```
~/.openclaw/skills/delete-subagent/  ← 公共技能目录（所有 agent 可用）
```

## 备份位置

每个 agent 的备份存储在其各自的 sessions 目录：

```
~/.openclaw/agents/{agent-name}/sessions/backups/
~/.openclaw/agents/{agent-name}/sessions/archive/
```
