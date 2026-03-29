#!/bin/bash
# Smart Search v2.0 - 智能搜索引擎切换
# 基于搜索意图自动选择 SearX 或 Tavily

QUERY="$1"
MAX_RESULTS="${2:-5}"

# 加载环境变量
if [ -f ~/.openclaw/.env ]; then
    source ~/.openclaw/.env 2>/dev/null || export $(cat ~/.openclaw/.env | grep -v '^#' | xargs)
fi

# 决策逻辑：基于关键词分析搜索意图
decide_engine() {
    local query="$1"
    local query_lower=$(echo "$query" | tr '[:upper:]' '[:lower:]')
    
    # 用户指定优先
    if [[ "$query" == *"用 sear"* ]] || [[ "$query" == *"用 SearX"* ]] || [[ "$query" == *"用 searx"* ]]; then
        echo "searx"
        return
    fi
    
    if [[ "$query" == *"用 tavily"* ]] || [[ "$query" == *"用 Tavily"* ]]; then
        echo "tavily"
        return
    fi
    
    # AI 内容生成场景 → 优先 Tavily（带 AI 摘要）
    if [[ "$query_lower" == *"小红书"* ]] || \
       [[ "$query_lower" == *"写文案"* ]] || \
       [[ "$query_lower" == *"公众号"* ]] || \
       [[ "$query_lower" == *"生成"* ]] || \
       [[ "$query_lower" == *"总结"* ]] || \
       [[ "$query_lower" == *"摘要"* ]] || \
       [[ "$query_lower" == *"提炼"* ]] || \
       [[ "$query_lower" == *"创作"* ]] || \
       [[ "$query_lower" == *"草稿"* ]] || \
       [[ "$query_lower" == *"爆款标题"* ]] || \
       [[ "$query_lower" == *"内容角度"* ]] || \
       [[ "$query_lower" == *"话题标签"* ]] || \
       [[ "$query_lower" == *"写文章"* ]]; then
        echo "tavily"
        return
    fi
    
    # 默认使用 SearX（免费无限）
    echo "searx"
}

ENGINE=$(decide_engine "$QUERY")
echo "🔍 Smart Search: 使用 $ENGINE"
echo ""

# SearX 搜索（免费无限）
call_searx() {
    [ -z "$SEARXNG_URL" ] && { echo "⚠️  SEARXNG_URL 未配置"; return 1; }
    
    RESPONSE=$(curl -s -A "Mozilla/5.0" --max-time 10 \
      "$SEARXNG_URL/search?q=$(echo "$QUERY" | sed 's/ /+/g')&format=json" 2>/dev/null)
    
    # 检查是否返回有效 JSON
    if echo "$RESPONSE" | grep -q '"results"'; then
        echo "$RESPONSE"
        return 0
    else
        return 1
    fi
}

# Tavily 搜索（单 Key，简单直接）
call_tavily() {
    [ -z "$TAVILY_API_KEY" ] && return 1
    
    RESPONSE=$(curl -s -X POST https://api.tavily.com/search \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TAVILY_API_KEY" \
      -m 15 \
      -d "{\"query\": \"$QUERY\", \"max_results\": $MAX_RESULTS, \"include_answer\": true}" 2>/dev/null)
    
    # 检查是否成功
    if echo "$RESPONSE" | grep -q '"results"'; then
        echo "$RESPONSE"
        return 0
    else
        return 1
    fi
}

# 显示 SearX 结果
display_searx() {
    python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', [])
    if not results:
        print('⚠️  无搜索结果')
        sys.exit(1)
    for i, r in enumerate(results[:$MAX_RESULTS], 1):
        print(f\"{i}. {r.get('title', '无标题')}\")
        print(f\"   {r.get('url', '无链接')}\")
        content = r.get('content', '')[:200]
        print(f\"   {content}...\")
        print()
    print(f\"✅ 共找到 {len(results)} 条结果（SearX 免费）\")
except Exception as e:
    print(f'解析失败：{e}')
    sys.exit(1)
"
}

# 显示 Tavily 结果（带 AI 摘要）
display_tavily() {
    python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    answer = data.get('answer', '')
    if answer:
        print('📝 AI 摘要：')
        print(answer)
        print()
    results = data.get('results', [])[:$MAX_RESULTS]
    for i, r in enumerate(results, 1):
        print(f\"{i}. {r.get('title', '无标题')}\")
        print(f\"   {r.get('url', '无链接')}\")
        content = r.get('content', '')[:200]
        print(f\"   {content}...\")
        print()
    print('✅ 搜索成功（Tavily）')
except Exception as e:
    print(f'解析失败：{e}')
"
}

# 主逻辑
case "$ENGINE" in
  "searx")
    RESULT=$(call_searx)
    
    if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
        echo "$RESULT" | display_searx
    else
        echo "⚠️  SearX 不可用，降级到 Tavily..."
        echo ""
        RESULT=$(call_tavily)
        if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
            echo "$RESULT" | display_tavily
        else
            echo "❌ 搜索失败，请检查网络连接"
            exit 1
        fi
    fi
    ;;
  
  "tavily")
    if [ -z "$TAVILY_API_KEY" ]; then
        echo "⚠️  Tavily API Key 未配置"
        echo ""
        echo "📝 当前场景需要 AI 摘要功能（如小红书文案、内容总结等）"
        echo "💡 建议配置 Tavily API Key 以获得更好的体验"
        echo ""
        echo "🔑 获取免费 API Key（2 分钟）："
        echo "   1. 访问 https://tavily.com"
        echo "   2. 注册免费账号（1000 次/月免费）"
        echo "   3. 获取 API Key"
        echo "   4. 添加到 ~/.openclaw/.env："
        echo "      TAVILY_API_KEY=tvly-your-key-here"
        echo ""
        echo "⚡ 或者，我现在用 SearX 为您搜索（无 AI 摘要）："
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        RESULT=$(call_searx)
        if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
            echo "$RESULT" | display_searx
            echo ""
            echo "💡 配置 Tavily 后，AI 内容生成效果会更好哦！"
        else
            echo "❌ 搜索失败，请检查 SearX 配置"
            exit 1
        fi
    else
        RESULT=$(call_tavily)
        
        if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
            echo "$RESULT" | display_tavily
        else
            echo "⚠️  Tavily 暂时不可用，降级到 SearX..."
            echo ""
            RESULT=$(call_searx)
            if [ $? -eq 0 ] && [ -n "$RESULT" ]; then
                echo "$RESULT" | display_searx
            else
                echo "❌ 搜索失败，请检查网络或 SearX 配置"
                exit 1
            fi
        fi
    fi
    ;;
esac
