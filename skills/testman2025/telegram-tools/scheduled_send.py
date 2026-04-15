#!/usr/bin/env python3
import asyncio
import os
import time
from dotenv import load_dotenv
from telethon import TelegramClient

# 加载.env配置
load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
session_name = os.getenv("TELEGRAM_SESSION_NAME", "xiaomei_session")
phone = os.getenv("TELEGRAM_PHONE")
proxy_host = os.getenv("TELEGRAM_PROXY_HTTP_HOST", "127.0.0.1")
proxy_port = int(os.getenv("TELEGRAM_PROXY_HTTP_PORT", 1087))
proxy = ("http", proxy_host, proxy_port)

# 配置项（可自定义修改）
SEND_INTERVAL_HOURS = 3  # 发送间隔：3小时
TARGET_GROUP_ID = -5204394907  # 目标群：嘿嘿虚拟信用卡vcc
SEND_CONTENT = "vcc找我"  # 发送内容

async def send_msg():
    # 每次发送新建客户端，避免长期连接bug，用独立session避免和监控脚本冲突
    client = TelegramClient("xiaomei_send_session", api_id, api_hash, proxy=proxy, receive_updates=False)
    await client.start(phone=phone)
    try:
        await client.send_message(TARGET_GROUP_ID, SEND_CONTENT)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✅ 消息发送成功：{SEND_CONTENT}")
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ 发送失败：{str(e)}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    print(f"✅ 定时群发服务已启动，每{SEND_INTERVAL_HOURS}小时向群[嘿嘿虚拟信用卡vcc]发送消息：{SEND_CONTENT}")
    while True:
        asyncio.run(send_msg())
        # 等待指定间隔
        time.sleep(SEND_INTERVAL_HOURS * 3600)
