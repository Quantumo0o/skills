#!/usr/bin/env python3
# 获取股票信息脚本
# 数据来源：同花顺 (10jqka.com.cn)

import sys
import requests
import re
from datetime import datetime

def fetch_stock_info(code, name):
    """获取股票行情信息"""
    try:
        # 同花顺股票页面
        url = f"https://stockpage.10jqka.com.cn/{code}/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            text = response.text
            
            # 提取综合评分
            score = "N/A"
            score_match = re.search(r'综合判断：([\d.]+) 分', text)
            if score_match:
                score = score_match.group(1)
            
            # 提取短期趋势
            short_trend = "N/A"
            short_match = re.search(r'短期趋势：\s*([^\n。]+)', text)
            if short_match:
                short_trend = short_match.group(1).strip()
            
            # 提取平均成本
            avg_cost = "N/A"
            cost_match = re.search(r'近期的平均成本为 ([\d.]+) 元', text)
            if cost_match:
                avg_cost = cost_match.group(1)
            
            # 提取机构评级
            rating = "N/A"
            rating_match = re.search(r'机构评级以 (\w+) 为主', text)
            if rating_match:
                rating = rating_match.group(1)
            
            # 生成建议（基于评分和趋势）
            suggestion = "观望"
            try:
                if score != "N/A":
                    score_val = float(score)
                    if score_val >= 7:
                        suggestion = "强烈推荐"
                    elif score_val >= 6:
                        suggestion = "关注"
                    elif score_val >= 5:
                        suggestion = "持有"
                    elif score_val >= 4:
                        suggestion = "观望"
                    else:
                        suggestion = "谨慎"
                    
                    # 根据趋势调整
                    if "上涨" in short_trend:
                        if suggestion == "观望":
                            suggestion = "关注"
                    elif "回调" in short_trend or "下跌" in short_trend:
                        if suggestion in ["强烈推荐", "关注"]:
                            suggestion = "持有"
            except:
                pass
            
            # 输出 Markdown 表格行
            print(f"| {code} | {name} | {avg_cost} | {score} | {suggestion} |")
            print(f"  - 短期：{short_trend}")
            print(f"  - 评级：{rating}")
            
        else:
            print(f"| {code} | {name} | 获取失败 | - | 观望 |")
            
    except Exception as e:
        print(f"| {code} | {name} | 错误 | - | 观望 |")
        print(f"错误：{str(e)}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        code = sys.argv[1]
        name = sys.argv[2]
        fetch_stock_info(code, name)
    else:
        print("用法：python3 fetch-stock-info.py <股票代码> <股票名称>")
        sys.exit(1)
