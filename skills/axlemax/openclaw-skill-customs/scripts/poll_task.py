#!/usr/bin/env python3
"""
轮询 Leap 任务状态直到完成或超时。
用法:
  python scripts/poll_task.py <result_id>
  python scripts/poll_task.py <result_id> --interval 8 --max-wait 300

退出码:
  0  任务 completed（结果 JSON 输出到 stdout）
  1  任务 failed 或超时（错误信息输出到 stdout）

零外部依赖 — 仅使用 Python 标准库。
"""
import json
import os
import sys
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path

CREDENTIALS_PATH = Path.home() / ".config" / "openclaw" / "credentials"
DEFAULT_BASE_URL = "https://platform.daofeiai.com"


def load_credentials():
    """自动从 credentials 文件加载配置（不覆盖已有环境变量）"""
    if not CREDENTIALS_PATH.exists():
        return
    for line in CREDENTIALS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def get_json(url: str, api_key: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"连接失败: {e}")


def poll_task(result_id: str, interval: int = 8, max_wait: int = 300):
    load_credentials()
    api_key = os.environ.get("LEAP_API_KEY", "")
    base_url = os.environ.get("LEAP_API_BASE_URL", DEFAULT_BASE_URL)

    if not api_key:
        print(json.dumps({
            "status": "error",
            "error_message": (
                "LEAP_API_KEY 未配置。\n"
                "方式1（推荐）：在 OpenClaw skill 设置界面配置 LEAP_API_KEY 环境变量\n"
                "方式2（备用）：运行 python scripts/setup.py"
            )
        }, ensure_ascii=False, indent=2))
        return None

    url = f"{base_url}/api/v1/process/tasks/{result_id}"
    start_time = time.time()

    # 首次等待
    time.sleep(5)

    attempt = 0
    while True:
        attempt += 1
        elapsed = int(time.time() - start_time)

        if elapsed > max_wait:
            result = {
                "status": "timeout",
                "result_id": result_id,
                "elapsed_seconds": elapsed,
                "message": f"等待超过 {max_wait} 秒，任务可能仍在执行中。",
                "manual_check": f'curl -H "Authorization: Bearer $LEAP_API_KEY" "{url}"',
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return None

        try:
            data = get_json(url, api_key)
            status = data.get("status", "unknown")
            progress = data.get("progress", 0)

            # 结构化进度输出到 stderr（Agent 读取用于驱动互动话术）
            progress_info = {
                "poll_attempt": attempt,
                "elapsed_seconds": elapsed,
                "status": status,
                "progress": progress,
            }
            print(json.dumps(progress_info, ensure_ascii=False), file=sys.stderr)

            if status == "completed":
                print(json.dumps(data, ensure_ascii=False, indent=2))
                return data

            if status == "failed":
                result = {
                    "status": "failed",
                    "error_message": data.get("error_message", "未知错误"),
                    "result_id": result_id,
                    "elapsed_seconds": elapsed,
                    "suggestion": "请检查上传文件是否完整，或尝试重新提交任务。",
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return None

        except RuntimeError as e:
            err_str = str(e)
            if "404" in err_str:
                print(json.dumps({
                    "status": "error",
                    "error_message": f"任务不存在: {result_id}，请检查 result_id 是否正确"
                }, ensure_ascii=False, indent=2))
                return None
            print(json.dumps({
                "poll_attempt": attempt,
                "elapsed_seconds": elapsed,
                "error": err_str
            }, ensure_ascii=False), file=sys.stderr)

        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="轮询 Leap 任务状态")
    parser.add_argument("result_id", help="任务结果 ID (result_id)")
    parser.add_argument("--interval", type=int, default=8, help="轮询间隔（秒），默认 8")
    parser.add_argument("--max-wait", type=int, default=300, help="最长等待秒数，默认 300")
    args = parser.parse_args()

    result = poll_task(args.result_id, args.interval, args.max_wait)
    sys.exit(0 if result and result.get("status") == "completed" else 1)


if __name__ == "__main__":
    main()
