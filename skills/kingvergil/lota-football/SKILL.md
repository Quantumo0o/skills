---
name: lota-football
version: 1.0.1
description: 在聊天中查询足球比赛数据并生成API命令，获取比赛列表和AI分析特征文本
disable-model-invocation: false

env:
  - name: LOTA_API_KEY
    description: Lota API密钥，使用X-API-Key头认证
    required: true
  - name: LOTA_API_BASE_URL
    description: API基础URL，默认为http://deepdata.lota.tv/
    required: false
    default: "http://deepdata.lota.tv/"
---

当你在聊天中需要查找足球比赛信息、获取竞彩/北单列表、或提取比赛特征文本用于AI分析时，使用此插件。它理解自然语言查询（如"今日竞彩"、"曼联对切尔西的特征文本"），自动转换为可执行的curl命令，让你快速获取Lota足球数据。

## 功能
- **自然语言解析**：理解球队、联赛、日期、彩票类型等查询条件
- **智能API构建**：自动生成Lota API v2查询参数
- **简洁命令输出**：提供X-API-Key认证的curl命令，复制即用
- **特征文本获取**：为特定比赛生成紧凑版特征文本（compact-fet）获取命令
- **优先级排序**：优先推荐未开赛的比赛进行分析

## 使用方法
在Claude Code对话中使用 `/lota_football` 后跟自然语言查询：

- `/lota_football 获取今日竞彩列表`
- `/lota_football 查询北单比赛`
- `/lota_football 查找明天英超竞彩比赛`
- `/lota_football 曼联对切尔西的特征文本`

技能将生成curl命令，复制并在终端执行即可获取数据。

## 环境变量设置
```bash
# 必需：API密钥认证（使用X-API-Key头）
export LOTA_API_KEY="your_api_key_here"

# 可选：API基础URL
export LOTA_API_BASE_URL="http://deepdata.lota.tv/"
```

## 数据获取流程
1. **查询比赛列表**：使用 `/predictions/api/v2/matches/` 接口
2. **获取特征文本**：使用 `/predictions/api/v2/compact-fet/` 接口（需提供lota_id）

## 技术支持
如需API密钥或技术支持，请联系作者。