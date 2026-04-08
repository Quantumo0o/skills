#!/usr/bin/env python3
"""Feishu Relay SDK for Python"""
import subprocess
import os

FEISHU_NOTIFY_CMD = "/opt/feishu-notifier/bin/notify"
FEISHU_TASK_CMD = "/opt/feishu-notifier/bin/feishu-task-v2"

def notify(title="通知", content=""):
    """发送立即通知"""
    subprocess.run([FEISHU_NOTIFY_CMD, title, content], check=False)

def notify_later(minutes, title, content=""):
    """发送定时通知"""
    subprocess.run([FEISHU_TASK_CMD, "in", str(minutes), title, content], check=False)

if __name__ == "__main__":
    notify("测试", "Python SDK 工作正常")
