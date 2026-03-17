# 当前持仓 - Holdings

> **POST** `https://openapi-sit.fosunxcz.com/api/v1/portfolio/Holdings`

查询指定账户的持仓列表。

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
| `clientId` | integer | 否 | 客户号 |
| `count` | integer | 否 | 返回数量 |
| `currencies` | array[string] | 否 | 币种信息 |
| `productTypes` | array[string] | 否 | 产品类型 |
| `start` | integer | 否 | 偏移 |
| `subAccountId` | string | 否 | 证券账户 |
| `symbols` | array[string] | 否 | 产品信息数组，例如 `["hk00700"]` |
| `useUsNight` | boolean | 否 | 是否使用美股夜盘价，`true` 使用，`false` 不使用，默认 `false` |
| `useUsPost` | boolean | 否 | 是否使用美股盘后，默认 `false` |
| `useUsPre` | boolean | 否 | 是否使用美股盘前，默认 `false` |

---

## 响应

### 200 - 成功

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "count": 0,
    "list": [
      {
        "avgCost": "string",
        "buyable": true,
        "closePrice": "string",
        "currency": "string",
        "dilutedCost": "string",
        "dtdcQty": "string",
        "marketCode": "string",
        "stockCode": "string",
        "symbol": "string",
        "name": "string",
        "price": "string",
        "qtyOnHold": "string",
        "quantity": "string",
        "quantityAvail": "string",
        "sellable": true,
        "t1Qty": "string",
        "t2Qty": "string",
        "todayBuyAmount": "string",
        "todayBuyCount": 0,
        "todaySellAmount": "string",
        "todaySellCount": 0
      }
    ],
    "start": 0,
    "total": 0
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | 状态码，`0` 表示成功 |
| `message` | string | 状态消息 |
| `data.count` | integer | 当前返回记录数，最大 999 |
| `data.list` | array[object] | 持仓列表 |
| `data.start` | integer | 起始偏移量 |
| `data.total` | integer | 总记录数 |

#### list 数组中每个对象的字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `avgCost` | string | 平均成本 |
| `buyable` | boolean | 是否可买入 |
| `closePrice` | string | 收盘价 |
| `currency` | string | 币种 |
| `dilutedCost` | string | 摊薄成本 |
| `dtdcQty` | string | DTDC 数量 |
| `marketCode` | string | 市场代码 |
| `stockCode` | string | 股票代码 |
| `symbol` | string | 产品标识 |
| `name` | string | 产品名称 |
| `price` | string | 当前价格 |
| `qtyOnHold` | string | 冻结数量 |
| `quantity` | string | 持仓数量 |
| `quantityAvail` | string | 可用数量 |
| `sellable` | boolean | 是否可卖出 |
| `t1Qty` | string | T+1 待交收数量 |
| `t2Qty` | string | T+2 待交收数量 |
| `todayBuyAmount` | string | 今日买入金额 |
| `todayBuyCount` | integer | 今日买入笔数 |
| `todaySellAmount` | string | 今日卖出金额 |
| `todaySellCount` | integer | 今日卖出笔数 |

### 400 - 请求错误

请求参数不合法或缺少必填字段时返回。

---

## 使用示例

### cURL

```bash
curl --request POST \
  --url https://openapi-sit.fosunxcz.com/api/v1/portfolio/Holdings \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'X-api-key: YOUR_API_KEY' \
  --header 'X-lang: zh-CN' \
  --header 'X-request-id: UNIQUE_REQUEST_ID' \
  --header 'X-session: YOUR_SESSION_ID' \
  --data '{
  "clientId": 12345,
  "subAccountId": "SA001",
  "count": 50,
  "start": 0
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

payload = {
    "clientId": 12345,
    "subAccountId": "SA001",
    "count": 50,
    "start": 0,
}

url = f"{BASE_URL}/api/v1/portfolio/Holdings"
response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

---

## 常见场景

### 1. 查询全部持仓

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "count": 999,
  "start": 0
}
```

### 2. 查询指定股票的持仓

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "symbols": ["hk00700"]
}
```

### 3. 按币种筛选持仓

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "currencies": ["HKD"]
}
```

### 4. 查询美股持仓（使用盘前价格）

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "productTypes": ["us"],
  "useUsPre": true
}
```

### 5. 分页查询持仓

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "count": 20,
  "start": 0
}
```

第二页：

```json
{
  "clientId": 12345,
  "subAccountId": "SA001",
  "count": 20,
  "start": 20
}
```
