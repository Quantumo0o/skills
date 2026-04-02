# SIF-关键词流量来源 API 参考

## 调用规范

- **请求地址**：`https://tool-gateway.linkfox.com/sif/keywordSummary`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOXAGENT_API_KEY` 读取（如未配置，提示用户前往 https://yxgb3sicy7.feishu.cn/wiki/GIkkweGghiyzkqkRXQKc2n0Tnre 申请）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKeyword | string | 是 | 搜索关键词，尽量翻译成对应国家站点的语言。最大长度1000字符 |
| country | string | 否 | 国家站点，默认 `US`。可选值：US、CA、MX、UK、DE、FR、IT、ES、JP、IN、AU、BR、NL、SE、PL、TR、AE、SA、SG |
| condition | string | 否 | 条件筛选，每次只能传一个。可选值：`nfPosition`（自然流量词）、`isSpAd`（SP广告词）、`isTopAd`（顶部品牌广告词）、`isBottomAd`（底部品牌广告词）、`isVedioAd`（视频广告词）、`isAC`（AC词）、`isER`（ER词）、`isTR`（TR词）、`isTRFOB`（TRFOB词）、`isBrandAd`（品牌广告词）、`isPPCAd`（PPC广告词）、`isSearchRecommend`（搜索推荐词） |
| pageNum | integer | 否 | 页码，默认 `1` |
| pageSize | integer | 否 | 每页数量，最小10，最大100，默认 `100` |
| desc | boolean | 否 | 是否降序，默认 `true` |


## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| code | string | 返回码 |
| msg | string | 消息 |
| total | integer | 本次实际返回的数据数量 |
| data | array | 返回数据，商品关键词流量数据对象数组 |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| title | string | 标题 |
| isParentAsin | boolean | 搜索的是否是父ASIN |
| variantsNum | integer | 有关键词的变体商品数量 |
| noKeywordVariantsNum | integer | 无关键词的变体商品数量 |
| costTime | integer | 耗时（ms） |
| costToken | integer | 消耗token |

### 数据项字段（`data` 数组中的每个对象）

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN编码。亚马逊商品标准识别码（Amazon Standard Identification Number） |
| productTitle | string | 商品标题。亚马逊页面显示的完整商品标题 |
| productCategory | string | 商品类目。该商品在亚马逊上所属的行业类目 |
| productPrice | number | 商品售价。当前亚马逊页面显示的商品价格 |
| productImageUrl | string | 商品主图URL。商品在亚马逊页面上的主要展示图片链接 |
| productFeatures | array | 商品特征列表。商品在亚马逊页面上列出的主要特性和卖点 |
| customerRatingCount | integer | 客户评分总数。该商品在亚马逊上获得的客户评分总数 |
| isVariantProduct | boolean | 是否为变体。true=该ASIN是父ASIN下的变体（如不同颜色、尺寸），false=独立ASIN或父ASIN |
| isMonitored | boolean | 是否已监控。true=该商品在监控列表中，false=未监控 |
| monitoringStartTime | string | 商品关注时间。该商品被添加到监控系统的时间 |
| totalTrafficKeywordCount | integer | 流量关键词总数。该商品在所有渠道（自然搜索+各类广告位+推荐位）被发现的关键词总数 |
| totalExposureScore | number | 总曝光分数。该商品在所有关键词下的曝光量综合评分，分数越高表示整体曝光量越大 |
| naturalSearchKeywordCount | integer | 自然搜索关键词数量。该商品在自然搜索结果中被发现的关键词总数（不包括广告位） |
| naturalSearchExposureScore | number | 自然搜索曝光总分。该商品在自然搜索结果位置的曝光量综合评分 |
| naturalSearchExposureRatio | number | 自然搜索曝光占比。自然搜索曝光分数占总曝光分数的百分比，反映自然流量的比重 |
| naturalSearchTrafficSources | array | 自然搜索流量来源标记。如果该数组不为空，表示商品有自然搜索流量。数组内容标记具体的自然搜索类型 |
| sponsoredProductsKeywordCount | integer | SP广告关键词数量。该商品在Sponsored Products（赞助商品）广告位展示的关键词总数 |
| sponsoredProductsExposureScore | number | SP广告曝光总分。该商品在SP广告位的曝光量综合评分 |
| sponsoredProductsExposureRatio | number | SP广告曝光占比。SP广告曝光分数占总曝光分数的百分比，反映付费广告流量的比重 |
| brandAdKeywordCount | integer | 品牌广告关键词总数。该商品在品牌广告位（包括页面顶部和底部）展示的关键词总数 |
| brandAdExposureScore | number | 品牌广告曝光总分。该商品在品牌广告位的曝光量综合评分 |
| brandAdExposureRatio | number | 品牌广告曝光占比。品牌广告曝光分数占总曝光分数的百分比 |
| topBrandAdKeywordCount | integer | 页面顶部品牌广告关键词数量。该商品在搜索结果页面顶部品牌广告位展示的关键词总数 |
| bottomBrandAdKeywordCount | integer | 页面底部品牌广告关键词数量。该商品在搜索结果页面底部品牌广告位展示的关键词总数 |
| videoAdKeywordCount | integer | 视频广告关键词数量。该商品在视频广告位展示的关键词总数 |
| videoAdExposureScore | number | 视频广告曝光总分。该商品在视频广告位的曝光量综合评分 |
| videoAdExposureRatio | number | 视频广告曝光占比。视频广告曝光分数占总曝光分数的百分比 |
| amazonsChoiceKeywordCount | integer | Amazon's Choice关键词数量。该商品获得Amazon's Choice（亚马逊精选）推荐标志的关键词总数 |
| amazonsChoiceExposureScore | number | Amazon's Choice曝光总分。该商品作为AC推荐商品的曝光量综合评分 |
| amazonsChoiceExposureRatio | number | Amazon's Choice曝光占比。AC推荐曝光分数占总曝光分数的百分比 |
| editorialRecommendationsKeywordCount | integer | Editorial Recommendations关键词数量。该商品在编辑推荐位展示的关键词总数 |
| editorialRecommendationsExposureScore | number | Editorial Recommendations曝光总分。该商品在编辑推荐位的曝光量综合评分 |
| editorialRecommendationsExposureRatio | number | Editorial Recommendations曝光占比。ER推荐曝光分数占总曝光分数的百分比 |
| topRatedKeywordCount | integer | Top Rated推荐关键词数量。该商品在高评分推荐位展示的关键词总数 |
| topRatedExposureScore | number | Top Rated推荐曝光总分。该商品在TR推荐位的曝光量综合评分 |
| topRatedExposureRatio | number | Top Rated推荐曝光占比。TR推荐曝光分数占总曝光分数的百分比 |
| frequentlyBoughtKeywordCount | integer | 高频购买推荐关键词数量。该商品在Top Rated Frequently Bought（高评分高频购买）推荐位展示的关键词总数 |
| ppcTrafficSources | array | PPC付费广告流量来源标记。包含：SP广告（Sponsored Products）、头部品牌广告（Top Brand Ad）、底部品牌广告（Bottom Brand Ad）、视频广告（Video Ad） |
| amazonRecommendationSources | array | 亚马逊推荐流量来源标记。包含：Best Seller榜单、Amazon's Choice推荐、编辑推荐（ER）、高评分推荐（TR）、高频购买推荐（TRFOB）等 |
| promotionalDealSources | array | 促销活动流量来源标记。包含：优惠券（Coupon）、限时优惠（Limited Time Deal）、30天内最低价（Lowest Price in 30 Days）等 |

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
curl -X POST https://tool-gateway.linkfox.com/sif/keywordSummary \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"searchKeyword": "wireless charger", "country": "US"}'
```

### 带条件筛选（仅SP广告词）：

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/keywordSummary \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"searchKeyword": "wireless charger", "country": "US", "condition": "isSpAd"}'
```

### 带分页参数：

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/keywordSummary \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"searchKeyword": "phone case", "country": "US", "pageNum": 2, "pageSize": 50}'
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
