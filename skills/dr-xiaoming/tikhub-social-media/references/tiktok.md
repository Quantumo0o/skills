# Tiktok API Reference

Total endpoints: 197


## /api/v1/tiktok/web

### `GET /api/v1/tiktok/web/fetch_post_detail`
**获取单个作品数据/Get single video data**

Parameters:
  - `itemId`*: 作品id/Video id

### `GET /api/v1/tiktok/web/fetch_post_detail_v2`
**获取单个作品数据 V2/Get single video data V2**

Parameters:
  - `itemId`*: 作品id/Video id

### `GET /api/v1/tiktok/web/fetch_explore_post`
**获取探索作品数据/Get explore video data**

Parameters:
  - `categoryType`: 作品分类/Video category
  - `count`: 每页数量/Number per page

### `GET /api/v1/tiktok/web/fetch_trending_post`
**获取每日热门内容作品数据/Get daily trending video data**

### `GET /api/v1/tiktok/web/fetch_trending_searchwords`
**获取每日趋势搜索关键词/Get daily trending search words**

### `GET /api/v1/tiktok/web/fetch_user_profile`
**获取用户的个人信息/Get user profile**

Parameters:
  - `uniqueId`: 用户uniqueId/User uniqueId
  - `secUid`: 用户secUid/User secUid

### `GET /api/v1/tiktok/web/fetch_user_post`
**获取用户的作品列表/Get user posts**

Parameters:
  - `secUid`*: 用户secUid/User secUid
  - `cursor`: 翻页游标/Page cursor
  - `count`: 每页数量/Number per page
  - `coverFormat`: 封面格式/Cover format
  - `post_item_list_request_type`: 排序方式/Sort type

### `GET /api/v1/tiktok/web/fetch_user_repost`
**获取用户的转发作品列表/Get user reposts**

Parameters:
  - `secUid`*: 用户secUid/User secUid
  - `cursor`: 翻页游标/Page cursor
  - `count`: 每页数量/Number per page
  - `coverFormat`: 封面格式/Cover format

### `GET /api/v1/tiktok/web/fetch_user_like`
**获取用户的点赞列表/Get user likes**

Parameters:
  - `secUid`*: 用户secUid/User secUid
  - `cursor`: 翻页游标/Page cursor
  - `count`: 每页数量/Number per page
  - `coverFormat`: 封面格式/Cover format
  - `post_item_list_request_type`: 排序方式/Sort type

### `GET /api/v1/tiktok/web/fetch_user_collect`
**获取用户的收藏列表/Get user favorites**

Parameters:
  - `cookie`*: 用户cookie/User cookie
  - `secUid`*: 用户secUid/User secUid
  - `cursor`: 翻页游标/Page cursor
  - `count`: 每页数量/Number per page
  - `coverFormat`: 封面格式/Cover format

### `GET /api/v1/tiktok/web/fetch_user_play_list`
**获取用户的播放列表/Get user play list**

Parameters:
  - `secUid`*: 用户secUid/User secUid
  - `cursor`: 翻页游标/Page cursor
  - `count`: 每页数量/Number per page

### `GET /api/v1/tiktok/web/fetch_user_mix`
**获取用户的合辑列表/Get user mix list**

Parameters:
  - `mixId`*: 合辑id/Mix id
  - `cursor`: 翻页游标/Page cursor
  - `count`: 每页数量/Number per page

### `GET /api/v1/tiktok/web/fetch_post_comment`
**获取作品的评论列表/Get video comments**

Parameters:
  - `aweme_id`*: 作品id/Video id
  - `cursor`: 翻页游标/Page cursor
  - `count`: 每页数量/Number per page
  - `current_region`: 当前地区/Current region

### `GET /api/v1/tiktok/web/fetch_post_comment_reply`
**获取作品的评论回复列表/Get video comment replies**

Parameters:
  - `item_id`*: 作品id/Video id
  - `comment_id`*: 评论id/Comment id
  - `cursor`: 翻页游标/Page cursor
  - `count`: 每页数量/Number per page
  - `current_region`: 当前地区/Current region

### `GET /api/v1/tiktok/web/fetch_user_fans`
**获取用户的粉丝列表/Get user followers**

Parameters:
  - `secUid`*: 用户secUid/User secUid
  - `count`: 每页数量/Number per page
  - `maxCursor`: 最大游标/Max cursor
  - `minCursor`: 最小游标/Min cursor

### `GET /api/v1/tiktok/web/fetch_user_follow`
**获取用户的关注列表/Get user followings**

Parameters:
  - `secUid`*: 用户secUid/User secUid
  - `count`: 每页数量/Number per page
  - `maxCursor`: 最大游标/Max cursor
  - `minCursor`: 最小游标/Min cursor

### `GET /api/v1/tiktok/web/fetch_user_live_detail`
**获取用户的直播详情/Get user live details**

Parameters:
  - `uniqueId`*: 用户uniqueId/User uniqueId

### `GET /api/v1/tiktok/web/fetch_general_search`
**获取综合搜索列表/Get general search list**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `offset`: 翻页游标/Page cursor
  - `search_id`: 搜索id，翻页时需要提供/Search id, need to provide when paging
  - `cookie`: 用户cookie(按需提供)/User cookie(if needed)

### `GET /api/v1/tiktok/web/fetch_search_keyword_suggest`
**搜索关键字推荐/Search keyword suggest**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword

### `GET /api/v1/tiktok/web/fetch_search_user`
**搜索用户/Search user**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `cursor`: 翻页游标/Page cursor
  - `search_id`: 搜索id，翻页时需要提供/Search id, need to provide when paging
  - `cookie`: 用户cookie(按需提供)/User cookie(if needed)

### `GET /api/v1/tiktok/web/fetch_search_video`
**搜索视频/Search video**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `count`: 每页数量/Number per page
  - `offset`: 翻页游标/Page cursor
  - `search_id`: 搜索id，翻页时需要提供/Search id, need to provide when paging
  - `cookie`: 用户cookie(按需提供)/User cookie(if needed)

### `GET /api/v1/tiktok/web/fetch_search_live`
**搜索直播/Search live**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `count`: 每页数量/Number per page
  - `offset`: 翻页游标/Page cursor
  - `search_id`: 搜索id，翻页时需要提供/Search id, need to provide when paging
  - `cookie`: 用户cookie(按需提供)/User cookie(if needed)

### `GET /api/v1/tiktok/web/fetch_search_photo`
**搜索照片/Search photo**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `count`: 每页数量/Number per page
  - `offset`: 翻页游标/Page offset
  - `search_id`: 搜索id，翻页时需要提供/Search id, need to provide when paging
  - `cookie`: 用户cookie(按需提供)/User cookie(if needed)

### `GET /api/v1/tiktok/web/fetch_tag_detail`
**Tag详情/Tag Detail**

Parameters:
  - `tag_name`*: Tag名称/Tag name

### `GET /api/v1/tiktok/web/fetch_tag_post`
**Tag作品/Tag Post**

Parameters:
  - `challengeID`*: Tag ID
  - `count`: 每页数量/Number per page
  - `cursor`: 翻页游标/Page cursor

### `POST /api/v1/tiktok/web/fetch_home_feed`
**首页推荐作品/Home Feed**

### `GET /api/v1/tiktok/web/generate_real_msToken`
**生成真实msToken/Generate real msToken**

Parameters:
  - `random_strData`: 
  - `browser_type`: 

### `GET /api/v1/tiktok/web/encrypt_strData`
**加密strData/Encrypt strData**

Parameters:
  - `data`*: 原始指纹数据字符串（JSON格式或字典字符串）/Raw fingerprint data string (JSON fo

### `GET /api/v1/tiktok/web/decrypt_strData`
**解密strData/Decrypt strData**

Parameters:
  - `encrypted_data`*: 加密后的strData字符串/Encrypted strData string

### `GET /api/v1/tiktok/web/generate_fingerprint`
**生成浏览器指纹/Generate browser fingerprint**

Parameters:
  - `browser_type`: 

### `GET /api/v1/tiktok/web/generate_webid`
**生成web_id/Generate web_id**

Parameters:
  - `cookie`: 
  - `user_agent`: 
  - `url`: 
  - `referer`: 
  - `user_unique_id`: 
  - `app_id`: 

### `GET /api/v1/tiktok/web/generate_ttwid`
**生成ttwid/Generate ttwid**

Parameters:
  - `user_agent`: 

### `POST /api/v1/tiktok/web/generate_xbogus`
**生成 XBogus/Generate XBogus**

### `POST /api/v1/tiktok/web/generate_xgnarly`
**生成 XGnarly /Generate XGnarly**

### `POST /api/v1/tiktok/web/generate_xgnarly_and_xbogus`
**生成 XGnarly 和 XBogus /Generate XGnarly and XBogus**

### `GET /api/v1/tiktok/web/get_user_id`
**提取用户user_id/Extract user user_id**

Parameters:
  - `url`*: 用户主页链接/User homepage link

### `GET /api/v1/tiktok/web/get_sec_user_id`
**提取用户sec_user_id/Extract user sec_user_id**

Parameters:
  - `url`*: 用户主页链接/User homepage link

### `POST /api/v1/tiktok/web/get_all_sec_user_id`
**提取列表用户sec_user_id/Extract list user sec_user_id**

### `GET /api/v1/tiktok/web/get_aweme_id`
**提取单个作品id/Extract single video id**

Parameters:
  - `url`*: 作品链接/Video link

### `POST /api/v1/tiktok/web/get_all_aweme_id`
**提取列表作品id/Extract list video id**

### `GET /api/v1/tiktok/web/get_unique_id`
**获取用户unique_id/Get user unique_id**

Parameters:
  - `url`*: 用户主页链接/User homepage link

### `POST /api/v1/tiktok/web/get_all_unique_id`
**获取列表unique_id/Get list unique_id**

### `GET /api/v1/tiktok/web/tiktok_live_room`
**提取直播间弹幕/Extract live room danmaku**

Parameters:
  - `live_room_url`*: 直播间链接/Live room link
  - `danmaku_type`*: 消息类型/Message type

### `GET /api/v1/tiktok/web/fetch_live_im_fetch`
**TikTok直播间弹幕参数获取/tiktok live room danmaku parameters**

Parameters:
  - `room_id`*: 直播间号/Live room id
  - `user_unique_id`*: 用户唯一ID/User unique ID

### `GET /api/v1/tiktok/web/get_live_room_id`
**根据直播间链接提取直播间ID/Extract live room ID from live room link**

Parameters:
  - `live_room_url`*: 直播间链接/Live room link

### `GET /api/v1/tiktok/web/fetch_check_live_alive`
**直播间开播状态检测/Live room start status check**

Parameters:
  - `room_id`*: 直播间ID/Live room ID

### `GET /api/v1/tiktok/web/fetch_batch_check_live_alive`
**批量直播间开播状态检测/Batch live room start status check**

Parameters:
  - `room_ids`*: 直播间ID列表，用英文逗号分隔，最多支持50个/Live room ID list separated by comma

### `GET /api/v1/tiktok/web/fetch_tiktok_live_data`
**通过直播链接获取直播间信息/Get live room information via live link**

Parameters:
  - `live_room_url`*: 直播间链接/Live room link

### `GET /api/v1/tiktok/web/fetch_live_recommend`
**获取直播间首页推荐列表/Get live room homepage recommendation list**

Parameters:
  - `related_live_tag`*: 相关直播标签/Related live tag

### `GET /api/v1/tiktok/web/fetch_live_gift_list`
**获取直播间礼物列表/Get live room gift list**

Parameters:
  - `room_id`: 直播间ID，可选参数/Live room ID, optional parameter

### `GET /api/v1/tiktok/web/fetch_sso_login_qrcode`
**获取SSO登录二维码/Get SSO login QR code**

Parameters:
  - `device_id`*: 设备ID/Device ID
  - `region`*: 地区/Region
  - `proxy`*: 代理/Proxy

### `GET /api/v1/tiktok/web/fetch_sso_login_status`
**获取SSO登录状态/Get SSO login status**

Parameters:
  - `token`*: 登录令牌/Login token
  - `device_id`*: 设备ID/Device ID
  - `verifyFp`*: verifyFp
  - `region`*: 地区/Region
  - `proxy`*: 代理/Proxy

### `GET /api/v1/tiktok/web/fetch_sso_login_auth`
**认证SSO登录/Authenticate SSO login**

Parameters:
  - `device_id`*: 设备ID/Device ID
  - `verifyFp`*: verifyFp
  - `region`*: 地区/Region
  - `proxy`*: 代理/Proxy

### `GET /api/v1/tiktok/web/generate_hashed_id`
**生成哈希ID/Generate hashed ID**

Parameters:
  - `email`*: 邮箱地址/Email address

### `POST /api/v1/tiktok/web/fetch_gift_name_by_id`
**根据Gift ID查询礼物名称/Get gift name by gift ID**

### `POST /api/v1/tiktok/web/fetch_gift_names_by_ids`
**批量查询Gift ID对应的礼物名称($0.025/次,建议50个)/Batch get gift names by gift IDs ($0.025/call, suggest 50)**

### `GET /api/v1/tiktok/web/fetch_tiktok_web_guest_cookie`
**获取游客 Cookie/Get the guest Cookie**

Parameters:
  - `user_agent`*: 用户浏览器代理/User browser agent

### `GET /api/v1/tiktok/web/device_register`
**设备注册/Register device for TikTok Web**


## /api/v1/tiktok/app

### `GET /api/v1/tiktok/app/v3/fetch_one_video`
**获取单个作品数据/Get single video data**

Parameters:
  - `aweme_id`*: 作品id/Video id

### `GET /api/v1/tiktok/app/v3/fetch_one_video_v2`
**获取单个作品数据 V2/Get single video data V2**

Parameters:
  - `aweme_id`*: 作品id/Video id

### `GET /api/v1/tiktok/app/v3/fetch_one_video_v3`
**获取单个作品数据 V3(支持国家参数)/Get single video data V3 (support country parameter)**

Parameters:
  - `aweme_id`*: 作品id/Video id
  - `region`: 国家代码/Country code

### `POST /api/v1/tiktok/app/v3/fetch_multi_video`
**批量获取视频信息/Batch Get Video Information**

### `POST /api/v1/tiktok/app/v3/fetch_multi_video_v2`
**批量获取视频信息 V2/Batch Get Video Information V2**

### `GET /api/v1/tiktok/app/v3/fetch_one_video_by_share_url_v2`
**根据分享链接获取单个作品数据/Get single video data by sharing link**

Parameters:
  - `share_url`*: 分享链接/Share link

### `GET /api/v1/tiktok/app/v3/fetch_one_video_by_share_url`
**根据分享链接获取单个作品数据/Get single video data by sharing link**

Parameters:
  - `share_url`*: 分享链接/Share link

### `GET /api/v1/tiktok/app/v3/get_user_id_and_sec_user_id_by_username`
**使用用户名获取用户 user_id 和 sec_user_id/Get user_id and sec_user_id by Username**

Parameters:
  - `username`*: 用户名/Username

### `GET /api/v1/tiktok/app/v3/handler_user_profile`
**获取指定用户的信息/Get information of specified user**

Parameters:
  - `user_id`: 用户uid （可选，纯数字）/User uid (optional, pure number)
  - `sec_user_id`: 用户sec_user_id/User sec_user_id
  - `unique_id`: 用户unique_id （用户名）/User unique_id (username)

### `GET /api/v1/tiktok/app/v3/fetch_webcast_user_info`
**获取指定 Webcast 用户的信息/Get information of specified Webcast user**

Parameters:
  - `user_id`: 用户uid （可选，纯数字）/User uid (optional, pure number)
  - `sec_user_id`: 用户sec_user_id/User sec_user_id

### `GET /api/v1/tiktok/app/v3/fetch_user_country_by_username`
**通过用户名获取用户账号国家地区/Get user account country by username**

Parameters:
  - `username`*: 用户名/Username

### `GET /api/v1/tiktok/app/v3/fetch_similar_user_recommendations`
**获取类似用户推荐/Similar User Recommendations**

Parameters:
  - `sec_uid`*: 用户sec_uid/User sec_uid
  - `page_token`: 分页标记/Page token

### `GET /api/v1/tiktok/app/v3/fetch_user_repost_videos`
**获取用户转发的作品数据/Get user repost video data**

Parameters:
  - `user_id`*: 用户id/User id
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number

### `GET /api/v1/tiktok/app/v3/fetch_user_post_videos`
**获取用户主页作品数据 V1/Get user homepage video data V1**

Parameters:
  - `sec_user_id`: 用户sec_user_id/User sec_user_id
  - `unique_id`: 用户unique_id/User unique_id
  - `max_cursor`: 最大游标/Maximum cursor
  - `count`: 每页数量/Number per page
  - `sort_type`: 排序类型/Sort type

### `GET /api/v1/tiktok/app/v3/fetch_user_post_videos_v2`
**获取用户主页作品数据 V2/Get user homepage video data V2**

Parameters:
  - `sec_user_id`: 用户sec_user_id/User sec_user_id
  - `unique_id`: 用户unique_id/User unique_id
  - `max_cursor`: 最大游标/Maximum cursor
  - `count`: 每页数量/Number per page
  - `sort_type`: 排序类型/Sort type

### `GET /api/v1/tiktok/app/v3/fetch_user_post_videos_v3`
**获取用户主页作品数据 V3（精简数据-更快速）/Get user homepage video data V3 (simplified data - faster)**

Parameters:
  - `sec_user_id`: 用户sec_user_id/User sec_user_id
  - `unique_id`: 用户unique_id/User unique_id
  - `max_cursor`: 最大游标/Maximum cursor
  - `count`: 每页数量/Number per page
  - `sort_type`: 排序类型/Sort type

### `GET /api/v1/tiktok/app/v3/fetch_user_like_videos`
**获取用户喜欢作品数据/Get user like video data**

Parameters:
  - `sec_user_id`*: 用户sec_user_id/User sec_user_id
  - `max_cursor`: 最大游标/Maximum cursor
  - `counts`: 每页数量/Number per page

### `GET /api/v1/tiktok/app/v3/fetch_video_comments`
**获取单个视频评论数据/Get single video comments data**

Parameters:
  - `aweme_id`*: 作品id/Video id
  - `cursor`: 游标/Cursor
  - `count`: 数量/Number

### `GET /api/v1/tiktok/app/v3/fetch_video_comment_replies`
**获取指定视频的评论回复数据/Get comment replies data of specified video**

Parameters:
  - `item_id`*: 作品id/Video id
  - `comment_id`*: 评论id/Comment id
  - `cursor`: 游标/Cursor
  - `count`: 数量/Number

### `GET /api/v1/tiktok/app/v3/fetch_general_search_result`
**获取指定关键词的综合搜索结果/Get comprehensive search results of specified keywords**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number
  - `sort_type`: 排序类型/Sort type
  - `publish_time`: 发布时间/Publish time

### `GET /api/v1/tiktok/app/v3/fetch_video_search_result`
**获取指定关键词的视频搜索结果/Get video search results of specified keywords**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number
  - `sort_type`: 排序类型/Sort type
  - `publish_time`: 发布时间/Publish time
  - `region`: 地区/Region

### `GET /api/v1/tiktok/app/v3/fetch_user_search_result`
**获取指定关键词的用户搜索结果/Get user search results of specified keywords**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number
  - `user_search_follower_count`: 根据粉丝数排序/Sort by number of followers
  - `user_search_profile_type`: 根据账号类型排序/Sort by account type
  - `user_search_other_pref`: 根据其他偏好排序/Sort by other preferences

### `GET /api/v1/tiktok/app/v3/fetch_music_search_result`
**获取指定关键词的音乐搜索结果/Get music search results of specified keywords**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number
  - `filter_by`: 过滤类型/Filter type
  - `sort_type`: 排序类型/Sort type
  - `region`: 地区/Region

### `GET /api/v1/tiktok/app/v3/fetch_hashtag_search_result`
**获取指定关键词的话题搜索结果/Get hashtag search results of specified keywords**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number

### `GET /api/v1/tiktok/app/v3/fetch_live_search_result`
**获取指定关键词的直播搜索结果/Get live search results of specified keywords**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number
  - `region`: 地区/Region

### `GET /api/v1/tiktok/app/v3/fetch_location_search`
**获取地点搜索结果/Get location search results**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `count`: 数量/Number

### `GET /api/v1/tiktok/app/v3/fetch_music_detail`
**获取指定音乐的详情数据/Get details of specified music**

Parameters:
  - `music_id`*: 音乐id/Music id

### `GET /api/v1/tiktok/app/v3/fetch_music_video_list`
**获取指定音乐的视频列表数据/Get video list of specified music**

Parameters:
  - `music_id`*: 音乐id/Music id
  - `cursor`: 游标/Cursor
  - `count`: 数量/Number

### `GET /api/v1/tiktok/app/v3/fetch_hashtag_detail`
**获取指定话题的详情数据/Get details of specified hashtag**

Parameters:
  - `ch_id`*: 话题id/Hashtag id

### `GET /api/v1/tiktok/app/v3/fetch_hashtag_video_list`
**获取指定话题的作品数据/Get video list of specified hashtag**

Parameters:
  - `ch_id`*: 话题id/Hashtag id
  - `cursor`: 游标/Cursor
  - `count`: 数量/Number

### `GET /api/v1/tiktok/app/v3/fetch_user_follower_list`
**获取指定用户的粉丝列表数据/Get follower list of specified user**

Parameters:
  - `user_id`: 用户ID/User ID (与sec_user_id二选一/One of user_id and sec_user_id
  - `sec_user_id`: 用户sec_user_id/User sec_user_id (与user_id二选一/One of user_id a
  - `count`: 数量/Number
  - `min_time`: 最小时间，用于翻页/Minimum time for paging
  - `page_token`: 翻页token/Page token

### `GET /api/v1/tiktok/app/v3/fetch_user_following_list`
**获取指定用户的关注列表数据/Get following list of specified user**

Parameters:
  - `user_id`: 用户ID/User ID (与sec_user_id二选一/One of user_id and sec_user_id
  - `sec_user_id`: 用户sec_user_id/User sec_user_id (与user_id二选一/One of user_id a
  - `count`: 数量/Number
  - `min_time`: 最小时间，用于翻页/Minimum time for paging
  - `page_token`: 翻页token/Page token

### `GET /api/v1/tiktok/app/v3/fetch_creator_search_insights`
**创作者搜索洞察/Creator Search Insights**

Parameters:
  - `offset`: 分页偏移量/Pagination offset
  - `limit`: 每页数量/Number per page
  - `tab`: 标签页类型/Tab type (all/content_gap/follower_searched/life_style
  - `language_filters`: 语言过滤器，多个用逗号分隔/Language filters (id/de/en/es/fr/pt/vi/tr/ar/t
  - `category_filters`: 分类过滤器，多个用逗号分隔/Category filters (Gaming/Fashion/Tourism/Scien
  - `creator_source`: 创作者来源/Creator source
  - `force_refresh`: 是否强制刷新/Force refresh

### `GET /api/v1/tiktok/app/v3/fetch_creator_search_insights_detail`
**创作者搜索洞察详情/Creator Search Insights Detail**

Parameters:
  - `query_id_str`*: 搜索词条ID，从 fetch_creator_search_insights 接口获取/Query ID from fe
  - `time_range`: 时间范围/Time range (past_7_days/past_30_days/past_60_days/past_
  - `start_date`: 开始时间戳（秒），仅当 time_range=custom 时生效/Start timestamp (seconds),
  - `end_date`: 结束时间戳（秒），仅当 time_range=custom 时生效/End timestamp (seconds), o
  - `dimension_list`: 维度列表，多个用逗号分隔/Dimension list (gender/age/country)

### `GET /api/v1/tiktok/app/v3/fetch_creator_search_insights_trend`
**创作者搜索洞察趋势/Creator Search Insights Trend**

Parameters:
  - `query_id_str`*: 搜索词条ID，从 fetch_creator_search_insights 接口获取/Query ID from fe
  - `from_tab_path`: 来源标签路径/From tab path
  - `query_analysis_required`: 是否需要查询分析/Whether query analysis is required

### `GET /api/v1/tiktok/app/v3/fetch_creator_search_insights_videos`
**创作者搜索洞察相关视频/Creator Search Insights Videos**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `offset`: 分页偏移量/Pagination offset
  - `count`: 每页数量/Number per page

### `GET /api/v1/tiktok/app/v3/fetch_music_chart_list`
**音乐排行榜/Music Chart List**

Parameters:
  - `scene`: 排行榜类型/Chart type (0: Top 50, 1: Viral 50)
  - `cursor`: 分页游标/Pagination cursor
  - `count`: 每页数量/Number per page (max 50)

### `GET /api/v1/tiktok/app/v3/search_follower_list`
**搜索粉丝列表/Search follower list**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `keyword`*: 搜索关键词/Search keyword

### `GET /api/v1/tiktok/app/v3/search_following_list`
**搜索关注列表/Search following list**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `keyword`*: 搜索关键词/Search keyword

### `GET /api/v1/tiktok/app/v3/fetch_live_room_info`
**获取指定直播间的数据/Get data of specified live room**

Parameters:
  - `room_id`*: 直播间id/Live room id

### `GET /api/v1/tiktok/app/v3/fetch_live_ranking_list`
**获取直播间排行榜数据/Get live room ranking list**

Parameters:
  - `room_id`*: 直播间id/Live room id
  - `anchor_id`*: 主播id/Anchor id

### `GET /api/v1/tiktok/app/v3/check_live_room_online`
**检测直播间是否在线/Check if live room is online**

Parameters:
  - `room_id`*: 直播间id/Live room id

### `POST /api/v1/tiktok/app/v3/check_live_room_online_batch`
**批量检测直播间是否在线/Batch check if live rooms are online**

### `GET /api/v1/tiktok/app/v3/fetch_share_short_link`
**获取分享短链接/Get share short link**

Parameters:
  - `url`*: 分享链接/Share link

### `GET /api/v1/tiktok/app/v3/fetch_share_qr_code`
**获取分享二维码/Get share QR code**

Parameters:
  - `object_id`*: 对象id/Object id
  - `schema_type`: 模式类型/Schema type

### `GET /api/v1/tiktok/app/v3/fetch_product_search`
**获取商品搜索结果/Get product search results**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `cursor`: 游标/Cursor
  - `count`: 数量/Number
  - `sort_type`: 商品排序条件/Product sorting conditions
  - `customer_review_four_star`: 四星以上评价/Four-star or more reviews
  - `have_discount`: 有优惠/Having discount
  - `min_price`: 最低价格/Minimum price
  - `max_price`: 最高价格/Maximum price

### `GET /api/v1/tiktok/app/v3/fetch_creator_info`
**获取带货创作者信息/Get shopping creator information**

Parameters:
  - `creator_uid`*: 创作者uid/Creator uid

### `GET /api/v1/tiktok/app/v3/fetch_creator_showcase_product_list`
**获取创作者橱窗商品列表/Get creator showcase product list**

Parameters:
  - `kol_id`*: 创作者的sec_user_id/Creator's sec_user_id
  - `count`: 数量/Number
  - `next_scroll_param`: 翻页参数/Page parameter

### `GET /api/v1/tiktok/app/v3/fetch_shop_id_by_share_link`
**通过分享链接获取店铺ID/Get Shop ID by Share Link**

Parameters:
  - `share_link`*: 分享链接/Share link

### `GET /api/v1/tiktok/app/v3/fetch_product_id_by_share_link`
**通过分享链接获取商品ID/Get Product ID by Share Link**

Parameters:
  - `share_link`*: 分享链接/Share link

### `GET /api/v1/tiktok/app/v3/fetch_product_detail`
**获取商品详情数据（即将弃用，使用 fetch_product_detail_v2 代替）/Get product detail data (will be deprecated, use fetch_product_detail_v2 instead)**

Parameters:
  - `product_id`*: 商品id/Product id

### `GET /api/v1/tiktok/app/v3/fetch_product_detail_v2`
**获取商品详情数据V2/Get product detail data V2**

Parameters:
  - `product_id`*: 商品id/Product id

### `GET /api/v1/tiktok/app/v3/fetch_product_detail_v3`
**获取商品详情数据V3 / Get product detail data V3**

Parameters:
  - `product_id`*: 商品id / Product ID
  - `region`: 商品的国家/地区代码/ Country/region code of the product

### `GET /api/v1/tiktok/app/v3/fetch_product_detail_v4`
**获取商品详情数据V4 / Get product detail data V4**

Parameters:
  - `product_id`*: 商品id / Product ID
  - `region`: 商品的国家/地区代码/ Country/region code of the product

### `GET /api/v1/tiktok/app/v3/fetch_product_review`
**获取商品评价数据/Get product review data**

Parameters:
  - `product_id`*: 商品id/Product id
  - `cursor`: 游标/Cursor
  - `size`: 数量/Number
  - `filter_id`: 筛选条件/Filter condition
  - `sort_type`: 排序条件/Sorting conditions

### `GET /api/v1/tiktok/app/v3/fetch_shop_home_page_list`
**获取商家主页Page列表数据/Get shop home page list data**

Parameters:
  - `seller_id`*: 商家id,店铺id/Seller id, shop id

### `GET /api/v1/tiktok/app/v3/fetch_shop_home`
**获取商家主页数据/Get shop home page data**

Parameters:
  - `page_id`*: 爬取的商家主页Page id/Page id of the crawled shop home page
  - `seller_id`*: 商家id,店铺id/Seller id, shop id

### `GET /api/v1/tiktok/app/v3/fetch_shop_product_recommend`
**获取商家商品推荐数据/Get shop product recommend data**

Parameters:
  - `seller_id`*: 商家id,店铺id/Seller id, shop id
  - `scroll_param`: 滚动参数，用于加载更多商品数据/Scroll parameter, used to load more product 
  - `page_size`: 每页数量/Number per page

### `GET /api/v1/tiktok/app/v3/fetch_shop_product_list`
**获取商家商品列表数据/Get shop product list data**

Parameters:
  - `seller_id`*: 商家id,店铺id/Seller id, shop id
  - `scroll_params`: 滚动参数，用于加载更多商品数据/Scroll parameter, used to load more product 
  - `page_size`: 每页数量/Number per page
  - `sort_field`: 排序字段/Sorting field
  - `sort_order`: 排序方式/Sorting method

### `GET /api/v1/tiktok/app/v3/fetch_shop_product_list_v2`
**获取商家商品列表数据 V2/Get shop product list data V2**

Parameters:
  - `seller_id`*: 商家id,店铺id/Seller id, shop id
  - `scroll_params`: 滚动参数，用于加载更多商品数据/Scroll parameter, used to load more product 
  - `page_size`: 每页数量/Number per page
  - `sort_field`: 排序字段/Sorting field
  - `sort_order`: 排序方式/Sorting method

### `GET /api/v1/tiktok/app/v3/fetch_shop_info`
**获取商家信息数据/Get shop information data**

Parameters:
  - `shop_id`*: 商家id,店铺id/Seller id, shop id

### `GET /api/v1/tiktok/app/v3/fetch_shop_product_category`
**获取商家产品分类数据/Get shop product category data**

Parameters:
  - `seller_id`*: 商家id,店铺id/Seller id, shop id

### `GET /api/v1/tiktok/app/v3/fetch_live_daily_rank`
**获取直播每日榜单数据/Get live daily rank data**

Parameters:
  - `anchor_id`: 主播id/Anchor id
  - `room_id`: 直播间id/Live room id
  - `rank_type`: 榜单类型/Rank type
  - `region_type`: 地区类型/Region type
  - `gap_interval`: 时间间隔/Time interval
  - `cookie`: 用户自己的cookie/User's own cookie

### `GET /api/v1/tiktok/app/v3/fetch_user_music_list`
**获取用户音乐列表数据/Get user music list data**

Parameters:
  - `sec_uid`*: 用户sec_uid/User sec_uid
  - `cursor`: 游标/Cursor
  - `count`: 数量/Number

### `POST /api/v1/tiktok/app/v3/fetch_content_translate`
**获取内容翻译数据/Get content translation data**

### `POST /api/v1/tiktok/app/v3/fetch_home_feed`
**获取主页视频推荐数据/Get home feed(recommend) video data**

### `POST /api/v1/tiktok/app/v3/TTencrypt_algorithm`
**TikTok APP加密算法/TikTok APP encryption algorithm**

### `GET /api/v1/tiktok/app/v3/fetch_live_room_product_list`
**获取直播间商品列表数据/Get live room product list data**

Parameters:
  - `room_id`*: 直播间id/Live room id
  - `author_id`*: 主播id/Anchor id
  - `page_size`: 数量/Number
  - `offset`: 数量/Number
  - `region`: 地区/Region
  - `cookie`: 用户自己的cookie/User's own cookie

### `GET /api/v1/tiktok/app/v3/fetch_live_room_product_list_v2`
**获取直播间商品列表数据 V2 /Get live room product list data V2**

Parameters:
  - `room_id`*: 直播间id/Live room id
  - `author_id`*: 主播id/Anchor id
  - `page_size`: 数量/Number
  - `offset`: 数量/Number
  - `region`: 地区/Region
  - `cookie`: 用户自己的cookie/User's own cookie

### `GET /api/v1/tiktok/app/v3/add_video_play_count`
**根据视频ID来增加作品的播放数/Increase the number of plays of the work according to the video ID**

Parameters:
  - `aweme_type`*: 作品类型/Video type
  - `item_id`*: 作品id/Video id

### `POST /api/v1/tiktok/app/v3/encrypt_decrypt_login_request`
**加密或解密 TikTok APP 登录请求体/Encrypt or Decrypt TikTok APP login request body**

### `GET /api/v1/tiktok/app/v3/open_tiktok_app_to_video_detail`
**生成TikTok分享链接，唤起TikTok APP，跳转指定作品详情页/Generate TikTok share link, call TikTok APP, and jump to the specified video details page**

Parameters:
  - `aweme_id`*: 作品id/Video id

### `GET /api/v1/tiktok/app/v3/open_tiktok_app_to_user_profile`
**生成TikTok分享链接，唤起TikTok APP，跳转指定用户主页/Generate TikTok share link, call TikTok APP, and jump to the specified user profile**

Parameters:
  - `uid`*: 用户id/User id

### `GET /api/v1/tiktok/app/v3/open_tiktok_app_to_keyword_search`
**生成TikTok分享链接，唤起TikTok APP，跳转指定关键词搜索结果/Generate TikTok share link, call TikTok APP, and jump to the specified keyword search result**

Parameters:
  - `keyword`*: 关键词/Keyword

### `GET /api/v1/tiktok/app/v3/open_tiktok_app_to_send_private_message`
**生成TikTok分享链接，唤起TikTok APP，给指定用户发送私信/Generate TikTok share link, call TikTok APP, and send private messages to specified users**

Parameters:
  - `uid`*: 用户id/User id


## /api/v1/tiktok/creator

### `POST /api/v1/tiktok/creator/get_account_health_status`
**获取创作者账号健康状态/Get Creator Account Health Status**

### `POST /api/v1/tiktok/creator/get_account_violation_list`
**获取创作者账号违规记录列表/Get Creator Account Violation Record List**

### `POST /api/v1/tiktok/creator/get_account_insights_overview`
**获取创作者账号概览/Get Creator Account Overview**

### `POST /api/v1/tiktok/creator/get_live_analytics_summary`
**获取创作者直播概览/Get Creator Live Overview**

### `POST /api/v1/tiktok/creator/get_video_analytics_summary`
**获取创作者视频概览/Get Creator Video Overview**

### `POST /api/v1/tiktok/creator/get_video_list_analytics`
**获取创作者视频列表分析/Get Creator Video List Analytics**

### `POST /api/v1/tiktok/creator/get_product_analytics_list`
**获取创作者商品列表分析/Get Creator Product List Analytics**

### `POST /api/v1/tiktok/creator/get_creator_account_info`
**获取创作者账号信息/Get Creator Account Info**

### `POST /api/v1/tiktok/creator/get_showcase_product_list`
**获取橱窗商品列表/Get Showcase Product List**

### `POST /api/v1/tiktok/creator/get_video_associated_product_list`
**获取视频关联商品列表/Get Video Associated Product List**

### `POST /api/v1/tiktok/creator/get_video_detailed_stats`
**获取视频详细分段统计数据/Get Video Detailed Statistics**

### `POST /api/v1/tiktok/creator/get_video_to_product_stats`
**获取视频与商品关联统计数据/Get Video-Product Association Statistics**

### `POST /api/v1/tiktok/creator/get_product_related_videos`
**获取同款商品关联视频/Get Product Related Videos**

### `POST /api/v1/tiktok/creator/get_video_audience_stats`
**获取视频受众分析数据/Get Video Audience Analysis Data**


## /api/v1/tiktok/analytics

### `GET /api/v1/tiktok/analytics/fetch_video_metrics`
**获取作品的统计数据/Get video metrics**

Parameters:
  - `item_id`*: 作品id/Video id

### `GET /api/v1/tiktok/analytics/detect_fake_views`
**检测视频虚假流量分析/Detect fake views in video**

Parameters:
  - `item_id`*: 作品id/Video id
  - `content_category`: 内容分类/Content category, options: default, entertainment, educ

### `GET /api/v1/tiktok/analytics/fetch_comment_keywords`
**获取视频评论关键词分析/Get comment keywords analysis**

Parameters:
  - `item_id`*: 作品id/Video id

### `GET /api/v1/tiktok/analytics/fetch_creator_info_and_milestones`
**获取创作者信息和里程碑数据/Get creator info and milestones**

Parameters:
  - `user_id`*: 用户id/User id


## /api/v1/tiktok/ads

### `GET /api/v1/tiktok/ads/get_ads_detail`
**获取单个广告详情/Get single ad detail**

Parameters:
  - `ads_id`*: 广告ID/Ad ID

### `GET /api/v1/tiktok/ads/search_ads`
**搜索广告/Search ads**

Parameters:
  - `objective`: 广告目标类型/Ad objective (1:流量 2:应用安装 3:转化 4:视频浏览 5:触达 6:潜在客户 7:产
  - `like`: 表现排名/Performance rank (1:前1-20% 2:前21-40% 3:前41-60% 4:前61-80
  - `period`: 时间段/Time period (days)
  - `industry`: 行业ID/Industry ID
  - `keyword`: 搜索关键词/Search keyword
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page
  - `order_by`: 排序方式/Sort by (for_you, likes)
  - `country_code`: 国家代码/Country code
  - `ad_format`: 广告格式/Ad format (1:视频)
  - `ad_language`: 广告语言/Ad language
  - `search_id`: 搜索ID（可选）/Search ID (optional)

### `GET /api/v1/tiktok/ads/get_keyword_insights`
**获取关键词洞察数据/Get keyword insights data**

Parameters:
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page
  - `period`: 时间段（天）/Time period (days, 7/30/120/180)
  - `country_code`: 国家代码/Country code
  - `order_by`: 排序字段/Sort field (post, ctr, click_rate, etc.)
  - `order_type`: 排序方式/Sort order (desc, asc)
  - `industry`: 行业ID/Industry ID
  - `objective`: 广告目标/Ad objective
  - `keyword_type`: 关键词类型/Keyword type
  - `keyword`: 关键词/Keyword

### `GET /api/v1/tiktok/ads/get_top_products`
**获取热门产品列表/Get top products list**

Parameters:
  - `last`: 最近天数/Last days
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page
  - `country_code`: 国家代码/Country code
  - `first_ecom_category_id`: 电商类目ID，多个用逗号分隔/E-commerce category IDs, comma separated
  - `ecom_type`: 电商类型/E-commerce type (l3)
  - `period_type`: 时间类型/Period type (last)
  - `order_by`: 排序字段/Sort field (post, ctr, cvr)
  - `order_type`: 排序方式/Sort order (desc, asc)

### `GET /api/v1/tiktok/ads/get_hashtag_list`
**获取热门标签列表/Get popular hashtags list**

Parameters:
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page
  - `period`: 时间范围（天）/Time period (days)
  - `country_code`: 国家代码/Country code
  - `sort_by`: 排序方式/Sort by (popular, new)
  - `industry_id`: 行业ID/Industry ID
  - `filter_by`: 筛选条件/Filter (new_on_board)

### `GET /api/v1/tiktok/ads/get_sound_rank_list`
**获取热门音乐排行榜/Get popular sound rankings**

Parameters:
  - `period`: 时间范围（天）/Time period (days)
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page
  - `rank_type`: 排行类型/Rank type (popular, surging)
  - `new_on_board`: 是否只看新上榜/Only new on board
  - `commercial_music`: 是否商业音乐/Commercial music only
  - `country_code`: 国家代码/Country code

### `GET /api/v1/tiktok/ads/get_keyword_list`
**获取关键词列表/Get keyword list**

Parameters:
  - `keyword`: 关键词/Keyword
  - `period`: 时间范围（天）/Time period (days)
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page
  - `country_code`: 国家代码/Country code
  - `industry`: 行业ID列表，逗号分隔/Industry IDs, comma separated

### `GET /api/v1/tiktok/ads/get_top_ads_spotlight`
**获取热门广告聚光灯/Get top ads spotlight**

Parameters:
  - `industry`: 行业ID/Industry ID
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page

### `GET /api/v1/tiktok/ads/get_ad_keyframe_analysis`
**获取广告关键帧分析/Get ad keyframe analysis**

Parameters:
  - `material_id`*: 广告素材ID/Ad material ID
  - `metric`: 分析指标/Analysis metric (retain_ctr, retain_cvr, click_cnt, con

### `GET /api/v1/tiktok/ads/get_ad_percentile`
**获取广告百分位数据/Get ad percentile data**

Parameters:
  - `material_id`*: 广告素材ID/Ad material ID
  - `metric`: 分析指标/Analysis metric (ctr_percentile, time_attr_conversion_r
  - `period_type`: 时间范围(天)/Time period (days)

### `GET /api/v1/tiktok/ads/get_ad_interactive_analysis`
**获取广告互动分析/Get ad interactive analysis**

Parameters:
  - `material_id`*: 广告素材ID/Ad material ID
  - `metric_type`: 分析类型/Analysis type (ctr, cvr, clicks, conversion, remain)
  - `period_type`: 时间范围(天)/Period type (days)

### `GET /api/v1/tiktok/ads/get_recommended_ads`
**获取推荐广告/Get recommended ads**

Parameters:
  - `material_id`*: 广告素材ID/Ad material ID
  - `industry`: 行业ID/Industry ID
  - `country_code`: 国家代码/Country code

### `GET /api/v1/tiktok/ads/get_query_suggestions`
**获取查询建议/Get query suggestions**

Parameters:
  - `count`: 建议数量/Suggestion count
  - `scenario`: 场景类型/Scenario type

### `GET /api/v1/tiktok/ads/get_keyword_filters`
**获取关键词筛选器/Get keyword filters**

### `GET /api/v1/tiktok/ads/get_related_keywords`
**获取相关关键词/Get related keywords**

Parameters:
  - `keyword`: 目标关键词/Target keyword
  - `period`: 时间段（天）/Time period (days, 7/30/120)
  - `country_code`: 国家/地区代码/Country code
  - `rank_type`: 排名类型/Rank type (popular: 热门, breakout: 突破性)
  - `content_type`: 内容类型/Content type (keyword, hashtag)
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page

### `GET /api/v1/tiktok/ads/get_keyword_details`
**获取关键词详细信息/Get keyword details**

Parameters:
  - `keyword`: 关键词（可选）/Keyword (optional)
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page
  - `period`: 时间范围（天）/Time period (days)
  - `country_code`: 国家代码/Country code
  - `order_by`: 排序字段/Sort field
  - `order_type`: 排序方式/Sort order (desc, asc)
  - `industry`: 行业ID/Industry ID
  - `objective`: 广告目标/Ad objective
  - `keyword_type`: 关键词类型/Keyword type

### `GET /api/v1/tiktok/ads/get_creative_patterns`
**获取创意模式排行榜/Get creative pattern rankings**

Parameters:
  - `first_industry_id`: 一级行业ID/First industry ID
  - `period_type`: 时间周期类型/Period type (week, month)
  - `order_field`: 排序字段/Order field (ctr, play_over_rate)
  - `order_type`: 排序方式/Sort order (desc, asc)
  - `week`: 特定周（可选）/Specific week (optional)
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page

### `GET /api/v1/tiktok/ads/get_product_filters`
**获取产品筛选器/Get product filters**

### `GET /api/v1/tiktok/ads/get_product_metrics`
**获取产品指标数据/Get product metrics**

Parameters:
  - `id`*: 产品类目ID/Product category ID
  - `last`: 最近天数/Last days
  - `metrics`: 指标类型，逗号分隔/Metrics types, comma separated
  - `ecom_type`: 电商类型/E-commerce type
  - `period_type`: 时间类型/Period type
  - `country_code`: 国家代码/Country code

### `GET /api/v1/tiktok/ads/get_product_detail`
**获取产品详细信息/Get product detail**

Parameters:
  - `id`*: 产品类目ID/Product category ID
  - `last`: 最近天数/Last days
  - `ecom_type`: 电商类型/E-commerce type
  - `period_type`: 时间类型/Period type
  - `country_code`: 国家代码/Country code

### `GET /api/v1/tiktok/ads/get_hashtag_filters`
**获取标签筛选器/Get hashtag filters**

### `GET /api/v1/tiktok/ads/get_hashtag_creator`
**获取标签创作者信息/Get hashtag creator info**

Parameters:
  - `hashtag`*: 标签名称，不包含#符号/Hashtag name (without # symbol)

### `GET /api/v1/tiktok/ads/get_sound_filters`
**获取音乐筛选器/Get sound filters**

Parameters:
  - `rank_type`: 排行类型/Rank type (popular, surging)

### `GET /api/v1/tiktok/ads/get_sound_detail`
**获取音乐详情/Get sound detail**

Parameters:
  - `clip_id`*: 音乐ID/Sound clip ID
  - `period`: 时间范围（天）/Time period (days)
  - `country_code`: 国家代码/Country code

### `GET /api/v1/tiktok/ads/search_sound_hint`
**搜索音乐提示/Search sound hints**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `period`: 时间范围（天）/Time period (days)
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page
  - `rank_type`: 排行类型/Rank type (popular, surging)
  - `country_code`: 国家代码/Country code
  - `filter_by_checked`: 是否只看已验证/Only verified
  - `commercial_music`: 是否商业音乐/Commercial music only

### `GET /api/v1/tiktok/ads/search_sound`
**搜索音乐/Search sounds**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `period`: 时间范围（天）/Time period (days)
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page
  - `rank_type`: 排行类型/Rank type (popular, surging)
  - `new_on_board`: 是否只看新上榜/Only new on board
  - `commercial_music`: 是否商业音乐/Commercial music only
  - `country_code`: 国家代码/Country code

### `GET /api/v1/tiktok/ads/get_sound_recommendations`
**获取音乐推荐/Get sound recommendations**

Parameters:
  - `clip_id`*: 参考音乐ID/Reference sound clip ID
  - `limit`: 推荐数量/Number of recommendations

### `GET /api/v1/tiktok/ads/get_creator_filters`
**获取创作者筛选器/Get creator filters**

### `GET /api/v1/tiktok/ads/get_creator_list`
**获取创作者列表/Get creator list**

Parameters:
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page
  - `sort_by`: 排序方式/Sort by (follower, engagement, avg_views)
  - `creator_country`: 创作者国家/Creator country
  - `audience_country`: 受众国家/Audience country
  - `audience_count`: 受众数量筛选/Audience count filter
  - `keyword`: 关键词/Keyword

### `GET /api/v1/tiktok/ads/search_creators`
**搜索创作者/Search creators**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page
  - `sort_by`: 排序方式/Sort by (follower, avg_views)
  - `creator_country`: 创作者国家/Creator country

### `GET /api/v1/tiktok/ads/get_popular_trends`
**获取流行趋势视频/Get popular trend videos**

Parameters:
  - `period`: 时间范围（天）/Time period (days)
  - `page`: 页码/Page number
  - `limit`: 每页数量/Items per page
  - `order_by`: 排序字段/Order by (vv, like, comment, repost)
  - `country_code`: 国家代码/Country code


## /api/v1/tiktok/shop

### `GET /api/v1/tiktok/shop/web/fetch_product_detail`
**获取商品详情V1(桌面端-数据完整)/Get product detail V1(Full data)**

Parameters:
  - `product_id`*: 商品ID/Product ID
  - `seller_id`: 卖家ID(可选)/Seller ID (optional)
  - `region`: 地区代码/Region code

### `GET /api/v1/tiktok/shop/web/fetch_product_detail_v2`
**获取商品详情V2(移动端-数据少)/Get product detail V2 (Less Data)**

Parameters:
  - `product_id`*: 商品ID/Product ID
  - `seller_id`: 卖家ID(可选)/Seller ID (optional)
  - `region`: 地区代码/Region code

### `GET /api/v1/tiktok/shop/web/fetch_product_detail_v3`
**获取商品详情V3(移动端-数据完整)/Get product detail V3 (Full Data)**

Parameters:
  - `product_id`*: 商品ID/Product ID
  - `region`: 地区代码/Region code

### `GET /api/v1/tiktok/shop/web/fetch_product_reviews_v1`
**获取商品评论V1/Get product reviews V1**

Parameters:
  - `product_id`*: 商品ID/Product ID
  - `sort_type`: 排序方式/Sort type: 1=相关性/Relevance, 2=最新/Recent
  - `filter_id`: 筛选ID/Filter ID
  - `offset`: 分页偏移量/Offset for pagination

### `GET /api/v1/tiktok/shop/web/fetch_product_reviews_v2`
**获取商品评论V2/Get product reviews V2**

Parameters:
  - `product_id`*: 商品ID/Product ID
  - `page_start`: 起始页码/Page start
  - `sort_rule`: 排序规则/Sort rule
  - `filter_type`: 筛选类型/Filter type: 1=默认, 2=有图片/视频, 3=真实购买
  - `filter_value`: 星级筛选/Star filter: 6=全部, 5-1=对应星级
  - `region`: 地区代码/Region code

### `GET /api/v1/tiktok/shop/web/fetch_seller_products_list`
**获取商家商品列表V1/Get seller products list V1**

Parameters:
  - `seller_id`*: 卖家ID/Seller ID
  - `search_params`: 搜索参数(用于分页)/Search params (for pagination)
  - `region`: 地区代码/Region code

### `GET /api/v1/tiktok/shop/web/fetch_seller_products_list_v2`
**获取商家商品列表V2(移动端)/Get seller products list V2 (Mobile)**

Parameters:
  - `seller_id`*: 卖家ID/Seller ID
  - `searchParams`: 搜索参数/Search params
  - `region`: 地区代码/Region code

### `GET /api/v1/tiktok/shop/web/fetch_search_word_suggestion`
**获取搜索关键词建议V1/Get search keyword suggestions V1**

Parameters:
  - `search_word`*: 搜索关键词/Search keyword
  - `lang`: 语言/Language
  - `region`: 地区代码/Region code

### `GET /api/v1/tiktok/shop/web/fetch_search_word_suggestion_v2`
**获取搜索关键词建议V2(移动端)/Get search keyword suggestions V2 (Mobile)**

Parameters:
  - `search_word`*: 搜索关键词/Search keyword
  - `lang`: 语言/Language
  - `region`: 地区代码/Region code

### `GET /api/v1/tiktok/shop/web/fetch_search_products_list`
**搜索商品列表V1/Search products list V1**

Parameters:
  - `search_word`*: 搜索关键词/Search keyword
  - `offset`: 偏移量/Offset
  - `page_token`: 分页标记/Page token
  - `region`: 地区代码/Region code

### `GET /api/v1/tiktok/shop/web/fetch_search_products_list_v2`
**搜索商品列表V2(移动端)/Search products list V2 (Mobile)**

Parameters:
  - `search_word`*: 搜索关键词/Search keyword
  - `offset`: 偏移量/Offset
  - `page_token`: 分页标记/Page token
  - `region`: 地区代码/Region code

### `GET /api/v1/tiktok/shop/web/fetch_search_products_list_v3`
**搜索商品列表V3/Search products list V3**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `offset`: 偏移量/Offset
  - `region`: 地区代码/Region code (Alpha-2)
  - `sort_by`: 排序方式/Sort by: RELEVANCE, PRICE_ASC, PRICE_DESC, BEST_SELLERS
  - `filters_data`: 筛选数据JSON/Filters data JSON

### `GET /api/v1/tiktok/shop/web/fetch_products_category_list`
**获取商品分类列表/Get product category list**

Parameters:
  - `region`: 地区代码/Region code

### `GET /api/v1/tiktok/shop/web/fetch_products_by_category_id`
**根据分类ID获取商品列表/Get products by category ID**

Parameters:
  - `category_id`*: 分类ID/Category ID
  - `offset`: 翻页偏移量/Offset for pagination
  - `region`: 地区代码/Region code

### `GET /api/v1/tiktok/shop/web/fetch_hot_selling_products_list`
**获取热卖商品列表/Get hot selling products list**

Parameters:
  - `region`: 地区代码/Region code
  - `count`: 返回商品数量/Number of products to return
