#!/usr/bin/env python3
"""
Morning Coach Push - 09:00
今日恢复状态 + 训练建议

推送内容包含：
- 今日恢复评分及解读
- HRV和静息心率专业解析
- 睡眠质量分析
- 7日训练概况
- 个性化训练建议
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, "/root/.openclaw/workspace-healthgao/skill/whoop-guru")

from lib.pusher import CoachPushMessage

OUTPUT_FILE = "/root/.openclaw/workspace-healthgao/skill/whoop-guru/data/logs/morning_push.json"


def generate_morning_push():
    """生成早安教练推送"""
    
    # 使用增强版的推送消息
    message = CoachPushMessage.morning()
    
    # 保存推送记录
    result = {
        "type": "morning",
        "timestamp": datetime.now().isoformat(),
        "message": message
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 打印消息供Telegram发送
    print(message)
    
    return result


if __name__ == "__main__":
    generate_morning_push()
