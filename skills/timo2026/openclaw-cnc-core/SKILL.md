---
name: openclaw-cnc-core
description: 🦞 OpenClaw CNC 智能报价系统核心框架 - 支持 STEP 解析、智能报价、风险控制
version: 1.2.0
author: Timo2026
license: MIT
repository: https://github.com/Timo2026/openclaw-cnc-core
tags:
  - cnc
  - quote
  - cad
  - step
  - manufacturing
  - ai
  - openclaw
metadata:
  openclaw:
    runtime: python3.8
    entrypoint: core/quote_engine
    channels:
      - qqbot
      - email
      - feishu
requirements:
  env_vars:
    - name: OPENCLAW_WORKSPACE
      description: 工作目录路径（可选，默认当前目录）
    - name: DASHSCOPE_API_KEY
      description: DashScope API密钥（用于向量嵌入，可选）
  external_apis:
    - name: DashScope
      purpose: 向量嵌入服务
      optional: true
    - name: Feishu Webhook
      purpose: 风险预警通知
      optional: true
---

# OpenClaw CNC Core 🦞

> 基于 OpenClaw 的 CNC 智能报价系统核心框架

## ⚠️ 重要说明

### 外部API声明

本系统使用以下外部服务（均为可选）：

| 服务 | 用途 | 必需 |
|------|------|------|
| **DashScope API** | 向量嵌入服务 | ❌ 可选 |
| **Feishu Webhook** | 风险预警通知 | ❌ 可选 |

### 环境变量

```bash
# 可选：设置工作目录
export OPENCLAW_WORKSPACE=/your/workspace/path

# 可选：DashScope API密钥（用于向量嵌入）
export DASHSCOPE_API_KEY=your_api_key
```

## ✨ Features

- 🔧 **Smart Quote Engine** - Rule + RAG hybrid decision system
- 📐 **3D Drawing Parser** - STEP/STP file support, auto geometry extraction
- ⚠️ **Risk Control** - Auto anomaly detection, manual review trigger
- 🔍 **Case Retrieval** - Similar order matching for accuracy
- 🚀 **OpenClaw Integration** - QQ/Email/Feishu multi-channel

## 🚀 Quick Start

```python
from core.quote_engine import OpenClawQuoteEngine

engine = OpenClawQuoteEngine(config_dir="./config/examples")
result = engine.calculate_quote(order_data)
print(f"Quote: ¥{result.total_price}")
```

## 📦 Versions

| Version | Features | Use Case |
|---------|----------|----------|
| **Community (Free)** | Engine framework + CAD parser + Examples | Learning, Small projects |
| **Commercial (Paid)** | Pre-trained model + Price database + Support | Production, Enterprise |

## 📥 Install

```bash
pip install cadquery trimesh open3d flask numpy pandas scipy
```

## 🔗 Links

- **Gitee**: https://gitee.com/timo2026/openclaw-cnc-core
- **GitHub**: https://github.com/Timo2026/openclaw-cnc-core
- **Commercial**: cnc@openclaw.ai

## 📄 License

- Community: MIT License
- Commercial: Contact for licensing

---

Made with ❤️ by [OpenClaw Team](https://openclaw.ai)