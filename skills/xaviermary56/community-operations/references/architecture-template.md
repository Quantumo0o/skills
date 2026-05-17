# Community Operations - 架构模板

## 1. 业务目标
- 自动发帖 / 自动评论 / 多账号运营 / 混合

## 2. 账号模型
- account_id
- platform
- role
- status
- cooldown_until
- daily_limit
- hourly_limit
- last_action_at

## 3. 内容模型
- draft_id
- content_type
- title
- body
- medias
- topic_id
- tags
- uniqueness_key

## 4. 任务流
```text
task source
→ select content
→ select account
→ optional moderation
→ publish/comment
→ log result
→ retry/cooldown
```

## 5. 必备控制
- 幂等
- 超时
- 重试上限
- 频控
- 去重
- 审核衔接
- 审计日志
