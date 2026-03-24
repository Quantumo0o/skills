---
name: freeads-snap-ad
description: "Transforms product photos into professional 8-second advertising videos using AI with brand protection. Use when user asks to create a product ad, generate advertising video, make a commercial, product marketing video, 随手拍广告, 生成广告片, 产品广告, or discusses creating AI-generated advertising content from product photos. Workflow includes brand/LOGO collection, intelligent background removal with LOGO protection, AI-generated slogan, cost estimation, and cinematic video production with consistency protection via Atlas Cloud API."
version: 2.0.7
author: lipeng10
metadata:
  category: media-generation
  platforms:
    - codeflicker
    - openclaw
    - claude-code
  required-env:
    - ATLASCLOUD_API_KEY
  estimated-cost: "$1.63-3.27 per video"
---

# FreeAds 随手拍广告 v2.0

> **🚀 快速安装**
> 
> 复制以下命令安装此 Skill：
> ```
> clawhub install lipeng10/freeads-snap-ad
> ```
> 
> 或在 AI 助手中输入：`帮我安装 clawhub.ai/lipeng10/freeads-snap-ad`

---

一键将产品照片转化为高端广告片，全新增加 **品牌/LOGO 保护** 和 **费用精准预估** 功能。

**⚠️ 重要：最终产出是 8 秒 AI 广告视频，不是海报或静态图片！**

通过 Atlas Cloud API 调用：
- **Nano Banana 2** 进行智能抠图 ← **必须执行，提取产品主体，避免背景杂物干扰**
- **Gemini 3.1 Pro** 生成广告文案和视频描述
- **Veo 3.1 Image-to-Video** 制作 8 秒高品质广告视频 ← **这是核心输出**

全程保护品牌标识不走样。

## 概述

"随手拍广告" 是一个 AI 驱动的 **产品广告视频** 生成工作流，让用户只需提供一张产品照片，即可自动完成：

1. **品牌/LOGO 收集**（可选）- 询问用户品牌信息，支持图片/URL/网络搜索 LOGO
2. **🔍 产品识别（关键步骤）** - 使用 **Gemini 3.1 Pro** 视觉能力**准确识别**产品类型、材质、用途
3. **🖼️ 智能抠图（必须执行）** - 使用 Nano Banana 2 **提取产品主体**，去除背景杂物，保护 LOGO 不走样
4. **文案生成** - 基于准确的产品识别结果，生成匹配的广告文案和视频描述
5. **费用预估** - 在生成前展示详细费用，让用户确认后再继续
6. **🎬 视频制作（核心输出）** - 使用 **Veo 3.1 Image-to-Video** 生成 8 秒广告视频

**⚠️ 为什么抠图是必须的？**
- 用户拍摄的产品照片通常包含背景杂物（桌面、其他物品等）
- 背景杂物会干扰 AI 视频生成，导致不相关内容出现在广告中
- 提取纯净的产品主体可以让广告更专业、更聚焦

**⚠️ 关键规则：**
- **必须先抠图**：用户上传的图片必须先通过 Nano Banana 2 提取产品主体，再用于视频生成
- 最终产出**必须是视频文件**，不能用文字方案或图片替代
- 如果视频 API 调用失败，**必须向用户报告具体错误**，不能静默失败

**⚠️ 关键提醒：**
- **最终产出必须是视频文件（.mp4）**，不是图片或文案文档
- 必须调用 `POST https://api.atlascloud.ai/api/v1/model/generateVideo` 接口
- 模型名称：`google/veo3.1/image-to-video`
- 如果视频生成 API 失败，必须报告错误并告知用户，而不是用其他内容替代

## 首次使用配置

### API Key 设置

在首次使用前，用户需要配置 Atlas Cloud API Key：

1. **获取 API Key**
   - 访问 [Atlas Cloud Console](https://console.atlascloud.ai/)
   - 注册账号并创建 API Key

2. **配置环境变量**（推荐）
   ```bash
   # 在 ~/.zshrc 或 ~/.bashrc 中添加
   export ATLASCLOUD_API_KEY="your-api-key"
   ```

3. **安全提示**
   - 请勿将 API Key 提交到版本控制系统
   - 请勿在公开场合分享 API Key
   - 建议定期轮换 API Key
   - 开发和生产环境使用不同的 Key

### 询问用户 API Key

如果环境变量未设置，请询问用户：

> 请提供您的 Atlas Cloud API Key（可在 https://console.atlascloud.ai/ 获取）。
> 
> 您的 API Key 将仅用于本次会话的 API 调用，不会被存储或传输到其他地方。

---

## 完整工作流程

### Step 1: 获取用户图片

请用户提供产品图片，支持以下方式：
- 直接粘贴图片
- 提供本地文件路径
- 提供图片 URL

---

### Step 1.5: 品牌/LOGO 收集（新增）

**在处理图片前，询问用户品牌信息：**

> 在生成广告前，我想了解一下您的品牌信息，以确保广告效果最佳：
>
> **您的产品是否有品牌 LOGO 或标识？**
>
> **选项 A：有品牌 LOGO** 
> 我可以帮您在生成过程中保护 LOGO 不走样、产品外观不变形。请提供：
> - 直接粘贴 LOGO 图片
> - 提供 LOGO 图片链接
> - 告诉我品牌名称，我来帮您网络搜索
>
> **选项 B：没有品牌/暂时跳过**
> 直接进行广告生成

**收集的品牌信息结构：**

```python
brand_info = {
    "has_brand": True,               # 是否有品牌
    "brand_name": "品牌名称",         # 品牌名称
    "logo_url": "LOGO图片URL",        # LOGO 图片链接
    "logo_position": "产品正面中央",   # LOGO 在产品上的位置描述
    "brand_colors": ["#FF0000"],      # 品牌主色调（可选）
    "protection_level": "high"        # 保护等级：high/medium/low
}
```

**LOGO 获取方式：**

1. **用户直接提供图片**：上传到 Atlas Cloud 获取 URL
2. **用户提供 URL**：直接使用
3. **网络搜索**：使用 `search_web` 工具搜索 `[品牌名] logo png 透明背景`

---

### Step 2: 上传图片到 Atlas Cloud

```python
import requests
import os

api_key = os.environ.get("ATLASCLOUD_API_KEY")

# 上传本地图片
upload_response = requests.post(
    "https://api.atlascloud.ai/api/v1/model/uploadMedia",
    headers={"Authorization": f"Bearer {api_key}"},
    files={"file": open("product_photo.jpg", "rb")}
)
image_url = upload_response.json().get("url")
print(f"图片已上传: {image_url}")
```

---

### Step 3: 使用 Nano Banana 2 抠图提取产品主体（必须执行）

**⚠️ 重要：此步骤必须执行，不能跳过！**

用户拍摄的产品照片通常包含背景杂物（桌面、其他物品、杂乱背景等），这些杂物会干扰 AI 视频生成。因此必须先抠图提取产品主体。

Nano Banana 2 (Gemini 3.1 Flash Image) 支持智能抠图和背景替换。

基本提示词中已包含关键要求：
- **提取产品主体**：仅保留产品本身，去除所有背景杂物
- **品牌保护**：保持 LOGO 清晰、不走样
- **产品完整性**：保持形状、比例、颜色、纹理不变

```python
import requests
import time

# 根据是否有品牌信息选择不同的 prompt
def get_background_removal_prompt(brand_info: dict) -> str:
    """
    生成抠图提示词，包含品牌保护要求
    """
    base_prompt = """Remove the background COMPLETELY while applying STRICT protection requirements:

PRODUCT INTEGRITY (CRITICAL):
- Maintain EXACT product shape and proportions - no distortion allowed
- Keep ALL textures and surface details crisp and sharp
- Preserve material appearance (metal, glass, plastic, fabric, etc.) perfectly
- Colors must remain accurate - no color shifting"""

    if brand_info.get("has_brand"):
        brand_prompt = f"""

BRAND LOGO PROTECTION (TOP PRIORITY):
- Keep ALL brand logos 100% sharp, legible, and undistorted
- The brand LOGO located at: {brand_info.get('logo_position', 'on the product')}
- Maintain exact logo colors without ANY shift
- Preserve logo proportions PERFECTLY - no stretching or compression
- Do NOT blur, obscure, or modify any brand text or symbols
- Brand name: {brand_info.get('brand_name', 'N/A')}"""
    else:
        brand_prompt = """

DETAIL PRESERVATION:
- Keep any text, labels, or markings on the product clear and readable
- Preserve all fine details and textures"""

    output_prompt = """

OUTPUT REQUIREMENTS:
- Place on pure white (#FFFFFF) background
- Add subtle professional shadow for depth
- Professional studio lighting simulation
- Ensure edges are clean and precise

The product authenticity and any brand elements are the TOP PRIORITY."""

    return base_prompt + brand_prompt + output_prompt


# 使用增强的 prompt 进行抠图
def remove_background_with_brand_protection(image_url: str, api_key: str, brand_info: dict) -> str:
    """
    使用 Nano Banana 2 Edit 去除背景，保护品牌 LOGO
    """
    prompt = get_background_removal_prompt(brand_info)
    
    response = requests.post(
        "https://api.atlascloud.ai/api/v1/model/generateImage",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/nano-banana-2/edit",
            "prompt": prompt,
            "image_url": image_url,
            "output_format": "png"
        }
    )
    
    prediction_id = response.json().get("predictionId")
    
    # 轮询获取结果
    while True:
        result = requests.get(
            f"https://api.atlascloud.ai/api/v1/model/getResult?predictionId={prediction_id}",
            headers={"Authorization": f"Bearer {api_key}"}
        ).json()
        
        if result.get("status") == "completed":
            return result.get("output")
        elif result.get("status") == "failed":
            raise Exception(f"抠图失败: {result.get('error')}")
        
        time.sleep(2)

# 使用示例
white_bg_image_url = remove_background_with_brand_protection(image_url, api_key, brand_info)
print(f"白底图生成完成（已保护品牌LOGO）: {white_bg_image_url}")
```

---

### Step 4: 使用 Gemini 3.1 Pro 分析产品并生成文案

在生成文案前，询问用户是否有特定需求：

> 我已经完成产品抠图，现在准备为您的产品生成广告文案。
>
> 请选择文案风格：
> 1. **高端奢华风** - 适合高端产品，强调品质与格调
> 2. **科技未来风** - 适合科技产品，突出创新与智能
> 3. **自然清新风** - 适合生活用品，传递自然健康理念
> 
> 或者您可以：
> - 提供自定义文案方向
> - 补充产品的核心卖点

```python
from openai import OpenAI

client = OpenAI(
    api_key=api_key,
    base_url="https://api.atlascloud.ai/v1"
)

# ========================================
# 关键：首先使用 Gemini 3.1 Pro 准确识别产品
# ========================================
# 注意：不能靠猜测，必须让模型仔细分析图片中的实际内容

style_instruction = "高端奢华广告风格，强调品质、工艺和格调"

# 如果有品牌信息，加入品牌要求
brand_instruction = ""
if brand_info.get("has_brand"):
    brand_instruction = f"""

品牌信息：
- 品牌名称：{brand_info.get('brand_name')}
- 请在文案中适当融入品牌名称
- 视频提示词中需要强调品牌 LOGO 的保护"""

response = client.chat.completions.create(
    model="gemini-3.1-pro",
    messages=[
        {
            "role": "system",
            "content": f"""你是一位资深广告创意总监，擅长为产品创作高端广告文案。

**第一步：仔细识别产品（最重要）**
请非常仔细地观察图片，准确判断：
1. 这是什么产品？（具体品类，如：金属纪念品、电子产品、食品饮料、服装配饰等）
2. 产品的材质是什么？（金属、塑料、玻璃、织物、陶瓷等）
3. 产品的用途是什么？
4. 产品的设计特点和工艺细节

**禁止猜测！** 如果不确定，请在回复中说明。

**第二步：基于准确识别生成文案**
1. 一句简短有力的 Slogan（不超过10个字）
2. 一段8秒广告视频的解说词（30-50字，适合配音）
3. 视频画面描述（英文，用于 Veo 3.1 视频生成，需包含产品一致性保护要求）

风格要求：{style_instruction}
{brand_instruction}

输出格式：
产品识别: [准确描述这是什么产品，材质，用途]
SLOGAN: [你的Slogan]
解说词: [你的解说词]
画面描述: [英文，用于Veo 3.1视频生成，必须包含产品一致性保护要求]"""
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": white_bg_image_url}
                },
                {
                    "type": "text",
                    "text": "请分析这个产品并生成广告文案"
                }
            ]
        }
    ],
    max_tokens=1024
)

ad_content = response.choices[0].message.content
print(ad_content)
```

---

### Step 5: 确认文案方案

向用户展示生成的文案方案，让用户选择或修改：

> 我为您生成了以下广告方案：
>
> **Slogan**: [生成的Slogan]
> **解说词**: [生成的解说词]
>
> 请确认是否满意，或者您可以：
> - 要求重新生成
> - 提供修改意见
> - 直接使用您自己的文案

---

### Step 5.5: 费用预估确认（新增）

**在生成视频前，向用户展示详细费用预估：**

```python
def estimate_ad_cost(
    video_duration: int = 8,
    with_audio: bool = True,
    resolution: str = "1080p"
) -> dict:
    """
    精准估算广告生成费用
    
    Args:
        video_duration: 视频时长（4/6/8秒）
        with_audio: 是否生成音频
        resolution: 分辨率（720p/1080p）
        
    Returns:
        费用明细字典
    """
    # 各步骤费用
    costs = {
        "background_removal": {
            "name": "智能抠图",
            "model": "Nano Banana 2 Edit",
            "min": 0.02,
            "max": 0.05,
            "unit": "次"
        },
        "copywriting": {
            "name": "文案生成",
            "model": "Gemini 3.1 Pro",
            "min": 0.01,
            "max": 0.02,
            "unit": "次"
        },
        "video_generation": {
            "name": "视频生成",
            "model": "Veo 3.1 I2V",
            "min": video_duration * 0.09,
            "max": video_duration * (0.20 if with_audio else 0.10),
            "unit": f"{video_duration}秒"
        }
    }
    
    # 计算总费用
    total_min = sum(item["min"] for item in costs.values())
    total_max = sum(item["max"] for item in costs.values())
    
    return {
        "breakdown": costs,
        "total_min": round(total_min, 2),
        "total_max": round(total_max, 2),
        "currency": "USD",
        "params": {
            "duration": video_duration,
            "with_audio": with_audio,
            "resolution": resolution
        }
    }


def format_cost_estimate(cost_data: dict) -> str:
    """
    格式化费用预估展示
    """
    breakdown = cost_data["breakdown"]
    params = cost_data["params"]
    
    audio_status = "含音频" if params["with_audio"] else "无音频"
    
    output = f"""
📊 **本次广告生成费用预估**

| 步骤 | 模型 | 费用估算 |
|------|------|----------|
| 🖼️ {breakdown['background_removal']['name']} | {breakdown['background_removal']['model']} | ${breakdown['background_removal']['min']:.2f} - ${breakdown['background_removal']['max']:.2f} |
| ✍️ {breakdown['copywriting']['name']} | {breakdown['copywriting']['model']} | ${breakdown['copywriting']['min']:.2f} - ${breakdown['copywriting']['max']:.2f} |
| 🎬 {breakdown['video_generation']['name']} ({params['duration']}秒, {audio_status}) | {breakdown['video_generation']['model']} | ${breakdown['video_generation']['min']:.2f} - ${breakdown['video_generation']['max']:.2f} |
| **💰 预计总费用** | - | **${cost_data['total_min']:.2f} - ${cost_data['total_max']:.2f}** |

**当前配置：**
- 视频时长：{params['duration']} 秒
- 音频：{'含音频（费用较高）' if params['with_audio'] else '无音频'}
- 分辨率：{params['resolution']}

**省钱建议：**
- 选择 4 秒视频可节省约 50% 费用
- 不需要音频可节省约 50% 视频费用

⚠️ *实际费用以 Atlas Cloud 账单为准*

**是否继续生成？（Y/N）**
"""
    return output

# 使用示例
cost_estimate = estimate_ad_cost(video_duration=8, with_audio=True)
print(format_cost_estimate(cost_estimate))
```

**向用户展示费用预估：**

> 📊 **本次广告生成费用预估**
>
> | 步骤 | 模型 | 费用估算 |
> |------|------|----------|
> | 🖼️ 智能抠图 | Nano Banana 2 Edit | $0.02 - $0.05 |
> | ✍️ 文案生成 | Gemini 3.1 Pro | $0.01 - $0.02 |
> | 🎬 视频生成 (8秒, 含音频) | Veo 3.1 I2V | $0.72 - $1.60 |
> | **💰 预计总费用** | - | **$0.75 - $1.67** |
>
> **省钱建议：**
> - 选择 4 秒视频可节省约 50% 费用
> - 不需要音频可节省约 50% 视频费用
>
> **是否继续生成？**

**等待用户确认后再继续生成视频。**

---

### Step 6: 使用 Veo 3.1 生成广告视频（一致性保护增强）

**关键增强：在视频生成时保持产品外观、LOGO、场景的一致性**

```python
def get_video_prompt_with_consistency(
    base_prompt: str,
    brand_info: dict,
    camera_style: str = "dolly_in"
) -> str:
    """
    生成包含一致性保护要求的视频提示词
    
    Args:
        base_prompt: 基础视频描述
        brand_info: 品牌信息
        camera_style: 摄像机风格
    """
    
    # 摄像机运动选项
    camera_movements = {
        "dolly_in": "Camera slowly dollies in, gradually revealing product details",
        "orbit": "Camera smoothly orbits around the product at a consistent distance",
        "zoom": "Gentle zoom emphasizing the product's premium quality",
        "static": "Static shot with subtle product rotation"
    }
    
    camera_desc = camera_movements.get(camera_style, camera_movements["dolly_in"])
    
    # 品牌保护要求
    brand_protection = ""
    if brand_info.get("has_brand"):
        brand_protection = f"""

BRAND PROTECTION (CRITICAL - MUST FOLLOW):
- The brand LOGO must remain CLEARLY VISIBLE throughout ALL frames
- LOGO must stay sharp, legible, and NEVER distorted
- LOGO position: {brand_info.get('logo_position', 'on the product')}
- Brand colors must remain CONSISTENT - no color shifting
- Any brand text must remain readable at all times"""

    consistency_prompt = f"""Cinematic product advertisement video.

{base_prompt}

{camera_desc}

MANDATORY CONSISTENCY REQUIREMENTS (CRITICAL):
1. PRODUCT SHAPE CONSISTENCY:
   - Product MUST maintain EXACT shape throughout ALL frames
   - Size and proportions MUST NOT change at any point
   - No morphing, warping, stretching, or deformation allowed
   - Product silhouette must remain identical from start to finish

2. PRODUCT APPEARANCE CONSISTENCY:
   - Colors must remain EXACTLY the same throughout
   - Textures and surface details must stay consistent
   - Material appearance (reflections, highlights) must be uniform
   - No unexpected changes in product appearance
{brand_protection}

3. SCENE CONSISTENCY:
   - Lighting must remain uniform throughout the video
   - Background must stay consistent (pure white)
   - Shadow position and intensity must be consistent
   - No sudden lighting changes or flickering

4. MOTION QUALITY:
   - Camera movement must be SMOOTH and STEADY
   - No jarring transitions or sudden movements
   - Motion should be elegant and professional
   - Maintain cinematic quality throughout

TECHNICAL SPECIFICATIONS:
- Professional studio lighting with soft diffused key light
- Premium advertising aesthetic
- Clean, elegant motion
- 1080p resolution, 24fps
- Pure white or subtle gradient background

The product is the HERO - it must look IDENTICAL and PERFECT from the first frame to the last."""

    return consistency_prompt


# 生成广告视频
def generate_ad_video_with_protection(
    image_url: str,
    video_description: str,
    api_key: str,
    brand_info: dict,
    duration: int = 8,
    aspect_ratio: str = "16:9",
    with_audio: bool = True
) -> str:
    """
    使用 Veo 3.1 生成广告视频，保护品牌和产品一致性
    """
    # 构建完整的视频提示词
    full_prompt = get_video_prompt_with_consistency(
        base_prompt=video_description,
        brand_info=brand_info,
        camera_style="dolly_in"
    )
    
    response = requests.post(
        "https://api.atlascloud.ai/api/v1/model/generateVideo",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/veo3.1/image-to-video",
            "prompt": full_prompt,
            "image_url": image_url,
            "durationSeconds": duration,
            "resolution": "1080p",
            "aspectRatio": aspect_ratio,
            "withAudio": with_audio
        }
    )
    
    prediction_id = response.json().get("predictionId")
    print(f"视频生成中，任务ID: {prediction_id}")
    print("预计需要 2-3 分钟，请耐心等待...")
    
    # 轮询获取结果
    while True:
        result = requests.get(
            f"https://api.atlascloud.ai/api/v1/model/getResult?predictionId={prediction_id}",
            headers={"Authorization": f"Bearer {api_key}"}
        ).json()
        
        if result.get("status") == "completed":
            return result.get("output")
        elif result.get("status") == "failed":
            raise Exception(f"视频生成失败: {result.get('error')}")
        
        print("视频生成中，请稍候...")
        time.sleep(10)

# 使用示例
video_url = generate_ad_video_with_protection(
    image_url=white_bg_image_url,
    video_description="The premium product elegantly showcases its design",
    api_key=api_key,
    brand_info=brand_info,
    duration=8,
    aspect_ratio="16:9",
    with_audio=True
)
print(f"广告视频生成完成！视频链接: {video_url}")
```

---

## 参数选项

### 视频方向
- **横屏 (16:9)** - 默认选项，适合电脑/电视/横向社交媒体
- **竖屏 (9:16)** - 适合手机观看、抖音、小红书等竖屏平台

### 文案风格
- **高端奢华风** - 强调品质、工艺、格调
- **科技未来风** - 突出创新、智能、未来感
- **自然清新风** - 传递自然、健康、纯净

### 视频时长与费用
| 时长 | 仅视频费用 | 含音频费用 |
|------|-----------|-----------|
| 4秒  | ~$0.80    | ~$1.60    |
| 6秒  | ~$1.20    | ~$2.40    |
| 8秒  | ~$1.60    | ~$3.20    |

### 品牌保护等级
- **高 (high)** - 严格保护 LOGO 和产品外观，推荐用于品牌广告
- **中 (medium)** - 适度保护，允许轻微的艺术效果
- **低 (low)** - 基本保护，允许更多创意变化

---

## 费用估算详情

### 完整费用计算器

| 步骤 | 模型 | 计费方式 | 价格范围 |
|------|------|----------|----------|
| 图片上传 | - | 免费 | $0 |
| 智能抠图 | Nano Banana 2 Edit | 按次 | $0.02 - $0.05 |
| 文案生成 | Gemini 3.1 Pro | 按 Token | $0.01 - $0.02 |
| 视频生成 | Veo 3.1 I2V | 按秒 | $0.09 - $0.20/秒 |

### 视频费用详细参考

| 配置 | 4秒 | 6秒 | 8秒 |
|------|-----|-----|-----|
| 仅视频 (720p) | $0.80 | $1.20 | $1.60 |
| 仅视频 (1080p) | $0.80 | $1.20 | $1.60 |
| 含音频 (720p) | $1.60 | $2.40 | $3.20 |
| 含音频 (1080p) | $1.60 | $2.40 | $3.20 |

### 套餐费用参考

| 套餐 | 包含内容 | 总费用估算 |
|------|----------|-----------|
| 经济版 | 4秒无音频 | $0.83 - $0.87 |
| 标准版 | 8秒无音频 | $1.63 - $1.67 |
| 专业版 | 8秒含音频 | $1.63 - $3.27 |

---

## 注意事项

1. **图片质量** - 提供高清、光线充足的产品照片效果更佳
2. **LOGO 清晰度** - 如果产品有品牌 LOGO，确保 LOGO 在原图中清晰可见
3. **生成时间** - 视频生成约需2-3分钟，请耐心等待
4. **API 限制** - 注意 Atlas Cloud 的速率限制和配额
5. **版权** - 确保产品图片和品牌 LOGO 有合法使用权
6. **费用确认** - 在生成视频前务必确认费用预估

---

## 支持文件

- **`references/atlas-cloud-api.md`** - Atlas Cloud API 详细文档
- **`references/brand-protection-guide.md`** - 品牌保护最佳实践指南
- **`examples/ad-copy-templates.md`** - 广告文案模板和示例
- **`scripts/setup-api-key.sh`** - API Key 配置脚本

---

## 故障排查

### 常见问题

1. **API Key 无效**
   - 检查环境变量是否正确设置
   - 确认 API Key 未过期

2. **图片上传失败**
   - 检查图片格式（支持 JPEG/PNG/WEBP）
   - 确认图片大小不超过限制

3. **抠图后 LOGO 模糊**
   - 确保原图中 LOGO 清晰
   - 使用更高保护等级的 prompt
   - 尝试提供单独的 LOGO 图片参考

4. **视频中产品变形**
   - 使用增强的一致性保护 prompt
   - 检查原图是否清晰
   - 尝试更简单的摄像机运动（如静态镜头）

5. **视频生成超时**
   - 视频生成需要2-3分钟，请耐心等待
   - 如持续失败，检查 API 配额

6. **费用超出预期**
   - 在生成前使用费用预估功能
   - 选择较短时长或无音频模式节省成本
