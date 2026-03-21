# Vidu Video Generate API Reference

视频生成 API 参考，包含文生视频、图生视频、参考生视频、首尾帧视频。

## Base URL

```
https://api.vidu.cn/ent/v2
```

**域名选择规则**：
- **简体中文用户**：使用 `api.vidu.cn`
- **非简体中文用户**：使用 `api.vidu.com`

根据用户交流语言自动切换域名。

## Authentication

```
Authorization: Token YOUR_API_KEY
```

---

## 视频生成 API

### 1. 文生视频 (text2video)

**POST** `/text2video`

```json
{
  "model": "viduq3-pro",
  "prompt": "视频描述",
  "duration": 5,
  "aspect_ratio": "16:9",
  "resolution": "720p",
  "audio": true
}
```

**模型选择**：
| 模型 | 时长范围 | 分辨率 | 特点 |
|------|----------|--------|------|
| viduq3-pro-fast | 1-16秒 | 720p/1080p | 支持音画同步，支持视频分镜，速度快 |
| viduq3-turbo | 1-16秒 | 540p/720p/1080p | 支持音画同步，支持视频分镜，速度快 |
| viduq3-pro | 1-16秒 | 540p/720p/1080p | 支持音画同步，支持视频分镜，效果最好 |
| viduq2 | 1-10秒 | 540p/720p/1080p | 最新模型，情绪表达强，细节更丰富 |
| viduq1 | 固定5秒 | 固定1080p | 画面清晰，平滑转场，运镜稳定 |

---

### 2. 图生视频 (img2video)

**POST** `/img2video`

```json
{
  "model": "viduq3-pro",
  "images": ["图片URL或base64"],
  "prompt": "视频描述",
  "duration": 5,
  "resolution": "720p",
  "audio": true
}
```

**用途**：单张图片生成视频，图片作为首帧。

**模型选择**：
| 模型 | 时长范围 | 分辨率 | 特点 |
|------|----------|--------|------|
| viduq3-pro-fast | 1-16秒 | 720p/1080p | 速度最快，效果对标viduq3-pro |
| viduq3-turbo | 1-16秒 | 540p/720p/1080p | 速度快，效果好 |
| viduq3-pro | 1-16秒 | 540p/720p/1080p | 效果最好 |
| viduq2-pro-fast | 1-10秒 | 720p/1080p | 价格触底，速度提升2-3倍 |
| viduq2-pro | 1-10秒 | 540p/720p/1080p | 情感表达强，动态细节丰富 |
| viduq2-turbo | 1-10秒 | 540p/720p/1080p | 效果好，生成快 |
| viduq1 | 固定5秒 | 固定1080p | 画面清晰，平滑转场 |
| viduq1-classic | 固定5秒 | 固定1080p | 转场、运镜更丰富 |
| vidu2.0 | 4/8秒 | 360p/720p/1080p | 生成速度快 |

---

### 3. 参考生视频 (reference2video)

**POST** `/reference2video`

```json
{
  "model": "viduq3",
  "images": ["图片1", "图片2", "..."],
  "prompt": "视频描述",
  "duration": 5,
  "audio": true
}
```

**用途**：多张参考图生成视频（多人、多主体场景）。

**限制**：最多 7 张参考图。

**模型选择**：
| 模型 | 图片上限 | 时长范围 | 分辨率 | 特点 |
|------|----------|----------|--------|------|
| viduq3 | 7张 | 3-16秒 | 540p/720p/1080p | 默认，多人场景，智能切镜 |
| viduq3-beta | 5张 | 3-10秒 | 540p/720p/1080p | 最新模型（预览版），支持音画同出 |
| viduq2-pro | 7张 | 1-10秒 | 540p/720p/1080p | 支持参考视频，支持视频编辑 |
| viduq2 | 7张 | 1-10秒 | 540p/720p/1080p | 动态效果好，细节丰富 |
| viduq1 | 7张 | 5秒 | 固定1080p | 画面清晰，平滑转场 |
| vidu2.0 | 7张 | 4秒 | 360p/720p | 生成速度快 |

---

### 4. 首尾帧视频 (start-end2video)

**POST** `/start-end2video`

```json
{
  "model": "viduq3-pro",
  "images": ["首帧图片", "尾帧图片"],
  "prompt": "视频描述",
  "duration": 5
}
```

**用途**：提供首尾帧，生成过渡动画。

**限制**：必须输入 2 张图片（首帧 + 尾帧）。

**模型选择**：
| 模型 | 时长范围 | 分辨率 | 特点 |
|------|----------|--------|------|
| viduq3-pro-fast | 1-16秒 | 720p/1080p | 速度最快 |
| viduq3-turbo | 1-16秒 | 540p/720p/1080p | 速度快 |
| viduq3-pro | 1-16秒 | 540p/720p/1080p | 效果最好 |
| viduq2-pro-fast | 1-10秒 | 720p/1080p | 价格触底，速度快 |
| viduq2-pro | 1-10秒 | 540p/720p/1080p | 效果好，细节丰富 |
| viduq2-turbo | 1-10秒 | 540p/720p/1080p | 效果好，生成快 |
| viduq1 | 固定5秒 | 固定1080p | 画面清晰，平滑转场 |
| viduq1-classic | 固定5秒 | 固定1080p | 转场、运镜更丰富 |
| vidu2.0 | 4/8秒 | 360p/720p/1080p | 生成速度快 |

---

## 任务管理 API

### 查询任务状态

**GET** `/tasks`

返回任务列表，根据 `task_id` 查找。

### 取消任务

**DELETE** `/tasks/{task_id}`

---

## 响应格式

### 任务创建响应

```json
{
  "task_id": "xxx",
  "state": "pending",
  "model": "viduq3-pro",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### 任务完成响应

```json
{
  "task_id": "xxx",
  "state": "success",
  "creations": [
    {
      "url": "https://...",
      "cover_url": "https://..."
    }
  ]
}
```

---

## 错误码

| 错误 | 说明 |
|------|------|
| Invalid API key | API 密钥错误 |
| Image size exceeds | 图片超过 50MB |
| Invalid aspect ratio | 不支持的比例 |
| Task failed | 生成失败 |

---

## 参数速查

### 视频参数

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| duration | 1-16秒 | 5 |
| aspect_ratio | 16:9, 9:16, 4:3, 3:4, 1:1 | 16:9 |
| resolution | 540p, 720p, 1080p | 720p |
| audio | true/false | false |
