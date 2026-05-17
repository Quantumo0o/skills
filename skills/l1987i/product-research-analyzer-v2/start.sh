#!/bin/bash
# Product Research Analyzer | 产品调研分析师 - 快速启动脚本

echo "======================================================================"
echo "📊 Product Research Analyzer | 产品调研分析师"
echo "======================================================================"
echo ""
echo "请选择使用模式："
echo ""
echo "  1) 交互式模式（推荐）- 通过对话引导输入"
echo "  2) 命令行模式 - 直接提供参数"
echo "  3) 查看使用示例"
echo "  4) 查看帮助文档"
echo ""
read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "启动交互式模式..."
        echo ""
        python3 scripts/research_interactive.py
        ;;
    2)
        echo ""
        read -p "请输入产品名称： " product
        read -p "请输入调研问题（可选，直接回车跳过）： " questions
        read -p "请输入对标项目（可选，默认蝉小狗）： " target
        
        if [ -z "$target" ]; then
            target="蝉小狗"
        fi
        
        if [ -z "$questions" ]; then
            python3 scripts/research.py "{\"product_name\": \"$product\", \"target_project\": \"$target\"}"
        else
            python3 scripts/research.py "{\"product_name\": \"$product\", \"research_questions\": \"$questions\", \"target_project\": \"$target\"}"
        fi
        ;;
    3)
        echo ""
        echo "查看使用示例..."
        echo ""
        cat EXAMPLES.md | head -100
        ;;
    4)
        echo ""
        echo "查看帮助文档..."
        echo ""
        cat README.md | head -100
        ;;
    *)
        echo "无效的选项，请输入 1-4"
        ;;
esac
