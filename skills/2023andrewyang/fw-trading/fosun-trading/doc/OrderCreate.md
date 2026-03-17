# 下单接口 - OrderCreate

> **POST** `https://openapi-sit.fosunxcz.com/api/v1/trade/OrderCreate`

提交委托订单。支持正股、期权（`productType=15`）、期权组合（`productType=16`）下单；期权需传 `expiry`、`strike`、`right`；期权组合需传 `combosType`、`legs` 等字段。

---

## 请求

### Headers

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `X-api-key` | string | 是 | API Key，标识客户端 |
| `X-lang` | string | 是 | 语言，如 `zh-CN`、`en` |
| `X-request-id` | string | 是 | 请求追踪 ID，每次请求需唯一 |
| `X-session` | string | 是 | 会话 ID，通过 SessionCreate 接口获取 |
| `Content-Type` | string | 是 | 固定值 `application/json` |
| `Accept` | string | 是 | 固定值 `application/json` |

### Body（application/json）

#### 基础字段

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `clientId` | integer | 是 | 客户 ID |
| `subAccountId` | string | 是 | 证券账户 ID，用于鉴权与路由 |
| `stockCode` | string | 是 | 股票代码，如 `00700` |
| `marketCode` | string | 是 | 市场代码。枚举值：`hk`=港股，`us`=美股，`sh`=上交所，`sz`=深交所 |
| `currency` | string | 是 | 币种。枚举值：`HKD`=港币，`USD`=美元，`CNH`=人民币 |
| `direction` | integer | 是 | 买卖方向。枚举值：`1`=买，`2`=卖（取值范围 1~2） |
| `orderType` | integer | 是 | 订单类型（见下方枚举表） |
| `quantity` | string | 是 | 委托订单数量，正整数 |
| `price` | string | 条件必填 | 委托价格。港股保留 3 位小数，其他保留 2 位小数。**非追踪单且非市价单时必填** |
| `productType` | integer | 否 | 产品类型。枚举值：`0`=正股（默认），`15`=期权，`16`=期权组合 |
| `expType` | integer | 否 | 订单时效类型。枚举值：`1`=当日有效（默认），`2`=撤单前有效（GTC） |
| `expiryDate` | string | 否 | 过期日期，格式 `YYYY-MM-DD`，用于 GTD 订单 |
| `allowPrePost` | integer | 否 | 是否允许盘前盘后。枚举值：`0`=不允许（默认），`1`=允许。美股支持 |
| `shortSellType` | string | 否 | 沽空类型（见下方枚举表），默认 `N` |

#### orderType 订单类型枚举

| 值 | 说明 |
|----|------|
| `1` | 竞价限价单 |
| `2` | 竞价单 |
| `3` | 限价单 |
| `4` | 增强限价单 |
| `5` | 特殊限价单 |
| `9` | 市价单 |
| `31` | 止损限价单 |
| `32` | 止盈限价单 |
| `33` | 跟踪止损单 |
| `34` | 止损单 |
| `35` | 止盈止损单 |

#### shortSellType 沽空类型枚举

| 值 | 说明 |
|----|------|
| `A` | 指数套利 |
| `B` | 强制平仓 |
| `C` | 补仓 |
| `F` | 被迫抛售 |
| `M` | 做市商/证券专家 |
| `N` | 没有沽空（默认） |
| `S` | 做市商/衍生品专家 |
| `Y` | 沽空 |

#### 期权相关字段（productType=15 时使用）

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `expiry` | string | 期权必填 | 期权到期日，格式 `YYYYMMDD`（如 `20260102`） |
| `strike` | string | 期权必填 | 行权价 |
| `right` | string | 期权必填 | 期权方向。枚举值：`CALL`=看涨，`PUT`=看跌 |

#### 期权组合相关字段（productType=16 时使用）

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `combosType` | string | 组合必填 | 期权组合类型（如垂直价差、跨式、蝶式等） |
| `legs` | array[object] | 组合必填 | 期权组合腿，非空数组 |

**legs 数组中每个对象的字段：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `stockCode` | string | 标的代码，期权对应的股票代码 |
| `expiry` | string | 该腿期权到期日，格式 `YYYYMMDD` |
| `strike` | string | 该腿行权价 |
| `right` | string | 该腿期权方向。枚举值：`CALL`=看涨，`PUT`=看跌 |
| `direction` | integer | 该腿买卖方向。枚举值：`1`=买，`2`=卖 |
| `productType` | integer | 该腿产品类型。枚举值：`15`=期权 |
| `ratio` | integer | 该腿比例，组合中各腿数量比例，默认 `1` |

#### 条件单/追踪止损单相关字段

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `trigPrice` | string | 条件必填 | 触发价，orderType 为 `31`、`32` 时必填 |
| `spread` | string | 否 | 追踪止损单价差 |
| `tailType` | integer | 条件必填 | 追踪类型。枚举值：`1`=金额，`2`=比例。orderType 为 `33` 时必填 |
| `tailAmount` | string | 条件必填 | 追踪金额，orderType 为 `33` 且 `tailType=1` 时必填 |
| `tailPct` | string | 条件必填 | 追踪比例，orderType 为 `33` 且 `tailType=2` 时必填，如 `0.05` 表示 5% |

---

## 响应

### 200 - 成功

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "orderId": "string",
    "orderStatus": 0
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | 状态码，`0` 表示成功 |
| `message` | string | 状态消息 |
| `data.orderId` | string | 订单 ID，系统生成的唯一订单标识 |
| `data.orderStatus` | integer | 订单状态（见下方枚举表） |

#### orderStatus 订单状态枚举

| 值 | 说明 |
|----|------|
| `10` | 未报 |
| `20` | 待报 |
| `40` | 已报 |
| `50` | 全成 |
| `60` | 部成 |
| `70` | 已撤 |
| `80` | 部撤 |
| `90` | 废单 |

### 400 - 请求错误

请求参数不合法或缺少必填字段时返回。

---

## 使用示例

### cURL

```bash
curl --request POST \
  --url https://openapi-sit.fosunxcz.com/api/v1/trade/OrderCreate \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'X-api-key: YOUR_API_KEY' \
  --header 'X-lang: zh-CN' \
  --header 'X-request-id: UNIQUE_REQUEST_ID' \
  --header 'X-session: YOUR_SESSION_ID' \
  --data '{
  "clientId": 12345,
  "subAccountId": "SA001",
  "stockCode": "00700",
  "marketCode": "hk",
  "currency": "HKD",
  "direction": 1,
  "orderType": 3,
  "price": "400.000",
  "quantity": "100",
  "productType": 0,
  "expType": 1,
  "allowPrePost": 0,
  "shortSellType": "N"
}'
```

### Python（使用 SDK）

```python
import uuid
import json
import requests

BASE_URL = "https://openapi-sit.fosunxcz.com"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-api-key": "YOUR_API_KEY",
    "X-lang": "zh-CN",
    "X-request-id": str(uuid.uuid4()),
    "X-session": "YOUR_SESSION_ID",
}

# 正股限价买单示例
payload = {
    "clientId": 12345,
    "subAccountId": "SA001",
    "stockCode": "00700",
    "marketCode": "hk",
    "currency": "HKD",
    "direction": 1,        # 买入
    "orderType": 3,        # 限价单
    "price": "400.000",    # 港股保留 3 位小数
    "quantity": "100",
    "productType": 0,      # 正股
    "expType": 1,          # 当日有效
    "allowPrePost": 0,
    "shortSellType": "N",
}

url = f"{BASE_URL}/api/v1/trade/OrderCreate"
response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

---

## 常见场景

### 1. 港股限价买入

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "stockCode": "00700",
  "marketCode": "hk",
  "currency": "HKD",
  "direction": 1,
  "orderType": 3,
  "price": "400.000",
  "quantity": "100",
  "productType": 0
}
```

### 2. 美股市价卖出（允许盘前盘后）

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "stockCode": "AAPL",
  "marketCode": "us",
  "currency": "USD",
  "direction": 2,
  "orderType": 9,
  "quantity": "10",
  "productType": 0,
  "allowPrePost": 1
}
```

### 3. 期权下单（看涨期权买入）

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "stockCode": "AAPL",
  "marketCode": "us",
  "currency": "USD",
  "direction": 1,
  "orderType": 3,
  "price": "5.50",
  "quantity": "1",
  "productType": 15,
  "expiry": "20260630",
  "strike": "200.00",
  "right": "CALL"
}
```

### 4. 止损限价单

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "stockCode": "00700",
  "marketCode": "hk",
  "currency": "HKD",
  "direction": 2,
  "orderType": 31,
  "price": "380.000",
  "quantity": "100",
  "productType": 0,
  "trigPrice": "385.000"
}
```

### 5. 跟踪止损单（按比例）

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "stockCode": "00700",
  "marketCode": "hk",
  "currency": "HKD",
  "direction": 2,
  "orderType": 33,
  "quantity": "100",
  "productType": 0,
  "tailType": 2,
  "tailPct": "0.05"
}
```
