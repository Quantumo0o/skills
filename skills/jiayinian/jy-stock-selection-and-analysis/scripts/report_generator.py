#!/usr/bin/env python3
"""
股票分析报告生成器 - 辅助脚本
用于验证数据格式和生成报告框架
"""

import json
from datetime import datetime
from typing import Dict, List, Any


def validate_financial_data(data: Dict[str, Any]) -> bool:
    """验证财务数据完整性"""
    required_fields = ['revenue', 'gross_profit', 'net_profit', 'deducted_net_profit']
    
    if 'reports' not in data:
        return False
    
    for report in data['reports']:
        for field in required_fields:
            if field not in report:
                print(f"缺少字段: {field}")
                return False
    
    return True


def format_table_row(cells: List[str]) -> str:
    """格式化Markdown表格行"""
    return "| " + " | ".join(cells) + " |"


def generate_financial_table(reports: List[Dict], currency: str = "百万元") -> str:
    """生成核心财务指标表格"""
    lines = []
    lines.append(f"（单位：{currency}，增长率除外）\n")
    lines.append(format_table_row(["报告期", "营业总收入", "毛利润", "归属净利润", "扣非净利润"]))
    lines.append(format_table_row(["-" * 10, "-" * 12, "-" * 10, "-" * 12, "-" * 12]))
    
    for report in reports:
        period = report.get('period', 'N/A')
        revenue = f"{report.get('revenue', 0):,.2f}"
        gross_profit = f"{report.get('gross_profit', 0):,.2f}"
        net_profit = f"{report.get('net_profit', 0):,.2f}"
        deducted = f"{report.get('deducted_net_profit', 0):,.2f}"
        
        lines.append(format_table_row([period, revenue, gross_profit, net_profit, deducted]))
    
    return "\n".join(lines)


def generate_growth_table(reports: List[Dict]) -> str:
    """生成增长率表格"""
    lines = []
    lines.append(format_table_row(["指标", "同比", "环比"]))
    lines.append(format_table_row(["-" * 10, "-" * 10, "-" * 10]))
    
    if reports:
        latest = reports[0]
        yoy = latest.get('yoy_growth', 'N/A')
        qoq = latest.get('qoq_growth', 'N/A')
        lines.append(format_table_row(["最新报告期", f"{yoy}%", f"{qoq}%"]))
    
    return "\n".join(lines)


def generate_valuation_table(valuation: Dict[str, Any]) -> str:
    """生成估值指标表格"""
    lines = []
    lines.append(format_table_row(["指标", "数值"]))
    lines.append(format_table_row(["-" * 10, "-" * 15]))
    
    fields = [
        ('最新价', 'price', '元'),
        ('总市值', 'market_cap', '亿元'),
        ('PE (TTM)', 'pe_ttm', ''),
        ('PB (LF)', 'pb_lf', ''),
        ('PEG', 'peg', ''),
        ('股息率', 'dividend_yield', '%')
    ]
    
    for label, key, unit in fields:
        value = valuation.get(key, 'N/A')
        if unit:
            value = f"{value} {unit}" if value != 'N/A' else 'N/A'
        lines.append(format_table_row([label, str(value)]))
    
    return "\n".join(lines)


def generate_chart_instruction(chart_type: str, title: str, data: Dict) -> str:
    """生成图表绘制指令"""
    instructions = {
        'bar': f"""
**【图表】{title}**
- 图表类型：叠加柱状图
- X轴：{data.get('x_axis', [])}
- 数据系列：{data.get('series', [])}
- 输出格式：PNG
""",
        'line': f"""
**【图表】{title}**
- 图表类型：叠加折线图
- X轴：{data.get('x_axis', [])}
- 数据系列：{data.get('series', [])}
- 输出格式：PNG
""",
        'pie': f"""
**【图表】{title}**
- 图表类型：饼图
- 标签：{data.get('labels', [])}
- 数据：{data.get('data', [])}
- 输出格式：PNG
"""
    }
    
    return instructions.get(chart_type, '')


def check_data_completeness(stock_data: Dict) -> List[str]:
    """检查数据完整性并返回缺失项"""
    missing = []
    
    if not stock_data.get('basic_info'):
        missing.append('公司基本信息')
    
    if not stock_data.get('ownership'):
        missing.append('股权结构')
    
    if not stock_data.get('financial_reports') or len(stock_data.get('financial_reports', [])) < 5:
        missing.append('完整财务数据（至少5期）')
    
    if not stock_data.get('valuation'):
        missing.append('估值数据')
    
    if not stock_data.get('forecasts'):
        missing.append('机构预期')
    
    return missing


def main():
    """主函数 - 示例用法"""
    print("股票分析报告生成器 - 辅助工具")
    print("=" * 50)
    
    # 示例数据验证
    sample_data = {
        'stock_code': '000001.SZ',
        'stock_name': '示例公司',
        'reports': [
            {
                'period': '2025H1',
                'revenue': 12345.67,
                'gross_profit': 5678.90,
                'net_profit': 3456.78,
                'deducted_net_profit': 3234.56
            }
        ]
    }
    
    if validate_financial_data(sample_data):
        print("✓ 数据验证通过")
        print("\n生成的财务表格：")
        print(generate_financial_table(sample_data['reports']))
    else:
        print("✗ 数据验证失败")


if __name__ == '__main__':
    main()
