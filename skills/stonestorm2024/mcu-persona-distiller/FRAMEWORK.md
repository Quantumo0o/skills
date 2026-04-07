# MCU Persona Distiller Framework — 使用指南

## 🎯 这是什么

一个标准化框架，用于将 MCU（漫威电影宇宙）中的任意角色蒸馏成可加载的 AI Agent Skill。

每个角色只需要一个 JSON 配置文件，运行构建脚本即可自动生成完整的 SKILL.md + 维度文件。

## 📦 框架结构

```
mcu-persona-distiller/
├── FRAMEWORK.md           # 本文档
├── README.md             # 项目介绍
├── SKILL.md              # 框架主入口（暂未使用）
├── config/
│   └── characters/        # 角色配置文件目录
│       ├── thanos-distill.json
│       ├── loki-distill.json
│       ├── strange-distill.json
│       └── thor-distill.json
├── templates/
│   └── base-SKILL.md     # SKILL.md 模板
└── scripts/
    ├── build.sh          # 构建脚本
    └── publish.sh        # 发布脚本
```

## 🚀 快速开始

### 添加新角色

在 `config/characters/` 创建 `xxx-distill.json`：

```json
{
  "slug": "xxx-distill",
  "displayName": "角色蒸馏器",
  "mcuName": "Character Name (中文名)",
  "description": "一句话描述角色",
  "sourceMovies": ["电影1", "电影2"],
  "keyTraits": ["特质1", "特质2"],
  "signatureLines": [
    {
      "text": "经典台词",
      "movie": "出自哪部电影",
      "context": "说这句话的情境"
    }
  ],
  "personalityProfile": {
    "core": "核心性格",
    "belief": "核心信念",
    "contradiction": "性格矛盾"
  },
  "interactionStyle": {
    "tone": "语气基调",
    "humor": "幽默风格",
    "threatStyle": "威胁风格（反派适用）"
  },
  "decisionLogic": {
    "method": "决策方法",
    "framework": "决策框架"
  },
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
    "procedure": "low"
  }
}
```

### 构建

```bash
chmod +x scripts/build.sh scripts/publish.sh
./scripts/build.sh <character-slug>
```

### 发布

```bash
./scripts/publish.sh <character-slug> [github|clawhub|both]
```

## ⚖️ 法律声明

- 所有角色蒸馏均基于 MCU 公开电影资料
- 仅供学习研究，不构成商业授权
- 遵循 Fair Use 原则
- 迪士尼/漫威拥有相关 IP 权益

## 🔗 相关链接

- 框架 GitHub：https://github.com/stonestorm2024/mcu-persona-distiller
- 框架 ClawHub：待发布
