# 法律检索技能 (Legal Retrieval Skill)

> 基于PossibLaw possiblaw-legal设计理念，为OpenClaw打造的专业法律检索工具

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/legal-ai-team)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

---

## 📖 简介

法律检索技能是一个智能法律文档检索系统，支持多数据源搜索、智能排名算法、带引用的证据包输出。

**核心特性:**

- 🎯 **多数据源搜索** - 知识库 + 外部API
- 🧠 **智能排名** - 语义 + 关键词 + 来源优先级混合算法
- 📋 **证据包输出** - 结构化、带引用的检索结果
- 🛡️ **降级模式** - 网络失败时使用本地知识库
- ⚡ **高性能** - 缓存机制 + 并行检索

---

## 🚀 快速开始

### 安装

无需安装，直接使用：

```bash
cd /workspace/projects/agents/legal-ai-team/legal-ceo/workspace
```

### 基本使用

```bash
# 检索合同违约责任
python skills/legal-retrieval/legal-retrieval.py \
  --query "合同违约责任" \
  --limit 5 \
  --output human
```

### Python API

```python
from skills.legal_retrieval import LegalRetrieval

retriever = LegalRetrieval()
results = retriever.search(query="合同违约责任", limit=10)
```

---

## 📚 文档

| 文档 | 说明 |
|-----|------|
| [SKILL.md](./SKILL.md) | 完整技能文档 |
| [QUICKSTART.md](./QUICKSTART.md) | 5分钟快速入门 |
| [README.md](./README.md) | 本文件 |

---

## 🎯 使用场景

### 1. 合同审查

```python
# 检索赔偿限额条款的相关法规
results = retriever.search(
    query="赔偿限额条款的有效性",
    sources=["regulations", "cases"],
    limit=5
)
```

### 2. 案件研究

```python
# 检索类似案例
results = retriever.search(
    query="房屋买卖合同纠纷 逾期交房",
    sources=["cases", "reference"],
    limit=10
)
```

### 3. 文书起草

```python
# 检索标准文书模板
results = retriever.search(
    query="买卖合同纠纷 起诉状",
    sources=["documents", "reference"],
    limit=3
)
```

### 4. 法律研究

```python
# 综合检索
results = retriever.search(
    query="民法典 债权转让 通知义务",
    sources=["all"],
    limit=15
)
```

---

## 🔧 配置

### 环境变量

```bash
export KNOWLEDGE_BASE_PATH=/path/to/knowledge-base
export RETRIEVAL_MAX_EVIDENCE=10
export RETRIEVAL_MIN_SCORE=0.3
```

### 配置文件

创建 `config.json`:

```json
{
  "retrieval": {
    "max_evidence": 10,
    "min_score": 0.3
  },
  "sources": {
    "knowledge_base": {
      "enabled": true,
      "path": "/path/to/knowledge-base"
    }
  }
}
```

---

## 📊 支持的数据源

| 数据源 | 类型 | 优先级 | 状态 |
|--------|------|--------|------|
| 知识库-法规库 | 本地 | 0.95 | ✅ |
| 知识库-案例库 | 本地 | 0.95 | ✅ |
| 知识库-合同库 | 本地 | 0.95 | ✅ |
| 知识库-文书库 | 本地 | 0.90 | ✅ |
| 知识库-参考库 | 本地 | 0.90 | ✅ |
| 北大法宝 API | 外部 | 0.85 | ⚠️ 待实现 |
| 万方数据 API | 外部 | 0.85 | ⚠️ 待实现 |

---

## 🧠 排名算法

```
final_score = 0.55 × semantic_score + 0.30 × keyword_score + 0.15 × source_priority
```

- **semantic_score** (55%): 基于向量嵌入的语义相似度
- **keyword_score** (30%): 查询关键词匹配度
- **source_priority** (15%): 数据源优先级权重

---

## 💻 命令行接口

### 基本语法

```bash
python skills/legal-retrieval/legal-retrieval.py [QUERY] [OPTIONS]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| `query` | 查询字符串 | 必需 |
| `--sources` | 数据源列表 | all |
| `--limit` | 返回结果数量 | 10 |
| `--output` | 输出格式（json/human） | json |
| `--kb-path` | 知识库路径 | 环境变量 |
| `--clear-cache` | 清空缓存 | false |

### 示例

```bash
# 基本检索
python skills/legal-retrieval/legal-retrieval.py "合同违约责任"

# 指定数据源
python skills/legal-retrieval/legal-retrieval.py \
  "违约责任" \
  --sources regulations cases

# 人性化输出
python skills/legal-retrieval/legal-retrieval.py \
  "违约责任" \
  --output human

# 清空缓存
python skills/legal-retrieval/legal-retrieval.py --clear-cache
```

---

## 🔌 集成到OpenClaw

### 方法1: 通过sessions_send调用

```python
sessions_send(
    sessionKey="agent:knowledge-management:main",
    message="使用法律检索技能搜索'合同违约责任'，限制10条结果"
)
```

### 方法2: 在智能体工作流中使用

智能体提示词示例：

```markdown
你是一名法律研究律师。

当需要检索相关法律依据时：
1. 提取关键法律问题
2. 调用法律检索技能：`python skills/legal-retrieval/legal-retrieval.py --query "关键问题"`
3. 分析检索结果
4. 提供专业意见
```

---

## 📈 性能

| 操作 | 时间 | 说明 |
|-----|------|------|
| 首次检索 | 2-5秒 | 取决于知识库大小 |
| 缓存命中 | <0.1秒 | 相同查询 |
| 批量检索 | 1-2秒/查询 | 并行处理 |

---

## 🛡️ 安全

- ✅ 所有检索在本地进行
- ✅ 敏感文档可通过配置排除
- ✅ 支持访问日志记录
- ✅ API密钥通过环境变量配置

---

## 🤝 贡献

欢迎提交问题和改进建议！

---

## 📄 许可

MIT License

---

## 👥 作者

**开发者**: 阿拉丁（法律AI团队 - 知识库管理）
**设计参考**: PossibLaw possiblaw-legal
**许可**: MIT License

---

## 📞 支持

如有问题或建议，请联系：
- 飞书: ou_5701bdf1ba73fc12133c04858da7af5c
- 智能体: 知识库管理

---

**最后更新**: 2026-03-07
**版本**: v1.0.0
