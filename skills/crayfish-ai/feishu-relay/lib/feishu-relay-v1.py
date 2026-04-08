#!/usr/bin/env python3
# feishu-relay.py - Feishu Relay Service
# 飞书中继服务 - 统一通知队列处理

import sqlite3
import time
import subprocess
import sys
import os

# 强制行缓冲输出，确保日志及时写入 journald
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 1)

FEISHU_NOTIFY = "/opt/feishu-notifier/bin/feishu_notify.sh"
DB = "/opt/feishu-notifier/queue/notify-queue.db"
CONFIG_FILE = "/opt/feishu-notifier/config/feishu.env"
MAX_RETRY = 3
POLL_INTERVAL = 30

def process_one():
    """处理队列中的一条消息"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    # 取最早的一条待处理消息
    cursor.execute(
        "SELECT id, title, content, retry FROM queue ORDER BY created_at LIMIT 1"
    )
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return False
    
    msg_id, title, content, retry = row
    
    try:
        # 加载环境变量
        env = os.environ.copy()
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, val = line.strip().split('=', 1)
                        env[key] = val
        
        # 调用 feishu_notify.sh 发送
        result = subprocess.run(
            [FEISHU_NOTIFY, "-t", title, "-m", content],
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )
        
        if result.returncode == 0:
            # 发送成功，删除记录
            cursor.execute("DELETE FROM queue WHERE id = ?", (msg_id,))
            log(f"Sent: {title[:40]}")
        else:
            raise Exception(result.stderr.strip() or "Unknown error")
            
    except Exception as e:
        # 发送失败
        if retry >= MAX_RETRY:
            # 超过重试次数，放弃
            cursor.execute("DELETE FROM queue WHERE id = ?", (msg_id,))
            log(f"Failed permanently: {title[:40]} ({e})")
        else:
            # 增加重试计数
            cursor.execute(
                "UPDATE queue SET retry = retry + 1 WHERE id = ?",
                (msg_id,)
            )
            log(f"Retry {retry + 1}/{MAX_RETRY}: {title[:40]}")
    
    conn.commit()
    conn.close()
    return True

def log(msg):
    """输出日志到 stdout（journald）"""
    timestamp = time.strftime('%H:%M:%S')
    print(f"[{timestamp}] {msg}", flush=True)

def main():
    log("Feishu Relay started")
    log(f"DB: {DB}")
    log(f"Config: {CONFIG_FILE}")
    log(f"Notify script: {FEISHU_NOTIFY}")
    
    while True:
        try:
            had_work = process_one()
            if not had_work:
                time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            log("Shutting down...")
            break
        except Exception as e:
            log(f"Error: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
