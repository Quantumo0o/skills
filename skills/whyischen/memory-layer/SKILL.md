---
name: memory-layer
description: 基于 Claude Code 记忆哲学的三层记忆管理系统。当需要以下操作时使用：(1) 设计 Index/Topic/Transcript 记忆架构，(2) 迁移现有记忆文件到分层结构，(3) 配置 autoDream 自动整理，(4) 优化上下文窗口使用率 70%+，(5) 实现基于重要性评分的记忆排序和检索。
---

# Memory Layer - 三层记忆系统

> 🧠 基于 Claude Code 记忆哲学，为 OpenClaw 设计

---

## 何时使用

**Agent 应在以下场景触发本 Skill**：

| 场景 | 说明 |
|------|------|
| 设计记忆架构 | 新建 Index/Topic/Transcript 三层结构 |
| 迁移现有记忆 | 将 memory/investments/等迁移到 memory/topics/ |
| 配置 autoDream | 设置每日自动记忆整理 |
| 优化上下文 | 减少上下文加载量 70%+ |
| 重要性排序 | 实现基于重要性的记忆检索 |

---

## 核心架构

```
┌─────────────────────────────────────────┐
│   MEMORY.md (Index 层)                   │
│   - 仅指针，≤25KB，≤150 字符/行            │
│   - 始终加载到上下文                      │
└───────────────┬─────────────────────────┘
                │ 按需加载 (2-5 个文件)
                ▼
┌─────────────────────────────────────────┐
│   memory/topics/*.md (Topic 层)          │
│   - 结构化知识，≤50KB/文件               │
│   - 仅在相关时加载                        │
└───────────────┬─────────────────────────┘
                │ 永不加载，仅 grep
                ▼
┌─────────────────────────────────────────┐
│   memory/transcripts/*.log (Transcript 层)│
│   - 原始日志，仅追加                      │
│   - >90 天自动归档                        │
└─────────────────────────────────────────┘
```

---

## 核心原则

| 原则 | Agent 行为规范 |
|------|---------------|
| **带宽感知** | 上下文稀缺，分层加载 |
| **写纪律** | 先写 Topic，再更新 Index（防止膨胀） |
| **验证优先** | 记忆是提示，不是真相（实时数据从 API 获取） |
| **职责分离** | Index/Topic/Transcript 职责明确 |
| **自动整理** | autoDream 每日夜间去重/合并 |

---

## 写操作规范

**Agent 写入记忆时必须遵循的顺序**：

```
1. 写入 Transcript（完整日志）
   ↓
2. 提取关键事实 → 更新 Topic
   ↓
3. 压缩摘要 → 更新 Index
```

**禁止行为**：
- ❌ 直接更新 Index 而不写 Topic
- ❌ 在 Topic 中存储可实时获取的数据（价格、汇率等）
- ❌ 在 Transcript 中存储长期知识

---

## 读操作规范

**Agent 读取记忆时的加载策略**：

| 层 | 加载条件 | 加载方式 |
|----|----------|----------|
| Index | 始终 | 启动时加载 MEMORY.md |
| Topic | 相关查询时 | 按需加载 2-5 个文件 |
| Transcript | 深度搜索时 | grep，不加载到上下文 |

---

## 重要性评分

**Agent 应为每条记忆计算重要性分数 (0.0-1.0)**：

```
importance = domainBase + accessBonus + userBonus
```

| 领域 | 基础权重 |
|------|----------|
| 投资 | 0.8 |
| 项目 | 0.7 |
| 资产 | 0.7 |
| 知识 | 0.5 |
| 健康 | 0.6 |

---

## autoDream 规范

**触发条件**：每日 23:00 Asia/Shanghai

**Agent 应执行的操作**：
1. 读取当日 Transcripts
2. 提取关键事实
3. 去重（相似度 >0.95 视为重复）
4. 合并相似 Topic（相似度 0.8-0.95）
5. 检测并标记矛盾（不自动解决）
6. 重新计算重要性
7. 更新 Topic 文件
8. 压缩 Index
9. 归档 >90 天的 Transcripts

---

## 配置

**位置**：`~/.openclaw/config/memory-config.json`

**核心参数**：
```json
{
  "index": { "maxSizeKB": 25, "lruSize": 5 },
  "topic": { "maxSizeKB": 50 },
  "transcript": { "archiveDays": 90 },
  "autoDream": { "schedule": "23:00", "similarityThreshold": 0.8 }
}
```

---

## 文档导航

| 文档 | Agent 何时读取 |
|------|---------------|
| [references/architecture.md](references/architecture.md) | 完整架构设计 |
| [references/index-spec.md](references/index-spec.md) | Index 层格式规范 |
| [references/topic-spec.md](references/topic-spec.md) | Topic 层格式规范 |
| [references/transcript-spec.md](references/transcript-spec.md) | Transcript 层格式规范 |
| [references/autodream.md](references/autodream.md) | autoDream 算法详情 |
| [references/config.md](references/config.md) | 完整配置参数 |

---

## 快速开始

```bash
# 1. 创建目录结构
mkdir -p memory/topics memory/transcripts/$(date +%Y-%m)

# 2. 复制默认配置
cp config/default.json ~/.openclaw/config/memory-config.json

# 3. 启用 autoDream
openclaw cron add "0 23 * * *" "memory-system auto-dream"
```

---

*版本：2.0 | 最后更新：2026-04-03 | 代号：Memory Layer*
