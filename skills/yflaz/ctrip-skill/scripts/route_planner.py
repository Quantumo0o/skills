#!/usr/bin/env python3
"""
行程规划引擎 - 最优路线推荐

功能:
- 多城市自动排序（最省钱/最省时）
- 每日行程建议
- 预算估算
- 景点推荐
"""

import json
import sys
from itertools import permutations
from typing import List, Dict, Optional
from datetime import datetime, timedelta

# 导入本地模块
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from flight_search import search_multi_city


# 热门城市景点数据库（简化版）
CITY_ATTRACTIONS = {
    "上海": ["外滩", "东方明珠", "豫园", "南京路", "迪士尼"],
    "曼谷": ["大皇宫", "卧佛寺", "湄南河", "考山路", "乍都乍周末市场"],
    "清迈": ["素贴山", "清迈古城", "夜间动物园", "丛林飞跃", "周日夜市"],
    "吉隆坡": ["双子塔", "独立广场", "茨厂街", "黑风洞", "中央市场"],
    "新加坡": ["滨海湾花园", "鱼尾狮", "环球影城", "牛车水", "小印度"],
    "东京": ["浅草寺", "东京塔", "涩谷", "新宿", "秋叶原"],
    "首尔": ["景福宫", "明洞", "南山塔", "弘大", "北村韩屋村"],
    "巴黎": ["埃菲尔铁塔", "卢浮宫", "凯旋门", "塞纳河", "蒙马特"],
    "伦敦": ["大本钟", "伦敦眼", "大英博物馆", "塔桥", "白金汉宫"],
    "纽约": ["自由女神", "时代广场", "中央公园", "大都会博物馆", "布鲁克林大桥"]
}

# 城市间参考距离（公里，用于估算时间）
CITY_DISTANCES = {
    ("上海", "曼谷"): 2900,
    ("上海", "清迈"): 2600,
    ("上海", "吉隆坡"): 3800,
    ("上海", "新加坡"): 3900,
    ("曼谷", "清迈"): 700,
    ("曼谷", "吉隆坡"): 1200,
    ("清迈", "吉隆坡"): 1600,
    ("吉隆坡", "新加坡"): 350
}


def plan_optimal_route(cities: List[str], days: int, budget: Optional[float] = None, 
                       preference: str = "price") -> Dict:
    """
    规划最优路线
    
    Args:
        cities: 城市列表 ["上海", "曼谷", "清迈", "吉隆坡"]
        days: 总天数
        budget: 预算（可选）
        preference: "price" 或 "time"
    
    Returns:
        {"optimal_route": [...], "total_price": 2600, "daily_plan": [...]}
    """
    if len(cities) < 2:
        return {"error": "至少需要 2 个城市"}
    
    print(f"🗺 规划路线：{cities}, {days}天，偏好：{preference}")
    
    # 固定起点
    start = cities[0]
    rest = cities[1:]
    
    best_route = None
    best_price = float('inf')
    best_time = float('inf')
    
    # 计算所有排列组合
    route_options = []
    
    for perm in permutations(rest):
        route = [start] + list(perm)
        
        # 计算总距离（时间代理）
        total_distance = 0
        for i in range(len(route) - 1):
            city1, city2 = route[i], route[i+1]
            dist = CITY_DISTANCES.get((city1, city2), CITY_DISTANCES.get((city2, city1), 2000))
            total_distance += dist
        
        # 估算价格（简化：距离 * 0.5 元/公里）
        estimated_price = total_distance * 0.5
        
        route_options.append({
            "route": route,
            "distance": total_distance,
            "estimated_price": estimated_price
        })
        
        # 根据偏好选择最优
        if preference == "price" and estimated_price < best_price:
            best_price = estimated_price
            best_route = route
        elif preference == "time" and total_distance < best_time:
            best_time = total_distance
            best_route = route
    
    # 如果没有找到（理论上不会），选第一个
    if not best_route and route_options:
        best_route = route_options[0]["route"]
        best_price = route_options[0]["estimated_price"]
    
    # 生成每日计划
    daily_plan = _generate_daily_plan(best_route, days)
    
    # 生成预算详情
    budget_detail = _calculate_budget(best_route, daily_plan)
    
    return {
        "cities": cities,
        "optimal_route": best_route,
        "total_days": days,
        "preference": preference,
        "estimated_price": int(best_price),
        "daily_plan": daily_plan,
        "budget_detail": budget_detail,
        "recommendation": _generate_route_recommendation(best_route, days, budget)
    }


def _generate_daily_plan(route: List[str], days: int) -> List[Dict]:
    """生成每日行程计划"""
    daily_plan = []
    cities_count = len(route)
    
    # 平均分配天数，剩余天数加到最后一个城市
    base_days = days // cities_count
    extra_days = days % cities_count
    
    current_day = 1
    
    for i, city in enumerate(route):
        city_days = base_days + (1 if i == cities_count - 1 else 0)
        if extra_days > 0 and i == cities_count - 1:
            city_days += extra_days
        
        # 获取景点
        attractions = CITY_ATTRACTIONS.get(city, ["市中心", "当地市场", "博物馆"])
        
        plan = {
            "day_range": f"第{current_day}-{current_day + city_days - 1}天",
            "city": city,
            "days": city_days,
            "highlights": attractions[:3],
            "activities": _suggest_activities(city, city_days)
        }
        
        daily_plan.append(plan)
        current_day += city_days
    
    return daily_plan


def _suggest_activities(city: str, days: int) -> List[str]:
    """根据城市和天数推荐活动"""
    attractions = CITY_ATTRACTIONS.get(city, [])
    activities = []
    
    if days >= 3:
        activities.append(f"深度游览{city}主要景点")
        activities.append("体验当地美食和文化")
        activities.append("购物和休闲")
    elif days == 2:
        activities.append(f"游览{attractions[0] if attractions else '市中心'}")
        activities.append(f"探索{attractions[1] if len(attractions) > 1 else '当地特色'}")
    else:
        activities.append(f"快速游览{attractions[0] if attractions else '主要景点'}")
    
    return activities


def _calculate_budget(route: List[str], daily_plan: List[Dict]) -> Dict:
    """计算预算详情"""
    # 简化预算估算
    flight_budget = 0
    for i in range(len(route) - 1):
        flight_budget += 800  # 每段航班估算 800 元
    
    hotel_budget = sum(plan["days"] * 300 for plan in daily_plan)  # 每晚 300 元
    food_budget = sum(plan["days"] * 150 for plan in daily_plan)   # 每天 150 元
    activity_budget = sum(plan["days"] * 100 for plan in daily_plan)  # 每天 100 元
    
    total = flight_budget + hotel_budget + food_budget + activity_budget
    
    return {
        "flights": flight_budget,
        "hotels": hotel_budget,
        "food": food_budget,
        "activities": activity_budget,
        "total": total,
        "per_day": total / sum(plan["days"] for plan in daily_plan)
    }


def _generate_route_recommendation(route: List[str], days: int, budget: Optional[float]) -> str:
    """生成路线推荐建议"""
    recommendations = []
    
    # 根据城市数量
    if len(route) > 4:
        recommendations.append("⚠ 城市较多，建议延长总天数或减少城市")
    elif len(route) <= 3:
        recommendations.append("✓ 城市数量适中，可以深度游玩")
    
    # 根据预算
    if budget:
        estimated = (len(route) - 1) * 800 + days * 550
        if estimated > budget:
            recommendations.append(f"⚠ 预估花费¥{estimated}超出预算¥{budget}，建议调整")
        else:
            recommendations.append(f"✓ 预估花费¥{estimated}在预算内")
    
    # 根据天数
    if days / len(route) < 2:
        recommendations.append("⚠ 每个城市停留时间较短，建议增加天数")
    elif days / len(route) > 4:
        recommendations.append("✓ 每个城市有充足时间深度游")
    
    # 特色建议
    if "曼谷" in route and "清迈" in route:
        recommendations.append("💡 泰国线：曼谷购物 + 清迈休闲，建议至少 7 天")
    if "吉隆坡" in route and "新加坡" in route:
        recommendations.append("💡 马新线：可考虑陆路跨境，节省机票")
    
    return " | ".join(recommendations) if recommendations else "路线合理，祝旅途愉快！"


def compare_routes(route1: List[str], route2: List[str], days: int) -> Dict:
    """
    对比两条路线
    
    Args:
        route1: 路线 1
        route2: 路线 2
        days: 总天数
    
    Returns:
        {"route1": {...}, "route2": {...}, "recommendation": "..."}
    """
    plan1 = plan_optimal_route(route1, days)
    plan2 = plan_optimal_route(route2, days)
    
    diff = plan1.get('estimated_price', 0) - plan2.get('estimated_price', 0)
    
    if diff > 0:
        recommendation = f"路线 2 更省钱（便宜¥{diff}）"
    elif diff < 0:
        recommendation = f"路线 1 更省钱（便宜¥{abs(diff)}）"
    else:
        recommendation = "两条路线价格相当"
    
    return {
        "route1": plan1,
        "route2": plan2,
        "price_difference": abs(diff),
        "recommendation": recommendation
    }


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "plan" and len(sys.argv) >= 4:
        # 解析城市列表：上海，曼谷，清迈，吉隆坡
        cities = [c.strip() for c in sys.argv[2].split(',')]
        days = int(sys.argv[3])
        budget = float(sys.argv[4]) if len(sys.argv) > 4 else None
        preference = sys.argv[5] if len(sys.argv) > 5 else "price"
        
        result = plan_optimal_route(cities, days, budget, preference)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "compare" and len(sys.argv) >= 5:
        route1 = [c.strip() for c in sys.argv[2].split(',')]
        route2 = [c.strip() for c in sys.argv[3].split(',')]
        days = int(sys.argv[4])
        
        result = compare_routes(route1, route2, days)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        print("用法:")
        print("  python route_planner.py plan '<city1,city2,city3,...>' <days> [budget] [preference]")
        print("  python route_planner.py compare '<route1>' '<route2>' <days>")
        print("\n示例:")
        print("  python route_planner.py plan '上海，曼谷，清迈，吉隆坡' 8")
        print("  python route_planner.py plan '上海，曼谷，清迈，吉隆坡' 8 3000 price")
        sys.exit(1)


if __name__ == "__main__":
    main()
