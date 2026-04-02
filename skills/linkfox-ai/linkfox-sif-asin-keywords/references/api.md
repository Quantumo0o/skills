# SIF-ASIN的关键词 API 参考

## 调用规范

- **请求地址**：`https://tool-gateway.linkfox.com/sif/asinKeywords`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOXAGENT_API_KEY` 读取（如未配置，提示用户前往 https://yxgb3sicy7.feishu.cn/wiki/GIkkweGghiyzkqkRXQKc2n0Tnre 申请）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| asin | string | 是 | ASIN码，最大长度1000字符。本工具一次只能查询一个ASIN |
| country | string | 否 | 国家站点，默认 `US`。可选值：US、CA、MX、UK、DE、FR、IT、ES、JP、IN、AU、BR、NL、SE、PL、TR、AE、SA、SG |
| keyword | string | 否 | 关键词，最大长度1000。尽量翻译成对应国家站点的语言 |
| conditions | string | 否 | 条件筛选，多个条件以英文逗号隔开。可选值：`nfPosition`（自然流量词）、`isSpAd`（SP广告词）、`isBrandAd`（品牌广告词）、`isVedioAd`（视频广告词）、`isAC`（AC推荐词）、`isER`（ER推荐词）、`isTr`（TR推荐词）、`isMainKw`（主要流量词）、`isAccurateKw`（精准流量词）、`isAccurateAboveKw`（精准大词）、`isAccurateTailKw`（精准长尾词）、`isPurchaseKw`（出单词）、`isQualityKw`（转化优质词）、`isStableKw`（转化平稳词）、`isLossKw`（转化流失词）、`isInvalidKw`（无效曝光词） |
| sortBy | string | 否 | 排序字段。可选值：`lastRank`（自然排名）、`adLastRank`（广告排名）、`updateTime`（关键词抓取时间）、`searchesRank`（搜索排名）、`estSearchesNum`（月搜索量）。空字符串为默认系统排序 |
| desc | boolean | 否 | 是否降序，默认 `true` |
| pageNum | integer | 否 | 页码，默认 `1` |
| pageSize | integer | 否 | 每页数量，最小10，最大100，默认 `100` |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| code | string | 返回码 |
| msg | string | 消息 |
| total | integer | 本次实际返回的数据数量 |
| data | array | 返回数据数组（详见下方） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| title | string | 标题 |
| isParentAsin | boolean | 是否是父体 |
| hasVaiants | boolean | 是否有变体 |
| abaCreateDateWeek | string | 最新周ABA时间 |
| costTime | integer | 耗时（ms） |
| costToken | integer | 消耗token |

### data 数组元素字段

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | string | 关键词 |
| asin | string | 商品ASIN |
| productNaturalRank | integer | 商品自然搜索排名。该商品在此关键词下的自然搜索结果中的位置排名，如1表示排在搜索结果第1位（首位） |
| naturalRankDisplay | string | 自然排名显示文本。自然搜索排名的字符串表示形式 |
| productAdRank | integer | 商品SP广告排名。该商品在此关键词下的Sponsored Products广告位中的排名位置，如3表示排在广告位第3位 |
| adRankDisplay | string | 广告排名显示文本。SP广告排名的字符串表示形式 |
| weeklySearchVolume | integer | 周搜索量。该关键词在亚马逊平台每周的预估搜索次数 |
| keywordPopularityRank | integer | 关键词搜索热度排名。该关键词的月搜索量在亚马逊所有关键词中的排名，数值越小表示搜索量越大，如203表示该词搜索热度排第203名 |
| trafficShare | number | 流量占比。该关键词为商品带来的流量占所有关键词总流量的比例，其中1表示100% |
| displayPositionTypes | array | 商品展示位置类型数组。可能包含以下值：natural=自然搜索结果位；ac=Amazon's Choice推荐位；sp=Sponsored Products赞助商品广告位；top=页面顶部品牌广告位；bottom=页面底部品牌广告位；er=Editorial Recommendations编辑推荐位；vedio=视频广告位；tr=Top Rated高评分推荐位；trfob=Top Rated Frequently Bought高频购买推荐位 |
| trafficCharacteristicMarkers | array | 关键词流量特征标记数组。可能包含以下值：isMainKw=主要流量词（为该商品带来主要流量的核心词）；isAccurateKw=精准流量词（与商品高度相关的精准词）；isAccurateAboveKw=精准大词（搜索量大且精准的关键词）；isAccurateTailKw=精准长尾词（搜索量较小但精准的长尾关键词） |
| conversionPerformanceMarkers | array | 转化效果标记数组。可能包含以下值：isPurchaseKw=出单词（通过该词产生过订单）；isQualityKw=转化优质词（转化率高的优质关键词）；isStableKw=转化平稳词（转化表现稳定的关键词）；isLossKw=转化流失词（曾经转化好但现在流失的关键词）；isInvalidKw=无效曝光词（有曝光但无转化的无效词） |
| lastNaturalRankTime | string | 最近有效自然排名的时间。商品在此关键词下最近一次有效自然搜索排名的记录时间 |
| lastAdRankTime | string | 最近有效SP广告排名的时间。商品在此关键词下最近一次Sponsored Products广告排名的记录时间 |
| updateTime | string | 关键词数据更新时间 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | 检查 `Authorization` Header 是否正确传入 API Key |
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/asinKeywords \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asin": "B0XXXXXXXX", "country": "US", "pageSize": 100, "sortBy": "estSearchesNum", "desc": true}'
```

### 带关键词筛选和条件的示例

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/asinKeywords \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asin": "B0XXXXXXXX", "country": "US", "keyword": "charger", "conditions": "nfPosition,isPurchaseKw", "sortBy": "lastRank", "desc": false, "pageNum": 1, "pageSize": 50}'
```

---

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-xxx-xxx",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter
- `sentiment`: Choose ONE — `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE — `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
