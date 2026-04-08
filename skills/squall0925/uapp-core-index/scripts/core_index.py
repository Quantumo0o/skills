#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""uapp-core-index: 友盟 App 核心指标问答入口脚本

最小实现目标：
- 读取 umeng-config.json（支持 --config / UMENG_CONFIG_PATH / 当前目录 / .env）
- 解析应用（支持 --app / --account / --platform，含模糊匹配）
- 支持基础指标查询：DAU、新增用户、启动次数
- 支持时间范围：yesterday / last_7_days / last_30_days
- 输出：
  - 文本模式：自然语言简要摘要
  - JSON 模式：结构化趋势数据表，便于上层 Agent 使用
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta

# -------------------------
# 工具函数：路径 & 配置加载
# -------------------------


def resolve_workspace_root() -> str:
    """解析 workspace 根目录。

    约定：
    - skill 独立发布时，workspace 即为 skill 所在的父目录
    - openclaw 运行时会将 skill 目录作为一个单元挂载
    """
    # 当前文件: skills/uapp-core-index/scripts/core_index.py
    # workspace:   <workspace>/
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    workspace = os.path.dirname(skill_dir)
    return workspace


def load_env_config_path() -> str | None:
    """从环境变量或 .env 中加载 UMENG_CONFIG_PATH。

    优先级：
    1. 环境变量 UMENG_CONFIG_PATH
    2. workspace/.env 中的 UMENG_CONFIG_PATH
    """
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
    """解析配置文件路径。

    优先级：
    1. CLI 参数 --config
    2. UMENG_CONFIG_PATH（环境变量/.env）
    3. workspace 根目录下的 umeng-config.json
    """
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
    """解析最终使用的应用配置。

    - 优先使用 --app 指定的应用名
    - 否则使用配置中的 defaultApp（如有）
    """
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

    # 没有指定 app，尝试 defaultApp
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
# 时间范围解析
# -------------------------


def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def _get_last_week_range(today: date) -> tuple[date, date]:
    """计算上周一-周日范围（相对 today 的上一个完整自然周）。"""
    # 上周日 = today - (weekday + 1)
    last_sunday = today - timedelta(days=today.weekday() + 1)
    last_monday = last_sunday - timedelta(days=6)
    return last_monday, last_sunday


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
    if range_name == "last_week":
        return _get_last_week_range(today)
    if range_name == "today_yesterday":
        # S5 场景：今天 vs 昨天对比，返回特殊标记，由上层处理
        return "today_yesterday", "today_yesterday"

    # 默认视作单日日期
    try:
        d = parse_date(range_name)
        return d, d
    except Exception as exc:  # noqa: F841
        raise ValueError(f"不支持的时间范围: {range_name}")


# -------------------------
# Umeng SDK 调用占位（最小集）
# -------------------------


def get_sdk_root() -> str:
    """获取当前 skill 内部 SDK 根目录。"""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(skill_dir, "友盟_openapi_python_SDK")


def init_sdk(api_key: str, api_security: str) -> None:
    """初始化 SDK 路径和默认服务器配置。

    必须在调用任何 API 之前执行。
    """
    # 1. 设置 SDK 路径
    sdk_root = get_sdk_root()
    if sdk_root not in sys.path:
        sys.path.insert(0, sdk_root)

    # 2. 导入并初始化 aop
    import aop
    aop.set_default_server('gateway.open.umeng.com')
    aop.set_default_appinfo(int(api_key), api_security)


def _query_duration_for_day(api, appkey: str, day: date) -> float | None:
    """查询某一天的平均使用时长（秒）。

    使用 umeng.uapp.getDurations，直接返回 API 提供的 average 字段。
    若无法获取，返回 None。
    """
    req = api.UmengUappGetDurationsRequest()
    req.appkey = appkey
    req.date = day.strftime("%Y-%m-%d")
    resp = req.get_response()
    if not isinstance(resp, dict):
        return None
    # API 响应根节点包含 average 字段（平均使用时长，单位：秒）
    avg = resp.get("average")
    if avg is None:
        return None
    return float(avg)


def query_today_yesterday(app_cfg: dict, metric: str) -> dict:
    """查询今天 vs 昨天的对比数据（S5 场景）。

    使用 umeng.uapp.getTodayYesterdayData，返回 today 和 yesterday 的指标值。
    """
    from aop import api

    appkey = app_cfg["app"].get("appkey")
    if not appkey:
        raise ValueError("应用配置缺少 appkey")

    req = api.UmengUappGetTodayYesterdayDataRequest()
    req.appkey = appkey
    resp = req.get_response()
    if not isinstance(resp, dict):
        raise ValueError("API 响应格式错误")

    value_key = {
        "dau": "activityUsers",
        "new_users": "newUsers",
        "launches": "launches",
    }.get(metric)
    if not value_key:
        raise ValueError(f"指标 {metric} 不支持 today_yesterday 对比")

    today_data = resp.get("todayData", {})
    yesterday_data = resp.get("yesterdayData", {})

    return {
        "today": {
            "date": today_data.get("date"),
            "value": today_data.get(value_key),
        },
        "yesterday": {
            "date": yesterday_data.get("date"),
            "value": yesterday_data.get(value_key),
        },
    }


def query_metric_series(app_cfg: dict, metric: str, start: date, end: date) -> list[dict]:
    """查询某个指标在指定日期区间的序列数据。

    当前实现：
    - dau/new_users/launches：使用 getDailyData 逐日查询
    - duration：使用 getDurations 逐日查询并计算加权平均时长（秒）
    """
    from aop import api  # 延迟导入，避免在未初始化 SDK 路径时出错

    appkey = app_cfg["app"].get("appkey")
    if not appkey:
        raise ValueError("应用配置缺少 appkey")

    series: list[dict] = []
    cur = start
    while cur <= end:
        if metric == "duration":
            value = _query_duration_for_day(api, appkey, cur)
            raw = None  # duration 场景暂不提供原始 dailyData
        else:
            req = api.UmengUappGetDailyDataRequest()
            req.appkey = appkey
            req.date = cur.strftime("%Y-%m-%d")
            resp = req.get_response()
            # dailyData 可能在不同字段中，沿用 get_stats 的 extract_stats 思路
            if isinstance(resp, dict):
                daily = resp.get("dailyData") or resp.get("yesterdayData") or resp
            else:
                daily = None

            if daily:
                value_key = {
                    "dau": "activityUsers",
                    "new_users": "newUsers",
                    "launches": "launches",
                }.get(metric)
                value = daily.get(value_key) if value_key else None
            else:
                value = None
            raw = daily

        series.append({
            "date": cur.strftime("%Y-%m-%d"),
            "value": value,
            "raw": raw,
        })
        cur += timedelta(days=1)

    return series


# -------------------------
# 输出格式化
# -------------------------


def build_summary_text(app_info: dict, metric: str, start: date, end: date, series: list[dict]) -> str:
    """构造简单的中文摘要文案。

    当前版本：
    - 单日：给出该日的指标值
    - 区间：给出日均值、起止值与大致趋势（上升/下降/持平）
    """
    app_name = app_info["app"].get("name")

    # 提取有效值
    values = [item["value"] for item in series if item.get("value") is not None]
    metric_label = {
        "dau": "活跃用户数",
        "new_users": "新增用户数",
        "launches": "启动次数",
        "duration": "平均使用时长",
    }.get(metric, metric)

    if not values:
        if start == end:
            return f"应用 {app_name} 在 {start} 的 {metric_label} 暂无可用数据。"
        return f"应用 {app_name} 在 {start} 至 {end} 的 {metric_label} 暂无可用数据。"

    first_val = values[0]
    last_val = values[-1]
    avg_val = sum(values) / len(values)

    # 格式化数值（时长保留 1 位小数，其余取整）
    if metric == "duration":
        fmt = lambda x: f"{x:.1f} 秒"  # noqa: E731
    else:
        fmt = lambda x: f"{int(round(x))}"  # noqa: E731

    if start == end:
        return f"应用 {app_name} 在 {start} 的 {metric_label} 为 {fmt(last_val)}。"

    # 区间趋势
    if first_val == 0:
        trend = "变化情况不明显"
    else:
        change_rate = (last_val - first_val) / float(first_val)
        if change_rate > 0.05:
            trend = f"整体呈上升趋势，末日值约为首日的 {last_val/first_val:.2f} 倍"
        elif change_rate < -0.05:
            trend = f"整体呈下降趋势，末日值约为首日的 {last_val/first_val:.2f} 倍"
        else:
            trend = "整体基本持平"

    # 多日均值提示（对 last_week 等自然时间段尤其有用）
    return (
        f"应用 {app_name} 在 {start} 至 {end} 的 {metric_label} 日均 {fmt(avg_val)}，"
        f"从 {fmt(first_val)} 变化到 {fmt(last_val)}，{trend}。"
    )


def build_today_yesterday_summary(app_info: dict, metric: str, data: dict) -> str:
    """构造今天 vs  yesterday 对比的中文摘要文案。"""
    app_name = app_info["app"].get("name")
    metric_label = {
        "dau": "活跃用户数",
        "new_users": "新增用户数",
        "launches": "启动次数",
    }.get(metric, metric)

    today_val = data["today"]["value"]
    yesterday_val = data["yesterday"]["value"]
    today_date = data["today"]["date"]
    yesterday_date = data["yesterday"]["date"]

    if today_val is None or yesterday_val is None:
        return f"应用 {app_name} 的 {metric_label} 对比数据暂无可用。"

    if yesterday_val == 0:
        change_desc = "昨天数据为 0，无法计算变化率"
    else:
        change_rate = (today_val - yesterday_val) / float(yesterday_val)
        change_pct = abs(change_rate) * 100
        if change_rate > 0:
            change_desc = f"比昨天上升 {change_pct:.1f}%"
        elif change_rate < 0:
            change_desc = f"比昨天下降 {change_pct:.1f}%"
        else:
            change_desc = "与昨天持平"

    return (
        f"应用 {app_name} 今天（{today_date}）的 {metric_label} 为 {today_val}，"
        f"昨天（{yesterday_date}）为 {yesterday_val}，{change_desc}。"
    )


def build_today_yesterday_json(app_info: dict, metric: str, data: dict) -> dict:
    """构造今天 vs yesterday 对比的 JSON 输出。"""
    today_val = data["today"]["value"]
    yesterday_val = data["yesterday"]["value"]

    change_rate = None
    if yesterday_val is not None and yesterday_val != 0 and today_val is not None:
        change_rate = (today_val - yesterday_val) / float(yesterday_val)

    return {
        "app": {
            "name": app_info["app"].get("name"),
            "appkey": app_info["app"].get("appkey"),
            "platform": app_info["app"].get("platform"),
        },
        "metric": metric,
        "comparison": "today_yesterday",
        "today": data["today"],
        "yesterday": data["yesterday"],
        "change_rate": change_rate,
    }


def build_json_output(app_info: dict, metric: str, start: date, end: date, series: list[dict]) -> dict:
    return {
        "app": {
            "name": app_info["app"].get("name"),
            "appkey": app_info["app"].get("appkey"),
            "platform": app_info["app"].get("platform"),
        },
        "metric": metric,
        "start_date": start.isoformat() if isinstance(start, date) else start,
        "end_date": end.isoformat() if isinstance(end, date) else end,
        "series": series,
    }


# -------------------------
# CLI 入口
# -------------------------


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="uapp-core-index: 友盟 App 核心指标问答入口")
    parser.add_argument("--config", help="配置文件路径（默认为 workspace/umeng-config.json 或 UMENG_CONFIG_PATH 指定路径）")
    parser.add_argument("--app", help="应用名称（支持模糊匹配）")
    parser.add_argument("--account", help="账号 ID，用于区分多账号下同名应用")
    parser.add_argument("--platform", help="平台标识，如 android/ios")

    parser.add_argument("--metric", required=True, choices=["dau", "new_users", "launches", "duration"], help="查询指标类型")
    parser.add_argument("--range", dest="time_range", required=True, help="时间范围：yesterday/last_7_days/last_30_days/last_week/today_yesterday 或 yyyy-mm-dd")

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

        start, end = resolve_time_range(args.time_range)

        # 初始化 SDK（设置服务器域名和认证信息）
        init_sdk(app_info["apiKey"], app_info["apiSecurity"])

        # S5 场景：今天 vs 昨天对比
        if start == "today_yesterday" and end == "today_yesterday":
            data = query_today_yesterday(app_info, args.metric)
            if args.json:
                output = build_today_yesterday_json(app_info, args.metric, data)
                print(json.dumps(output, ensure_ascii=False, indent=2))
            else:
                text = build_today_yesterday_summary(app_info, args.metric, data)
                print(text)
        else:
            series = query_metric_series(app_info, args.metric, start, end)
            if args.json:
                output = build_json_output(app_info, args.metric, start, end, series)
                print(json.dumps(output, ensure_ascii=False, indent=2))
            else:
                text = build_summary_text(app_info, args.metric, start, end, series)
                print(text)

        return 0

    except ValueError as e:
        # 配置或参数错误
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
    except Exception as e:  # noqa: BLE001
        # 其他错误（包括 API 错误）
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


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
