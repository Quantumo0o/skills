#!/bin/bash

# 法律检索技能测试脚本

echo "=========================================="
echo "  法律检索技能 - 功能测试"
echo "=========================================="
echo ""

cd /workspace/projects/agents/legal-ai-team/legal-ceo/workspace

echo "📋 测试1: 基本检索 - 合同违约责任"
echo "----------------------------------------"
python skills/legal-retrieval/legal-retrieval.py \
  --query "合同违约责任" \
  --limit 3 \
  --output json

echo ""
echo "=========================================="
echo ""
echo "📋 测试2: 指定数据源 - 只检索法规库"
echo "----------------------------------------"
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任" \
  --sources regulations \
  --limit 3 \
  --output human

echo ""
echo "=========================================="
echo ""
echo "✅ 测试完成！"
echo ""
