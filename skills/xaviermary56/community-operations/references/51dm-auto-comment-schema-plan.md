# Community Operations - 51dm 自动评论表结构与字段规划

## 1. 目标

基于 51dm 现有内容表结构，规划自动评论系统第一版应读取哪些表、哪些字段，以及评论结果应落到哪些表。

第一版目标：
- 针对站内已有内容自动生成评论
- 优先覆盖：漫画 / 文章 / 视频 / 社区帖子
- 小说能力先预留，待确认实际内容表后接入
- 评论仍走项目原有评论表与审核流

---

## 2. 已确认的主要内容表

## 2.1 漫画内容
表 / Model：
- `books` / `BooksModel`

建议读取字段：
- `id`
- `category_id`
- `category_title`
- `name`
- `description`
- `author`
- `tags`
- `chapter_count`
- `comment_count`
- `view_count`
- `rating`
- `status`
- `is_end`
- `type`
- `created_at`
- `updated_at`

推荐评论输入映射：
- `content_type` = `comic`
- `content_id` = `id`
- `title` = `name`
- `summary` = `description`
- `author` = `author`
- `tags` = `tags`
- `category_id` = `category_id`
- `extra.chapter_count` = `chapter_count`
- `extra.is_end` = `is_end`

---

## 2.2 文章内容
表 / Model：
- `contents` / `ContentsModel`

建议读取字段：
- `id`
- `title`
- `text`
- `aff`
- `tags`
- `type`
- `coins`
- `status`
- `comment_num`
- `view_num`
- `like_num`
- `favorite_num`
- `created_at`
- `updated_at`

推荐评论输入映射：
- `content_type` = `article`
- `content_id` = `id`
- `title` = `title`
- `summary` = `text` 的摘要截断
- `author` = `aff`
- `tags` = `tags`
- `extra.type` = `type`

说明：
- `text` 可能较长，建议先做摘要化，不要直接整段喂给评论生成器。

---

## 2.3 视频内容
表 / Model：
- `mv` / `MvModel`

建议读取字段：
- `id`
- `title`
- `second_title`
- `category_id`
- `category_title`
- `actors`
- `tags`
- `duration`
- `desc`
- `status`
- `count_comment`
- `count_play`
- `count_like`
- `created_at`
- `updated_at`

推荐评论输入映射：
- `content_type` = `video`
- `content_id` = `id`
- `title` = `title`
- `summary` = `desc`
- `tags` = `tags`
- `category_id` = `category_id`
- `extra.second_title` = `second_title`
- `extra.actors` = `actors`
- `extra.duration` = `duration`

---

## 2.4 社区帖子
表 / Model：
- `post` / `PostModel`

建议读取字段：
- `id`
- `topic_id`
- `topics`
- `title`
- `content`
- `aff`
- `status`
- `type`
- `post_type`
- `comment_num`
- `like_num`
- `favorite_num`
- `created_at`
- `updated_at`

推荐评论输入映射：
- `content_type` = `post`
- `content_id` = `id`
- `title` = `title`
- `summary` = `content` 摘要
- `author` = `aff`
- `tags` = `topics`
- `topic_id` = `topic_id`
- `extra.post_type` = `post_type`

---

## 2.5 小说内容
当前已见模型：
- `MemberNovelModel`

但从当前已读信息里，还没有确认它是否就是“可公开评论的小说主内容表”。

因此第一版建议：
- 先把小说作为可扩展内容类型保留
- 等确认小说主表、章节表、评论表后再正式接入

---

## 3. 已确认的评论表

## 3.1 漫画评论
表 / Model：
- `book_comments` / `BookCommentsModel`

字段：
- `id`
- `book_id`
- `aff`
- `parent_id`
- `content`
- `reply_count`
- `like_count`
- `status`
- `created_at`
- `updated_at`

说明：
- `status=0` 未审核
- `status=1` 已审核

---

## 3.2 视频评论
表 / Model：
- `mv_comments` / `MvCommentsModel`

字段：
- `id`
- `mv_id`
- `aff`
- `parent_id`
- `content`
- `reply_count`
- `like_count`
- `status`
- `created_at`
- `updated_at`

说明：
- `status=0` 未审核
- `status=1` 已审核

---

## 3.3 文章评论
表 / Model：
- `contents_comment` / `ContentsCommentModel`

字段：
- `id`
- `cid`
- `pid`
- `aff`
- `comment`
- `status`
- `refuse_reason`
- `is_top`
- `is_finished`
- `like_num`
- `created_at`
- `updated_at`

说明：
- `status=0` 待审核
- `status=1` 已通过
- `status=2` 已拒绝

---

## 3.4 社区评论
表 / Model：
- `post_comment` / `PostCommentModel`

字段建议（基于现有项目链路）：
- `id`
- `post_id`
- `pid`
- `aff`
- `comment`
- `status`
- `refuse_reason`
- `is_top`
- `is_finished`
- `like_num`
- `created_at`
- `updated_at`

说明：
- 当前社区评论已有待审核 / 通过 / 拒绝状态流
- 适合直接复用现有自动审核链路

---

## 4. 账号来源建议

自动评论账号建议优先复用：
- `members` / `MemberModel`

建议至少读取：
- `aff`
- `nickname`
- `status`（如有）
- `lastvisit` / 最近活跃字段（如有）
- `vip_level`（如有）
- `expired_at`（如有）
- `oauth_type` / `oauth_id`（如业务链路需要）

自动评论系统建议额外维护一张独立的“运营账号配置表”，不要直接在 `members` 里硬塞运营状态。

建议独立配置字段：
- `aff`
- `role`
- `enabled`
- `cooldown_until`
- `daily_comment_limit`
- `hourly_comment_limit`
- `last_comment_at`
- `risk_score`

---

## 5. 第一版建议覆盖范围

优先级建议：

### 第一批接入
1. 社区帖子评论（`post` → `post_comment`）
2. 文章评论（`contents` → `contents_comment`）
3. 漫画评论（`books` → `book_comments`）
4. 视频评论（`mv` → `mv_comments`）

### 第二批接入
5. 小说评论（待确认实际主表 / 评论表后接入）

原因：
- 当前这四类内容和评论表结构已较明确
- 已存在现成评论模型和基础审核逻辑
- 更适合做第一版自动评论落地
