---
name: life-query
description: Query everyday life info — parcel tracking via Kuaidi100 for Chinese carriers (顺丰/圆通/中通/韵达/京东), real-time and historical currency exchange rates and conversion from ECB (30 currencies including CNY/USD/EUR/JPY/GBP/HKD/KRW), gasoline/diesel fuel prices for all 31 provinces in China from NDRC, and global city weather forecasts via wttr.in (current conditions, multi-day forecasts, hourly details). Use when user asks "查快递", "快递单号", "track package", "shipping", "delivery", "物流查询", "包裹到哪了", "顺丰到哪了", "汇率", "外汇", "换算", "exchange rate", "currency converter", "多少钱换", "美元人民币", "日元汇率", "货币转换", "油价", "加油", "gas price", "fuel price", "今天92多少钱", "加油多少钱", "加油站", "天气", "气温", "weather", "forecast", "明天天气", "今天多少度", "会下雨吗", "穿什么衣服", "天气预报", "温度", "湿度", "紫外线", "日出日落".
clawhub-slug: life-query
clawhub-owner: eamanc-lab
homepage: https://github.com/eamanc-lab/life-query
---

# Life Query — 日常生活查询助手

快递物流跟踪、实时汇率换算、全国油价查询、全球天气预报。四合一日常信息查询工具。

## 使用场景

- 用户给了一个快递单号，想查物流到哪了
- 用户问"100美元换多少人民币"、"今天日元汇率"
- 用户问"今天油价多少"、"北京92号多少钱"
- 用户问"北京天气怎么样"、"明天会下雨吗"、"东京这周气温"
- 用户出差/旅行前想了解目的地天气、油价或货币汇率
- 用户想对比一段时间内的汇率走势

**不适用场景**：不要用于股票行情、航班查询、地图导航、新闻资讯等非本 skill 覆盖的查询。如果用户问的是天气之外的气象分析（如气候趋势、空气质量 AQI），本 skill 不支持。

## 前置条件

- **必需**：`curl`、`python3`（系统自带即可）
- **可选**：自有快递100凭证（不配也能用，有默认免费额度；配置后直连快递100，不经过任何第三方）

## 决策流程

```
用户输入
  │
  ├─ 包含单号/快递/物流关键词 → courier-track
  │     └─ 没给单号？→ 追问用户要单号
  │
  ├─ 包含货币/汇率/换算关键词 → exchange-rate
  │     ├─ 明确了币种和金额 → 直接查询
  │     ├─ 只说了"汇率" → 默认 USD→CNY
  │     └─ 问"走势/趋势" → 用 startDate/endDate 查时间序列
  │
  ├─ 包含油价/加油/汽油关键词 → oil-price
  │     ├─ 提到了省份/城市 → --city 参数
  │     └─ 没提 → 默认全国
  │
  ├─ 包含天气/气温/预报/下雨关键词 → weather
  │     ├─ 明确了城市 → --city 参数
  │     ├─ 没提城市 → 追问用户所在城市
  │     ├─ 问"明天/这周" → --days 3
  │     └─ 问"逐小时" → --detail
  │
  └─ 不确定 → 追问用户想查什么
```

## 可用接口

所有接口通过 `bash scripts/run.sh call <接口名> [参数...]` 统一调用。

| 接口 | 实现方式 | 说明 | 数据源 |
|------|---------|------|--------|
| courier-track | Shell 脚本 | 快递物流轨迹查询 | 快递100（直连或免费代理） |
| exchange-rate | Shell 脚本 | 实时/历史汇率，货币换算 | 欧洲央行 ECB（frankfurter.app） |
| oil-price | Shell 脚本 | 全国各省油价（92/95/柴油） | 东方财富/国家发改委 |
| weather | Shell 脚本 | 全球城市天气（当前+多日预报） | wttr.in / WorldWeatherOnline |

> **目录约定**：`apis/` 存放所有可调用接口（Shell 脚本），`scripts/run.sh` 是统一调度引擎。新增接口只需在 `apis/` 下添加 `.sh` 文件。

## 使用方式

### 快递查询

```bash
# 查快递（自动识别快递公司）
bash scripts/run.sh call courier-track --trackingNumber SF1234567890

# 指定快递公司
bash scripts/run.sh call courier-track --trackingNumber SF1234567890 --carrierCode shunfeng
```

输出示例（JSON）：
```json
{
  "trackingNumber": "SF1234567890",
  "carrierName": "顺丰速运",
  "status": "已签收",
  "events": [
    {"time": "2026-03-18 14:30", "desc": "已签收，签收人：本人"},
    {"time": "2026-03-18 08:00", "desc": "派件中，快递员张三 138****1234"},
    {"time": "2026-03-17 22:00", "desc": "已到达 北京转运中心"}
  ]
}
```

### 汇率查询

```bash
# 100 人民币换算成美元、欧元、日元
bash scripts/run.sh call exchange-rate --from CNY --to USD,EUR,JPY --amount 100

# 查询某天的历史汇率
bash scripts/run.sh call exchange-rate --from USD --to CNY --date 2025-01-01

# 查询一段时间内的汇率走势
bash scripts/run.sh call exchange-rate --from USD --to CNY --startDate 2026-03-01 --endDate 2026-03-10

# 表格格式输出
bash scripts/run.sh call exchange-rate --from CNY --to USD,EUR,JPY --format table
```

常用货币代码：CNY（人民币）、USD（美元）、EUR（欧元）、JPY（日元）、GBP（英镑）、HKD（港币）、KRW（韩元）。完整列表约 30 种，详见 ECB 支持范围。

### 油价查询

```bash
# 查询全国所有省份最新油价
bash scripts/run.sh call oil-price

# 查询指定省份
bash scripts/run.sh call oil-price --city 北京

# 查询指定省份的历史油价（取最近5条）
bash scripts/run.sh call oil-price --city 北京 --pageSize 5

# 表格格式输出
bash scripts/run.sh call oil-price --format table
```

输出示例（table 格式）：
```
调价日期: 2026-03-04

省份     92号     95号     柴油    92涨跌   95涨跌
──────────────────────────────────────────────────
北京     7.78    8.28    7.45   +0.10   +0.11
上海     7.74    8.24    7.40   +0.10   +0.11
```

### 天气查询

```bash
# 查询当前天气
bash scripts/run.sh call weather --city 北京

# 查询 3 天预报（表格格式）
bash scripts/run.sh call weather --city Shanghai --days 3 --format table

# 查询含逐小时详情的预报
bash scripts/run.sh call weather --city Tokyo --days 1 --detail

# 支持多种位置格式
bash scripts/run.sh call weather --city "New York"
bash scripts/run.sh call weather --city 广州
```

输出示例（table 格式）：
```
上海 天气
当前: Partly cloudy, 15°C (体感 15°C)
湿度: 41%  风: ENE 15km/h  UV: 3  降水: 0.0mm

日期              最高    最低 天气                   降雨概率
────────────────────────────────────────────────────────
2026-03-20     14°C    7°C Partly Cloudy          0%
2026-03-21     15°C    7°C Sunny                  0%
2026-03-22     13°C   10°C Patchy rain nearby      65%

日出: 05:58 AM  日落: 06:05 PM
```

JSON 格式返回字段：`city`、`current`（temp_C/feels_like_C/desc/humidity/wind_kmph/wind_dir/precip_mm/uv_index/sunrise/sunset）、`forecast`（date/max_C/min_C/desc/chance_of_rain，`--detail` 时含 hourly 数组）。

## 自然语言映射

| 用户说 | 接口 | 关键参数 |
|--------|------|---------|
| "帮我查一下 SF1234567890" | courier-track | trackingNumber=SF1234567890 |
| "这个单号的物流在哪里" | courier-track | trackingNumber=... |
| "100美元换多少人民币" | exchange-rate | from=USD, to=CNY, amount=100 |
| "今天美元汇率多少" | exchange-rate | from=USD, to=CNY |
| "最近一周日元走势" | exchange-rate | from=JPY, to=CNY, startDate/endDate |
| "今天油价多少" | oil-price | 默认全国 |
| "北京92号汽油多少钱" | oil-price | city=北京 |
| "广东最近几次油价调整" | oil-price | city=广东, pageSize=5 |
| "北京天气怎么样" | weather | city=北京 |
| "明天上海会下雨吗" | weather | city=上海, days=3 |
| "东京这周气温多少" | weather | city=Tokyo, days=3, format=table |
| "今天适合出门吗" | weather | city=（追问）|

## 错误处理

| 故障点 | 分类 | 现象 | 处理方式 |
|--------|------|------|---------|
| 快递中转服务不可用 | B-API | curl 返回非 0 | 提示用户"快递服务暂时不可用，请稍后重试"；如果配置了自有 Key，提示检查凭证 |
| 单号不存在或格式错误 | C-运行时 | 返回空 data 或错误码 | 提示用户核实单号，建议检查位数和字母 |
| 快递公司识别失败 | C-运行时 | carrierName 为空 | 追问用户快递公司名称，用 --carrierCode 指定 |
| frankfurter.app 不可用 | B-API | curl 超时/失败 | 告知用户"汇率服务暂时不可用"，建议稍后重试 |
| 不支持的货币代码 | C-运行时 | 返回 404 或空 rates | 提示用户检查货币代码，给出常用代码列表 |
| 东方财富 API 反爬/限流 | B-API | 返回 success=False | 告知用户"油价数据暂时获取失败"，可稍后重试 |
| wttr.in 不可用或限速 | B-API | curl 超时/返回空 | 告知用户"天气服务暂时不可用"，建议稍后重试 |
| 城市名无法识别 | C-运行时 | 返回错误 JSON 或意外城市 | 提示用户换英文城市名或检查拼写 |
| python3/pyyaml 未安装 | A-环境 | 命令不存在 | 提示用户安装：`pip install pyyaml` |

**铁律**：单个接口失败不影响其他接口。用户同时问了汇率和油价，一个挂了另一个照常查。

## 外部服务声明

本 skill 调用以下外部服务，所有网络请求均可在 `apis/*.sh` 中审查：

| 接口 | 端点 | 发送的数据 | 凭证处理 |
|------|------|-----------|---------|
| courier-track（免费模式） | `api.fenxianglife.com` | 仅快递单号 | **不发送任何凭证** |
| courier-track（自有凭证） | `poll.kuaidi100.com` | 快递单号 + 签名 | **直连快递100，不经过任何第三方** |
| exchange-rate | `api.frankfurter.app` | 货币代码、金额 | 无需凭证 |
| oil-price | `datacenter-web.eastmoney.com` | 省份名 | 无需凭证 |
| weather | `wttr.in` | 城市名 | 无需凭证 |

**凭证隔离保证**：当配置了 `KUAIDI100_KEY`/`KUAIDI100_CUSTOMER` 时，快递查询直连 `poll.kuaidi100.com`，你的 API Key **绝不会**发送到 fenxianglife.com 或其他第三方。

```bash
# 配置自有凭证后自动切换到直连通道
export KUAIDI100_KEY=你的授权Key
export KUAIDI100_CUSTOMER=你的Customer编码
```

## 更新本 Skill

ClawHub 唯一标识：**slug `life-query`**（owner: `eamanc-lab`）

```bash
npx clawhub@latest update life-query
```
