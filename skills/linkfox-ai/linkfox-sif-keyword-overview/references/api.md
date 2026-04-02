# SIF-关键词竞品数量 API 参考

## 调用规范

- **请求地址**：`https://tool-gateway.linkfox.com/sif/keywordOverview`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOXAGENT_API_KEY` 读取（如未配置，提示用户前往 https://yxgb3sicy7.feishu.cn/wiki/GIkkweGghiyzkqkRXQKc2n0Tnre 申请）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 是 | 关键词，尽量翻译成对应国家站点的语言。最大长度：1000字符 |
| country | string | 否 | 国家站点，默认 `US`。可选值：US、CA、MX、UK、DE、FR、IT、ES、JP、IN、AU、BR、NL、SE、PL、TR、AE、SA、SG |


## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| msg | string | 消息 |
| total | integer | 数据总量。注意：本接口通常只返回单条数据，total 通常为1 |
| code | string | 返回码 |
| data | array | 返回数据（详见下方数据字段） |
| costTime | integer | 耗时（ms） |
| costToken | integer | 消耗token |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| title | string | 标题 |

### 数据字段（`data` 数组中的每个对象）

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | string | 关键词。搜索查询的关键词文本 |
| keywordPopularityRank | integer | 关键词热度排名。该关键词的月搜索量在亚马逊所有关键词中的排名，数值越小表示搜索量越大 |
| estimatedWeeklySearchVolume | integer | 周预估搜索量。该关键词在亚马逊上每周的预估搜索次数，反映该词的搜索热度 |
| supplyDemandRatio | number | 供需比率。供应与需求的比率，计算公式：搜索结果商品数 / 月搜索量，数值越小表示竞争越小、机会越大 |
| totalSearchResultProductCount | integer | 搜索结果商品总数。在该关键词下显示的所有商品总数（包括自然搜索、广告位、推荐位等） |
| naturalSearchProductCount | integer | 自然搜索商品数量。在该关键词的自然搜索结果中展示的商品数量（不包括广告位） |
| sponsoredProductsCount | integer | SP广告商品数量。在该关键词下投放Sponsored Products（赞助商品）广告的商品数量 |
| brandAdProductCount | integer | 品牌广告商品数量。在该关键词下投放品牌广告（Brand Ads）的商品数量 |
| videoAdProductCount | integer | 视频广告商品数量。在该关键词下投放视频广告（Video Ads）的商品数量 |
| paidAdvertisingProductCount | integer | PPC广告商品总数。在该关键词下所有PPC付费广告（包括SP、品牌广告、视频广告等）的商品总数 |
| amazonChoiceProductCount | integer | Amazon's Choice商品数量。在该关键词下获得Amazon's Choice推荐标志的商品数量 |
| topRatedProductCount | integer | Top Rated推荐商品数量。在该关键词下出现在Top Rated（高评分）推荐位的商品数量 |
| searchRecommendationProductCount | integer | 搜索推荐商品数量。在该关键词搜索时亚马逊推荐的商品数量 |
| editorialRecommendationsProductCount | integer | Editorial Recommendations商品数量。在该关键词下出现在编辑推荐位的商品数量 |
| totalMarketplaceKeywordCount | integer | 站点关键词总量。该站点（如美国站）所有关键词的总数量，用于了解市场整体规模 |
| keywordDataUpdateTime | string | 关键词数据更新时间。该关键词相关数据的最后更新时间 |

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
curl -X POST https://tool-gateway.linkfox.com/sif/keywordOverview \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "wireless charger", "country": "US"}'
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
