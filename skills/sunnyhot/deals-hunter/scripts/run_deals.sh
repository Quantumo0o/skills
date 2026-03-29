#!/bin/bash
# Deals Hunter 运行脚本 - 支持分段发送到 Discord

set -e

WORKSPACE="/Users/xufan65/.openclaw/workspace/skills/deals-hunter"
CHANNEL_ID="1482243346692051105"

# 运行 Python 脚本
cd "$WORKSPACE"
OUTPUT=$(python3 scripts/deals-hunter-v3.py 2>&1)

# 提取分段
CHUNKS=$(echo "$OUTPUT" | grep -A 1000000 "DISCORD_CHUNK_1" | grep -B 1000000 "END_CHUNK" | grep -v "DISCORD_CHUNK" | grep -v "END_CHUNK")

# 如果有分段，逐个发送
if [ -n "$CHUNKS" ]; then
  # 分割成多个消息
  echo "$CHUNKS" | while IFS= read -r line; do
    if [[ $line == "---" ]]; then
      # 发送当前累积的消息
      if [ -n "$MESSAGE" ]; then
        openclaw message send discord --to "$CHANNEL_ID" "$MESSAGE"
        MESSAGE=""
        sleep 1
      fi
    else
      MESSAGE="$MESSAGE
$line"
    fi
  done
  
  # 发送最后一部分
  if [ -n "$MESSAGE" ]; then
    openclaw message send discord --to "$CHANNEL_ID" "$MESSAGE"
  fi
else
  # 如果没有分段标记，直接发送输出
  openclaw message send discord --to "$CHANNEL_ID" "$OUTPUT"
fi

echo "✅ Deals Hunter 完成"
