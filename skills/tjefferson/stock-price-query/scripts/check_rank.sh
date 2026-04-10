#!/bin/bash
# 快速查看 stock-price-query 在 ClawHub 的统计数据
# 用法: bash check_rank.sh

echo "📊 stock-price-query Stats"
echo "=========================="
clawhub inspect stock-price-query --json 2>/dev/null | python3 -c "
import sys, json
raw = ''
capture = False
for line in sys.stdin:
    if line.strip().startswith('{'):
        capture = True
    if capture:
        raw += line
try:
    data = json.loads(raw)
    stats = data.get('skill', {}).get('stats', {})
    print(f'Downloads:       {stats.get(\"downloads\", \"?\")}')
    print(f'Stars:           {stats.get(\"stars\", \"?\")}')
    print(f'Installs (now):  {stats.get(\"installsCurrent\", \"?\")}')
    print(f'Installs (all):  {stats.get(\"installsAllTime\", \"?\")}')
    print(f'Versions:        {stats.get(\"versions\", \"?\")}')
    print()
    print('Ranking page: https://clawhub.ai/skills?sort=downloads&nonSuspicious=true')
except Exception as e:
    print(f'Error: {e}')
"
