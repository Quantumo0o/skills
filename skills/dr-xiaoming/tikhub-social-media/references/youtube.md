# Youtube API Reference

Total endpoints: 37


## /api/v1/youtube/web

### `GET /api/v1/youtube/web/get_video_info`
**获取视频信息 V1/Get video information V1**

Parameters:
  - `video_id`*: 视频ID/Video ID
  - `url_access`: URL访问模式：normal（包含音视频URL）| blocked（不包含音视频URL） / URL access mo
  - `lang`: 语言代码（IETF标签），默认en-US / Language code
  - `videos`: 视频格式：auto（自动）| true（简化格式）| raw（原始格式）| false（不获取） / Video for
  - `audios`: 音频格式：auto（自动）| true（简化格式）| raw（原始格式）| false（不获取） / Audio for
  - `subtitles`: 是否获取字幕 / Include subtitles
  - `related`: 是否获取相关视频 / Include related content

### `GET /api/v1/youtube/web/get_video_info_v2`
**获取视频信息 V2/Get video information V2**

Parameters:
  - `video_id`*: 视频ID/Video ID

### `GET /api/v1/youtube/web/get_video_info_v3`
**获取视频详情 V3/Get video information V3**

Parameters:
  - `video_id`*: 视频ID/Video ID
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code

### `GET /api/v1/youtube/web/get_video_subtitles`
**获取视频字幕/Get video subtitles**

Parameters:
  - `subtitle_url`*: 字幕URL（需先调用获取视频详情接口） / Subtitle URL from video details
  - `format`: 字幕格式：srt/xml/vtt/txt / Subtitle format
  - `fix_overlap`: 修复重叠字幕（默认开启） / Fix overlapping subtitles
  - `target_lang`: 目标语言代码（留空保持原语言） / Target language code

### `GET /api/v1/youtube/web/get_video_comments`
**获取视频评论/Get video comments**

Parameters:
  - `video_id`*: 视频ID/Video ID
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `country_code`: 国家代码（如US, JP等）/Country code
  - `sort_by`: 排序方式 | Sort by
  - `continuation_token`: 翻页令牌/Pagination token
  - `need_format`: 是否需要清洗数据，提取关键内容，移除冗余数据/Whether to clean and format the data

### `GET /api/v1/youtube/web/get_video_comment_replies`
**获取视频二级评论/Get video sub comments**

Parameters:
  - `continuation_token`*: 回复的continuation token（从一级评论的reply_continuation_token字段获取）/Re
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `country_code`: 国家代码（如US, JP等）/Country code
  - `need_format`: 是否需要清洗数据，提取关键内容，移除冗余数据/Whether to clean and format the data

### `GET /api/v1/youtube/web/get_channel_description`
**获取频道描述信息/Get channel description**

Parameters:
  - `channel_id`: 频道ID（格式如：UCeu6U67OzJhV1KwBansH3Dg），可通过get_channel_id_v2接口从频道
  - `continuation_token`: 翻页标志（用于获取频道注册时间等高级信息）/Continuation token for getting advance
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `country_code`: 国家代码（如US, JP等）/Country code
  - `need_format`: 是否需要清洗数据，提取关键内容，移除冗余数据/Whether to clean and format the data

### `GET /api/v1/youtube/web/get_relate_video`
**获取推荐视频/Get related videos**

Parameters:
  - `video_id`*: 视频ID/Video ID
  - `continuation_token`: 翻页令牌/Pagination token

### `GET /api/v1/youtube/web/search_video`
**搜索视频/Search video**

Parameters:
  - `search_query`*: 搜索关键字/Search keyword
  - `language_code`: 语言代码/Language code
  - `order_by`: 排序方式/Order by
  - `country_code`: 国家代码/Country code
  - `continuation_token`: 翻页令牌/Pagination token

### `GET /api/v1/youtube/web/get_general_search`
**综合搜索（支持过滤条件）/General search with filters**

Parameters:
  - `search_query`*: 搜索关键字/Search keyword
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `country_code`: 国家代码（如US, CN等）/Country code
  - `time_zone`: 时区（如America/Los_Angeles, Asia/Shanghai等）/Time zone
  - `upload_time`: 上传时间过滤 | Upload time filter
  - `duration`: 视频时长过滤 | Duration filter
  - `content_type`: 内容类型过滤 | Content type filter
  - `feature`: 特征过滤 | Feature filter
  - `sort_by`: 排序方式 | Sort by
  - `continuation_token`: 翻页令牌/Pagination token

### `GET /api/v1/youtube/web/get_shorts_search`
**YouTube Shorts短视频搜索/YouTube Shorts search**

Parameters:
  - `search_query`*: 搜索关键字/Search keyword
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `country_code`: 国家代码（如US, CN等）/Country code
  - `time_zone`: 时区（如America/Los_Angeles, Asia/Shanghai等）/Time zone
  - `upload_time`: 上传时间过滤 | Upload time filter for Shorts
  - `sort_by`: 排序方式 | Sort by for Shorts
  - `continuation_token`: 翻页令牌/Pagination token
  - `filter_mixed_content`: 是否过滤混合内容（长视频），默认True / Filter mixed content (long videos), d

### `GET /api/v1/youtube/web/get_channel_id`
**获取频道ID/Get channel ID**

Parameters:
  - `channel_name`*: 频道名称/Channel name

### `GET /api/v1/youtube/web/get_channel_id_v2`
**从频道URL获取频道ID V2/Get channel ID from URL V2**

Parameters:
  - `channel_url`*: 频道URL/Channel URL，支持多种格式如：https://www.youtube.com/@username,

### `GET /api/v1/youtube/web/get_channel_url`
**从频道ID获取频道URL/Get channel URL from channel ID**

Parameters:
  - `channel_id`*: 频道ID/Channel ID (格式如：UCeu6U67OzJhV1KwBansH3Dg)

### `GET /api/v1/youtube/web/get_channel_info`
**获取频道信息/Get channel information**

Parameters:
  - `channel_id`*: 频道ID/Channel ID

### `GET /api/v1/youtube/web/get_channel_videos`
**获取频道视频 V1（即将过时，优先使用 V2）/Get channel videos V1 (deprecated soon, use V2 first)**

Parameters:
  - `channel_id`*: 频道ID/Channel ID
  - `continuation_token`: 翻页令牌/Pagination token

### `GET /api/v1/youtube/web/get_channel_videos_v2`
**获取频道视频 V2/Get channel videos V2**

Parameters:
  - `channel_id`*: 频道ID/Channel ID
  - `lang`: 视频结果语言代码/Video result language code
  - `sortBy`: 排序方式/Sort by
  - `contentType`: 内容类型/Content type
  - `nextToken`: 翻页令牌/Pagination token

### `GET /api/v1/youtube/web/get_channel_videos_v3`
**获取频道视频 V3/Get channel videos V3**

Parameters:
  - `channel_id`*: 频道ID/Channel ID
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `country_code`: 国家代码（如US, JP等）/Country code
  - `continuation_token`: 分页token，用于获取下一页/Pagination token for next page
  - `need_format`: 是否需要清洗数据，提取关键内容，移除冗余数据/Whether to clean and format the data

### `GET /api/v1/youtube/web/get_channel_short_videos`
**获取频道短视频/Get channel short videos**

Parameters:
  - `channel_id`*: 频道ID/Channel ID
  - `continuation_token`: 翻页令牌/Pagination token

### `GET /api/v1/youtube/web/search_channel`
**搜索频道/Search channel**

Parameters:
  - `channel_id`*: 频道ID/Channel ID
  - `search_query`*: 搜索关键字/Search keyword
  - `language_code`: 语言代码/Language code
  - `country_code`: 国家代码/Country code
  - `continuation_token`: 翻页令牌/Pagination token

### `GET /api/v1/youtube/web/get_trending_videos`
**获取趋势视频/Get trending videos**

Parameters:
  - `language_code`: 语言代码/Language code
  - `country_code`: 国家代码/Country code
  - `section`: 类型/Section


## /api/v1/youtube/web_v2

### `GET /api/v1/youtube/web_v2/get_video_info`
**获取视频详情 /Get video information**

Parameters:
  - `video_id`*: 视频ID/Video ID
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `need_format`: 是否需要清洗数据，提取关键内容，移除冗余数据/Whether to clean and format the data

### `GET /api/v1/youtube/web_v2/get_video_comments`
**获取视频评论/Get video comments**

Parameters:
  - `video_id`*: 视频ID/Video ID
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `country_code`: 国家代码（如US, JP等）/Country code
  - `sort_by`: 排序方式 | Sort by
  - `continuation_token`: 翻页令牌/Pagination token
  - `need_format`: 是否需要清洗数据，提取关键内容，移除冗余数据/Whether to clean and format the data

### `GET /api/v1/youtube/web_v2/get_video_comment_replies`
**获取视频二级评论/Get video sub comments**

Parameters:
  - `continuation_token`*: 回复的continuation token（从一级评论的reply_continuation_token字段获取）/Re
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `country_code`: 国家代码（如US, JP等）/Country code
  - `need_format`: 是否需要清洗数据，提取关键内容，移除冗余数据/Whether to clean and format the data

### `GET /api/v1/youtube/web_v2/get_channel_description`
**获取频道描述信息/Get channel description**

Parameters:
  - `channel_id`: 频道ID（格式如：UCeu6U67OzJhV1KwBansH3Dg），可通过get_channel_id接口从频道URL
  - `continuation_token`: 翻页标志（用于获取频道注册时间等高级信息）/Continuation token for getting advance
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `country_code`: 国家代码（如US, JP等）/Country code
  - `need_format`: 是否需要清洗数据，提取关键内容，移除冗余数据/Whether to clean and format the data

### `GET /api/v1/youtube/web_v2/get_general_search`
**综合搜索（支持过滤条件）/General search with filters**

Parameters:
  - `search_query`*: 搜索关键字/Search keyword
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `country_code`: 国家代码（如US, CN等）/Country code
  - `time_zone`: 时区（如America/Los_Angeles, Asia/Shanghai等）/Time zone
  - `upload_time`: 上传时间过滤 | Upload time filter
  - `duration`: 视频时长过滤 | Duration filter
  - `content_type`: 内容类型过滤 | Content type filter
  - `feature`: 特征过滤 | Feature filter
  - `sort_by`: 排序方式 | Sort by
  - `continuation_token`: 翻页令牌/Pagination token

### `GET /api/v1/youtube/web_v2/get_shorts_search`
**YouTube Shorts短视频搜索/YouTube Shorts search**

Parameters:
  - `search_query`*: 搜索关键字/Search keyword
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `country_code`: 国家代码（如US, CN等）/Country code
  - `time_zone`: 时区（如America/Los_Angeles, Asia/Shanghai等）/Time zone
  - `upload_time`: 上传时间过滤 | Upload time filter for Shorts
  - `sort_by`: 排序方式 | Sort by for Shorts
  - `continuation_token`: 翻页令牌/Pagination token
  - `filter_mixed_content`: 是否过滤混合内容（长视频），默认True / Filter mixed content (long videos), d

### `GET /api/v1/youtube/web_v2/get_channel_id`
**从频道URL获取频道ID /Get channel ID from URL**

Parameters:
  - `channel_url`*: 频道URL/Channel URL，支持多种格式如：https://www.youtube.com/@username,

### `GET /api/v1/youtube/web_v2/get_channel_url`
**从频道ID获取频道URL/Get channel URL from channel ID**

Parameters:
  - `channel_id`*: 频道ID/Channel ID (格式如：UCeu6U67OzJhV1KwBansH3Dg)

### `GET /api/v1/youtube/web_v2/get_channel_videos`
**获取频道视频 /Get channel videos**

Parameters:
  - `channel_id`*: 频道ID/Channel ID
  - `language_code`: 语言代码（如zh-CN, en-US等）/Language code
  - `country_code`: 国家代码（如US, JP等）/Country code
  - `continuation_token`: 分页token，用于获取下一页/Pagination token for next page
  - `need_format`: 是否需要清洗数据，提取关键内容，移除冗余数据/Whether to clean and format the data

### `GET /api/v1/youtube/web_v2/get_video_streams`
**获取视频流信息/Get video streams info**

Parameters:
  - `video_id`: 视频ID/Video ID
  - `video_url`: 视频URL/Video URL (如果提供video_id则忽略此参数/Ignored if video_id is p

### `GET /api/v1/youtube/web_v2/get_video_streams_v2`
**获取视频流信息 V2/Get video streams info V2**

Parameters:
  - `video_id`: 视频ID/Video ID
  - `video_url`: 视频URL/Video URL (如果提供video_id则忽略此参数/Ignored if video_id is p

### `GET /api/v1/youtube/web_v2/get_signed_stream_url`
**获取已签名的视频流URL/Get signed video stream URL**

Parameters:
  - `video_id`: 视频ID/Video ID
  - `video_url`: 视频URL/Video URL (如果提供video_id则忽略此参数/Ignored if video_id is p
  - `itag`*: 格式标识符 itag (从 get_video_streams 接口获取)/Format identifier itag

### `GET /api/v1/youtube/web_v2/get_related_videos`
**获取视频相似内容/Get related videos**

Parameters:
  - `video_id`: 视频ID/Video ID
  - `video_url`: 视频URL/Video URL (如果提供video_id则忽略此参数/Ignored if video_id is p
  - `need_format`: 是否格式化数据。true: 返回格式化的结构化数据，false: 返回原始API结构/Whether to format

### `GET /api/v1/youtube/web_v2/get_channel_shorts`
**获取频道短视频列表/Get channel shorts**

Parameters:
  - `channel_id`: 频道ID/Channel ID (e.g., UCuAXFkgsw1L7xaCfnd5JJOw)
  - `channel_url`: 频道URL/Channel URL (如果提供channel_id则忽略/Ignored if channel_id i
  - `continuation_token`: 分页token/Pagination token
  - `need_format`: 是否格式化数据/Whether to format data

### `GET /api/v1/youtube/web_v2/get_search_suggestions`
**获取搜索推荐词/Get search suggestions**

Parameters:
  - `keyword`*: 搜索关键词/Search keyword
  - `language`: 语言代码/Language code (e.g., en, zh-cn, ja)
  - `region`: 地区代码/Region code (e.g., US, SG, CN, JP)

### `GET /api/v1/youtube/web_v2/search_channels`
**搜索频道/Search channels**

Parameters:
  - `keyword`: 搜索关键词/Search keyword
  - `continuation_token`: 分页token/Pagination token
  - `need_format`: 是否格式化数据/Whether to format data
