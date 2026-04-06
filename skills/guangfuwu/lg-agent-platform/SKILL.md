---
name: lg-agent-platform
description: Monitor A/H stocks with natural language, run strategies in the cloud, and send instant alerts to Feishu/WeChat. LG Data supports stock monitoring, price alerts, webhook notifications, portfolio PnL lookup, real-time quotes, minute bars, and serverless strategy execution. Keywords: stock monitor, quant, trading alert, market data, Feishu, webhook, portfolio pnl, price alert, A-share, H-share, minute bars.
---

# LG Data Stock Monitor

Turn stock monitoring into a 24/7 cloud task with real-time alerts to Feishu/WeChat.

**Best for:** stock alerts, price monitoring, webhook notifications, portfolio PnL lookup, and lightweight quant workflows without maintaining your own cron jobs or market data stack.

![演示](./lg-data-demo.gif)

## 能做什么

| 功能 | 说明 |
|------|------|
| **自动盯盘** | 设置预警条件（突破均线、涨跌幅、换手率等），触发即通知 |
| **实时行情** | A股、港股实时行情 + 分钟线数据，无需购买第三方API |
| **飞书/微信推送** | 策略触发毫秒级推送到飞书机器人或微信 webhook |
| **Serverless 运行** | 云端托管策略，无需自建服务器，无 Token 税 |
| **资产盈亏查询** | 查询持仓盈亏、当日盈亏、持仓明细 |

## Quick Start

### 1) Get your token

- Sign up at `https://lg-data.cc`
- Open your account settings / token page
- Copy your `LG_AGENT_TOKEN`

### 2) Set environment

```bash
export LG_AGENT_BASE_URL=https://lg-data.cc
export LG_AGENT_TOKEN=your_token_here
```

### 3) Try it in 30 seconds

### 查询实时资产盈亏

```bash
scripts/lg_agent_exec.sh '{
  "skillId": "dataasset.data.get",
  "pathParams": {"id": "21"},
  "confirm": false
}'
```

返回：持仓明细、浮动盈亏、收益率数据。

### 列出可用数据资产

```bash
scripts/lg_agent_list.sh
```

返回：可订阅的数据源列表（股票行情、分钟线、持仓数据等）。

## 使用场景

### 场景1：监控茅台突破MA20

```
用户：帮我监控茅台，突破MA20均线就通知我

数据虾：已创建监控任务
- 标的：贵州茅酒 (SH600519)
- 条件：价格突破 MA20
- 数据源：A股实时行情
- 通知：飞书/微信
- 状态：运行中✓

【触发时】
飞书通知：
📈 突破预警触发
- 标的：贵州茅酒 (SH600519)
- 触发：突破MA20
- 最新价：¥1,680.00
- 响应延迟：42ms
```

### 场景2：查询当日盈亏

```
用户：帮我查下今天的盈亏

数据虾：
当日盈亏：+319 元
累计浮动：-19,135 元
---
持仓明细：
- 中国核电：+2.06%
- 永和股份：-32.45%
- 中国联通：-16.25%
...
```

## 技能列表

| skillId | 功能 |
|---------|------|
| `dataasset.list` | 列出数据资产 |
| `dataasset.get` | 获取资产详情 |
| `dataasset.data.get` | 查询资产数据（盈亏、行情等）|
| `dashboard.list` | 列出看板 |
| `dashboard.get` | 获取看板详情 |

## 环境要求

### 必需

- `LG_AGENT_BASE_URL` - 平台地址（默认 `https://lg-data.cc`）
- `LG_AGENT_TOKEN` - Bearer Token（推荐）

### 可选

- `LG_AGENT_COOKIE_HEADER` - 会话Cookie（兼容模式）
- `LG_AGENT_CSRF_TOKEN` - CSRF Token（兼容模式）

## 注意事项

- 高危操作会返回 `approval-required`，需要确认后才执行
- `idempotencyKey` 用于幂等控制，写操作请保持稳定
- Token 从平台获取，不要硬编码在脚本中

---

**传送门：** [https://lg-data.cc](https://lg-data.cc)