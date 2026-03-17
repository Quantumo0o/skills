# 查询订单列表 - OrderList

> **POST** `https://openapi-sit.fosunxcz.com/api/v1/trade/OrderList`

分页查询指定账户的订单列表。支持按市场、方向、状态、股票代码、日期范围等条件筛选，按提交时间排序。

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
| `subAccountId` | string | 是 | 证券账户 |
| `clientId` | integer | 否 | 客户 ID |
| `start` | integer | 否 | 偏移量，分页起始位置，从 0 开始 |
| `count` | integer | 否 | 返回数量，分页大小，默认 20 |
| `sort` | string | 否 | 排序方式。枚举值：`desc`=逆序（默认），`asc`=顺序。按提交时间排序 |
| `direction` | integer | 否 | 查询指定订单方向。枚举值：`1`=买，`2`=卖。不传则返回全部方向 |
| `market` | array[string] | 否 | 查询指定市场。枚举值：`hk`=港股，`us`=美股。不传则返回全部市场 |
| `stockCode` | string | 否 | 股票代码，如 `00700` |
| `statusArr` | array[integer] | 否 | 查询指定状态订单（见下方枚举表）。不传返回所有状态 |
| `fromDate` | string | 否 | 开始日期，格式 `yyyy-mm-dd`，不传则默认查询最近 7 天 |
| `toDate` | string | 否 | 结束日期，格式 `yyyy-mm-dd` |

#### statusArr 订单状态枚举

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
        "canCancel": 0,
        "canModify": 0,
        "currency": "string",
        "direction": 0,
        "embeddedBillStatus": 0,
        "expType": 0,
        "filledPrice": "string",
        "filledQuantity": "string",
        "filledTime": "string",
        "marketCode": "string",
        "name": "string",
        "orderId": "string",
        "orderStatus": 0,
        "orderType": 0,
        "power": 0,
        "price": "string",
        "quantity": "string",
        "spread": "string",
        "spreadCode": 0,
        "stockCode": "string",
        "subAccountId": "string",
        "submittedTime": "string",
        "submittedTimestamp": 0,
        "tailAmount": "string",
        "tailPct": "string",
        "tailType": 0,
        "timeInForce": 0,
        "timeZone": "string",
        "trigPrice": "string",
        "trigTime": "string"
      }
    ],
    "start": 0,
    "total": 0
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
| `count` | integer | 当前返回的记录数量 |
| `start` | integer | 当前分页起始位置 |
| `total` | integer | 符合条件的订单总数 |
| `list` | array[object] | 订单列表 |

#### list 中每个订单对象的字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `orderId` | string | 订单 ID |
| `stockCode` | string | 股票代码 |
| `name` | string | 股票名称 |
| `marketCode` | string | 市场代码（`hk`、`us`） |
| `currency` | string | 币种（`HKD`、`USD`、`CNH`） |
| `subAccountId` | string | 证券账户 |
| `direction` | integer | 买卖方向。`1`=买，`2`=卖 |
| `orderType` | integer | 订单类型（见下方枚举表） |
| `orderStatus` | integer | 订单状态（见上方 statusArr 枚举表） |
| `price` | string | 委托价格 |
| `quantity` | string | 委托数量 |
| `filledPrice` | string | 成交价格 |
| `filledQuantity` | string | 成交数量 |
| `filledTime` | string | 成交时间 |
| `submittedTime` | string | 提交时间 |
| `submittedTimestamp` | integer | 提交时间戳 |
| `timeZone` | string | 时区 |
| `expType` | integer | 订单时效类型。`1`=当日有效，`2`=撤单前有效（GTC） |
| `timeInForce` | integer | 有效期类型 |
| `canCancel` | integer | 是否可撤单。`0`=否，`1`=是 |
| `canModify` | integer | 是否可改单。`0`=否，`1`=是 |
| `power` | integer | 购买力标识 |
| `embeddedBillStatus` | integer | 内嵌账单状态 |
| `trigPrice` | string | 条件单触发价 |
| `trigTime` | string | 条件单触发时间 |
| `spread` | string | 追踪止损价差 |
| `spreadCode` | integer | 价差代码 |
| `tailType` | integer | 追踪类型。`1`=金额，`2`=比例 |
| `tailAmount` | string | 追踪金额 |
| `tailPct` | string | 追踪比例 |

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

### 400 - 请求错误

请求参数不合法或缺少必填字段时返回。

---

## 使用示例

### cURL

```bash
curl --request POST \
  --url https://openapi-sit.fosunxcz.com/api/v1/trade/OrderList \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'X-api-key: YOUR_API_KEY' \
  --header 'X-lang: zh-CN' \
  --header 'X-request-id: UNIQUE_REQUEST_ID' \
  --header 'X-session: YOUR_SESSION_ID' \
  --data '{
  "subAccountId": "SA001",
  "clientId": 12345,
  "start": 0,
  "count": 20,
  "sort": "desc"
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
    "subAccountId": "SA001",
    "clientId": 12345,
    "start": 0,
    "count": 20,
    "sort": "desc",
}

url = f"{BASE_URL}/api/v1/trade/OrderList"
response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

if result["code"] == 0:
    data = result["data"]
    print(f"总订单数: {data['total']}")
    for order in data["list"]:
        print(f"  订单 {order['orderId']}: {order['stockCode']} "
              f"{'买' if order['direction'] == 1 else '卖'} "
              f"数量={order['quantity']} 价格={order['price']} "
              f"状态={order['orderStatus']}")
```

---

## 常见场景

### 1. 查询全部订单（默认分页）

```json
{
  "subAccountId": "SA001",
  "start": 0,
  "count": 20,
  "sort": "desc"
}
```

### 2. 按市场筛选（仅港股）

```json
{
  "subAccountId": "SA001",
  "market": ["hk"],
  "start": 0,
  "count": 20
}
```

### 3. 查询指定状态订单（已报 + 部成）

```json
{
  "subAccountId": "SA001",
  "statusArr": [40, 60],
  "start": 0,
  "count": 20
}
```

### 4. 按日期范围查询

```json
{
  "subAccountId": "SA001",
  "fromDate": "2026-03-01",
  "toDate": "2026-03-12",
  "start": 0,
  "count": 50
}
```

### 5. 查询指定股票的买单

```json
{
  "subAccountId": "SA001",
  "stockCode": "00700",
  "direction": 1,
  "start": 0,
  "count": 20
}
```
