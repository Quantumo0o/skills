"""Family Trip Planner - 家庭旅行规划师"""
import json
import re
from typing import Optional, List, Dict

DESTINATIONS = {
    "北京": {"type": "文化", "score": 9.2, "budget_per_day": 800, "attractions": ["故宫", "天安门", "颐和园", "北京动物园"]},
    "上海": {"type": "城市", "score": 8.8, "budget_per_day": 900, "attractions": ["外滩", "豫园", "迪士尼"]},
    "成都": {"type": "美食/自然", "score": 9.0, "budget_per_day": 600, "attractions": ["大熊猫基地", "宽窄巷子", "青城山"]},
    "杭州": {"type": "自然", "score": 8.7, "budget_per_day": 700, "attractions": ["西湖", "灵隐寺", "千岛湖"]},
    "西安": {"type": "历史", "score": 8.9, "budget_per_day": 650, "attractions": ["兵马俑", "大雁塔", "城墙"]},
    "广州": {"type": "美食/城市", "score": 8.5, "budget_per_day": 700, "attractions": ["广州塔", "长隆", "沙面"]},
    "深圳": {"type": "城市", "score": 8.3, "budget_per_day": 800, "attractions": ["世界之窗", "东部华侨城", "深圳湾"]},
    "青岛": {"type": "海滨", "score": 8.6, "budget_per_day": 650, "attractions": ["栈桥", "崂山", "金沙滩"]},
    "厦门": {"type": "海滨/文艺", "score": 8.7, "budget_per_day": 700, "attractions": ["鼓浪屿", "厦门大学", "曾厝垵"]},
    "苏州": {"type": "园林", "score": 8.8, "budget_per_day": 600, "attractions": ["拙政园", "平江路", "虎丘"]},
}

def parse_request(text: str) -> dict:
    result = {"destination": None, "days": None, "budget": None, "child_age": None, "family_size": None}
    m = re.search(r'(\d+)(?:天|天左右|天以内)', text)
    if m: result["days"] = int(m.group(1))
    m = re.search(r'(\d+)(?:岁|周岁)', text)
    if m: result["child_age"] = int(m.group(1))
    m = re.search(r'(\d+)(?:元|元左右|元以内)', text)
    if m: result["budget"] = int(m.group(1))
    for city in DESTINATIONS:
        if city in text: result["destination"] = city
    return result

def recommend_destinations(parsed: dict) -> List[dict]:
    budget = parsed.get("budget", 8000)
    days = parsed.get("days", 4)
    child_age = parsed.get("child_age", 8)
    results = []
    for name, info in DESTINATIONS.items():
        est = round(info["budget_per_day"] * days * (1 + 0.3 * (child_age > 10)))
        if est <= budget * 1.2:
            results.append({"name": name, "type": info["type"], "score": info["score"], "budget_estimate": {"low": round(est*0.85), "high": round(est*1.15)}, "key_attractions": info["attractions"][:3]})
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5]

def generate_itinerary(destination: str, days: int) -> List[dict]:
    schedules = {
        "北京": ["故宫深度游（3小时，含儿童讲解）", "天安门广场 + 前门大街", "什刹海胡同游"],
        "成都": ["大熊猫基地（上午，早起）", "宽窄巷子 + 人民公园", "夜游锦里"],
        "杭州": ["西湖苏堤晨跑/骑行", "灵隐寺 + 龙井村品茶", "宋城千古情演出"],
        "上海": ["外滩万国建筑", "豫园城隍庙", "迪士尼全天"],
        "西安": ["兵马俑（提前预约）", "大雁塔 + 大唐不夜城", "城墙骑行"],
    }
    default = ["当地主要景点游览", "特色美食品尝", "休闲活动"]
    schedule = schedules.get(destination, default)
    return [{"day": d+1, "activity": schedule[d % len(schedule)], "tips": ["注意休息节奏", "带好儿童必备物品"]} for d in range(days)]

def handle(text: str) -> dict:
    parsed = parse_request(text)
    recommendations = recommend_destinations(parsed)
    days = parsed.get("days", 4)
    destination = parsed.get("destination", recommendations[0]["name"] if recommendations else "成都")
    itinerary = generate_itinerary(destination, days)
    budget_range = recommendations[0]["budget_estimate"] if recommendations else {"low": 5000, "high": 8000}
    return {
        "destinationRecommendations": recommendations,
        "dailyItinerary": itinerary,
        "budgetEstimate": {"low": budget_range["low"], "high": budget_range["high"], "currency": "CNY"},
        "packingList": {"衣物": ["T恤", "长裤", "外套"], "洗漱": ["儿童牙刷", "防晒霜"], "药品": ["儿童退烧药", "创可贴"], "证件": ["身份证", "儿童户口本"]},
        "safetyTips": ["提前查看天气预报", "儿童必备药品要带够", "热门景点提前预约"]
    }

if __name__ == "__main__":
    test_cases = [
        "五一假期带6岁孩子去北京玩4天，预算8000元左右",
        "暑假带孩子去海边，孩子4岁和8岁，5天预算15000元",
    ]
    print("=== Family Trip Planner 自测 ===\n")
    for tc in test_cases:
        r = handle(tc)
        dests = [d["name"] for d in r["destinationRecommendations"]]
        print(f"Input: {tc}\n  -> 推荐: {dests}\n  -> 行程天数: {len(r['dailyItinerary'])}天\n  -> 预算: {r['budgetEstimate']}\n")
