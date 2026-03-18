"""报警规则管理 + 飞书Webhook通知"""

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent / "config.json"

# 冷却记录: {rule_id: last_trigger_timestamp}
_cooldowns = {}  # {rule_id: last_trigger_timestamp}
COOLDOWN_SECONDS = 30 * 60  # 30分钟


def _load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {"alerts": [], "feishu_webhook_url": ""}


def _save_config(config: dict):
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")


def get_alerts() -> list[dict]:
    return _load_config().get("alerts", [])


def add_alert(rule: dict) -> dict:
    config = _load_config()
    rule["id"] = str(uuid.uuid4())[:8]
    rule.setdefault("enabled", True)
    config["alerts"].append(rule)
    _save_config(config)
    return rule


def delete_alert(rule_id: str) -> bool:
    config = _load_config()
    before = len(config["alerts"])
    config["alerts"] = [a for a in config["alerts"] if a.get("id") != rule_id]
    _save_config(config)
    return len(config["alerts"]) < before


def get_webhook_url() -> str:
    return _load_config().get("feishu_webhook_url", "")


def set_webhook_url(url: str):
    config = _load_config()
    config["feishu_webhook_url"] = url
    _save_config(config)


def check_alerts(prices: list[dict]):
    """检查所有报警规则，满足条件则发送飞书通知"""
    config = _load_config()
    webhook_url = config.get("feishu_webhook_url", "")
    if not webhook_url:
        return

    price_map = {p["symbol"]: p for p in prices}
    now = time.time()

    for rule in config.get("alerts", []):
        if not rule.get("enabled", True):
            continue
        rule_id = rule.get("id", "")
        # 冷却检查
        if rule_id in _cooldowns and (now - _cooldowns[rule_id]) < COOLDOWN_SECONDS:
            continue

        symbol = rule.get("symbol", "")
        price_info = price_map.get(symbol)
        if not price_info or price_info.get("error"):
            continue

        triggered = False
        condition = rule.get("condition", "")
        threshold = float(rule.get("threshold", 0))
        current_price = price_info["price"]
        change_pct = price_info["change_pct"]

        if condition == "price_above" and current_price > threshold:
            triggered = True
        elif condition == "price_below" and current_price < threshold:
            triggered = True
        elif condition == "change_pct_above" and change_pct > threshold:
            triggered = True
        elif condition == "change_pct_below" and change_pct < -threshold:
            triggered = True

        if triggered:
            _cooldowns[rule_id] = now
            _send_feishu_alert(webhook_url, rule, price_info)


def _send_feishu_alert(webhook_url: str, rule: dict, price_info: dict):
    """发送飞书富文本消息卡片"""
    condition_text = {
        "price_above": "价格高于",
        "price_below": "价格低于",
        "change_pct_above": "涨幅超过",
        "change_pct_below": "跌幅超过",
    }
    cond = condition_text.get(rule.get("condition", ""), rule.get("condition", ""))
    threshold = rule.get("threshold", 0)
    unit_suffix = "%" if "pct" in rule.get("condition", "") else ""

    change_sign = "+" if price_info["change"] >= 0 else ""
    color = "red" if price_info["change"] >= 0 else "green"

    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": f"⚠️ 黄金监控报警"},
                "template": color,
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            f"**品种**: {price_info['name']}\n"
                            f"**当前价**: {price_info['price']} {price_info['unit']}\n"
                            f"**涨跌**: {change_sign}{price_info['change']} ({change_sign}{price_info['change_pct']}%)\n"
                            f"**触发条件**: {cond} {threshold}{unit_suffix}\n"
                            f"**时间**: {price_info['update_time']}"
                        ),
                    },
                }
            ],
        },
    }
    try:
        resp = requests.post(webhook_url, json=card, timeout=10)
        resp.raise_for_status()
        logger.info("飞书通知已发送: %s", price_info["name"])
    except Exception as e:
        logger.error("飞书通知发送失败: %s", e)


def send_test_notification(webhook_url: str) -> bool:
    """发送测试通知"""
    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": "✅ 黄金监控测试通知"},
                "template": "blue",
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "黄金监控面板通知功能正常工作！\n\n这是一条测试消息。",
                    },
                }
            ],
        },
    }
    try:
        resp = requests.post(webhook_url, json=card, timeout=10)
        resp.raise_for_status()
        return True
    except Exception as e:
        logger.error("测试通知发送失败: %s", e)
        return False
