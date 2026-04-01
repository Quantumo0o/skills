# Runtime

## Entry Point

所有真实 PixCake 调用统一通过：

```bash
node ./scripts/pixcake_bridge.js
```

## Execution Flow

每次真实调用都按以下顺序执行：

1. `doctor`
2. `list`
3. `call`

不要跳过 `doctor`，也不要在没有 `list` 结果时猜工具名。

## Step 1: `doctor`

```bash
node ./scripts/pixcake_bridge.js doctor --json
```

规则：

- 只有 `ready=true` 才能进入下一步
- `ready=false` 时立即停止
- 如果 app 已运行但仍无法连通，转到 `compatibility.md`

## Step 2: `list`

```bash
node ./scripts/pixcake_bridge.js list --json
```

规则：

- 只从 `list` 返回结果里选择真实工具名
- 工具名还必须同时落在 `capabilities.md` 的工具面内
- 当前场景必需工具缺失时，转到 `compatibility.md`

## Step 3: `call`

```bash
node ./scripts/pixcake_bridge.js call <tool_name> --args '{"key":"value"}' --json
```

规则：

- 只传当前这一步真正需要的字段
- 关键上下文不明确时，先回业务 reference 澄清
- `call` 报工具不存在或方法不存在时，转到 `compatibility.md`

## Discovery Strategy

runtime 已内置以下发现逻辑：

- macOS：扫描正在运行的 PixCake 进程，以及 `/Applications`、`~/Applications` 下名称包含 `pixcake` 的 `.app`
- Windows：优先从正在运行的 PixCake 进程路径推导 bridge，再读取注册表安装位置
- 两个平台最后都回退到 PATH 中的 `pixcake-mcp-bridge`

## Optional Overrides

只有在用户明确需要覆盖自动发现时，才使用：

```bash
PIXCAKE_BRIDGE_CMD=/absolute/path/to/pixcake-mcp-bridge
PIXCAKE_SOCKET_PATH=/custom/socket/or/pipe
PIXCAKE_SKILLS_CONFIG=/absolute/path/to/config.local.json
```

或：

```bash
node ./scripts/pixcake_bridge.js --bridge /absolute/path/to/pixcake-mcp-bridge doctor --json
node ./scripts/pixcake_bridge.js --socket /custom/socket/or/pipe doctor --json
```

## Guardrails

- 不安装依赖
- 不修改系统环境
- 不执行用户拼接的 shell 命令
- 不切换到未知脚本
- 不在失败后做连续试探
