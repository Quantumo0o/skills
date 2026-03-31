# 法律检索技能 (Legal Retrieval Skill)

## 概述

智能法律检索技能，支持多数据源搜索、混合排名算法、带引用的证据包输出。

**版本**: 1.0.0
**创建日期**: 2026-03-07
**基于**: PossibLaw possiblaw-legal 设计理念

---

## 功能特性

### 🎯 核心功能

1. **多数据源搜索**
   - 知识库搜索（案例、法规、合同、文书）
   - 本地文档索引
   - 可扩展的外部API（如北大法宝、万方）

2. **智能排名**
   - 混合评分算法（语义 + 关键词 + 来源优先级）
   - 自适应权重调整
   - 相关性排序

3. **证据包输出**
   - 结构化证据列表
   - 完整引用来源
   - 上下文摘要
   - 提示词就绪格式

4. **降级模式**
   - 网络失败时使用本地知识库
   - 保证检索可用性
   - 透明的降级状态通知

---

## 支持的数据源

| 数据源 | 类型 | 优先级 | 状态 |
|--------|------|--------|------|
| 知识库-法规库 | 本地 | 0.95 | ✅ 已实现 |
| 知识库-案例库 | 本地 | 0.95 | ✅ 已实现 |
| 知识库-合同库 | 本地 | 0.95 | ✅ 已实现 |
| 知识库-文书库 | 本地 | 0.95 | ✅ 已实现 |
| 知识库-参考库 | 本地 | 0.90 | ✅ 已实现 |
| 北大法宝 API | 外部 | 0.85 | ⚠️ 待实现 |
| 万方数据 API | 外部 | 0.85 | ⚠️ 待实现 |
| 中国裁判文书网 | 外部 | 0.85 | ⚠️ 待实现 |

---

## 使用方法

### 命令行调用

```bash
python /workspace/projects/agents/legal-ai-team/legal-ceo/workspace/skills/legal-retrieval/legal-retrieval.py \
  --query "合同违约责任" \
  --sources all \
  --limit 10 \
  --output json
```

### Python API 调用

```python
from skills.legal_retrieval import LegalRetrieval

# 初始化检索器
retriever = LegalRetrieval()

# 执行检索
results = retriever.search(
    query="合同违约责任",
    sources=["regulations", "cases", "contracts"],
    limit=10
)

# 输出结果
print(results.summary)
for evidence in results.evidence:
    print(f"[{evidence.rank}] {evidence.title}")
    print(f"来源: {evidence.source_url}")
    print(f"相关性: {evidence.score:.2f}")
    print(f"摘要: {evidence.excerpt}")
    print()
```

### OpenClaw 智能体调用

智能体可以通过以下方式调用：

```
@阿拉丁 使用法律检索技能搜索"合同违约责任"
```

或通过 sessions_send：

```python
sessions_send(
    sessionKey="agent:knowledge-management:main",
    message="使用法律检索技能搜索'合同违约责任'，限制10条结果"
)
```

---

## 输出格式

### JSON 格式

```json
{
  "query": "合同违约责任",
  "timestamp": "2026-03-07T10:30:00Z",
  "sources": ["regulations", "cases", "contracts"],
  "mode": "full",
  "summary": "找到 15 条相关文档，按相关性排序",
  "evidence": [
    {
      "rank": 1,
      "title": "民法典第577条（违约责任）",
      "source_type": "regulations",
      "source_url": "/knowledge-base/02-法规库/01-法律法规/民法典/民法典第577条.md",
      "score": 0.95,
      "excerpt": "当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。",
      "keywords": ["违约", "责任", "民法典"],
      "tags": ["民法典", "合同法", "违约责任"]
    }
  ],
  "total": 15,
  "retrieved": 10
}
```

### 人性化格式

```
📋 检索结果

查询: 合同违约责任
来源: 法规库, 案例库, 合同库
找到: 15 条相关文档
显示: 前 10 条

---

🥇 第1条 [相关性: 0.95]

**民法典第577条（违约责任）**
📂 法规库 → 民法典
🔗 /knowledge-base/02-法规库/01-法律法规/民法典/民法典第577条.md

📝 摘要:
当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。

🏷️ 标签: 民法典, 合同法, 违约责任
🔑 关键词: 违约, 责任, 民法典

---

... (更多结果)
```

---

## 排名算法

### 混合评分公式

```python
final_score = (
    0.55 × semantic_score +      # 语义相似度
    0.30 × keyword_score +        # 关键词匹配
    0.15 × source_priority       # 来源优先级
)
```

### 评分组件

| 组件 | 权重 | 说明 |
|------|------|------|
| semantic_score | 55% | 基于向量嵌入的语义相似度 |
| keyword_score | 30% | 查询关键词在文档中的匹配度 |
| source_priority | 15% | 数据源的优先级权重 |

### 来源优先级

| 数据源 | 优先级 | 说明 |
|--------|--------|------|
| 知识库-法规库 | 0.95 | 权威性最高 |
| 知识库-案例库 | 0.95 | 实际判例参考 |
| 知识库-合同库 | 0.95 | 真实合同样本 |
| 知识库-文书库 | 0.90 | 标准文书格式 |
| 知识库-参考库 | 0.90 | 实务经验参考 |
| 外部API | 0.85 | 需要网络访问 |

---

## 配置选项

### 环境变量

```bash
# 检索配置
RETRIEVAL_MAX_EVIDENCE=10        # 最大返回证据数量
RETRIEVAL_MIN_SCORE=0.3          # 最低相关性分数
RETRIEVAL_CHUNK_SIZE=500         # 文档分块大小（字符）
RETRIEVAL_CHUNK_OVERLAP=120      # 分块重叠大小（字符）

# 外部API配置（可选）
NPM_API_KEY=your_api_key         # 北大法宝API密钥
WANFANG_API_KEY=your_api_key    # 万方数据API密钥
COURT_API_KEY=your_api_key      # 裁判文书网API密钥

# 向量嵌入配置
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536
```

### 配置文件

创建 `config.json`:

```json
{
  "retrieval": {
    "max_evidence": 10,
    "min_score": 0.3,
    "chunk_size": 500,
    "chunk_overlap": 120
  },
  "sources": {
    "knowledge_base": {
      "enabled": true,
      "path": "/workspace/projects/agents/legal-ai-team/knowledge-base"
    },
    "npm": {
      "enabled": false,
      "api_key": ""
    }
  },
  "ranking": {
    "weights": {
      "semantic": 0.55,
      "keyword": 0.30,
      "source_priority": 0.15
    }
  }
}
```

---

## 高级功能

### 1. 自定义查询过滤器

```python
results = retriever.search(
    query="合同违约责任",
    filters={
        "source_type": ["regulations"],
        "date_range": ("2020-01-01", "2026-03-07"),
        "tags": ["民法典"]
    }
)
```

### 2. 批量检索

```python
queries = [
    "合同违约责任",
    "债权转让条件",
    "侵权责任构成"
]

for result in retriever.batch_search(queries, limit=5):
    print(f"查询: {result.query}")
    print(f"找到: {result.total} 条结果")
```

### 3. 增量索引更新

```python
# 更新知识库索引
retriever.update_index(
    paths=["/path/to/new/documents"],
    incremental=True
)
```

---

## 性能优化

### 索引缓存

首次检索后，索引会被缓存到内存，后续检索速度大幅提升。

### 并行检索

多个数据源的检索并行执行，减少总体延迟。

### 结果缓存

相同查询的结果会被缓存（TTL: 1小时），避免重复计算。

---

## 错误处理

### 降级模式

当外部API不可用时，自动切换到本地知识库：

```python
{
  "mode": "degraded",
  "message": "外部API不可用，使用本地知识库",
  "sources_used": ["knowledge_base"],
  "evidence": [...]
}
```

### 空结果处理

当没有找到相关结果时：

```python
{
  "mode": "no_results",
  "message": "未找到相关文档，建议扩大搜索范围或使用更通用的关键词",
  "suggestions": [
    "尝试使用更通用的关键词",
    "扩大搜索的数据源范围",
    "检查查询的拼写和用词"
  ]
}
```

---

## 安全考虑

### 数据安全

- 所有检索操作在本地进行
- 敏感文档不会被索引（可通过配置排除）
- 支持访问日志记录

### API安全

- 外部API密钥通过环境变量配置
- 请求速率限制
- 请求超时保护

---

## 使用场景

### 1. 合同审查

```python
# 检索特定条款的法规依据
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
# 综合检索法规、案例、学术观点
results = retriever.search(
    query="民法典 债权转让 通知义务",
    sources=["all"],
    limit=15
)
```

---

## 扩展开发

### 添加新数据源

1. 创建适配器类继承 `BaseAdapter`:

```python
class CustomAdapter(BaseAdapter):
    def search(self, query: str) -> List[Evidence]:
        # 实现检索逻辑
        pass
```

2. 注册适配器:

```python
retriever.register_adapter("custom", CustomAdapter())
```

### 自定义排名算法

```python
class CustomRanker(BaseRanker):
    def rank(self, evidence: List[Evidence]) -> List[Evidence]:
        # 实现自定义排名逻辑
        pass

retriever.set_ranker(CustomRanker())
```

---

## 维护指南

### 更新索引

```bash
# 重建完整索引
python skills/legal-retrieval/legal-retrieval.py --rebuild-index

# 增量更新索引
python skills/legal-retrieval/legal-retrieval.py --update-index
```

### 查看统计信息

```bash
python skills/legal-retrieval/legal-retrieval.py --stats
```

### 清理缓存

```bash
python skills/legal-retrieval/legal-retrieval.py --clear-cache
```

---

## 版本历史

### v1.0.0 (2026-03-07)
- 初始版本发布
- 支持知识库检索
- 实现混合排名算法
- 支持证据包输出
- 降级模式支持

---

## 作者

**开发者**: 阿拉丁（法律AI团队 - 知识库管理）
**设计参考**: PossibLaw possiblaw-legal
**许可**: MIT License

---

## 相关文档

- [法律检索实现文档](./IMPLEMENTATION.md)
- [检索算法详解](./ALGORITHM.md)
- [API参考](./API_REFERENCE.md)
- [故障排查](./TROUBLESHOOTING.md)

---

## 反馈与支持

如有问题或建议，请联系：
- 飞书: ou_5701bdf1ba73fc12133c04858da7af5c
- 智能体: 知识库管理
