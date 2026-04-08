"""
Image Edit client using the Zoe API (REST + polling).

Usage:
    python scripts/image_edit_request.py --image ./input.png --prompt "replace the text with Hello"
    python scripts/image_edit_request.py --image uploads/abc.png --prompt "remove watermark"
    python scripts/image_edit_request.py --image ./input.png --prompt "remove watermark" --save-path /tmp/openclaw/edit.png
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
DEFAULT_POLL_INTERVAL = 5.0
DEFAULT_TIMEOUT = 300.0
API_KEY_ENV = "ZOE_INFOG_API_KEY"

load_dotenv()


def build_headers(api_key: str) -> dict[str, str]:
    return {"Authorization": api_key}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit an image-edit task via Zoe API and download the result."
    )
    parser.add_argument(
        "--base-url",
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
        "--image",
        required=True,
        help="Local image path, remote URL, or cached file key",
    )
    parser.add_argument("--prompt", required=True, help="Edit instruction prompt")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
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
        "--output",
        dest="save_path",
        type=Path,
        default=Path("outputs/image_edit.png"),
        help="Output image path (default: outputs/image_edit.png)",
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


def is_local_file(value: str) -> bool:
    return Path(value).is_file()


def extract_task_input(task: dict) -> dict:
    task_input = task.get("input")
    if isinstance(task_input, dict):
        return task_input
    return {key: task.get(key) for key in ("image", "prompt", "seed") if key in task}


def extract_task_image(task: dict) -> dict | None:
    image = task.get("image")
    if isinstance(image, dict) and image.get("url"):
        return image
    return None


def upload_local_image(
    client: httpx.Client,
    base_url: str,
    headers: dict[str, str],
    image_path: Path,
) -> str:
    with image_path.open("rb") as image_file:
        response = client.post(
            f"{base_url}/v1/generation/files",
            headers=headers,
            files={"upload_file": (image_path.name, image_file)},
        )
    response.raise_for_status()
    body = response.json()
    if not isinstance(body, str) or not body:
        raise ValueError(f"unexpected upload response: {body}")
    return body


def generate_presigned_url(
    client: httpx.Client,
    base_url: str,
    headers: dict[str, str],
    oss_path: str,
) -> str:
    response = client.get(
        f"{base_url}/v1/generation/files/generate-presigned-url",
        headers=headers,
        params={"oss_path": oss_path},
    )
    response.raise_for_status()
    body = response.json()
    if not isinstance(body, str) or not body:
        raise ValueError(f"unexpected presigned url response: {body}")
    return body


def resolve_image_ref(
    client: httpx.Client,
    base_url: str,
    headers: dict[str, str],
    image_value: str,
) -> str:
    if is_absolute_url(image_value):
        return image_value
    if is_local_file(image_value):
        uploaded_path = upload_local_image(client, base_url, headers, Path(image_value))
        return generate_presigned_url(client, base_url, headers, uploaded_path)
    return image_value


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

    headers = build_headers(args.api_key)
    base_url = args.base_url.rstrip("/")
    output_path = ensure_output_path(args.save_path)
    is_json = args.output_format == "json"

    try:
        with httpx.Client(timeout=30.0, verify=not args.insecure) as client:
            image_ref = resolve_image_ref(client, base_url, headers, args.image)
            if image_ref != args.image and not is_json:
                print(f"uploaded image: {image_ref}")

            payload = {
                "image": image_ref,
                "prompt": args.prompt,
            }
            if args.seed is not None:
                payload["seed"] = args.seed

            create_response = client.post(
                f"{base_url}/v1/generation/image-edit",
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
                    f"{base_url}/v1/generation/image-edit/{task_id}",
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
                        base_url=base_url,
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
                        message="Image edited successfully",
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
