#!/usr/bin/env python3
"""
执行完整的报关工作流：上传 → 分类 → 报关 → 下载

用法:
  python scripts/customs_workflow.py <file_path> [--output-dir ./output]
  python scripts/customs_workflow.py <file_path> --skip-confirm

零外部依赖 — 仅使用 Python 标准库。
"""
import json
import mimetypes
import os
import sys
import time
import uuid
import argparse
import urllib.request
import urllib.error
from pathlib import Path

CREDENTIALS_PATH = Path.home() / ".config" / "openclaw" / "credentials"
DEFAULT_BASE_URL = "https://platform.daofeiai.com"


def load_credentials():
    if not CREDENTIALS_PATH.exists():
        return
    for line in CREDENTIALS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def _encode_multipart(files: dict) -> tuple:
    """手动编码 multipart/form-data，无需第三方库"""
    boundary = uuid.uuid4().hex
    body = b""
    for field_name, (filename, data, content_type) in files.items():
        body += f"--{boundary}\r\n".encode()
        body += (
            f'Content-Disposition: form-data; name="{field_name}"; '
            f'filename="{filename}"\r\n'
        ).encode()
        body += f"Content-Type: {content_type}\r\n\r\n".encode()
        body += data + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return body, f"multipart/form-data; boundary={boundary}"


def _request(method: str, url: str, api_key: str,
             json_body=None, multipart=None, timeout: int = 120) -> dict:
    """通用 HTTP 请求，支持 JSON 和 multipart"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif multipart is not None:
        data, ct = _encode_multipart(multipart)
        headers["Content-Type"] = ct
    else:
        data = None

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"连接失败: {e}")


class CustomsWorkflow:
    def __init__(self, base_url: str = None, api_key: str = None):
        load_credentials()
        self.api_key = api_key or os.environ.get("LEAP_API_KEY", "")
        self.base_url = base_url or os.environ.get("LEAP_API_BASE_URL", DEFAULT_BASE_URL)

        if not self.api_key:
            raise ValueError(
                "LEAP_API_KEY 未配置。\n"
                "  方式1（推荐）：在 OpenClaw skill 设置界面配置 LEAP_API_KEY 环境变量\n"
                "  方式2（备用）：运行 python scripts/setup.py"
            )

    def upload_file(self, file_path: str) -> dict:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        print(f"📤 上传文件: {path.name}", file=sys.stderr)
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"

        result = _request(
            "POST",
            f"{self.base_url}/api/v1/files/upload",
            self.api_key,
            multipart={"file": (path.name, path.read_bytes(), mime)},
        )
        print(f"✅ 上传成功: file_id={result['file_id']}", file=sys.stderr)
        return result

    def classify(self, file_id: str) -> dict:
        print(f"🔍 提交分类: {file_id}", file=sys.stderr)
        task = _request(
            "POST",
            f"{self.base_url}/api/v1/process",
            self.api_key,
            json_body={"file_id": file_id, "output": "classify_fast"},
        )
        print(f"⏳ 分类任务已提交: result_id={task['result_id']}", file=sys.stderr)
        return self._poll(task["result_id"])

    def submit_customs(self, files_with_segments: list) -> dict:
        print("📋 提交报关任务...", file=sys.stderr)
        task = _request(
            "POST",
            f"{self.base_url}/api/v1/process",
            self.api_key,
            json_body={"output": "customs", "params": {"files": files_with_segments}},
        )
        print(f"⏳ 报关任务已提交: result_id={task['result_id']}", file=sys.stderr)
        return self._poll(task["result_id"])

    def download_result(self, result_id: str, filename: str, output_dir: str = "."):
        url = f"{self.base_url}/api/v1/results/{result_id}/files/{filename}"
        output_path = Path(output_dir) / filename
        print(f"📥 下载: {filename}", file=sys.stderr)

        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(resp.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"下载失败 HTTP {e.code}: {e.read().decode('utf-8', 'replace')}")

        print(f"✅ 已保存: {output_path}", file=sys.stderr)
        return str(output_path)

    def _poll(self, result_id: str, interval: int = 8, max_wait: int = 300) -> dict:
        url = f"{self.base_url}/api/v1/process/tasks/{result_id}"
        start = time.time()
        time.sleep(5)

        while True:
            elapsed = int(time.time() - start)
            if elapsed > max_wait:
                raise TimeoutError(f"轮询超时（{max_wait}s）: result_id={result_id}")

            data = _request("GET", url, self.api_key)
            status = data.get("status", "unknown")
            progress = data.get("progress", 0)
            print(f"  [{elapsed}s] {status} ({progress}%)", file=sys.stderr)

            if status == "completed":
                return data
            if status == "failed":
                raise RuntimeError(f"任务失败: {data.get('error_message', '未知错误')}")

            time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="报关工作流")
    parser.add_argument("file_path", help="待处理的文件路径")
    parser.add_argument("--output-dir", default="./output", help="结果输出目录，默认 ./output")
    parser.add_argument("--skip-confirm", action="store_true", help="跳过分类确认（自动使用分类结果）")
    args = parser.parse_args()

    wf = CustomsWorkflow()

    upload_result = wf.upload_file(args.file_path)
    file_id = upload_result["file_id"]

    classify_result = wf.classify(file_id)
    files_data = classify_result.get("result_data", {}).get("files", [])

    print("\n📋 分类结果:", file=sys.stderr)
    for f in files_data:
        print(f"  文件: {f.get('file_name', 'unknown')}", file=sys.stderr)
        for i, seg in enumerate(f.get("segments", []), 1):
            pages = seg.get("pages", [])
            print(
                f"    分片{i}: {seg.get('file_type')} "
                f"(置信度: {seg.get('confidence', 0):.0%})"
                + (f" 页码: {pages}" if pages else ""),
                file=sys.stderr,
            )

    if not args.skip_confirm:
        print("\n请确认分类结果后按 Enter 继续...", file=sys.stderr)
        input()

    files_with_segments = [
        {"file_id": f["file_id"], "file_name": f.get("file_name", ""), "segments": f.get("segments", [])}
        for f in files_data
    ]
    customs_result = wf.submit_customs(files_with_segments)

    for of in customs_result.get("result_data", {}).get("output_files", []):
        filename = of.get("file_name", "")
        if filename:
            wf.download_result(customs_result.get("result_id", ""), filename, args.output_dir)

    print(json.dumps(customs_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
