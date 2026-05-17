#!/bin/bash
# 基金经理观点分析 Skill - 入口脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 检查 mcporter 是否安装
if ! command -v mcporter &> /dev/null; then
    echo "❌ mcporter 未安装，请先运行：npm install -g mcporter"
    exit 1
fi

# 检查 MCP 服务配置
echo "检查 MCP 服务配置..."
if mcporter list 2>/dev/null | grep -q "jy-financedata"; then
    echo "✅ MCP 服务配置正常"
else
    echo "⚠️  未检测到聚源 MCP 服务配置"
    echo ""
    echo "请先配置 MCP 服务 (需要 JY_API_KEY)"
    echo ""
    echo "配置命令:"
    echo "  mcporter config add jy-financedata-tool --url \"https://api.gildata.com/mcp-servers/aidata-assistant-srv-tool?token=你的 JY_API_KEY\""
    echo "  mcporter config add jy-financedata-api --url \"https://api.gildata.com/mcp-servers/aidata-assistant-srv-api?token=你的 JY_API_KEY\""
    echo ""
    echo "申请 JY_API_KEY: 发送邮件至 datamap@gildata.com"
    exit 1
fi

# 显示使用说明
echo ""
echo "=========================================="
echo "📊 基金经理观点分析"
echo "=========================================="
echo ""
echo "用法 1: 准备分析数据"
echo "  $0 <行业> <季度 1> <季度 2>"
echo "  示例：$0 新能源 2025Q3 2025Q4"
echo ""
echo "用法 2: 生成报告 (已有分析结果)"
echo "  python3 scripts/generate_report.py <request.json> <result.json>"
echo ""
echo "=========================================="
echo ""

if [ $# -ge 3 ]; then
    python3 "$SCRIPT_DIR/scripts/analyze_viewpoints.py" "$1" "$2" "$3"
else
    echo "请提供参数：行业 季度 1 季度 2"
    echo "示例：$0 新能源 2025Q3 2025Q4"
fi
