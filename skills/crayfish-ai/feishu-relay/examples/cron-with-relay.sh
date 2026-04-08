#!/bin/bash
# 使用 feishu-relay 的定时任务示例

# 方案1: 直接调用 notify
/opt/feishu-notifier/bin/notify "定时提醒" "该睡觉了"

# 方案2: 使用脚本包装
echo "该睡觉了" | /opt/feishu-notifier/bin/notify "定时提醒"
