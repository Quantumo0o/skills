# 查询账户资金金额 - CashSummary

> **POST** `https://openapi-sit.fosunxcz.com/api/v1/portfolio/CashSummary`

查询指定账户的资金汇总与分币种明细。

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
| `subAccountId` | string | 是 | 证券账号 |
| `clientId` | integer | 否 | 客户号 |
| `currency` | string | 否 | 币种 |

---

## 响应

### 200 - 成功

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "breakdown": [
      {
        "cashPurchasingPower": "string",
        "currency": "string",
        "excessLiquidity": "string",
        "exchangeBalance": "string",
        "frozenBalance": "string",
        "fxRateToHKD": "string",
        "initialMargin": "string",
        "ledgerBalance": "string",
        "maintenanceMargin": "string",
        "marginPurchasingPower": "string",
        "maxPurchasingPower": "string",
        "realBuyBalance": "string",
        "realSellBalance": "string",
        "settdayBalance": "string",
        "t1dayBalance": "string",
        "tradedayBalance": "string",
        "unComeBuyBalance": "string",
        "unComeSellBalance": "string"
      }
    ],
    "summary": {
      "cashPurchasingPower": "string",
      "currency": "string",
      "excessLiquidity": "string",
      "frozenBalance": "string",
      "initialMargin": "string",
      "ledgerBalance": "string",
      "maintenanceMargin": "string",
      "marginPurchasingPower": "string",
      "maxPurchasingPower": "string",
      "realBuyBalance": "string",
      "realSellBalance": "string",
      "settdayBalance": "string",
      "t1dayBalance": "string",
      "tradedayBalance": "string",
      "unComeBuyBalance": "string",
      "unComeSellBalance": "string"
    }
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | 状态码，`0` 表示成功 |
| `message` | string | 状态消息 |
| `data.breakdown` | array[object] | 分币种资金明细列表 |
| `data.summary` | object | 资金汇总（折算后） |

#### breakdown 数组中每个对象的字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `cashPurchasingPower` | string | 现金购买力 |
| `currency` | string | 币种 |
| `excessLiquidity` | string | 超额流动性 |
| `exchangeBalance` | string | 交易所余额 |
| `frozenBalance` | string | 冻结金额 |
| `fxRateToHKD` | string | 兑港币汇率 |
| `initialMargin` | string | 初始保证金 |
| `ledgerBalance` | string | 账面余额 |
| `maintenanceMargin` | string | 维持保证金 |
| `marginPurchasingPower` | string | 保证金购买力 |
| `maxPurchasingPower` | string | 最大购买力 |
| `realBuyBalance` | string | 实际买入金额 |
| `realSellBalance` | string | 实际卖出金额 |
| `settdayBalance` | string | 交收日余额 |
| `t1dayBalance` | string | T+1 日余额 |
| `tradedayBalance` | string | 交易日余额 |
| `unComeBuyBalance` | string | 未交收买入金额 |
| `unComeSellBalance` | string | 未交收卖出金额 |

#### summary 对象的字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `cashPurchasingPower` | string | 现金购买力 |
| `currency` | string | 汇总币种 |
| `excessLiquidity` | string | 超额流动性 |
| `frozenBalance` | string | 冻结金额 |
| `initialMargin` | string | 初始保证金 |
| `ledgerBalance` | string | 账面余额 |
| `maintenanceMargin` | string | 维持保证金 |
| `marginPurchasingPower` | string | 保证金购买力 |
| `maxPurchasingPower` | string | 最大购买力 |
| `realBuyBalance` | string | 实际买入金额 |
| `realSellBalance` | string | 实际卖出金额 |
| `settdayBalance` | string | 交收日余额 |
| `t1dayBalance` | string | T+1 日余额 |
| `tradedayBalance` | string | 交易日余额 |
| `unComeBuyBalance` | string | 未交收买入金额 |
| `unComeSellBalance` | string | 未交收卖出金额 |

### 400 - 请求错误

请求参数不合法或缺少必填字段时返回。

---

## 使用示例

### cURL

```bash
curl --request POST \
  --url https://openapi-sit.fosunxcz.com/api/v1/portfolio/CashSummary \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'X-api-key: YOUR_API_KEY' \
  --header 'X-lang: zh-CN' \
  --header 'X-request-id: UNIQUE_REQUEST_ID' \
  --header 'X-session: YOUR_SESSION_ID' \
  --data '{
  "subAccountId": "SA001"
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
}

url = f"{BASE_URL}/api/v1/portfolio/CashSummary"
response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

---

## 常见场景

### 1. 查询账户全部币种资金汇总

```json
{
  "subAccountId": "SA001"
}
```

### 2. 查询指定币种的资金明细

```json
{
  "subAccountId": "SA001",
  "currency": "HKD"
}
```

### 3. 指定客户号查询资金

```json
{
  "subAccountId": "SA001",
  "clientId": 123456
}
```
