---
name: fosun-trading
description: Trade stocks (query price, check funds/holdings/cash flows, place/cancel orders) using Fosun OpenAPI SDK via command-line scripts. Supports HK (L2), US (L1), and A-share (Shanghai-HK/Shenzhen-HK Stock Connect, L1) markets. Supports limit and market order types. Use when the user wants to check stock prices, query account balance, check cash flow history, buy/sell stocks, or manage orders.
---

# 复星交易工具集

通过命令行脚本完成港股/美股/A 股（港股通）的行情查询、资金查询、资金流水查询、下单和订单管理。所有脚本位于 `code/` 目录下。

## 前置条件

1. SDK 已安装（参考 `fosun-sdk-setup` skill）
2. 环境变量已配置：
   - `FSOPENAPI_SERVER_PUBLIC_KEY` — 服务端公钥（PEM）
   - `FSOPENAPI_CLIENT_PRIVATE_KEY` — 客户端私钥（PEM）
   - `FSOPENAPI_API_KEY` — API Key（也可通过 `--api-key` 传入）
   - `FSOPENAPI_BASE_URL` — 网关地址（可选，默认 `https://openapi-sit.fosunxcz.com`）

> 如果工作区或 `/tmp` 下存在 `fosun.env`，脚本会自动加载其中的凭证。

---

## 环境约束（必须遵守）

- **优先复用现有虚拟环境**：如果 `{workspace_root}/.venv-fosun` 存在，必须使用它。
- **禁止擅自新建虚拟环境**：未经用户明确要求，**不得**执行 `python -m venv ...`、`uv venv ...`、`conda create ...` 等命令。
- **禁止安装到系统 Python 或其他临时环境**。
- **不要使用裸 `python` / `pip`**；统一使用目标虚拟环境里的绝对路径解释器与 pip。

当前 workspace 的标准环境为：

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python
/Users/admin/.openclaw/workspace/.venv-fosun/bin/pip
```

所有脚本运行示例应使用：

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python <脚本名>.py <子命令> [参数]
```

如果 `.venv-fosun` 不存在：
- 先检查记忆文件（`memory/YYYY-MM-DD.md` 或 `MEMORY.md`）里是否记录了其他既有环境路径；
- 若存在既有环境，则复用该环境；
- 若不存在既有环境，**不要自行创建新环境**，先向用户确认。

## 支持的市场

| 市场代码 | 说明 | 行情级别 | 币种 |
|----------|------|----------|------|
| `hk` | 港股 | L2（含盘口、经纪商队列） | HKD |
| `us` | 美股 | L1（支持盘前/盘中/盘后） | USD |
| `sh` | 上交所（港股通） | L1 | CNH |
| `sz` | 深交所（港股通） | L1 | CNH |

**标的代码格式**：`marketCode + stockCode`

| 示例 | 说明 |
|------|------|
| `hk00700` | 腾讯控股（港股） |
| `usAAPL` | 苹果（美股） |
| `sh600519` | 贵州茅台（A 股-沪） |
| `sz000001` | 平安银行（A 股-深） |

## 支持的订单类型

| 名称 | order_type 值 | CLI 参数 | 是否需要 price | 适用市场 | 说明 |
|------|---------------|----------|----------------|----------|------|
| 竞价限价单 | `1` | `auction_limit` | 是 | 港股 | 竞价时段以指定价格参与竞价 |
| 竞价单 | `2` | `auction` | 否 | 港股 | 竞价时段以市场价参与竞价 |
| 限价单 | `3` | `limit`（默认） | 是 | 港/美/A | 普通限价委托 |
| 增强限价单 | `4` | `enhanced_limit` | 是 | 港股 | 最多配对 10 个价位，未成交部分保留为限价单 |
| 特别限价单 | `5` | `special_limit` | 是 | 港股 | 最多配对 10 个价位，未成交部分自动取消 |
| 市价单 | `9` | `market` | 否 | 港/美 | 以当前市场价成交 |

## 运行方式

所有脚本在 `code/` 目录下运行：

```bash
cd /Users/admin/.openclaw/workspace/skills/fosun_skills/fosun-trading/code
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python <脚本名>.py <子命令> [参数]
```

或者使用完整路径：

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python /Users/admin/.openclaw/workspace/skills/fosun_skills/fosun-trading/code/<脚本名>.py <子命令> [参数]
```

所有脚本支持公共参数：`--api-key`、`--base-url`、`--sub-account-id`。

---

## 1. 查询行情 — query_price.py

> **仅支持主动拉取（API 调用），不支持推送。**
>
> - 港股：L2 行情（含盘口、经纪商队列）
> - 美股：L1 行情（支持盘前/盘中/盘后）
> - A 股（港股通）：L1 行情

### 批量报价（最常用）

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py quote hk00700 usAAPL sh600519
```

### 盘口/买卖档

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py orderbook hk00700 --count 5
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py orderbook sh600519 --count 5
```

### K 线

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py kline hk00700 --ktype day -n 30
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py kline sh600519 --ktype min5 -n 60
```

`ktype` 可选：`day` / `week` / `month` / `year` / `min1` / `min5` / `min15` / `min30` / `min60`

### 分时

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py min hk00700 --count 5
```

### 逐笔成交

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py tick hk00700 -n 20
```

### 经纪商队列（仅港股 L2）

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py broker hk00700
```

---

## 2. 查询买卖信息 — query_bidask.py

> 查询某只股票的**每手股数（lotSize）**、最大可买/可卖数量、购买力等信息。
> 对应 API 接口：`POST /api/v1/trade/BidAskInfo`

### 查询每手股数

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700                           # 港股（默认限价买入）
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --lot-size-only           # 仅输出 lotSize 数值
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock AAPL --market us --lot-size-only
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 600519 --market sh --lot-size-only
```

### 查询可买/可卖数量

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --price 350.000           # 指定价格查更精确的可买数量
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --direction sell           # 查可卖数量
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock AAPL --market us                 # 美股
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 600519 --market sh               # A 股（沪）
```

### 指定订单类型查询

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --order-type market           # 市价单
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --order-type enhanced_limit   # 增强限价单
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --order-type special_limit    # 特别限价单
```

### 全部参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--stock` | 是 | 股票代码（不含市场前缀） |
| `--market` | 否 | `hk`（默认）/ `us` / `sh` / `sz` |
| `--direction` | 否 | `buy`（默认）/ `sell` |
| `--order-type` | 否 | `limit`（默认）/ `enhanced_limit` / `special_limit` / `market` |
| `--price` | 否 | 委托价格（传入可得到更精确的可买数量） |
| `--quantity` | 否 | 委托数量 |
| `--lot-size-only` | 否 | 仅输出每手股数数值 |

### 响应关键字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `maxPurchasePower` | string | 最大购买力（含融资） |
| `cashPurchasePower` | string | 现金购买力 |
| `availableWithdrawBalance` | string | 总账户可用现金 |
| `singleWithdrawBalance` | string | 当前币种可提现金 |
| `currency` | string | 币种（HKD/USD/CNH） |
| `lotSize` | int | **每手股数**（如港股腾讯 = 100，即一手 100 股） |
| `cashQuantityBuy` | int | 现金可买数量 |
| `maxQuantityBuy` | int | 最大可买数量 |
| `baseQuantitySell` | int | 本币种可卖数量 |
| `maxQuantitySell` | int | 持仓可卖数量（含关联币种） |

> **⚠️ 每手股数（lotSize）说明**
>
> 不同股票的每手股数不同，**必须通过此接口动态查询**，不可硬编码。
>
> | 市场 | 每手规则 | 示例 |
> |------|----------|------|
> | 港股 | 每只股票不同，由交易所定义 | 腾讯(00700) = 100 股/手 |
> | 美股 | 通常 1 股起买，无整手限制 | AAPL lotSize = 1 |
> | A 股（港股通） | 通常 100 股/手 | 贵州茅台(600519) = 100 股/手 |
>
> 港股下单时 quantity 必须是 lotSize 的整数倍，否则会被拒单。

---

## 3. 查询资金/持仓 — query_funds.py

### 资金汇总（可用资金/冻结资金/总资产）

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py summary
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py summary --currency HKD
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py summary --currency CNH     # A 股人民币资金
```

关键字段：

| 字段 | 说明 |
|------|------|
| `summary.cashPurchasingPower` | 现金购买力（可用资金） |
| `summary.frozenBalance` | 冻结资金 |
| `summary.ledgerBalance` | 账面余额（总资产） |
| `summary.maxPurchasingPower` | 最大购买力 |
| `breakdown[]` | 分币种明细（HKD/USD/CNH） |

完整字段见 [docs/CashSummary.md](docs/CashSummary.md)。

### 持仓列表（持仓数量/当前市值/成本价）

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py holdings
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py holdings --symbols hk00700 --currencies HKD USD
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py holdings --symbols sh600519 --currencies CNH
```

关键字段：

| 字段 | 说明 |
|------|------|
| `list[].stockCode` | 股票代码 |
| `list[].quantity` | 持仓数量 |
| `list[].quantityAvail` | 可用数量 |
| `list[].price` | 当前市价 |
| `list[].avgCost` | 平均成本 |
| `list[].dilutedCost` | 摊薄成本 |

完整字段见 [docs/Holdings.md](docs/Holdings.md)。

> **⚠️ 成本字段说明：持仓有两种成本，务必区分，没有明确说明哪个成本就必须都告诉用户且区分**
>
> | 字段 | 含义 | 计算方式 |
> |------|------|----------|
> | `avgCost` | **平均成本** | 所有买入交易的加权平均价格，不因卖出而变化 |
> | `dilutedCost` | **摊薄成本** | 在平均成本基础上，将已实现盈亏摊薄到剩余持仓中 |
>
> - 如果只买入未卖出过，两者相同。
> - 一旦部分卖出且产生盈利，`dilutedCost` 会低于 `avgCost`（盈利被摊薄到剩余持仓）；反之亏损卖出时 `dilutedCost` 会高于 `avgCost`。
> - **查看买入均价**用 `avgCost`；**评估真实持仓成本（含已实现盈亏）**用 `dilutedCost`。

### 账户列表

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py accounts
```

---

## 4. 查询资金流水 — query_cashflows.py

> 查询账户的资金进出明细（交易结算、出入金、利息、费用等）。
> 对应 API 接口：`POST /api/v1/trade/CashFlows`

### 查询全部流水

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_cashflows.py
```

### 按日期范围查询

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_cashflows.py --from-date 2025-01-01 --to-date 2025-01-31
```

### 查询指定日期

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_cashflows.py --date 2025-03-15
```

### 按类型筛选

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_cashflows.py --flow-type 1
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_cashflows.py --business-type 1 2
```

### 全部参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--from-date` | 否 | 开始日期 yyyy-mm-dd |
| `--to-date` | 否 | 结束日期 yyyy-mm-dd |
| `--date` | 否 | 指定日期 yyyy-mm-dd（查询单日流水） |
| `--flow-type` | 否 | 流水类型 |
| `--business-type` | 否 | 业务类型（可多个） |

---

## 5. 下单 — place_order.py

> 支持限价单、增强限价单、特别限价单、竞价单、竞价限价单和市价单，覆盖港/美/A 股市场。

> **⚠️ 重要：下单前必须与用户二次确认！**
> 当已解析出明确的订单参数（股票代码、方向、数量、价格等）后，**禁止直接执行下单命令**。
> 必须先将完整的订单参数汇总展示给用户（适合用户阅读的格式），等待用户明确确认后才能执行。
> 这是一项涉及真实资金的操作，任何情况下都不得跳过确认步骤。

> **⚠️ 重要：用户说"买/卖 N 手"时，必须先查询每手股数再换算成股数！**
> 当用户的指令中使用"手"作为数量单位（如"帮我买 1 手腾讯"、"卖 3 手 00700"），**必须先调用 `query_bidask.py --lot-size-only` 查询该股票的每手股数（lotSize）**，再将手数换算为股数（quantity = 手数 × lotSize），最终以股数下单。
>
> ```bash
> # 示例：用户说"买 2 手腾讯 (00700)"
> # 第一步：查询每手股数
> /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --lot-size-only
> # 假设输出 100，即一手 = 100 股
> # 第二步：计算 quantity = 2 × 100 = 200
> # 第三步：下单时 --quantity 200
> ```
>
> **禁止假设每手股数**，不同股票的 lotSize 不同，必须动态查询。

> **⚠️ 重要：最大可买/可卖数量必须通过接口查询，禁止自行计算！**
> 下单前需要确认可买/可卖数量时，**必须调用 `query_bidask.py` 接口查询**，不得根据资金余额、股价、持仓数量等信息自行推算。
> 接口返回的 `maxQuantityBuy`（最大可买）和 `maxQuantitySell`（最大可卖）已综合考虑购买力、保证金、风控规则等因素，手动计算无法覆盖这些逻辑，极易导致下单失败或数量错误。
>
> ```bash
> # 查询最大可买数量（指定价格更精确）
> /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --price 350.000
> # 查询最大可卖数量
> /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --direction sell
> ```

### 港股限价买入（默认 order_type=limit）

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 00700 --direction buy --quantity 100 --price 350.000
```

### 港股增强限价买入

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 00700 --direction buy --quantity 100 --price 350.000 --order-type enhanced_limit
```

### 港股特别限价买入

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 00700 --direction buy --quantity 100 --price 350.000 --order-type special_limit
```

### 港股市价买入

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 00700 --direction buy --quantity 100 --order-type market
```

### 港股竞价限价买入

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 00700 --direction buy --quantity 100 --price 350.000 --order-type auction_limit
```

### 港股竞价买入

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 00700 --direction buy --quantity 100 --order-type auction
```

### 美股市价买入（盘中）

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock AAPL --market us --direction buy --quantity 5 --order-type market
```

### 美股限价卖出

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock AAPL --market us --direction sell --quantity 5 --price 180.00 --currency USD
```

### A 股（港股通）限价买入

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 600519 --market sh --direction buy --quantity 100 --price 1800.00
```

### A 股（港股通）市价买入

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 000001 --market sz --direction buy --quantity 100 --order-type market
```

### 下单前校验（不实际下单）

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 00700 --direction buy --quantity 100 --price 350.000 --check-only
```

`--check-only` 返回可买/可卖数量、购买力、每手股数等信息。

### 全部参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--stock` | 是 | 股票代码（不含市场前缀） |
| `--direction` | 是 | `buy` / `sell` |
| `--quantity` | 是 | 委托数量 |
| `--order-type` | 否 | `auction_limit`(1) / `auction`(2) / `limit`(3,默认) / `enhanced_limit`(4) / `special_limit`(5) / `market`(9) |
| `--price` | 条件 | 委托价格。市价单可不传，限价单必填 |
| `--market` | 否 | `hk`（默认）/ `us` / `sh` / `sz` |
| `--currency` | 否 | 自动根据 market 选择（HKD/USD/CNH） |
| `--check-only` | 否 | 仅校验，不下单 |
| `--exp-type` | 否 | `1`=当日有效（默认），`2`=GTC |

### price 小数位规则

- 港股：3 位小数（如 `350.000`）
- 美股：2 位小数（如 `180.00`）
- A 股：2 位小数（如 `1800.00`）

---

## 6. 查询订单 — list_orders.py

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --stock 00700 --status 20 40
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --status-group pending             # 快捷: 未成交
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --status-group filled              # 快捷: 已成交
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --status-group cancelled           # 快捷: 已撤销
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --from-date 2025-01-01 --to-date 2025-01-31
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --direction buy --market hk
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --market sh sz                     # A 股订单
```

| 参数 | 说明 |
|------|------|
| `--stock` | 按股票代码筛选 |
| `--status` | 按状态筛选（可多个） |
| `--status-group` | 快捷状态分组（与 `--status` 互斥） |
| `--from-date` / `--to-date` | 日期范围 |
| `--direction` | `buy` / `sell` |
| `--market` | `hk` / `us` / `sh` / `sz`（可多个） |
| `--count` | 返回数量（默认 20） |

### 状态分组快捷筛选

| --status-group | 包含状态 | 说明 |
|----------------|----------|------|
| `pending` | 10, 20, 21, 40, 60 | 未成交（未报/待报/条件单待触发/已报/部成） |
| `filled` | 50 | 已成交（全部成交） |
| `cancelled` | 70, 80, 90, 100 | 已撤销（已撤/部撤/废单/已失效） |

### 订单状态枚举

| 值 | 说明 |
|----|------|
| `10` | 未报 |
| `20` | 待报 |
| `21` | 条件单-待触发 |
| `40` | 已报 |
| `50` | 全成 |
| `60` | 部成 |
| `70` | 已撤 |
| `80` | 部撤 |
| `90` | 废单 |
| `100` | 已失效 |

### 订单响应关键字段

| 字段 | 说明 |
|------|------|
| `orderId` | 订单 ID |
| `stockCode` | 股票代码 |
| `orderType` | 订单类型 (3=限价单, 9=市价单) |
| `orderStatus` | 订单状态 |
| `price` | 委托价格 |
| `quantity` | 委托数量 |
| `filledPrice` | 成交价格 |
| `filledQuantity` | 成交数量 |
| `canCancel` | 是否可撤单 (0=否, 1=是) |

---

## 7. 撤单 — cancel_order.py

> **⚠️ 重要：撤单前必须与用户二次确认！**
> 撤单同样是不可逆操作，执行前必须向用户展示待撤订单的详情（订单号、股票、方向、数量等），等待用户明确确认后才能执行。

```bash
/Users/admin/.openclaw/workspace/.venv-fosun/bin/python cancel_order.py <ORDER_ID>
```

支持港/美/A 股所有市场的订单撤销。

---

## 下单工作流（推荐步骤）

```
1. 查询行情      → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py quote hk00700
2. 查看盘口      → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py orderbook hk00700
3. 查询每手股数  → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --lot-size-only
4. 确认资金      → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py summary
5. 下单前校验    → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 00700 --direction buy --quantity 100 --price 350.000 --check-only
6. 提交订单      → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 00700 --direction buy --quantity 100 --price 350.000
7. 确认结果      → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --stock 00700
```

**A 股下单示例：**

```
1. 查询行情      → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py quote sh600519
2. 查询每手股数  → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 600519 --market sh --lot-size-only
3. 确认资金      → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py summary --currency CNH
4. 下单前校验    → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 600519 --market sh --direction buy --quantity 100 --price 1800.00 --check-only
5. 提交订单      → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 600519 --market sh --direction buy --quantity 100 --price 1800.00
6. 确认结果      → /Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --market sh
```

---

## ⛔ AI 交易限制（必须遵守）

> 通用调用频率、IP 白名单等基础限制见 `fosun-sdk-setup` skill。

### 下单频率限制

| 维度 | 限制 | 超限处理 |
|------|------|---------|
| 每小时下单次数（买卖一起） | 单个客户 ≤ 10 笔/小时 | 该小时内拒绝新委托 |
| 每日总下单次数（买卖一起） | 单个客户 ≤ 50 笔/天 | 当日拒绝新委托 |

### 美股市场

| 限制项 | 具体规则 |
|--------|---------|
| 可交易品种 | 仅开放美股正股交易 |
| 交易单位 | 1 股起买，仅支持整股，不允许碎股委托 |
| 单笔委托买入 | ≤ 10 股 且 ≤ 50 USD（市价单没有价格，只有股数限制） |
| 委托类型 | 仅支持限价单、市价单 |

### 港股市场

| 限制项 | 具体规则 |
|--------|---------|
| 交易单位 | 必须按手交易，每手股数以交易所官方定义为准 |
| 单笔委托买入 | 仅允许委托 1 手，不允许多手 且 ≤ 2000 HKD（竞价单、市价单没有价格，仅检验手数股数） |
| 委托类型 | 仅支持：港股限价单(3)、特别限价单(5)、增强限价单(4)、竞价单、竞价限价单、市价单(9) |

### A 股市场（中华通 / 港股通）

| 限制项 | 具体规则 |
|--------|---------|
| 交易单位 | 必须按手交易，每手股数以交易所官方定义为准 |
| 单笔委托买入 | 仅允许委托 1 手，不允许多手 且 ≤ 2000 CNH |
| 委托类型 | 仅支持限价单 |

> 市场代码：上交所 `sh`，深交所 `sz`。币种为 CNH（人民币），价格保留 2 位小数。

### 统一客户额度限制

| 限制项 | 具体规则 |
|--------|---------|
| 单日累计交易金额（成交 + 未完成订单总额） | 单个客户 AI 渠道买卖总和 ≤ 15000 HKD（港美A不区分） |
| 每小时下单次数（买卖一起） | 单个客户 AI 渠道 ≤ 10 笔/小时 |

## 常见错误处理

| 场景 | 处理方式 |
|------|---------|
| 鉴权过期 | SDK 自动续期，一般无需处理 |
| 资金不足 | 先用 `query_funds.py summary` 确认 |
| 价格不合法 | 先用 `query_price.py quote` 获取最新价 |
| 数量不合法 | 港股注意整手（用 `--check-only` 查 `lotSize`），美股可 1 股起 |
| 订单类型不支持 | 仅支持竞价限价单(1)、竞价单(2)、限价单(3)、增强限价单(4)、特别限价单(5)和市价单(9)，参考上方订单类型表 |
