---
name: agent-factory
description: 创建新的 OpenClaw Agent 并自动配置飞书机器人。当用户说"帮我创建 Agent"、"新建机器人"、"添加新 agent"、"配置新机器人"时触发。用户提供：agent 名称、飞书 appId、appSecret、角色定位。执行完毕后汇报结果。
---

# agent-factory

自动创建新 OpenClaw Agent 并绑定飞书机器人。

## 输入参数

用户需提供：

| 参数 | 说明 | 示例 |
|------|------|------|
| `name` | Agent 名称（英文，无空格） | `baikexia` |
| `displayName` | 显示名称 | `百科虾` |
| `appId` | 飞书机器人 App ID | `cli_xxx` |
| `appSecret` | 飞书机器人 Secret | `xxx` |
| `identity` | 角色定位描述 | `蜗牛公司问答助手` |
| `soul` | 行为准则（可选） | `只答知识库有的问题` |

## 执行流程

### Step 1: 验证凭证

调用飞书 API 验证 appId/appSecret：

```powershell
$body = @{
  app_id = $appId
  app_secret = $appSecret
} | ConvertTo-Json

$resp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"

if ($resp.code -ne 0) { throw "凭证无效：$($resp.msg)" }
```

### Step 2: 创建 Agent

```powershell
openclaw agents add $name --workspace "~/.openclaw/workspace-$name"
```

### Step 3: 配置飞书账号

读取当前配置，追加新账号：

```powershell
$config = Get-Content "$env:USERPROFILE\.openclaw\openclaw.json" | ConvertFrom-Json
$config.channels.feishu.accounts | Add-Member -NotePropertyName $name -NotePropertyValue @{
  appId = $appId
  appSecret = $appSecret
  name = $displayName
}
```

### Step 4: 配置路由规则

追加 binding：

```powershell
$binding = @{
  type = "route"
  agentId = $name
  match = @{
    channel = "feishu"
    accountId = $name
  }
}
$config.bindings += $binding
```

### Step 5: 写入配置文件

```powershell
$config | ConvertTo-Json -Depth 10 | Set-Content "$env:USERPROFILE\.openclaw\openclaw.json"
```

### Step 6: 创建角色文件

在 `~/.openclaw/workspace-{name}/` 下创建：

- `IDENTITY.md` — 名字、emoji、定位
- `SOUL.md` — 行为准则（用户提供的 soul 或默认模板）
- `AGENTS.md` — 工作手册（可选）
- `USER.md` — 用户占位符

### Step 7: 安装 Skill（如有指定）

用户指定了 `--skill xxx` 时：

```powershell
openclaw skills install $skillName
```

### Step 8: 开启工具权限

```powershell
openclaw config set channels.feishu.tools.wiki true
openclaw config set channels.feishu.tools.doc true
openclaw config set channels.feishu.tools.drive true
```

### Step 9: 重启网关

```powershell
openclaw gateway restart
```

## 完整脚本

提供两个版本：**Windows (PowerShell)** 和 **Linux/macOS (Bash + jq)**。

### Linux / macOS (Bash)

将以下脚本保存为 `create-agent.sh`，执行 `chmod +x create-agent.sh` 后运行：

```bash
#!/usr/bin/env bash
# create-agent.sh — Linux/macOS 版（需安装 jq）
set -euo pipefail

# ---------- 参数 ----------
while [[ $# -gt 0 ]]; do
  case $1 in
    --name) NAME="$2"; shift 2 ;;
    --display-name) DISPLAY_NAME="$2"; shift 2 ;;
    --app-id) APP_ID="$2"; shift 2 ;;
    --app-secret) APP_SECRET="$2"; shift 2 ;;
    --identity) IDENTITY="$2"; shift 2 ;;
    --soul) SOUL="$2"; shift 2 ;;
    *) shift ;;
  esac
done

[[ -z "${NAME:-}" ]] && echo "错误：缺少 --name" && exit 1
[[ -z "${DISPLAY_NAME:-}" ]] && echo "错误：缺少 --display-name" && exit 1
[[ -z "${APP_ID:-}" ]] && echo "错误：缺少 --app-id" && exit 1
[[ -z "${APP_SECRET:-}" ]] && echo "错误：缺少 --app-secret" && exit 1
[[ -z "${IDENTITY:-}" ]] && echo "错误：缺少 --identity" && exit 1
SOUL="${SOUL:-}"
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
CONFIG_FILE="$OPENCLAW_DIR/openclaw.json"
BACKUP_FILE="$OPENCLAW_DIR/openclaw.json.bak"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace-$NAME"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# ---------- 颜色 ----------
RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'

# ============ Step 1: Validate Feishu credentials ============
echo -e "${CYAN}[1/8]${NC} 验证飞书凭证..."

RESP=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "$(jq -n --arg id "$APP_ID" --arg secret "$APP_SECRET" '{app_id: $id, app_secret: $secret}')" \
  --max-time 10) || true

CODE=$(echo "$RESP" | jq -r '.code // 99')
if [[ "$CODE" != "0" ]]; then
  MSG=$(echo "$RESP" | jq -r '.msg // "unknown error"')
  echo -e "${RED}错误：凭证无效：$MSG (code: $CODE)${NC}" >&2
  exit 1
fi
BOT_NAME=$(echo "$RESP" | jq -r '.app // "?"')
echo -e "  ${GREEN}✓${NC} 凭证有效，bot name: $BOT_NAME"

# ============ Step 2: Create Agent ============
echo -e "${CYAN}[2/8]${NC} 创建 Agent '$NAME'..."
openclaw agents add "$NAME" --workspace "$WORKSPACE_DIR" 2>&1 || {
  if ! openclaw agents add "$NAME" --workspace "$WORKSPACE_DIR" 2>&1 | grep -q "already exists"; then
    echo -e "${RED}错误：创建 Agent 失败${NC}" >&2
    exit 1
  fi
}
echo -e "  ${GREEN}✓${NC} Agent 创建完成"

# ============ Step 3: Read & backup config ============
echo -e "${CYAN}[3/8]${NC} 读取当前配置..."
cp "$CONFIG_FILE" "$BACKUP_FILE"
CONFIG=$(cat "$CONFIG_FILE")
echo -e "  ${GREEN}✓${NC} 配置已备份到 $BACKUP_FILE"

# ============ Step 4: Add Feishu account ============
echo -e "${CYAN}[4/8]${NC} 配置飞书账号..."

# Ensure accounts object exists
if ! echo "$CONFIG" | jq -e '.channels.feishu.accounts' >/dev/null 2>&1; then
  CONFIG=$(echo "$CONFIG" | jq '.channels.feishu.accounts = {}')
fi
CONFIG=$(echo "$CONFIG" | jq \
  --arg n "$NAME" \
  --arg id "$APP_ID" \
  --arg secret "$APP_SECRET" \
  --arg name "$DISPLAY_NAME" \
  '.channels.feishu.accounts[$n] = {appId: $id, appSecret: $secret, name: $name}')
echo -e "  ${GREEN}✓${NC} 账号 '$DISPLAY_NAME' 已添加"

# ============ Step 5: Add binding rule ============
echo -e "${CYAN}[5/8]${NC} 配置路由规则..."

BINDING=$(jq -n \
  --arg agentId "$NAME" \
  --arg accountId "$NAME" \
  '{type: "route", agentId: $agentId, match: {channel: "feishu", accountId: $accountId}}')

EXISTING=$(echo "$CONFIG" | jq \
  --arg agentId "$NAME" \
  --arg accountId "$NAME" \
  '.bindings[]? | select(.agentId == $agentId and .match.accountId == $accountId)')

if [[ "$EXISTING" == "null" || "$EXISTING" == "" ]]; then
  CONFIG=$(echo "$CONFIG" | jq --argjson binding "$BINDING" '.bindings += [$binding]')
  echo -e "  ${GREEN}✓${NC} 路由规则已添加"
else
  echo -e "  ${GREEN}✓${NC} 路由规则已存在，跳过"
fi

# ============ Step 6: Write config ============
echo -e "${CYAN}[6/8]${NC} 保存配置..."
echo "$CONFIG" | jq '.' > "$CONFIG_FILE"
echo -e "  ${GREEN}✓${NC} 配置已保存"

# ============ Step 7: Create identity files ============
echo -e "${CYAN}[7/8]${NC} 创建角色文件..."
mkdir -p "$WORKSPACE_DIR"

# IDENTITY.md
cat > "$WORKSPACE_DIR/IDENTITY.md" <<EOF
# IDENTITY.md - $DISPLAY_NAME

- **Name:** $DISPLAY_NAME
- **Creature:** $IDENTITY
- **Emoji:** 🦐
- **Avatar:** _(待定)_

---

由 agent-factory skill 于 $TIMESTAMP 自动创建。
EOF

# SOUL.md
if [[ -n "$SOUL" ]]; then
  cat > "$WORKSPACE_DIR/SOUL.md" <<EOF
# SOUL.md - $DISPLAY_NAME 的灵魂

$SOUL

---

由 agent-factory skill 于 $TIMESTAMP 自动创建。
EOF
else
  cat > "$WORKSPACE_DIR/SOUL.md" <<EOF
# SOUL.md - $DISPLAY_NAME 的灵魂

## 我是谁

我是**$DISPLAY_NAME**，$IDENTITY。

## 行事准则

- 全力帮助用户
- 不知道就说不知道，不编造
- 只做本职工作范围内的事

---

由 agent-factory skill 于 $TIMESTAMP 自动创建。
EOF
fi

# AGENTS.md
cat > "$WORKSPACE_DIR/AGENTS.md" <<EOF
# AGENTS.md - $DISPLAY_NAME 工作手册

## 角色

$IDENTITY

## 注意事项

- 保持专注，不越界
- 遇到不确定的问题，告知用户

---

由 agent-factory skill 于 $TIMESTAMP 自动创建。
EOF

# USER.md
cat > "$WORKSPACE_DIR/USER.md" <<EOF
# USER.md

- **Name:** _(待填写)_
- **What to call them:** _(待填写)_

## Context

_(随着对话积累，持续更新这里。)_
EOF

echo -e "  ${GREEN}✓${NC} IDENTITY.md, SOUL.md, AGENTS.md, USER.md 已创建"

# ============ Step 8: Restart gateway ============
echo -e "${CYAN}[8/8]${NC} 重启网关..."
openclaw gateway restart 2>/dev/null || true
sleep 3
echo -e "  ${GREEN}✓${NC} 网关重启请求已发送"

# ============ Done ============
echo ""
echo -e "${GREEN}✅ Agent '$DISPLAY_NAME' 创建完成！${NC}"
echo ""
echo -e "${CYAN}配置汇总：${NC}"
echo "  Agent 名称: $NAME"
echo "  显示名称: $DISPLAY_NAME"
echo "  飞书 App ID: $APP_ID"
echo "  Workspace: $WORKSPACE_DIR"
echo "  路由: feishu:$NAME -> $NAME agent"
echo ""
echo -e "${YELLOW}下一步：在飞书里找到 '$DISPLAY_NAME' 机器人，向它发消息测试。${NC}"
```

### Windows (PowerShell)

将以下脚本保存为 `create-agent.ps1`，直接执行即可完成全部流程：

```powershell
#Requires -Version 5.1
param(
    [Parameter(Mandatory=$true)]
    [string]$Name,

    [Parameter(Mandatory=$true)]
    [string]$DisplayName,

    [Parameter(Mandatory=$true)]
    [string]$AppId,

    [Parameter(Mandatory=$true)]
    [string]$AppSecret,

    [Parameter(Mandatory=$true)]
    [string]$Identity,

    [string]$Soul = "",

    [string]$Skill = ""
)

$ErrorActionPreference = "Stop"
$SkillDir = Split-Path -Parent $PSScriptRoot
$RefsDir = Join-Path $SkillDir "references"

# ============ Step 1: Validate Feishu credentials ============
Write-Host "[1/8] 验证飞书凭证..."

$body = @{
    app_id = $AppId
    app_secret = $AppSecret
} | ConvertTo-Json -Compress

try {
    $resp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" `
        -Method POST `
        -Body $body `
        -ContentType "application/json" `
        -TimeoutSec 10
} catch {
    Write-Error "无法连接飞书服务器：$_"
    exit 1
}

if ($resp.code -ne 0) {
    Write-Error "凭证无效：$($resp.msg) (code: $($resp.code))"
    exit 1
}
Write-Host "  ✓ 凭证有效，bot name: $($resp.app)"

# ============ Step 2: Create Agent ============
Write-Host "[2/8] 创建 Agent '$Name'..."

$agentCmd = "openclaw agents add $Name --workspace `"$env:USERPROFILE\.openclaw\workspace-$Name`""
$addResult = Invoke-Expression $agentCmd 2>&1
if ($LASTEXITCODE -ne 0 -and $addResult -notmatch "already exists") {
    Write-Error "创建 Agent 失败：$addResult"
    exit 1
}
Write-Host "  ✓ Agent 创建完成"

# ============ Step 3: Read current config ============
Write-Host "[3/8] 读取当前配置..."

$configPath = "$env:USERPROFILE\.openclaw\openclaw.json"
$backupPath = "$env:USERPROFILE\.openclaw\openclaw.json.bak"
Copy-Item $configPath $backupPath -Force

$config = Get-Content $configPath -Raw | ConvertFrom-Json
Write-Host "  ✓ 配置已备份到 $backupPath"

# ============ Step 4: Add Feishu account ============
Write-Host "[4/8] 配置飞书账号..."

if (-not $config.channels.feishu.accounts) {
    $config.channels | Add-Member -NotePropertyName "accounts" -NotePropertyValue ([ordered]@{}) -Force
}
$config.channels.feishu.accounts | Add-Member -NotePropertyName $Name -NotePropertyValue ([ordered]@{
    appId = $AppId
    appSecret = $AppSecret
    name = $DisplayName
}) -Force

Write-Host "  ✓ 账号 '$DisplayName' 已添加"

# ============ Step 5: Add binding rule ============
Write-Host "[5/8] 配置路由规则..."

$newBinding = @{
    type = "route"
    agentId = $Name
    match = @{
        channel = "feishu"
        accountId = $Name
    }
}

$existingBinding = $config.bindings | Where-Object {
    $_.agentId -eq $Name -and $_.match.accountId -eq $Name
}
if (-not $existingBinding) {
    $config.bindings += $newBinding
    Write-Host "  ✓ 路由规则已添加"
} else {
    Write-Host "  ✓ 路由规则已存在，跳过"
}

# ============ Step 6: Write config ============
Write-Host "[6/8] 保存配置..."
$newConfig = $config | ConvertTo-Json -Depth 20 -Compress
$config = $newConfig | ConvertFrom-Json | ConvertTo-Json -Depth 20 -Compress
Set-Content -Path $configPath -Value ($config | ConvertFrom-Json | ConvertTo-Json -Depth 20) -NoNewline -Encoding UTF8
Write-Host "  ✓ 配置已保存"

# ============ Step 7: Create identity files ============
Write-Host "[7/8] 创建角色文件..."

$workspaceDir = "$env:USERPROFILE\.openclaw\workspace-$Name"
if (-not (Test-Path $workspaceDir)) {
    New-Item -ItemType Directory -Path $workspaceDir -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"

# IDENTITY.md
$identityContent = @"
# IDENTITY.md - $DisplayName

- **Name:** $DisplayName
- **Creature:** $Identity
- **Emoji:** 🦐
- **Avatar:** _(待定)_

---

由 agent-factory skill 于 $timestamp 自动创建。
"@

# SOUL.md
if ($Soul -ne "") {
    $soulContent = @"
# SOUL.md - $DisplayName 的灵魂

$Soul

---

由 agent-factory skill 于 $timestamp 自动创建。
"@
} else {
    $soulContent = @"
# SOUL.md - $DisplayName 的灵魂

## 我是谁

我是**$DisplayName**，$Identity。

## 行事准则

- 全力帮助用户
- 不知道就说不知道，不编造
- 只做本职工作范围内的事

---

由 agent-factory skill 于 $timestamp 自动创建。
"@
}

# AGENTS.md
$agentsContent = @"
# AGENTS.md - $DisplayName 工作手册

## 角色

$Identity

## 注意事项

- 保持专注，不越界
- 遇到不确定的问题，告知用户

---

由 agent-factory skill 于 $timestamp 自动创建。
"@

# USER.md
$userContent = @"
# USER.md

- **Name:** _(待填写)_
- **What to call them:** _(待填写)_

## Context

_(随着对话积累，持续更新这里。)_
"@

Set-Content -Path (Join-Path $workspaceDir "IDENTITY.md") -Value $identityContent -Encoding UTF8
Set-Content -Path (Join-Path $workspaceDir "SOUL.md") -Value $soulContent -Encoding UTF8
Set-Content -Path (Join-Path $workspaceDir "AGENTS.md") -Value $agentsContent -Encoding UTF8
Set-Content -Path (Join-Path $workspaceDir "USER.md") -Value $userContent -Encoding UTF8

Write-Host "  ✓ IDENTITY.md, SOUL.md, AGENTS.md, USER.md 已创建"

# ============ Step 8: Restart gateway ============
Write-Host "[8/8] 重启网关..."
openclaw gateway restart 2>&1 | Out-Null
Start-Sleep -Seconds 3
Write-Host "  ✓ 网关重启请求已发送"

# ============ Done ============
Write-Host ""
Write-Host "✅ Agent '$DisplayName' 创建完成！" -ForegroundColor Green
Write-Host ""
Write-Host "配置汇总：" -ForegroundColor Cyan
Write-Host "  Agent 名称: $Name"
Write-Host "  显示名称: $DisplayName"
Write-Host "  飞书 App ID: $AppId"
Write-Host "  Workspace: $workspaceDir"
Write-Host "  路由: feishu:$Name -> $Name agent"
Write-Host ""
Write-Host "下一步：在飞书里找到 '$DisplayName' 机器人，向它发消息测试。" -ForegroundColor Yellow
```

## 执行示例

用户说：
> 帮我创建百科虾，AppID: cli_xxx，Secret: xxx，名字是百科虾，定位是蜗牛公司问答助手

**Linux / macOS：**
```bash
chmod +x create-agent.sh
./create-agent.sh \
  --name "baikexia" \
  --display-name "百科虾" \
  --app-id "cli_xxx" \
  --app-secret "xxx" \
  --identity "蜗牛公司问答助手"
```

**Windows：**
```powershell
.\create-agent.ps1 -Name "baikexia" -DisplayName "百科虾" -AppId "cli_xxx" -AppSecret "xxx" -Identity "蜗牛公司问答助手"
```

## 错误处理

| 错误 | 处理 |
|------|------|
| 凭证无效 | 抛出 `credentials_invalid`，告知用户检查 appId/appSecret |
| Agent 已存在 | 跳过创建，保留现有配置 |
| 配置文件写入失败 | 抛出 `config_write_failed`，保留备份 |
| 路由规则冲突 | 跳过重复规则，继续执行 |

## 注意事项

- 所有 PowerShell 脚本使用 UTF-8 BOM 编码
- 配置文件写入前自动备份到 `openclaw.json.bak`
- Agent 名称只能包含字母、数字、连字符
