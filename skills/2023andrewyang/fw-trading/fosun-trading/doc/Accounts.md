# 查询账户列表 - Accounts

> **POST** `https://openapi-sit.fosunxcz.com/api/v1/account/Accounts`

查询主账户与子账户列表。

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

请求体为空 JSON 对象 `{}`，无需传入业务参数。

---

## 响应

### 200 - 成功

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "clientId": 0,
    "clientStatus": 0,
    "clientType": 0,
    "subAccounts": [
      {
        "chineseName": "string",
        "englishName": "string",
        "openDate": "string",
        "status": 0,
        "subAccountId": "string"
      }
    ]
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | 状态码，`0` 表示成功 |
| `message` | string | 状态消息 |
| `data.clientId` | integer | 客户号 |
| `data.clientStatus` | integer | 客户状态 |
| `data.clientType` | integer | 客户类型 |
| `data.subAccounts` | array[object] | 账户列表 |

#### subAccounts 数组中每个对象的字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `chineseName` | string | 中文名称 |
| `englishName` | string | 英文名称 |
| `openDate` | string | 开户日期 |
| `status` | integer | 账户状态 |
| `subAccountId` | string | 子账户 ID |

### 400 - 请求错误

请求参数不合法或缺少必填字段时返回。

---

## 使用示例

### cURL

```bash
curl --request POST \
  --url https://openapi-sit.fosunxcz.com/api/v1/account/Accounts \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'X-api-key: YOUR_API_KEY' \
  --header 'X-lang: zh-CN' \
  --header 'X-request-id: UNIQUE_REQUEST_ID' \
  --header 'X-session: YOUR_SESSION_ID' \
  --data '{}'
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

url = f"{BASE_URL}/api/v1/account/Accounts"
response = requests.post(url, headers=headers, json={})
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```
