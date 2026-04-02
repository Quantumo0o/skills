---
name: baikexia
description: 蜗牛公司百科虾技能包。为员工解答公司相关问题（制度、福利、流程、组织架构等）。当用户询问公司相关问题时触发。知识库没有的问题一律不答，不编造，不联网搜索。
---

# 百科虾技能包

蜗牛公司百科虾知识库 Q&A 技能。

## 文件结构

```
walter-baikexia/
├── SKILL.md                    # 本文件
├── config/
│   └── app.json                # 飞书应用凭证（需用户创建）
├── cache/                      # 运行时知识库缓存（同步后生成）
│   ├── content.json
│   ├── metadata.json
│   └── images/
├── scripts/
│   ├── send-message.js         # 飞书消息发送（含 mention 支持）
│   └── sync.js                 # 知识库同步脚本
└── references/                 # Agent 角色模板（供 agent-factory 使用）
    ├── IDENTITY.md
    ├── SOUL.md
    └── AGENTS.md
```

## 部署步骤

### Step 1：安装本 Skill

```bash
openclaw skills install walter-baikexia
```

### Step 2：创建 Agent

```bash
openclaw agents add baikexia --workspace ~/.openclaw/workspace-baikexia
```

### Step 3：配置飞书凭证

在 skill 目录下创建 `config/app.json`：

```json
{
  "app_id": "cli_xxx",
  "app_secret": "xxx"
}
```

### Step 4：初始化知识库

```bash
node ~/.openclaw/skills/walter-baikexia/scripts/sync.js
```

成功后会生成 `cache/content.json`（知识库内容）和 `cache/metadata.json`（同步元数据）。

## 管理员命令

| 命令 | 操作 |
|------|------|
| `同步知识库` | 执行 `sync.js` 增量同步（内容变化才更新） |
| `同步知识库 --force` | 强制全量同步 |
| `同步状态` | 读取 `cache/metadata.json` 汇报同步状态 |

## 核心文件说明

### scripts/send-message.js

通过飞书 IM API 发送消息，支持 mention（@人）和图片。

```
node send-message.js <receive_id> <receive_id_type> [content_file]
```

- `receive_id`：接收者 ID（open_id / user_id 等）
- `receive_id_type`：ID 类型（`open_id` / `user_id` 等）
- `content_file`：消息内容文件路径，默认从 stdin 读取

**mention 格式**：回复中的 `『AT:user_id:姓名』` 会被转换为飞书 `<at user_id="...">姓名</at>` 标签发送。

### scripts/sync.js

从飞书知识库同步文档内容到本地缓存。

- 依赖 `config/app.json` 中的凭证
- 缓存输出到 `cache/content.json`
- 支持增量同步（hash 对比）
- `--force` 参数强制全量同步

### references/

供 agent-factory 创建新 agent 时复制到目标 workspace 的模板文件：

- `IDENTITY.md` — 百科虾身份定义
- `SOUL.md` — 行为准则（只答知识库有的、mention 处理、图片发送）
- `AGENTS.md` — 工作手册（知识库路径、禁止事项）

## 知识库路径

Agent 运行时通过以下路径读取知识库：

- 内容：`../skills/walter-baikexia/cache/content.json`（相对于 agent workspace）
- 元数据：`../skills/walter-baikexia/cache/metadata.json`
- 同步图片：`../skills/walter-baikexia/cache/images/`

## 注意事项

- `cache/` 目录为运行时生成，不属于 skill 源码，无需提交
- `config/app.json` 包含敏感凭证，勿提交到版本控制
- 知识库同步需要机器能访问飞书 API（`open.feishu.cn`）
