#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""uapp-channel-version: 友盟 App 渠道/版本分析脚本

阶段一实现：
- 单日快照查询（--dimension, --date, --top, --sort-by）
- 支持渠道和版本维度
- 输出：排名表格 + JSON 数据
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta

# -------------------------
# 常量定义
# -------------------------

DIMENSION_LABEL = {
    "channel": "渠道",
    "version": "版本",
}

SORT_FIELD_MAP = {
    "new_users": "newUser",
    "active_users": "activeUser",
    "launches": "launch",
    "total_user": "totalUser",
}

METRIC_LABEL = {
    "new_users": "新增用户",
    "active_users": "活跃用户",
    "launches": "启动次数",
}

METRIC_RESPONSE_KEY = {
    "new_users": "newUserInfo",
    "active_users": "activeUserInfo",
    "launches": "launchInfo",
}

# -------------------------
# 工具函数：路径 & 配置加载（从 uapp-core-index 复制）
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
# 应用解析（从 uapp-core-index 复制）
# -------------------------


def normalize_app_name(name: str) -> str:
    """去除半角/全角空格，用于模糊匹配。"""
    return name.replace(" ", "").replace("\u3000", "")


def find_app_by_name(config: dict, app_name: str, account_id: str | None = None, platform: str | None = None):
    """按应用名称查找应用配置，支持精确匹配 + 去空格模糊匹配。"""
    matches = []
    normalized_input = normalize_app_name(app_name)

    for account in config.get("accounts", []):
        if account_id and account.get("id") != account_id:
            continue
        for app in account.get("apps", []):
            if platform and app.get("platform") != platform:
                continue
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


def resolve_app(config: dict, app_name: str | None, account_id: str | None, platform: str | None) -> dict:
    """解析最终使用的应用配置。"""
    if app_name:
        result = find_app_by_name(config, app_name, account_id=account_id, platform=platform)
        if not result:
            available = []
            for account in config.get("accounts", []):
                for app in account.get("apps", []):
                    available.append(app.get("name", ""))
            raise ValueError(f"未找到名称匹配的应用: {app_name}，可用应用: {', '.join(available)}")
        if isinstance(result, list):
            raise ValueError("存在多个同名应用，请通过 --account / --platform 进一步限定")
        return result

    default_app = config.get("defaultApp")
    if default_app:
        return {
            "account_id": default_app.get("account_id"),
            "apiKey": default_app.get("apiKey"),
            "apiSecurity": default_app.get("apiSecurity"),
            "app": {
                "name": default_app.get("name"),
                "appkey": default_app.get("appkey"),
                "platform": default_app.get("platform"),
            },
        }

    raise ValueError("未指定应用且配置中未设置 defaultApp，请使用 --app 指定应用名称")


# -------------------------
# 日期解析
# -------------------------


def parse_date(s: str) -> date:
    """解析日期字符串。"""
    return datetime.strptime(s, "%Y-%m-%d").date()


def resolve_date(date_str: str | None) -> date:
    """解析日期参数，默认为昨天。"""
    if date_str is None:
        return date.today() - timedelta(days=1)
    return parse_date(date_str)


def resolve_time_range(range_name: str, today: date | None = None) -> tuple[date, date]:
    """解析时间范围名称到起止日期（含）。"""
    if today is None:
        today = date.today()

    if range_name == "yesterday":
        d = today - timedelta(days=1)
        return d, d
    if range_name == "last_7_days":
        end = today - timedelta(days=1)
        start = end - timedelta(days=6)
        return start, end
    if range_name == "last_30_days":
        end = today - timedelta(days=1)
        start = end - timedelta(days=29)
        return start, end
    if range_name == "last_90_days":
        end = today - timedelta(days=1)
        start = end - timedelta(days=89)
        return start, end

    # 尝试解析为日期
    try:
        d = parse_date(range_name)
        return d, d
    except Exception:
        raise ValueError(f"不支持的时间范围: {range_name}")


# -------------------------
# SDK 初始化
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
# API 查询（阶段一：单日快照）
# -------------------------


def query_channel_data(app_cfg: dict, query_date: date) -> list[dict]:
    """查询单日渠道数据。"""
    from aop import api

    appkey = app_cfg["app"].get("appkey")
    if not appkey:
        raise ValueError("应用配置缺少 appkey")

    req = api.UmengUappGetChannelDataRequest()
    req.appkey = appkey
    req.date = query_date.strftime("%Y-%m-%d")

    resp = req.get_response()
    if not isinstance(resp, dict):
        raise ValueError("API 响应格式错误")

    return resp.get("channelInfos", [])


def query_version_data(app_cfg: dict, query_date: date) -> list[dict]:
    """查询单日版本数据。"""
    from aop import api

    appkey = app_cfg["app"].get("appkey")
    if not appkey:
        raise ValueError("应用配置缺少 appkey")

    req = api.UmengUappGetVersionDataRequest()
    req.appkey = appkey
    req.date = query_date.strftime("%Y-%m-%d")

    resp = req.get_response()
    if not isinstance(resp, dict):
        raise ValueError("API 响应格式错误")

    return resp.get("versionInfos", [])


def query_metric_trend(
    app_cfg: dict,
    metric: str,
    dimension: str,
    start: date,
    end: date,
    channel: str | None = None,
    version: str | None = None,
) -> list[dict]:
    """查询渠道/版本维度的指标趋势数据。"""
    from aop import api

    appkey = app_cfg["app"].get("appkey")
    if not appkey:
        raise ValueError("应用配置缺少 appkey")

    # 根据指标选择 API
    if metric == "new_users":
        req = api.UmengUappGetNewUsersByChannelOrVersionRequest()
    elif metric == "active_users":
        req = api.UmengUappGetActiveUsersByChannelOrVersionRequest()
    elif metric == "launches":
        req = api.UmengUappGetLaunchesByChannelOrVersionRequest()
    else:
        raise ValueError(f"不支持的指标类型: {metric}")

    req.appkey = appkey
    req.startDate = start.strftime("%Y-%m-%d")
    req.endDate = end.strftime("%Y-%m-%d")
    req.periodType = "daily"

    # 设置渠道或版本筛选
    if dimension == "channel" and channel:
        req.channel = channel
    elif dimension == "version" and version:
        req.version = version

    resp = req.get_response()
    if not isinstance(resp, dict):
        raise ValueError("API 响应格式错误")

    # 获取响应数据
    response_key = METRIC_RESPONSE_KEY.get(metric, "newUserInfo")
    return resp.get(response_key, [])


# -------------------------
# 数据处理
# -------------------------


def sort_data(data: list[dict], sort_by: str, reverse: bool = True) -> list[dict]:
    """按指定字段排序数据。"""
    field = SORT_FIELD_MAP.get(sort_by, sort_by)

    def get_sort_key(item):
        value = item.get(field, 0)
        # 处理字符串类型的数字（如 duration）
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return value
        return value if value is not None else 0

    return sorted(data, key=get_sort_key, reverse=reverse)


def filter_by_name(data: list[dict], dimension: str, name: str) -> list[dict]:
    """按渠道名或版本名筛选数据。"""
    field = "channel" if dimension == "channel" else "version"
    return [item for item in data if item.get(field) == name]


def filter_top_n(data: list[dict], n: int) -> list[dict]:
    """返回 Top N 数据。"""
    return data[:n] if n > 0 else data


# -------------------------
# 输出格式化
# -------------------------


def format_number(num: int | float | None) -> str:
    """格式化数字，添加千分位。"""
    if num is None:
        return "-"
    if isinstance(num, float):
        return f"{num:,.2f}"
    return f"{num:,}"


def build_snapshot_table(
    app_info: dict,
    dimension: str,
    query_date: date,
    data: list[dict],
    sort_by: str,
) -> str:
    """构造单日快照的表格输出。"""
    app_name = app_info["app"].get("name")
    dim_label = DIMENSION_LABEL.get(dimension, dimension)

    lines = [
        f"应用 {app_name} 的 {dim_label} 表现对比（{query_date}）：",
        "",
    ]

    if not data:
        lines.append(f"暂无 {dim_label} 数据。")
        return "\n".join(lines)

    # 表头
    if dimension == "channel":
        lines.append(f"{'排名':<6} {'渠道':<20} {'新增用户':<12} {'活跃用户':<12} {'启动次数':<12} {'总用户':<12}")
    else:
        lines.append(f"{'排名':<6} {'版本':<20} {'新增用户':<12} {'活跃用户':<12} {'总用户':<12}")

    lines.append("-" * 80)

    # 数据行
    for idx, item in enumerate(data, 1):
        name = item.get("channel" if dimension == "channel" else "version", "N/A")
        new_user = item.get("newUser", 0)
        active_user = item.get("activeUser", 0)
        total_user = item.get("totalUser", 0)

        if dimension == "channel":
            launch = item.get("launch", 0)
            lines.append(
                f"{idx:<6} {name:<20} {format_number(new_user):<12} "
                f"{format_number(active_user):<12} {format_number(launch):<12} "
                f"{format_number(total_user):<12}"
            )
        else:
            lines.append(
                f"{idx:<6} {name:<20} {format_number(new_user):<12} "
                f"{format_number(active_user):<12} {format_number(total_user):<12}"
            )

    return "\n".join(lines)


def build_snapshot_json(
    app_info: dict,
    dimension: str,
    query_date: date,
    data: list[dict],
    sort_by: str,
) -> dict:
    """构造单日快照的 JSON 输出。"""
    return {
        "app": {
            "name": app_info["app"].get("name"),
            "appkey": app_info["app"].get("appkey"),
            "platform": app_info["app"].get("platform"),
        },
        "dimension": dimension,
        "date": query_date.isoformat(),
        "sort_by": sort_by,
        "count": len(data),
        "data": data,
    }


def build_trend_summary(
    app_info: dict,
    metric: str,
    dimension: str,
    start: date,
    end: date,
    series: list[dict],
    channel: str | None = None,
    version: str | None = None,
) -> str:
    """构造趋势分析的文本摘要。"""
    app_name = app_info["app"].get("name")
    metric_label = METRIC_LABEL.get(metric, metric)
    dim_label = DIMENSION_LABEL.get(dimension, dimension)

    # 构建维度描述
    filter_desc = ""
    if channel:
        filter_desc = f"渠道 {channel} 的"
    elif version:
        filter_desc = f"版本 {version} 的"

    lines = [
        f"应用 {app_name} {filter_desc}{metric_label}趋势（{start} 至 {end}）：",
        "",
    ]

    if not series:
        lines.append(f"暂无 {metric_label} 数据。")
        return "\n".join(lines)

    # 提取数值
    values = [item.get("value", 0) for item in series if item.get("value") is not None]

    if not values:
        lines.append(f"暂无有效 {metric_label} 数据。")
        return "\n".join(lines)

    first_val = values[0]
    last_val = values[-1]
    avg_val = sum(values) / len(values)

    # 趋势判断
    if first_val == 0:
        trend = "变化情况不明显"
    else:
        change_rate = (last_val - first_val) / float(first_val)
        if change_rate > 0.05:
            trend = f"整体呈上升趋势，末期较初期上升 {change_rate*100:.1f}%"
        elif change_rate < -0.05:
            trend = f"整体呈下降趋势，末期较初期下降 {abs(change_rate)*100:.1f}%"
        else:
            trend = "整体基本持平"

    lines.append(f"日均 {metric_label}：{format_number(avg_val)}")
    lines.append(f"初期值：{format_number(first_val)}，末期值：{format_number(last_val)}")
    lines.append(trend)

    return "\n".join(lines)


def build_trend_json(
    app_info: dict,
    metric: str,
    dimension: str,
    start: date,
    end: date,
    series: list[dict],
    channel: str | None = None,
    version: str | None = None,
) -> dict:
    """构造趋势分析的 JSON 输出。"""
    return {
        "app": {
            "name": app_info["app"].get("name"),
            "appkey": app_info["app"].get("appkey"),
            "platform": app_info["app"].get("platform"),
        },
        "metric": metric,
        "dimension": dimension,
        "channel": channel,
        "version": version,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "series": series,
    }


# -------------------------
# CLI 入口
# -------------------------


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="uapp-channel-version: 友盟 App 渠道/版本分析")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--app", help="应用名称（支持模糊匹配）")
    parser.add_argument("--account", help="账号 ID")
    parser.add_argument("--platform", help="平台标识")

    parser.add_argument(
        "--dimension",
        choices=["channel", "version"],
        default="channel",
        help="分析维度：channel（渠道，默认）/ version（版本）",
    )
    parser.add_argument(
        "--date",
        help="查询日期（yyyy-mm-dd），默认昨天（单日快照模式）",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="显示 Top N 结果，默认 10（单日快照模式）",
    )
    parser.add_argument(
        "--sort-by",
        choices=["new_users", "active_users", "launches", "total_user"],
        default="active_users",
        help="排序字段，默认 active_users（单日快照模式）",
    )

    # 趋势分析参数（阶段二）
    parser.add_argument(
        "--metric",
        choices=["new_users", "active_users", "launches"],
        help="趋势指标类型（趋势模式）",
    )
    parser.add_argument(
        "--range",
        dest="time_range",
        help="时间范围：yesterday/last_7_days/last_30_days/last_90_days（趋势模式）",
    )
    parser.add_argument(
        "--filter-channel",
        dest="filter_channel",
        help="筛选指定渠道（趋势模式）",
    )
    parser.add_argument(
        "--filter-version",
        dest="filter_version",
        help="筛选指定版本（趋势模式）",
    )

    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出结果")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    try:
        args = parse_args(argv)

        config_path = resolve_config_path(args.config)
        config = load_config(config_path)

        app_info = resolve_app(config, app_name=args.app, account_id=args.account, platform=args.platform)

        init_sdk(app_info["apiKey"], app_info["apiSecurity"])

        # 判断模式：趋势模式 vs 单日快照模式
        if args.metric or args.time_range:
            # 趋势分析模式
            if not args.metric:
                raise ValueError("趋势模式需要指定 --metric 参数")
            if not args.time_range:
                raise ValueError("趋势模式需要指定 --range 参数")

            start, end = resolve_time_range(args.time_range)

            # 查询趋势数据
            series = query_metric_trend(
                app_info,
                metric=args.metric,
                dimension=args.dimension,
                start=start,
                end=end,
                channel=args.filter_channel,
                version=args.filter_version,
            )

            # 输出结果
            if args.json:
                output = build_trend_json(
                    app_info,
                    args.metric,
                    args.dimension,
                    start,
                    end,
                    series,
                    channel=args.filter_channel,
                    version=args.filter_version,
                )
                print(json.dumps(output, ensure_ascii=False, indent=2))
            else:
                text = build_trend_summary(
                    app_info,
                    args.metric,
                    args.dimension,
                    start,
                    end,
                    series,
                    channel=args.filter_channel,
                    version=args.filter_version,
                )
                print(text)

        else:
            # 单日快照模式
            query_date = resolve_date(args.date)

            # 根据维度查询数据
            if args.dimension == "channel":
                data = query_channel_data(app_info, query_date)
            else:
                data = query_version_data(app_info, query_date)

            # 筛选（阶段三：支持快照模式筛选）
            if args.dimension == "channel" and args.filter_channel:
                data = filter_by_name(data, "channel", args.filter_channel)
            elif args.dimension == "version" and args.filter_version:
                data = filter_by_name(data, "version", args.filter_version)

            # 排序和筛选
            sorted_data = sort_data(data, args.sort_by)
            top_data = filter_top_n(sorted_data, args.top)

            # 输出结果
            if args.json:
                output = build_snapshot_json(
                    app_info,
                    args.dimension,
                    query_date,
                    top_data,
                    args.sort_by,
                )
                print(json.dumps(output, ensure_ascii=False, indent=2))
            else:
                text = build_snapshot_table(
                    app_info,
                    args.dimension,
                    query_date,
                    top_data,
                    args.sort_by,
                )
                print(text)

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
            "help": "配置方式:\n"
                    "1. --config /path/to/umeng-config.json\n"
                    "2. export UMENG_CONFIG_PATH=/path/to/umeng-config.json\n"
                    "3. 在当前目录创建 umeng-config.json",
        }
        if hasattr(args, 'json') and args.json:
            print(json.dumps(error_result, ensure_ascii=False, indent=2))
        else:
            print(f"[配置错误] {e}", file=sys.stderr)
            print("\n可用配置方式:", file=sys.stderr)
            print("  1. --config /path/to/umeng-config.json", file=sys.stderr)
            print("  2. export UMENG_CONFIG_PATH=/path/to/umeng-config.json", file=sys.stderr)
            print("  3. 在当前目录创建 umeng-config.json", file=sys.stderr)
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
