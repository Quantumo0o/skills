---
name: browser-collector
description: "浏览器自动化+数据采集框架。支持Playwright控制、DdddOcr验证码识别、东方财富/雪球/AKShare金融数据采集。反爬对抗、UA池、代理。"
---

# browser-collector Skill

**版本**: 1.0.0
**定位**: 浏览器自动化 + 数据采集框架
**依赖**: Playwright, DdddOcr, OpenCV

## 快速开始

```python
from collectors import EastMoneyCollector

em = EastMoneyCollector()
result = em.get_limit_up(limit=10)
```

## 采集器

| 采集器 | 方法 | 说明 |
|--------|------|------|
| eastmoney | get_limit_up/get_limit_down | 涨跌停 |
| eastmoney | get_stock_quote | 个股行情 |
| eastmoney | get_top_money_flow | 行业资金流 |
| akshare | collect_stock_quote | AKShare股票 |
| akshare | collect_index | 指数行情 |

## 浏览器模式

```python
from collectors import EastMoneyCollector
em = EastMoneyCollector()
result = em.get_limit_up_browser(direction="up", limit=10)
```

## CLI

```bash
python collectors/cli.py list
python collectors/cli.py collect eastmoney limit-up --limit 10
```
