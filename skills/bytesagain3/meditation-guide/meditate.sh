#!/usr/bin/env bash
CMD="$1"; shift 2>/dev/null; INPUT="$*"
case "$CMD" in
  mindful) cat << 'PROMPT'
You are an expert. Help with: 正念冥想引导. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  breathe) cat << 'PROMPT'
You are an expert. Help with: 呼吸练习. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  body-scan) cat << 'PROMPT'
You are an expert. Help with: 身体扫描. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  sleep) cat << 'PROMPT'
You are an expert. Help with: 睡前冥想. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  focus) cat << 'PROMPT'
You are an expert. Help with: 专注力训练. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  plan) cat << 'PROMPT'
You are an expert. Help with: 21天冥想计划. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  *) cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Meditation Guide — 使用指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  mindful         正念冥想引导
  breathe         呼吸练习
  body-scan       身体扫描
  sleep           睡前冥想
  focus           专注力训练
  plan            21天冥想计划

  Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
EOF
    ;;
esac
