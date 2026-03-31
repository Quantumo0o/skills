# Kinema's Skill Making Pipeline

> **ClawHub**: https://clawhub.ai/leeshunee/kinema-skill-making-pipeline | `clawhub install kinema-skill-making-pipeline`


> OpenClaw Skill 开发与发布规范 | OpenClaw Skill Development & Publishing Specification

## 概述 | Overview

本仓库定义了 **KinemaClaw** 生态中 Skill 的开发、版本管理和发布的标准化流程。所有在 KinemaClaw 下开发的 Skill 必须遵循此规范。

This repository defines the standard process for skill development, version management, and publishing in the KinemaClaw ecosystem.

## 核心原则 | Core Principles

| 原则 | 说明 |
|------|------|
| **Git First** | 所有修改必须在 Git 仓库中管理 |
| **Atomic Commits** | 每次 commit 必须是有意义的独立变更 |
| **Versioned Releases** | 发布前必须打 Git tag |
| **No In-Place Publishing** | 禁止直接从 /app/skills/ 发布 |
| **Onboarding Required** | 每个 Skill 必须有安装/配置引导 |

## SKILL.md 规范 | SKILL.md Specification

每个 Skill 必须包含以下 YAML frontmatter 字段：

```yaml
---
name: skill-name
displayName: "Skill Name (Feature Description)"
version: 1.0.0
description: |
  功能描述和触发条件。
  Trigger: 触发场景描述。
---
```

### 必填字段 | Required Fields

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | Skill 标识符 | `alist-cli` |
| `displayName` | 人类可读名称（含功能描述） | `AList-CLI (Cloud Storage CLI for AList, with OpenClaw Skill)` |
| `version` | 语义化版本号 | `1.0.2` |
| `description` | 功能描述 + 触发条件 | 含 Trigger 说明 |

### displayName 格式规范

统一格式: **`Name (Feature Description)`**

示例：
- `AList-CLI (Cloud Storage CLI for AList, with OpenClaw Skill)`
- `Kinema's Concept Re-Search`
- `Kinema's Skill Making Pipeline`
- `SearXNG Search CLI (Free, Self-hosted, Auto-deploy, Multi-Channel)`

### 必须包含的链接

```markdown
- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)
```

## 发布流程 | Release Process

```bash
cd projects/<skill-name>

# 1. 确保所有修改已 commit
git status

# 2. 打版本 tag (语义化版本)
git tag v1.2.0

# 3. 推送 tag
git push origin v1.2.0

# 4. 创建 GitHub Release
gh release create v1.2.0 --title "v1.2.0 - description" --notes "changes..."

# 5. 发布到 ClawHub（--name 必须使用 displayName）
clawhub publish . --slug <skill-name> --name "<displayName>" --version 1.2.0 --changelog "changes..."
```

### 版本号规则 | Version Numbering

遵循语义化版本 (Semantic Versioning):

- **MAJOR**: 不兼容的 API 变更
- **MINOR**: 向后兼容的新功能
- **PATCH**: 向后兼容的 bug 修复

## 目录结构 | Directory Structure

```
<skill-name>/
├── SKILL.md              # 必需: Skill 定义
├── README.md             # 推荐: 仓库说明
├── LICENSE               # 推荐: 开源协议
├── scripts/              # 可选: 自动化脚本
└── references/           # 可选: 参考资料
```

## 禁止内容 | Prohibited Content

Skill 中**禁止**包含：
- 个人网站、域名
- 密码、账号、Token
- 个人邮箱、电话
- 真实姓名、身份信息

## GitHub 仓库规范

- 默认创建 **Private** 仓库
- 使用有意义的仓库名称
- 保持 README.md 与 SKILL.md 同步

## 许可证 | License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## 组织 | Organization

[KinemaClawWorkspace](https://github.com/KinemaClawWorkspace) — Building AI-powered OpenClaw Skills for the community.
