#!/bin/bash
# 模拟系统监控 - 每5分钟执行

CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
CPU_INT=${CPU_USAGE%.*}

if [ "$CPU_INT" -gt 80 ]; then
    /opt/feishu-notifier/bin/notify "⚠️ CPU告警" "CPU使用率 ${CPU_USAGE}%"
fi

echo "CPU监控完成: ${CPU_USAGE}%"
