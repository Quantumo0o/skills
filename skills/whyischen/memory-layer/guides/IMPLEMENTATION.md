# 实现指南

> 💡 本 Skill 是纯文档设计，不包含实现代码。以下是核心操作的实现思路。

---

## 核心操作

### 1. 迁移现有记忆文件

```bash
# 备份
cp -r memory/ memory.backup.$(date +%Y%m%d)

# 创建目录
mkdir -p memory/topics memory/transcripts/$(date +%Y-%m)

# 移动文件
for dir in memory/investments memory/projects memory/assets; do
  [ -d "$dir" ] && mv "$dir"/*.md memory/topics/
done
```

---

### 2. 跨层搜索

```bash
grep -r "关键词" MEMORY.md memory/topics/
```

---

### 3. 结构验证

```bash
[ -f MEMORY.md ] && du -k MEMORY.md
ls memory/topics/*.md | wc -l
```

---

### 4. autoDream 触发

```bash
openclaw cron add "0 23 * * *" "memory-system auto-dream"
```

---

### 5. Transcript 写入

```bash
cat >> memory/transcripts/$(date +%Y-%m)/$(date +%Y-%m-%d).log << EOF
[TRANSCRIPT] $(date -Iseconds)
[TYPE] query
[DATA] 用户查询：金价
EOF
```

---

### 6. Index 更新

手动编辑 `MEMORY.md`（推荐），或用 `sed` 自动更新。

---

### 7. 矛盾检测

```bash
grep -A3 "## 待解决问题" memory/topics/*.md
```

高级检测建议用 Python 解析。

---

## 最佳实践

1. **备份优先**：`cp -r memory/ memory.backup.$(date +%Y%m%d)`
2. **小步验证**：先单文件测试，再批量执行
3. **手动优先**：初期手动编辑，熟练后再自动化

---

## 总结

Memory Layer 是**设计模式**，不是工具包：

1. **分层加载**：Index 永远加载，Topic 按需，Transcript 仅 grep
2. **写纪律**：先写 Topic，再更新 Index
3. **自动化**：夜间整理（autoDream）

理解原理，自行实现。

---

*最后更新：2026-04-03 | Memory Layer*
