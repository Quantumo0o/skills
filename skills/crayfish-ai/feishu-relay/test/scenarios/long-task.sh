#!/bin/bash
# 模拟长耗时任务

# 先发送开始通知
/opt/feishu-notifier/bin/notify "🕐 长任务开始" "数据处理任务已启动，预计需要 5 分钟"

# 模拟长时间处理
sleep 10

# 发送完成通知
/opt/feishu-notifier/bin/notify "✅ 长任务完成" "数据处理任务已完成"
