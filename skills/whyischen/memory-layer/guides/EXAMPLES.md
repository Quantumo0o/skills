# 使用示例

## 核心场景

---

## 示例 1：写入流程（监控 → 记忆）

```bash
# 监控完成后，写入 3 层：

# 1. Transcript（自动追加）
memory/transcripts/2026-04/2026-04-02.log

# 2. Topic（更新动态状态）
memory/topics/investment-strategy.md

# 3. Index（更新指针）
MEMORY.md
```

---

## 示例 2：查询流程

```bash
# 1. 搜索 Index（始终加载）
grep "关键词" MEMORY.md

# 2. 加载 Topic（按需）
cat memory/topics/investment-strategy.md

# 3. 搜索 Transcripts（可选，仅 grep）
grep -r "关键词" memory/transcripts/
```

---

*理解模式，自行实现。*

*最后更新：2026-04-03 | Memory Layer*
