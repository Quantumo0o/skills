"""
Text-to-Image client using the Zoe API (REST + polling).

Usage:
    python text_to_image_request.py --prompt "a cute cat" --api-key "sk-xxx"
    python text_to_image_request.py --prompt "a cute cat" --base-url "https://example.com/zoe-model"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import quote, urlparse

import httpx

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency

    def load_dotenv() -> None:
        return None


DEFAULT_BASE_URL = "https://zoe-api.sensetime.com/zoe-model"
DEFAULT_MODEL_SIZE = "2k"
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_POLL_INTERVAL = 5.0
DEFAULT_TIMEOUT = 300.0
API_KEY_ENV = "ZOE_INFOG_API_KEY"

load_dotenv()


def build_headers(api_key: str) -> dict[str, str]:
    return {"Authorization": api_key}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit a text-to-image task via Zoe API and download the result."
    )
    parser.add_argument(
        "--base-url",
        "--host",
        dest="base_url",
        default=os.getenv("API_BASE_URL", DEFAULT_BASE_URL),
        help="API base URL (default: https://zoe-api.sensetime.com/zoe-model)",
    )
    parser.add_argument(
        "--api-key",
        dest="api_key",
        default=os.getenv(API_KEY_ENV, ""),
        help=f"API key (also via {API_KEY_ENV} env var)",
    )
    parser.add_argument(
        "--prompt", required=True, help="Text prompt for image generation"
    )
    parser.add_argument("--negative-prompt", default="", help="Negative prompt")
    parser.add_argument(
        "--image-size",
        default=DEFAULT_MODEL_SIZE,
        choices=["1k", "2k"],
        help="Image size preset (default: 2k)",
    )
    parser.add_argument(
        "--aspect-ratio",
        "--ratio",
        dest="aspect_ratio",
        default=DEFAULT_ASPECT_RATIO,
        choices=[
            "2:3",
            "3:2",
            "3:4",
            "4:3",
            "4:5",
            "5:4",
            "1:1",
            "16:9",
            "9:16",
            "21:9",
            "9:21",
        ],
        help="Aspect ratio (default: 16:9)",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--unet-name", dest="unet_name", default=None, help="UNet model name (optional)")
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=DEFAULT_POLL_INTERVAL,
        help="Polling interval in seconds (default: 5.0)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="Max wait time in seconds (default: 300.0)",
    )
    parser.add_argument(
        "--save-path",
        dest="save_path",
        type=Path,
        default=Path("outputs/text_to_image.png"),
        help="Output image path (default: outputs/text_to_image.png)",
    )
    parser.add_argument(
        "--insecure", action="store_true", help="Disable TLS certificate verification"
    )
    parser.add_argument(
        "-o",
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    return parser.parse_args()


def ensure_output_path(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def is_absolute_url(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)


def extract_task_input(task: dict) -> dict:
    task_input = task.get("input")
    if isinstance(task_input, dict):
        return task_input
    return {
        key: task.get(key)
        for key in ("prompt", "negative_prompt", "image_size", "aspect_ratio", "seed", "unet_name")
        if key in task
    }


def extract_task_image(task: dict) -> dict | None:
    image = task.get("image")
    if isinstance(image, dict) and image.get("url"):
        return image
    return None


def download_image(
    client: httpx.Client,
    base_url: str,
    headers: dict[str, str],
    image_ref: str,
    output_path: Path,
) -> Path:
    if is_absolute_url(image_ref):
        response = client.get(image_ref, headers=headers)
    else:
        image_key = image_ref.lstrip("/")
        response = client.get(
            f"{base_url}/v1/generation/files/{quote(image_key, safe='/')}",
            headers=headers,
        )
    response.raise_for_status()
    output_path.write_bytes(response.content)
    return output_path


def output_result(
    output_format: str,
    status: str,
    output_path: Path | None = None,
    error: str = "",
    message: str = "",
    task_id: str = "",
) -> None:
    if output_format == "json":
        result = {"status": status}
        if output_path:
            result["output"] = str(output_path)
        if task_id:
            result["task_id"] = task_id
        if message:
            result["message"] = message
        if error:
            result["error"] = error
        print(json.dumps(result, ensure_ascii=False))
    else:
        # Text mode: existing behavior
        if status == "ok":
            if message:
                print(message)
            if output_path:
                print(output_path)
        else:
            print(error or message, file=sys.stderr)


def main() -> int:
    args = parse_args()
    if not args.api_key:
        error_msg = (
            f"{API_KEY_ENV} is required. Set it in the environment or pass --api-key."
        )
        output_result(
            args.output_format,
            status="failed",
            error="API key is required",
            message=error_msg,
        )
        return 1

    payload = {
        "prompt": args.prompt,
        "negative_prompt": args.negative_prompt,
        "image_size": args.image_size,
        "aspect_ratio": args.aspect_ratio,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.unet_name is not None:
        payload["unet_name"] = args.unet_name

    headers = build_headers(args.api_key)
    output_path = ensure_output_path(args.save_path)
    is_json = args.output_format == "json"

    try:
        with httpx.Client(timeout=30.0, verify=not args.insecure) as client:
            create_response = client.post(
                f"{args.base_url.rstrip('/')}/v1/generation/text-to-image",
                json=payload,
                headers=headers,
            )
            create_response.raise_for_status()
            task = create_response.json()
            task_id = task["id"]

            if not is_json:
                print(f"created task: {task_id}")
                task_input = extract_task_input(task)
                if task_input:
                    print(f"submitted input: {task_input}")

            deadline = time.monotonic() + args.timeout
            while True:
                status_response = client.get(
                    f"{args.base_url.rstrip('/')}/v1/generation/text-to-image/{task_id}",
                    headers=headers,
                )
                status_response.raise_for_status()
                task = status_response.json()
                state = task["state"]
                progress = task.get("progress", 0.0)

                if not is_json:
                    print(
                        f"state={state} progress={progress:.2f}", end="\r", flush=True
                    )

                if state == "completed":
                    if not is_json:
                        print()
                    image = extract_task_image(task)
                    if not image:
                        error_msg = f"task completed but no image found: {task}"
                        output_result(
                            args.output_format,
                            status="failed",
                            error="No image found",
                            message=error_msg,
                            task_id=task_id,
                        )
                        return 1
                    saved_path = download_image(
                        client=client,
                        base_url=args.base_url.rstrip("/"),
                        headers=headers,
                        image_ref=image["url"],
                        output_path=output_path,
                    )

                    if not is_json:
                        print(f"image saved to {saved_path}")

                    output_result(
                        args.output_format,
                        status="ok",
                        output_path=saved_path,
                        message="Image generated successfully",
                        task_id=task_id,
                    )
                    return 0

                if state in {"failed", "canceled", "interrupted"}:
                    if not is_json:
                        print()
                    error_msg = task.get("error_message") or "unknown error"
                    output_result(
                        args.output_format,
                        status="failed",
                        error=f"Task {state}",
                        message=f"task failed: {error_msg}",
                        task_id=task_id,
                    )
                    return 1

                if time.monotonic() >= deadline:
                    if not is_json:
                        print()
                    output_result(
                        args.output_format,
                        status="failed",
                        error="Timeout",
                        message=f"timed out waiting for task {task_id}",
                        task_id=task_id,
                    )
                    return 1

                time.sleep(args.poll_interval)
    except httpx.HTTPStatusError as exc:
        error_msg = f"http error: {exc.response.status_code} {exc.response.text}"
        output_result(
            args.output_format,
            status="failed",
            error=f"HTTP {exc.response.status_code}",
            message=error_msg,
        )
        return 1
    except (httpx.HTTPError, OSError, ValueError) as exc:
        output_result(
            args.output_format,
            status="failed",
            error=type(exc).__name__,
            message=f"request error: {exc}",
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
