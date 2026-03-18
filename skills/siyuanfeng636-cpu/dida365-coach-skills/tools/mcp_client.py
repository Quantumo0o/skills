"""处理滴答清单 MCP 检测与设置文案。"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

DEFAULT_SERVER_NAME = "dida365"
DEFAULT_MCP_URL = "https://mcp.dida365.com"


def _resolve_mcp_config_path() -> Path:
    override = os.environ.get("DIDA_COACH_MCP_CONFIG_PATH")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".claude" / "mcp.json"


def _load_mcp_config(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict):
        return data
    return {}


def _find_server(config: Dict[str, Any], server_name: str) -> Optional[Dict[str, Any]]:
    for key in ("mcpServers", "servers"):
        server_map = config.get(key)
        if isinstance(server_map, dict) and isinstance(server_map.get(server_name), dict):
            return server_map[server_name]
    return None


def build_setup_guide() -> str:
    """返回 MCP 未配置时的引导文案。"""

    return (
        "👋 欢迎使用 Dida Coach！\n\n"
        "检测到你还没有连接滴答清单，请先完成下面两步：\n\n"
        "1. 运行：claude mcp add --transport http dida365 https://mcp.dida365.com\n"
        "2. 在客户端内运行：/mcp\n"
        "3. 按提示完成滴答清单授权\n\n"
        "完成后告诉我“已连接”，我会继续帮你拆目标、排时间盒和做复盘。"
    )


def check_mcp_configured(server_name: str = DEFAULT_SERVER_NAME) -> Tuple[bool, str]:
    """
    检查滴答清单 MCP 是否已配置。

    返回:
        (是否已配置, 文案)
    """

    config_path = _resolve_mcp_config_path()
    if not config_path.exists():
        return False, build_setup_guide()

    try:
        config = _load_mcp_config(config_path)
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"❌ 读取 MCP 配置失败：{exc}"

    server = _find_server(config, server_name)
    if not server:
        return False, (
            "👋 检测到已有 MCP 配置文件，但里面没有 dida365。\n\n"
            "请运行：claude mcp add --transport http dida365 https://mcp.dida365.com\n"
            "然后运行 /mcp 完成授权。"
        )

    server_url = str(server.get("url") or "")
    if server_url and DEFAULT_MCP_URL not in server_url:
        return True, f"✅ 已检测到 {server_name} MCP（URL: {server_url}）"

    return True, "✅ 滴答清单 MCP 已配置"


def get_mcp_setup_command(server_name: str = DEFAULT_SERVER_NAME) -> str:
    """返回标准 MCP 添加命令。"""

    return f"claude mcp add --transport http {server_name} {DEFAULT_MCP_URL}"


def get_mcp_server_config(server_name: str = DEFAULT_SERVER_NAME) -> Optional[Dict[str, Any]]:
    """返回当前 dida365 MCP 配置，若不存在则返回 None。"""

    config_path = _resolve_mcp_config_path()
    if not config_path.exists():
        return None

    try:
        config = _load_mcp_config(config_path)
    except (OSError, json.JSONDecodeError):
        return None

    return _find_server(config, server_name)
