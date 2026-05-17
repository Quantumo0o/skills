
import asyncio
import os
import re
import sqlite3
from datetime import datetime, timedelta

from telethon import TelegramClient, events

try:
    from openpyxl import Workbook
except ImportError:
    Workbook = None

from tg_monitor_kit.client import build_client
from tg_monitor_kit.config import load_config

TARGET_GROUP_NAME = [
    '梦西游-出海交流群',
    'Face_🅱️⭕🆗',
    '棉花糖Marshmello Facebook交流群',
    '花花虚拟信用卡vcc服务交流群',
    '嘿嘿虚拟信用卡vcc'
]
_PLATFORM_AD = (
    r'(?:\b(?:facebook|google|tiktok|meta)\s+ads\b|\badvertisement\b|'
    r'(?:谷歌|Google|脸书|Facebook|Meta|TikTok|抖音)\s*广告)'
)
KEYWORD_RULES = [
    ('vcc', re.compile(r'\bvcc\b', re.I)),
    ('虚拟卡', re.compile(r'虚拟卡|虚拟\s*信用卡')),
    ('绑卡', re.compile(r'绑卡|绑\s*卡')),
    ('开卡', re.compile(r'(?<![不没])(?:开卡|开\s*卡)')),
    ('绑定', re.compile(r'(?<!不)绑定')),
    ('bin', re.compile(r'\bbin\b', re.I)),
    (
        '绑定/绑卡+广告平台',
        re.compile(rf'(?is)(?=.*(?:绑定|绑\s*卡))(?=.*{_PLATFORM_AD})'),
    ),
    (
        '开卡+广告平台',
        re.compile(rf'(?is)(?=.*(?<![不没])(?:开卡|开\s*卡))(?=.*{_PLATFORM_AD})'),
    ),
    (
        'vcc+广告平台',
        re.compile(rf'(?is)(?=.*\bvcc\b)(?=.*{_PLATFORM_AD})'),
    ),
    (
        '虚拟卡+广告平台',
        re.compile(rf'(?is)(?=.*(?:虚拟卡|虚拟\s*信用卡))(?=.*{_PLATFORM_AD})'),
    ),
]


def match_keywords(message_text: str):
    matched = []
    seen = set()
    for label, rx in KEYWORD_RULES:
        if label in seen:
            continue
        if rx.search(message_text):
            matched.append(label)
            seen.add(label)
    return matched


SPAM_SKIP_PATTERNS = [
    re.compile(r'(?i)recover your account'),
    re.compile(r'(?i)SEND ME A MESSAGE FOR ANY KIND OF SERVICE'),
    re.compile(r'(?i)facebook\s+recovery'),
    re.compile(r'(?i)(?:whatsapp|instagram|gmail|yahoo)\s+hacking'),
    re.compile(r'(?i)(?:windows|android|wifi|network|ip address)\s+hacking'),
    re.compile(r'(?i)software\s+cracking'),
    re.compile(r'(?i)website\s+hacking'),
    re.compile(r'(?i)clearing of credit score'),
    re.compile(r'(?i)tower location finder'),
    re.compile(r'(?i)virus available'),
    re.compile(r'(?i)private number available'),
    re.compile(r'(?is)❌\s*NO\s*SCAM'),
]


def should_skip_notification(message_text: str) -> bool:
    if any(rx.search(message_text) for rx in SPAM_SKIP_PATTERNS):
        return True
    if len(re.findall(r'(?i)\bhacking\b', message_text)) >= 2:
        return True
    return False


NOTIFY_TARGET = 'me'
NORMALIZED_TARGET_GROUPS = {name.replace('\ufe0f', '').strip() for name in TARGET_GROUP_NAME}
SUMMARY_OUTPUT_DIR = 'daily_excel_summary'
SUMMARY_HEADERS = ['触发时间(北京时间)', '来源群组', '发送用户', '命中关键词', '消息内容']
_daily_records = {}
_daily_records_lock = asyncio.Lock()
_project_root = None


def _set_project_root(path):
    global _project_root
    _project_root = path


def to_beijing_time(dt):
    return dt + timedelta(hours=8)


def normalize_title(title):
    return (title or '').replace('\ufe0f', '').strip()


def beijing_now():
    return datetime.utcnow() + timedelta(hours=8)


def _seconds_until_next_daily_export(target_hour=18, target_minute=0):
    now = beijing_now()
    target = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    return max(1, int((target - now).total_seconds()))


async def record_hit_for_daily_summary(date_str, time_str, group_title, sender_name, matched, message_text):
    async with _daily_records_lock:
        bucket = _daily_records.setdefault(date_str, [])
        bucket.append({
            'time': time_str,
            'group': group_title,
            'sender': sender_name,
            'keywords': '、'.join(matched),
            'message': message_text,
        })


def export_daily_summary_excel(date_str, rows):
    if Workbook is None:
        print("❌ 未安装 openpyxl，无法导出 Excel。请先执行：python3 -m pip install openpyxl")
        return None
    base_dir = _project_root or os.getcwd()
    output_dir = os.path.join(base_dir, SUMMARY_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{date_str}_监控汇总.xlsx')

    wb = Workbook()
    ws = wb.active
    ws.title = '监控汇总'
    ws.append(SUMMARY_HEADERS)
    for row in rows:
        ws.append([
            row['time'],
            row['group'],
            row['sender'],
            row['keywords'],
            row['message'],
        ])
    wb.save(output_path)
    return output_path


async def daily_summary_scheduler():
    while True:
        wait_seconds = _seconds_until_next_daily_export(18, 0)
        print(f"🗓️ 下次日报导出计划：{wait_seconds} 秒后（北京时间 18:00）")
        await asyncio.sleep(wait_seconds)

        today = beijing_now().strftime('%Y-%m-%d')
        async with _daily_records_lock:
            rows = list(_daily_records.get(today, []))
            _daily_records.clear()
            _daily_records[today] = rows
        output_path = export_daily_summary_excel(today, rows)
        if output_path:
            print(f"📊 今日汇总已导出：{output_path}（共 {len(rows)} 条）")


async def message_handler(event):
    try:
        chat = await event.get_chat()
        sender = await event.get_sender()

        if not hasattr(chat, 'title'):
            return
        normalized_chat_title = normalize_title(chat.title)
        if normalized_chat_title not in NORMALIZED_TARGET_GROUPS:
            return

        message_text = event.text or ''
        if not message_text.strip():
            return

        matched = match_keywords(message_text)
        if not matched:
            return
        if should_skip_notification(message_text):
            print(f"⏭️ 已跳过（垃圾模板过滤）：{chat.title} | {message_text[:100]}...")
            return

        sender_name = sender.first_name if sender else "未知用户"
        if hasattr(sender, 'last_name') and sender.last_name:
            sender_name += f" {sender.last_name}"
        bj_time = to_beijing_time(event.date)
        time_str = bj_time.strftime("%Y-%m-%d %H:%M:%S")
        date_str = bj_time.strftime("%Y-%m-%d")
        hit_display = '、'.join(matched)
        await record_hit_for_daily_summary(
            date_str=date_str,
            time_str=time_str,
            group_title=chat.title,
            sender_name=sender_name,
            matched=matched,
            message_text=message_text,
        )
        notify_content = f"""【关键词监控通知】
🔑 命中关键词：{hit_display}
👤 发送用户：{sender_name}
💬 消息内容：{message_text}
👥 来源群组：{chat.title}
⏰ 触发时间：{time_str}"""
        print(notify_content)
        print(f"✅ 匹配到关键词：{chat.title} | {message_text[:80]}...")
        try:
            await event.client.send_message(NOTIFY_TARGET, notify_content)
        except Exception as send_exc:
            print(f"❌ 推送失败（send_message）：{send_exc}")
    except Exception as exc:
        print(f"❌ 处理消息失败: {exc}")


async def run_monitor():
    cfg = load_config()
    _set_project_root(str(cfg.project_root))
    session_label = cfg.session_name
    retry_seconds = [2, 5, 10, 30]
    retry_idx = 0
    asyncio.create_task(daily_summary_scheduler())
    while True:
        client = None
        try:
            client = build_client(cfg)
            client.add_event_handler(
                message_handler,
                events.NewMessage(incoming=True, outgoing=True),
            )
            print("🔌 正在连接 Telegram...")
            await client.start()
            print(
                f"🚀 Telegram 监控服务已启动（北京时间），监听白名单群；"
                f"关键词正则匹配（{len(KEYWORD_RULES)} 条规则），垃圾模板过滤（{len(SPAM_SKIP_PATTERNS)} 条）；"
                f"命中后打印控制台并用本账号推送到：{NOTIFY_TARGET!r}"
            )
            retry_idx = 0
            await client.run_until_disconnected()
            raise ConnectionError("连接已断开")
        except (asyncio.CancelledError, KeyboardInterrupt):
            raise
        except Exception as exc:
            if isinstance(exc, sqlite3.DatabaseError) and 'file is not a database' in str(exc).lower():
                print(
                    f"❌ 会话文件损坏：{session_label}.session 不是有效的 SQLite 数据库。\n"
                    "   请先备份并删除对应 .session / .session-journal，\n"
                    "   然后重新执行登录（tg-monitor login），再启动监控。"
                )
                return
            wait_seconds = retry_seconds[min(retry_idx, len(retry_seconds) - 1)]
            retry_idx += 1
            print(f"❌ 连接异常：{exc}")
            print(f"⏳ {wait_seconds} 秒后自动重连...")
            await asyncio.sleep(wait_seconds)
        finally:
            if client is None:
                continue
            try:
                await client.disconnect()
            except sqlite3.OperationalError as exc:
                if 'database is locked' in str(exc).lower():
                    print("⚠️ 会话文件被占用（database is locked），已忽略本次断开异常，稍后重试。")
                else:
                    raise
