#!/bin/bash
# 腾讯云企业网盘 TCED Skill 环境检查脚本
# 用法:
#   setup.sh --check       检查环境状态和 tced-mcp 可用性

set -e

# ========== 配置 ==========

# Skill 最新版下载地址（发布后替换为实际地址）
# 支持：npm 包附件、GitHub Release、COS 等
SKILL_DOWNLOAD_URL="https://registry.npmjs.org/tced-mcp/-/tced-mcp-latest.tgz"
SKILL_VERSION_CHECK_URL=""  # 可选：版本检查 API

# 颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }
warn() { echo -e "${YELLOW}!${NC} $1"; }

# ========== 检查函数 ==========

check_node() {
  if command -v node &>/dev/null; then
    local ver
    ver=$(node --version)
    local major
    major=$(echo "$ver" | sed 's/v//' | cut -d'.' -f1)
    if [ "$major" -ge 18 ]; then
      ok "Node.js $ver (>= v18 ✓)"
      return 0
    else
      fail "Node.js $ver (需要 >= v18)"
      return 1
    fi
  else
    fail "Node.js 未安装"
    return 1
  fi
}

check_npm() {
  if command -v npm &>/dev/null; then
    ok "npm $(npm --version)"
    return 0
  else
    fail "npm 未安装"
    return 1
  fi
}

check_npx() {
  if command -v npx &>/dev/null; then
    ok "npx 可用"
    return 0
  else
    fail "npx 不可用"
    return 1
  fi
}

check_tced_mcp_package() {
  # 检查 tced-mcp 是否可从 npm 获取
  if npm view tced-mcp version &>/dev/null 2>&1; then
    local ver
    ver=$(npm view tced-mcp version 2>/dev/null)
    ok "tced-mcp v${ver} 已发布到 npm"
    return 0
  else
    fail "tced-mcp 未在 npm 上找到"
    return 1
  fi
}

check_tced_mcp_global() {
  # 检查是否已全局安装
  if command -v tced-mcp &>/dev/null; then
    ok "tced-mcp 已全局安装"
    return 0
  else
    warn "tced-mcp 未全局安装（可通过 npx 直接运行，无需全局安装）"
    return 0
  fi
}

check_gui_environment() {
  # macOS 始终有桌面环境
  if [[ "$OSTYPE" == "darwin"* ]]; then
    ok "macOS 桌面环境"
    return 0
  fi
  # Windows (Git Bash / MSYS / Cygwin)
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    ok "Windows 桌面环境"
    return 0
  fi
  # WSL 环境（可通过 wslview 唤起 Windows 浏览器）
  if grep -qi microsoft /proc/version 2>/dev/null; then
    ok "WSL 环境（可通过 wslview 唤起浏览器）"
    return 0
  fi
  # Linux: 检查 DISPLAY（X11）或 WAYLAND_DISPLAY
  if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
    ok "Linux 桌面环境 (DISPLAY=${DISPLAY:-$WAYLAND_DISPLAY})"
    return 0
  fi
  # 未检测到图形界面
  fail "未检测到图形界面环境（Headless 服务器）"
  echo "    tced-mcp 需要唤起浏览器完成 OAuth2 授权登录，不支持无界面服务器。"
  echo "    请在有桌面环境的机器上使用（macOS / Windows / Linux 桌面 / WSL）。"
  return 1
}

check_env_vars() {
  if [ -n "$TCED_PAN_DOMAIN" ]; then
    ok "TCED_PAN_DOMAIN = $TCED_PAN_DOMAIN"
  else
    warn "TCED_PAN_DOMAIN 未设置（使用默认 https://pan.tencent.com）"
  fi
  if [ -n "$TCED_BASE_PATH" ]; then
    ok "TCED_BASE_PATH = $TCED_BASE_PATH"
  else
    warn "TCED_BASE_PATH 未设置（使用默认 https://api.tencentsmh.cn）"
  fi
  return 0
}

# ========== 检查模式 ==========

do_check() {
  echo "=== 腾讯云企业网盘 TCED Skill 环境检查 ==="
  echo ""
  echo "--- 基础环境 ---"
  check_gui_environment || true
  check_node || true
  check_npm || true
  check_npx || true
  echo ""
  echo "--- tced-mcp ---"
  check_tced_mcp_package || true
  check_tced_mcp_global || true
  echo ""
  echo "--- 环境变量（可选） ---"
  check_env_vars || true
  echo ""
  echo "--- MCP 客户端配置 ---"
  echo ""
  echo "将以下配置添加到你的 MCP 客户端配置文件（mcp.json）中："
  echo ""
  cat <<'EOF'
{
  "mcpServers": {
    "tced-mcp": {
      "command": "npx",
      "args": ["-y", "tced-mcp@1.0.1"],
      "env": {
        "TCED_PAN_DOMAIN": "https://pan.tencent.com",
        "TCED_BASE_PATH": "https://api.tencentsmh.cn"
      }
    }
  }
}
EOF
  echo ""
  echo "安全建议: 建议使用锁定版本号，升级前查看 npm 包变更记录"
  echo "  https://www.npmjs.com/package/tced-mcp"
  echo ""
  echo "然后使用 MCP 工具调用 login 进行 OAuth2 授权即可开始使用。"
}

# ========== 更新 MCP 缓存 ==========

do_update_mcp() {
  echo "=== 更新 tced-mcp ==="
  echo ""

  # 1. 检查 npm 上最新版本
  echo "--- 检查最新版本 ---"
  local latest_ver
  latest_ver=$(npm view tced-mcp version 2>/dev/null || echo "unknown")
  echo "npm 最新版本: tced-mcp@${latest_ver}"

  # 2. 清除 npx 缓存
  echo ""
  echo "--- 清除 npx 缓存 ---"
  npm cache clean --force 2>/dev/null && ok "npm 缓存已清除" || warn "缓存清除失败（不影响使用）"

  # 3. 检查本地认证文件是否存在（不读取内容）
  echo ""
  echo "--- 检查本地配置 ---"
  local auth_file="$HOME/.tced-mcp/auth.json"
  if [ -f "$auth_file" ]; then
    ok "本地认证文件存在: ~/.tced-mcp/auth.json"
    echo "  提示: 域名配置以 mcp.json 中的 env 字段为准"
  else
    warn "本地认证文件不存在（首次登录后会自动创建）"
  fi

  echo ""
  echo "--- 推荐的 mcp.json 配置 ---"
  echo ""
  echo "将版本号更新为最新版本后刷新 MCP 连接："
  echo ""
  cat <<EOF
{
  "mcpServers": {
    "tced-mcp": {
      "command": "npx",
      "args": ["-y", "tced-mcp@${latest_ver}"],
      "env": {
        "TCED_PAN_DOMAIN": "https://pan.tencent.com",
        "TCED_BASE_PATH": "https://api.tencentsmh.cn"
      }
    }
  }
}
EOF
  echo ""
  echo "安全建议: 升级前请查看 npm 包页面确认变更内容"
  echo "  https://www.npmjs.com/package/tced-mcp"
  echo ""
  ok "更新完成！请刷新 MCP 连接使其生效。"
}

# ========== 主入口 ==========

case "$1" in
  --check|--check-only)
    do_check
    ;;
  --update-mcp)
    do_update_mcp
    ;;
  *)
    echo "腾讯云企业网盘 TCED Skill 工具"
    echo ""
    echo "用法:"
    echo "  $0 --check         检查环境状态和 tced-mcp 可用性"
    echo "  $0 --update-mcp    更新 tced-mcp（清除缓存、检查配置）"
    echo ""
    echo "tced-mcp 已发布到 npm，在 MCP 客户端配置中添加以下配置即可："
    echo ""
    cat <<'EOF'
{
  "mcpServers": {
    "tced-mcp": {
      "command": "npx",
      "args": ["-y", "tced-mcp@1.0.1"],
      "env": {
        "TCED_PAN_DOMAIN": "https://pan.tencent.com",
        "TCED_BASE_PATH": "https://api.tencentsmh.cn"
      }
    }
  }
}
EOF
    echo ""
    ;;
esac
