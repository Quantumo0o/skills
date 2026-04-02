---
name: skill-perf
description: "测量 OpenClaw 环境中 Skill 的 token 消耗和性能开销（仅适用于 OpenClaw Agent 环境）。当用户提到「测量」「测试」「性能」「token 消耗」「多少 token」「开销」「成本」「效率」或想要评估、对比、优化某个 skill 的资源使用时，立即使用此 skill。也适用于 skill 发布前的性能验证、多轮测试对比、热/冷缓存分析、以及分析两个 skill 之间消耗差异。英文触发词：measure token cost, performance test, how many tokens, benchmark skill。即使用户没有明确说「skill-perf」，只要涉及 OpenClaw skill 性能分析就应触发。技术实现：通过 OpenClaw 的 sessions_spawn 启动双 subagent 并发测量，自动扣除系统底噪，生成 HTML 报告和置信度评级。"
user-invocable: true
metadata:
  openclaw:
    emoji: "📊"
---
