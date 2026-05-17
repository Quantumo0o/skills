# Community Operations - 51dm 自动评论第一版任务拆分

## 1. 目标

将 51dm 自动评论第一版拆成可执行的研发任务，优先覆盖：
- 社区帖子自动评论
- contents 图文内容自动评论

漫画与视频评论作为第二阶段。

---

## 2. 第一版范围

### 本期纳入
- 社区帖子自动评论
- contents 内容自动评论
- 评论生成
- 基础去重
- 账号轮换
- 审核衔接
- 定时触发
- 日志记录

### 本期不纳入
- 自动发帖
- 漫画自动评论
- 视频自动评论
- article 评论
- 评论对话链
- 智能养号
- 复杂 campaign 调度

---

## 3. 模块任务拆分

## 任务 A：目标内容选择器

### A1. 社区帖子候选选择
目标：
- 从 `post` 中选出可评论内容

建议过滤条件：
- 已发布
- 未删除
- 评论数未过高
- 近期未被自动评论过
- 内容文本长度满足最低要求

输出：
- 统一内容结构

### A2. contents 候选选择
目标：
- 从 `contents` 中选出可评论内容

建议过滤条件：
- `status=OK`
- 评论数未过高
- 文本存在
- 近期未被自动评论过

输出：
- 统一内容结构

---

## 任务 B：内容摘要器

### B1. 社区帖子摘要
- 读取 `title + content`
- 对正文做长度截断
- 提取关键词

### B2. contents 摘要
- 读取 `title + text + tags`
- 对 `text` 做摘要化
- 保留标签与风格信息

输出：
```json
{
  "content_type": "post|article",
  "content_id": 123,
  "title": "标题",
  "summary": "摘要",
  "tags": [],
  "extra": {}
}
```

---

## 任务 C：评论生成器

### C1. 风格设计
至少支持：
- praise
- discussion
- question
- expectation
- emotion

### C2. 社区帖子评论生成
- 基于标题/正文生成 3~5 条候选评论
- 偏向轻共鸣、讨论、提问

### C3. contents 评论生成
- 基于标题/摘要/标签生成 3~5 条候选评论
- 偏向观点反馈、体验反馈、轻讨论

### C4. 质量约束
- 评论必须和内容相关
- 评论长度自然分布
- 不允许明显模板化
- 不允许联系方式、引流词、广告词

---

## 任务 D：评论去重与筛选器

### D1. 候选评论去重
- 同一内容下近似评论去重
- 同一任务批次内去重

### D2. 历史评论相似度控制
- 同账号历史评论相似度控制
- 同内容历史自动评论相似度控制

### D3. 低质量评论过滤
过滤：
- 过短无意义评论
- 空泛评论
- 过度重复句式

---

## 任务 E：账号池与账号选择器

### E1. 运营账号配置
建议新增独立配置来源，至少管理：
- aff
- enabled
- role
- daily_limit
- hourly_limit
- cooldown_until
- last_comment_at

### E2. 账号选择规则
- 轮换选择账号
- 过滤冷却中账号
- 过滤达到限额账号
- 支持按内容类型匹配账号风格

### E3. 账号风格映射
建议角色：
- 轻共鸣型
- 讨论型
- 安静型
- 提问型

---

## 任务 F：审核适配

### F1. 社区评论审核衔接
- 复用 `CommunityService` 现有评论链路
- 评论进入现有待审/审核流

### F2. contents 评论审核衔接
- 复用 `ContentsService::createComment()`
- 评论进入现有待审/审核流

### F3. 生成后预审核（可选）
如需前置保护，可在生成后、提交前调用 moderation。

---

## 任务 G：评论提交器

### G1. 社区帖子评论提交
复用：
- `CommunityService::createPostComment()`

### G2. 社区回复评论提交（第二步再做）
复用：
- `CommunityService::createComComment()`

### G3. contents 评论提交
复用：
- `ContentsService::createComment()`

要求：
- 不第一版直写评论表
- 统一返回提交结果
- 统一记录失败原因

---

## 任务 H：日志与审计

建议新增自动评论日志表或统一日志模型，至少记录：
- task_id
- content_type
- content_id
- account_aff
- generated_comment
- final_comment
- strategy
- submit_result
- failure_reason
- created_at

---

## 任务 I：定时任务 / 命令入口

### I1. 社区自动评论命令
例如：
```bash
php cli auto-comment:post 50
```

### I2. contents 自动评论命令
例如：
```bash
php cli auto-comment:contents 50
```

### I3. 汇总命令
例如：
```bash
php cli auto-comment:all 100
```

### I4. 定时任务建议
- 社区评论：5~10 分钟
- contents 评论：10~15 分钟

---

## 4. 实施阶段建议

## Phase 1
- A1 / A2 目标选择器
- B1 / B2 摘要器
- C1~C4 评论生成器
- D1~D3 去重筛选
- E1 / E2 账号池与选择

## Phase 2
- F1 / F2 审核适配
- G1 / G3 评论提交器
- H 日志记录

## Phase 3
- I1~I4 命令与定时任务
- 观察效果
- 调整评论风格、频率、去重策略

---

## 5. 第一版交付标准

满足以下条件即视为第一版可落地：
- 能从社区和 contents 中选出可评论内容
- 能生成多条与内容相关的评论候选
- 能做基础去重和低质量过滤
- 能按账号池轮换评论
- 能复用现有业务逻辑提交评论
- 能进入现有审核流
- 能记录日志
- 能通过 CLI / cron 周期执行
