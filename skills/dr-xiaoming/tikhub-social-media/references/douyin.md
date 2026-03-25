# Douyin API Reference

Total endpoints: 247


## /api/v1/douyin/web

### `GET /api/v1/douyin/web/fetch_one_video`
**获取单个作品数据/Get single video data**

Parameters:
  - `aweme_id`*: 作品id/Video id
  - `need_anchor_info`: 是否需要锚点信息/Whether anchor information is needed

### `GET /api/v1/douyin/web/fetch_one_video_v2`
**获取单个作品数据 V2/Get single video data V2**

Parameters:
  - `aweme_id`*: 作品id/Video id

### `GET /api/v1/douyin/web/fetch_one_video_by_share_url`
**根据分享链接获取单个作品数据/Get single video data by sharing link**

Parameters:
  - `share_url`*: 分享链接/Share link

### `GET /api/v1/douyin/web/fetch_video_high_quality_play_url`
**获取视频的最高画质播放链接/Get the highest quality play URL of the video**

Parameters:
  - `aweme_id`: 作品id/Video id
  - `share_url`: 可选，分享链接/Optional, share link

### `POST /api/v1/douyin/web/fetch_multi_video_high_quality_play_url`
**批量获取视频的最高画质播放链接/Batch get the highest quality play URL of videos**

### `POST /api/v1/douyin/web/fetch_multi_video`
**批量获取视频信息/Batch Get Video Information**

### `GET /api/v1/douyin/web/fetch_one_video_danmaku`
**获取单个作品视频弹幕数据/Get single video danmaku data**

Parameters:
  - `item_id`*: 作品id/Video id
  - `duration`*: 视频总时长/Video total duration
  - `end_time`*: 结束时间/End time
  - `start_time`*: 开始时间/Start time

### `GET /api/v1/douyin/web/fetch_home_feed`
**获取首页推荐数据/Get home feed data**

Parameters:
  - `count`: 数量/Number
  - `refresh_index`: 翻页索引/Paging index

### `GET /api/v1/douyin/web/fetch_related_posts`
**获取相关作品推荐数据/Get related posts recommendation data**

Parameters:
  - `aweme_id`*: 作品id/Video id
  - `refresh_index`: 翻页索引/Paging index
  - `count`: 数量/Number

### `GET /api/v1/douyin/web/fetch_user_post_videos`
**获取用户主页作品数据/Get user homepage video data**

Parameters:
  - `sec_user_id`*: 用户sec_user_id/User sec_user_id
  - `max_cursor`: 最大游标/Maximum cursor
  - `count`: 每页数量/Number per page
  - `filter_type`: 过滤类型/Filter type
  - `cookie`: 用户网页版抖音Cookie/Your web version of Douyin Cookie

### `POST /api/v1/douyin/web/fetch_user_like_videos`
**获取用户喜欢作品数据/Get user like video data**

### `POST /api/v1/douyin/web/fetch_user_collection_videos`
**获取用户收藏作品数据/Get user collection video data**

### `POST /api/v1/douyin/web/fetch_user_collects`
**获取用户收藏夹/Get user collection**

### `GET /api/v1/douyin/web/fetch_user_collects_videos`
**获取用户收藏夹数据/Get user collection data**

Parameters:
  - `collects_id`*: 收藏夹id/Collection id
  - `max_cursor`: 最大游标/Maximum cursor
  - `counts`: 每页数量/Number per page

### `GET /api/v1/douyin/web/fetch_user_mix_videos`
**获取用户合辑作品数据/Get user mix video data**

Parameters:
  - `mix_id`*: 合辑id/Mix id
  - `max_cursor`: 最大游标/Maximum cursor
  - `counts`: 每页数量/Number per page

### `GET /api/v1/douyin/web/fetch_user_live_videos`
**获取用户直播流数据/Get user live video data**

Parameters:
  - `webcast_id`*: 直播间webcast_id/Room webcast_id

### `GET /api/v1/douyin/web/fetch_user_live_videos_by_sec_uid`
**通过sec_uid获取指定用户的直播流数据/Get live video data of specified user by sec_uid**

Parameters:
  - `sec_uid`*: 用户sec_uid/User sec_uid

### `GET /api/v1/douyin/web/fetch_user_live_videos_by_room_id`
**通过room_id获取指定用户的直播流数据 V1/Get live video data of specified user by room_id V1**

Parameters:
  - `room_id`*: 直播间room_id/Room room_id

### `GET /api/v1/douyin/web/fetch_user_live_videos_by_room_id_v2`
**通过room_id获取指定用户的直播流数据 V2/Gets the live stream data of the specified user by room_id V2**

Parameters:
  - `room_id`*: 直播间room_id/Room room_id

### `GET /api/v1/douyin/web/fetch_live_gift_ranking`
**获取直播间送礼用户排行榜/Get live room gift user ranking**

Parameters:
  - `room_id`*: 直播间room_id/Room room_id
  - `rank_type`: 排行类型/Leaderboard type

### `GET /api/v1/douyin/web/fetch_live_room_product_result`
**抖音直播间商品信息/Douyin live room product information**

Parameters:
  - `room_id`*: 直播间room_id/Room room_id
  - `author_id`*: 作者id/Author id
  - `offset`: 偏移量/Offset
  - `limit`: 数量/Number

### `GET /api/v1/douyin/web/fetch_product_detail`
**获取商品详情/Get product detail**

Parameters:
  - `product_id`*: 商品ID/Product ID
  - `aweme_id`: 作品ID（可选）/Video ID (optional)
  - `room_id`: 直播间ID（可选）/Room ID (optional)
  - `sec_user_id`: 用户sec_user_id（可选）/User sec_user_id (optional)

### `GET /api/v1/douyin/web/fetch_product_sku_list`
**获取商品SKU列表/Get product SKU list**

Parameters:
  - `product_id`*: 商品ID/Product ID
  - `author_id`*: 作者ID/Author ID

### `GET /api/v1/douyin/web/fetch_product_coupon`
**获取商品优惠券信息/Get product coupon information**

Parameters:
  - `product_id`*: 商品ID/Product ID
  - `shop_id`*: 店铺ID/Shop ID
  - `price`*: 价格/Price
  - `author_id`*: 作者ID/Author ID
  - `sec_user_id`*: 作者ID/Secure Author ID

### `GET /api/v1/douyin/web/fetch_product_review_score`
**获取商品评价评分/Get product review score**

Parameters:
  - `product_id`*: 商品ID/Product ID
  - `shop_id`*: 店铺ID/Shop ID

### `GET /api/v1/douyin/web/fetch_product_review_list`
**获取商品评价列表/Get product review list**

Parameters:
  - `product_id`*: 商品ID/Product ID
  - `shop_id`*: 店铺ID/Shop ID
  - `cursor`: 游标/Cursor
  - `count`: 数量/Count
  - `sort_type`: 排序类型 (0: 默认排序, 1: 最新排序)/Sort Type (0: Default, 1: Latest)

### `GET /api/v1/douyin/web/fetch_user_profile_by_uid`
**使用UID获取用户信息/Get user information by UID**

Parameters:
  - `uid`*: 用户UID/User UID

### `GET /api/v1/douyin/web/fetch_batch_user_profile_v1`
**获取批量用户信息(最多10个)/Get batch user profile (up to 10)**

Parameters:
  - `sec_user_ids`*: 用户sec_user_id列表，用逗号分隔/User sec_user_id list, separated by co

### `GET /api/v1/douyin/web/fetch_batch_user_profile_v2`
**获取批量用户信息(最多50个)/Get batch user profile (up to 50)**

Parameters:
  - `sec_user_ids`*: 用户sec_user_id列表，用逗号分隔/User sec_user_id list, separated by co

### `GET /api/v1/douyin/web/fetch_user_live_info_by_uid`
**使用UID获取用户开播信息/Get user live information by UID**

Parameters:
  - `uid`*: 用户UID/User UID

### `GET /api/v1/douyin/web/fetch_user_profile_by_short_id`
**使用Short ID获取用户信息/Get user information by Short ID**

Parameters:
  - `short_id`*: 用户Short ID/User Short ID

### `GET /api/v1/douyin/web/handler_shorten_url`
**生成短链接**

Parameters:
  - `target_url`*: 待转换的短链接/Target URL to be converted

### `GET /api/v1/douyin/web/handler_user_profile`
**使用sec_user_id获取指定用户的信息/Get information of specified user by sec_user_id**

Parameters:
  - `sec_user_id`*: 用户sec_user_id/User sec_user_id

### `GET /api/v1/douyin/web/handler_user_profile_v2`
**使用unique_id（抖音号）获取指定用户的信息/Get information of specified user by unique_id**

Parameters:
  - `unique_id`*: 用户unique_id/User unique_id

### `GET /api/v1/douyin/web/encrypt_uid_to_sec_user_id`
**加密用户uid到sec_user_id/Encrypt user uid to sec_user_id**

Parameters:
  - `uid`*: 用户uid(short_id)/User uid(short_id)

### `GET /api/v1/douyin/web/handler_user_profile_v3`
**根据抖音uid获取指定用户的信息/Get information of specified user by uid**

Parameters:
  - `uid`*: 用户uid(short_id)/User uid(short_id)

### `GET /api/v1/douyin/web/handler_user_profile_v4`
**根据sec_user_id获取指定用户的信息（性别，年龄，直播等级、牌子）/Get information of specified user by sec_user_id (gender, age, live level、brand)**

Parameters:
  - `sec_user_id`*: 用户sec_user_id/User sec_user_id

### `GET /api/v1/douyin/web/fetch_user_fans_list`
**获取用户粉丝列表/Get user fans list**

Parameters:
  - `sec_user_id`: 用户sec_user_id/User sec_user_id
  - `max_time`: 最大时间戳/Maximum timestamp
  - `count`: 数量/Number
  - `source_type`: 来源类型/Source type

### `GET /api/v1/douyin/web/fetch_user_following_list`
**获取用户关注列表/Get user following list**

Parameters:
  - `sec_user_id`: 用户sec_user_id/User sec_user_id
  - `max_time`: 最大时间戳/Maximum timestamp
  - `count`: 数量/Number
  - `source_type`: 来源类型/Source type

### `GET /api/v1/douyin/web/fetch_video_comments`
**获取单个视频评论数据/Get single video comments data**

Parameters:
  - `aweme_id`*: 作品id/Video id
  - `cursor`: 游标/Cursor
  - `count`: 数量/Number

### `GET /api/v1/douyin/web/fetch_video_comment_replies`
**获取指定视频的评论回复数据/Get comment replies data of specified video**

Parameters:
  - `item_id`*: 作品id/Video id
  - `comment_id`*: 评论id/Comment id
  - `cursor`: 游标/Cursor
  - `count`: 数量/Number

### `GET /api/v1/douyin/web/fetch_general_search_result`
**[已弃用/Deprecated] 获取指定关键词的综合搜索结果/Get comprehensive search results of specified keywords**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number
  - `sort_type`: 排序类型/Sort type
  - `publish_time`: 发布时间/Publish time
  - `filter_duration`: 视频时长/Duration filter
  - `search_range`: 搜索范围/Search range
  - `content_type`: 内容类型/Content type
  - `search_id`: 搜索id，翻页时需要提供/Search id, need to provide when paging

### `GET /api/v1/douyin/web/fetch_video_search_result`
**[已弃用/Deprecated] 获取指定关键词的视频搜索结果/Get video search results of specified keywords**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number
  - `sort_type`: 排序类型/Sort type
  - `publish_time`: 发布时间/Publish time
  - `filter_duration`: 视频时长/Duration filter
  - `search_id`: 搜索id，翻页时需要提供/Search id, need to provide when paging

### `GET /api/v1/douyin/web/fetch_video_search_result_v2`
**获取指定关键词的视频搜索结果 V2 （废弃，替代接口请参考下方文档）/Get video search results of specified keywords V2 (Deprecated, please refer to the following document for replacement interface)**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `sort_type`: 排序类型/Sort type
  - `publish_time`: 发布时间/Publish time
  - `filter_duration`: 视频时长/Duration filter
  - `page`: 页码/Page
  - `search_id`: 搜索id，翻页时需要提供/Search id, need to provide when paging

### `GET /api/v1/douyin/web/fetch_user_search_result`
**获取指定关键词的用户搜索结果(废弃，替代接口请参考下方文档)/Get user search results of specified keywords (deprecated, please refer to the following document for replacement interface)**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number
  - `douyin_user_fans`: 粉丝数/Fans
  - `douyin_user_type`: 用户类型/User type
  - `search_id`: 搜索id，翻页时需要提供/Search id, need to provide when paging

### `GET /api/v1/douyin/web/fetch_user_search_result_v2`
**获取指定关键词的用户搜索结果 V2 (已弃用，替代接口请参考下方文档)/Get user search results of specified keywords V2 (deprecated, please refer to the following document for replacement interface)**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `cursor`: 游标/Cursor

### `GET /api/v1/douyin/web/fetch_user_search_result_v3`
**获取指定关键词的用户搜索结果 V3 (已弃用，替代接口请参考下方文档)/Get user search results of specified keywords V3 (deprecated, please refer to the following document for replacement interface)**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `cursor`: 游标/Cursor
  - `douyin_user_type`: 用户类型/User type
  - `douyin_user_fans`: 粉丝数/Fans

### `GET /api/v1/douyin/web/fetch_live_search_result`
**[已弃用/Deprecated] 获取指定关键词的直播搜索结果/Get live search results of specified keywords**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number
  - `search_id`: 搜索id，翻页时需要提供/Search id, need to provide when paging

### `POST /api/v1/douyin/web/fetch_search_challenge`
**[已弃用/Deprecated] 搜索话题/Search Challenge**

### `POST /api/v1/douyin/web/fetch_challenge_posts`
**话题作品/Challenge Posts**

### `GET /api/v1/douyin/web/fetch_hot_search_result`
**获取抖音热榜数据/Get Douyin hot search results**

### `GET /api/v1/douyin/web/fetch_video_channel_result`
**抖音视频频道数据/Douyin video channel data**

Parameters:
  - `tag_id`*: 标签id/Tag id
  - `count`: 数量/Number
  - `refresh_index`: 刷新索引/Refresh index

### `GET /api/v1/douyin/web/fetch_douyin_web_guest_cookie`
**获取抖音Web的游客Cookie/Get the guest Cookie of Douyin Web**

Parameters:
  - `user_agent`*: 用户浏览器代理/User browser agent

### `GET /api/v1/douyin/web/generate_real_msToken`
**生成真实msToken/Generate real msToken**

### `GET /api/v1/douyin/web/generate_ttwid`
**生成ttwid/Generate ttwid**

Parameters:
  - `user_agent`: 

### `POST /api/v1/douyin/web/fetch_query_user`
**查询抖音用户基本信息/Query Douyin user basic information**

### `GET /api/v1/douyin/web/generate_verify_fp`
**生成verify_fp/Generate verify_fp**

### `GET /api/v1/douyin/web/generate_s_v_web_id`
**生成s_v_web_id/Generate s_v_web_id**

### `GET /api/v1/douyin/web/generate_wss_xb_signature`
**生成弹幕xb签名/Generate barrage xb signature**

Parameters:
  - `user_agent`*: 用户浏览器代理/User browser agent
  - `room_id`*: 房间号/Room ID
  - `user_unique_id`*: 用户唯一ID/User unique ID

### `POST /api/v1/douyin/web/generate_x_bogus`
**使用接口网址生成X-Bogus参数/Generate X-Bogus parameter using API URL**

### `POST /api/v1/douyin/web/generate_a_bogus`
**使用接口网址生成A-Bogus参数/Generate A-Bogus parameter using API URL**

### `GET /api/v1/douyin/web/get_sec_user_id`
**提取单个用户id/Extract single user id**

Parameters:
  - `url`*: 

### `POST /api/v1/douyin/web/get_all_sec_user_id`
**提取列表用户id/Extract list user id**

### `GET /api/v1/douyin/web/get_aweme_id`
**提取单个作品id/Extract single video id**

Parameters:
  - `url`*: 

### `POST /api/v1/douyin/web/get_all_aweme_id`
**提取列表作品id/Extract list video id**

### `GET /api/v1/douyin/web/get_webcast_id`
**提取直播间号/Extract webcast id**

Parameters:
  - `url`*: 

### `POST /api/v1/douyin/web/get_all_webcast_id`
**提取列表直播间号/Extract list webcast id**

### `GET /api/v1/douyin/web/webcast_id_2_room_id`
**直播间号转房间号/Webcast id to room id**

Parameters:
  - `webcast_id`*: 直播间号/Webcast id

### `GET /api/v1/douyin/web/douyin_live_room`
**提取直播间弹幕/Extract live room danmaku**

Parameters:
  - `live_room_url`*: 直播间链接/Live room link
  - `danmaku_type`*: 消息类型/Message type

### `GET /api/v1/douyin/web/fetch_live_im_fetch`
**抖音直播间弹幕参数获取/Douyin live room danmaku parameters**

Parameters:
  - `room_id`*: 直播间号/Live room id
  - `user_unique_id`*: 用户唯一ID/User unique ID

### `GET /api/v1/douyin/web/fetch_series_aweme`
**短剧作品/Series Video**

Parameters:
  - `offset`*: 页码/Page number
  - `count`*: 每页数量/Number per page
  - `content_type`*: 短剧类型/Subtype
  - `cookie`: 用户自行提供的Cookie/User provided Cookie

### `GET /api/v1/douyin/web/fetch_knowledge_aweme`
**知识作品推荐/Knowledge Video**

Parameters:
  - `count`*: 每页数量/Number per page
  - `refresh_index`: 翻页索引/Paging index
  - `cookie`: 用户自行提供的Cookie/User provided Cookie

### `GET /api/v1/douyin/web/fetch_game_aweme`
**游戏作品推荐/Game Video**

Parameters:
  - `count`*: 每页数量/Number per page
  - `refresh_index`: 翻页索引/Paging index
  - `cookie`: 用户自行提供的Cookie/User provided Cookie

### `GET /api/v1/douyin/web/fetch_cartoon_aweme`
**二次元作品推荐/Anime Video**

Parameters:
  - `count`*: 每页数量/Number per page
  - `refresh_index`: 翻页索引/Paging index
  - `cookie`: 用户自行提供的Cookie/User provided Cookie

### `GET /api/v1/douyin/web/fetch_music_aweme`
**音乐作品推荐/Music Video**

Parameters:
  - `count`*: 每页数量/Number per page
  - `refresh_index`: 翻页索引/Paging index
  - `cookie`: 用户自行提供的Cookie/User provided Cookie

### `GET /api/v1/douyin/web/fetch_food_aweme`
**美食作品推荐/Food Video**

Parameters:
  - `count`*: 每页数量/Number per page
  - `refresh_index`: 翻页索引/Paging index
  - `cookie`: 用户自行提供的Cookie/User provided Cookie


## /api/v1/douyin/app

### `GET /api/v1/douyin/app/v3/fetch_one_video`
**获取单个作品数据/Get single video data**

Parameters:
  - `aweme_id`*: 作品id/Video id

### `GET /api/v1/douyin/app/v3/fetch_one_video_v2`
**获取单个作品数据 V2/Get single video data V2**

Parameters:
  - `aweme_id`*: 作品id/Video id

### `GET /api/v1/douyin/app/v3/fetch_one_video_v3`
**获取单个作品数据 V3 (无版权限制)/Get single video data V3 (No copyright restrictions)**

Parameters:
  - `aweme_id`*: 作品或文章ID/Video or Article ID

### `GET /api/v1/douyin/app/v3/fetch_share_info_by_share_code`
**根据分享口令获取分享信息/Get share info by share code**

Parameters:
  - `share_code`*: 分享口令/Share code

### `POST /api/v1/douyin/app/v3/fetch_multi_video`
**批量获取视频信息 V1/Batch Get Video Information V1**

### `POST /api/v1/douyin/app/v3/fetch_multi_video_v2`
**批量获取视频信息 V2/Batch Get Video Information V2**

### `GET /api/v1/douyin/app/v3/fetch_one_video_by_share_url`
**根据分享链接获取单个作品数据/Get single video data by sharing link**

Parameters:
  - `share_url`*: 分享链接/Share link

### `GET /api/v1/douyin/app/v3/fetch_video_high_quality_play_url`
**获取视频的最高画质播放链接/Get the highest quality play URL of the video**

Parameters:
  - `aweme_id`: 作品id/Video id
  - `share_url`: 可选，分享链接/Optional, share link

### `POST /api/v1/douyin/app/v3/fetch_multi_video_high_quality_play_url`
**批量获取视频的最高画质播放链接/Batch get the highest quality play URL of videos**

### `GET /api/v1/douyin/app/v3/fetch_video_statistics`
**根据视频ID获取作品的统计数据（点赞数、下载数、播放数、分享数）/Get the statistical data of the Post according to the video ID (like count, download count, play count, share count)**

Parameters:
  - `aweme_ids`*: 作品id/Video id

### `GET /api/v1/douyin/app/v3/fetch_multi_video_statistics`
**根据视频ID批量获取作品的统计数据（点赞数、下载数、播放数、分享数）/Get the statistical data of the Post according to the video ID (like count, download count, play count, share count)**

Parameters:
  - `aweme_ids`*: 作品id/Video id

### `GET /api/v1/douyin/app/v3/add_video_play_count`
**根据视频ID来增加作品的播放数/Increase the number of plays of the work according to the video ID**

Parameters:
  - `aweme_type`*: 作品类型/Video type
  - `item_id`*: 作品id/Video id
  - `cookie`: 可选，默认使用游客Cookie/Optional, use guest Cookie by default

### `GET /api/v1/douyin/app/v3/handler_user_profile`
**获取指定用户的信息/Get information of specified user**

Parameters:
  - `sec_user_id`*: 用户sec_user_id/User sec_user_id

### `GET /api/v1/douyin/app/v3/fetch_user_fans_list`
**获取用户粉丝列表/Get user fans list**

Parameters:
  - `sec_user_id`: 用户sec_user_id/User sec_user_id
  - `max_time`: 最大时间戳/Maximum timestamp
  - `count`: 数量/Number

### `GET /api/v1/douyin/app/v3/fetch_user_following_list`
**获取用户关注列表 (弃用，使用 /api/v1/douyin/web/fetch_user_following_list 替代)/Get user following list (Deprecated, use /api/v1/douyin/web/fetch_user_following_list instead)**

Parameters:
  - `sec_user_id`: 用户sec_user_id/User sec_user_id
  - `max_time`: 最大时间戳/Maximum timestamp
  - `count`: 数量/Number

### `GET /api/v1/douyin/app/v3/fetch_user_post_videos`
**获取用户主页作品数据/Get user homepage video data**

Parameters:
  - `sec_user_id`*: 用户sec_user_id/User sec_user_id
  - `max_cursor`: 最大游标/Maximum cursor
  - `count`: 每页数量/Number per page
  - `sort_type`: 排序类型/Sort type

### `GET /api/v1/douyin/app/v3/fetch_user_like_videos`
**获取用户喜欢作品数据/Get user like video data**

Parameters:
  - `sec_user_id`*: 用户sec_user_id/User sec_user_id
  - `max_cursor`: 最大游标/Maximum cursor
  - `counts`: 每页数量/Number per page

### `GET /api/v1/douyin/app/v3/fetch_video_comments`
**获取单个视频评论数据/Get single video comments data**

Parameters:
  - `aweme_id`*: 作品id/Video id
  - `cursor`: 游标/Cursor
  - `count`: 数量/Number

### `GET /api/v1/douyin/app/v3/fetch_video_comment_replies`
**获取指定视频的评论回复数据/Get comment replies data of specified video**

Parameters:
  - `item_id`*: 作品id/Video id
  - `comment_id`*: 评论id/Comment id
  - `cursor`: 游标/Cursor
  - `count`: 数量/Number

### `GET /api/v1/douyin/app/v3/fetch_video_mix_detail`
**获取抖音视频合集详情数据/Get Douyin video mix detail data**

Parameters:
  - `mix_id`*: 合集id/Mix id

### `GET /api/v1/douyin/app/v3/fetch_video_mix_post_list`
**获取抖音视频合集作品列表数据/Get Douyin video mix post list data**

Parameters:
  - `mix_id`*: 合集id/Mix id
  - `cursor`: 游标/Cursor
  - `count`: 数量/Number

### `GET /api/v1/douyin/app/v3/fetch_user_series_list`
**获取用户短剧合集列表/Get user series list**

Parameters:
  - `user_id`: 用户id/User id
  - `sec_user_id`: 用户加密id/User sec id
  - `cursor`: 游标/Cursor

### `GET /api/v1/douyin/app/v3/fetch_series_video_list`
**获取短剧视频列表/Get series video list**

Parameters:
  - `series_id`*: 短剧id/Series id
  - `cursor`: 游标/Cursor

### `GET /api/v1/douyin/app/v3/fetch_series_detail`
**获取短剧详情信息/Get series detail**

Parameters:
  - `series_id`*: 短剧id/Series id

### `GET /api/v1/douyin/app/v3/fetch_general_search_result`
**获取指定关键词的综合搜索结果（弃用，替代接口见下方文档说明）/Get comprehensive search results of specified keywords (deprecated, see the documentation below for alternative interfaces)**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number
  - `sort_type`: 排序类型/Sort type
  - `publish_time`: 发布时间/Publish time
  - `filter_duration`: 时长/Duration
  - `content_type`: 内容类型/Content type

### `GET /api/v1/douyin/app/v3/fetch_video_search_result`
**获取指定关键词的视频搜索结果（弃用，替代接口见下方文档说明）/Get video search results of specified keywords (deprecated, see the documentation below for alternative interfaces)**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number
  - `sort_type`: 排序类型/Sort type
  - `publish_time`: 发布时间/Publish time
  - `filter_duration`: 时长/Duration

### `GET /api/v1/douyin/app/v3/fetch_video_search_result_v2`
**获取指定关键词的视频搜索结果 V2 （弃用，替代接口见下方文档说明）/Get video search results of specified keywords V2 (deprecated, see the documentation below for alternative interfaces)**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `sort_type`: 排序类型/Sort type
  - `publish_time`: 发布时间/Publish time
  - `filter_duration`: 视频时长/Duration filter
  - `page`: 页码/Page
  - `search_id`: 搜索id，翻页时需要提供/Search id, need to provide when paging

### `GET /api/v1/douyin/app/v3/fetch_user_search_result`
**获取指定关键词的用户搜索结果（弃用，替代接口见下方文档说明）/Get user search results of specified keywords (deprecated, see the documentation below for alternative interfaces)**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number
  - `douyin_user_fans`: 粉丝数/Fans
  - `douyin_user_type`: 用户类型/User type

### `GET /api/v1/douyin/app/v3/fetch_live_search_result`
**获取指定关键词的直播搜索结果（弃用，替代接口见下方文档说明）/Get live search results of specified keywords (deprecated, see the documentation below for alternative interfaces)**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `cursor`: 偏移量/Offset
  - `count`: 数量/Number

### `GET /api/v1/douyin/app/v3/fetch_music_search_result`
**获取指定关键词的音乐搜索结果（弃用，替代接口见下方文档说明）/Get music search results of specified keywords (deprecated, see the documentation below for alternative interfaces)**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number

### `GET /api/v1/douyin/app/v3/fetch_hashtag_search_result`
**获取指定关键词的话题搜索结果（弃用，替代接口见下方文档说明）/Get hashtag search results of specified keywords (deprecated, see the documentation below for alternative interfaces)**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number

### `GET /api/v1/douyin/app/v3/fetch_music_detail`
**获取指定音乐的详情数据/Get details of specified music**

Parameters:
  - `music_id`*: 音乐id/Music id

### `GET /api/v1/douyin/app/v3/fetch_music_video_list`
**获取指定音乐的视频列表数据/Get video list of specified music**

Parameters:
  - `music_id`*: 音乐id/Music id
  - `cursor`: 游标/Cursor
  - `count`: 数量/Number

### `GET /api/v1/douyin/app/v3/fetch_hashtag_detail`
**获取指定话题的详情数据/Get details of specified hashtag**

Parameters:
  - `ch_id`*: 话题id/Hashtag id

### `GET /api/v1/douyin/app/v3/fetch_hashtag_video_list`
**获取指定话题的作品数据/Get video list of specified hashtag**

Parameters:
  - `ch_id`*: 话题id/Hashtag id
  - `cursor`: 游标/Cursor
  - `sort_type`: 排序类型/Sort type
  - `count`: 数量/Number

### `GET /api/v1/douyin/app/v3/fetch_hot_search_list`
**获取抖音热搜榜数据/Get Douyin hot search list data**

Parameters:
  - `board_type`: 榜单类型/Board type
  - `board_sub_type`: 榜单子类型/Board sub type

### `GET /api/v1/douyin/app/v3/fetch_live_hot_search_list`
**获取抖音直播热搜榜数据/Get Douyin live hot search list data**

### `GET /api/v1/douyin/app/v3/fetch_music_hot_search_list`
**获取抖音音乐榜数据/Get Douyin music hot search list data**

Parameters:
  - `chart_type`: 榜单类型/Chart type
  - `cursor`: 游标/Cursor

### `GET /api/v1/douyin/app/v3/fetch_brand_hot_search_list`
**获取抖音品牌热榜分类数据/Get Douyin brand hot search list data**

### `GET /api/v1/douyin/app/v3/fetch_brand_hot_search_list_detail`
**获取抖音品牌热榜具体分类数据/Get Douyin brand hot search list detail data**

Parameters:
  - `category_id`*: 分类id/Category id

### `GET /api/v1/douyin/app/v3/generate_douyin_short_url`
**生成抖音短链接/Generate Douyin short link**

Parameters:
  - `url`*: 抖音链接/Douyin link

### `GET /api/v1/douyin/app/v3/generate_douyin_video_share_qrcode`
**生成抖音视频分享二维码/Generate Douyin video share QR code**

Parameters:
  - `object_id`*: 作品id/Video id

### `GET /api/v1/douyin/app/v3/register_device`
**抖音APP注册设备/Douyin APP register device**

Parameters:
  - `proxy`: 代理/Proxy

### `GET /api/v1/douyin/app/v3/open_douyin_app_to_video_detail`
**生成抖音分享链接，唤起抖音APP，跳转指定作品详情页/Generate Douyin share link, call Douyin APP, and jump to the specified video details page**

Parameters:
  - `aweme_id`*: 作品id/Video id

### `GET /api/v1/douyin/app/v3/open_douyin_app_to_user_profile`
**生成抖音分享链接，唤起抖音APP，跳转指定用户主页/Generate Douyin share link, call Douyin APP, and jump to the specified user profile**

Parameters:
  - `uid`*: 用户id/User id
  - `sec_uid`*: 用户sec_uid/User sec_uid

### `GET /api/v1/douyin/app/v3/open_douyin_app_to_keyword_search`
**生成抖音分享链接，唤起抖音APP，跳转指定关键词搜索结果/Generate Douyin share link, call Douyin APP, and jump to the specified keyword search result**

Parameters:
  - `keyword`*: 关键词/Keyword

### `GET /api/v1/douyin/app/v3/open_douyin_app_to_send_private_message`
**生成抖音分享链接，唤起抖音APP，给指定用户发送私信/Generate Douyin share link, call Douyin APP, and send private messages to specified users**

Parameters:
  - `uid`*: 用户id/User id
  - `sec_uid`*: 用户sec_uid/User sec_uid


## /api/v1/douyin/creator

### `GET /api/v1/douyin/creator/fetch_creator_activity_list`
**获取创作者活动列表/Get creator activity list**

Parameters:
  - `start_time`*: 开始时间戳/Start timestamp
  - `end_time`*: 结束时间戳/End timestamp

### `GET /api/v1/douyin/creator/fetch_creator_activity_detail`
**获取创作者活动详情/Get creator activity detail**

Parameters:
  - `activity_id`*: 活动ID/Activity ID

### `GET /api/v1/douyin/creator/fetch_creator_material_center_config`
**获取创作者中心配置/Get creator material center config**

### `GET /api/v1/douyin/creator/fetch_creator_material_center_billboard`
**获取创作者中心热门视频榜单/Get creator material center billboard**

Parameters:
  - `billboard_tag`: 榜单标签，0=全部，其他值请通过config接口获取/Billboard tag, 0=all, other value
  - `order_key`: 排序键: 1=播放最高, 2=点赞最多, 3=评论最多, 4=热度最高/Order key: 1=highest vie
  - `time_filter`: 时间筛选: 1=24小时, 2=7天, 3=30天/Time filter: 1=24 hours, 2=7 days,

### `GET /api/v1/douyin/creator/fetch_creator_hot_spot_billboard`
**获取创作者中心创作热点/Get creator hot spot billboard**

Parameters:
  - `billboard_tag`: 热点标签，多个标签用逗号分隔，如'1004,1000,1002'/Hot spot tag - multiple tag
  - `hot_search_type`: 热搜类型: 1=热点总榜, 2=同城热点榜, 3=热点上升榜/Hot search type: 1=Overall ra
  - `city_code`: 城市代码，当hot_search_type=2时必需/City code - required when hot_sea

### `GET /api/v1/douyin/creator/fetch_creator_hot_topic_billboard`
**获取创作者热门话题榜单/Get creator hot topic billboard**

Parameters:
  - `billboard_tag`: 榜单标签，0=全部，其他值请通过config接口获取/Billboard tag, 0=all, other value
  - `order_key`: 排序键: 1=播放最高, 2=点赞最多, 3=评论最多, 4=投稿最多/Order key: 1=highest vie
  - `time_filter`: 时间筛选: 1=24小时, 2=7天, 3=30天/Time filter: 1=24 hours, 2=7 days,

### `GET /api/v1/douyin/creator/fetch_creator_hot_props_billboard`
**获取创作者热门道具榜单/Get creator hot props billboard**

Parameters:
  - `billboard_tag`: 榜单标签，0=全部，其他值请通过config接口获取/Billboard tag, 0=all, other value
  - `order_key`: 排序键: 1=播放最高, 5=投稿最多, 6=展现最高, 7=收藏最高/Order key: 1=highest vie
  - `time_filter`: 时间筛选: 1=24小时, 2=7天, 3=30天/Time filter: 1=24 hours, 2=7 days,

### `GET /api/v1/douyin/creator/fetch_creator_hot_challenge_billboard`
**获取创作者热门挑战榜单/Get creator hot challenge billboard**

### `GET /api/v1/douyin/creator/fetch_creator_hot_music_billboard`
**获取创作者热门音乐榜单/Get creator hot music billboard**

Parameters:
  - `billboard_tag`: 榜单标签/Billboard tag (0=全部，具体分类值可通过配置接口获取)
  - `order_key`: 排序键/Order key (1=播放最高, 2=点赞最多, 4=热度最高, 5=投稿最多)
  - `time_filter`: 时间筛选/Time filter (1=24小时, 2=7天, 3=30天)

### `GET /api/v1/douyin/creator/fetch_creator_hot_course`
**获取创作者热门课程/Get creator hot course**

Parameters:
  - `order`: 排序方式/Order type (1=推荐排序, 2=最受欢迎, 3=最新上传)
  - `limit`: 每页数量/Items per page (建议24)
  - `offset`: 偏移量/Offset
  - `category_id`: 精选专题分类ID/Selected topic category ID - 不传则为热门课程，传入则为精选专题
    

### `GET /api/v1/douyin/creator/fetch_creator_content_category`
**获取创作者内容创作合集分类/Get creator content creation category**

### `GET /api/v1/douyin/creator/fetch_creator_content_course`
**获取创作者内容创作课程/Get creator content creation course**

Parameters:
  - `category_id`*: 分类ID/Category ID
  - `order`: 排序方式/Order type (1=推荐排序, 2=最受欢迎, 3=最新上传)
  - `limit`: 每页数量/Items per page
  - `offset`: 偏移量/Offset (starting position)

### `GET /api/v1/douyin/creator/fetch_video_danmaku_list`
**获取作品弹幕列表/Get video danmaku list**

Parameters:
  - `item_id`*: 作品ID/Video item ID
  - `count`: 每页数量/Items per page
  - `offset`: 偏移量/Offset (starting position)
  - `order_type`: 排序类型/Order type (1=时间排序, 2=其他排序)
  - `is_blocked`: 是否被屏蔽/Is blocked

### `GET /api/v1/douyin/creator/fetch_user_search`
**搜索用户/Search users**

Parameters:
  - `user_name`*: 用户名/Username (支持抖音号和抖音昵称)

### `GET /api/v1/douyin/creator/fetch_mission_task_list`
**获取商单任务列表/Get mission task list**

Parameters:
  - `cursor`: 游标/Cursor (分页)
  - `limit`: 每页数量/Items per page
  - `mission_type`: 任务类型/Mission type
  - `tab_scene`: 场景类型/Scene type (1=可投稿, 2=可报名, 3=好物测评)
  - `industry_lv1`: 一级行业/Primary industry (-1=全部)
  - `industry_lv2`: 二级行业/Secondary industry (-1=全部)
  - `platform_channel`: 平台渠道/Platform channel (1=抖音视频, 2=抖音直播, 3=抖音图文)
  - `pay_type`: 付费类型/Pay type (1=视频等级, 2=自定义, 3=按转化付费, 4=按有效播放量, 5=按销售量, 9=按
  - `greater_than_cost_progress`: 成本进度/Cost progress (20=高于20%, 50=高于50%, 80=高于80%)
  - `publish_time_start`: 发布开始时间/Publish start time (时间戳)
  - `quick_selector_scene`: 快速选择场景/Quick selector (1=高收益, 4=保底收入, 5=合作过)
  - `keyword`: 关键词/Keyword (任务名称或ID)

### `GET /api/v1/douyin/creator/fetch_industry_category_config`
**获取行业分类配置/Get industry category config**


## /api/v1/douyin/creator_v2

### `POST /api/v1/douyin/creator_v2/fetch_item_overview_data`
**获取作品总览数据/Fetch item overview data**

### `POST /api/v1/douyin/creator_v2/fetch_item_play_source`
**获取作品流量来源统计/Fetch item play source statistics**

### `POST /api/v1/douyin/creator_v2/fetch_item_search_keyword`
**获取作品搜索关键词统计/Fetch item search keywords statistics**

### `POST /api/v1/douyin/creator_v2/fetch_item_watch_trend`
**获取作品观看趋势分析/Fetch item watch trend analysis**

### `POST /api/v1/douyin/creator_v2/fetch_item_danmaku_analysis`
**获取作品弹幕分析/Fetch item bullet analysis**

### `POST /api/v1/douyin/creator_v2/fetch_item_audience_portrait`
**获取作品观众数据分析/Fetch item audience portrait**

### `POST /api/v1/douyin/creator_v2/fetch_item_audience_others`
**获取作品观众其他数据分析/Fetch item audience others analysis**

### `POST /api/v1/douyin/creator_v2/fetch_item_analysis_involved_vertical`
**获取作品垂类标签/Fetch item analysis involved vertical**

### `POST /api/v1/douyin/creator_v2/fetch_item_analysis_overview`
**获取投稿分析概览/Fetch item analysis overview**

### `POST /api/v1/douyin/creator_v2/fetch_item_analysis_item_performance`
**获取投稿表现数据/Fetch item analysis item performance**

### `POST /api/v1/douyin/creator_v2/fetch_item_list`
**获取投稿作品列表/Fetch item list**

### `POST /api/v1/douyin/creator_v2/fetch_item_list_download`
**导出投稿作品列表/Download item list**

### `POST /api/v1/douyin/creator_v2/fetch_live_room_history_list`
**获取直播场次历史记录/Fetch live room history list**

### `POST /api/v1/douyin/creator_v2/fetch_author_diagnosis`
**获取创作者账号诊断/Fetch author diagnosis**


## /api/v1/douyin/search

### `POST /api/v1/douyin/search/fetch_general_search_v1`
**获取综合搜索 V1/Fetch general search V1**

### `POST /api/v1/douyin/search/fetch_general_search_v2`
**获取综合搜索 V2/Fetch general search V2**

### `POST /api/v1/douyin/search/fetch_general_search_v3`
**获取综合搜索 V3/Fetch general search V3**

### `POST /api/v1/douyin/search/fetch_search_suggest`
**获取搜索关键词推荐/Fetch search keyword suggestions**

### `POST /api/v1/douyin/search/fetch_video_search_v1`
**获取视频搜索 V1/Fetch video search V1**

### `POST /api/v1/douyin/search/fetch_video_search_v2`
**获取视频搜索 V2/Fetch video search V2**

### `POST /api/v1/douyin/search/fetch_multi_search`
**获取多重搜索/Fetch multi-type search**

### `POST /api/v1/douyin/search/fetch_user_search`
**获取用户搜索/Fetch user search**

### `POST /api/v1/douyin/search/fetch_user_search_v2`
**获取用户搜索 V2/Fetch user search V2**

### `POST /api/v1/douyin/search/fetch_image_search`
**获取图片搜索/Fetch image search**

### `POST /api/v1/douyin/search/fetch_image_search_v3`
**获取图文搜索 V3/Fetch image-text search V3**

### `POST /api/v1/douyin/search/fetch_live_search_v1`
**获取直播搜索 V1/Fetch live search V1**

### `POST /api/v1/douyin/search/fetch_challenge_search_v1`
**获取话题搜索 V1/Fetch hashtag search V1**

### `POST /api/v1/douyin/search/fetch_challenge_search_v2`
**获取话题搜索 V2/Fetch hashtag search V2**

### `POST /api/v1/douyin/search/fetch_challenge_suggest`
**获取话题推荐搜索/Fetch hashtag suggestions**

### `POST /api/v1/douyin/search/fetch_experience_search`
**获取经验搜索/Fetch experience search**

### `POST /api/v1/douyin/search/fetch_music_search`
**获取音乐搜索/Fetch music search**

### `POST /api/v1/douyin/search/fetch_discuss_search`
**获取讨论搜索/Fetch discussion search**

### `POST /api/v1/douyin/search/fetch_school_search`
**获取学校搜索/Fetch school search**

### `POST /api/v1/douyin/search/fetch_vision_search`
**获取图像识别搜索/Fetch vision search (image-based search)**


## /api/v1/douyin/billboard

### `GET /api/v1/douyin/billboard/fetch_city_list`
**获取中国城市列表/Fetch Chinese city list**

### `GET /api/v1/douyin/billboard/fetch_content_tag`
**获取垂类内容标签/Fetch vertical content tags**

### `GET /api/v1/douyin/billboard/fetch_hot_category_list`
**获取热点榜分类/Fetch hot list category**

Parameters:
  - `billboard_type`*: 榜单类型
  - `snapshot_time`: 快照时间 格式yyyyMMddHHmmss
  - `start_date`: 快照开始时间 格式yyyyMMdd
  - `end_date`: 快照结束时间 格式yyyyMMdd
  - `keyword`: 热点搜索词

### `GET /api/v1/douyin/billboard/fetch_hot_rise_list`
**获取上升热点榜/Fetch rising hot list**

Parameters:
  - `page`*: 页码
  - `page_size`*: 每页数量
  - `order`*: 排序方式
  - `sentence_tag`: 热点分类标签，从热点榜分类获取，多个分类用逗号分隔，空为全部
  - `keyword`: 热点搜索词

### `GET /api/v1/douyin/billboard/fetch_hot_city_list`
**获取同城热点榜/Fetch city hot list**

Parameters:
  - `page`*: 页码
  - `page_size`*: 每页数量
  - `order`*: 排序方式
  - `city_code`: 城市编码，从城市列表获取，空为全部
  - `sentence_tag`: 热点分类标签，从热点榜分类获取，多个分类用逗号分隔，空为全部
  - `keyword`: 热点搜索词

### `GET /api/v1/douyin/billboard/fetch_hot_challenge_list`
**获取挑战热榜/Fetch hot challenge list**

Parameters:
  - `page`*: 页码
  - `page_size`*: 每页数量
  - `keyword`: 热点搜索词

### `GET /api/v1/douyin/billboard/fetch_hot_total_list`
**获取热点总榜/Fetch total hot list**

Parameters:
  - `page`*: 页码
  - `page_size`*: 每页数量
  - `type`*: 快照类型 snapshot 按时刻查看 range 按时间范围
  - `snapshot_time`: 快照时间 格式yyyyMMddHHmmss
  - `start_date`: 快照开始时间 格式yyyyMMdd
  - `end_date`: 快照结束时间 格式yyyyMMdd
  - `sentence_tag`: 热点分类标签，从热点榜分类获取，多个分类用逗号分隔，空为全部
  - `keyword`: 热点搜索词

### `POST /api/v1/douyin/billboard/fetch_hot_calendar_list`
**获取活动日历/Fetch activity calendar**

### `GET /api/v1/douyin/billboard/fetch_hot_calendar_detail`
**获取活动日历详情/Fetch activity calendar detail**

Parameters:
  - `calendar_id`*: 活动id

### `GET /api/v1/douyin/billboard/fetch_hot_user_portrait_list`
**获取作品点赞观众画像-仅限热门榜/Fetch work like audience portrait - hot list only**

Parameters:
  - `aweme_id`*: 作品id
  - `option`: 选项，1 手机价格分布 2 性别分布 3 年龄分布 4 地域分布-省份 5 地域分布-城市 6 城市等级 7 手机品牌分

### `GET /api/v1/douyin/billboard/fetch_hot_comment_word_list`
**获取作品评论分析-词云权重/Fetch work comment analysis word cloud weight**

Parameters:
  - `aweme_id`*: 作品id

### `GET /api/v1/douyin/billboard/fetch_hot_item_trends_list`
**获取作品数据趋势/Fetch post data trend**

Parameters:
  - `aweme_id`: 作品id
  - `option`: 选项，7 点赞量 8 分享量 9 评论量
  - `date_window`: 时间窗口，1 按小时 2 按天

### `POST /api/v1/douyin/billboard/fetch_hot_account_list`
**获取热门账号/Fetch hot account list**

### `GET /api/v1/douyin/billboard/fetch_hot_account_search_list`
**搜索用户名或抖音号/Fetch account search list**

Parameters:
  - `keyword`*: 搜索的用户名或抖音号
  - `cursor`*: 游标，默认空

### `GET /api/v1/douyin/billboard/fetch_hot_account_trends_list`
**获取账号粉丝数据趋势/Fetch account fan data trend**

Parameters:
  - `sec_uid`*: 用户sec_id
  - `option`: 选项，2 新增点赞量 3 新增作品量 4 新增评论量 5 新增分享量
  - `date_window`: 时间窗口，1 按小时 2 按天

### `GET /api/v1/douyin/billboard/fetch_hot_account_item_analysis_list`
**获取账号作品分析-上周/Fetch account work analysis - last week**

Parameters:
  - `sec_uid`*: 用户sec_id

### `GET /api/v1/douyin/billboard/fetch_hot_account_fans_portrait_list`
**获取粉丝画像/Fetch fan portrait**

Parameters:
  - `sec_uid`*: 用户sec_id
  - `option`: 选项，1 手机价格分布 2 性别分布 3 年龄分布 4 地域分布-省份 5 地域分布-城市 6 城市等级 7 手机品牌分

### `GET /api/v1/douyin/billboard/fetch_hot_account_fans_interest_account_list`
**获取粉丝兴趣作者 20个用户/Fetch fan interest author 20 users**

Parameters:
  - `sec_uid`*: 用户sec_id

### `GET /api/v1/douyin/billboard/fetch_hot_account_fans_interest_topic_list`
**获取粉丝近3天感兴趣的话题 10个话题/Fetch fan interest topic in the last 3 days 10 topics**

Parameters:
  - `sec_uid`*: 用户sec_id

### `GET /api/v1/douyin/billboard/fetch_hot_account_fans_interest_search_list`
**获取粉丝近3天搜索词 10个搜索词/Fetch fan interest search term in the last 3 days 10 search terms**

Parameters:
  - `sec_uid`*: 用户sec_id

### `POST /api/v1/douyin/billboard/fetch_hot_total_video_list`
**获取视频热榜/Fetch video hot list**

### `POST /api/v1/douyin/billboard/fetch_hot_total_low_fan_list`
**获取低粉爆款榜/Fetch low fan explosion list**

### `POST /api/v1/douyin/billboard/fetch_hot_total_high_play_list`
**获取高完播率榜/Fetch high completion rate list**

### `POST /api/v1/douyin/billboard/fetch_hot_total_high_like_list`
**获取高点赞率榜/Fetch high like rate list**

### `POST /api/v1/douyin/billboard/fetch_hot_total_high_fan_list`
**获取高涨粉率榜/Fetch high fan rate list**

### `POST /api/v1/douyin/billboard/fetch_hot_total_topic_list`
**获取话题热榜/Fetch topic hot list**

### `POST /api/v1/douyin/billboard/fetch_hot_total_high_topic_list`
**获取热度飙升的话题榜/Fetch topic list with rising popularity**

### `POST /api/v1/douyin/billboard/fetch_hot_total_search_list`
**获取搜索热榜/Fetch search hot list**

### `POST /api/v1/douyin/billboard/fetch_hot_total_high_search_list`
**获取热度飙升的搜索榜/Fetch search list with rising popularity**

### `POST /api/v1/douyin/billboard/fetch_hot_total_hot_word_list`
**获取全部热门内容词/Fetch all hot content words**

### `GET /api/v1/douyin/billboard/fetch_hot_total_hot_word_detail_list`
**获取内容词详情/Fetch content word details**

Parameters:
  - `keyword`*: 搜索关键字
  - `word_id`*: 内容词id
  - `query_day`*: 查询日期，格式为YYYYMMDD，需为当日


## /api/v1/douyin/xingtu

### `GET /api/v1/douyin/xingtu/get_sign_image`
**获取加密图片解析/Get Sign Image**

Parameters:
  - `uri`*: 图片的uri/Image URI
  - `durationTS`: 有效期时长（秒）/Duration in seconds
  - `format`: 图片格式/Image format

### `GET /api/v1/douyin/xingtu/get_xingtu_kolid_by_uid`
**根据抖音用户ID获取游客星图kolid/Get XingTu kolid by Douyin User ID**

Parameters:
  - `uid`*: 抖音用户ID/Douyin User ID

### `GET /api/v1/douyin/xingtu/get_xingtu_kolid_by_sec_user_id`
**根据抖音sec_user_id获取游客星图kolid/Get XingTu kolid by Douyin sec_user_id**

Parameters:
  - `sec_user_id`*: 抖音用户sec_user_id/Douyin User sec_user_id

### `GET /api/v1/douyin/xingtu/get_xingtu_kolid_by_unique_id`
**根据抖音号获取游客星图kolid/Get XingTu kolid by Douyin unique_id**

Parameters:
  - `unique_id`*: 抖音号/Douyin User unique_id

### `GET /api/v1/douyin/xingtu/kol_base_info_v1`
**获取kol基本信息V1/Get kol Base Info V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId
  - `platformChannel`*: 平台渠道/Platform Channel

### `GET /api/v1/douyin/xingtu/kol_audience_portrait_v1`
**获取kol观众画像V1/Get kol Audience Portrait V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId

### `GET /api/v1/douyin/xingtu/kol_fans_portrait_v1`
**获取kol粉丝画像V1/Get kol Fans Portrait V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId
  - `fansType`: 粉丝类型/Fans Type

### `GET /api/v1/douyin/xingtu/kol_service_price_v1`
**获取kol服务报价V1/Get kol Service Price V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId
  - `platformChannel`*: 平台渠道/Platform Channel

### `GET /api/v1/douyin/xingtu/kol_data_overview_v1`
**获取kol数据概览V1/Get kol Data Overview V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId
  - `_type`*: 类型/Type
  - `_range`*: 范围/Range
  - `flowType`*: 流量类型/Flow Type
  - `onlyAssign`: 是否指派/Whether assigned (optional)

### `GET /api/v1/douyin/xingtu/search_kol_v1`
**关键词搜索kol V1/Search Kol V1**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `platformSource`*: 平台来源/Platform Source
  - `page`*: 页码/Page

### `GET /api/v1/douyin/xingtu/search_kol_v2`
**高级搜索kol V2/Search Kol Advanced V2**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `followerRange`: 粉丝范围(可选)/Follower Range (optional), 例如 10-100 表示10万-100万粉丝
  - `contentTag`: 内容标签(可选)/Content Tag (optional), 例如 tag-1 或 tag_level_two-7

### `GET /api/v1/douyin/xingtu/kol_conversion_ability_analysis_v1`
**获取kol转化能力分析V1/Get kol Conversion Ability Analysis V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId
  - `_range`*: 时间范围/Time Range

### `GET /api/v1/douyin/xingtu/kol_video_performance_v1`
**获取kol视频表现V1/Get kol Video Performance V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId
  - `onlyAssign`*: 是否只显示分配作品/Whether to display only assigned works

### `GET /api/v1/douyin/xingtu/kol_xingtu_index_v1`
**获取kol星图指数V1/Get kol Xingtu Index V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId

### `GET /api/v1/douyin/xingtu/kol_convert_video_display_v1`
**获取kol转化视频展示V1/Get kol Convert Video Display V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId
  - `detailType`*: 详情类型/Detail Type
  - `page`*: 页码/Page

### `GET /api/v1/douyin/xingtu/kol_link_struct_v1`
**获取kol连接用户V1/Get kol Link Struct V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId

### `GET /api/v1/douyin/xingtu/kol_touch_distribution_v1`
**获取kol连接用户来源V1/Get kol Touch Distribution V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId

### `GET /api/v1/douyin/xingtu/kol_cp_info_v1`
**获取kol性价比能力分析V1/Get kol Cp Info V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId

### `GET /api/v1/douyin/xingtu/kol_rec_videos_v1`
**获取kol内容表现V1/Get kol Rec Videos V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId

### `GET /api/v1/douyin/xingtu/kol_daily_fans_v1`
**获取kol粉丝趋势V1/Get kol Daily Fans V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId
  - `startDate`*: 开始日期/Start Date
  - `endDate`*: 结束日期/End Date

### `GET /api/v1/douyin/xingtu/author_hot_comment_tokens_v1`
**获取kol热词分析评论V1/Get Author Hot Comment Tokens V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId

### `GET /api/v1/douyin/xingtu/author_content_hot_comment_keywords_v1`
**获取kol热词分析内容V1/Get Author Content Hot Comment Keywords V1**

Parameters:
  - `kolId`*: 用户的kolId/User kolId


## /api/v1/douyin/xingtu_v2

### `GET /api/v1/douyin/xingtu_v2/get_ranking_list_catalog`
**获取星图热榜分类/Get Ranking List Catalog**

Parameters:
  - `codes`: 分类代码，默认为空字符串/Classification codes, default is empty string
  - `biz_scene`: 业务场景/Business scene

### `GET /api/v1/douyin/xingtu_v2/get_ranking_list_data`
**获取星图达人商业榜数据/Get Ranking List Data**

Parameters:
  - `code`: 榜单类型代码/Ranking type code
  - `qualifier`: 榜单分类ID，从get_ranking_list_catalog获取/Category qualifier_id
  - `version`: 版本/Version
  - `period`: 统计周期，7=周榜，30=月榜/Period, 7=weekly, 30=monthly
  - `date`: 统计日期，格式YYYYMMDD/Date, format YYYYMMDD
  - `limit`: 返回数量/Result limit

### `POST /api/v1/douyin/xingtu_v2/get_playlet_actor_rank_catalog`
**获取短剧演员热榜分类/Get Playlet Actor Rank Catalog**

### `GET /api/v1/douyin/xingtu_v2/get_playlet_actor_rank_list`
**获取短剧演员热榜/Get Playlet Actor Rank List**

Parameters:
  - `category`: 分类/Category
  - `name`: 榜单名称/Ranking name
  - `qualifier`: 达人类型，空字符串=不限/Actor type, empty=all
  - `period`: 统计周期，7=周榜，30=月榜/Period, 7=weekly, 30=monthly
  - `date`: 统计日期，格式YYYYMMDD/Date, format YYYYMMDD
  - `limit`: 返回数量/Result limit

### `GET /api/v1/douyin/xingtu_v2/get_author_market_fields`
**获取达人广场筛选字段/Get Author Market Fields**

Parameters:
  - `market_scene`: 市场场景，1=默认场景/Market scene, 1=default

### `GET /api/v1/douyin/xingtu_v2/get_author_base_info`
**获取创作者基本信息/Get Author Base Info**

Parameters:
  - `o_author_id`*: 创作者ID/Creator author ID
  - `platform_source`: 平台来源/Platform source
  - `platform_channel`: 平台渠道/Platform channel
  - `recommend`: 是否返回推荐信息/Whether to return recommendation info
  - `need_sec_uid`: 是否返回sec_uid/Whether to return sec_uid
  - `need_linkage_info`: 是否返回联动信息/Whether to return linkage info

### `GET /api/v1/douyin/xingtu_v2/get_author_business_card_info`
**获取创作者商业卡片信息/Get Author Business Card Info**

Parameters:
  - `o_author_id`*: 创作者ID/Creator author ID

### `GET /api/v1/douyin/xingtu_v2/get_author_local_info`
**获取创作者位置信息/Get Author Local Info**

Parameters:
  - `o_author_id`*: 创作者ID/Creator author ID
  - `platform_source`: 平台来源/Platform source
  - `platform_channel`: 平台渠道/Platform channel
  - `time_range`: 时间范围(天)/Time range in days

### `GET /api/v1/douyin/xingtu_v2/get_author_show_items`
**获取创作者视频列表/Get Author Show Items**

Parameters:
  - `o_author_id`*: 创作者ID/Creator author ID
  - `platform_source`: 平台来源/Platform source
  - `platform_channel`: 平台渠道/Platform channel
  - `limit`: 返回数量/Result limit
  - `only_assign`: 仅看指派视频/Only show assigned videos
  - `flow_type`: 流量类型/Flow type

### `GET /api/v1/douyin/xingtu_v2/get_author_hot_comment_tokens`
**获取创作者评论热词/Get Author Hot Comment Tokens**

Parameters:
  - `author_id`*: 创作者ID/Creator author ID
  - `num`: 返回热词数量/Number of hot tokens
  - `without_emoji`: 是否排除emoji/Whether to exclude emoji

### `GET /api/v1/douyin/xingtu_v2/get_author_content_hot_keywords`
**获取创作者内容热词/Get Author Content Hot Keywords**

Parameters:
  - `author_id`*: 创作者ID/Creator author ID
  - `keyword_type`: 热词类型/Keyword type

### `POST /api/v1/douyin/xingtu_v2/get_recommend_for_star_authors`
**获取相似创作者推荐/Get Recommend Similar Star Authors**

### `GET /api/v1/douyin/xingtu_v2/get_excellent_case_category_list`
**获取优秀行业分类列表/Get Excellent Case Category List**

Parameters:
  - `platform_source`: 平台来源/Platform source

### `GET /api/v1/douyin/xingtu_v2/get_author_spread_info`
**获取创作者传播价值/Get Author Spread Info**

Parameters:
  - `o_author_id`*: 创作者ID/Creator author ID
  - `platform_source`: 平台来源/Platform source
  - `platform_channel`: 平台渠道/Platform channel
  - `type`: 视频类型，1=个人视频/Video type, 1=personal video
  - `flow_type`: 流量类型/Flow type
  - `only_assign`: 仅看指派视频/Only assigned videos
  - `range`: 时间范围，2=近30天，3=近90天/Time range, 2=last 30 days, 3=last 90 day

### `GET /api/v1/douyin/xingtu_v2/get_user_profile_qrcode`
**获取用户主页二维码/Get User Profile QRCode**

Parameters:
  - `core_user_id`: 用户核心ID(与sec_uid二选一)/User core ID (pick one with sec_uid)
  - `sec_uid`: 用户sec_uid(与core_user_id二选一)/User sec_uid (pick one with core

### `GET /api/v1/douyin/xingtu_v2/get_content_trend_guide`
**获取内容趋势指南/Get Content Trend Guide**

### `GET /api/v1/douyin/xingtu_v2/get_ip_activity_industry_list`
**获取星图IP日历行业列表/Get IP Activity Industry List**

### `POST /api/v1/douyin/xingtu_v2/get_ip_activity_list`
**获取星图IP日历活动列表/Get IP Activity List**

### `GET /api/v1/douyin/xingtu_v2/get_ip_activity_detail`
**获取星图IP活动详情/Get IP Activity Detail**

Parameters:
  - `id`*: 活动ID，从get_ip_activity_list获取/Activity ID from get_ip_activit

### `GET /api/v1/douyin/xingtu_v2/get_resource_list`
**获取营销活动案例/Get Resource List**

Parameters:
  - `resource_id`*: 资源ID/Resource ID

### `GET /api/v1/douyin/xingtu_v2/get_demander_mcn_list`
**搜索MCN机构列表/Get Demander MCN List**

Parameters:
  - `mcn_name`: MCN机构名称，支持模糊搜索/MCN name, supports fuzzy search
  - `page`: 页码/Page number
  - `limit`: 每页数量/Page size
  - `order_by`: 排序方式/Sort by
