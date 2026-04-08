#!/bin/bash
# 模拟 cron 定时任务

echo "[$(date '+%H:%M:%S')] Cron 任务执行"
/opt/feishu-notifier/bin/notify "⏰ 定时任务" "Cron 定时任务执行: $(date)"
