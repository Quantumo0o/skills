"""
OpenClaw-oriented wrapper around the Zoe REST clients.

This wrapper owns timestamped output naming under /tmp/openclaw so the skill
does not have to build fragile shell one-liners with shared variables.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("/tmp/openclaw")
TEXT_TO_IMAGE_PREFIX = "zoe_infog"
IMAGE_EDIT_PREFIX = "zoe_edit"
SCRIPT_DIR = Path(__file__).resolve().parent
API_KEY_ENV = "ZOE_INFOG_API_KEY"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run zoe-infog workflows with stable OpenClaw output paths."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    text_parser = subparsers.add_parser(
        "text-to-image", help="Run text-to-image generation"
    )
    text_parser.add_argument(
        "--prompt",
        required=True,
        help="Raw text prompt; backend handles prompt expansion",
    )
    text_parser.add_argument("--negative-prompt", default="", help="Negative prompt")
    text_parser.add_argument(
        "--image-size", default="2k", choices=["1k", "2k"], help="Image size preset"
    )
    text_parser.add_argument(
        "--aspect-ratio",
        default="16:9",
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
        help="Aspect ratio",
    )
    text_parser.add_argument("--base-url", help="Override API base URL")
    text_parser.add_argument("--api-key", help="Override API key")
    text_parser.add_argument("--seed", type=int, help="Random seed")
    text_parser.add_argument("--unet-name", dest="unet_name", help="UNet model name (optional)")
    text_parser.add_argument(
        "--poll-interval", type=float, default=5.0, help="Polling interval in seconds"
    )
    text_parser.add_argument(
        "--timeout", type=float, default=300.0, help="Max wait time in seconds"
    )
    text_parser.add_argument(
        "--insecure", action="store_true", help="Disable TLS verification"
    )
    text_parser.add_argument(
        "-o",
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    edit_parser = subparsers.add_parser("image-edit", help="Run image-edit generation")
    edit_parser.add_argument(
        "--image",
        required=True,
        help="Local image path, remote URL, or cached file key",
    )
    edit_parser.add_argument("--prompt", required=True, help="Edit instruction prompt")
    edit_parser.add_argument("--base-url", help="Override API base URL")
    edit_parser.add_argument("--api-key", help="Override API key")
    edit_parser.add_argument("--seed", type=int, help="Random seed")
    edit_parser.add_argument(
        "--poll-interval", type=float, default=5.0, help="Polling interval in seconds"
    )
    edit_parser.add_argument(
        "--timeout", type=float, default=300.0, help="Max wait time in seconds"
    )
    edit_parser.add_argument(
        "--insecure", action="store_true", help="Disable TLS verification"
    )
    edit_parser.add_argument(
        "-o",
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    return parser


def timestamped_output(prefix: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return OUTPUT_DIR / f"{prefix}_{timestamp}.png"


def add_common_args(command: list[str], args: argparse.Namespace) -> list[str]:
    if args.base_url:
        command.extend(["--base-url", args.base_url])
    resolved_api_key = resolve_api_key(args.api_key)
    if resolved_api_key:
        command.extend(["--api-key", resolved_api_key])
    if args.seed is not None:
        command.extend(["--seed", str(args.seed)])
    if hasattr(args, 'unet_name') and args.unet_name is not None:
        command.extend(["--unet-name", args.unet_name])
    command.extend(["--poll-interval", str(args.poll_interval)])
    command.extend(["--timeout", str(args.timeout)])
    if args.insecure:
        command.append("--insecure")
    if args.output_format:
        command.extend(["--output-format", args.output_format])
    return command


def resolve_api_key(cli_value: str | None) -> str:
    if cli_value:
        return cli_value
    return os.getenv(API_KEY_ENV, "")


def run_child(command: list[str], output_path: Path, is_json: bool = False) -> int:
    completed = subprocess.run(command)
    if completed.returncode == 0 and not is_json:
        print(output_path)
    return completed.returncode


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    is_json = args.output_format == "json"

    if args.command == "text-to-image":
        output_path = timestamped_output(TEXT_TO_IMAGE_PREFIX)
        command = [
            sys.executable,
            str(SCRIPT_DIR / "text_to_image_request.py"),
            "--prompt",
            args.prompt,
            "--negative-prompt",
            args.negative_prompt,
            "--image-size",
            args.image_size,
            "--aspect-ratio",
            args.aspect_ratio,
            "--save-path",
            str(output_path),
        ]
        command = add_common_args(command, args)
        return run_child(command, output_path, is_json)

    output_path = timestamped_output(IMAGE_EDIT_PREFIX)
    command = [
        sys.executable,
        str(SCRIPT_DIR / "image_edit_request.py"),
        "--image",
        args.image,
        "--prompt",
        args.prompt,
        "--save-path",
        str(output_path),
    ]
    command = add_common_args(command, args)
    return run_child(command, output_path, is_json)


if __name__ == "__main__":
    raise SystemExit(main())
