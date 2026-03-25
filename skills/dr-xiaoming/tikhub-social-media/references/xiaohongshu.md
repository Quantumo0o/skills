# Xiaohongshu API Reference

Total endpoints: 68


## /api/v1/xiaohongshu/app_v2

### `GET /api/v1/xiaohongshu/app_v2/get_image_note_detail`
**获取图文笔记详情/Get image note detail**

Parameters:
  - `note_id`: 笔记ID/Note ID
  - `share_text`: 分享链接/Share link

### `GET /api/v1/xiaohongshu/app_v2/get_video_note_detail`
**获取视频笔记详情/Get video note detail**

Parameters:
  - `note_id`: 笔记ID/Note ID
  - `share_text`: 分享链接/Share link

### `GET /api/v1/xiaohongshu/app_v2/get_mixed_note_detail`
**获取首页推荐流笔记详情/Get mixed note detail from feed**

Parameters:
  - `note_id`: 笔记ID/Note ID
  - `share_text`: 分享链接/Share link

### `GET /api/v1/xiaohongshu/app_v2/get_note_comments`
**获取笔记评论列表/Get note comments**

Parameters:
  - `note_id`: 笔记ID/Note ID
  - `share_text`: 分享链接/Share link
  - `cursor`: 分页游标，首次请求留空/Pagination cursor, leave empty for first request
  - `index`: 评论索引，首次请求传0/Comment index, pass 0 for first request
  - `sort_strategy`: 排序策略/Sort strategy: default, latest_v2, like_count

### `GET /api/v1/xiaohongshu/app_v2/get_note_sub_comments`
**获取笔记二级评论列表/Get note sub comments**

Parameters:
  - `note_id`: 笔记ID/Note ID
  - `share_text`: 分享链接/Share link
  - `comment_id`*: 父评论ID/Parent comment ID
  - `cursor`: 分页游标，首次留空，翻页时从$.data.data.cursor中提取cursor值/Pagination cursor
  - `index`: 分页索引，首次传1，翻页时从$.data.data.cursor中提取index值/Pagination index, 

### `GET /api/v1/xiaohongshu/app_v2/get_user_info`
**获取用户信息/Get user info**

Parameters:
  - `user_id`: 用户ID/User ID
  - `share_text`: 分享链接/Share link

### `GET /api/v1/xiaohongshu/app_v2/get_user_posted_notes`
**获取用户笔记列表/Get user posted notes**

Parameters:
  - `user_id`: 用户ID/User ID
  - `share_text`: 分享链接/Share link
  - `cursor`: 分页游标，首次请求留空/Pagination cursor, leave empty for first request

### `GET /api/v1/xiaohongshu/app_v2/get_user_faved_notes`
**获取用户收藏笔记列表/Get user faved notes**

Parameters:
  - `user_id`: 用户ID/User ID
  - `share_text`: 分享链接/Share link
  - `cursor`: 分页游标，首次请求留空，翻页时传入上一页最后一条笔记的note_id/Pagination cursor, leave 

### `GET /api/v1/xiaohongshu/app_v2/search_notes`
**搜索笔记/Search notes**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `page`: 页码，从1开始/Page number, start from 1
  - `sort_type`: 排序方式/Sort type
  - `note_type`: 笔记类型/Note type: 不限, 视频笔记, 普通笔记, 直播笔记
  - `time_filter`: 发布时间筛选/Time filter: 不限, 一天内, 一周内, 半年内
  - `search_id`: 搜索ID，翻页时传入首次搜索返回的值/Search ID for pagination
  - `search_session_id`: 搜索会话ID，翻页时传入首次搜索返回的值/Search session ID for pagination
  - `source`: 来源/Source
  - `ai_mode`: AI模式：0=关闭, 1=开启/AI mode: 0=off, 1=on

### `GET /api/v1/xiaohongshu/app_v2/search_users`
**搜索用户/Search users**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `page`: 页码，从1开始/Page number, start from 1
  - `search_id`: 搜索ID，翻页时传入首次搜索返回的值/Search ID for pagination
  - `source`: 来源/Source

### `GET /api/v1/xiaohongshu/app_v2/search_images`
**搜索图片/Search images**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `page`: 页码，从1开始/Page number, start from 1
  - `search_id`: 搜索ID，翻页时传入首次搜索返回的值/Search ID for pagination
  - `search_session_id`: 搜索会话ID，翻页时传入首次搜索返回的值/Search session ID for pagination
  - `word_request_id`: 词请求ID，翻页时传入首次搜索返回的值/Word request ID for pagination
  - `source`: 来源/Source

### `GET /api/v1/xiaohongshu/app_v2/search_products`
**搜索商品/Search products**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `page`: 页码，从1开始/Page number, start from 1
  - `search_id`: 搜索ID，翻页时传入首次搜索返回的值/Search ID for pagination
  - `source`: 来源/Source

### `GET /api/v1/xiaohongshu/app_v2/search_groups`
**搜索群聊/Search groups**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `page_no`: 页码，从0开始/Page number, start from 0
  - `search_id`: 搜索ID，翻页时传入首次搜索返回的值/Search ID for pagination
  - `source`: 来源/Source
  - `is_recommend`: 是否推荐：0=否, 1=是/Is recommend: 0=no, 1=yes

### `GET /api/v1/xiaohongshu/app_v2/get_product_detail`
**获取商品详情/Get product detail**

Parameters:
  - `sku_id`*: 商品SKU ID/Product SKU ID
  - `source`: 来源/Source
  - `pre_page`: 前置页面/Previous page

### `GET /api/v1/xiaohongshu/app_v2/get_product_review_overview`
**获取商品评论总览/Get product review overview**

Parameters:
  - `sku_id`*: 商品SKU ID/Product SKU ID
  - `tab`: 标签类型/Tab type

### `GET /api/v1/xiaohongshu/app_v2/get_product_reviews`
**获取商品评论列表/Get product reviews**

Parameters:
  - `sku_id`*: 商品SKU ID/Product SKU ID
  - `page`: 页码，从0开始/Page number, start from 0
  - `sort_strategy_type`: 排序策略：0=综合排序, 1=最新排序/Sort strategy: 0=general, 1=latest
  - `share_pics_only`: 仅看有图评论：0=否, 1=是/Show reviews with images only: 0=no, 1=yes
  - `from_page`: 来源页面/From page

### `GET /api/v1/xiaohongshu/app_v2/get_product_recommendations`
**获取商品推荐列表/Get product recommendations**

Parameters:
  - `sku_id`*: 商品SKU ID/Product SKU ID
  - `cursor_score`: 分页游标，首次请求留空/Pagination cursor, leave empty for first request
  - `region`: 地区/Region

### `GET /api/v1/xiaohongshu/app_v2/get_topic_info`
**获取话题详情/Get topic info**

Parameters:
  - `page_id`*: 话题页面ID/Topic page ID
  - `source`: 来源/Source
  - `note_id`: 来源笔记ID，从笔记跳转到话题时传入/Source note ID, pass when jumping from no

### `GET /api/v1/xiaohongshu/app_v2/get_topic_feed`
**获取话题笔记列表/Get topic feed**

Parameters:
  - `page_id`*: 话题页面ID/Topic page ID
  - `sort`: 排序方式/Sort: trend(最热), time(最新)
  - `cursor_score`: 分页游标分数，翻页时传入/Pagination cursor score for next page
  - `last_note_id`: 上一页最后一条笔记ID，翻页时传入/Last note ID from previous page
  - `last_note_ct`: 上一页最后一条笔记创建时间，翻页时传入/Last note create time from previous page
  - `session_id`: 会话ID，翻页时保持一致/Session ID, keep consistent for pagination
  - `first_load_time`: 首次加载时间戳，翻页时保持一致/First load timestamp, keep consistent for pa
  - `source`: 来源/Source

### `GET /api/v1/xiaohongshu/app_v2/get_creator_inspiration_feed`
**获取创作者推荐灵感列表/Get creator inspiration feed**

Parameters:
  - `cursor`: 分页游标，首次请求留空/Pagination cursor, leave empty for first request
  - `tab`: 标签类型/Tab type
  - `source`: 来源/Source

### `GET /api/v1/xiaohongshu/app_v2/get_creator_hot_inspiration_feed`
**获取创作者热点灵感列表/Get creator hot inspiration feed**

Parameters:
  - `cursor`: 分页游标，首次请求留空/Pagination cursor, leave empty for first request


## /api/v1/xiaohongshu/app

### `GET /api/v1/xiaohongshu/app/get_note_info`
**获取笔记信息 V1/Get note info V1**

Parameters:
  - `note_id`: 笔记ID/Note ID
  - `share_text`: 分享链接/Share link

### `GET /api/v1/xiaohongshu/app/get_note_info_v2`
**获取笔记信息 V2 (蒲公英商家后台)/Get note info V2 (Pugongying Business Backend)**

Parameters:
  - `note_id`: 笔记ID/Note ID
  - `share_text`: 分享链接/Share link

### `GET /api/v1/xiaohongshu/app/get_note_comments`
**获取笔记评论/Get note comments**

Parameters:
  - `note_id`*: 笔记ID/Note ID
  - `start`: 翻页游标/Pagination cursor
  - `sort_strategy`: 排序策略：1-默认排序，2-最新评论/Sort strategy: 1-default, 2-latest

### `GET /api/v1/xiaohongshu/app/get_sub_comments`
**获取子评论/Get sub comments**

Parameters:
  - `note_id`*: 笔记ID/Note ID
  - `comment_id`*: 一级评论ID/Parent comment ID
  - `start`: 翻页游标/Pagination cursor

### `GET /api/v1/xiaohongshu/app/get_notes_by_topic`
**[已弃用/Deprecated] 根据话题标签获取作品/Get notes by topic**

Parameters:
  - `page_id`*: 话题标签ID/Topic tag ID
  - `first_load_time`*: 首次请求时间戳（毫秒）/First load timestamp (ms)
  - `sort`: 排序方式：hot-综合，time-最新，trend-最热/Sort: hot-comprehensive, time-l
  - `session_id`: 会话ID/Session ID
  - `last_note_ct`: 最后一条笔记创建时间/Last note create time
  - `last_note_id`: 最后一条笔记ID/Last note ID
  - `cursor_score`: 游标分数/Cursor score

### `GET /api/v1/xiaohongshu/app/search_notes`
**搜索笔记/Search notes**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `page`*: 页码（从1开始）/Page number (start from 1)
  - `search_id`: 搜索ID，翻页时使用/Search ID for pagination
  - `session_id`: 会话ID，翻页时使用/Session ID for pagination
  - `sort_type`: 排序方式/Sort type
  - `filter_note_type`: 笔记类型筛选：不限、视频笔记、普通笔记/Note type filter
  - `filter_note_time`: 发布时间筛选：不限、一天内、一周内、半年内/Time filter

### `GET /api/v1/xiaohongshu/app/get_user_info`
**获取用户信息/Get user info**

Parameters:
  - `user_id`*: 用户ID/User ID

### `GET /api/v1/xiaohongshu/app/get_user_notes`
**获取用户作品列表/Get user notes**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `cursor`: 翻页游标/Pagination cursor

### `GET /api/v1/xiaohongshu/app/extract_share_info`
**提取分享链接信息/Extract share link info**

Parameters:
  - `share_link`*: 分享链接/Share link

### `GET /api/v1/xiaohongshu/app/get_user_id_and_xsec_token`
**从分享链接中提取用户ID和xsec_token/Extract user ID and xsec_token from share link**

Parameters:
  - `share_link`*: 用户分享链接/User share link

### `GET /api/v1/xiaohongshu/app/get_product_detail`
**获取商品详情/Get product detail**

Parameters:
  - `sku_id`*: 商品skuId/Product SKU ID

### `GET /api/v1/xiaohongshu/app/search_products`
**搜索商品/Search products**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `page`*: 页码（从1开始）/Page number (start from 1)
  - `search_id`: 搜索ID，翻页时使用/Search ID for pagination
  - `session_id`: 会话ID，翻页时使用/Session ID for pagination
  - `sort`: 排序规则：sales_qty-销量、price_asc-价格升序、price_desc-价格降序/Sort: sales
  - `scope`: 搜索范围：purchased-买过的店、following-关注的店/Scope: purchased, followi
  - `service_guarantee`: 物流权益，多选用英文逗号分割/Service guarantee, comma separated
  - `min_price`: 最低价/Min price
  - `max_price`: 最高价/Max price
  - `super_promotion`: 标签ID/Promotion tag ID


## /api/v1/xiaohongshu/web_v2

### `GET /api/v1/xiaohongshu/web_v2/fetch_feed_notes`
**获取单一笔记和推荐笔记 V1 (已弃用)/Fetch one note and feed notes V1 (deprecated)**

Parameters:
  - `note_id`*: 笔记ID/Note ID

### `GET /api/v1/xiaohongshu/web_v2/fetch_feed_notes_v2`
**获取单一笔记和推荐笔记 V2/Fetch one note and feed notes V2(v2稳定, 推荐使用此接口)**

Parameters:
  - `note_id`*: 笔记ID/Note ID

### `GET /api/v1/xiaohongshu/web_v2/fetch_feed_notes_v3`
**获取单一笔记和推荐笔记 V3/Fetch one note and feed notes V3(通过短链获取笔记详情)**

Parameters:
  - `short_url`*: 短链/Short URL

### `GET /api/v1/xiaohongshu/web_v2/fetch_feed_notes_v4`
**获取单一笔记和推荐笔记 V4 (互动量有延迟)/Fetch one note and feed notes V4 (interaction volume has a delay)**

Parameters:
  - `note_id`*: 笔记ID/Note ID

### `GET /api/v1/xiaohongshu/web_v2/fetch_feed_notes_v5`
**获取单一笔记和推荐笔记 V5 (互动量有缺失)/Fetch one note and feed notes V5 (interaction volume has a missing)**

Parameters:
  - `note_id`*: 笔记ID/Note ID

### `GET /api/v1/xiaohongshu/web_v2/fetch_note_image`
**获取小红书笔记图片/Fetch Xiaohongshu note image**

Parameters:
  - `note_id`*: 笔记ID/Note ID

### `GET /api/v1/xiaohongshu/web_v2/fetch_search_notes`
**获取搜索笔记/Fetch search notes**

Parameters:
  - `keywords`*: 搜索关键词/Search keywords
  - `page`: 页码/Page number
  - `sort_type`: 排序方式/Sort type
  - `note_type`: 笔记类型/Note type

### `GET /api/v1/xiaohongshu/web_v2/fetch_search_users`
**获取搜索用户/Fetch search users**

Parameters:
  - `keywords`*: 搜索关键词/Search keywords
  - `page`: 页码/Page number

### `GET /api/v1/xiaohongshu/web_v2/fetch_home_notes`
**获取Web用户主页笔记/Fetch web user profile notes**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `cursor`: 游标/Cursor

### `GET /api/v1/xiaohongshu/web_v2/fetch_home_notes_app`
**获取App用户主页笔记/Fetch App user home notes**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `cursor`: 游标/Cursor

### `GET /api/v1/xiaohongshu/web_v2/fetch_note_comments`
**获取笔记评论/Fetch note comments**

Parameters:
  - `note_id`*: 笔记ID/Note ID
  - `cursor`: 游标/Cursor

### `GET /api/v1/xiaohongshu/web_v2/fetch_sub_comments`
**获取子评论/Fetch sub comments**

Parameters:
  - `note_id`*: 笔记ID/Note ID
  - `comment_id`*: 评论ID/Comment ID
  - `cursor`: 游标/Cursor

### `GET /api/v1/xiaohongshu/web_v2/fetch_user_info`
**获取用户信息/Fetch user info**

Parameters:
  - `user_id`*: 用户ID/User ID

### `GET /api/v1/xiaohongshu/web_v2/fetch_user_info_app`
**获取App用户信息/Fetch App user info**

Parameters:
  - `user_id`*: 用户ID/User ID

### `GET /api/v1/xiaohongshu/web_v2/fetch_follower_list`
**获取用户粉丝列表/Fetch follower list**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `cursor`: 游标/Cursor

### `GET /api/v1/xiaohongshu/web_v2/fetch_following_list`
**获取用户关注列表/Fetch following list**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `cursor`: 游标/Cursor

### `GET /api/v1/xiaohongshu/web_v2/fetch_product_list`
**获取小红书商品列表/Fetch Xiaohongshu product list**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `page`: 页码/Page number

### `GET /api/v1/xiaohongshu/web_v2/fetch_hot_list`
**获取小红书热榜/Fetch Xiaohongshu hot list**


## /api/v1/xiaohongshu/web

### `POST /api/v1/xiaohongshu/web/get_home_recommend`
**获取首页推荐/Get home recommend**

### `GET /api/v1/xiaohongshu/web/get_note_info_v2`
**获取笔记信息 V2/Get note info V2**

Parameters:
  - `note_id`: 笔记ID/Note ID
  - `share_text`: 分享链接/Share link

### `GET /api/v1/xiaohongshu/web/get_note_info_v4`
**获取笔记信息 V4/Get note info V4**

Parameters:
  - `note_id`: 笔记ID/Note ID
  - `share_text`: 分享链接/Share link

### `POST /api/v1/xiaohongshu/web/get_note_info_v5`
**获取笔记信息 V5 (自带Cookie)/Get note info V5 (Self-provided Cookie)**

### `GET /api/v1/xiaohongshu/web/get_note_info_v7`
**获取笔记信息 V7/Get note info V7**

Parameters:
  - `note_id`: 笔记ID/Note ID
  - `share_text`: 分享链接/Share link

### `GET /api/v1/xiaohongshu/web/get_note_comments`
**获取笔记评论 V1/Get note comments V1**

Parameters:
  - `note_id`*: 笔记ID/Note ID
  - `lastCursor`: 上一页的游标/Last cursor

### `GET /api/v1/xiaohongshu/web/get_note_comment_replies`
**获取笔记评论回复 V1/Get note comment replies V1**

Parameters:
  - `note_id`*: 笔记ID/Note ID
  - `comment_id`*: 评论ID/Comment ID
  - `lastCursor`: 上一页的游标/Last cursor

### `GET /api/v1/xiaohongshu/web/get_user_info`
**获取用户信息 V1/Get user info V1**

Parameters:
  - `user_id`*: 用户ID/User ID

### `GET /api/v1/xiaohongshu/web/get_user_info_v2`
**获取用户信息 V2/Get user info V2**

Parameters:
  - `user_id`: 用户ID/User ID
  - `share_text`: 分享文本或链接/Share text or link

### `GET /api/v1/xiaohongshu/web/search_notes`
**搜索笔记/Search notes**

Parameters:
  - `keyword`*: 搜索关键词/Keyword
  - `page`: 页码/Page
  - `sort`: 排序方式/Sort
  - `noteType`: 笔记类型/Note type
  - `noteTime`: 发布时间/Release time

### `GET /api/v1/xiaohongshu/web/search_notes_v3`
**搜索笔记 V3/Search notes V3**

Parameters:
  - `keyword`*: 搜索关键词/Keyword
  - `page`: 页码/Page
  - `sort`: 排序方式/Sort
  - `noteType`: 笔记类型/Note type
  - `noteTime`: 发布时间/Release time

### `GET /api/v1/xiaohongshu/web/search_users`
**搜索用户/Search users**

Parameters:
  - `keyword`*: 搜索关键词/Keyword
  - `page`: 页码/Page

### `GET /api/v1/xiaohongshu/web/get_user_notes_v2`
**获取用户的笔记 V2/Get user notes V2**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `lastCursor`: 上一页的游标/Last cursor

### `GET /api/v1/xiaohongshu/web/get_visitor_cookie`
**获取游客Cookie/Get visitor cookie**

Parameters:
  - `proxy`: 代理/Proxy

### `POST /api/v1/xiaohongshu/web/sign`
**小红书Web签名/Xiaohongshu Web sign**

### `GET /api/v1/xiaohongshu/web/get_note_id_and_xsec_token`
**通过分享链接获取小红书的Note ID 和 xsec_token/Get Xiaohongshu Note ID and xsec_token by share link**

Parameters:
  - `share_text`*: 分享链接/Share link

### `GET /api/v1/xiaohongshu/web/get_product_info`
**获取小红书商品信息/Get Xiaohongshu product info**

Parameters:
  - `share_text`: 分享链接/Share link
  - `item_id`: 商品ID/Item ID
  - `xsec_token`: X-Sec-Token
