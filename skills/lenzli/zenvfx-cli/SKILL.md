---
name: zenvfx-cli
description: Use this skill when the user needs to create AI videos, manage canvases, nodes, files, or interact with the ZenVFX platform via CLI. Trigger keywords include "画布", "视频生成", "zenvfx", "canvas", "node", "AI视频", "文生视频".
metadata: {"openclaw": {"emoji": "🎬", "os": ["darwin", "linux"], "requires": {"bins": ["zenvfx"], "env": ["ZENVFX_MCP_TOKEN"]}, "primaryEnv": "ZENVFX_MCP_TOKEN", "install": [{"id": "npm", "kind": "command", "command": "npm install -g @tencent/zenvfx-cli --registry https://mirrors.tencent.com/npm/", "bins": ["zenvfx"], "label": "Install ZenVFX CLI (npm)"}]}}
---

# ZenVFX CLI Skill

## 概述

ZenVFX CLI 是 AI 视频创作平台的命令行工具，通过画布（Canvas）中的节点（Node）+ 连线（Edge）构建 AI 生成任务。

**CLI 入口**：`zenvfx <command>`
**输出协议**：stdout 输出纯 JSON（`{"ok":true,"data":{...}}` / `{"ok":false,"error":{...}}`），stderr 输出调试日志。解析返回值时用 `2>/dev/null` 过滤 stderr。

---

## 安装

```bash
npm install -g @tencent/zenvfx-cli --registry https://mirrors.tencent.com/npm/
# OpenClaw 环境安装 skill（非交互模式须加 --force）
npx clawhub@latest install zenvfx-cli --force
```

---

## 认证

```bash
zenvfx auth:login <your-mcp-token>
# 指定 host: zenvfx auth:login <token> --host <host-url>
```

`auth:login` 自动保存：`mcpToken`、`defaultUserId`、`defaultUsername`、`defaultProject`、`defaultWorkspace`、`wsHost`。后续命令无需再手动 `config:set`。

也可通过环境变量：`ZENVFX_MCP_TOKEN`、`ZENVFX_PROJECT`

---

## 命令速查

### 配置

| 命令 | 用途 |
|------|------|
| `auth:login <token>` | 一键认证（自动保存所有配置），可选 `--host` |
| `config:set <key> <value>` | 手动设置配置项 |
| `config:get <key>` / `config:list` | 读取配置 |

合法 key：`host`, `wsHost`, `mcpToken`, `defaultProject`, `defaultUsername`, `defaultUserId`, `defaultWorkspace`

### 文件系统

路径格式：`/<projectId>/目录/文件名`

| 命令 | 用途 |
|------|------|
| `file:stat --path <path>` | 查看文件/目录详情 |
| `file:readdir --path <path>` | 读取目录内容（不递归） |
| `file:mkdir --path <path>` | 创建目录（默认递归） |
| `file:rm --path <path>` | 删除文件/目录 |
| `file:tree --path <path>` | 目录树，可选 `--max-depth` |
| `file:path-to-id --path <path>` | 路径转内部 ID |
| `file:upload` | 上传本地文件 |
| `project:list` | 列出项目 |

### 画布管理

标注 `[S]` 的命令需先 `canvas:open`（会自动拉起 daemon）。

| 命令 | 用途 |
|------|------|
| `canvas:create --name <名称>` | 创建画布，可选 `--path`（默认 `defaultWorkspace`） |
| `canvas:list` | 列出画布（不递归），可选 `--list-path` |
| `canvas:open --canvas <path>` | 打开画布（启动 Session） |
| `canvas:info` `[S]` | 查看画布信息 |
| `canvas:save` `[S]` | 保存画布 |
| `canvas:run --node <id>` `[S]` | 运行节点。`--wait` 自动轮询等待（默认超时 10 分钟） |

### 节点操作 `[S]`

编辑类命令执行后**自动保存**画布。

| 命令 | 用途 |
|------|------|
| `canvas:node:list` | 列出所有节点 |
| `canvas:node:info --id <id>` | 查看节点详情（含 taskId/taskStatus） |
| `canvas:node:add <type>` | 添加节点，可选 `--name --position "x,y"` |
| `canvas:node:remove --id <id>` | 删除节点 |
| `canvas:node:set --id <id>` | 设置参数（推荐 `--options-json`） |

> **节点位置**：添加多个节点时用 `--position "x,y"` 指定坐标，避免叠加。建议水平间隔 400px：`"0,0"`、`"400,0"`、`"800,0"`。

### 连线操作 `[S]`

| 命令 | 用途 |
|------|------|
| `canvas:edge:list` | 列出所有连线 |
| `canvas:edge:add` | 连接节点（`--source --source-handle --target --target-handle`） |
| `canvas:edge:remove --id <id>` | 删除连线 |

### 查询

| 命令 | 用途 |
|------|------|
| `node:list` | 列出所有可用节点类型定义（本地，不需网络） |
| `node:model <nodeType>` | 查询节点支持的模型列表（需认证） |
| `task:status <taskId> --canvas-id <id>` | 查询任务状态（不需 daemon） |

### 守护进程

| 命令 | 用途 |
|------|------|
| `daemon:ping` / `daemon:status` / `daemon:stop` | 检测/查看/停止 daemon |

---

## 画布路径说明

`canvas:create` 返回的 `canvasPath` **不含** `.canvas` 后缀。canvas 类命令带不带后缀均可。
`file:stat`、`file:path-to-id` 等文件命令**需要**完整文件名（带 `.canvas`）。

**建议**：直接用 `canvas:create` 返回的 `canvasPath` 传给后续 canvas 命令。

---

## 核心流程：生成 AI 视频

```
0. auth:login <token>                          （一次性）
1. canvas:create --name "xxx"                  （自动使用 defaultWorkspace）
2. canvas:open --canvas "${CANVAS_PATH}.canvas"
3. canvas:node:add normal_video_generator --position "0,0"
4. canvas:node:set --options-json '{...}'
5. canvas:run --node <id> --wait --timeout 1800000
```

### 视频节点运行

**方式 1：`--wait` 同步等待（推荐）**

```bash
zenvfx canvas:run --node $NODE_ID --canvas "${CANVAS_PATH}" --wait --timeout 1800000
# 内置自动轮询，完成后返回 {"status":"completed","outputs":[{"url":"..."}]}
```

**方式 2：异步提交 + cron job 轮询**

适用于不希望阻塞进程的场景。**建议创建 cron job 定时轮询**：

1. `canvas:run --node <id>` — 立即返回 `{"submitted":true,"taskId":"xxx"}`
2. 获取 `canvasId`：`file:path-to-id --path "${CANVAS_PATH}.canvas"`
3. **创建 cron job**，每 **10 秒**执行 `task:status <taskId> --canvas-id <canvasId>`
4. 当 `status` 为 `completed`/`failed` 时停止，最长 **30 分钟**

> `outputs` 中有效 URL 在 `url` 字段（带 COS 签名），`download_url` 可能为空。

### 完整示例

```bash
# 0. 认证
zenvfx auth:login <your-mcp-token>

# 1. 创建画布
CREATE_RESULT=$(zenvfx canvas:create --name "测试画布" 2>/dev/null)
CANVAS_PATH=$(echo $CREATE_RESULT | grep -o '"canvasPath":"[^"]*"' | sed 's/"canvasPath":"//;s/"$//')

# 2. 打开画布
zenvfx canvas:open --canvas "${CANVAS_PATH}.canvas"

# 3. 添加节点
RESULT=$(zenvfx canvas:node:add normal_video_generator --name "文生视频" --position "0,0" --canvas "${CANVAS_PATH}" 2>/dev/null)
NODE_ID=$(echo $RESULT | grep -o '"id":"[^"]*"' | head -1 | sed 's/"id":"//;s/"$//')

# 4. 设置参数（建议 kling + 720P 加速生成）
zenvfx canvas:node:set --id $NODE_ID --options-json \
  '{"prompt":"傍晚的海边，小孩子嬉戏玩水","model":"kling","clarity":"RESOLUTION_720P","ratio":"16:9","duration":5}' \
  --canvas "${CANVAS_PATH}"

# 5. 运行并等待（超时 30 分钟）
zenvfx canvas:run --node $NODE_ID --canvas "${CANVAS_PATH}" --wait --timeout 1800000 2>/dev/null
```

---

## 节点参数

> **重要**：model/clarity/ratio/duration 的值**必须通过 `node:model <nodeType>` 动态查询**，不要硬编码。

> **视频节点建议**：模型 `kling` + 分辨率 `RESOLUTION_720P`（比 1080P 快 2-3 倍）。

通过 `--options-json` 统一传参：

| 参数 | 类型 | 说明 |
|------|------|------|
| `prompt` | string | 提示词 |
| `model` | string | 模型 ID（动态查询） |
| `clarity` | string | 分辨率枚举 |
| `ratio` | string | 画幅比例 |
| `duration` | number | 时长秒数（仅视频节点） |

**常用节点类型**：`normal_video_generator`（文/图生视频）、`image_generator`（文/图生图）、`composite_video_generator`（视频编辑）、`first_to_last_video_generator`（首尾帧视频）

---

## 异常处理

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| `AUTH_REQUIRED` | Token 未配置 | `auth:login <token>` |
| `MCP_TOKEN_INVALID` | Token 无效/过期 | 重新获取后 `auth:login` |
| `CANVAS_NOT_FOUND` | 画布不存在 | 检查路径，`file:stat` 确认 |
| `CANVAS_SAVE_FAILED` | 保存失败（server overload） | 重试 2-3 次，间隔 3-5 秒 |
| `NODE_NOT_FOUND` | 节点不存在 | `canvas:node:list` 确认 |
| `OPTION_NOT_FOUND` | 无该选项 | `canvas:node:info --id <id>` 查看 |
| `DAEMON_TIMEOUT` | daemon 超时 | `daemon:stop` 后重试 |
| `TIMEOUT` | 请求超时 | 增大 `--timeout` |
| `TASK_SUBMIT_FAILED` | 任务提交失败 | 检查节点参数 |

**daemon 异常**时强制清理：
```bash
zenvfx daemon:stop
kill $(cat ~/.config/zenvfx/daemon.pid) 2>/dev/null
rm -f ~/.config/zenvfx/daemon.sock ~/.config/zenvfx/daemon.pid
```
