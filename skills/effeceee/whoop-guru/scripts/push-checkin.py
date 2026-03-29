#!/usr/bin/env python3
"""
Check-in Reminder Push - 20:00
训练打卡提醒

推送内容包含：
- 今日训练状态
- 打卡重要性说明
- 打卡格式示例
- 恢复提示
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, "/root/.openclaw/workspace-healthgao/skill/whoop-guru")

from lib.pusher import CoachPushMessage

OUTPUT_FILE = "/root/.openclaw/workspace-healthgao/skill/whoop-guru/data/logs/checkin_push.json"


def generate_checkin_push():
    """生成打卡提醒"""
    
    # 使用增强版的推送消息
    message = CoachPushMessage.checkin_reminder()
    
    # 保存推送记录
    result = {
        "type": "checkin_reminder",
        "timestamp": datetime.now().isoformat(),
        "message": message
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 打印消息供Telegram发送
    print(message)
    
    return result


if __name__ == "__main__":
    generate_checkin_push()
