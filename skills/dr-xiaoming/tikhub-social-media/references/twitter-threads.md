# Twitter Threads API Reference

Total endpoints: 24


## /api/v1/twitter/web

### `GET /api/v1/twitter/web/fetch_tweet_detail`
**获取单个推文数据/Get single tweet data**

Parameters:
  - `tweet_id`*: 推文ID/Tweet ID

### `GET /api/v1/twitter/web/fetch_user_profile`
**获取用户资料/Get user profile**

Parameters:
  - `screen_name`: 用户名/Screen Name
  - `rest_id`: 用户ID（如果使用用户ID则会忽略用户名）/User ID (If the user ID is used, the u

### `GET /api/v1/twitter/web/fetch_user_post_tweet`
**获取用户发帖/Get user post**

Parameters:
  - `screen_name`: 用户名/Screen Name
  - `rest_id`: 用户ID/User ID
  - `cursor`: 游标/Cursor

### `GET /api/v1/twitter/web/fetch_search_timeline`
**搜索/Search**

Parameters:
  - `keyword`*: 搜索关键字/Search Keyword
  - `search_type`: 搜索类型/Search Type
  - `cursor`: 游标/Cursor

### `GET /api/v1/twitter/web/fetch_post_comments`
**获取评论/Get comments**

Parameters:
  - `tweet_id`*: 推文ID/Tweet ID
  - `cursor`: 游标/Cursor

### `GET /api/v1/twitter/web/fetch_latest_post_comments`
**获取最新的推文评论/Get the latest tweet comments**

Parameters:
  - `tweet_id`*: 推文ID/Tweet ID
  - `cursor`: 游标/Cursor

### `GET /api/v1/twitter/web/fetch_user_tweet_replies`
**获取用户推文回复/Get user tweet replies**

Parameters:
  - `screen_name`*: 用户名/Screen Name
  - `cursor`: 游标/Cursor

### `GET /api/v1/twitter/web/fetch_user_highlights_tweets`
**获取用户高光推文/Get user highlights tweets**

Parameters:
  - `userId`*: 用户ID/User ID
  - `count`: 数量/Count
  - `cursor`: 游标/Cursor

### `GET /api/v1/twitter/web/fetch_user_media`
**获取用户媒体/Get user media**

Parameters:
  - `screen_name`*: 用户名/Screen Name
  - `rest_id`: 用户ID/User ID
  - `cursor`: 翻页游标/Page Cursor

### `GET /api/v1/twitter/web/fetch_retweet_user_list`
**转推用户列表/ReTweet User list**

Parameters:
  - `tweet_id`*: 推文ID/Tweet ID
  - `cursor`: 游标/Cursor

### `GET /api/v1/twitter/web/fetch_trending`
**趋势/Trending**

Parameters:
  - `country`: 国家/Country

### `GET /api/v1/twitter/web/fetch_user_followings`
**用户关注/User Followings**

Parameters:
  - `screen_name`*: 用户名/Screen Name
  - `cursor`: 游标/Cursor

### `GET /api/v1/twitter/web/fetch_user_followers`
**用户粉丝/User Followers**

Parameters:
  - `screen_name`*: 用户名/Screen Name
  - `cursor`: 游标/Cursor


## /api/v1/threads/web

### `GET /api/v1/threads/web/fetch_user_info`
**获取用户信息/Get user info**

Parameters:
  - `username`*: 用户名/Username

### `GET /api/v1/threads/web/fetch_user_info_by_id`
**根据用户ID获取用户信息/Get user info by ID**

Parameters:
  - `user_id`*: 用户ID/User ID

### `GET /api/v1/threads/web/fetch_user_posts`
**获取用户帖子列表/Get user posts**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `end_cursor`: 分页游标/Pagination cursor (optional)

### `GET /api/v1/threads/web/fetch_user_reposts`
**获取用户转发列表/Get user reposts**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `end_cursor`: 分页游标/Pagination cursor (optional)

### `GET /api/v1/threads/web/fetch_user_replies`
**获取用户回复列表/Get user replies**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `end_cursor`: 分页游标/Pagination cursor (optional)

### `GET /api/v1/threads/web/fetch_post_detail`
**获取帖子详情/Get post detail**

Parameters:
  - `post_id`*: 帖子ID/Post ID

### `GET /api/v1/threads/web/fetch_post_detail_v2`
**获取帖子详情 V2(支持链接)/Get post detail V2(supports URL)**

Parameters:
  - `post_id`: 帖子短代码/Post short code
  - `url`: 完整帖子URL/Full post URL

### `GET /api/v1/threads/web/fetch_post_comments`
**获取帖子评论/Get post comments**

Parameters:
  - `post_id`*: 帖子ID/Post ID
  - `end_cursor`: 分页游标/Pagination cursor (optional)

### `GET /api/v1/threads/web/search_top`
**搜索热门内容/Search top content**

Parameters:
  - `query`*: 搜索关键词/Search query
  - `end_cursor`: 分页游标/Pagination cursor (optional)

### `GET /api/v1/threads/web/search_recent`
**搜索最新内容/Search recent content**

Parameters:
  - `query`*: 搜索关键词/Search query
  - `end_cursor`: 分页游标/Pagination cursor (optional)

### `GET /api/v1/threads/web/search_profiles`
**搜索用户档案/Search profiles**

Parameters:
  - `query`*: 搜索关键词/Search query
