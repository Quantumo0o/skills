# ctrip-skill · 携程机票/火车票搜索

携程旅行搜索 Skill，通过 Playwright 自动化实现机票、火车票查询和行程规划功能。

---

## 📦 安装

```bash
# 通过 clawhub 安装
clawhub install ctrip-skill

# 或手动安装
cd /root/.openclaw/workspace-taizi/skills/ctrip-skill
pip install -r requirements.txt
playwright install chromium
```

---

## 🚀 快速开始

### 1. 搜索机票（单程）

```bash
python scripts/ctrip_client.py flight 上海 曼谷 2026-10-01
```

### 2. 搜索往返机票

```bash
python scripts/flight_search.py roundtrip 上海 曼谷 2026-10-01 2026-10-08
```

### 3. 多程机票搜索

```bash
python scripts/flight_search.py multi '上海，曼谷，2026-10-01;曼谷，清迈，2026-10-04;清迈，吉隆坡，2026-10-07'
```

### 4. 火车票搜索

```bash
python scripts/train_search.py search 北京 上海 2026-10-01
```

### 5. 行程规划

```bash
python scripts/route_planner.py plan '上海，曼谷，清迈，吉隆坡' 8
```

### 6. 多日期价格对比

```bash
python scripts/flight_search.py compare 上海 曼谷
```

---

## 📋 功能模块

### ctrip_client.py - 核心客户端

Playwright 自动化客户端，负责与携程网站交互。

```python
from ctrip_client import CtripClient

client = CtripClient(headless=True)
client.launch()

# 搜索机票
result = client.search_flight("上海", "曼谷", "2026-10-01")

# 搜索火车票
result = client.search_train("北京", "上海", "2026-10-01")

client.close()
```

### flight_search.py - 机票搜索

支持单程、往返、多程搜索和价格对比。

**命令：**
- `oneway <from> <to> <date>` - 单程
- `roundtrip <from> <to> <depart> <return>` - 往返
- `multi '<from1,to1,date1;from2,to2,date2;...>'` - 多程
- `compare <from> <to>` - 多日期对比

### train_search.py - 火车票搜索

支持直达、换乘方案查询。

**命令：**
- `search <from> <to> <date>` - 直达搜索
- `transfer <from> <to> <date> [via]` - 含换乘
- `compare <from> <to> <date>` - 车型对比

### route_planner.py - 行程规划

智能路线规划，支持最省钱/最省时偏好。

**命令：**
- `plan '<city1,city2,...>' <days> [budget] [preference]` - 规划路线
- `compare '<route1>' '<route2>' <days>` - 路线对比

---

## 📊 输出示例

### 机票搜索结果

```json
{
  "route": "上海→曼谷",
  "date": "2026-10-01",
  "prices": ["¥1,280", "¥1,350", "¥1,420"],
  "flights": [...],
  "min_price": 1280
}
```

### 行程规划结果

```json
{
  "optimal_route": ["上海", "曼谷", "清迈", "吉隆坡"],
  "total_days": 8,
  "estimated_price": 2600,
  "daily_plan": [
    {
      "day_range": "第 1-2 天",
      "city": "上海",
      "days": 2,
      "highlights": ["外滩", "东方明珠", "豫园"]
    },
    ...
  ],
  "recommendation": "泰国线：曼谷购物 + 清迈休闲，建议至少 7 天"
}
```

---

## ⚙️ 配置

### requirements.txt

```
playwright>=1.40.0
requests>=2.31.0
```

### 环境变量（可选）

```bash
# 设置浏览器头模式
export CTRIP_HEADLESS=false

# 设置超时时间（秒）
export CTRIP_TIMEOUT=90
```

---

## ⚠️ 注意事项

1. **Playwright 依赖**: 首次使用需运行 `playwright install chromium`
2. **反爬策略**: 携程有反爬机制，建议控制请求频率（间隔 >5 秒）
3. **价格时效**: 机票价格实时变化，搜索结果仅供参考
4. **行李费用**: 廉航（春秋、亚航等）行李额需另购
5. **网络要求**: 需要稳定的网络连接访问携程网站

---

## 🛠 开发调试

### 有头模式调试

```python
client = CtripClient(headless=False)  # 显示浏览器
```

### 日志级别

```bash
# 启用详细日志
export DEBUG=1
python scripts/ctrip_client.py flight 上海 曼谷 2026-10-01
```

---

## 📝 更新日志

- **v1.0.0** (2026-03-24)
  - 初始版本发布
  - 支持机票/火车票搜索
  - 支持行程规划
  - 支持多程路线对比

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- 参考架构：xiaohongshu-mcp
- 数据源：携程旅行 (ctrip.com)

---

**作者**: 三省六部  
**版本**: 1.0.0  
**最后更新**: 2026-03-24
