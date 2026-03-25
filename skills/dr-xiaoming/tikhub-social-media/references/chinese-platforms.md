# Chinese Platforms API Reference

Total endpoints: 236


## /api/v1/xigua/app

### `GET /api/v1/xigua/app/v2/fetch_one_video`
**获取单个作品数据/Get single video data**

Parameters:
  - `item_id`*: 作品id/Video id

### `GET /api/v1/xigua/app/v2/fetch_one_video_v2`
**获取单个作品数据 V2/Get single video data V2**

Parameters:
  - `item_id`*: 作品id/Video id

### `GET /api/v1/xigua/app/v2/fetch_one_video_play_url`
**获取单个作品的播放链接/Get single video play URL**

Parameters:
  - `item_id`*: 作品id/Video id

### `GET /api/v1/xigua/app/v2/fetch_video_comment_list`
**视频评论列表/Video comment list**

Parameters:
  - `item_id`*: 作品id/Video id
  - `offset`: 偏移量/Offset
  - `count`: 数量/Count

### `GET /api/v1/xigua/app/v2/search_video`
**搜索视频/Search video**

Parameters:
  - `keyword`*: 关键词/Keyword
  - `offset`: 偏移量/Offset
  - `order_type`: 排序方式/Order type
  - `min_duration`: 最小时长/Minimum duration
  - `max_duration`: 最大时长/Maximum duration

### `GET /api/v1/xigua/app/v2/fetch_user_info`
**个人信息/Personal information**

Parameters:
  - `user_id`*: 用户id/User id

### `GET /api/v1/xigua/app/v2/fetch_user_post_list`
**获取个人作品列表/Get user post list**

Parameters:
  - `user_id`*: 用户id/User id
  - `max_behot_time`: 最大行为时间/Maximum behavior time


## /api/v1/toutiao/web

### `GET /api/v1/toutiao/web/get_article_info`
**获取指定文章的信息/Get information of specified article**

Parameters:
  - `aweme_id`*: 作品ID/Post ID

### `GET /api/v1/toutiao/web/get_video_info`
**获取指定视频的信息/Get information of specified video**

Parameters:
  - `aweme_id`*: 作品ID/Post ID


## /api/v1/toutiao/app

### `GET /api/v1/toutiao/app/get_article_info`
**获取指定文章的信息/Get information of specified article**

Parameters:
  - `group_id`*: 作品ID/Post ID

### `GET /api/v1/toutiao/app/get_video_info`
**获取指定视频的信息/Get information of specified video**

Parameters:
  - `group_id`*: 作品ID/Post ID

### `GET /api/v1/toutiao/app/get_comments`
**获取指定作品的评论/Get comments of specified post**

Parameters:
  - `group_id`*: 作品ID/Post ID
  - `offset`*: 偏移量/Offset

### `GET /api/v1/toutiao/app/get_user_info`
**获取指定用户的信息/Get information of specified user**

Parameters:
  - `user_id`*: 用户ID/User ID

### `GET /api/v1/toutiao/app/get_user_id`
**从头条用户主页获取用户user_id/Get user_id from user profile**

Parameters:
  - `user_profile_url`*: 用户主页链接/User profile URL


## /api/v1/lemon8/app

### `GET /api/v1/lemon8/app/fetch_user_profile`
**获取指定用户的信息/Get information of specified user**

Parameters:
  - `user_id`*: 用户ID/User ID

### `GET /api/v1/lemon8/app/fetch_post_detail`
**获取指定作品的信息/Get information of specified post**

Parameters:
  - `item_id`*: 作品ID/Post ID

### `GET /api/v1/lemon8/app/fetch_user_follower_list`
**获取指定用户的粉丝列表/Get fans list of specified user**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `cursor`: 翻页参数/Pagination parameter

### `GET /api/v1/lemon8/app/fetch_user_following_list`
**获取指定用户的关注列表/Get following list of specified user**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `cursor`: 翻页参数/Pagination parameter

### `GET /api/v1/lemon8/app/fetch_post_comment_list`
**获取指定作品的评论列表/Get comments list of specified post**

Parameters:
  - `group_id`*: 作品的group_id/Post's group_id
  - `item_id`*: 作品的item_id/Post's item_id
  - `media_id`*: 作品的media_id/Post's media_id
  - `offset`: 翻页参数/Pagination parameter

### `GET /api/v1/lemon8/app/fetch_discover_banners`
**获取发现页Banner/Get banners of discover page**

### `GET /api/v1/lemon8/app/fetch_discover_tab`
**获取发现页主体内容/Get main content of discover page**

### `GET /api/v1/lemon8/app/fetch_discover_tab_information_tabs`
**获取发现页的 Editor's Picks/Get Editor's Picks of discover page**

### `GET /api/v1/lemon8/app/fetch_hot_search_keywords`
**获取热搜关键词/Get hot search keywords**

### `GET /api/v1/lemon8/app/fetch_topic_info`
**获取话题信息/Get topic information**

Parameters:
  - `forum_id`*: 话题ID/Topic ID

### `GET /api/v1/lemon8/app/fetch_topic_post_list`
**获取话题作品列表/Get topic post list**

Parameters:
  - `category`*: 话题分类 ID/Topic category ID
  - `max_behot_time`: 翻页参数/Pagination parameter
  - `category_parameter`*: 分类参数/Category parameter
  - `hashtag_name`*: Hashtag名称/Hashtag name
  - `sort_type`: 排序方式/Sort type

### `GET /api/v1/lemon8/app/fetch_search`
**搜索接口/Search API**

Parameters:
  - `query`*: 搜索关键词/Search keyword
  - `max_cursor`: 翻页参数/Pagination parameter
  - `filter_type`: 搜索过滤类型/Search filter type
  - `order_by`: 搜索排序方式/Search sort type
  - `search_tab`: 搜索类型/Search type

### `GET /api/v1/lemon8/app/get_item_id`
**通过分享链接获取作品ID/Get post ID through sharing link**

Parameters:
  - `share_text`*: 分享链接/Share link

### `GET /api/v1/lemon8/app/get_user_id`
**通过分享链接获取用户ID/Get user ID through sharing link**

Parameters:
  - `share_text`*: 分享链接/Share link

### `POST /api/v1/lemon8/app/get_item_ids`
**通过分享链接批量获取作品ID/Get post IDs in batch through sharing links**

### `POST /api/v1/lemon8/app/get_user_ids`
**通过分享链接批量获取用户ID/Get user IDs in batch through sharing links**


## /api/v1/kuaishou/web

### `GET /api/v1/kuaishou/web/fetch_one_video`
**获取单个作品数据 V1/Get single video data V1**

Parameters:
  - `share_text`*: 

### `GET /api/v1/kuaishou/web/fetch_one_video_v2`
**获取单个作品数据 V2/Get single video data V2**

Parameters:
  - `photo_id`*: 

### `GET /api/v1/kuaishou/web/fetch_one_video_by_url`
**链接获取作品数据/Fetch single video by URL**

Parameters:
  - `url`*: 

### `GET /api/v1/kuaishou/web/fetch_one_video_comment`
**获取作品一级评论/Fetch video comments**

Parameters:
  - `photo_id`*: 
  - `pcursor`: 

### `GET /api/v1/kuaishou/web/fetch_one_video_sub_comment`
**获取作品二级评论/Fetch video sub comments**

Parameters:
  - `photo_id`*: 
  - `pcursor`: 
  - `root_comment_id`*: 

### `GET /api/v1/kuaishou/web/generate_share_short_url`
**生成分享短连接/Generate share short URL**

Parameters:
  - `photo_id`*: 

### `GET /api/v1/kuaishou/web/fetch_user_info`
**获取用户信息/Fetch user info**

Parameters:
  - `user_id`*: 

### `GET /api/v1/kuaishou/web/fetch_user_post`
**获取用户发布作品/Fetch user posts**

Parameters:
  - `user_id`*: 
  - `pcursor`: 

### `GET /api/v1/kuaishou/web/fetch_user_live_replay`
**获取用户直播回放/Fetch user live replay**

Parameters:
  - `user_id`*: 
  - `pcursor`: 

### `GET /api/v1/kuaishou/web/fetch_user_collect`
**获取用户收藏作品/Fetch user collect**

Parameters:
  - `user_id`*: 
  - `pcursor`: 

### `GET /api/v1/kuaishou/web/fetch_kuaishou_hot_list_v1`
**获取快手热榜 V1/Fetch Kuaishou Hot List V1**

### `GET /api/v1/kuaishou/web/fetch_kuaishou_hot_list_v2`
**获取快手热榜 V2/Fetch Kuaishou Hot List V2**

Parameters:
  - `board_type`: 

### `GET /api/v1/kuaishou/web/fetch_get_user_id`
**获取用户ID/Fetch user ID**

Parameters:
  - `share_link`*: 


## /api/v1/kuaishou/app

### `GET /api/v1/kuaishou/app/fetch_one_video`
**视频详情V1/Video detailsV1**

Parameters:
  - `photo_id`*: 

### `GET /api/v1/kuaishou/app/fetch_videos_batch`
**快手批量视频查询接口/Kuaishou batch video query API**

Parameters:
  - `photo_ids`*: 多个作品ID用逗号分隔，单次最多40个/Multiple photo IDs separated by commas, 

### `GET /api/v1/kuaishou/app/fetch_one_video_by_url`
**根据链接获取单个作品数据/Fetch single video by URL**

Parameters:
  - `share_text`*: 

### `GET /api/v1/kuaishou/app/fetch_one_video_comment`
**获取单个作品评论数据/Get single video comment data**

Parameters:
  - `photo_id`*: 
  - `pcursor`: 

### `GET /api/v1/kuaishou/app/fetch_one_user_v2`
**获取单个用户数据V2/Get single user data V2**

Parameters:
  - `user_id`*: 

### `GET /api/v1/kuaishou/app/fetch_user_live_info`
**获取用户直播信息/Get user live info**

Parameters:
  - `user_id`*: 

### `GET /api/v1/kuaishou/app/fetch_user_hot_post`
**获取用户热门作品数据/Get user hot post data**

Parameters:
  - `user_id`*: 
  - `pcursor`: 

### `GET /api/v1/kuaishou/app/fetch_user_post_v2`
**用户视频列表V2/User video list V2**

Parameters:
  - `user_id`*: 
  - `pcursor`: 

### `GET /api/v1/kuaishou/app/search_comprehensive`
**综合搜索/Comprehensive search**

Parameters:
  - `keyword`*: 
  - `pcursor`: 
  - `sort_type`: 可选值: all(综合排序), newest(最新发布), most_likes(最多点赞)
  - `publish_time`: 可选值: all(全部), one_day(近一日), one_week(近一周), one_month(近一月)
  - `duration`: 可选值: all(全部), under_1_min(1分钟以内), 1_to_5_min(1-5分钟), over_5_
  - `search_scope`: 可选值: all(全部)

### `GET /api/v1/kuaishou/app/search_video_v2`
**搜索视频V2/Search video V2**

Parameters:
  - `keyword`*: 
  - `page`: 

### `GET /api/v1/kuaishou/app/search_user_v2`
**搜索用户V2/Search user V2**

Parameters:
  - `keyword`*: 
  - `page`: 

### `GET /api/v1/kuaishou/app/fetch_hot_board_categories`
**快手热榜分类/Kuaishou hot categories**

### `GET /api/v1/kuaishou/app/fetch_hot_board_detail`
**快手热榜详情/Kuaishou hot board detail**

Parameters:
  - `boardType`: 
  - `boardId`: 

### `GET /api/v1/kuaishou/app/fetch_hot_search_person`
**快手热搜人物榜单/Kuaishou hot search person board**

### `GET /api/v1/kuaishou/app/fetch_live_top_list`
**快手直播榜单/Kuaishou live top list**

Parameters:
  - `subTabId`: 
  - `subTabName`: 

### `GET /api/v1/kuaishou/app/fetch_shopping_top_list`
**快手购物榜单/Kuaishou shopping top list**

Parameters:
  - `subTabId`: 
  - `subTabName`: 

### `GET /api/v1/kuaishou/app/fetch_brand_top_list`
**快手品牌榜单/Kuaishou brand top list**

Parameters:
  - `subTabId`: 
  - `subTabName`: 

### `GET /api/v1/kuaishou/app/generate_kuaishou_share_link`
**生成快手分享链接/Generate Kuaishou share link**

Parameters:
  - `shareObjectId`*: 

### `GET /api/v1/kuaishou/app/fetch_magic_face_usage`
**获取魔法表情使用人数/Fetch magic face usage count**

Parameters:
  - `magic_face_id`*: 

### `GET /api/v1/kuaishou/app/fetch_magic_face_hot`
**获取魔法表情热门视频/Fetch magic face hot videos**

Parameters:
  - `magic_face_id`*: 
  - `pcursor`: 
  - `count`: 


## /api/v1/zhihu/web

### `GET /api/v1/zhihu/web/fetch_column_articles`
**获取知乎专栏文章列表/Get Zhihu Column Articles**

Parameters:
  - `column_id`*: 专栏ID/Column ID
  - `limit`: 每页文章数量/Number of articles per page
  - `offset`: 偏移量/Offset

### `GET /api/v1/zhihu/web/fetch_column_article_detail`
**获取知乎专栏文章详情/Get Zhihu Column Article Detail**

Parameters:
  - `article_id`*: 文章ID/Article ID

### `GET /api/v1/zhihu/web/fetch_column_recommend`
**获取知乎相似专栏推荐/Get Zhihu Similar Column Recommend**

Parameters:
  - `article_id`*: 文章ID/Article ID
  - `limit`: 每页专栏数量/Number of columns per page
  - `offset`: 偏移量/Offset

### `GET /api/v1/zhihu/web/fetch_column_relationship`
**获取知乎专栏文章互动关系/Get Zhihu Column Article Relationship**

Parameters:
  - `article_id`*: 文章ID/Article ID

### `GET /api/v1/zhihu/web/fetch_column_comment_config`
**获取知乎专栏评论区配置/Get Zhihu Column Comment Config**

Parameters:
  - `article_id`*: 文章ID/Article ID

### `GET /api/v1/zhihu/web/fetch_hot_recommend`
**获取知乎首页推荐/Get Zhihu Hot Recommend**

Parameters:
  - `offset`: 偏移量/Offset
  - `page_number`: 页码/Page Number
  - `session_token`: 会话令牌/Session Token

### `GET /api/v1/zhihu/web/fetch_hot_list`
**获取知乎首页热榜/Get Zhihu Hot List**

Parameters:
  - `limit`: 每页文章数量/Number of articles per page
  - `desktop`: 是否为桌面端/Is it a desktop

### `GET /api/v1/zhihu/web/fetch_video_list`
**获取知乎首页视频榜/Get Zhihu Video List**

Parameters:
  - `offset`: 偏移量/Offset
  - `limit`: 每页视频数量/Number of videos per page

### `GET /api/v1/zhihu/web/fetch_article_search_v3`
**获取知乎文章搜索V3/Get Zhihu Article Search V3**

Parameters:
  - `keyword`*: 搜索关键词/Search Keywords
  - `offset`: 偏移量/Offset
  - `limit`: 每页文章数量/Number of articles per page
  - `show_all_topics`: 显示所有主题/Show all topics
  - `search_source`: 搜索来源/Search Source
  - `search_hash_id`: 搜索哈希ID/Search Hash ID
  - `vertical`: 垂类/Vertical Type
  - `sort`: 排序/Sort
  - `time_interval`: 时间间隔/Time Interval
  - `vertical_info`: 垂类信息/Vertical Info

### `GET /api/v1/zhihu/web/fetch_user_search_v3`
**获取知乎用户搜索V3/Get Zhihu User Search V3**

Parameters:
  - `keyword`*: 搜索关键词/Search Keywords
  - `offset`: 偏移量/Offset
  - `limit`: 每页用户数量/Number of users per page

### `GET /api/v1/zhihu/web/fetch_topic_search_v3`
**获取知乎话题搜索V3/Get Zhihu Topic Search V3**

Parameters:
  - `keyword`*: 搜索关键词/Search Keywords
  - `offset`: 偏移量/Offset
  - `limit`: 每页话题数量/Number of topics per page

### `POST /api/v1/zhihu/web/fetch_scholar_search_v3`
**获取知乎论文搜索V3/Get Zhihu Scholar Search V3**

Parameters:
  - `keyword`*: 搜索关键词/Search Keywords
  - `offset`: 偏移量/Offset
  - `limit`: 每页论文数量/Number of papers per page

### `GET /api/v1/zhihu/web/fetch_ai_search`
**获取知乎AI搜索/Get Zhihu AI Search**

Parameters:
  - `message_content`*: 搜索内容/Search Content

### `GET /api/v1/zhihu/web/fetch_ai_search_result`
**获取知乎AI搜索结果/Get Zhihu AI Search Result**

Parameters:
  - `message_id`*: 消息ID/Message ID

### `GET /api/v1/zhihu/web/fetch_video_search_v3`
**获取知乎视频搜索V3/Get Zhihu Video Search V3**

Parameters:
  - `keyword`*: 搜索关键词/Search Keywords
  - `limit`: 每页视频数量/Number of videos per page
  - `offset`: 偏移量/Offset
  - `search_hash_id`: 搜索哈希ID/Search Hash ID

### `GET /api/v1/zhihu/web/fetch_column_search_v3`
**获取知乎专栏搜索V3/Get Zhihu Column Search V3**

Parameters:
  - `keyword`*: 搜索关键词/Search Keywords
  - `offset`: 偏移量/Offset
  - `limit`: 每页专栏数量/Number of columns per page
  - `search_hash_id`: 搜索哈希ID/Search Hash ID

### `GET /api/v1/zhihu/web/fetch_salt_search_v3`
**获取知乎盐选内容搜索V3/Get Zhihu Salt Search V3**

Parameters:
  - `keyword`*: 搜索关键词/Search Keywords
  - `offset`: 偏移量/Offset
  - `limit`: 每页内容数量/Number of contents per page
  - `search_hash_id`: 搜索哈希ID/Search Hash ID

### `GET /api/v1/zhihu/web/fetch_ebook_search_v3`
**获取知乎电子书搜索V3/Get Zhihu Ebook Search V3**

Parameters:
  - `keyword`*: 搜索关键词/Search Keywords
  - `offset`: 偏移量/Offset
  - `limit`: 每页电子书数量/Number of ebooks per page
  - `search_hash_id`: 搜索哈希ID/Search Hash ID

### `GET /api/v1/zhihu/web/fetch_preset_search`
**获取知乎搜索预设词/Get Zhihu Preset Search**

### `GET /api/v1/zhihu/web/fetch_search_recommend`
**获取知乎搜索发现/Get Zhihu Search Recommend**

### `GET /api/v1/zhihu/web/fetch_search_suggest`
**知乎搜索预测词/Get Zhihu Search Suggest**

Parameters:
  - `keyword`*: 搜索关键词/Search Keywords

### `GET /api/v1/zhihu/web/fetch_comment_v5`
**获取知乎评论区V5/Get Zhihu Comment V5**

Parameters:
  - `answer_id`*: 回答ID/Answer ID
  - `order_by`: 排序/Sort
  - `limit`: 每页评论数量/Number of comments per page
  - `offset`: 偏移量/Offset

### `GET /api/v1/zhihu/web/fetch_sub_comment_v5`
**获取知乎子评论区V5/Get Zhihu Sub Comment V5**

Parameters:
  - `comment_id`*: 评论ID/Comment ID
  - `order_by`: 排序/Sort
  - `limit`: 每页评论数量/Number of comments per page
  - `offset`: 偏移量/Offset

### `GET /api/v1/zhihu/web/fetch_user_info`
**获取知乎用户信息/Get Zhihu User Info**

Parameters:
  - `user_url_token`*: 用户ID/User ID

### `GET /api/v1/zhihu/web/fetch_user_followees`
**获取知乎用户关注列表/Get Zhihu User Following**

Parameters:
  - `user_url_token`*: 用户ID/User ID
  - `offset`: 偏移量/Offset
  - `limit`: 每页用户数量/Number of users per page

### `GET /api/v1/zhihu/web/fetch_user_followers`
**获取知乎用户粉丝列表/Get Zhihu User Followers**

Parameters:
  - `user_url_token`*: 用户ID/User ID
  - `offset`: 偏移量/Offset
  - `limit`: 每页用户数量/Number of users per page

### `GET /api/v1/zhihu/web/fetch_user_follow_columns`
**获取知乎用户订阅的专栏/Get Zhihu User Columns**

Parameters:
  - `user_url_token`*: 用户ID/User ID
  - `offset`: 偏移量/Offset
  - `limit`: 每页专栏数量/Number of columns per page

### `GET /api/v1/zhihu/web/fetch_user_follow_questions`
**获取知乎用户关注的问题/Get Zhihu User Follow Questions**

Parameters:
  - `user_url_token`*: 用户ID/User ID
  - `offset`: 偏移量/Offset
  - `limit`: 每页问题数量/Number of questions per page

### `GET /api/v1/zhihu/web/fetch_user_follow_collections`
**获取知乎用户关注的收藏/Get Zhihu User Follow Collections**

Parameters:
  - `user_url_token`*: 用户ID/User ID
  - `offset`: 偏移量/Offset
  - `limit`: 每页收藏数量/Number of collections per page

### `GET /api/v1/zhihu/web/fetch_user_follow_topics`
**获取知乎用户关注的话题/Get Zhihu User Follow Topics**

Parameters:
  - `user_url_token`*: 用户ID/User ID
  - `offset`: 偏移量/Offset
  - `limit`: 每页话题数量/Number of topics per page

### `GET /api/v1/zhihu/web/fetch_recommend_followees`
**获取知乎推荐关注列表/Get Zhihu Recommend Followees**

### `GET /api/v1/zhihu/web/fetch_question_answers`
**获取知乎问题回答列表/Get Zhihu Question Answers**

Parameters:
  - `question_id`*: 问题ID/Question ID
  - `cursor`: 分页游标/Pagination cursor
  - `limit`: 每页回答数量/Number of answers per page
  - `offset`: 偏移量/Offset
  - `order`: 排序方式：default=默认排序，updated=按时间排序/Sort order: default=default 
  - `session_id`: 会话ID/Session ID


## /api/v1/pipixia/app

### `GET /api/v1/pipixia/app/fetch_post_detail`
**获取单个作品数据/Get single video data**

Parameters:
  - `cell_id`*: 作品id/Video id
  - `cell_type`: 作品类型/Video type

### `GET /api/v1/pipixia/app/fetch_increase_post_view_count`
**增加作品浏览数/Increase post view count**

Parameters:
  - `cell_id`*: 作品id/Video id
  - `cell_type`: 作品类型/Video type

### `GET /api/v1/pipixia/app/fetch_post_statistics`
**获取作品统计数据/Get post statistics**

Parameters:
  - `cell_id`*: 作品id/Video id

### `GET /api/v1/pipixia/app/fetch_user_info`
**获取用户信息/Get user information**

Parameters:
  - `user_id`*: 用户id/User id

### `GET /api/v1/pipixia/app/fetch_user_post_list`
**获取用户作品列表/Get user post list**

Parameters:
  - `user_id`*: 用户id/User id
  - `cursor`: 翻页游标/Page cursor
  - `feed_count`: 翻页数量/Page count

### `GET /api/v1/pipixia/app/fetch_user_follower_list`
**获取用户粉丝列表/Get user follower list**

Parameters:
  - `user_id`*: 用户id/User id
  - `cursor`: 翻页游标/Page cursor

### `GET /api/v1/pipixia/app/fetch_user_following_list`
**获取用户关注列表/Get user following list**

Parameters:
  - `user_id`*: 用户id/User id
  - `cursor`: 翻页游标/Page cursor

### `GET /api/v1/pipixia/app/fetch_post_comment_list`
**获取作品评论列表/Get post comment list**

Parameters:
  - `cell_id`*: 作品id/Video id
  - `cell_type`: 作品类型/Video type
  - `offset`: 翻页游标/Page cursor

### `GET /api/v1/pipixia/app/fetch_short_url`
**生成短连接/Generate short URL**

Parameters:
  - `original_url`*: 原始链接/Original URL

### `GET /api/v1/pipixia/app/fetch_home_feed`
**获取首页推荐/Get home feed**

Parameters:
  - `cursor`: 翻页游标/Page cursor

### `GET /api/v1/pipixia/app/fetch_hot_search_words`
**获取热搜词条/Get hot search words**

### `GET /api/v1/pipixia/app/fetch_hot_search_board_list`
**获取热搜榜单列表/Get hot search board list**

### `GET /api/v1/pipixia/app/fetch_hot_search_board_detail`
**获取热搜榜单详情/Get hot search board detail**

Parameters:
  - `block_type`*: 榜单类型/Board type

### `GET /api/v1/pipixia/app/fetch_search`
**搜索接口/Search API**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `offset`: 翻页游标/Page cursor
  - `search_type`: 搜索类型/Search type

### `GET /api/v1/pipixia/app/fetch_hashtag_detail`
**获取话题详情/Get hashtag detail**

Parameters:
  - `hashtag_id`*: 话题id/Hashtag id

### `GET /api/v1/pipixia/app/fetch_hashtag_post_list`
**获取话题作品列表/Get hashtag post list**

Parameters:
  - `hashtag_id`*: 话题id/Hashtag id
  - `cursor`: 翻页游标/Page cursor
  - `feed_count`: 翻页数量/Page count
  - `hashtag_request_type`: 话题请求类型/Hashtag request type
  - `hashtag_sort_type`: 话题排序类型/Hashtag sort type

### `GET /api/v1/pipixia/app/fetch_home_short_drama_feed`
**获取首页短剧推荐/Get home short drama feed**

Parameters:
  - `page`: 页码/Page number


## /api/v1/weibo/web

### `GET /api/v1/weibo/web/fetch_config_list`
**获取频道配置列表/Get channel config list**

### `GET /api/v1/weibo/web/fetch_trend_top`
**获取频道热门趋势/Get channel trend top**

Parameters:
  - `containerid`*: 频道容器ID/Channel container ID
  - `page`: 页码/Page number

### `GET /api/v1/weibo/web/fetch_channel_feed`
**根据频道名称获取热门内容/Get channel feed by name**

Parameters:
  - `channel_name`: 频道名称，不传则使用默认频道/Channel name, use default if not provided
  - `page`: 页码/Page number

### `GET /api/v1/weibo/web/fetch_user_info`
**获取用户信息/Get user information**

Parameters:
  - `uid`*: 用户ID/User ID

### `GET /api/v1/weibo/web/fetch_user_posts`
**获取用户微博列表/Get user posts**

Parameters:
  - `uid`*: 用户ID/User ID
  - `page`: 页码/Page number
  - `since_id`: 翻页ID，从上一页结果获取/Pagination ID from previous page

### `GET /api/v1/weibo/web/fetch_post_detail`
**获取微博详情/Get post detail**

Parameters:
  - `post_id`*: 微博ID/Post ID

### `GET /api/v1/weibo/web/fetch_post_comments`
**获取微博评论/Get post comments**

Parameters:
  - `post_id`*: 微博ID/Post ID
  - `mid`*: 微博MID/Post MID
  - `max_id`: 翻页ID/Pagination ID
  - `max_id_type`: 翻页ID类型/Pagination ID type

### `GET /api/v1/weibo/web/fetch_comment_replies`
**获取评论子评论/Get comment replies**

Parameters:
  - `cid`*: 根评论ID/Root comment ID
  - `max_id`: 翻页ID，默认0为第一页/Pagination ID, default 0 for first page

### `GET /api/v1/weibo/web/fetch_search`
**搜索微博/Search Weibo**

Parameters:
  - `keyword`*: 搜索关键词，支持话题搜索如 #话题名#/Search keyword, supports hashtag like #t
  - `page`: 页码，从1开始递增(1,2,3...)，每页约10-20条/Page number, starts from 1 (1,
  - `search_type`: 搜索类型/Search type: 1=综合, 61=实时, 3=用户, 60=热门, 64=视频, 63=图片, 21
  - `time_scope`: 时间范围/Time scope: hour=一小时内, day=一天内, week=一周内, month=一个月内, n

### `GET /api/v1/weibo/web/fetch_hot_search`
**获取热搜榜/Get hot search ranking**

### `GET /api/v1/weibo/web/fetch_search_topics`
**获取搜索页热搜词/Get search page hot topics**


## /api/v1/weibo/web_v2

### `GET /api/v1/weibo/web_v2/check_allow_comment_with_pic`
**检查微博是否允许带图评论/Check if Weibo allows image comments**

Parameters:
  - `id`*: 微博ID/Weibo ID

### `GET /api/v1/weibo/web_v2/fetch_post_detail`
**获取单个作品数据/Get single post data**

Parameters:
  - `id`*: 作品id/Post id
  - `is_get_long_text`: 是否获取长微博全文/Whether to get the full text of long Weibo posts (

### `GET /api/v1/weibo/web_v2/fetch_user_info`
**获取用户信息/Get user information**

Parameters:
  - `uid`: 用户id/User id
  - `custom`: 自定义微博用户名/Custom Weibo username

### `GET /api/v1/weibo/web_v2/fetch_user_basic_info`
**获取用户基本信息/Get user basic information**

Parameters:
  - `uid`*: 用户id/User id

### `GET /api/v1/weibo/web_v2/fetch_user_posts`
**获取微博用户文章数据/Get Weibo user posts**

Parameters:
  - `uid`*: 用户id/User id
  - `page`: 页数/Page number
  - `feature`: 特征值，控制返回数据的数量和字段：0=返回10条基础数据，1=返回20条扩展数据，2=返回20条图片相关数据，3=返回2
  - `since_id`: 翻页标识，用于获取下一页数据/Pagination identifier for getting next page d

### `GET /api/v1/weibo/web_v2/fetch_user_original_posts`
**获取微博用户原创微博数据/Get Weibo user original posts**

Parameters:
  - `uid`*: 用户id/User id
  - `page`: 页数/Page number
  - `since_id`: 翻页标识，用于获取下一页数据/Pagination identifier for getting next page d

### `GET /api/v1/weibo/web_v2/fetch_post_comments`
**获取微博评论/Get Weibo comments**

Parameters:
  - `id`*: 微博ID/Weibo ID
  - `count`: 评论数量/Number of comments
  - `max_id`: 页码/Page number

### `GET /api/v1/weibo/web_v2/fetch_post_sub_comments`
**获取微博子评论/Get Weibo sub-comments**

Parameters:
  - `id`*: 主评论ID/Comment ID
  - `count`: 子评论数量/Number of sub-comments
  - `max_id`: 分页标识/Page identifier

### `GET /api/v1/weibo/web_v2/search_user_posts`
**搜索用户微博/Search user posts**

Parameters:
  - `uid`*: 用户ID/User ID
  - `q`*: 搜索关键词/Search keyword
  - `page`: 页数/Page number
  - `starttime`*: 开始时间戳/Start timestamp
  - `endtime`*: 结束时间戳/End timestamp
  - `hasori`: 是否包含原创微博，1=包含，0=不包含/Include original posts, 1=include, 0=exc
  - `hasret`: 是否包含转发微博，1=包含，0=不包含/Include retweets, 1=include, 0=exclude
  - `hastext`: 是否包含文字微博，1=包含，0=不包含/Include text posts, 1=include, 0=exclude
  - `haspic`: 是否包含图片微博，1=包含，0=不包含/Include image posts, 1=include, 0=exclud
  - `hasvideo`: 是否包含视频微博，1=包含，0=不包含/Include video posts, 1=include, 0=exclud
  - `hasmusic`: 是否包含音乐微博，1=包含，0=不包含/Include music posts, 1=include, 0=exclud

### `GET /api/v1/weibo/web_v2/fetch_user_video_collection_list`
**获取用户微博视频收藏夹列表/Get user video collection list**

Parameters:
  - `uid`*: 用户ID/User ID

### `GET /api/v1/weibo/web_v2/fetch_user_video_collection_detail`
**获取用户微博视频收藏夹详情/Get user video collection detail**

Parameters:
  - `cid`*: 收藏夹ID/Collection ID
  - `cursor`: 分页游标/Pagination cursor
  - `tab_code`: 排序方式：0=默认，1=最热，2=最新/Sort type: 0=default, 1=hottest, 2=lates

### `GET /api/v1/weibo/web_v2/fetch_user_video_list`
**获取微博用户全部视频/Get user all videos**

Parameters:
  - `uid`*: 用户ID/User ID
  - `cursor`: 分页游标/Pagination cursor

### `GET /api/v1/weibo/web_v2/fetch_user_following`
**获取用户关注列表/Get user following list**

Parameters:
  - `uid`*: 用户ID/User ID
  - `page`: 页码/Page number

### `GET /api/v1/weibo/web_v2/fetch_user_fans`
**获取用户粉丝列表/Get user fans list**

Parameters:
  - `uid`*: 用户ID/User ID
  - `page`: 页码/Page number

### `GET /api/v1/weibo/web_v2/fetch_all_groups`
**获取所有分组信息/Get all groups information**

### `GET /api/v1/weibo/web_v2/fetch_user_recommend_timeline`
**获取微博主页推荐时间轴/Get user recommend timeline**

Parameters:
  - `refresh`: 刷新类型，0=正常刷新，1=强制刷新/Refresh type, 0=normal refresh, 1=force r
  - `group_id`: 分组ID/Group ID
  - `containerid`: 容器ID/Container ID
  - `extparam`: 扩展参数/Extended parameters
  - `max_id`: 最大ID/Max ID
  - `count`: 获取数量/Count

### `GET /api/v1/weibo/web_v2/fetch_hot_ranking_timeline`
**获取微博热门榜单时间轴/Get hot ranking timeline**

Parameters:
  - `ranking_type`*: 榜单类型：hour=小时榜，yesterday=昨日榜，day_before=前日榜，week=周榜，male=男榜，f
  - `since_id`: 分页标识，默认为0/Pagination identifier, default is 0
  - `max_id`: 最大ID，默认为0/Max ID, default is 0
  - `count`: 获取数量，默认10/Count, default is 10

### `GET /api/v1/weibo/web_v2/fetch_hot_search_index`
**获取微博热搜词条(10条)/Get Weibo hot search index (10 items)**

### `GET /api/v1/weibo/web_v2/fetch_hot_search_summary`
**获取微博完整热搜榜单(50条)/Get Weibo complete hot search ranking (50 items)**

### `GET /api/v1/weibo/web_v2/fetch_hot_search`
**获取微博热搜榜单/Get Weibo hot search ranking**

### `GET /api/v1/weibo/web_v2/fetch_entertainment_ranking`
**获取微博文娱榜单/Get Weibo entertainment ranking**

### `GET /api/v1/weibo/web_v2/fetch_life_ranking`
**获取微博生活榜单/Get Weibo life ranking**

### `GET /api/v1/weibo/web_v2/fetch_social_ranking`
**获取微博社会榜单/Get Weibo social ranking**

### `GET /api/v1/weibo/web_v2/fetch_similar_search`
**获取微博相似搜索词推荐/Get Weibo similar search recommendations**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword

### `GET /api/v1/weibo/web_v2/fetch_ai_search`
**微博智能搜索/Weibo AI Search**

Parameters:
  - `query`*: 搜索关键词/Search keyword

### `GET /api/v1/weibo/web_v2/fetch_ai_related_search`
**微博AI搜索内容扩展/Weibo AI Search Content Extension**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword

### `GET /api/v1/weibo/web_v2/fetch_advanced_search`
**微博高级搜索/Weibo Advanced Search**

Parameters:
  - `q`*: 搜索关键词/Search keyword
  - `search_type`: 搜索类型/Search type: all(全部), hot(热门), original(原创), verified(认
  - `include_type`: 包含类型/Include type: all(全部), pic(含图片), video(含视频), music(含音乐)
  - `timescope`: 时间范围/Time scope (custom:start:end)
  - `page`: 页码/Page number

### `GET /api/v1/weibo/web_v2/fetch_city_list`
**地区省市映射/Region City List**

Parameters:
  - `normalized`: 是否返回标准化结构（省份列表+城市数组）/Whether to return normalized structure

### `GET /api/v1/weibo/web_v2/fetch_realtime_search`
**实时搜索/Weibo Realtime Search**

Parameters:
  - `query`*: 搜索关键词/Search keyword
  - `page`: 页码/Page number

### `GET /api/v1/weibo/web_v2/fetch_user_search`
**用户搜索/User search**

Parameters:
  - `query`: 搜索关键词/Query（提供则视为“全部”搜索；留空则仅应用高级筛选参数）
  - `page`: 页码/Page
  - `region`: 地区编码，从 /city_list 获取/Region code from /city_list
  - `auth`: 认证类型 org_vip(机构)/per_vip(个人)/ord(普通)/Auth type
  - `gender`: 性别 man / women / Gender
  - `age`: 年龄段 18y/22y/29y/39y/40y / Age bucket
  - `nickname`: 昵称筛选/Nickname filter
  - `tag`: 标签筛选/Tag filter
  - `school`: 学校筛选/School filter
  - `work`: 公司筛选/Company filter

### `GET /api/v1/weibo/web_v2/fetch_video_search`
**视频搜索（热门/全部）/Weibo video search (hot/all)**

Parameters:
  - `query`*: 搜索关键词/Search keyword
  - `mode`: 搜索模式：hot=热门 / all=全部
  - `page`: 页码/Page number

### `GET /api/v1/weibo/web_v2/fetch_pic_search`
**图片搜索/Weibo picture search**

Parameters:
  - `query`*: 搜索关键词/Search keyword
  - `page`: 页码/Page number

### `GET /api/v1/weibo/web_v2/fetch_topic_search`
**话题搜索/Weibo topic search**

Parameters:
  - `query`*: 搜索关键词/Search keyword
  - `page`: 页码/Page number


## /api/v1/weibo/app

### `GET /api/v1/weibo/app/fetch_user_info`
**获取用户信息/Get user information**

Parameters:
  - `uid`*: 用户ID

### `GET /api/v1/weibo/app/fetch_user_info_detail`
**获取用户详细信息/Get user detail information**

Parameters:
  - `uid`*: 用户ID

### `GET /api/v1/weibo/app/fetch_user_timeline`
**获取用户发布的微博/Get user timeline**

Parameters:
  - `uid`*: 用户ID
  - `page`: 页码
  - `filter_type`: 筛选类型
  - `month`: 时间筛选(YYYYMMDD格式)

### `GET /api/v1/weibo/app/fetch_user_videos`
**获取用户视频列表/Get user videos**

Parameters:
  - `uid`*: 用户ID
  - `since_id`: 翻页游标

### `GET /api/v1/weibo/app/fetch_user_super_topics`
**获取用户参与的超话列表/Get user super topics**

Parameters:
  - `uid`*: 用户ID
  - `page`: 页码

### `GET /api/v1/weibo/app/fetch_user_album`
**获取用户相册/Get user album**

Parameters:
  - `uid`*: 用户ID
  - `since_id`: 翻页游标

### `GET /api/v1/weibo/app/fetch_user_articles`
**获取用户文章列表/Get user articles**

Parameters:
  - `uid`*: 用户ID
  - `since_id`: 翻页游标

### `GET /api/v1/weibo/app/fetch_user_audios`
**获取用户音频列表/Get user audios**

Parameters:
  - `uid`*: 用户ID
  - `since_id`: 翻页游标

### `GET /api/v1/weibo/app/fetch_user_profile_feed`
**获取用户主页动态/Get user profile feed**

Parameters:
  - `uid`*: 用户ID
  - `since_id`: 翻页游标

### `GET /api/v1/weibo/app/fetch_status_detail`
**获取微博详情/Get post detail**

Parameters:
  - `status_id`*: 微博ID

### `GET /api/v1/weibo/app/fetch_status_comments`
**获取微博评论/Get post comments**

Parameters:
  - `status_id`*: 微博ID
  - `max_id`: 翻页游标
  - `sort_type`: 排序类型: 0=按热度排序, 1=按时间排序

### `GET /api/v1/weibo/app/fetch_status_reposts`
**获取微博转发列表/Get post reposts**

Parameters:
  - `status_id`*: 微博ID
  - `max_id`: 翻页游标

### `GET /api/v1/weibo/app/fetch_status_likes`
**获取微博点赞列表/Get post likes**

Parameters:
  - `status_id`*: 微博ID
  - `attitude_type`: 点赞类型: 0=全部, 1=点赞, 2=开心, 3=惊讶, 4=伤心, 5=愤怒, 6=打赏, 8=抱抱

### `GET /api/v1/weibo/app/fetch_video_detail`
**获取视频详情/Get video detail**

Parameters:
  - `mid`*: 视频微博ID

### `GET /api/v1/weibo/app/fetch_video_featured_feed`
**获取短视频精选Feed流/Get video featured feed**

Parameters:
  - `page`: 页码，首页不传，第二页传2

### `GET /api/v1/weibo/app/fetch_search_all`
**综合搜索/Comprehensive search**

Parameters:
  - `query`*: 搜索关键词
  - `page`: 页码
  - `search_type`: 搜索类型: 1=综合, 61=实时, 3=用户, 64=视频, 63=图片, 62=关注, 60=热门, 21=全网, 

### `GET /api/v1/weibo/app/fetch_ai_smart_search`
**AI智搜/AI Smart Search**

Parameters:
  - `query`*: 搜索关键词
  - `page`: 页码

### `GET /api/v1/weibo/app/fetch_home_recommend_feed`
**获取首页推荐Feed流/Get home recommend feed**

Parameters:
  - `page`: 页码，首页不传，第二页传2
  - `count`: 每页数量

### `GET /api/v1/weibo/app/fetch_hot_search`
**获取热搜榜/Get hot search**

Parameters:
  - `category`: 热搜分类: mineband=我的, realtimehot=热搜, social=社会, fun=文娱, techno
  - `page`: 页码
  - `count`: 每页数量
  - `region_name`: 同城热搜城市名称，仅 category=region 时有效，支持: 北京/上海/广州/深圳/杭州/成都/重庆/武汉/南

### `GET /api/v1/weibo/app/fetch_hot_search_categories`
**获取热搜分类列表/Get hot search categories**


## /api/v1/wechat_mp/web

### `GET /api/v1/wechat_mp/web/fetch_mp_article_detail_json`
**获取微信公众号文章详情的JSON/Get Wechat MP Article Detail JSON**

Parameters:
  - `url`*: 文章链接/Article URL

### `GET /api/v1/wechat_mp/web/fetch_mp_article_detail_html`
**获取微信公众号文章详情的HTML/Get Wechat MP Article Detail HTML**

Parameters:
  - `url`*: 文章链接/Article URL

### `GET /api/v1/wechat_mp/web/fetch_mp_article_list`
**获取微信公众号文章列表/Get Wechat MP Article List**

Parameters:
  - `ghid`*: 公众号ID/MP ID
  - `offset`: 偏移量/Offset

### `GET /api/v1/wechat_mp/web/fetch_mp_article_read_count`
**获取微信公众号文章阅读量/Get Wechat MP Article Read Count**

Parameters:
  - `url`*: 文章链接/Article URL
  - `comment_id`*: 评论ID/Comment ID

### `GET /api/v1/wechat_mp/web/fetch_mp_article_url`
**获取微信公众号文章永久链接/Get Wechat MP Article URL**

Parameters:
  - `sogou_url`*: 搜狗链接/Sogou URL

### `GET /api/v1/wechat_mp/web/fetch_mp_article_comment_list`
**获取微信公众号文章评论列表/Get Wechat MP Article Comment List**

Parameters:
  - `url`*: 文章链接/Article URL
  - `comment_id`: 评论ID/Comment ID
  - `buffer`: 偏移量/Offset

### `GET /api/v1/wechat_mp/web/fetch_mp_article_comment_reply_list`
**获取微信公众号文章评论回复列表/Get Wechat MP Article Comment Reply List**

Parameters:
  - `url`: 文章链接/Article URL
  - `comment_id`*: 评论ID/Comment ID
  - `content_id`*: 内容ID/Content ID
  - `offset`: 偏移量/Offset

### `GET /api/v1/wechat_mp/web/fetch_mp_article_ad`
**获取微信公众号广告/Get Wechat MP Article Ad**

Parameters:
  - `url`*: 文章链接/Article URL

### `GET /api/v1/wechat_mp/web/fetch_mp_article_url_conversion`
**获取微信公众号长链接转短链接/Get Wechat MP Long URL to Short URL**

Parameters:
  - `url`*: 文章链接/Article URL

### `GET /api/v1/wechat_mp/web/fetch_mp_related_articles`
**获取微信公众号关联文章/Get Wechat MP Related Articles**

Parameters:
  - `url`*: 文章链接/Article URL


## /api/v1/wechat_channels/fetch_default_search

### `POST /api/v1/wechat_channels/fetch_default_search`
**微信视频号默认搜索/WeChat Channels Default Search**


## /api/v1/wechat_channels/fetch_search_latest

### `GET /api/v1/wechat_channels/fetch_search_latest`
**微信视频号搜索最新视频/WeChat Channels Search Latest Videos**

Parameters:
  - `keywords`*: 搜索关键词/Search keywords


## /api/v1/wechat_channels/fetch_search_ordinary

### `GET /api/v1/wechat_channels/fetch_search_ordinary`
**微信视频号综合搜索/WeChat Channels Comprehensive Search**

Parameters:
  - `keywords`*: 搜索关键词/Search keywords


## /api/v1/wechat_channels/fetch_user_search

### `GET /api/v1/wechat_channels/fetch_user_search`
**微信视频号用户搜索/WeChat Channels User Search**

Parameters:
  - `keywords`*: 搜索关键词/Search keywords
  - `page`: 页码/Page number


## /api/v1/wechat_channels/fetch_video_detail

### `GET /api/v1/wechat_channels/fetch_video_detail`
**微信视频号视频详情/WeChat Channels Video Detail**

Parameters:
  - `id`: 视频ID/Video ID
  - `exportId`: 导出ID会过期，优先用视频ID，使用时可不传id/Export ID may expire, prefer to use


## /api/v1/wechat_channels/fetch_home_page

### `POST /api/v1/wechat_channels/fetch_home_page`
**微信视频号主页/WeChat Channels Home Page**


## /api/v1/wechat_channels/fetch_comments

### `POST /api/v1/wechat_channels/fetch_comments`
**微信视频号评论/WeChat Channels Comments**


## /api/v1/wechat_channels/fetch_live_history

### `GET /api/v1/wechat_channels/fetch_live_history`
**微信视频号直播回放/WeChat Channels Live History**

Parameters:
  - `username`*: 用户名/Username


## /api/v1/wechat_channels/fetch_hot_words

### `GET /api/v1/wechat_channels/fetch_hot_words`
**微信视频号热门话题/WeChat Channels Hot Topics**


## /api/v1/bilibili/web

### `GET /api/v1/bilibili/web/fetch_one_video`
**获取单个视频详情信息/Get single video data**

Parameters:
  - `bv_id`*: 作品id/Video id

### `GET /api/v1/bilibili/web/fetch_one_video_v2`
**获取单个视频详情信息V2/Get single video data V2**

Parameters:
  - `a_id`*: 作品id/Video id
  - `c_id`*: 作品cid/Video cid

### `GET /api/v1/bilibili/web/fetch_one_video_v3`
**获取单个视频详情信息V3/Get single video data V3**

Parameters:
  - `url`*: 视频链接/Video URL

### `GET /api/v1/bilibili/web/fetch_video_detail`
**获取单个视频详情/Get single video detail**

Parameters:
  - `aid`*: 作品id/Video id

### `GET /api/v1/bilibili/web/fetch_video_play_info`
**获取单个视频播放信息/Get single video play info**

Parameters:
  - `url`*: 视频链接/Video URL

### `GET /api/v1/bilibili/web/fetch_video_subtitle`
**获取视频字幕信息/Get video subtitle info**

Parameters:
  - `a_id`*: 作品id/Video id
  - `c_id`*: 作品cid/Video cid

### `GET /api/v1/bilibili/web/fetch_hot_search`
**获取热门搜索信息/Get hot search data**

Parameters:
  - `limit`*: 返回数量/Return number

### `GET /api/v1/bilibili/web/fetch_general_search`
**获取综合搜索信息/Get general search data**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `order`*: 排序方式/Order method
  - `page`*: 页码/Page number
  - `page_size`*: 每页数量/Number per page
  - `duration`: 时长筛选/Duration filter
  - `pubtime_begin_s`: 开始日期/Start date (10-digit timestamp)
  - `pubtime_end_s`: 结束日期/End date (10-digit timestamp)

### `GET /api/v1/bilibili/web/fetch_video_playurl`
**获取视频流地址/Get video playurl**

Parameters:
  - `bv_id`*: 作品id/Video id
  - `cid`*: 作品cid/Video cid

### `POST /api/v1/bilibili/web/fetch_vip_video_playurl`
**获取大会员清晰度视频流地址/Get VIP video playurl**

### `GET /api/v1/bilibili/web/fetch_user_post_videos`
**获取用户主页作品数据/Get user homepage video data**

Parameters:
  - `uid`*: 用户UID
  - `pn`: 页码/Page number
  - `order`: 排序方式/Order method

### `GET /api/v1/bilibili/web/fetch_collect_folders`
**获取用户所有收藏夹信息/Get user collection folders**

Parameters:
  - `uid`*: 用户UID

### `GET /api/v1/bilibili/web/fetch_user_collection_videos`
**获取指定收藏夹内视频数据/Gets video data from a collection folder**

Parameters:
  - `folder_id`*: 收藏夹id/collection folder id
  - `pn`: 页码/Page number

### `GET /api/v1/bilibili/web/fetch_user_profile`
**获取指定用户的信息/Get information of specified user**

Parameters:
  - `uid`*: 用户UID

### `GET /api/v1/bilibili/web/fetch_user_up_stat`
**获取UP主状态统计/Get UP stat (total likes and views)**

Parameters:
  - `uid`*: 用户UID/User UID

### `GET /api/v1/bilibili/web/fetch_user_relation_stat`
**获取用户关系状态统计/Get user relation stat (following and followers)**

Parameters:
  - `uid`*: 用户UID/User UID

### `GET /api/v1/bilibili/web/fetch_com_popular`
**获取综合热门视频信息/Get comprehensive popular video information**

Parameters:
  - `pn`: 页码/Page number

### `GET /api/v1/bilibili/web/fetch_video_comments`
**获取指定视频的评论/Get comments on the specified video**

Parameters:
  - `bv_id`*: 作品id/Video id
  - `pn`: 页码/Page number

### `GET /api/v1/bilibili/web/fetch_comment_reply`
**获取视频下指定评论的回复/Get reply to the specified comment**

Parameters:
  - `bv_id`*: 作品id/Video id
  - `pn`: 页码/Page number
  - `rpid`*: 回复id/Reply id

### `GET /api/v1/bilibili/web/fetch_user_dynamic`
**获取指定用户动态/Get dynamic information of specified user**

Parameters:
  - `uid`*: 用户UID
  - `offset`: 开始索引/offset

### `GET /api/v1/bilibili/web/fetch_dynamic_detail`
**获取动态详情/Get dynamic detail**

Parameters:
  - `dynamic_id`*: 动态id/Dynamic id

### `GET /api/v1/bilibili/web/fetch_dynamic_detail_v2`
**获取动态详情v2/Get dynamic detail v2**

Parameters:
  - `dynamic_id`*: 动态id/Dynamic id

### `GET /api/v1/bilibili/web/fetch_video_danmaku`
**获取视频实时弹幕/Get Video Danmaku**

Parameters:
  - `cid`*: 作品cid/Video cid

### `GET /api/v1/bilibili/web/fetch_live_room_detail`
**获取指定直播间信息/Get information of specified live room**

Parameters:
  - `room_id`*: 直播间ID/Live room ID

### `GET /api/v1/bilibili/web/fetch_live_videos`
**获取直播间视频流/Get live video data of specified room**

Parameters:
  - `room_id`*: 直播间ID/Live room ID

### `GET /api/v1/bilibili/web/fetch_live_streamers`
**获取指定分区正在直播的主播/Get live streamers of specified live area**

Parameters:
  - `area_id`*: 直播分区id/Live area ID
  - `pn`: 页码/Page number

### `GET /api/v1/bilibili/web/fetch_all_live_areas`
**获取所有直播分区列表/Get a list of all live areas**

### `GET /api/v1/bilibili/web/bv_to_aid`
**通过bv号获得视频aid号/Generate aid by bvid**

Parameters:
  - `bv_id`*: 作品id/Video id

### `GET /api/v1/bilibili/web/fetch_video_parts`
**通过bv号获得视频分p信息/Get Video Parts By bvid**

Parameters:
  - `bv_id`*: 作品id/Video id

### `GET /api/v1/bilibili/web/fetch_get_user_id`
**提取用户ID/Extract user ID**

Parameters:
  - `share_link`*: 用户分享链接/User share link


## /api/v1/bilibili/app

### `GET /api/v1/bilibili/app/fetch_one_video`
**获取单个视频详情信息/Get single video data**

Parameters:
  - `av_id`: AV号/AV ID
  - `bv_id`: BV号/BV ID

### `GET /api/v1/bilibili/app/fetch_video_comments`
**获取视频评论列表/Get video comments**

Parameters:
  - `av_id`: AV号/AV ID
  - `bv_id`: BV号/BV ID
  - `mode`: 排序模式/Sort mode (3=热门/hot, 2=时间/time)
  - `next_offset`: 分页游标/Pagination cursor

### `GET /api/v1/bilibili/app/fetch_reply_detail`
**获取二级评论回复/Get reply detail**

Parameters:
  - `root`*: 一级评论ID/Root comment ID
  - `av_id`: AV号/AV ID
  - `bv_id`: BV号/BV ID
  - `next_offset`: 下一页游标/Next page cursor
  - `ps`: 每页数量/Page size

### `GET /api/v1/bilibili/app/fetch_user_videos`
**获取用户投稿视频/Get user videos**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `post_filter`: 过滤类型/Filter type (archive/season/contribute)
  - `page`: 页码/Page number
  - `ps`: 每页数量/Page size

### `GET /api/v1/bilibili/app/fetch_user_info`
**获取用户信息/Get user info**

Parameters:
  - `user_id`*: 用户ID/User ID

### `GET /api/v1/bilibili/app/fetch_home_feed`
**获取主页推荐视频流/Get home feed**

Parameters:
  - `idx`: 页面索引/Page index
  - `flush`: 刷新标记/Flush flag (0=普通加载, 1=刷新)
  - `pull`: 是否下拉刷新/Pull to refresh

### `GET /api/v1/bilibili/app/fetch_popular_feed`
**获取热门推荐/Get popular feed**

Parameters:
  - `idx`: 页面索引/Page index
  - `last_param`: 上一页最后一个视频ID/Last video ID

### `GET /api/v1/bilibili/app/fetch_search_all`
**综合搜索/search all**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `page`: 页码/Page number
  - `page_size`: 每页数量/Page size
  - `order`: 排序方式/Sort order (0=综合排序)

### `GET /api/v1/bilibili/app/fetch_search_by_type`
**分类搜索/ search by type**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `search_type`: 搜索类型/Search type (video/bangumi/pgc/live/article/user)
  - `page`: 页码/Page number
  - `page_size`: 每页数量/Page size
  - `order`: 排序方式/Sort order (0=综合, 1=最新, 2=播放量, 3=弹幕数)

### `GET /api/v1/bilibili/app/fetch_cinema_tab`
**获取影视推荐/Get cinema tab**

### `GET /api/v1/bilibili/app/fetch_bangumi_tab`
**获取番剧推荐/Get bangumi tab**
