---
name: mcu-persona-distiller
description: MCU漫威电影宇宙角色蒸馏框架。将任意MCU角色转化为可加载的AI Agent Skill，输出到GitHub和ClawHub。
emoji: 🛡️
tags:
  - mcu
  - marvel
  - framework
  - persona-distill
  - automation
license: MIT
---

# MCU Persona Distiller Framework

> 漫威电影宇宙角色蒸馏框架 — 将任意 MCU 角色转化为可加载的 AI Agent Skill。

## 框架功能

1. **标准化配置** — 每个角色一个 JSON 文件，定义所有核心维度
2. **自动构建** — 运行 `build.sh` 自动生成完整 SKILL.md
3. **一键发布** — 运行 `publish.sh` 同时发布到 GitHub + ClawHub

## 支持角色

| 角色 | GitHub | ClawHub |
|------|--------|----------|
| 灭霸 (Thanos) | ✅ | ✅ |
| 洛基 (Loki) | ✅ | ✅ |
| 奇异博士 (Strange) | ✅ | ✅ |
| 雷神 (Thor) | ✅ | ✅ |

## 快速开始

```bash
# 构建角色包
./scripts/build.sh thanos-distill

# 发布（二选一或两者）
./scripts/publish.sh thanos-distill github
./scripts/publish.sh thanos-distill clawhub
./scripts/publish.sh thanos-distill both
```

## 配置文件格式

详见 [FRAMEWORK.md](FRAMEWORK.md)

## 免责声明

⚠️ 所有角色蒸馏均基于漫威电影宇宙（MCU）公开影视资料，仅供学习研究参考，不构成任何商业授权或官方关联声明。
