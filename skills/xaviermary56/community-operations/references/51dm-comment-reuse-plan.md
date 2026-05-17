# Community Operations - 51dm 各内容类型评论复用方案

## 1. 目标

明确 51dm 在做自动评论时，不同内容类型应优先复用哪一段现有业务逻辑，尽量避免第一版直接写评论表。

原则：
- 优先复用现有业务创建逻辑
- 优先复用现有审核流
- 优先复用现有状态与计数维护
- 尽量不要第一版直写评论表

---

## 2. 社区评论

### 内容链路
- 内容表：`post`
- 评论表：`post_comment`

### 推荐复用点
文件：
- `application/modules/Api/controllers/Community.php`
- `application/library/service/CommunityService.php`

核心方法：
- `CommunityService::createPostComment($member, $id, $content, $cityname)`
- `CommunityService::createComComment($member, $commentId, $content, $cityname)`

### 推荐方案
第一版自动评论直接复用 `CommunityService` 的创建逻辑，不要直接写 `post_comment`。

### 原因
- 已有评论待审核状态
- 已有回复评论逻辑
- 已有现成审核链路
- 已有状态与计数维护语义
- 与当前 post-content-moderation 改造后的链路最一致

### 结论
优先级：**最高**

---

## 3. 图文/文章内容评论（contents）

### 内容链路
- 内容表：`contents`
- 评论表：`contents_comment`

### 推荐复用点
文件：
- `application/modules/Api/controllers/Contents.php`
- `application/library/service/ContentsService.php`

核心方法：
- `ContentsService::createComment($member, $cid, $commentId, $content, $cityname)`

### 推荐方案
第一版自动评论优先复用 `ContentsService::createComment()`，不要直接写 `contents_comment`。

### 原因
- 已有长度限制
- 已有频率控制
- 已有评论次数限制
- 已有关键词/URL/字符过滤
- 已有待审核状态流
- 已有拒绝原因字段

### 结论
优先级：**最高**

---

## 4. 漫画评论

### 内容链路
- 内容表：`books`
- 评论表：`book_comments`

### 当前现有入口
文件：
- `application/modules/Api/controllers/Book.php`

核心方法：
- `BookController::commentAction()`
- `BookController::commentReplyAction()`

### 当前问题
漫画评论创建逻辑目前主要写在 controller 中，还没有单独沉到 service 层。

### 推荐方案
第一版不要直写 `book_comments`。
建议先抽一个轻量 service，例如：
- `BookCommentService`

抽出的逻辑至少包括：
- 校验书籍存在
- 校验评论权限
- 创建评论
- 维护 `books.comment_count`

### 原因
如果自动评论直接自己写表，会复制 controller 逻辑，后续容易分叉。

### 结论
优先级：**中高**
建议：**先抽 service，再接自动评论**

---

## 5. 视频评论

### 内容链路
- 内容表：`mv`
- 评论表：`mv_comments`

### 当前现有入口
文件：
- `application/modules/Api/controllers/Mv.php`

核心方法：
- `MvController::commentAction()`
- `MvController::commentReplyAction()`

### 当前问题
视频评论逻辑也主要在 controller 中，且比漫画多一层事件埋点逻辑。

### 推荐方案
第一版不要直写 `mv_comments`。
建议先抽一个轻量 service，例如：
- `MvCommentService`

抽出的逻辑至少包括：
- 校验视频存在
- 校验评论权限
- 创建评论
- 维护 `mv.count_comment`
- 可选保留事件埋点

### 原因
直写表会绕过现有业务逻辑和埋点逻辑。

### 结论
优先级：**中高**
建议：**先抽 service，再接自动评论**

---

## 6. article 文章评论

### 内容链路
- 内容表：`article`
- 评论表：`comment`

### 当前现有入口
文件：
- `application/modules/Api/controllers/Article.php`

核心方法：
- `ArticleController::commentAction()`

### 当前特点
这条链路额外依赖：
- VIP 校验
- 文章状态校验
- 订阅校验
- 购买校验

### 推荐方案
第一版不优先接。
如果后续要接，也建议先抽 service，再评估自动评论账号如何满足这些权限前置条件。

### 结论
优先级：**较低**
建议：**延后接入**

---

## 7. 第一版推荐接入顺序

### 第一梯队
1. 社区评论（复用 `CommunityService`）
2. 图文/文章内容评论（复用 `ContentsService`）

### 第二梯队
3. 漫画评论（先抽 `BookCommentService`）
4. 视频评论（先抽 `MvCommentService`）

### 第三梯队
5. article 评论（后补）

---

## 8. 研发落地原则

### 直接复用
适用于：
- 社区评论
- contents 评论

### 先抽 service 再复用
适用于：
- 漫画评论
- 视频评论
- article 评论

### 不建议第一版使用
- 自动任务直接写评论表
- 自动任务直接复制 controller 内部逻辑
- 自动任务自己补 comment_count 之类的计数字段

---

## 9. 一句话结论

在 51dm 中做自动评论时：
- **社区 / contents 优先直接复用现有 service**
- **漫画 / 视频先轻量抽 service，再接自动评论**
- **article 评论延后接入**
- **第一版不建议直写评论表**
