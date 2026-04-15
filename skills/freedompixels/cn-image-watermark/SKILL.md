---
name: cn-image-watermark
description: |
  图片水印工具。为图片添加文字或Logo水印，防止内容被搬运。
  支持批量处理、九宫格定位、透明度调节。
  当用户说"水印"、"图片水印"、"添加水印"、"防伪"、"版权"时触发。
  Keywords: 图片水印, 添加水印, 防搬运, 版权保护, watermark, image.
metadata: {"openclaw": {"emoji": "🖼️"}}
---

# cn-image-watermark - 图片水印工具

为图片添加文字或图片水印，防止搬运。

## 核心功能
- **文字水印**：叠加文字（半透明、位置可调）
- **图片水印**：叠加Logo/小图标
- **批量处理**：对整个文件夹批量加水印
- **位置控制**：九宫格位置（9个锚点）
- **透明度**：0-100可调

## 使用场景
- 知识付费内容防搬运（水印"，禁止转载"）
- 社交媒体图片品牌标识
- 封面图添加版权信息
- 批量处理产品图片

## 输出格式
```json
{
  "input": "photo.jpg",
  "output": "photo_watermarked.jpg",
  "type": "text",
  "position": "右下",
  "status": "ok"
}
```

## 使用方式
```bash
# 文字水印
python ~/.qclaw/skills/cn-image-watermark/watermark.py text "photo.jpg" "©养虾记" --position bottom-right

# Logo水印
python ~/.qclaw/skills/cn-image-watermark/watermark.py image "photo.jpg" "logo.png" --position bottom-right --opacity 60

# 批量处理
python ~/.qclaw/skills/cn-image-watermark/watermark.py batch "./photos" "output" "©养虾记"
```

## 依赖
- Python3
- Pillow（PIL）：`pip3 install Pillow`

## 标签
cn, watermark, image, photo, protection
