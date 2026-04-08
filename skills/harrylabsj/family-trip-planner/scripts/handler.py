#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from models import Destination, DailyItinerary, BudgetBreakdown, KidFriendlyAttraction, PackingList
DESTINATIONS={"北京":{"score":9.2,"days":4,"budget":[7500,9500],"attractions":["故宫","颐和园","北京动物园","天安门"]},"上海":{"score":8.8,"days":4,"budget":[8000,11000],"attractions":["迪士尼","科技馆","外滩","海洋馆"]},"三亚":{"score":8.9,"days":5,"budget":[12000,18000],"attractions":["亚龙湾","海昌梦幻海洋不夜城","蜈支洲岛"]},"成都":{"score":9.0,"days":4,"budget":[6500,9000],"attractions":["熊猫基地","宽窄巷子","都江堰"]}}
def parse_query(query):
    city=None
    for c in DESTINATIONS:
        if c in query: city=c; break
    m=re.search(r'(\d+)天', query); days=int(m.group(1)) if m else 4
    m=re.search(r'(\d{4,6})', query); budget=int(m.group(1)) if m else 8000
    ages=[int(x) for x in re.findall(r'(\d+)岁', query)]
    return city,days,budget,ages
def recommend(city,days):
    if city and city in DESTINATIONS:
        d=DESTINATIONS[city]; return [Destination(city,d['score'],d['attractions'],days or d['days'],{"low":d['budget'][0],"high":d['budget'][1]})]
    return [Destination(n,d['score'],d['attractions'],d['days'],{"low":d['budget'][0],"high":d['budget'][1]}) for n,d in DESTINATIONS.items()][:3]
def itinerary(city,days):
    acts=DESTINATIONS.get(city, DESTINATIONS['北京'])['attractions']
    return [DailyItinerary(i, f'{acts[(i-1)%len(acts)]} 游玩', '午休+轻松活动', '家庭散步或休闲', ['中午留足休息时间','带水和备用衣物']) for i in range(1,days+1)]
def budget_breakdown(total):
    return BudgetBreakdown(int(total*0.25),int(total*0.35),int(total*0.2),int(total*0.1),int(total*0.06),int(total*0.04))
def attractions(city):
    acts=DESTINATIONS.get(city, DESTINATIONS['北京'])['attractions']
    return [KidFriendlyAttraction(a,'3-12岁','2-3小时',['适合亲子','建议错峰'],['综合']) for a in acts]
def packing(days,ages):
    return PackingList([f'T恤 {days}件','长裤 2条','外套 1件'],['牙刷','牙膏','防晒霜','驱蚊液'],['退烧药','创可贴','肠胃药'],['身份证','儿童证件'],['手机充电器','充电宝'],['湿巾','水杯'])
def handle(query):
    city,days,budget,ages=parse_query(query); recs=recommend(city,days); chosen=city or recs[0].name
    return {'destinationRecommendations':[r.__dict__ for r in recs],'dailyItinerary':[x.__dict__ for x in itinerary(chosen,days)],'budgetBreakdown':budget_breakdown(budget).__dict__,'kidFriendlyAttractions':[x.__dict__ for x in attractions(chosen)],'packingList':packing(days,ages).__dict__}
if __name__=='__main__':
    q=' '.join(sys.argv[1:]) or '我们五一带6岁孩子去北京玩4天，预算8000'
    print(json.dumps(handle(q), ensure_ascii=False, indent=2))
