#!/usr/bin/env python3
"""
机票搜索模块 - 支持多程/往返/单程

功能:
- 单程/往返/多程搜索
- 多日期价格对比
- 最优路线推荐（价格/时间）
"""

import json
import re
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 导入本地模块
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ctrip_client import CtripClient


def search_one_way(origin: str, dest: str, date: str) -> Dict:
    """
    单程机票搜索
    
    Args:
        origin: 出发城市
        dest: 目的城市
        date: 出发日期 (YYYY-MM-DD)
    
    Returns:
        dict: 搜索结果
    """
    client = CtripClient()
    client.launch()
    
    try:
        result = client.search_flight(origin, dest, date)
        return result
    finally:
        client.close()


def search_round_trip(origin: str, dest: str, depart_date: str, return_date: str) -> Dict:
    """
    往返机票搜索
    
    Args:
        origin: 出发城市
        dest: 目的城市
        depart_date: 去程日期
        return_date: 返程日期
    
    Returns:
        dict: {"outbound": {...}, "inbound": {...}, "total_price": ...}
    """
    client = CtripClient()
    client.launch()
    
    try:
        # 搜索去程
        outbound = client.search_flight(origin, dest, depart_date)
        
        # 搜索返程
        inbound = client.search_flight(dest, origin, return_date)
        
        total_price = outbound.get('min_price', 0) + inbound.get('min_price', 0)
        
        return {
            "outbound": outbound,
            "inbound": inbound,
            "total_price": total_price,
            "route": f"{origin}↔{dest}"
        }
    finally:
        client.close()


def search_multi_city(routes: List[Dict]) -> Dict:
    """
    多程搜索
    
    Args:
        routes: [{"from": "上海", "to": "曼谷", "date": "2026-10-01"}, ...]
    
    Returns:
        {"total_price": 2600, "routes": [...], "recommendation": "..."}
    """
    client = CtripClient()
    client.launch()
    
    try:
        results = []
        total_price = 0
        
        for route in routes:
            print(f"搜索第 {len(results)+1} 段：{route['from']} → {route['to']}")
            result = client.search_flight(route["from"], route["to"], route["date"])
            results.append(result)
            
            # 解析最低价格
            min_price = _parse_min_price(result.get("prices", []))
            total_price += min_price
        
        return {
            "routes": results,
            "total_price": total_price,
            "segments": len(routes),
            "recommendation": _generate_recommendation(results)
        }
    finally:
        client.close()


def compare_dates(origin: str, dest: str, dates: List[str]) -> Dict:
    """
    多日期价格对比
    
    Args:
        origin: 出发城市
        dest: 目的城市
        dates: 日期列表
    
    Returns:
        {"best_date": "...", "prices": [...]}
    """
    client = CtripClient()
    client.launch()
    
    try:
        price_list = []
        
        for date in dates:
            result = client.search_flight(origin, dest, date)
            min_price = result.get('min_price', 0)
            price_list.append({
                "date": date,
                "price": min_price
            })
            print(f"{date}: ¥{min_price}")
        
        # 找出最便宜的日期
        best = min(price_list, key=lambda x: x['price']) if price_list else None
        
        return {
            "route": f"{origin}→{dest}",
            "prices": price_list,
            "best_date": best['date'] if best else None,
            "best_price": best['price'] if best else 0
        }
    finally:
        client.close()


def _parse_min_price(prices: List[str]) -> int:
    """解析最低价格"""
    min_p = float('inf')
    for p in prices:
        match = re.search(r'[¥￥]([\d,]+)', str(p))
        if match:
            price = int(match.group(1).replace(',', ''))
            min_p = min(min_p, price)
    return min_p if min_p != float('inf') else 0


def _generate_recommendation(results: List[Dict]) -> str:
    """生成推荐建议"""
    if not results:
        return "暂无数据"
    
    total = sum(_parse_min_price(r.get('prices', [])) for r in results)
    segments = len(results)
    
    recommendations = []
    
    if segments >= 3:
        recommendations.append("多程旅行建议购买联程机票，可省 10-15%")
    
    if total > 5000:
        recommendations.append("总价较高，建议提前 45-60 天预订")
    elif total > 2000:
        recommendations.append("建议提前 30 天预订")
    else:
        recommendations.append("价格合适，可考虑近期出行")
    
    # 检查是否有廉航
    budget_airlines = ['春秋', '亚航', '狮航', '酷航']
    for result in results:
        for flight in result.get('flights', []):
            if any(airline in flight.get('info', '') for airline in budget_airlines):
                recommendations.append("⚠ 注意：包含廉航航班，行李额需另购")
                break
    
    return " | ".join(recommendations)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "oneway" and len(sys.argv) >= 5:
        result = search_one_way(sys.argv[2], sys.argv[3], sys.argv[4])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "roundtrip" and len(sys.argv) >= 6:
        result = search_round_trip(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "multi" and len(sys.argv) >= 3:
        # 解析多程路线：from1,to1,date1;from2,to2,date2;...
        routes_str = sys.argv[2]
        routes = []
        for segment in routes_str.split(';'):
            parts = segment.split(',')
            if len(parts) >= 3:
                routes.append({
                    "from": parts[0],
                    "to": parts[1],
                    "date": parts[2]
                })
        result = search_multi_city(routes)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "compare" and len(sys.argv) >= 4:
        origin = sys.argv[2]
        dest = sys.argv[3]
        # 生成未来 7 天日期
        dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
        result = compare_dates(origin, dest, dates)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        print("用法:")
        print("  python flight_search.py oneway <from> <to> <date>")
        print("  python flight_search.py roundtrip <from> <to> <depart> <return>")
        print("  python flight_search.py multi '<from1,to1,date1;from2,to2,date2;...>'")
        print("  python flight_search.py compare <from> <to>")
        sys.exit(1)


if __name__ == "__main__":
    main()
