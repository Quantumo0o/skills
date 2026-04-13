---
name: clawhub-publish-best-practices
description: ClawHub Skills 发布最佳实践和经验教训
version: 1.0.1
tags: [clawhub, skills, publish, best-practices, guide]
---

# ClawHub Skills 发布最佳实践

**创建时间**: 2026-04-09  
**维护者**: 韩雪原  
**用途**: 记录 ClawHub Skills 发布的正确流程、常见错误和经验教训

---

## ⚠️ 重要规则（血泪教训）

### 1. 只发布名单内的技能

**错误做法** ❌：
```bash
# 盲目执行 sync，会扫描所有本地技能
clawhub sync
```

**正确做法** ✅：
```bash
# 1. 先查看发布名单
cat PUBLISHED_SKILLS_MAINTENANCE.md

# 2. 确认待发布技能
# 3. 检查 slug 可用性
# 4. 只处理名单内的技能
```

**教训**：
- `clawhub sync` 会扫描**所有本地技能**，包括：
  - 本地使用的技能（如 self-improving-agent）
  - slug 被占用的技能（如 mcdonalds、netflix）
  - 测试技能（如 test-slug-check）
- 这会导致尝试发布不应该发布的技能

---

### 2. 不删除本地技能

**错误做法** ❌：
```bash
# 遇到冲突就删除本地文件
rm -rf skills/mcdonalds
rm -rf skills/self-improving-agent  # 大错特错！
```

**正确做法** ✅：
```bash
# 遇到冲突直接跳过，保留本地文件
# 即使是 slug 被占用的技能也保留
```

**教训**：
- **绝对不能删除本地使用的技能**（如 self-improving-agent）
- slug 被占用的技能可以删除（因为无法发布）
- 但要先确认不是本地正在使用的

---

### 3. 遇到 slug 冲突直接跳过

**错误做法** ❌：
```bash
# 尝试用奇怪的名字发布
mcdonalds-conflict-backup  # 没有意义
```

**正确做法** ✅：
```bash
# slug 被占用就直接放弃
# 记录到维护文件中，避免下次再试
```

**已被占用的 slug 示例**：
- mcdonalds → /kongdeyu/mcdonalds
- netflix → /duanc-chao/netflix
- booking → /ivangdavila/booking

---

### 4. 发布后及时更新追踪文件

**错误做法** ❌：
- 发布后不记录技能 ID
- 追踪文件与实际状态不一致
- 不知道哪些技能已经发布过了

**正确做法** ✅：
```markdown
# PUBLISHED_SKILLS_MAINTENANCE.md

| # | 技能名称 | 版本 | 技能 ID | 发布时间 |
|---|----------|------|---------|----------|
| 33 | starbucks | 0.1.2 | k971dyfnnw58b012r0p908g9sh84fnjg | 06:55 |
```

**教训**：
- 每次发布后**立即**更新追踪文件
- 记录技能 ID、版本、发布时间
- 避免重复发布或遗漏

---

## 📋 正确的发布流程

### 步骤 1：查看发布名单

```bash
cat /workspace/projects/workspace/skills/PUBLISHED_SKILLS_MAINTENANCE.md
```

确认：
- 哪些技能已经发布（有技能 ID）
- 哪些技能待发布（标记为待发布）
- 哪些 slug 被占用（放弃）

---

### 步骤 2：检查限流状态

```bash
# 查看当前限流状态
# 规则：5 个新技能/小时
```

- 如果限流中 → 等待刷新
- 如果有名额 → 继续

---

### 步骤 3：准备待发布技能

```bash
# 确认技能目录存在
ls -la /workspace/projects/lisah-workspace/workspace/skills/kfc/
ls -la /workspace/projects/lisah-workspace/workspace/skills/pizza-hut/

# 检查 SKILL.md 格式
head -10 skills/kfc/SKILL.md
```

确保：
- 技能目录存在
- SKILL.md 格式正确（name、version、tags）
- 没有 .clawhub/origin.json（表示未发布过）

---

### 步骤 4：执行发布

**方法 A：使用 sync（会扫描所有技能）**
```bash
cd /workspace/projects/lisah-workspace/workspace
clawhub sync
```

**方法 B：手动发布单个技能（推荐）**
```bash
cd /workspace/projects/lisah-workspace/workspace/skills/kfc
clawhub publish .
```

---

### 步骤 5：记录结果

**成功发布**：
```bash
# 更新追踪文件
# 记录技能 ID、版本、时间
```

**遇到冲突**：
```bash
# 记录到"已被占用的 Slug"列表
# 保留本地文件（如果是本地使用的技能）
# 或删除本地文件（如果确定无法发布）
```

**限流触发**：
```bash
# 停止发布
# 记录下次可发布时间（1 小时后）
```

---

## 🔒 限流规则

| 类型 | 限制 | 说明 |
|------|------|------|
| 新技能 | 5 个/小时 | 首次发布的技能 |
| 更新技能 | 无限制 | 已发布技能的版本更新 |

**注意事项**：
- 限流按小时计算，整点刷新
- 更新技能不占用新技能名额
- 遇到限流立即停止，等待刷新

---

## 📊 维护文件清单

| 文件 | 用途 | 位置 |
|------|------|------|
| PUBLISHED_SKILLS_MAINTENANCE.md | 已发布技能完整清单 | /workspace/projects/workspace/skills/ |
| PUBLISHED_SKILLS_TRACKING.md | 发布进度追踪 | /workspace/projects/lisah-workspace/workspace/skills/ |
| PUBLISH_LOG_2026-04.md | 发布日志 | /workspace/projects/workspace/skills/ |

---

## 🚫 常见错误汇总

### 错误 1：盲目执行 sync
- **现象**：尝试发布 self-improving-agent 等本地技能
- **原因**：sync 会扫描所有本地技能
- **解决**：先查看名单，只处理名单内的技能

### 错误 2：删除本地技能
- **现象**：删除了 self-improving-agent
- **原因**：脚本自动删除冲突技能
- **解决**：修改脚本，不自动删除；或手动确认后再删除

### 错误 3：发布无意义的名字
- **现象**：发布 mcdonalds-conflict-backup
- **原因**：slug 被占用后尝试变通
- **解决**：直接放弃，不要发布奇怪的名字

### 错误 4：不更新追踪文件
- **现象**：不知道 kfc 和 pizza-hut 是否已发布
- **原因**：发布后没有记录技能 ID
- **解决**：发布后立即更新追踪文件

---

## ✅ 检查清单

发布前：
- [ ] 查看 PUBLISHED_SKILLS_MAINTENANCE.md
- [ ] 确认技能在待发布名单中
- [ ] 检查限流状态（有可用名额）
- [ ] 确认技能目录和 SKILL.md 存在

发布后：
- [ ] 记录技能 ID
- [ ] 更新追踪文件
- [ ] 标记为已发布
- [ ] 提交 git 变更

遇到冲突：
- [ ] 记录到"已被占用的 Slug"列表
- [ ] 确认是否删除本地文件
- [ ] 更新维护文件

---

## 📝 经验教训总结（2026-04-09 更新）

### 核心原则
1. **严格按照名单发布** - 不要盲目执行 sync
2. **保护本地技能** - 绝对不删除本地使用的技能
3. **冲突直接跳过** - slug 被占用就放弃，不要尝试变通
4. **及时更新记录** - 发布后立即记录技能 ID
5. **限流时停止** - 遇到限流立即停止，等待刷新

### 新增经验（2026-04-09）

#### 6. 批量检查 slug 可用性
**方法**：
```bash
# 批量检查多个 slug
for slug in apple microsoft amazon; do 
  result=$(clawhub search "$slug" 2>&1 | grep "^$slug ")
  if [ -n "$result" ]; then 
    echo "$slug: OCCUPIED"
  else 
    echo "$slug: AVAILABLE ✅"
  fi
done
```

**教训**：
- TOP 34 高价值品牌中，约 90% 已被占用
- 发布前必须先检查，避免创建无用的 SKILL.md
- 记录检查结果到维护名单

#### 7. 24 小时限流规则
**规则**：
- 5 个新技能/小时
- **20 个新技能/24 小时**（重要！）

**教训**：
- 发布前检查 24 小时配额
- 接近 20 个时停止，等待次日刷新
- 更新技能不占用新技能名额

#### 8. 维护完整名单
**必须维护的文件**：
- `CLAWHUB_SKILLS_MASTER_LIST.md` - 完整状态清单
- `PUBLISHED_SKILLS_MAINTENANCE.md` - 已发布技能详情
- `PUBLISH_STATUS_SUMMARY.md` - 发布进度汇总

**每次发布后必须更新**：
1. 记录技能 ID 和发布时间
2. 验证技能（`clawhub search <slug>`）
3. 更新验证状态
4. 如遇冲突，记录占用者

#### 9. 识别已被占用的 slug
**常见占用者**：
- `/kongdeyu/*` - mcdonalds 等
- `/duanc-chao/*` - netflix 等
- `/ivangdavila/*` - booking, expedia, amazon 等
- `/agenticio/*` - instagram 等
- `/pskoett/*` - self-improving-agent 等

**策略**：
- 发现占用立即放弃
- 记录到维护名单
- 不要尝试变通名字

---

**技能用途**: 提供 ClawHub Skills 发布的最佳实践、正确流程和常见错误避免指南，帮助开发者高效、安全地发布技能。

---

**版本历史**:
- 1.0.1 (2026-04-09 09:55) - 更新：批量检查 slug、24 小时限流、维护名单规范
- 1.0.0 (2026-04-09) - 初始版本，记录发布经验和教训
