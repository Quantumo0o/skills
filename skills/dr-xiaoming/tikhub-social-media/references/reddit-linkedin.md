# Reddit Linkedin API Reference

Total endpoints: 49


## /api/v1/linkedin/web

### `GET /api/v1/linkedin/web/get_user_profile`
**获取用户资料/Get user profile**

Parameters:
  - `username`*: LinkedIn用户名/LinkedIn username
  - `include_follower_and_connection`: 包含粉丝和连接数（额外消耗1次请求）/Include follower and connection count (+1
  - `include_experiences`: 包含工作经历（额外消耗1次请求）/Include work experiences (+1 request)
  - `include_skills`: 包含技能（额外消耗1次请求）/Include skills (+1 request)
  - `include_certifications`: 包含认证（额外消耗1次请求）/Include certifications (+1 request)
  - `include_publications`: 包含出版物（额外消耗1次请求）/Include publications (+1 request)
  - `include_educations`: 包含教育背景（额外消耗1次请求）/Include educational background (+1 request)
  - `include_volunteers`: 包含志愿者经历（额外消耗1次请求）/Include volunteer experiences (+1 request)
  - `include_honors`: 包含荣誉奖项（额外消耗1次请求）/Include honors and awards (+1 request)
  - `include_interests`: 包含兴趣（额外消耗1次请求）/Include interests (+1 request)
  - `include_bio`: 包含个人简介（额外消耗1次请求）/Include bio/about (+1 request)

### `GET /api/v1/linkedin/web/get_user_posts`
**获取用户帖子/Get user posts**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number
  - `pagination_token`: 分页令牌/Pagination token

### `GET /api/v1/linkedin/web/get_user_comments`
**获取用户评论/Get user comments**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number
  - `pagination_token`: 分页令牌/Pagination token

### `GET /api/v1/linkedin/web/get_user_contact`
**获取用户联系信息/Get user contact information**

Parameters:
  - `username`*: LinkedIn用户名/LinkedIn username

### `GET /api/v1/linkedin/web/get_user_recommendations`
**获取用户推荐信/Get user recommendations**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number
  - `type`: 推荐类型：received(收到的)或given(给出的)/Type: received or given
  - `pagination_token`: 分页令牌/Pagination token

### `GET /api/v1/linkedin/web/get_user_videos`
**获取用户视频/Get user videos**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number
  - `pagination_token`: 分页令牌/Pagination token

### `GET /api/v1/linkedin/web/get_user_images`
**获取用户图片/Get user images**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number
  - `pagination_token`: 分页令牌/Pagination token

### `GET /api/v1/linkedin/web/get_company_profile`
**获取公司资料/Get company profile**

Parameters:
  - `company`: 公司名称/Company name
  - `company_id`: 公司ID（额外消耗1次请求）/Company ID (+1 request)

### `GET /api/v1/linkedin/web/get_company_people`
**获取公司员工/Get company people**

Parameters:
  - `company_id`*: 公司ID/Company ID
  - `page`: 页码/Page number

### `GET /api/v1/linkedin/web/get_company_posts`
**获取公司帖子/Get company posts**

Parameters:
  - `company_id`*: 公司ID/Company ID
  - `page`: 页码/Page number
  - `sort_by`: 排序方式：top(热门)或recent(最新)/Sort by: top or recent

### `GET /api/v1/linkedin/web/get_company_jobs`
**获取公司职位/Get company jobs**

Parameters:
  - `company_id`*: 公司ID/Company ID
  - `page`: 页码/Page number
  - `sort_by`: 排序方式：recent(最新)或relevant(相关)/Sort by: recent or relevant
  - `date_posted`: 发布时间过滤：anytime, past_month, past_week, past_24_hours
  - `experience_level`: 经验级别：internship, entry_level, associate, mid_senior, directo
  - `remote`: 工作地点类型：onsite, remote, hybrid
  - `job_type`: 工作类型：full_time, part_time, contract, temporary, volunteer, i
  - `easy_apply`: 是否易申请/Filter easy apply jobs
  - `under_10_applicants`: 是否少于10个申请者/Filter jobs with under 10 applicants
  - `fair_chance_employer`: 是否公平机会雇主/Filter fair chance employer jobs

### `GET /api/v1/linkedin/web/get_company_job_count`
**获取公司职位数量/Get company job count**

Parameters:
  - `company_id`*: 公司ID/Company ID

### `GET /api/v1/linkedin/web/get_user_about`
**获取用户简介/Get user about**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from

### `GET /api/v1/linkedin/web/get_user_follower_and_connection`
**获取用户粉丝和连接数/Get user follower and connection**

Parameters:
  - `username`*: LinkedIn用户名/LinkedIn username

### `GET /api/v1/linkedin/web/get_user_experience`
**获取用户工作经历/Get user experience**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number

### `GET /api/v1/linkedin/web/get_user_skills`
**获取用户技能/Get user skills**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number

### `GET /api/v1/linkedin/web/get_user_educations`
**获取用户教育背景/Get user educations**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number

### `GET /api/v1/linkedin/web/get_user_publications`
**获取用户出版物/Get user publications**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number

### `GET /api/v1/linkedin/web/get_user_certifications`
**获取用户认证/Get user certifications**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number

### `GET /api/v1/linkedin/web/get_user_honors`
**获取用户荣誉奖项/Get user honors**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number

### `GET /api/v1/linkedin/web/get_user_interests_groups`
**获取用户感兴趣的群组/Get user interests groups**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number

### `GET /api/v1/linkedin/web/get_user_interests_companies`
**获取用户感兴趣的公司/Get user interests companies**

Parameters:
  - `urn`*: 用户URN，可通过get_user_profile接口获取/User URN, can be obtained from
  - `page`: 页码/Page number

### `GET /api/v1/linkedin/web/get_job_detail`
**获取职位详情/Get job detail**

Parameters:
  - `job_id`*: 职位ID/Job ID
  - `include_skills`: 包含职位技能要求（额外消耗1次请求）/Include job skills (+1 request)

### `GET /api/v1/linkedin/web/search_jobs`
**搜索职位/Search jobs**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `page`: 页码/Page number
  - `sort_by`: 排序方式：recent(最新)或relevant(相关)/Sort by: recent or relevant
  - `date_posted`: 发布时间过滤：anytime, past_month, past_week, past_24_hours
  - `geocode`: 地理位置代码，可通过Search Geocode Location获取/Geocode for location
  - `company`: 公司ID过滤/Company ID filter (e.g., 1441 for Google)
  - `experience_level`: 经验级别：internship, entry_level, associate, mid_senior, directo
  - `remote`: 工作地点类型：onsite, remote, hybrid
  - `job_type`: 工作类型：full_time, part_time, contract, temporary, volunteer, i
  - `easy_apply`: 是否易申请/Filter easy apply jobs
  - `has_verifications`: 是否有公司认证/Filter jobs with company verifications
  - `under_10_applicants`: 是否少于10个申请者/Filter jobs with under 10 applicants
  - `fair_chance_employer`: 是否公平机会雇主/Filter fair chance employer jobs

### `GET /api/v1/linkedin/web/search_people`
**搜索用户/Search people**

Parameters:
  - `name`: 搜索关键词/Search keyword for people
  - `first_name`: 名/First name
  - `last_name`: 姓/Last name
  - `title`: 职位/Title
  - `company`: 公司/Company
  - `school`: 学校/School
  - `page`: 页码/Page number
  - `geocode_location`: 地理位置代码/Geocode for location (e.g., 103644278 for United Stat
  - `current_company`: 当前公司ID/Current company ID
  - `profile_language`: 个人资料语言/Profile language
  - `industry`: 行业ID/Industry ID
  - `service_category`: 服务类别ID/Service category ID


## /api/v1/reddit/app

### `GET /api/v1/reddit/app/fetch_home_feed`
**获取Reddit APP首页推荐内容/Fetch Reddit APP Home Feed**

Parameters:
  - `sort`: 排序方式/Sort method: HOT, NEW, TOP, BEST, CONTROVERSIAL
  - `filter_posts`: 过滤掉指定的帖子ID列表/Filter out specified post IDs
  - `after`: 分页参数/Pagination parameter for fetching next page
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_popular_feed`
**获取Reddit APP流行推荐内容/Fetch Reddit APP Popular Feed**

Parameters:
  - `sort`: 排序方式/Sort method: BEST, HOT, NEW, TOP, CONTROVERSIAL, RISING
  - `time`: 时间范围/Time range: ALL, HOUR, DAY, WEEK, MONTH, YEAR
  - `filter_posts`: 过滤帖子ID列表/Filter post IDs
  - `after`: 分页参数/Pagination parameter
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_games_feed`
**获取Reddit APP游戏推荐内容/Fetch Reddit APP Games Feed**

Parameters:
  - `sort`: 排序方式/Sort method: NEW, HOT, TOP, RISING
  - `time`: 时间范围/Time range: ALL, HOUR, DAY, WEEK, MONTH, YEAR
  - `after`: 分页参数/Pagination parameter
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_news_feed`
**获取Reddit APP资讯推荐内容/Fetch Reddit APP News Feed**

Parameters:
  - `subtopic_ids`: 子话题ID列表/Subtopic IDs list
  - `after`: 分页参数/Pagination parameter
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_post_details`
**获取单个Reddit帖子详情/Fetch Single Reddit Post Details**

Parameters:
  - `post_id`*: 帖子ID/Post ID (e.g., t3_1ojnh50)
  - `include_comment_id`: 是否包含特定评论ID/Include specific comment ID
  - `comment_id`: 评论ID/Comment ID (when include_comment_id is True)
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_post_details_batch`
**批量获取Reddit帖子详情(最多5条)/Fetch Reddit Post Details in Batch (Max 5)**

Parameters:
  - `post_ids`*: 帖子ID列表，逗号分隔，最多5条/Post IDs comma-separated, max 5 (e.g., t3_1
  - `include_comment_id`: 是否包含特定评论ID/Include specific comment ID
  - `comment_id`: 评论ID/Comment ID (when include_comment_id is True)
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_post_details_batch_large`
**大批量获取Reddit帖子详情(最多30条)/Fetch Reddit Post Details in Large Batch (Max 30)**

Parameters:
  - `post_ids`*: 帖子ID列表，逗号分隔，最多30条/Post IDs comma-separated, max 30 (e.g., t3
  - `include_comment_id`: 是否包含特定评论ID/Include specific comment ID
  - `comment_id`: 评论ID/Comment ID (when include_comment_id is True)
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_post_comments`
**获取Reddit APP帖子评论/Fetch Reddit APP Post Comments**

Parameters:
  - `post_id`*: 帖子ID/Post ID
  - `sort_type`: 排序方式/Sort method: CONFIDENCE, NEW, TOP, HOT, CONTROVERSIAL, 
  - `after`: 分页参数/Pagination parameter for fetching next page
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_comment_replies`
**获取Reddit APP评论回复（二级评论）/Fetch Reddit APP Comment Replies (Sub-comments)**

Parameters:
  - `post_id`*: 帖子ID/Post ID (e.g., t3_1qmup73)
  - `cursor`*: 评论游标/Comment cursor from more.cursor field (e.g., commenttre
  - `sort_type`: 排序方式/Sort method: CONFIDENCE, NEW, TOP, HOT, CONTROVERSIAL, 
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_subreddit_style`
**获取Reddit APP版块规则样式信息/Fetch Reddit APP Subreddit Rules and Style Info**

Parameters:
  - `subreddit_name`: 版块名称/Subreddit name
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_subreddit_post_channels`
**获取Reddit APP版块帖子频道信息/Fetch Reddit APP Subreddit Post Channels**

Parameters:
  - `subreddit_name`: 版块名称/Subreddit name
  - `sort`: 排序方式/Sort method: HOT, NEW, TOP, CONTROVERSIAL, RISING
  - `range`: 时间范围/Time range: HOUR, DAY, WEEK, MONTH, YEAR, ALL
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_subreddit_info`
**获取Reddit APP版块信息/Fetch Reddit APP Subreddit Info**

Parameters:
  - `subreddit_name`: 版块名称/Subreddit name
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_subreddit_settings`
**获取Reddit APP版块设置/Fetch Reddit APP Subreddit Settings**

Parameters:
  - `subreddit_id`*: 版块ID/Subreddit ID (format: t5_xxxxx)
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_search_typeahead`
**获取Reddit APP搜索自动补全建议/Fetch Reddit APP Search Typeahead Suggestions**

Parameters:
  - `query`*: 搜索关键词/Search query
  - `safe_search`: 安全搜索设置/Safe search setting: unset, strict
  - `allow_nsfw`: 是否允许NSFW内容/Allow NSFW content: 0 or 1
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_dynamic_search`
**获取Reddit APP动态搜索结果/Fetch Reddit APP Dynamic Search Results**

Parameters:
  - `query`*: 搜索关键词/Search query
  - `search_type`: 搜索类型/Search type: post(帖子), community(社区), comment(评论), medi
  - `sort`: 排序方式(仅适用于post/comment/media)/Sort method (only for post/comm
  - `time_range`: 时间范围(仅适用于post/media)/Time range (only for post/media): all(所
  - `safe_search`: 安全搜索设置/Safe search setting: unset, strict
  - `allow_nsfw`: 是否允许NSFW内容/Allow NSFW content: 0, 1
  - `after`: 分页参数/Pagination parameter
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_community_highlights`
**获取Reddit APP社区亮点/Fetch Reddit APP Community Highlights**

Parameters:
  - `subreddit_id`*: 版块ID/Subreddit ID (format: t5_xxxxx)
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_trending_searches`
**获取Reddit APP今日热门搜索/Fetch Reddit APP Trending Searches**

Parameters:
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_user_profile`
**获取Reddit APP用户资料信息/Fetch Reddit APP User Profile**

Parameters:
  - `username`*: 用户名/Username
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_user_active_subreddits`
**获取用户活跃的社区列表/Fetch User's Active Subreddits**

Parameters:
  - `username`*: 用户名/Username
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_user_comments`
**获取用户评论列表/Fetch User Comments**

Parameters:
  - `username`*: 用户名/Username
  - `sort`: 排序方式/Sort method: NEW, TOP, HOT, CONTROVERSIAL
  - `page_size`: 每页数量/Page size (default: 25)
  - `after`: 分页参数/Pagination parameter
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_user_posts`
**获取用户发布的帖子列表/Fetch User Posts**

Parameters:
  - `username`*: 用户名/Username
  - `sort`: 排序方式/Sort method: NEW, TOP, HOT, CONTROVERSIAL
  - `after`: 分页参数/Pagination parameter
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_subreddit_feed`
**获取Reddit APP版块Feed内容/Fetch Reddit APP Subreddit Feed**

Parameters:
  - `subreddit_name`*: 版块名称/Subreddit name
  - `sort`: 排序方式/Sort method: BEST, HOT, NEW, TOP, CONTROVERSIAL, RISING
  - `filter_posts`: 过滤帖子ID列表/Filter post IDs
  - `after`: 分页参数/Pagination parameter
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/check_subreddit_muted`
**检查版块是否静音/Check if Subreddit is Muted**

Parameters:
  - `subreddit_id`*: 版块ID/Subreddit ID (format: t5_xxxxx)
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data

### `GET /api/v1/reddit/app/fetch_user_trophies`
**获取用户公开奖杯/Fetch User Public Trophies**

Parameters:
  - `username`*: 用户名/Username
  - `need_format`: 是否需要清洗数据/Whether to clean and format the data
