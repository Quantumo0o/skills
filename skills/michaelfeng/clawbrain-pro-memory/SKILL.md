---
name: clawbrain-pro-memory
description: 教你的龙虾主动管理记忆：自动记录重要信息、定期整理、不再遗忘。适用于长期运行的 OpenClaw Agent。
user-invocable: true
metadata: {"openclaw": {"emoji": "🧠", "requires": {}}}
---

# ClawBrain Memory Manager

让你的龙虾学会"记住"——不只是当前对话，而是跨对话的长期记忆。

## 它解决什么问题

OpenClaw 的对话上下文会不断膨胀，最终被截断或压缩，导致：
- 聊过的事情下次就忘了
- 用户偏好需要反复说明
- 重要决策和关键事实丢失
- 长期运行的 Agent 越用越"笨"

## 安装后你的 Agent 会做什么

### 主动记忆

每次对话中遇到值得记住的内容，自动写入 `memory/当天日期.md`：
- 用户的新偏好和习惯
- 重要决策和结论
- 项目进展和关键事实
- 常用操作模式

### 智能回忆

当你提到之前讨论过的话题时，Agent 会：
1. 搜索 `memory/` 目录下的历史记忆文件
2. 搜索 `memory/archive/` 中的归档记忆
3. 在 workspace 中查找相关文件和数据
4. 基于找到的历史上下文回答

### 长期沉淀

重要信息会从每日记忆逐步沉淀到 `MEMORY.md` 长期记忆文件：
- 用户画像和偏好
- 工作习惯和常用流程
- 项目背景和关键决策

## 使用方法

安装后自动生效。你可以这样触发回忆：
- "你还记得之前我们讨论过XX吗？"
- "找一下上次关于XX的对话"
- "之前那个报告在哪？"

## 配合 ClawBrain 使用效果更佳

ClawBrain 的 `/v1/compress` API 可以在上下文压缩时自动提取记忆信息，实现压缩不丢失关键上下文。

了解更多：https://clawbrain.dev
