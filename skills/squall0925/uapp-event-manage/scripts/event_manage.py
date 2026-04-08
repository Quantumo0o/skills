#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""uapp-event-manage: 友盟自定义事件管理入口脚本

功能目标：
- 读取 umeng-config.json（支持 --config / UMENG_CONFIG_PATH / 当前目录 / .env）
- 解析应用（支持 --app / --account，含模糊匹配）
- 自动识别平台类型，调用对应API：
  - App类型（Android/iOS/HarmonyOS）：调用 umeng.uapp.event.create
  - 小程序类型（微信/支付宝等）：调用 umeng.umini.batchCreateEvent
- 支持单个事件创建和批量创建（仅小程序）
- 支持命令行JSON字符串和文件读取两种批量输入方式
- 支持可选的创建后验证功能
- 输出：
  - 文本模式：表格/摘要
  - JSON 模式：结构化数据
"""

import argparse
import json
import os
import re
import sys
from datetime import date, timedelta
from urllib.parse import quote

# -------------------------
# 平台类型常量
# -------------------------

APP_PLATFORMS = ["Android", "iOS", "HarmonyOS"]
MINI_PROGRAM_PLATFORMS = ["微信小程序", "支付宝小程序", "百度小程序", "字节跳动小程序", "QQ小程序", "H5", "小游戏"]

# -------------------------
# 参数校验正则表达式
# -------------------------

# eventName: 允许英文、数字、下划线
EVENT_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]+$')

# eventDisplayName: 允许中文、英文、数字、下划线（不允许特殊符号 ?/.\<>）
DISPLAY_NAME_PATTERN = re.compile(r'^[\u4e00-\u9fa5a-zA-Z0-9_]+$')

# 不允许的特殊符号
FORBIDDEN_CHARS = set('?/.\\<>')


# -------------------------
# 参数校验函数
# -------------------------


def validate_event_name(event_name: str) -> tuple[bool, str]:
    """校验事件名称格式。
    
    规则：允许英文字母、数字、下划线，不允许特殊符号 ?/.\<>
    
    返回：(是否有效, 错误信息)
    """
    if not event_name:
        return False, "事件名称不能为空"
    
    if not EVENT_NAME_PATTERN.match(event_name):
        return False, "事件名称只能包含英文字母、数字和下划线，不允许特殊符号 ?/.\\<>"
    
    return True, ""


def validate_display_name(display_name: str) -> tuple[bool, str]:
    """校验显示名称格式。
    
    规则：允许中文、英文、数字、下划线，不允许特殊符号 ?/.\<>
    
    返回：(是否有效, 错误信息)
    """
    if not display_name:
        return False, "显示名称不能为空"
    
    # 检查是否包含禁止字符
    for char in FORBIDDEN_CHARS:
        if char in display_name:
            return False, "显示名称只能包含中文、英文、数字和下划线，不允许特殊符号 ?/.\\<>"
    
    # 检查是否只包含允许的字符
    if not DISPLAY_NAME_PATTERN.match(display_name):
        return False, "显示名称只能包含中文、英文、数字和下划线，不允许特殊符号 ?/.\\<>"
    
    return True, ""


# -------------------------
# 工具函数：路径 & 配置加载
# -------------------------


def resolve_workspace_root() -> str:
    """解析 workspace 根目录。"""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    workspace = os.path.dirname(skill_dir)
    return workspace


def load_env_config_path() -> str | None:
    """从环境变量或 .env 中加载 UMENG_CONFIG_PATH。"""
    env_path = os.environ.get("UMENG_CONFIG_PATH")
    if env_path:
        return env_path

    workspace = resolve_workspace_root()
    env_file = os.path.join(workspace, ".env")
    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("UMENG_CONFIG_PATH="):
                        return line.split("UMENG_CONFIG_PATH=", 1)[1].strip()
        except Exception:
            pass
    return None


def resolve_config_path(cli_config: str | None) -> str:
    """解析配置文件路径。"""
    if cli_config:
        return cli_config

    env_config = load_env_config_path()
    if env_config:
        return env_config

    workspace = resolve_workspace_root()
    default_path = os.path.join(workspace, "umeng-config.json")
    return default_path


def load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------
# 应用解析（含模糊匹配）
# -------------------------


def normalize_app_name(name: str) -> str:
    """去除半角/全角空格，用于模糊匹配。"""
    return name.replace(" ", "").replace("\u3000", "")


def is_app_platform(platform: str) -> bool:
    """判断是否为App类型平台。"""
    return platform in APP_PLATFORMS


def is_mini_program_platform(platform: str) -> bool:
    """判断是否为小程序类型平台。"""
    return platform in MINI_PROGRAM_PLATFORMS


def find_app_by_name(config: dict, app_name: str, account_id: str | None = None):
    """按应用名称查找应用配置，支持精确匹配 + 去空格模糊匹配。"""
    matches = []
    normalized_input = normalize_app_name(app_name)

    for account in config.get("accounts", []):
        if account_id and account.get("id") != account_id:
            continue
        for app in account.get("apps", []):
            name = app.get("name", "")
            if name == app_name or normalize_app_name(name) == normalized_input:
                matches.append({
                    "account_id": account.get("id"),
                    "apiKey": account.get("apiKey"),
                    "apiSecurity": account.get("apiSecurity"),
                    "app": app,
                })

    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]
    return matches


def resolve_app(config: dict, app_name: str | None, account_id: str | None) -> dict:
    """解析最终使用的应用配置。"""
    if app_name:
        result = find_app_by_name(config, app_name, account_id=account_id)
        if not result:
            available = []
            for account in config.get("accounts", []):
                for app in account.get("apps", []):
                    available.append(app.get("name", ""))
            raise ValueError(f"未找到名称匹配的应用: {app_name}，可用应用: {', '.join(available)}")
        if isinstance(result, list):
            raise ValueError("存在多个同名应用，请通过 --account 进一步限定")
        return result

    raise ValueError("未指定应用，请使用 --app 指定应用名称")


# -------------------------
# Umeng SDK 调用
# -------------------------


def get_sdk_root() -> str:
    """获取当前 skill 内部 SDK 根目录。"""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(skill_dir, "友盟_openapi_python_SDK")


def init_sdk(api_key: str, api_security: str) -> None:
    """初始化 SDK 路径和默认服务器配置。"""
    sdk_root = get_sdk_root()
    if sdk_root not in sys.path:
        sys.path.insert(0, sdk_root)

    import aop
    aop.set_default_server('gateway.open.umeng.com')
    aop.set_default_appinfo(int(api_key), api_security)


# -------------------------
# App事件创建API
# -------------------------


def create_app_event(appkey: str, event_name: str, display_name: str, event_type: str | None = None) -> dict:
    """创建App类型自定义事件。
    
    参数说明：
    - appkey: 应用appkey
    - event_name: 事件名称（英文标识）
    - display_name: 事件显示名称（中文），会自动进行URL编码
    - event_type: 事件类型，"true"=计算事件（数值型），"false"=计数事件（字符串型），None=不传（API默认false）
    
    返回：
    - 成功：{"status": 0, "msg": "ok"}
    - 失败：{"status": 非0, "msg": "错误信息"}
    """
    from aop import api

    req = api.UmengUappEventCreateRequest()
    req.appkey = appkey
    req.eventName = event_name
    # 中文显示名称需要URL编码
    req.eventDisplayName = quote(display_name, safe='')
    
    # eventType为可选参数，只有明确指定时才传入
    if event_type is not None:
        req.eventType = event_type

    resp = req.get_response()
    return resp if isinstance(resp, dict) else {"status": -1, "msg": "Unknown error"}


# -------------------------
# 小程序批量事件创建API
# -------------------------


def batch_create_mini_events(data_source_id: str, event_list: list[dict]) -> dict:
    """批量创建小程序事件。
    
    参数说明：
    - data_source_id: 数据源ID（即appkey）
    - event_list: 事件列表，格式：[{"eventName": "...", "displayName": "..."}, ...]
    
    返回：
    - 成功：{"data": 创建数量, "msg": "SUCCESS", "code": 200, "success": true}
    - 失败：{"msg": "错误信息", "code": 错误码, "success": false}
    """
    from aop import api

    req = api.UmengUminiBatchCreateEventRequest()
    req.dataSourceId = data_source_id
    req.eventList = json.dumps(event_list, ensure_ascii=False)

    resp = req.get_response()
    return resp if isinstance(resp, dict) else {"success": False, "msg": "Unknown error"}


# -------------------------
# 事件列表查询
# -------------------------


def query_event_list_app(appkey: str, page: int = 1, per_page: int = 100) -> dict:
    """查询App类型事件列表。
    
    返回格式：
    {
        "events": [{"name": "...", "displayName": "...}, ...],
        "page": 1,
        "perPage": 100,
        "total": 50
    }
    """
    from aop import api

    today = date.today()
    start = today - timedelta(days=30)
    end = today - timedelta(days=1)

    req = api.UmengUappEventListRequest()
    req.appkey = appkey
    req.startDate = start.strftime("%Y-%m-%d")
    req.endDate = end.strftime("%Y-%m-%d")
    req.page = page
    req.perPage = per_page

    resp = req.get_response()
    if not isinstance(resp, dict):
        return {"events": [], "page": page, "perPage": per_page, "total": 0}

    events = resp.get("eventInfo", []) or resp.get("events", []) or []
    total_pages = resp.get("totalPage", 1) or 1
    current_page = resp.get("page", page) or page

    # 计算总数
    if total_pages > 0:
        if current_page >= total_pages:
            total = (total_pages - 1) * per_page + len(events)
        else:
            total = total_pages * per_page
    else:
        total = len(events)

    return {
        "events": events,
        "page": current_page,
        "perPage": per_page,
        "total": total,
        "totalPages": total_pages,
    }


def query_event_list_mini(data_source_id: str) -> dict:
    """查询小程序类型事件列表。
    
    返回格式：
    {
        "events": [{"eventName": "...", "displayName": "...}, ...],
        "total": 50
    }
    """
    from aop import api

    req = api.UmengUminiGetEventListRequest()
    req.dataSourceId = data_source_id

    resp = req.get_response()
    if not isinstance(resp, dict):
        return {"events": [], "total": 0}

    # 响应结构：{"data": {"data": [...]}} 或 {"data": [...]}
    outer_data = resp.get("data", {})
    if isinstance(outer_data, dict):
        events = outer_data.get("data", [])
    elif isinstance(outer_data, list):
        events = outer_data
    else:
        events = []

    return {
        "events": events,
        "total": len(events),
    }


# -------------------------
# 事件验证（可选）
# -------------------------


def verify_event_exists_app(appkey: str, event_name: str) -> bool:
    """验证App类型事件是否存在。"""
    from aop import api

    today = date.today()
    start = today - timedelta(days=30)
    end = today - timedelta(days=1)

    req = api.UmengUappEventListRequest()
    req.appkey = appkey
    req.startDate = start.strftime("%Y-%m-%d")
    req.endDate = end.strftime("%Y-%m-%d")
    req.page = 1
    req.perPage = 100

    resp = req.get_response()
    if not isinstance(resp, dict):
        return False

    events = resp.get("eventInfo", []) or resp.get("events", []) or []
    for event in events:
        evt_name = event.get("name") or event.get("eventName", "")
        if evt_name == event_name:
            return True
    return False


def verify_event_exists_mini(data_source_id: str, event_name: str) -> bool:
    """验证小程序类型事件是否存在。"""
    from aop import api

    req = api.UmengUminiGetEventListRequest()
    req.dataSourceId = data_source_id

    resp = req.get_response()
    if not isinstance(resp, dict):
        return False

    # 响应结构：{"data": {"data": [...]}} 或 {"data": [...]}
    outer_data = resp.get("data", {})
    if isinstance(outer_data, dict):
        events = outer_data.get("data", [])
    elif isinstance(outer_data, list):
        events = outer_data
    else:
        events = []

    for event in events:
        evt_name = event.get("eventName", "")
        if evt_name == event_name:
            return True
    return False


# -------------------------
# 输出格式化
# -------------------------


def build_create_result_text(event_name: str, display_name: str, platform: str, 
                              success: bool, verified: bool = False, exists: bool = False) -> str:
    """构建单个事件创建结果文本。"""
    if success:
        lines = [f"✓ 事件创建成功"]
        lines.append(f"  事件名称: {event_name}")
        lines.append(f"  显示名称: {display_name}")
        lines.append(f"  平台类型: {platform}")
        if verified:
            status = "已验证存在" if exists else "验证失败（事件可能尚未同步）"
            lines.append(f"  验证状态: {status}")
        return "\n".join(lines)
    else:
        return f"✗ 事件创建失败: {event_name}"


def build_batch_create_result_text(results: list[dict], platform: str) -> str:
    """构建批量事件创建结果文本。"""
    success_count = sum(1 for r in results if r.get("success"))
    fail_count = len(results) - success_count

    lines = []
    lines.append(f"批量事件创建结果（共 {len(results)} 个事件）")
    lines.append("-" * 60)
    lines.append(f"{'序号':<6} {'事件名称':<25} {'显示名称':<20} {'状态'}")
    lines.append("-" * 60)

    for i, r in enumerate(results):
        evt_name = r.get("eventName", "")[:23]
        display = r.get("displayName", "")[:18]
        status = "✓ 成功" if r.get("success") else f"✗ 失败: {r.get('msg', '')[:10]}"
        lines.append(f"{i+1:<6} {evt_name:<25} {display:<20} {status}")

    lines.append("-" * 60)
    lines.append(f"成功: {success_count}，失败: {fail_count}")

    return "\n".join(lines)


def build_event_list_table(result: dict, platform: str) -> str:
    """构建事件列表表格输出。"""
    events = result.get("events", [])
    if not events:
        return "未查询到事件数据。"

    total = result.get("total", len(events))
    page = result.get("page", 1)
    per_page = result.get("perPage", len(events))

    lines = []
    lines.append(f"事件列表（共 {total} 个事件）")
    lines.append("-" * 70)
    lines.append(f"{'序号':<6} {'事件名称':<30} {'显示名称'}")
    lines.append("-" * 70)

    start_idx = (page - 1) * per_page
    for i, event in enumerate(events):
        idx = start_idx + i + 1
        # 兼容App和小程序两种字段名
        evt_name = (event.get("name") or event.get("eventName", ""))[:28]
        display_name = event.get("displayName", "")
        lines.append(f"{idx:<6} {evt_name:<30} {display_name}")

    return "\n".join(lines)


def build_json_output(success: bool, data: dict, message: str = "") -> str:
    """构建 JSON 输出。"""
    output = {
        "success": success,
        "message": message,
        "data": data
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


# -------------------------
# CLI 入口
# -------------------------


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="uapp-event-manage: 友盟自定义事件管理入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 创建单个事件（App类型）
  python3 scripts/event_manage.py --create "purchase_click" --display-name "购买点击" --app "Android_Demo"

  # 创建计算事件（数值型）
  python3 scripts/event_manage.py --create "purchase_amount" --display-name "购买金额" --event-type true --app "Android_Demo"

  # 创建小程序事件
  python3 scripts/event_manage.py --create "view_page" --display-name "浏览页面" --app "友小盟数据官"

  # 批量创建事件（仅小程序）
  python3 scripts/event_manage.py --batch-create --events '[{"eventName":"click1","displayName":"点击1"}]' --app "友小盟数据官"

  # 从文件批量创建（仅小程序）
  python3 scripts/event_manage.py --batch-create --from-file events.json --app "友小盟数据官"

  # 查询事件列表
  python3 scripts/event_manage.py --list-events --app "友小盟数据官"

  # 创建并验证
  python3 scripts/event_manage.py --create "test_event" --display-name "测试事件" --verify --app "Android_Demo"

  # JSON 输出
  python3 scripts/event_manage.py --create "test_event" --display-name "测试事件" --json --app "Android_Demo"
"""
    )

    # 配置与应用
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--app", required=True, help="应用名称")
    parser.add_argument("--account", help="账号 ID")

    # 操作模式（互斥）
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--create", metavar="EVENT_NAME", help="创建单个事件")
    mode_group.add_argument("--batch-create", action="store_true", help="批量创建事件（仅小程序）")
    mode_group.add_argument("--list-events", action="store_true", help="查询事件列表")

    # 单个事件参数
    parser.add_argument("--display-name", help="事件显示名称")
    parser.add_argument("--event-type", choices=["true", "false"], 
                        help="事件类型：true=计算事件（数值型），false=计数事件（字符串型）")

    # 批量创建参数
    batch_group = parser.add_mutually_exclusive_group()
    batch_group.add_argument("--events", help="批量事件JSON字符串")
    batch_group.add_argument("--from-file", help="批量事件JSON文件路径")

    # 可选功能
    parser.add_argument("--verify", action="store_true", help="创建后验证事件是否存在")

    # 输出格式
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    try:
        args = parse_args(argv)

        # 解析配置与应用
        config_path = resolve_config_path(args.config)
        config = load_config(config_path)
        app_info = resolve_app(config, app_name=args.app, account_id=args.account)

        appkey = app_info["app"].get("appkey")
        platform = app_info["app"].get("platform", "")
        if not appkey:
            raise ValueError("应用配置缺少 appkey")

        # 初始化 SDK
        init_sdk(app_info["apiKey"], app_info["apiSecurity"])

        # 模式一：单个事件创建
        if args.create:
            event_name = args.create
            
            if not args.display_name:
                raise ValueError("--create 需要配合 --display-name 参数")

            display_name = args.display_name
            event_type = args.event_type

            # 参数格式校验
            valid, err_msg = validate_event_name(event_name)
            if not valid:
                raise ValueError(f"事件名称格式错误: {err_msg}")
            
            valid, err_msg = validate_display_name(display_name)
            if not valid:
                raise ValueError(f"显示名称格式错误: {err_msg}")

            # 判断平台类型并调用对应API
            if is_app_platform(platform):
                # App类型：调用 umeng.uapp.event.create
                resp = create_app_event(appkey, event_name, display_name, event_type)
                success = resp.get("status") == 0
                msg = resp.get("msg", "")

                # 可选验证
                verified = False
                exists = False
                if args.verify and success:
                    verified = True
                    exists = verify_event_exists_app(appkey, event_name)

                if args.json:
                    output = build_json_output(
                        success=success,
                        data={
                            "eventName": event_name,
                            "displayName": display_name,
                            "platform": platform,
                            "eventType": event_type,
                            "verified": verified,
                            "exists": exists,
                            "response": resp
                        },
                        message=msg
                    )
                    print(output)
                else:
                    print(build_create_result_text(event_name, display_name, platform, success, verified, exists))
                    if not success:
                        print(f"  错误信息: {msg}")

            elif is_mini_program_platform(platform):
                # 小程序类型：调用 umeng.umini.batchCreateEvent（单个事件也用批量接口）
                event_list = [{"eventName": event_name, "displayName": display_name}]
                resp = batch_create_mini_events(appkey, event_list)
                success = resp.get("success", False)
                msg = resp.get("msg", "")

                # 可选验证
                verified = False
                exists = False
                if args.verify and success:
                    verified = True
                    exists = verify_event_exists_mini(appkey, event_name)

                if args.json:
                    output = build_json_output(
                        success=success,
                        data={
                            "eventName": event_name,
                            "displayName": display_name,
                            "platform": platform,
                            "verified": verified,
                            "exists": exists,
                            "response": resp
                        },
                        message=msg
                    )
                    print(output)
                else:
                    print(build_create_result_text(event_name, display_name, platform, success, verified, exists))
                    if not success:
                        print(f"  错误信息: {msg}")
            else:
                raise ValueError(f"不支持的平台类型: {platform}")

        # 模式二：批量事件创建
        elif args.batch_create:
            # 检查平台类型
            if is_app_platform(platform):
                raise ValueError("App类型应用不支持批量创建，请使用 --create 单个创建")

            if not is_mini_program_platform(platform):
                raise ValueError(f"不支持的平台类型: {platform}")

            # 解析事件列表
            event_list = None
            if args.events:
                try:
                    event_list = json.loads(args.events)
                except json.JSONDecodeError as e:
                    raise ValueError(f"JSON解析失败: {e}")
            elif args.from_file:
                file_path = args.from_file
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"文件不存在: {file_path}")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        event_list = json.load(f)
                except json.JSONDecodeError as e:
                    raise ValueError(f"文件JSON解析失败: {e}")
            else:
                raise ValueError("--batch-create 需要配合 --events 或 --from-file 参数")

            if not isinstance(event_list, list) or len(event_list) == 0:
                raise ValueError("事件列表必须是非空数组")

            # 验证事件格式和参数
            for i, evt in enumerate(event_list):
                if not isinstance(evt, dict):
                    raise ValueError(f"事件 {i+1} 格式错误：必须是对象")
                if not evt.get("eventName"):
                    raise ValueError(f"事件 {i+1} 缺少 eventName 字段")
                if not evt.get("displayName"):
                    raise ValueError(f"事件 {i+1} 缺少 displayName 字段")
                
                # 参数格式校验
                valid, err_msg = validate_event_name(evt.get("eventName", ""))
                if not valid:
                    raise ValueError(f"事件 {i+1} eventName 格式错误: {err_msg}")
                
                valid, err_msg = validate_display_name(evt.get("displayName", ""))
                if not valid:
                    raise ValueError(f"事件 {i+1} displayName 格式错误: {err_msg}")

            # 调用批量创建API
            resp = batch_create_mini_events(appkey, event_list)
            api_success = resp.get("success", False)
            msg = resp.get("msg", "")

            # 构建结果
            results = []
            for evt in event_list:
                results.append({
                    "eventName": evt.get("eventName"),
                    "displayName": evt.get("displayName"),
                    "success": api_success,
                    "msg": msg if not api_success else ""
                })

            if args.json:
                output = build_json_output(
                    success=api_success,
                    data={
                        "platform": platform,
                        "total": len(event_list),
                        "successCount": sum(1 for r in results if r.get("success")),
                        "results": results,
                        "response": resp
                    },
                    message=msg
                )
                print(output)
            else:
                print(build_batch_create_result_text(results, platform))
                if not api_success:
                    print(f"\n错误信息: {msg}")

        # 模式三：事件列表查询
        elif args.list_events:
            if is_app_platform(platform):
                # App类型：调用 umeng.uapp.event.list
                result = query_event_list_app(appkey)
            elif is_mini_program_platform(platform):
                # 小程序类型：调用 umeng.umini.getEventList
                result = query_event_list_mini(appkey)
            else:
                raise ValueError(f"不支持的平台类型: {platform}")

            if args.json:
                output = build_json_output(
                    success=True,
                    data={
                        "platform": platform,
                        "events": result.get("events", []),
                        "total": result.get("total", 0),
                    },
                    message=""
                )
                print(output)
            else:
                print(build_event_list_table(result, platform))

        return 0

    except ValueError as e:
        error_result = {
            "success": False,
            "error_type": "ValueError",
            "message": str(e),
        }
        if hasattr(args, 'json') and args.json:
            print(json.dumps(error_result, ensure_ascii=False, indent=2))
        else:
            print(f"[错误] {e}", file=sys.stderr)
            print("\n提示：使用 --help 查看可用选项", file=sys.stderr)
        return 1

    except FileNotFoundError as e:
        error_result = {
            "success": False,
            "error_type": "FileNotFoundError",
            "message": str(e),
        }
        if hasattr(args, 'json') and args.json:
            print(json.dumps(error_result, ensure_ascii=False, indent=2))
        else:
            print(f"[配置错误] {e}", file=sys.stderr)
        return 1

    except Exception as e:
        error_result = {
            "success": False,
            "error_type": type(e).__name__,
            "message": str(e),
        }
        if hasattr(args, 'json') and args.json:
            print(json.dumps(error_result, ensure_ascii=False, indent=2))
        else:
            print(f"[错误] {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
