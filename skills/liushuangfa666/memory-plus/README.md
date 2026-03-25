# 🧠 Memory Workflow 记忆工作流

> 虾宝智能记忆工作流 —— 开箱即用，数据与代码分离，支持轻量降级。

## ✨ 特性

- **无外部数据库依赖** —— 文件系统存储，更新 skill 不丢数据
- **两阶段混合检索** —— 向量 + BM25 + RRF + Rerank 精排
- **Query Expansion** —— HyDE 假设文档 + Query Rewriting 多查询变体
- **自动降级** —— Ollama / Rerank / MiniMax 任意不可用时，自动降级到可用模式
- **后台自动存储** —— Daemon 线程每 10 分钟自动检查并存储，无需 cron
- **长对话分块** —— 自动分块存储（重叠 50 tokens），避免截断

## 📦 安装

```bash
# 轻量模式（只需 Python）
pip install scikit-learn

# 完整模式（推荐）
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

## 🚀 快速开始

```bash
# 检查状态
python3 memory_ops.py check

# 存储记忆
python3 memory_ops.py store --content "今天和用户讨论了龙虾平台 v2.0" --topic "lobster-platform"

# 搜索记忆
python3 memory_ops.py search --query "龙虾平台" --limit 5
```

## 🔧 配置

```bash
export OLLAMA_URL=http://localhost:11434
export RERANK_SERVICE_URL=http://localhost:18778
export MEMORY_WORKFLOW_DATA=~/.openclaw/memory-workflow-data
```

详细配置见 [SKILL.md](SKILL.md)。

## 📁 数据目录

```
~/.openclaw/memory-workflow-data/
├── memories/            # 记忆文件（JSON）
├── memory_state.json    # 状态
└── hot_sessions.json   # 热 session
```

> 更新 skill 时此目录不会被覆盖。

## ⚠️ 局限性

| 限制 | 说明 |
|------|------|
| 向量检索依赖 Ollama | 不用 Ollama 则降级为 BM25 |
| 单节点文件存储 | 不支持多实例共享 |
| RAGAs 评估脚本 | `ragas_eval.py` 仍在开发中 |

## 📄 文档

- [SKILL.md](SKILL.md) —— 完整文档（推荐）
- [CHANGELOG.md](CHANGELOG.md) —— 更新日志
