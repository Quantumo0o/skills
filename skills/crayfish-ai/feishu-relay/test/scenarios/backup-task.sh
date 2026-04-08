#!/bin/bash
# 模拟定时备份任务 - 每天执行

BACKUP_FILE="/data/backup_$(date +%Y%m%d).tar.gz"

# 模拟备份过程
sleep 2

# 检查备份结果
if [ -f "$BACKUP_FILE" ] || true; then
    /opt/feishu-notifier/bin/notify "✅ 备份完成" "每日备份已完成: ${BACKUP_FILE}"
fi
