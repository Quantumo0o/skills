---
name: memory-workflow
version: 2.1.1
description: |
  虾宝智能记忆工作流。开箱即用，数据目录与代码分离，支持轻量降级。

  特性：
  - 文件系统存储，无外部数据库依赖
  - Ollama 向量嵌入（可选，降级为 BM25）
  - bge-reranker-v2-m3 重排（可选）
  - HyDE + Query Rewriting（可选）
  - 后台线程自动存储（每10分钟）
  - 两阶段混合检索（向量 + BM25 + RRF + rerank）
---

# 🧠 Memory Workflow Skill

## 核心特性

### 先进性

| 特性 | 说明 |
|------|------|
| **两阶段混合检索** | Stage 1: 向量 + BM25 → RRF粗排 → rerank精排 → 取前1/3；Stage 2: 二次RRF融合，结果更精准 |
| **Query Expansion** | 支持 HyDE（假设文档生成）+ Query Rewriting（多查询变体），提升召回 |
| **分块存储** | 长对话自动分块（重叠50 tokens），避免截断丢失信息 |
| **自动降级** | Ollama/Rerank/MiniMax 任意一个不可用时，自动降级到可用模式，不中断服务 |
| **数据与代码分离** | 记忆文件独立存储在 `~/.openclaw/memory-workflow-data/`，更新 skill 不丢数据 |
| **后台自动存储** | Daemon 线程每10分钟自动检查并存储，无需外部 cron |

### 局限性

| 限制 | 说明 | 规避方式 |
|------|------|---------|
| **向量检索依赖 Ollama** | 轻量模式（BM25-only）精度低于向量检索 | 建议部署 Ollama + bge-m3 |
| **单节点文件存储** | 不支持多实例共享记忆 | 适合单用户本地部署 |
| **无增量更新** | 新对话全量追加，不支持对已有记忆的修改 | 可手动删除 `memories/` 下 JSON 文件 |
| **无访问控制** | 任何能读文件的人都能看记忆 | 依赖系统文件权限 |
| **RAG 评估脚本开发中** | `ragas_eval.py` 仍在开发中，暂不可用 | 预计后续版本提供 |

### RAG 评估（RAGAs）

> ⚠️ `ragas_eval.py` 评估脚本仍在开发中，暂不可用。

RAGAs（RAG Assessment）是记忆工作流的评估模块，计划用于量化检索质量和生成质量。功能上线后会支持：
- Context Precision / Context Recall
- Answer Faithfulness
- Answer Relevancy

---

## 架构概览

```
用户对话
    ↓
自动存储（Daemon 线程，每10分钟）
    ↓
记忆写入：memories/*.json  +  向量（可选 Milvus）
    ↓
搜索请求 → BM25 + 向量混合检索
         → HyDE/Rewriting 扩展（如有）
         → 两阶段 RRF + Rerank 精排
         → 返回结果
```

---

## 安装步骤

### 1. 轻量模式（无外部依赖）

```bash
# 只需 Python
pip install scikit-learn

# 安装 skill
claw use memory-workflow
```

### 2. 完整模式（推荐）

```bash
# Ollama + bge-m3（必须）
curl -fsSL https://ollama.com/install.sh | sh
ollama pull bge-m3:latest
ollama pull qwen3.5:latest

# Rerank 服务（推荐）
docker run -d -p 18778:8000 \
  --gpus all \
  -e MODEL_NAME=BAAI/bge-reranker-v2-m3 \
  ghcr.io/chgaowei/rerank_openai:latest

# 安装 skill
claw use memory-workflow
```

### 3. 配置环境变量

```bash
export OLLAMA_URL=http://localhost:11434
export RERANK_SERVICE_URL=http://localhost:18778   # 推荐
export MEMORY_WORKFLOW_DATA=~/.openclaw/memory-workflow-data
# MiniMax API（可选，也可只用 Ollama qwen3.5）
export MINIMAX_API_KEY=your_key
```

---

## 数据目录

```
~/.openclaw/memory-workflow-data/
├── memories/               # 记忆文件（JSON，一记忆一文件）
├── memory_state.json       # 状态（上次存储时间等）
└── hot_sessions.json      # 热 session 追踪
```

> 更新或重新安装 skill 时，此目录**不会被覆盖**，用户数据完全保留。

---

## CLI 用法

```bash
# 检查状态
python3 memory_ops.py check

# 存储记忆
python3 memory_ops.py store --content "对话内容" --topic "话题"

# 搜索
python3 memory_ops.py search --query "关键词" --limit 5

# 热 session
python3 memory_ops.py get_hot
```

---

## 与 OpenClaw Agent 集成

```markdown
## 每次消息时

1. 检查记忆状态
   Exec: python3 ~/.openclaw/skills/memory-workflow/memory_ops.py check

2. idle >= 10 分钟则存储
   Exec: python3 ~/.openclaw/skills/memory-workflow/memory_ops.py store \
     --content "【对话摘要】" --topic "conversation"

3. 搜索相关记忆
   Exec: python3 ~/.openclaw/skills/memory-workflow/memory_ops.py search \
     --query "【问题关键词】" --limit 3
```

---

## 搜索模式与降级

| Ollama | Rerank | 搜索模式 | 说明 |
|--------|--------|---------|------|
| ✅ | ✅ | two_stage_rerank | 最高精度 |
| ✅ | ❌ | two_stage_rerank | RRF 融合（无精排）|
| ❌ | - | bm25_only | BM25 纯关键词 |

---

## 环境变量

| 变量 | 默认值 | 必需 |
|------|--------|------|
| `OLLAMA_URL` | http://localhost:11434 | 完整功能必需 |
| `OLLAMA_MODEL` | bge-m3:latest | 向量模型 |
| `RERANK_SERVICE_URL` | http://localhost:18778 | 推荐 |
| `MINIMAX_API_KEY` | （空） | 可选 |
| `MILVUS_URI` | （空） | 可选 |
| `MEMORY_WORKFLOW_DATA` | ~/.openclaw/memory-workflow-data | 可选 |

---

## 故障排除

### Ollama 不可用
```
⚠️ Ollama 不可用，记忆搜索降级为轻量模式（BM25）
```
→ 不影响存储，检索降级为 BM25。安装 Ollama 后自动恢复。

### Rerank 服务未启动
→ 精度下降，不报错。安装 rerank 服务后自动启用。

### 记忆没有自动存储
→ 手动 `check` 查看 idle 时间；确认后台线程未中断。
