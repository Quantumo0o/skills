---
name: jiuma_free_text2image
description: 九码AI图片生成简单版。当用户需要根据文本提示词生成图片时使用此技能。调用九码AI异步API生成图片，轮询获取结果URL。简单直接的实现。
---

# 九码AI图片生成简单版

最简单的九码AI图片生成技能。输入提示词，生成图片URL。

## 使用方法

### 命令行使用

```bash
python agent.py "你的提示词"
```

## API说明

### 生成API
- **URL**: `POST https://api.jiuma.com/gpt/text2image`
- **参数**: `{"text": "提示词"}`

### 查询API  
- **URL**: `POST https://api.jiuma.com/gpt/get_text2image_result`
- **参数**: `{"task_id": "任务ID"}`

## 返回格式

成功时返回:
```json
{
  "status": "success",
  "message": "图片生成成功",
  "data": {
    "image_url": "图片URL",
    "task_id": "任务ID",
    "attempts": 轮询次数
  }
}
```

失败时返回:
```json
{
  "status": "failed|timeout|error",
  "message": "错误描述",
  "data": {}
}
```

## 示例

```bash
# 生成图片
$ python simple_jiuma_gen.py "宁静的湖边日落"

# 输出示例
{
  "status": "success",
  "message": "图片生成成功",
  "data": {
    "image_url": "https://example.com/image.jpg",
    "task_id": "task_123456",
    "attempts": 5
  }
}
```