---
name: clawbrain-pro
description: ClawBrain v1.2 — OpenClaw 的智慧大脑。可靠记忆 + 精准检索 + 来源标注 + 降级透明 + 10 模型智能调度 + 输出验证。205 场景评测第一。
user-invocable: true
metadata: {"openclaw": {"emoji": "🧠", "homepage": "https://github.com/michaelfeng/clawbrain", "requires": {}}}
---

# ClawBrain Pro

给你的 OpenClaw 装上最聪明的大脑。不只是更聪明——会自己想、自己规划、自己记住、越用越懂你。

## 它能帮你做什么

- **复杂任务自动规划**：你说一句话，它拆成步骤按顺序执行
- **10 个 AI 模型智能调度**：简单的事用快模型，难的事用强模型，出错自动切换
- **出错不放弃**：文件找不到自己去翻，命令出错换方法试，搞不定请另一个模型帮忙
- **做事做到底**：多步任务每一步都盯着，不半途而废
- **听得懂模糊的话**：说"帮我准备下"，它知道先查什么再做什么
- **结果自动验证**：独立模型四维评分（准确/完整/逻辑/格式），不合格就重来
- **知识图谱记忆**：跨会话记住你的偏好、项目、决策，越用越懂你
- **记忆更可靠**：长对话内容不再丢失，重要信息不会在句子中间被截断
- **记忆更精准**：搜索人名、工具名等关键词时显示相关度百分比
- **记忆有来源**：清晰区分"你说过的原话"和"AI 归纳的摘要"
- **降级透明**：记忆/搜索不可用时主动告知，不再静默降级
- **身份实时更新**：告诉 AI "我换工作了"，它马上更新
- **长对话不崩溃**：超长对话自动智能截断而非报错
- **兼容 Claude Code**：支持 Anthropic Messages API（/v1/messages）
- **模型健康监控**：实时监控后端模型状态，故障自动熔断切换

## 评测数据（205 场景 × 10 模型）

| 能力 | ClawBrain Auto | ClawBrain Pro | 最好的单模型 |
|------|:---:|:---:|:---:|
| 综合得分 | **90%** | 86% | 83% |
| 错误恢复 | **100%** | 100% | 80% |
| 模糊指令 | **100%** | 100% | 65% |
| 多步任务 | 80% | 80% | 80% |

## 接入方法

```json
{
  "models": {
    "providers": {
      "clawbrain": {
        "baseUrl": "https://api.factorhub.cn/v1",
        "apiKey": "你的 API Key",
        "api": "openai-completions",
        "models": [
          {"id": "clawbrain-auto", "name": "ClawBrain Auto", "input": ["text", "image"], "contextWindow": 128000, "maxTokens": 32768},
          {"id": "clawbrain-pro", "name": "ClawBrain Pro", "input": ["text", "image"], "contextWindow": 64000, "maxTokens": 16384},
          {"id": "clawbrain-max", "name": "ClawBrain Max", "input": ["text", "image"], "contextWindow": 128000, "maxTokens": 32768},
          {"id": "clawbrain-flash", "name": "ClawBrain Flash", "contextWindow": 32000, "maxTokens": 8192}
        ]
      }
    }
  },
  "agents": {"defaults": {"model": {"primary": "clawbrain/clawbrain-auto"}}}
}
```

然后 `openclaw gateway restart`。

## 其他工具

```bash
clawhub install clawbrain-boost            # 一键优化配置 + 记忆 + SOUL
clawhub install clawbrain-pro-benchmark    # 评测你的模型表现
clawhub install clawbrain-pro-doctor       # 诊断配置问题
clawhub install clawbrain-pro-retry        # 出错自动换方案
```

获取 API Key：https://clawbrain.dev/dashboard
