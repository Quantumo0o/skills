# 迁移指南

## 从现有记忆系统升级

---

## 迁移前准备

### 1. 备份现有数据

```bash
cp -r memory/ memory.backup.$(date +%Y%m%d)
cp MEMORY.md MEMORY.md.backup.$(date +%Y%m%d)
```

### 2. 创建新目录结构

```bash
mkdir -p memory/topics
mkdir -p memory/transcripts/$(date +%Y-%m)
```

### 3. 复制 Skill

```bash
cp -r /Users/ekko/Documents/CODE_SPACE/whyischen/mem-layer ~/.openclaw/skills/
```

---

## 迁移步骤

### 步骤 1：迁移核心 Topic 文件

```bash
# 投资领域
cp memory/investments/*.md memory/topics/

# 项目领域
cp memory/projects/*.md memory/topics/

# 资产领域
cp memory/assets/*.md memory/topics/
```

### 步骤 2：重构 MEMORY.md

手动重写 MEMORY.md 为新格式（或等待 autoDream）：

```markdown
# MEMORY.md - OpenClaw 记忆索引

> 📌 规则：仅指针，≤150 字符/行，≤25KB 总计

---

## 元数据
- version: 2.0
- last_dream: 2026-04-02T23:00:00+08:00
- total_topics: 12

## Topics
| 领域 | 主题 | 路径 | 更新 | 摘要 | 标签 | 重要性 | 热度 |
|------|------|------|------|------|------|--------|------|
| 投资 | 定投策略 | memory/topics/investment-dca.md | 2026-04-02 | 基金定投 | ETF | 0.9 | 🔥 |
```

### 步骤 3：迁移历史到 Transcripts

```bash
# 转换现有 daily/heartbeat 日志为 Transcript 格式
for file in memory/daily/*.md memory/heartbeat/*.md; do
  [ -f "$file" ] && echo "转换：$file"
  # 手动或脚本转换
done
```

### 步骤 4：验证

```bash
# 检查 Index 大小
du -h MEMORY.md

# 检查 Topic 数量
ls memory/topics/ | wc -l

# 测试搜索
grep -r "关键词" memory/topics/
```

### 步骤 5：启用 autoDream

```bash
openclaw cron add "0 23 * * *" "memory-system auto-dream"
```

---

## 迁移后检查清单

- [ ] MEMORY.md 大小 ≤25KB
- [ ] Topic 文件已移动到 `memory/topics/`
- [ ] Transcript 目录已创建
- [ ] autoDream Cron 已配置
- [ ] 搜索正常工作

---

## 回滚方案

如果迁移后发现问题：

```bash
# 删除新目录
rm -rf memory/topics
rm -rf memory/transcripts

# 恢复备份
cp -r memory.backup.20260402/* memory/
cp MEMORY.md.backup.20260402 MEMORY.md
```

---

*最后更新：2026-04-03*
