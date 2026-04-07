# MCU Persona Distiller Framework

> 漫威电影宇宙（MCU）角色蒸馏框架 — 将任意MCU角色转化为可加载的 AI Agent Skill。

## 🎯 项目目标

通过标准化的数据配置，自动生成符合 Agent Skills 规范的角色蒸馏包，发布到 GitHub 和 ClawHub。

## 📁 目录结构

```
mcu-persona-distiller/
├── FRAMEWORK.md           # 本框架使用指南
├── SKILL.md               # 主入口（OpenClaw 自动加载）
├── config/
│   ├── base-template.md   # 基础蒸馏模板
│   └── characters/
│       ├── thanos.json    # 灭霸配置
│       ├── loki.json      # 洛基配置
│       └── ...
├── scripts/
│   ├── build.sh           # 构建角色SKILL.md
│   └── publish.sh         # 一键发布到 GitHub + ClawHub
└── output/                # 构建产物输出目录
```

## 🚀 快速开始

### 1. 添加新角色

在 `config/characters/` 下创建 `xxx.json` 配置文件：

```json
{
  "slug": "thanos-distill",
  "displayName": "Thanos (灭霸)",
  "mcuName": "Thanos",
  "description": "MCU泰坦永恒者，梦想家与实践者",
  "sourceMovies": ["复仇者联盟3","复仇者联盟4"],
  "keyTraits": ["使命必达", "冷静哲学", "绝对理性", "代价承担者"],
  "signatureLines": [
    {"text": "I am inevitable.", "movie": "Endgame"},
    {"text": "Fine, I'll do it myself.", "movie": "Infinity War"}
  ],
  "dimensions": {
    "personality": true,
    "interaction": true,
    "memory": true,
    "procedure": true
  },
  "confidence": {
    "personality": "very-high",
    "interaction": "high",
    "memory": "medium",
    "procedure": "medium"
  }
}
```

### 2. 构建角色包

```bash
cd mcu-persona-distiller
./scripts/build.sh <character-slug>
# 例：./scripts/build.sh thanos
```

### 3. 发布

```bash
./scripts/publish.sh <character-slug>
# 交互式：让你选择发布到 GitHub / ClawHub / 两者
```

## 📋 已收录角色

| 角色 | 状态 | 置信度 |
|------|------|--------|
| thanos-distill (灭霸) | ✅ 已完成 | 高 |
| loki-distill (洛基) | 🔄 构建中 | - |
| strange-distill (奇异博士) | 🔄 构建中 | - |
| thor-distill (雷神) | 🔄 构建中 | - |

## ⚖️ 免责声明

所有角色蒸馏均基于漫威电影宇宙（MCU）公开影视资料，仅供学习研究参考。漫威、迪士尼及相关版权方拥有相关IP权益。本项目不构成任何商业使用授权或官方关联声明。

## 📜 许可证

MIT License — 可自由使用于学习、研究和非商业目的。
