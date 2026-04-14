---
name: clawhub-search
slug: skylv-clawhub-search
version: 1.0.0
description: "ClawHub Skill Discovery and Search. Find, browse, and install OpenClaw Skills from ClawHub marketplace. Triggers: search skills, find skills, clawhub, install skill, browse skills."
author: SKY-lv
license: MIT
tags: [clawhub, search, discovery, openclaw, marketplace]
---

# ClawHub Search — ClawHub 技能发现助手

## 功能说明

帮助用户在 ClawHub 市场中搜索、浏览和安装 OpenClaw Skills。提供技能推荐、分类浏览、安装指导等功能。

## 使用场景

1. **搜索技能** - 根据功能需求查找 Skills
2. **浏览分类** - 按类别浏览可用 Skills
3. **技能推荐** - 根据使用场景推荐 Skills
4. **安装指导** - 帮助用户安装 Skills
5. **技能对比** - 比较类似 Skills 的功能

## 使用方法

### 1. 搜索技能

```
用户：找一个能帮我写代码的 Skill
```

输出：
- 相关 Skills 列表（名称、描述、安装命令）
- 每个 Skill 的评分和下载量
- 安装建议

### 2. 浏览分类

```
用户：ClawHub 有哪些开发相关的 Skills？
```

输出：
- Development 分类下的所有 Skills
- 按热门程度排序
- 快速安装命令

### 3. 技能推荐

```
用户：我是前端开发者，需要什么 Skills？
```

输出：
- 前端开发推荐 Skills（5-10 个）
- 每个 Skill 的使用场景
- 安装优先级建议

### 4. 安装技能

```
用户：帮我安装 code-generation 这个 Skill
```

输出：
- 安装命令和执行步骤
- 安装后的配置说明
- 使用示例

## 技能分类

### AI Agents
- agent-builder
- browser-automation-agent
- database-agent
- multi-agent-orchestrator

### Development Helpers
- ci-cd-helper
- code-generation
- code-reviewer
- docker-helper
- git-helper
- kubernetes-helper
- sql-helper

### Developer Tools
- api-documentation
- function-calling
- graphql-helper
- mcp-server-builder
- prompt-engineer
- rag-engine
- regex-helper

### Productivity
- email-agent
- notion-skill
- workflow-automation

### Data & Analytics
- data-pipeline
- data-visualization
- financial-analyst
- research-assistant

## ClawHub API

### 搜索接口

```javascript
// 搜索 Skills
GET https://api.clawhub.ai/skills/search?q={query}

// 获取技能详情
GET https://api.clawhub.ai/skills/{slug}

// 获取分类列表
GET https://api.clawhub.ai/skills/categories
```

### 安装命令

```bash
# 安装单个 Skill
npx clawhub@latest install {skill-name}

# 同步所有 Skills
npx clawhub@latest sync

# 列出已安装 Skills
npx clawhub@latest list
```

## 推荐策略

### 按用户角色推荐

| 角色 | 推荐 Skills |
|------|-------------|
| 前端开发 | code-generation, git-helper, prompt-engineer |
| 后端开发 | database-agent, api-documentation, docker-helper |
| DevOps | ci-cd-helper, kubernetes-helper, monitoring-alerting |
| 数据科学 | data-pipeline, data-visualization, research-assistant |
| 产品经理 | notion-skill, workflow-automation, email-agent |

### 按热门程度推荐

1. skylv-code-generation - 代码生成（最热门）
2. skylv-git-helper - Git 操作
3. skylv-docker-helper - Docker 容器
4. skylv-prompt-engineer - Prompt 优化
5. skylv-database-agent - 数据库助手

## 安装指导

### 前置条件

- Node.js 18+
- OpenClaw CLI 已安装
- 网络连接正常

### 安装步骤

1. 打开终端
2. 运行安装命令
3. 等待下载完成
4. 验证安装成功

### 常见问题

**Q: 安装失败怎么办？**
A: 检查网络连接，确认 ClawHub 服务正常，重试安装命令。

**Q: Skill 不工作？**
A: 检查 OpenClaw 版本兼容性，查看 Skill 文档的依赖要求。

**Q: 如何卸载 Skill？**
A: 使用 `npx clawhub@latest remove {skill-name}` 命令。

## 相关文件

- ClawHub 官方文档：https://docs.openclaw.ai/tools/clawhub
- 技能市场：https://clawhub.ai
- OpenClaw 文档：https://docs.openclaw.ai

## 触发词

- 自动：检测技能搜索、安装相关关键词
- 手动：/clawhub, /search-skills, /install, /skills
- 短语：找技能、装技能、有什么技能、推荐技能
