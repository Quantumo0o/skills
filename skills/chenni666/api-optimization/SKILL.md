---
name: chenni-free-api
description: "发现和配置免费/超低价 AI 模型，支持智能分流和无感降级。支持 SiliconFlow、NVIDIA NIM、OpenRouter、DeepSeek、智谱等多平台。当用户说'免费模型'、'省钱配置'、'加免费 API'、'find free models'、'配置免费模型'、'低成本模型'时触发"
tools: ["Bash", "Read", "Write"]
metadata:
  openclaw:
    requires:
      env: ["OPENROUTER_API_KEY", "SILICONFLOW_API_KEY", "NVIDIA_API_KEY"]
    primaryEnv: OPENROUTER_API_KEY
---

# Chenni Free API - 免费模型聚合指南

一站式发现、配置和管理多平台免费 AI 模型。支持智能分流和无感降级。

## 核心功能

- 🆓 **推荐模型**：精选多平台免费模型列表
- 🔍 **自动发现**：每日刷新 OpenRouter 可用免费模型
- 🧠 **智能分流**：按任务类型选择最合适模型
- 🔄 **无感降级**：主模型失败时自动 fallback 并自动回切

---

## 推荐免费模型

### SiliconFlow（硅基流动）- 国内首选

| 模型 ID | 说明 | 免费额度 | 推荐用途 |
|---------|------|----------|----------|
| `Qwen/Qwen3-8B` | 通义千问 3 代 8B | 完全免费 | 日常对话、通用任务 |
| `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B` | DeepSeek R1 蒸馏版 | 完全免费 | 推理任务 |
| `THUDM/glm-4-9b-chat` | 智谱 GLM-4 | 完全免费 | 中文理解 |
| `Qwen/Qwen2.5-Coder-7B-Instruct` | Qwen 编码专用 | 完全免费 | 代码生成 |

**注册链接**：https://cloud.siliconflow.cn/i/hoxZec8I

### OpenRouter - 国际平台

| 模型 ID | 说明 | 价格 | 推荐用途 |
|---------|------|------|----------|
| `google/gemini-3.1-flash-lite` | Gemini Flash Lite | ~免费 | 快速任务 |
| `qwen/qwen3.5-flash-02-23` | Qwen 3.5 Flash | ~免费 | 预算选项 |
| `x-ai/grok-4.1-fast` | Grok Fast | 极低价 | 工具调用 |

**注册链接**：https://openrouter.ai/settings/keys

### DeepSeek - 国产高性价比

| 模型 | 免费额度 | 特点 |
|------|----------|------|
| DeepSeek V3 | 每天免费调用 | 国产最强，日常首选 |
| DeepSeek R1 | 部分免费 | 推理能力强 |

**注册链接**：https://platform.deepseek.com/

### 智谱 GLM - 稳定可靠

| 模型 | 免费额度 | 特点 |
|------|----------|------|
| GLM-4 | 每月 100 万 tokens | API 稳定，中文优秀 |

**注册链接**：https://open.bigmodel.cn/

### NVIDIA NIM - 免费多模态

| 模型 ID | 上下文 | 类型 | 说明 |
|---------|--------|------|------|
| `qwen/qwen3.5-397b-a17b` | 128k | text+image | Qwen 3.5 大参数版本 |
| `stepfun-ai/step-3.5-flash` | 256k | text+image | 阶跃星辰，超长上下文 |
| `moonshotai/kimi-k2.5` | 256k | text+image | Kimi，超长上下文 |
| `z-ai/glm4.7` | 128k | text+image | 智谱 GLM 4.7 |
| `z-ai/glm5` | 128k | text+image | 智谱 GLM 5 |
| `minimaxai/minimax-m2.5` | 192k | text+image | MiniMax |

**注册链接**：https://build.nvidia.com

---

## 配置步骤

### Step 1: 获取 API Keys

```bash
# SiliconFlow
export SILICONFLOW_API_KEY="sk-xxx"

# OpenRouter
export OPENROUTER_API_KEY="sk-or-v1-xxx"

# DeepSeek
export DEEPSEEK_API_KEY="sk-xxx"

# 智谱
export ZHIPU_API_KEY="xxx.xxx"
```

### Step 2: 自动发现免费模型

```bash
node scripts/discover.js --platform all
```

### Step 3: 生成 OpenClaw 配置

```bash
node scripts/configure.js --output ~/.openclaw/free-models.json
```

### Step 4: 应用配置

```bash
# 备份原配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup

# 合并配置
openclaw config.patch < ~/.openclaw/free-models.json

# 重启生效
openclaw gateway restart
```

---

## 智能分流配置

按任务类型自动选择最优模型：

```json
{
  "agents": {
    "defaults": {
      "models": {
        "routing": {
          "coding": ["siliconflow/Qwen/Qwen2.5-Coder-7B-Instruct", "deepseek/deepseek-coder"],
          "reasoning": ["siliconflow/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"],
          "translation": ["siliconflow/THUDM/glm-4-9b-chat"],
          "chat": ["siliconflow/Qwen/Qwen3-8B", "deepseek/deepseek-chat"],
          "vision": ["openrouter/google/gemini-3.1-flash-lite"]
        }
      }
    }
  }
}
```

---

## 无感降级配置

主模型失败时自动切换到备用模型：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "siliconflow/Qwen/Qwen3-8B",
        "fallbacks": [
          "siliconflow/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
          "openrouter/google/gemini-3.1-flash-lite",
          "deepseek/deepseek-chat"
        ],
        "retryPolicy": {
          "maxRetries": 3,
          "backoffMs": 1000,
          "autoRecover": true,
          "recoverIntervalMs": 300000
        }
      }
    }
  }
}
```

---

## 脚本使用说明

### discover.js - 自动发现

```bash
# 发现所有平台免费模型
node scripts/discover.js --platform all

# 只发现 OpenRouter
node scripts/discover.js --platform openrouter

# 只发现 SiliconFlow
node scripts/discover.js --platform siliconflow

# 输出为 JSON
node scripts/discover.js --platform all --json > models.json
```

### router.js - 智能分流

```bash
# 根据任务类型推荐模型
node scripts/router.js --task coding
node scripts/router.js --task reasoning
node scripts/router.js --task translation

# 生成分流配置
node scripts/router.js --generate-config > routing.json
```

### fallback.js - 无感降级

```bash
# 测试降级链
node scripts/fallback.js --test

# 监控模型状态
node scripts/fallback.js --monitor

# 生成降级配置
node scripts/fallback.js --generate-config > fallback.json
```

---

## 成本对比

| 平台 | 免费模型数量 | 付费最低价 | 推荐指数 |
|------|--------------|------------|----------|
| SiliconFlow | 10+ | ¥0.7/百万 tokens | ⭐⭐⭐⭐⭐ |
| NVIDIA NIM | 6 | 完全免费 | ⭐⭐⭐⭐⭐ |
| OpenRouter | 5+ | $0.0000002/百万 tokens | ⭐⭐⭐⭐ |
| DeepSeek | 2 | ¥1/百万 tokens | ⭐⭐⭐⭐ |
| 智谱 GLM | 1 | ¥5/百万 tokens | ⭐⭐⭐ |

---

## 注意事项

1. **API Key 安全**：不要将 API Key 提交到代码仓库
2. **免费额度限制**：免费模型通常有 QPS 或总量限制
3. **模型可用性**：免费模型可能随时调整，建议定期运行 `discover.js`
4. **降级策略**：建议至少配置 2-3 个备用模型

---

## 环境变量

| 变量 | 说明 | 必需 |
|------|------|------|
| `OPENROUTER_API_KEY` | OpenRouter API Key | 是 |
| `SILICONFLOW_API_KEY` | SiliconFlow API Key | 否 |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | 否 |
| `ZHIPU_API_KEY` | 智谱 API Key | 否 |
| `NVIDIA_API_KEY` | NVIDIA NIM API Key | 否 |
