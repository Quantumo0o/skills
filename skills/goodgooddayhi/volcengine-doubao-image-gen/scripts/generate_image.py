#!/usr/bin/env python3
"""
Doubao Image Generation - 豆包图片生成

使用火山引擎豆包 API 生成图片。
"""

import argparse
import json
import os
import sys
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
DEFAULT_MODEL = "doubao-seedream-4-5-251128"


def generate_image(
    prompt: str,
    api_key: str,
    size: str = "2K",
    watermark: bool = True,
    model: str = DEFAULT_MODEL,
    image=None,
    sequential: str = "disabled",
    max_images: int = None,
    stream: bool = False,
) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "sequential_image_generation": sequential,
        "response_format": "url",
        "size": size,
        "stream": stream,
        "watermark": watermark,
    }

    if image:
        payload["image"] = image if isinstance(image, list) else image

    if sequential == "auto" and max_images:
        payload["sequential_image_generation_options"] = {
            "max_images": max_images
        }

    data = json.dumps(payload).encode("utf-8")
    request = Request(API_URL, data=data, headers=headers, method="POST")

    try:
        with urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else "Unknown error"
        raise Exception(f"API Error {e.code}: {error_body}")
    except URLError as e:
        raise Exception(f"Network Error: {e.reason}")


def download_image(url: str, filepath: str) -> None:
    request = Request(url)
    with urlopen(request, timeout=60) as response:
        with open(filepath, "wb") as f:
            f.write(response.read())
    print(f"✓ Image saved to: {filepath}")


def generate_filename(prompt: str, index: int = None) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    words = prompt.split()[:5]
    name = "-".join(words).replace(",", "").replace("，", "")[:30]
    if index:
        return f"{timestamp}-{name}-{index}.png"
    return f"{timestamp}-{name}.png"


def main():
    parser = argparse.ArgumentParser(description="豆包图片生成 - 使用火山引擎 API 生成图片")
    parser.add_argument("--prompt", "-p", required=True, help="图片描述/提示词")
    parser.add_argument("--filename", "-f", help="输出文件名 (默认自动生成)")
    parser.add_argument("--size", "-s", choices=["1K", "2K", "4K"], default="2K", help="图片尺寸")
    parser.add_argument("--no-watermark", action="store_true", help="不添加水印")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"模型名称 (默认：{DEFAULT_MODEL})")
    parser.add_argument("--image", "-i", action="append", help="参考图 URL（可多次指定）")
    parser.add_argument("--sequential", choices=["disabled", "auto"], default="disabled", help="是否生成组图")
    parser.add_argument("--max-images", type=int, default=None, help="组图最大数量")
    parser.add_argument("--stream", action="store_true", help="流式输出")
    args = parser.parse_args()

    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("Error: No API key provided.")
        print("Please set ARK_API_KEY environment variable:")
        print("  export ARK_API_KEY='your-api-key'")
        sys.exit(1)

    image = None
    if args.image:
        image = args.image[0] if len(args.image) == 1 else args.image

    filename = args.filename or generate_filename(args.prompt)

    print("Generating image...")
    print(f"  Prompt: {args.prompt[:50]}...")
    print(f"  Size: {args.size}")
    print(f"  Model: {args.model}")

    try:
        result = generate_image(
            prompt=args.prompt,
            api_key=api_key,
            size=args.size,
            watermark=not args.no_watermark,
            model=args.model,
            image=image,
            sequential=args.sequential,
            max_images=args.max_images,
            stream=args.stream,
        )

        if "data" in result and len(result["data"]) > 0:
            for idx, item in enumerate(result["data"]):
                image_url = item.get("url")
                if image_url:
                    if len(result["data"]) > 1 and not args.filename:
                        output_file = generate_filename(args.prompt, idx + 1)
                    elif len(result["data"]) > 1 and args.filename:
                        root, ext = os.path.splitext(filename)
                        output_file = f"{root}-{idx + 1}{ext or '.png'}"
                    else:
                        output_file = filename
                    download_image(image_url, output_file)
                else:
                    print(f"Error: No image URL in response {idx + 1}")
            print(f"\n✅ Generated {len(result['data'])} image(s)")
        else:
            print("Error: No image URL in response")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
