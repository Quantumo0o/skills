---
name: quick-learn
description: 快速学习教练——支持两种学习模式：(1) 多日系统学习：搜索最新权威资料，基于费曼学习法生成学习路径，每日定时推送；(2) 快速学习：丢一篇文章/一本书/一个链接，立即结构化解读。当用户说"帮我学 xxx""快速入门 xxx""制定 xxx 学习计划""每天推送我学 xxx""学完考我 xxx""帮我解读这篇文章""快速读这本书""总结这个链接""快速学习 xxx 文章/书"时使用此技能。适用场景：理解陌生代码库、掌握新概念/技术、阅读总结长文档、系统化学习任何主题、快速理解一篇文章/一本书。
---

# Quick Learn — 快速学习教练

## 核心方法：费曼学习法

按费曼四步法驱动每日互动：

```
Step 1. 学习材料 → 推送今日阅读/视听内容
Step 2. 复述给我听 → 用户用自己的话解释
Step 3. 查漏 → 找出理解薄弱点，回补资料
Step 4. 简化 → 用户用通俗语言/类比重新解释
```

传统推送 = 单向灌输。费曼推送 = 对话式学习，逼用户「讲出来」，暴露理解盲区。

## 总流程

### 模式 A：多日系统学习

```
用户说想学 X → 搜索权威资料 → 智能评估天数 → 生成学习路径
→ 创建 cron 每日推送 → 每日费曼四步互动 → 到期自测 + 进阶推荐
```

### 模式 B：快速学习单篇文章/书籍

```
用户丢一篇文章/书籍/链接 → 识别类型 → 立即抓取 + 结构化解读 → 费曼引导 + 自测
```

触发词："帮我解读这篇文章"、"快速读这本书"、"总结这个链接"、"帮我快速学 xxx"。

## Step 1：搜索权威资料

用 `web_search` 或 `search` 技能（百度/谷歌）并行搜索 5 个维度：

| 搜索词 | 目的 |
|---|---|
| `{topic} tutorial beginner 2024..2026` | 最新入门教程 |
| `{topic} best practices guide` | 权威指南 |
| `{topic} documentation official` | 官方文档 |
| `{topic} awesome list` / `{topic} roadmap` | 社区精选 / 路线图 |
| `{topic} video course lecture` | 视频/音频课程 |

取前 15-25 条结果，`web_fetch` 抽查 3-5 个验证质量，筛选为必读/选读，写入 `learning-data/{topic-slug}/sources.md`。

**详细搜索策略与权威验证清单** → 见 [references/source-search.md](references/source-search.md)

## Step 2：生成学习路径

### 智能评估天数

**用户无需指定天数**——agent 基于教育心理学研究自动评估（见 [references/scientific-basis.md](references/scientific-basis.md)）：

```
基础天数 = max(3, ceil(新概念数量 / 3))
```

| 修正因子 | 调整 | 说明 |
|---|---|---|
| 零基础 | × 1.3 | 需建立先验知识 |
| 有相关经验 | × 0.7 | 可利用已有图式 |
| 需动手实践 | + 2 天 | 实验性学习需额外时间 |
| 速成模式 | max(3, -2天) | 牺牲深度保最低间隔 |
| 系统学习 | × 1.5 | 增加深度和广度 |

**评估流程**：搜索了解概念 → 统计新概念数 → 套公式 → 告知用户并征求确认。

### 路径结构

```
Day 1-2: 概念建立 → Day 3-4: 深入核心 → Day 5-6: 动手实践 → Day 7: 总结自测
```

### 路径 JSON

写入 `learning-data/{topic-slug}/path.json`：

```json
{
  "topic": "xxx",
  "slug": "xxx",
  "total_days": 7,
  "created_at": "2026-04-06",
  "status": "active",
  "current_day": 1,
  "daily_time_min": 30,
  "preferred_time": "09:00",
  "timezone": "Asia/Shanghai",
  "push_channel": "webchat",
  "learning_method": "feynman",
  "days": [
    {
      "day": 1,
      "title": "建立认知",
      "keywords": ["overview", "introduction"],
      "feynman_prompt": "试着用你自己的话解释：{topic} 是什么？为什么需要它？",
      "simplify_target": "想象你在给一个完全不懂的人解释。",
      "completed": false,
      "completed_at": null
    }
  ]
}
```

`title` 和 `keywords` 创建时固定，`materials` 推送时实时搜索填充。

### 脚本辅助

```bash
python3 skills/quick-learn/scripts/learner.py path "{topic}" {days} --output learning-data/{slug}/path.json
```

脚本生成骨架，agent 填入真实资料和费曼引导语。

## Step 3：创建每日推送

**一个 cron 管理一个计划，多计划互不干扰。**

### 推送策略：框架固定 + 内容实时更新

创建时（定框架）：Day 1: 核心概念, Day 2: 架构设计...
推送时（填内容）：读取今日 title → 实时搜索最新资料 → 抓取/整理/出图/推送

### Cron 配置

```json
{
  "name": "quick-learn: {topic-slug}",
  "schedule": { "kind": "cron", "expr": "0 {hour} * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "检查 learning-data/{slug}/path.json，如果 status=active 且 current_day <= total_days：\n1. 读取今日 title\n2. 实时搜索最新权威资料\n3. 整理成结构化笔记（见 Step 4）\n4. 推送给用户\n5. 附费曼引导语\n6. current_day += 1\n如果已学完，推送完成消息并禁用此 cron。"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

### 多计划并行

每个计划：独立数据目录、独立 cron、独立进度、独立费曼互动。推送标题标明主题避免混淆。

## Step 4：费曼四步推送

### Step 4-1. 推送结构化学习笔记

**关键原则：不要只丢链接！用 `web_fetch` 抓取后整理再推送。**

推送格式模板：

```
📚 学习计划 | {topic} · Day {n}/{total}
🎯 今日主题：{title}
⏱ 预计用时：{total_min} 分钟
━━━━━━━━━━━━━━━━━━━━━━━━━━
一、核心概念（2-4 段通俗易懂解释）
二、关键要点（附 `→ [来源](URL)`）
三、概念关系（一句话或图示）
四、图解（Mermaid 优先 / ASCII 备选）
五、实际例子（1-2 个生活类比）
━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 延伸阅读（可选） + 🎧 适合通勤听
━━━━━━━━━━━━━━━━━━━━━━━━━━
✏️ 现在，试着用自己的话回答：{feynman_prompt}
💡 今日预计 {total_min} 分钟。时间不够/想多学点随时说 👇
```

**整理内容 6 项要求：** 先抓后写、说人话举例子、标注原文出处、权威验证、时效验证（优先 2 年内）、控制篇幅（500-800 字不含图）。

**权威来源优先级：** ⭐⭐⭐ 官方文档/GitHub Org → ⭐⭐ 知名技术社区/权威课程 → ⭐ 高质量博客 → ❌ 拒绝无署名搬运/过时/营销内容。

### Step 4-2. 用户复述后 → 查漏

对比材料找遗漏 → 温和指出 → 回补 1-2 个关键概念 → 请用户重新解释。

### Step 4-3. 用户再复述后 → 简化

确认正确后，要求用最通俗语言/生活类比重新解释，控制在 3-5 句话。

### Step 4-4. 标记完成

更新 `path.json` → `completed: true`，点评简化版本，给出明日预告。

## Step 5：跳步与难度调整

- 「跳过费曼」→ 尊重选择，温和建议下次尝试
- 「没太看懂」→ 降低难度，用更简单类比解释

## Step 6：中途管理

### 放弃

共情不评判 → 诊断原因（太难/太简单/太忙）→ 给方案 → 若坚持：生成 `summary-abandoned.md`，标记 `status: abandoned`，禁用 cron。

### 重新开始

- 从某天重新学 → 修改 `current_day` 回退
- 完全重新开始 → 旧 `path.json` 存档为 `path-v1-backup.json`，新建 `path.json`
- 换个角度学 → 换资料方向，更新 `sources.md`

### 动态调整当日学习量

| 场景 | 响应 |
|---|---|
| 今天只有 15 分钟 | 只保留核心概念 + 图，费曼简化为 1 问 |
| 多学点 | 追加选读材料 + 深度追问，可跳 1 天 |
| 连续 3 天 time_ratio < 0.5 | 主动建议：拉长天数 / 每天量减半 / 暂停 |

在 `path.json` 中记录每日实际时长：

```json
{
  "days": [{
    "day": 1, "title": "建立认知",
    "planned_time_min": 30, "actual_time_min": 15,
    "time_ratio": 0.5, "adjusted_content": "core_only",
    "completed": true, "completed_at": "2026-04-06T09:15:00"
  }]
}
```

## Step 7：每日学习日志

每次推送和用户互动后，自动记录到 `learning-data/{slug}/daily-log.md` 和 `daily-log.json`：

| 字段 | 说明 |
|---|---|
| 完成时间 | 用户回复「完成」的时间戳 |
| 学习时长 | 用户自报或估算 |
| 费曼复述 | 是否完成用自己的话解释 |
| 薄弱点 | 查漏环节发现的理解不足 |
| 简化质量 | 1-5 星 |
| 情绪/动力 | 积极/中性/疲惫/想放弃 |

**用途：** 学习报告、调整节奏（连续「疲惫」→ 建议降速）、放弃总结、长期回顾。

## Step 8：遗忘曲线复习提醒

学完每个概念后，在 **1 天 / 3 天 / 7 天** 节点自动推送 5 分钟复习卡：

```
🔄 复习提醒 | {topic} · Day {n} 回顾
📌 一句话总结：{核心}
🧠 快速自测（30 秒）：{1 道简短问题}
💡 提示：{小提示}
```

**链式调度**：答对 → 安排下一次复习（+3 天）→ 连续 3 次答对 → 标记「已内化」终止；答错 → 1 天后重复习。

**实现**：为每个已完成的学习日创建独立的 `at` 类型 cron。

→ 完整复习卡格式、cron 配置、自适应规则见 [references/forgetting-curve.md](references/forgetting-curve.md)

## Step 9：知识图谱与周报

### 知识图谱

每学完 2-3 天生成 Mermaid 概念地图，展示已掌握/学习中/待学习概念状态。

→ 完整格式、状态维护见 [references/knowledge-map.md](references/knowledge-map.md)

### 学习周报

每周自动生成学习周报（时长柱状图、完成率进度条、情绪趋势折线图、费曼质量星级走势）。

→ 完整格式、cron 配置见 [references/weekly-report.md](references/weekly-report.md)

## Step 10：学习风格自适应

前 2 天使用均衡风格，第 3 天起根据用户行为（图文偏好、阅读时长、费曼质量、互动深度）自动调整推送风格。随时可通过「多给图/多给代码/精简点」手动调整。

→ 完整规则、数据存储、渐进式调整见 [references/learning-style.md](references/learning-style.md)

## Step 11：进阶路径推荐

自测完成或整个学习计划完成后，自动生成进阶建议（推荐 + 备选 + 拓展），基于主题依赖关系和学习表现。

→ 推荐逻辑和映射表见 [references/advanced-path.md](references/advanced-path.md)

## Step 12：进度管理

### 单计划操作

用户随时可对每个学习计划单独操作：

| 用户说 | 操作 |
|---|---|
| 「学到哪了」 | 读取 `path.json` + `daily-log.md` 报告进度 |
| 「暂停学习」 | 禁用对应 cron（`name: quick-learn:{slug}`） |
| 「继续学习」 | 恢复对应 cron |
| 「调整到晚上 8 点」 | 更新 cron schedule |
| 「放弃这个计划」 | 生成学习总结 → 删除 cron → 标记 abandoned |
| 「重新开始」 | 旧数据存档，新建 `path.json` |

### 多计划总览

```bash
# 查看所有活跃计划
for f in learning-data/*/path.json; do
  python3 -c "import json; d=json.load(open('$f')); print(f'{d[\"topic\"]}: Day {d[\"current_day\"]}/{d[\"total_days\"]} | {d[\"status\"]}')"
done
```

## 模式 B：快速学习数据隔离

快速学习数据存放在 `learning-data/` 下，使用 `quick-{slug}` 前缀区分：

```
learning-data/
├── react-intro/              ← 系统学习
├── quick-article-abc123/     ← 快速学习（文章）
└── quick-book-xxx/           ← 快速学习（书籍）
```

用户随时可查询快速学习历史或重新复习某篇文章。

## 参考资料

- 权威资料搜索策略 → [references/source-search.md](references/source-search.md)
- 不同领域学习模式 → [references/learning-patterns.md](references/learning-patterns.md)
- 费曼学习法实践 → [references/feynman-guide.md](references/feynman-guide.md)
- 图解设计指南 → [references/diagram-guide.md](references/diagram-guide.md)
- 学习天数科学评估（8 篇论文） → [references/scientific-basis.md](references/scientific-basis.md)
- 遗忘曲线复习 → [references/forgetting-curve.md](references/forgetting-curve.md)
- 知识图谱 → [references/knowledge-map.md](references/knowledge-map.md)
- 学习周报 → [references/weekly-report.md](references/weekly-report.md)
- 学习风格自适应 → [references/learning-style.md](references/learning-style.md)
- 进阶路径推荐 → [references/advanced-path.md](references/advanced-path.md)
