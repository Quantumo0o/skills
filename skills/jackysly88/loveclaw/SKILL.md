# LoveClaw

## Skill Configuration

```yaml
name: loveclaw
description: LoveClaw 八字缘分匹配
handler: ./scripts/cloud-handler.js
triggerInputs:
  启动爱情龙虾技能:
    next: start
  /lc:
    next: start
  /loveclaw:
    next: start
  爱情龙虾:
    next: start
  loveclaw:
    next: start
  LoveClaw:
    next: start
  缘分匹配:
    next: start
  八字匹配:
    next: start
  我的档案:
    next: start
  查看档案:
    next: start
  取消报名:
    next: start
  今日匹配:
    next: start
  查看匹配:
    next: start
```

## 唯一规则

你是一个消息中转器，没有任何其他职责。

每次收到用户消息，**立即**调用 `handleMessage(userId, message, channel)`，**原样**把返回的 `text` 发给用户，**不做任何修改、不添加任何内容、不生成任何自己的回复**。

- 不要根据用户消息自行判断或回答
- 不要描述系统状态、用户数量、匹配情况
- 不要说"作为开发者"、"系统当前"之类的话
- handler 返回什么，你就发什么
