#!/usr/bin/env python3
"""
A股报告推送公共模块
提供：企业微信推送、时间判断、去重状态管理
"""
import subprocess, json, os, sys
from datetime import datetime, timezone, timedelta

# Webhook URL 统一从 keys_loader 读取，不再硬编码
sys.path.insert(0, "/workspace")
from keys_loader import get_webhook_url

WEBHOOK_URL = ""

def load_config():
    global WEBHOOK_URL
    try:
        WEBHOOK_URL = get_webhook_url()
    except Exception as e:
        print(f"❌ 读取 Webhook URL 失败: {e}")
        sys.exit(1)

def wx_push(text: str) -> int:
    """推送文本到企业微信，返回 errcode（0=成功）"""
    load_config()
    payload = json.dumps({"msgtype": "text", "text": {"content": text}}, ensure_ascii=False)
    r = subprocess.run(
        ["curl", "-s", "-X", "POST", WEBHOOK_URL,
         "-H", "Content-Type: application/json", "-d", "@-"],
        input=payload.encode("utf-8"), capture_output=True
    )
    try:
        return json.loads(r.stdout.decode()).get("errcode", -1)
    except Exception:
        return -1

def wx_push_markdown(text: str) -> int:
    """推送 Markdown 格式（若企业微信版本支持）"""
    load_config()
    payload = json.dumps({"msgtype": "markdown", "markdown": {"content": text}}, ensure_ascii=False)
    r = subprocess.run(
        ["curl", "-s", "-X", "POST", WEBHOOK_URL,
         "-H", "Content-Type: application/json", "-d", "@-"],
        input=payload.encode("utf-8"), capture_output=True
    )
    try:
        return json.loads(r.stdout.decode()).get("errcode", -1)
    except Exception:
        return -1

def is_trading_day() -> bool:
    """判断今日是否为A股交易日（周一至五）"""
    now_bj = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
    return now_bj.weekday() < 5

def is_trading_window():
    """判断当前是否在A股交易时段（不含集合竞价）"""
    now_bj = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
    w = now_bj.weekday()
    if w >= 5:
        return False
    h, m = now_bj.hour, now_bj.minute
    morning = (h == 9 and m >= 30) or (10 <= h <= 11)
    afternoon = 13 <= h <= 15
    return morning or afternoon

def already_sent(state_file: str) -> bool:
    """根据状态文件判断今日是否已推送（去重）"""
    today = datetime.now(timezone(timedelta(hours=8))).strftime("%Y%m%d")
    f = os.path.join(os.path.dirname(__file__), state_file)
    return os.path.exists(f) and open(f).read().strip() == today

def mark_sent(state_file: str):
    """标记今日已推送"""
    f = os.path.join(os.path.dirname(__file__), state_file)
    with open(f, "w") as fp:
        fp.write(datetime.now(timezone(timedelta(hours=8))).strftime("%Y%m%d"))

def now_bj():
    return datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))

def ts():
    return now_bj().strftime("%Y-%m-%d %H:%M")
