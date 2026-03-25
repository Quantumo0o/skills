# Instagram API Reference

Total endpoints: 83


## /api/v1/instagram/v1

### `GET /api/v1/instagram/v1/shortcode_to_media_id`
**Shortcode转Media ID/Convert shortcode to media ID**

Parameters:
  - `shortcode`*: 帖子Shortcode/Post shortcode

### `GET /api/v1/instagram/v1/media_id_to_shortcode`
**Media ID转Shortcode/Convert media ID to shortcode**

Parameters:
  - `media_id`*: 帖子Media ID/Post media ID

### `GET /api/v1/instagram/v1/user_id_to_username`
**用户ID转用户信息/Get user info by user ID**

Parameters:
  - `user_id`*: 用户ID/User ID

### `GET /api/v1/instagram/v1/fetch_user_info_by_username`
**根据用户名获取用户数据/Get user data by username**

Parameters:
  - `username`*: Instagram用户名/Instagram username

### `GET /api/v1/instagram/v1/fetch_user_info_by_username_v2`
**根据用户名获取用户数据V2/Get user data by username V2**

Parameters:
  - `username`*: Instagram用户名/Instagram username

### `GET /api/v1/instagram/v1/fetch_user_info_by_username_v3`
**根据用户名获取用户数据V3/Get user data by username V3**

Parameters:
  - `username`*: Instagram用户名/Instagram username

### `GET /api/v1/instagram/v1/fetch_user_info_by_id`
**根据用户ID获取用户数据/Get user data by user ID**

Parameters:
  - `user_id`*: Instagram用户ID/Instagram user ID

### `GET /api/v1/instagram/v1/fetch_user_info_by_id_v2`
**根据用户ID获取用户数据V2/Get user data by user ID V2**

Parameters:
  - `user_id`*: Instagram用户ID/Instagram user ID

### `GET /api/v1/instagram/v1/fetch_user_about_info`
**获取用户的About信息/Get user about info**

Parameters:
  - `user_id`*: Instagram用户ID/Instagram user ID

### `GET /api/v1/instagram/v1/fetch_user_posts`
**获取用户帖子列表/Get user posts list**

Parameters:
  - `user_id`*: Instagram用户ID/Instagram user ID
  - `count`: 每页数量/Count per page
  - `max_id`: 分页游标，用于获取下一页/Pagination cursor for next page

### `GET /api/v1/instagram/v1/fetch_user_posts_v2`
**获取用户帖子列表V2/Get user posts list V2**

Parameters:
  - `user_id`*: Instagram用户ID/Instagram user ID
  - `count`: 每页数量/Count per page
  - `end_cursor`: 分页游标，用于获取下一页/Pagination cursor for next page

### `GET /api/v1/instagram/v1/fetch_user_reels`
**获取用户Reels列表/Get user Reels list**

Parameters:
  - `user_id`*: Instagram用户ID/Instagram user ID
  - `count`: 每页数量/Count per page
  - `max_id`: 分页游标，用于获取下一页/Pagination cursor for next page

### `GET /api/v1/instagram/v1/fetch_user_reposts`
**获取用户转发列表/Get user reposts list**

Parameters:
  - `user_id`*: Instagram用户ID/Instagram user ID
  - `max_id`: 分页游标，用于获取下一页/Pagination cursor for next page

### `GET /api/v1/instagram/v1/fetch_user_tagged_posts`
**获取用户被标记的帖子/Get user tagged posts**

Parameters:
  - `user_id`*: Instagram用户ID/Instagram user ID
  - `count`: 每页数量/Count per page
  - `end_cursor`: 分页游标，用于获取下一页/Pagination cursor for next page

### `GET /api/v1/instagram/v1/fetch_related_profiles`
**获取相关用户推荐/Get related profiles**

Parameters:
  - `user_id`*: Instagram用户ID/Instagram user ID

### `GET /api/v1/instagram/v1/fetch_search`
**搜索用户/话题/地点/Search users/hashtags/places**

Parameters:
  - `query`*: 搜索关键词/Search keyword
  - `select`: 筛选类型：users/hashtags/places，不传则返回全部/Filter type: users/hashta

### `GET /api/v1/instagram/v1/fetch_post_by_url`
**通过URL获取帖子详情/Get post by URL**

Parameters:
  - `post_url`*: 帖子URL/Post URL

### `GET /api/v1/instagram/v1/fetch_post_by_url_v2`
**通过URL获取帖子详情 V2/Get post by URL V2**

Parameters:
  - `post_url`*: 帖子URL/Post URL

### `GET /api/v1/instagram/v1/fetch_post_by_id`
**通过ID获取帖子详情/Get post by ID**

Parameters:
  - `post_id`*: 帖子ID/Post ID

### `GET /api/v1/instagram/v1/fetch_post_comments_v2`
**获取帖子评论列表V2/Get post comments V2**

Parameters:
  - `media_id`*: 帖子ID（媒体ID）/Post ID (Media ID)
  - `sort_order`: 排序方式：popular(热门)/recent(最新)/Sorting: popular/recent
  - `min_id`: 分页游标，从上一次响应的next_min_id获取/Pagination cursor from previous re

### `GET /api/v1/instagram/v1/fetch_comment_replies`
**获取评论的子评论列表/Get comment replies**

Parameters:
  - `media_id`*: 帖子ID（媒体ID）/Post ID (Media ID)
  - `comment_id`*: 父评论ID/Parent comment ID
  - `min_id`: 分页游标，从上一次响应的next_min_id获取/Pagination cursor from previous re

### `GET /api/v1/instagram/v1/fetch_music_posts`
**获取使用特定音乐的帖子/Get posts using specific music**

Parameters:
  - `music_id`: 音乐ID/Music ID
  - `music_url`: 音乐URL（与music_id二选一）/Music URL (alternative to music_id)
  - `max_id`: 分页游标，用于获取下一页/Pagination cursor for next page

### `GET /api/v1/instagram/v1/fetch_hashtag_posts`
**获取话题标签下的帖子/Get posts by hashtag**

Parameters:
  - `hashtag`*: 话题标签名称（不含#号）/Hashtag name (without #)
  - `end_cursor`: 分页游标，用于获取下一页/Pagination cursor for next page

### `GET /api/v1/instagram/v1/fetch_location_info`
**获取地点信息/Get location info**

Parameters:
  - `location_id`*: 地点ID/Location ID

### `GET /api/v1/instagram/v1/fetch_location_posts`
**获取地点下的帖子/Get posts by location**

Parameters:
  - `location_id`*: 地点ID/Location ID
  - `tab`: 排序方式：ranked(热门)/recent(最新)/Sorting: ranked(top)/recent(lates
  - `end_cursor`: 分页游标，用于获取下一页/Pagination cursor for next page

### `GET /api/v1/instagram/v1/fetch_cities`
**获取国家城市列表/Get cities by country**

Parameters:
  - `country_code`*: 国家代码（如US、CN、JP）/Country code (e.g. US, CN, JP)
  - `page`: 页码/Page number

### `GET /api/v1/instagram/v1/fetch_locations`
**获取城市地点列表/Get locations by city**

Parameters:
  - `city_id`*: 城市ID（从fetch_cities获取）/City ID (from fetch_cities)
  - `page`: 页码/Page number

### `GET /api/v1/instagram/v1/fetch_explore_sections`
**获取探索页面分类/Get explore page sections**

### `GET /api/v1/instagram/v1/fetch_section_posts`
**获取分类下的帖子/Get posts by section**

Parameters:
  - `section_id`*: 分类ID（从fetch_explore_sections获取）/Section ID (from fetch_explo
  - `count`: 每页数量/Count per page
  - `max_id`: 分页游标，用于获取下一页/Pagination cursor for next page


## /api/v1/instagram/v2

### `GET /api/v1/instagram/v2/shortcode_to_media_id`
**Shortcode转Media ID/Convert shortcode to media ID**

Parameters:
  - `shortcode`*: 帖子Shortcode/Post shortcode

### `GET /api/v1/instagram/v2/media_id_to_shortcode`
**Media ID转Shortcode/Convert media ID to shortcode**

Parameters:
  - `media_id`*: 帖子Media ID/Post media ID

### `GET /api/v1/instagram/v2/user_id_to_username`
**用户ID转用户信息/Get user info by user ID**

Parameters:
  - `user_id`*: 用户ID/User ID

### `GET /api/v1/instagram/v2/fetch_user_info`
**获取用户信息/Get user info**

Parameters:
  - `username`: 用户名/Username
  - `user_id`: 用户ID/User ID

### `GET /api/v1/instagram/v2/fetch_user_posts`
**获取用户帖子/Get user posts**

Parameters:
  - `username`: 用户名/Username
  - `user_id`: 用户ID/User ID
  - `pagination_token`: 分页token/Pagination token

### `GET /api/v1/instagram/v2/fetch_user_reels`
**获取用户Reels/Get user reels**

Parameters:
  - `username`: 用户名/Username
  - `user_id`: 用户ID/User ID
  - `pagination_token`: 分页token/Pagination token

### `GET /api/v1/instagram/v2/fetch_user_followers`
**获取用户粉丝/Get user followers**

Parameters:
  - `username`: 用户名/Username
  - `user_id`: 用户ID/User ID
  - `pagination_token`: 分页token/Pagination token

### `GET /api/v1/instagram/v2/fetch_user_following`
**获取用户关注/Get user following**

Parameters:
  - `username`: 用户名/Username
  - `user_id`: 用户ID/User ID
  - `pagination_token`: 分页token/Pagination token

### `GET /api/v1/instagram/v2/fetch_user_stories`
**获取用户故事/Get user stories**

Parameters:
  - `username`: 用户名/Username
  - `user_id`: 用户ID/User ID

### `GET /api/v1/instagram/v2/fetch_user_highlights`
**获取用户精选/Get user highlights**

Parameters:
  - `username`: 用户名/Username
  - `user_id`: 用户ID/User ID

### `GET /api/v1/instagram/v2/fetch_highlight_stories`
**获取精选故事详情/Get highlight stories**

Parameters:
  - `highlight_id`*: 精选ID/Highlight ID

### `GET /api/v1/instagram/v2/fetch_user_tagged_posts`
**获取用户被标记的帖子/Get user tagged posts**

Parameters:
  - `username`: 用户名/Username
  - `user_id`: 用户ID/User ID
  - `pagination_token`: 分页token/Pagination token

### `GET /api/v1/instagram/v2/fetch_similar_users`
**获取相似用户/Get similar users**

Parameters:
  - `username`: 用户名/Username
  - `user_id`: 用户ID/User ID

### `GET /api/v1/instagram/v2/search_users`
**搜索用户/Search users**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword

### `GET /api/v1/instagram/v2/general_search`
**综合搜索/General search**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `pagination_token`: 分页token/Pagination token

### `GET /api/v1/instagram/v2/search_reels`
**搜索Reels/Search reels**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `pagination_token`: 分页token/Pagination token

### `GET /api/v1/instagram/v2/search_music`
**搜索音乐/Search music**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword

### `GET /api/v1/instagram/v2/search_hashtags`
**搜索话题标签/Search hashtags**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword

### `GET /api/v1/instagram/v2/search_locations`
**搜索地点/Search locations**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword

### `GET /api/v1/instagram/v2/search_by_coordinates`
**根据坐标搜索地点/Search locations by coordinates**

Parameters:
  - `latitude`*: 纬度/Latitude
  - `longitude`*: 经度/Longitude

### `GET /api/v1/instagram/v2/fetch_post_info`
**获取帖子详情/Get post info**

Parameters:
  - `code_or_url`*: 帖子Shortcode或URL/Post shortcode or URL

### `GET /api/v1/instagram/v2/fetch_post_likes`
**获取帖子点赞列表/Get post likes**

Parameters:
  - `code_or_url`*: 帖子Shortcode或URL/Post shortcode or URL
  - `end_cursor`: 分页游标/Pagination cursor

### `GET /api/v1/instagram/v2/fetch_post_comments`
**获取帖子评论/Get post comments**

Parameters:
  - `code_or_url`*: 帖子Shortcode或URL/Post shortcode or URL
  - `sort_by`: 排序方式: recent(最新) 或 popular(热门)/Sort by: recent or popular
  - `pagination_token`: 分页token/Pagination token

### `GET /api/v1/instagram/v2/fetch_comment_replies`
**获取评论回复/Get comment replies**

Parameters:
  - `code_or_url`*: 帖子Shortcode或URL/Post shortcode or URL
  - `comment_id`*: 评论ID/Comment ID
  - `pagination_token`: 分页token/Pagination token

### `GET /api/v1/instagram/v2/fetch_music_posts`
**获取音乐帖子/Get music posts**

Parameters:
  - `audio_canonical_id`*: 音频ID/Audio ID
  - `pagination_token`: 分页token/Pagination token

### `GET /api/v1/instagram/v2/fetch_location_posts`
**获取地点帖子/Get location posts**

Parameters:
  - `location_id`*: 地点ID/Location ID
  - `pagination_token`: 分页token/Pagination token

### `GET /api/v1/instagram/v2/fetch_hashtag_posts`
**获取话题帖子/Get hashtag posts**

Parameters:
  - `keyword`*: 话题关键词（不含#号）/Hashtag keyword (without #)
  - `feed_type`: 帖子类型: top(热门), recent(最新), reels(仅Reels)/Feed type: top, rec
  - `pagination_token`: 分页token/Pagination token


## /api/v1/instagram/v3

### `GET /api/v1/instagram/v3/search_users`
**搜索用户/Search users**

Parameters:
  - `query`*: 搜索关键词/Search keyword

### `GET /api/v1/instagram/v3/search_hashtags`
**搜索话题标签/Search hashtags**

Parameters:
  - `query`*: 搜索关键词/Search keyword

### `GET /api/v1/instagram/v3/search_places`
**搜索地点/Search places**

Parameters:
  - `query`*: 搜索关键词/Search keyword

### `GET /api/v1/instagram/v3/general_search`
**综合搜索（支持分页）/General search (with pagination)**

Parameters:
  - `query`*: 搜索关键词/Search keyword
  - `next_max_id`: 分页ID，首次请求不传，从上一次响应的next_max_id获取/Pagination ID, omit for fir
  - `rank_token`: 排序token，首次请求不传，从上一次响应获取/Rank token, omit for first request, 
  - `enable_metadata`: 是否启用元数据/Enable metadata

### `GET /api/v1/instagram/v3/get_user_profile`
**获取用户信息/Get user profile**

Parameters:
  - `user_id`: 用户ID/User ID
  - `username`: 用户名/Username

### `GET /api/v1/instagram/v3/get_user_brief`
**获取用户短详情/Get user brief info**

Parameters:
  - `user_id`*: 用户ID/User ID
  - `username`*: 用户名/Username

### `GET /api/v1/instagram/v3/get_user_posts`
**获取用户帖子列表/Get user posts**

Parameters:
  - `username`: 用户名/Username
  - `user_id`: 用户ID/User ID
  - `first`: 获取帖子数量/Number of posts to fetch
  - `after`: 分页游标（从上次响应的page_info.end_cursor获取）/Pagination cursor (from p

### `GET /api/v1/instagram/v3/get_user_tagged_posts`
**获取用户被标记的帖子/Get user tagged posts**

Parameters:
  - `user_id`: 用户ID/User ID
  - `username`: 用户名/Username
  - `first`: 获取帖子数量/Number of posts to fetch
  - `after`: 分页游标（从上次响应的page_info.end_cursor获取）/Pagination cursor (from p

### `GET /api/v1/instagram/v3/get_user_reels`
**获取用户Reels列表/Get user reels**

Parameters:
  - `user_id`: 用户ID/User ID
  - `username`: 用户名/Username
  - `first`: 获取数量/Number of reels to fetch
  - `after`: 分页游标（从上次响应的page_info.end_cursor获取）/Pagination cursor (from p

### `GET /api/v1/instagram/v3/get_user_highlights`
**获取用户精选Highlights列表/Get user highlights**

Parameters:
  - `user_id`: 用户ID/User ID
  - `username`: 用户名/Username
  - `first`: 获取数量/Number of highlights to fetch
  - `after`: 分页游标（从上次响应的page_info.end_cursor获取）/Pagination cursor (from p

### `GET /api/v1/instagram/v3/get_highlight_stories`
**获取Highlight精选详情/Get highlight stories**

Parameters:
  - `highlight_id`*: 精选ID/Highlight ID (格式/format: highlight:xxx)
  - `reel_ids`: 精选ID列表，逗号分隔，如不提供则仅查询highlight_id/Highlight ID list, comma se

### `GET /api/v1/instagram/v3/get_user_about`
**获取用户账户简介/Get user about info**

Parameters:
  - `user_id`: 用户ID/User ID
  - `username`: 用户名/Username

### `GET /api/v1/instagram/v3/get_user_former_usernames`
**获取用户曾用用户名/Get user former usernames**

Parameters:
  - `user_id`: 用户ID/User ID
  - `username`: 用户名/Username

### `GET /api/v1/instagram/v3/get_user_stories`
**获取用户Stories（快拍）/Get user stories**

Parameters:
  - `user_id`: 用户ID/User ID
  - `username`: 用户名/Username
  - `reel_ids`: 用户ID列表，逗号分隔，可同时获取多个用户的Stories（如不提供则仅查询user_id）/User ID list,

### `GET /api/v1/instagram/v3/get_recommended_reels`
**获取Reels推荐列表/Get recommended Reels feed**

Parameters:
  - `first`: 获取数量/Number of reels to fetch
  - `after`: 分页游标，首次请求不传，从上一次响应的 page_info.end_cursor 获取/Pagination curso

### `GET /api/v1/instagram/v3/get_post_info`
**获取帖子详情/Get post info (media_id or URL)**

Parameters:
  - `media_id`: 帖子媒体ID/Post media ID
  - `url`: 帖子URL/Post URL

### `GET /api/v1/instagram/v3/get_post_info_by_code`
**获取帖子详情(code)/Get post info by shortcode**

Parameters:
  - `code`: 帖子短代码/Post shortcode
  - `url`: 帖子URL（自动提取短代码）/Post URL (auto extract shortcode)

### `GET /api/v1/instagram/v3/get_post_comments`
**获取帖子评论/Get post comments**

Parameters:
  - `media_id`: 帖子媒体ID/Post media ID
  - `code`: 帖子短代码/Post shortcode (e.g., DUajw4YkorV)
  - `url`: 帖子URL/Post URL
  - `min_id`: 分页游标，首次请求不传，从上一次响应的 next_min_id 获取/Pagination cursor, omit f
  - `sort_order`: 排序方式: popular(热门), newest(最新)/Sort order: popular, newest

### `GET /api/v1/instagram/v3/get_comment_replies`
**获取评论的子评论/回复/Get comment replies**

Parameters:
  - `media_id`: 帖子媒体ID/Post media ID
  - `code`: 帖子短代码/Post shortcode
  - `url`: 帖子URL/Post URL
  - `comment_id`*: 父评论ID/Parent comment ID
  - `min_id`: 分页游标，首次请求不传，从上一次响应的 next_min_child_cursor 获取/Pagination curs

### `GET /api/v1/instagram/v3/get_post_oembed`
**获取帖子oEmbed内嵌信息/Get post oEmbed info**

Parameters:
  - `url`*: Instagram帖子的完整URL/Full URL of Instagram post
  - `hidecaption`: 是否隐藏帖子文本/Whether to hide caption
  - `maxwidth`: 最大宽度（像素）/Max width in pixels

### `GET /api/v1/instagram/v3/translate_comment`
**翻译评论/帖子文本/Translate comment or caption**

Parameters:
  - `comment_id`*: 帖子媒体ID/Post media ID

### `GET /api/v1/instagram/v3/bulk_translate_comments`
**批量翻译评论/Bulk translate comments**

Parameters:
  - `comment_ids`*: 评论ID列表，逗号分隔/Comment ID list, comma separated

### `GET /api/v1/instagram/v3/get_explore`
**获取探索页推荐帖子/Get explore feed**

Parameters:
  - `max_id`: 分页游标，首次请求不传，从上一次响应的 next_max_id 获取/Pagination cursor, omit f

### `GET /api/v1/instagram/v3/get_user_following`
**获取用户关注列表/Get user following list**

Parameters:
  - `user_id`: 用户ID/User ID
  - `username`: 用户名/Username
  - `count`: 每次获取数量/Number of users to fetch per request
  - `max_id`: 分页游标，首次请求不传，从上一次响应的 next_max_id 获取/Pagination cursor, omit f

### `GET /api/v1/instagram/v3/get_user_followers`
**获取用户粉丝列表/Get user followers list**

Parameters:
  - `user_id`: 用户ID/User ID
  - `username`: 用户名/Username
  - `count`: 每次获取数量/Number of users to fetch per request
  - `max_id`: 分页游标，首次请求不传，从上一次响应的 next_max_id 获取/Pagination cursor, omit f

### `GET /api/v1/instagram/v3/get_location_info`
**获取地点详情/Get location info**

Parameters:
  - `location_id`*: 地点ID/Location ID
  - `show_nearby`: 是否显示附近地点/Whether to show nearby places

### `GET /api/v1/instagram/v3/get_location_posts`
**获取地点相关帖子/Get location posts**

Parameters:
  - `location_id`*: 地点ID/Location ID
  - `tab`: 帖子类型: ranked(热门), recent(最新)/Post type: ranked(top), recent(
  - `page_size_override`: 每页数量/Page size
