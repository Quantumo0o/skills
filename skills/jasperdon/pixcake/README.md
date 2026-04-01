# pixcake-skills

本地 PixCake skill 包，供 OpenClaw / 龙虾直接读取。

当前只暴露一个公开 skill：`pixcake`。  
当前只覆盖三条工作流：

- 项目管理
- 预设修图
- 导出任务

运行时统一通过：

```bash
node ./scripts/pixcake_bridge.js
```

不依赖 `mcporter`、Python 或 `openclaw.json`。

## Runtime Requirements

| Requirement | Value |
|---|---|
| Supported OS | macOS, Windows |
| PixCake client | `9.0.0` or newer |
| Local runtime | `node` |
| Local app state | PixCake desktop client installed and running |
| Local bridge | `pixcake-mcp-bridge` discoverable by the bundled runner |

bridge 自动发现来源：

- macOS：运行中的 PixCake 进程、`/Applications`、`~/Applications`
- Windows：运行中的 PixCake 进程路径、注册表安装位置
- Fallback：`PATH` 中的 `pixcake-mcp-bridge`

## Supported Surface

| Domain | Tools | Notes |
|---|---|---|
| Projects | `get_project_list`, `create_projects`, `import_images_to_projects` | 创建项目、查看项目、导入图片 |
| Images | `get_project_images` | 读取项目图片 |
| Retouch | `get_preset_suit_list`, `apply_preset_suit` | 仅支持预设修图 |
| Export | `export_images` | 仅提交导出任务，异步语义 |

## Out Of Scope

当前不支持：

- 联机拍摄
- AI 挑图
- AI 修图
- AI 追色
- 滤镜 / 换背景 / 去路人
- 智能裁剪

## Quick Start

1. 放到本地 skills 目录：

```bash
~/.openclaw/skills/pixcake-skills
```

2. 确认环境满足要求：

- PixCake desktop client 已安装
- PixCake 客户端版本为 `9.0.0` 或更高
- PixCake 客户端已启动
- agent 运行环境可用 `node`

3. 检查 bridge：

```bash
node ./scripts/pixcake_bridge.js doctor --json
```

4. 查看可用工具：

```bash
node ./scripts/pixcake_bridge.js list --json
```

5. 冒烟测试：

```bash
node ./scripts/pixcake_bridge.js call get_project_list --args '{"limit":5,"offset":0}' --json
```

## Compatibility Policy

以下情况优先按客户端版本不匹配处理：

- PixCake app 已运行且 bridge 已找到，但 socket / pipe 无法建立连接
- `doctor` 迟迟无法进入 `ready=true`
- `list` 缺少当前工作流必需工具
- `call` 返回 `tool not found`、`unknown tool` 或 `method not found`

处理顺序：

1. 提示用户升级到 PixCake `9.0.0` 或更高版本
2. 只有用户明确要求时才重试一次
3. 仍无法处理时，引导联系工作人员或客服支持

## Package Layout

```text
pixcake-skills/
├── SKILL.md
├── README.md
├── manifest.json
├── references/
│   ├── capabilities.md
│   ├── compatibility.md
│   ├── export.md
│   ├── projects.md
│   ├── response-policy.md
│   ├── retouch.md
│   └── runtime.md
└── scripts/
    └── pixcake_bridge.js
```
