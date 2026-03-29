#!/usr/bin/env python3
"""
Evening Coach Push - 18:00
今日训练完成情况 + 明日建议

推送内容包含：
- 今日训练总结
- 当前恢复状态分析
- 本周训练概况
- 明日训练建议
- 睡眠提醒
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, "/root/.openclaw/workspace-healthgao/skill/whoop-guru")

from lib.pusher import CoachPushMessage

OUTPUT_FILE = "/root/.openclaw/workspace-healthgao/skill/whoop-guru/data/logs/evening_push.json"


def generate_evening_push():
    """生成晚间教练推送"""
    
    # 使用增强版的推送消息
    message = CoachPushMessage.evening()
    
    # 保存推送记录
    result = {
        "type": "evening",
        "timestamp": datetime.now().isoformat(),
        "message": message
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 打印消息供Telegram发送
    print(message)
    
    return result


if __name__ == "__main__":
    generate_evening_push()
