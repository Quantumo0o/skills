# 角色 × Skill 推荐目录

根据用户角色推荐适合的 Claude Code Skill。本目录需要持续维护——发现新的好 Skill 时及时补充。

## 推荐原则

1. **精不贪多**：每个角色推荐 5-10 个，不是越多越好
2. **说清为什么**：每条推荐附一句话说明为什么这个角色需要它
3. **区分已装和未装**：运行时扫描 `~/.claude/skills/` 判断

## 通用 Skill（所有角色都适用）

| Skill | 说明 | 来源 |
|-------|------|------|
| openclaw-persona-forge | 锻造龙虾灵魂，定义 Agent 性格 | 内置 |
| openclaw-soul-forge | 同上，英文版 | 内置 |
| baoyu-image-gen | AI 生图，头像/示意图/信息图 | github.com/JimLiu/baoyu-skills |
| baoyu-infographic | 信息图生成 | github.com/JimLiu/baoyu-skills |

## 工程师（Software Engineer / Developer）

| Skill | 为什么适合 | 来源 |
|-------|-----------|------|
| test-driven-development | 写代码前先写测试，工程纪律 | 内置 |
| systematic-debugging | 结构化排查 bug，不靠直觉 | 内置 |
| verification-before-completion | 完工前跑验证，防止遗漏 | 内置 |
| requesting-code-review | 主动请求代码审查 | 内置 |
| receiving-code-review | 收到 review 后的处理流程 | 内置 |
| git-committing | 规范化提交 | 内置 |
| deploy-test | Jenkins 测试环境发布 | 内置 |

## 前端工程师（Frontend Engineer）

继承「工程师」全部，额外推荐：

| Skill | 为什么适合 | 来源 |
|-------|-----------|------|
| example-skills:frontend-design | 高质量 UI 组件生成 | Anthropic 官方 |
| example-skills:webapp-testing | Playwright 自动化测试 | Anthropic 官方 |
| ui-reference-to-code | 从 UI 参考图生成代码 | 内置 |
| rn-stream-content-block | React Native 流式渲染 | 内置 |

## 产品经理（Product Manager）

| Skill | 为什么适合 | 来源 |
|-------|-----------|------|
| writing-plans | 写实施方案，结构化拆解需求 | 内置 |
| brainstorming | 创意发散，功能探索 | 内置 |
| meeting-minutes | 会议纪要自动生成 | 内置 |
| example-skills:doc-coauthoring | 协作写 PRD/技术文档 | Anthropic 官方 |
| example-skills:pptx | 做演示文稿 | Anthropic 官方 |
| ipcha-mistabra | 批判性思考，决策分析 | 内置 |

## CEO / 创始人（Founder / CEO）

| Skill | 为什么适合 | 来源 |
|-------|-----------|------|
| ipcha-mistabra | 重大决策的对抗性分析 | 内置 |
| brainstorming | 战略头脑风暴 | 内置 |
| writing-plans | 战略规划拆解 | 内置 |
| weekly-report | 团队周报汇总 | 内置 |
| twitter-operation-for-indie-hackers | 个人品牌 & 推特运营 | 内置 |
| example-skills:internal-comms | 内部沟通模板 | Anthropic 官方 |

## 设计师（Designer）

| Skill | 为什么适合 | 来源 |
|-------|-----------|------|
| baoyu-image-gen | AI 快速出图 | github.com/JimLiu/baoyu-skills |
| baoyu-infographic | 信息图设计 | github.com/JimLiu/baoyu-skills |
| example-skills:canvas-design | 视觉设计创作 | Anthropic 官方 |
| example-skills:frontend-design | 设计转代码 | Anthropic 官方 |
| ui-reference-to-code | 参考 UI 转代码 | 内置 |
| example-skills:theme-factory | 主题/风格系统 | Anthropic 官方 |

## 内容创作者（Content Creator / Writer）

| Skill | 为什么适合 | 来源 |
|-------|-----------|------|
| transcript-summarizer | 播客/视频逐字稿总结 | 内置 |
| example-skills:doc-coauthoring | 协作写长文 | Anthropic 官方 |
| baoyu-infographic | 配图信息图 | github.com/JimLiu/baoyu-skills |
| reddit-translator | 中译英，Reddit 风格 | 内置 |
| rss-daily-digest | AI 资讯日报 | 内置 |

## 数据分析师（Data Analyst / Scientist）

| Skill | 为什么适合 | 来源 |
|-------|-----------|------|
| example-skills:xlsx | Excel 数据处理 | Anthropic 官方 |
| example-skills:pdf | PDF 数据提取 | Anthropic 官方 |
| systematic-debugging | 数据管道排查 | 内置 |
| writing-plans | 分析方案设计 | 内置 |

## 研究员（Researcher）

| Skill | 为什么适合 | 来源 |
|-------|-----------|------|
| github-kb | GitHub 知识库管理 | 内置 |
| quality-website-search | 优质资源搜索 | 内置 |
| transcript-summarizer | 论文/讲座总结 | 内置 |
| ipcha-mistabra | 研究方法论批判 | 内置 |
| guided-learning | 引导式学习 | 内置 |

## 学生（Student）

| Skill | 为什么适合 | 来源 |
|-------|-----------|------|
| guided-learning | 引导式学习新技术 | 内置 |
| systematic-debugging | 学习调试方法论 | 内置 |
| transcript-summarizer | 课程/讲座总结 | 内置 |
| example-skills:doc-coauthoring | 写论文/报告 | Anthropic 官方 |

## 运维 / DevOps

| Skill | 为什么适合 | 来源 |
|-------|-----------|------|
| deploy-test | Jenkins 发布管理 | 内置 |
| aliyun-init | 阿里云服务器初始化 | 内置 |
| systematic-debugging | 线上问题排查 | 内置 |
| verification-before-completion | 操作验证 | 内置 |

---

## 维护说明

- 发现新的好 Skill → 添加到对应角色下
- Skill 废弃或改名 → 及时移除或更新
- 新增角色分类 → 在末尾添加新 section
- 保持每个角色 5-10 条推荐，不要膨胀
