# 资金流水 - CashFlows

> **POST** `https://openapi-sit.fosunxcz.com/api/v1/trade/CashFlows`

查询指定账户的资金流水记录。

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
| `businessType` | array[integer] | 否 | 业务类型 |
| `date` | string | 否 | 日期，格式 `YYYY-MM-DD` |
| `flowType` | integer | 否 | 流水类型 |
| `tradeDateFrom` | string | 否 | 交易开始日期，格式 `YYYY-MM-DD` |
| `tradeDateTo` | string | 否 | 交易结束日期，格式 `YYYY-MM-DD` |

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
        "amount": 0,
        "businessType": 0,
        "createdAt": "string",
        "currency": "string",
        "description": "string",
        "direction": 0,
        "exchangeCode": "string",
        "flowId": "string",
        "flowType": 0,
        "productCode": "string",
        "remark": "string",
        "tradeDate": "string"
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
| `data.count` | integer | 当前返回记录数 |
| `data.list` | array[object] | 资金流水列表 |
| `data.start` | integer | 起始偏移量 |
| `data.total` | integer | 总记录数 |

#### list 数组中每个对象的字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `amount` | number | 金额 |
| `businessType` | integer | 业务类型 |
| `createdAt` | string | 创建时间 |
| `currency` | string | 币种 |
| `description` | string | 描述 |
| `direction` | integer | 资金方向 |
| `exchangeCode` | string | 交易所代码 |
| `flowId` | string | 流水 ID |
| `flowType` | integer | 流水类型 |
| `productCode` | string | 产品代码 |
| `remark` | string | 备注 |
| `tradeDate` | string | 交易日期 |

### 400 - 请求错误

请求参数不合法或缺少必填字段时返回。

---

## 使用示例

### cURL

```bash
curl --request POST \
  --url https://openapi-sit.fosunxcz.com/api/v1/trade/CashFlows \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'X-api-key: YOUR_API_KEY' \
  --header 'X-lang: zh-CN' \
  --header 'X-request-id: UNIQUE_REQUEST_ID' \
  --header 'X-session: YOUR_SESSION_ID' \
  --data '{
  "subAccountId": "SA001",
  "tradeDateFrom": "2026-03-01",
  "tradeDateTo": "2026-03-12"
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
    "subAccountId": "SA001",
    "tradeDateFrom": "2026-03-01",
    "tradeDateTo": "2026-03-12",
}

url = f"{BASE_URL}/api/v1/trade/CashFlows"
response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

---

## 常见场景

### 1. 查询指定日期范围的资金流水

```json
{
  "subAccountId": "SA001",
  "tradeDateFrom": "2026-03-01",
  "tradeDateTo": "2026-03-12"
}
```

### 2. 查询指定日期的资金流水

```json
{
  "subAccountId": "SA001",
  "date": "2026-03-12"
}
```

### 3. 按业务类型筛选资金流水

```json
{
  "subAccountId": "SA001",
  "businessType": [1, 2],
  "tradeDateFrom": "2026-03-01",
  "tradeDateTo": "2026-03-12"
}
```

### 4. 按流水类型筛选

```json
{
  "subAccountId": "SA001",
  "flowType": 1,
  "tradeDateFrom": "2026-03-01",
  "tradeDateTo": "2026-03-12"
}
```
