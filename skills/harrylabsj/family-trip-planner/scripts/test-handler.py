#!/usr/bin/env python3
import json, subprocess
out=subprocess.check_output(['python3','scripts/handler.py','我们五一带6岁孩子去北京玩4天，预算8000'], text=True)
data=json.loads(out)
assert 'destinationRecommendations' in data
assert 'dailyItinerary' in data
print('PASS family-trip-planner')
