# 查询买卖信息 - BidAskInfo

> **POST** `https://openapi-sit.fosunxcz.com/api/v1/trade/BidAskInfo`

根据账户与标的查询最大可买、可卖数量及购买力等信息。通常在下单前调用，用于展示用户的可用资金和可交易数量。

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

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `clientId` | integer | 否 | 客户 ID |
| `subAccountId` | string | 是 | 证券账号 |
| `stockCode` | string | 是 | 股票代码，如 `00700` |
| `marketCode` | string | 是 | 市场代码。枚举值：`hk`=港股，`us`=美股 |
| `orderType` | integer | 是 | 订单类型（见下方枚举表） |
| `direction` | integer | 否 | 订单方向。枚举值：`1`=买（默认），`2`=卖 |
| `quantity` | string | 否 | 委托订单数量 |
| `price` | string | 否 | 委托订单价格 |
| `trigPrice` | string | 条件必填 | 条件单触发价，orderType 为 `31`、`32` 时必填 |

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

---

## 响应

### 200 - 成功

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "availableWithdrawBalance": "string",
    "baseQuantitySell": 0,
    "cashPurchasePower": "string",
    "cashQuantityBuy": 0,
    "currency": "string",
    "financingQty": 0,
    "lotSize": 0,
    "maxPurchasePower": "string",
    "maxQuantityBuy": 0,
    "maxQuantitySell": 0,
    "singleWithdrawBalance": "string",
    "totalAssets": "string"
  }
}
```

#### 响应公共字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | 状态码，`0` 表示成功 |
| `message` | string | 状态消息 |

#### data 字段详解

| 字段 | 类型 | 说明 |
|------|------|------|
| `availableWithdrawBalance` | string | 总账户可用现金 |
| `singleWithdrawBalance` | string | 当前股票币种对应的币种账户可用现金 |
| `totalAssets` | string | 总资产 |
| `currency` | string | 币种。`HKD`=港币，`USD`=美元，`CNH`/`CNY`=人民币 |
| `maxPurchasePower` | string | 最大购买力 |
| `cashPurchasePower` | string | 现金购买力 |
| `maxQuantityBuy` | integer | 最大可买数量 |
| `cashQuantityBuy` | integer | 现金可买数量 |
| `maxQuantitySell` | integer | 持仓可卖数量（包含关联币种可卖持仓数量） |
| `baseQuantitySell` | integer | 本币种可卖数量（不包含关联币种可卖持仓数量） |
| `financingQty` | integer | 最大可融资（买多）/ 融券（卖空）数量 |
| `lotSize` | integer | 每手股数 |

### 400 - 请求错误

请求参数不合法或缺少必填字段时返回。

---

## 使用示例

### cURL

```bash
curl --request POST \
  --url https://openapi-sit.fosunxcz.com/api/v1/trade/BidAskInfo \
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
  "orderType": 3,
  "direction": 1,
  "price": "400.000"
}'
```

### Python

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

payload = {
    "clientId": 12345,
    "subAccountId": "SA001",
    "stockCode": "00700",
    "marketCode": "hk",
    "orderType": 3,
    "direction": 1,
    "price": "400.000",
}

url = f"{BASE_URL}/api/v1/trade/BidAskInfo"
response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

if result["code"] == 0:
    data = result["data"]
    print(f"最大可买: {data['maxQuantityBuy']}")
    print(f"持仓可卖: {data['maxQuantitySell']}")
    print(f"最大购买力: {data['maxPurchasePower']}")
    print(f"每手股数: {data['lotSize']}")
```

---

## 典型使用场景

### 1. 下单前查询可买数量

在买入下单前，先调用 BidAskInfo 查询该股票的最大可买数量和购买力，确保下单数量不超过可用额度。

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "stockCode": "00700",
  "marketCode": "hk",
  "orderType": 3,
  "direction": 1,
  "price": "400.000"
}
```

### 2. 卖出前查询可卖数量

在卖出下单前，查询当前持仓的可卖数量。

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "stockCode": "00700",
  "marketCode": "hk",
  "orderType": 3,
  "direction": 2
}
```

### 3. 美股市价单查询

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "stockCode": "AAPL",
  "marketCode": "us",
  "orderType": 9,
  "direction": 1
}
```
