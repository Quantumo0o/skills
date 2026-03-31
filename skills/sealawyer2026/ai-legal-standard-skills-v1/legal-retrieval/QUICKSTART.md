# 法律检索技能 - 快速入门

## 5分钟快速开始

### 1. 测试基本检索

```bash
cd /workspace/projects/agents/legal-ai-team/legal-ceo/workspace

python skills/legal-retrieval/legal-retrieval.py \
  --query "合同违约责任" \
  --limit 5 \
  --output human
```

### 2. 查看JSON格式输出

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "债权转让" \
  --sources regulations \
  --limit 3 \
  --output json
```

### 3. 批量检索

```python
from skills.legal_retrieval import LegalRetrieval

retriever = LegalRetrieval()

queries = [
    "合同违约责任",
    "债权转让条件",
    "侵权责任构成"
]

for result in retriever.batch_search(queries, limit=3):
    print(f"查询: {result.query}")
    print(f"找到: {result.total} 条结果")
    print()
```

---

## 常用查询示例

### 合同相关

```bash
# 合同违约责任
python skills/legal-retrieval/legal-retrieval.py --query "合同违约责任" --limit 10

# 合同解除条件
python skills/legal-retrieval/legal-retrieval.py --query "合同解除条件" --limit 10

# 合同赔偿限额
python skills/legal-retrieval/legal-retrieval.py --query "赔偿限额条款" --limit 10
```

### 债权相关

```bash
# 债权转让
python skills/legal-retrieval/legal-retrieval.py --query "债权转让" --limit 10

# 债权人权利
python skills/legal-retrieval/legal-retrieval.py --query "债权人权利" --limit 10
```

### 民法典相关

```bash
# 民法典合同编
python skills/legal-retrieval/legal-retrieval.py --query "民法典 合同" --limit 10

# 民法典侵权责任
python skills/legal-retrieval/legal-retrieval.py --query "民法典 侵权责任" --limit 10
```

---

## 按数据源检索

### 只检索法规库

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任" \
  --sources regulations \
  --limit 5
```

### 只检索案例库

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "房屋买卖合同纠纷" \
  --sources cases \
  --limit 5
```

### 只检索合同库

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "买卖合同模板" \
  --sources contracts \
  --limit 5
```

### 检索多个数据源

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "合同纠纷" \
  --sources regulations cases reference \
  --limit 10
```

---

## 集成到智能体工作流

### 在Python脚本中调用

```python
#!/usr/bin/env python3
"""
合同审查助手 - 使用法律检索技能
"""

from skills.legal_retrieval import LegalRetrieval

def review_contract_clause(clause_text: str):
    """审查合同条款"""
    retriever = LegalRetrieval()

    # 提取关键问题
    query = extract_key_issue(clause_text)

    # 检索相关法规和案例
    results = retriever.search(
        query=query,
        sources=["regulations", "cases"],
        limit=5
    )

    # 输出审查意见
    print(f"📋 条款审查: {clause_text[:50]}...")
    print(f"🔍 检索查询: {query}")
    print(f"📊 找到 {results.total} 条相关文档\n")

    for ev in results.evidence[:3]:
        print(f"• {ev.title} [相关性: {ev.score:.2f}]")
        print(f"  {ev.excerpt}\n")

def extract_key_issue(clause_text: str) -> str:
    """提取条款中的关键法律问题"""
    # 简化版，实际应该使用NLP提取
    keywords = ["赔偿", "责任", "违约", "解除", "终止", "责任限制", "赔偿限额"]
    for kw in keywords:
        if kw in clause_text:
            return f"合同 {kw}"

    return "合同条款"

if __name__ == "__main__":
    # 示例
    clause = "在任何情况下，乙方的赔偿责任不得超过合同总金额的10%。"
    review_contract_clause(clause)
```

### 在智能体提示词中使用

创建一个合同审查智能体的提示词：

```markdown
# 合同审查智能体

你是一名专业的合同审查律师。在审查合同时，你必须：

1. 识别关键条款和潜在风险
2. 使用法律检索技能查找相关法规和案例
3. 基于检索结果提供专业意见

## 工具使用

当需要检索相关法律依据时，调用法律检索技能：

```
请检索关于"{关键问题}"的法规和案例
```

## 审查流程

1. 阅读合同条款
2. 识别关键法律问题
3. 使用法律检索技能查找依据
4. 分析检索结果
5. 提供修改建议
```

---

## 输出格式选择

### JSON格式（适合程序处理）

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任" \
  --output json
```

输出：
```json
{
  "query": "违约责任",
  "timestamp": "2026-03-07T10:30:00Z",
  "sources": ["all"],
  "mode": "full",
  "summary": "找到 5 条相关文档",
  "evidence": [...],
  "total": 5,
  "retrieved": 5
}
```

### 人性化格式（适合阅读）

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任" \
  --output human
```

输出：
```
📋 检索结果

查询: 违约责任
来源: all
找到: 5 条相关文档
显示: 前 5 条

---

🥇 第1条 [相关性: 0.95]

**民法典第577条（违约责任）**
...
```

---

## 高级用法

### 1. 指定知识库路径

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "合同违约" \
  --kb-path /custom/path/to/knowledge-base
```

### 2. 清空缓存

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --clear-cache
```

### 3. 在Python中使用自定义逻辑

```python
from skills.legal_retrieval import LegalRetrieval

retriever = LegalRetrieval()

# 检索并过滤结果
result = retriever.search(
    query="合同违约责任",
    sources=["regulations", "cases"],
    limit=20
)

# 只保留高相关性结果
high_relevance = [ev for ev in result.evidence if ev.score > 0.8]

# 按来源分组
by_source = {}
for ev in result.evidence:
    if ev.source_type not in by_source:
        by_source[ev.source_type] = []
    by_source[ev.source_type].append(ev)

# 输出分组结果
for source_type, items in by_source.items():
    print(f"\n📂 {source_type}:")
    for item in items:
        print(f"  • {item.title} [{item.score:.2f}]")
```

---

## 常见问题

### Q: 为什么检索结果为空？

A: 可能的原因：
1. 查询关键词太具体 → 尝试使用更通用的关键词
2. 知识库中没有相关文档 → 需要添加相关文档
3. 数据源过滤太严格 → 移除 `--sources` 参数，搜索所有来源

### Q: 如何提高检索准确性？

A:
1. 使用更精确的关键词
2. 指定相关的数据源（如 `--sources regulations`）
3. 增加返回结果数量（`--limit 20`）

### Q: 性能如何？

A:
- 首次检索: 2-5秒（取决于知识库大小）
- 缓存命中: <0.1秒
- 支持批量检索，提高效率

### Q: 可以检索PDF/Word文档吗？

A: 当前版本只支持Markdown和纯文本文件。要支持PDF/Word，需要：
1. 提前转换为Markdown格式
2. 或扩展 `KnowledgeBaseAdapter` 类

---

## 下一步

- 📖 阅读完整文档: [SKILL.md](./SKILL.md)
- 🔧 配置检索选项: 编辑配置文件
- 🚀 集成到工作流: 创建自定义脚本
- 💡 提供反馈: 通过飞书联系

---

**最后更新**: 2026-03-07
**版本**: v1.0.0
