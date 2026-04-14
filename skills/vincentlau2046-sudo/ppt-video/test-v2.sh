#!/bin/bash
# PPT to Video v2.0 测试脚本

echo "=== PPT to Video v2.0 测试 ==="
echo ""

# 测试 1: 帮助信息（无参数）
echo "测试 1: 无参数运行（应报错）"
/home/Vincent/node-24.14.0-lts/bin/node /home/Vincent/.openclaw/workspace/skills/ppt-video/scripts/generate.js
echo ""

# 测试 2: 指定输入目录
echo "测试 2: 指定输入目录"
INPUT_DIR="/home/Vincent/.openclaw/workspace/wechat_articles/daily/presentation/2026-04-11"
if [ -d "$INPUT_DIR" ]; then
  echo "输入目录存在：$INPUT_DIR"
  /home/Vincent/node-24.14.0-lts/bin/node /home/Vincent/.openclaw/workspace/skills/ppt-video/scripts/generate.js \
    --input "$INPUT_DIR" \
    --project-name test_2026_04_11 \
    --ai-rewrite=false \
    --cleanup=false
else
  echo "输入目录不存在，跳过测试"
fi
echo ""

echo "=== 测试完成 ==="
