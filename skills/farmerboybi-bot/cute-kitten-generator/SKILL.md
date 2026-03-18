---
name: cute-kitten-generator
description: Generate high-detail cute kitten/animal images using ComfyUI local workflow. Use when user wants to create adorable animal photos with high clarity (1536×1536 resolution, 100 steps, RealVisXL V5.0). Supports kittens, puppies, and other small animals with close-up portrait, fur details, and home scene settings.
---

# Cute Kitten Generator

## Quick Start

生成可爱小猫/小动物高清图片：

```bash
cd /Users/lobster/.openclaw/workspace/ComfyUI
curl -X POST -H "Content-Type: application/json" \
  -d '{"prompt": '"$(cat cute_kitten_sofa.json)"', "client_id": "qiuer-bot"}' \
  http://127.0.0.1:8188/prompt
```

## 配置固化 🔒

- **分辨率**: 1536×1536（高清正方形）
- **步骤**: 100 steps（高细节）
- **CFG**: 8.0
- **模型**: RealVisXL_V5.0_fp16.safetensors
- **Sampler**: dpmpp_2m, scheduler: karras
- **Workflow**: `cute_kitten_sofa.json`

## 场景定制

修改 `cute_kitten_sana.json` 的 prompt（node 2）：

- **动物类型**: kitten → puppy / bunny / hamster
- **场景**: sofa → bed / carpet / garden / basket
- **光线**: golden hour → morning light / soft window light

## 发送 WhatsApp

生成完成后发送：

```bash
openclaw message send \
  --target "+17704012443" \
  --media "/Users/lobster/.openclaw/workspace/ComfyUI/output/CUTE_KITTEN_SOFA_00001_.png"
```

## 清晰度提升方案

### 方案 A（已固化 ✅）
- 1536×1536 + 100 steps → 2.9MB 高清版

### 方案 B（Hires. Fix）
如需更高清晰度：
- 先 1024×1024 生成
- 再 2x upscale + 重绘细节
- 创建 `cute_kitten_hires.json` workflow

## 文件位置
- **Workflow**: `/Users/lobster/.openclaw/workspace/ComfyUI/cute_kitten_sofa.json`
- **输出**: `/Users/lobster/.openclaw/workspace/ComfyUI/output/CUTE_KITTEN_*.png`
