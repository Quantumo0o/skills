#!/usr/bin/env python3
"""
火车票搜索模块 - 携程火车票查询

功能:
- 高铁/动车/普快查询
- 换乘方案推荐
- 余票信息
"""

import json
import sys
import re
from typing import List, Dict

# 导入本地模块
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ctrip_client import CtripClient


def search_train(origin: str, dest: str, date: str) -> Dict:
    """
    搜索火车票
    
    Args:
        origin: 出发城市
        dest: 目的城市
        date: 出发日期 (YYYY-MM-DD)
    
    Returns:
        dict: 火车票信息
    """
    client = CtripClient()
    client.launch()
    
    try:
        result = client.search_train(origin, dest, date)
        return result
    finally:
        client.close()


def search_with_transfer(origin: str, dest: str, date: str, via_city: str = None) -> Dict:
    """
    搜索含换乘的火车方案
    
    Args:
        origin: 出发城市
        dest: 目的城市
        date: 出发日期
        via_city: 中转城市（可选，如不指定则自动推荐）
    
    Returns:
        {"direct": [...], "transfer": [...], "recommendation": "..."}
    """
    client = CtripClient()
    client.launch()
    
    try:
        # 搜索直达
        print(f"搜索直达：{origin} → {dest}")
        direct = client.search_train(origin, dest, date)
        
        result = {
            "route": f"{origin}→{dest}",
            "date": date,
            "direct_trains": direct.get('trains', []),
            "transfer_options": []
        }
        
        # 如果有中转城市，搜索换乘方案
        if via_city:
            print(f"搜索换乘：{origin} → {via_city} → {dest}")
            
            # 第一段
            leg1 = client.search_train(origin, via_city, date)
            
            # 第二段（假设同一天，实际应该考虑时间衔接）
            leg2 = client.search_train(via_city, dest, date)
            
            if leg1.get('trains') and leg2.get('trains'):
                result["transfer_options"].append({
                    "via": via_city,
                    "leg1": leg1,
                    "leg2": leg2
                })
        
        # 生成推荐
        result["recommendation"] = _generate_train_recommendation(result)
        
        return result
        
    finally:
        client.close()


def compare_train_types(origin: str, dest: str, date: str) -> Dict:
    """
    对比不同车型（高铁/动车/普快）
    
    Args:
        origin: 出发城市
        dest: 目的城市
        date: 出发日期
    
    Returns:
        {"gaotie": {...}, "dongche": {...}, "pukuai": {...}}
    """
    result = search_train(origin, dest, date)
    trains = result.get('trains', [])
    
    # 分类
    gaotie = [t for t in trains if 'G' in t.get('info', '')]
    dongche = [t for t in trains if 'D' in t.get('info', '')]
    pukuai = [t for t in trains if re.search(r'[KZT]', t.get('info', ''))]
    
    return {
        "route": f"{origin}→{dest}",
        "gaotie": {
            "count": len(gaotie),
            "trains": gaotie[:5]
        },
        "dongche": {
            "count": len(dongche),
            "trains": dongche[:5]
        },
        "pukuai": {
            "count": len(pukuai),
            "trains": pukuai[:5]
        }
    }


def _generate_train_recommendation(result: Dict) -> str:
    """生成火车推荐建议"""
    recommendations = []
    
    direct_count = len(result.get('direct_trains', []))
    
    if direct_count == 0:
        recommendations.append("无直达车次，建议考虑换乘")
    elif direct_count < 3:
        recommendations.append("直达车次较少，建议提前预订")
    else:
        recommendations.append(f"有{direct_count}趟直达车次，选择较多")
    
    # 检查换乘选项
    transfer_count = len(result.get('transfer_options', []))
    if transfer_count > 0:
        recommendations.append(f"找到{transfer_count}个换乘方案，可作备选")
    
    return " | ".join(recommendations)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "search" and len(sys.argv) >= 5:
        result = search_train(sys.argv[2], sys.argv[3], sys.argv[4])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "transfer" and len(sys.argv) >= 5:
        origin = sys.argv[2]
        dest = sys.argv[3]
        date = sys.argv[4]
        via = sys.argv[5] if len(sys.argv) > 5 else None
        result = search_with_transfer(origin, dest, date, via)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "compare" and len(sys.argv) >= 5:
        result = compare_train_types(sys.argv[2], sys.argv[3], sys.argv[4])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        print("用法:")
        print("  python train_search.py search <from> <to> <date>")
        print("  python train_search.py transfer <from> <to> <date> [via]")
        print("  python train_search.py compare <from> <to> <date>")
        sys.exit(1)


if __name__ == "__main__":
    main()
