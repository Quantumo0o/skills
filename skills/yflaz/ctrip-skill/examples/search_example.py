#!/usr/bin/env python3
"""
携程搜索 Skill 使用示例

演示：
1. 上海→曼谷机票搜索
2. 多程路线规划（上海 - 曼谷 - 清迈 - 吉隆坡）
3. 火车票搜索
"""

import sys
import os

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ctrip_client import CtripClient
from flight_search import search_one_way, search_multi_city
from train_search import search_train
from route_planner import plan_optimal_route


def example_flight_search():
    """示例 1：上海→曼谷机票搜索"""
    print("=" * 60)
    print("✈ 示例 1：上海→曼谷机票搜索")
    print("=" * 60)
    
    result = search_one_way("上海", "曼谷", "2026-10-01")
    
    print(f"路线：{result.get('route')}")
    print(f"日期：{result.get('date')}")
    print(f"最低价：¥{result.get('min_price', 'N/A')}")
    print(f"价格选项：{len(result.get('prices', []))} 个")
    
    if result.get('error'):
        print(f"⚠ 错误：{result['error']}")
    
    print()
    return result


def example_multi_city():
    """示例 2：多程路线规划"""
    print("=" * 60)
    print("🗺 示例 2：多程路线规划（上海 - 曼谷 - 清迈 - 吉隆坡）")
    print("=" * 60)
    
    routes = [
        {"from": "上海", "to": "曼谷", "date": "2026-10-01"},
        {"from": "曼谷", "to": "清迈", "date": "2026-10-04"},
        {"from": "清迈", "to": "吉隆坡", "date": "2026-10-07"},
        {"from": "吉隆坡", "to": "上海", "date": "2026-10-10"}
    ]
    
    result = search_multi_city(routes)
    
    print(f"航段数：{result.get('segments')}")
    print(f"预估总价：¥{result.get('total_price', 'N/A')}")
    print(f"推荐建议：{result.get('recommendation')}")
    print()
    
    return result


def example_route_planning():
    """示例 3：智能行程规划"""
    print("=" * 60)
    print("📅 示例 3：智能行程规划（8 天 4 城）")
    print("=" * 60)
    
    cities = ["上海", "曼谷", "清迈", "吉隆坡"]
    days = 8
    
    result = plan_optimal_route(cities, days, budget=3000, preference="price")
    
    print(f"最优路线：{' → '.join(result.get('optimal_route', []))}")
    print(f"总天数：{result.get('total_days')} 天")
    print(f"预估费用：¥{result.get('estimated_price', 'N/A')}")
    print()
    
    print("每日计划：")
    for plan in result.get('daily_plan', []):
        print(f"  {plan['day_range']}: {plan['city']} ({plan['days']}天)")
        print(f"    亮点：{', '.join(plan['highlights'])}")
    print()
    
    print(f"推荐：{result.get('recommendation')}")
    print()
    
    return result


def example_train_search():
    """示例 4：火车票搜索"""
    print("=" * 60)
    print("🚄 示例 4：北京→上海火车票搜索")
    print("=" * 60)
    
    result = search_train("北京", "上海", "2026-10-01")
    
    print(f"路线：{result.get('route')}")
    print(f"日期：{result.get('date')}")
    print(f"车次数：{len(result.get('trains', []))}")
    
    if result.get('error'):
        print(f"⚠ 错误：{result['error']}")
    
    print()
    return result


def main():
    """运行所有示例"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "携程搜索 Skill 使用示例" + " " * 15 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    try:
        # 示例 1：单程机票
        example_flight_search()
        
        # 示例 2：多程机票
        example_multi_city()
        
        # 示例 3：行程规划
        example_route_planning()
        
        # 示例 4：火车票（可选，耗时较长）
        # example_train_search()
        
        print("=" * 60)
        print("✅ 所有示例执行完成！")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⚠ 用户中断")
    except Exception as e:
        print(f"\n✗ 执行错误：{str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
