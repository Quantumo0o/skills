# agentic-commerce-news

> Agentic Commerce 每周产品快报 — 搜索过去一周大V（VC、企业家、AI领袖）推荐的 Agentic Commerce 相关创业产品和动态，生成结构化新闻简报。

## What it does

这是一个新闻聚合类 skill，专注于 **Agentic Commerce**（AI Agent 代人购物）这个快速演化的赛道。每次触发时，它会：

1. 并行发起 10+ 条不同角度的 WebSearch 查询（过去 7 天窗口）
2. 过滤出有大V / 机构背书的创业产品和动态
3. 按 9 层 Agentic Commerce Stack 分类（品牌发现→支付→消费端 Agent→全栈平台）
4. 生成按事件类型分组的卡片（融资 / 产品发布 / 大V观点 / 合作 / 报告）
5. 附速览汇总表 + 本周趋势洞察

## When it triggers

- 用户输入 `/agentic-commerce-news`
- 用户提到 "agentic commerce 新闻"、"AI commerce 最新动态"、"agent shopping 本周新产品" 等关键词
- 用户说类似 "帮我看看 agentic commerce 这周有什么新动态" 的话
- 用户要求设置定时任务推送 agentic commerce 动态

## Scheduling（定时任务）

支持三种运行方式，根据你的环境选择：

| 环境 | 命令 | 说明 |
|------|------|------|
| Claude Code 当前会话 | `CronCreate` 工具 | 会话内定时，不持久化 |
| Claude Code 持久化 | `/schedule` skill | 在 claude.ai 云端运行，长期生效 |
| OpenClaw | `openclaw cron add` | 7×24 后台运行 |

### 示例：每天早上 8 点定时推送（Claude Code）

对 Claude 说：
> 设置一个定时任务，每天早上 8 点运行 agentic-commerce-news 推送给我

Claude 会用 `CronCreate` 创建 `"3 8 * * *"` 规则（8:03am，避开整点）。

### 示例：OpenClaw 持久化定时

```bash
openclaw cron add \
  --name "Agentic Commerce Daily" \
  --cron "3 8 * * *" \
  --tz "Asia/Shanghai" \
  --message "运行 agentic-commerce-news skill，搜索过去一周 agentic commerce 领域的最新动态" \
  --channel <your-channel> \
  --to "<your-id>"
```

## Quality Gates

- 只收录过去 7 天的动态
- 必须有大V / 机构背书（VC 投资、推文推荐、官方报告、平台合作）
- 必须附原文链接
- 最少 5 条（淡周可少，严禁用旧新闻充数）
- 排除纯广告 / PR 内容

## Output Format

```
## Agentic Commerce 周报（4月8日 - 4月15日）
> 本周 8 条值得关注的动态

### 融资动态
### ProductName（融资 $XM）— 一句话摘要
**时间：** 4月12日
**背书：** 谁投的
**核心内容：**
- 要点 1
- 要点 2
**所属层级：** Payment Infrastructure
原文链接：https://...

### 产品发布
...

### 大V观点
...

## 本周速览

| 日期 | 公司/人物 | 事件类型 | 一句话摘要 | 层级 |
|------|----------|----------|-----------|------|
| ... | ... | ... | ... | ... |

## 本周趋势
1. ...
2. ...
```

## Installation

### Option A: 本地手动安装（Claude Code）

```bash
# 克隆到 ~/.claude/skills/
cp -r agentic-commerce-news ~/.claude/skills/

# 验证 frontmatter
cat ~/.claude/skills/agentic-commerce-news/SKILL.md | head -5
```

重启 Claude Code 会话后即可使用。

### Option B: 从 .skill 包安装

```bash
# 解压 .skill 文件到 skills 目录
unzip agentic-commerce-news.skill -d ~/.claude/skills/
```

### Option C: 发布到 ClawHub（OpenClaw 生态）

```bash
# 确保 openclaw CLI 已安装并登录
openclaw auth login

# 发布
openclaw publish ./agentic-commerce-news
```

发布前请确保：
- `SKILL.md` 的 `name` 字段和目录名一致
- `description` 字段清晰描述触发场景
- README.md 包含使用示例

## Dependencies

- Claude Code ≥ 1.0（需要 `WebSearch` 工具）
- （可选）`CronCreate` 工具或 `openclaw cron` — 定时任务场景
- **无需** API key 或外部依赖

## Customization

如果你想调整搜索策略：

1. 修改 `SKILL.md` 的 Phase 1 部分，增加/替换 WebSearch 查询模板
2. 修改 Phase 3 的分类表，增加行业细分
3. 修改 Phase 4 的卡片格式，调整输出风格

如果你想调整时间窗口（比如改成 3 天或 30 天）：

- 修改 `## Time Window` 章节的 "past 7 days" 描述
- 调整搜索查询中的 `this week` / `today` 等时间关键词

## License

MIT — 可自由使用、修改、分发。
