---
name: volcengine-doubao-image-gen
description: 豆包图片生成。使用火山引擎 API 生成图片，支持文生图、图生图、单图/组图生成。触发词：豆包图片、doubao、生成图片、火山引擎、字节跳动图片生成。
---

# 豆包图片生成

使用火山引擎豆包 API 生成图片，支持文生图、图生图、单图/组图生成。

**默认模型：** `doubao-seedream-4-5-251128`

## 环境要求

### 必需凭证
- `ARK_API_KEY`：火山引擎豆包 API Key（必填）

### 可选环境变量
- `DOUBAO_MODEL`：覆盖默认模型版本（可选）

## 快速开始

```bash
# 设置 API Key
export ARK_API_KEY="your-api-key"

# 文生图
python3 scripts/generate_image.py --prompt "一只可爱的猫咪" --filename "cat.png"
```

## 参数说明

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| `--prompt` / `-p` | 图片描述（必填） | - |
| `--filename` / `-f` | 输出文件名 | 自动生成 |
| `--size` / `-s` | 图片尺寸 (1K/2K/4K) | 2K |
| `--no-watermark` | 不添加水印 | 默认有水印 |
| `--model` / `-m` | 模型名称 | doubao-seedream-4-5-251128 |
| `--image` / `-i` | 参考图 URL（可多次，图生图） | 无 |
| `--sequential` | 是否生成组图 (`disabled`/`auto`) | disabled |
| `--max-images` | 组图最大数量 | 无限制 |
| `--stream` | 流式输出 | false |

> 安全提示：不要通过命令行传递 API Key，请使用环境变量 `ARK_API_KEY`。

## 使用示例

### 文生图

```bash
python3 scripts/generate_image.py \
  --prompt "星空下的城市夜景，赛博朋克风格" \
  --filename "city.png"
```

### 图生图

```bash
python3 scripts/generate_image.py \
  --prompt "参考这个 LOGO，做一套户外运动品牌视觉设计，品牌名称为 GREEN" \
  --image "https://example.com/logo.png" \
  --sequential auto \
  --max-images 5 \
  --filename "brand_"
```

### 多图参考

```bash
python3 scripts/generate_image.py \
  --prompt "将图 1 的服装换为图 2 的服装" \
  --image "https://example.com/look1.png" \
  --image "https://example.com/look2.png" \
  --filename "outfit_swap.png"
```

## API Key 获取

1. 访问火山引擎控制台：https://console.volcengine.com/ark
2. 创建或选择一个接入点
3. 获取 API Key

## 提示词技巧

建议按以下结构编写：

1. 主体描述（是什么）
2. 场景/环境（在哪里）
3. 风格（赛博朋克、水彩、油画等）
4. 光影效果
5. 氛围/情绪

## 注意事项

1. 图片尺寸越大，生成时间越长
2. 默认添加水印，使用 `--no-watermark` 可去除
3. 组图使用 `--sequential auto` 和 `--max-images`
4. 图生图可通过多次 `--image` 传入多张参考图

## 故障排查

**错误：No API key provided**
- 设置环境变量：`export ARK_API_KEY="your-key"`

**错误：API Error 401**
- API Key 无效或过期

**错误：API Error 429**
- 请求频率超限，稍后重试

**错误：Network Error**
- 检查网络连接或代理设置

## 模型版本

| 模型 | 说明 | 状态 |
|------|------|------|
| `doubao-seedream-4-5-251128` | 文生图/图生图，支持组图 | 当前默认 |
| `doubao-seedream-5-0-260128` | 旧版本 | 已弃用 |
