#!/usr/bin/env python3
import sys
import os
import re
import json
import uuid
import mimetypes
from pathlib import Path
from urllib.parse import urlparse, unquote

import requests
import markdown
from weasyprint import HTML

API_URL = "https://api.aidso.com/openapi/skills/band_report/md"
API_KEY_URL = "https://geo.aidso.com/setting?type=apiKey&platform=GEO"
COMPLETE_ANALYSIS_URL = "https://geo.aidso.com/completeAnalysis"
GEO_HOME_URL = "https://geo.aidso.com"
PURCHASE_POINTS_URL = "https://geo.aidso.com"

STATE_DIR = Path(os.environ.get("AIDSO_STATE_DIR", str(Path(__file__).resolve().parent / ".state")))
STATE_FILE = STATE_DIR / "bindings.json"

CONFIRM_WORDS = {"确认", "是", "好的", "好", "继续", "yes", "y", "ok", "确认使用"}
CANCEL_WORDS = {"取消", "不", "否", "no", "n"}
CHECK_RESULT_WORDS = {"继续", "查看结果", "查询结果", "结果", "report status", "check result"}

PDF_CSS = """
body {
  font-family: Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
  font-size: 12px;
  line-height: 1.7;
  color: #222;
  padding: 24px;
}
h1, h2, h3, h4 {
  color: #111;
  margin-top: 20px;
  margin-bottom: 10px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0 20px 0;
  font-size: 11px;
}
th, td {
  border: 1px solid #d9d9d9;
  padding: 8px 10px;
  vertical-align: top;
  text-align: left;
}
th { background: #f5f5f5; }
code {
  background: #f6f8fa;
  padding: 2px 4px;
  border-radius: 4px;
}
pre {
  background: #f6f8fa;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
}
blockquote {
  border-left: 4px solid #ddd;
  margin: 12px 0;
  padding: 8px 12px;
  color: #555;
  background: #fafafa;
}
"""

def out_text(msg):
    print(msg, flush=True)

def out_media(path):
    print(f"MEDIA:{path}", flush=True)
    sys.exit(0)

def out_debug(msg):
    print(msg, file=sys.stderr, flush=True)

def first_use_upgrade_note():
    return (
        "欢迎使用 AIDSO 虾搜GEO品牌诊断技能。后续技能将持续更新，包括："
        "AI问题生成、GEO持续监测、根据监测优化建议生成素材等，欢迎关注后续更新。"
    )

def binding_prompt(include_upgrade_note=False):
    text = f"首次使用需要绑定爱搜账号，请输入你在后台创建的API key 完成绑定。获取地址：{API_KEY_URL}"
    if include_upgrade_note:
        text += "\\n\\n" + first_use_upgrade_note()
    return text

def custom_need_tip():
    return f"如有其他自定义诊断需求，可前往官网查看：{GEO_HOME_URL}"

def pending_extra_tip():
    return f"如果报告长时间未生成，也可以前往官网查看：{COMPLETE_ANALYSIS_URL}"

def format_backend_error_message(msg):
    if not msg:
        return ""
    if "积分不足" in msg:
        return f"{msg}\\n请前往{PURCHASE_POINTS_URL} 购买积分"
    return msg

def ensure_state():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        STATE_FILE.write_text("{}", encoding="utf-8")

def load_state():
    ensure_state()
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_state(data):
    ensure_state()
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def get_user_id():
    return os.environ.get("OPENCLAW_USER_ID") or os.environ.get("USER_ID") or os.environ.get("CHAT_USER_ID") or "default_user"

def get_user_state(all_state, user_id):
    if user_id not in all_state:
        all_state[user_id] = {
            "api_key": None,
            "awaiting_api_key": False,
            "awaiting_confirmation": False,
            "pending_brand": None,
            "pending_check_count": 0,
            "welcome_shown": False
        }
    return all_state[user_id]

def has_api_key(state):
    v = state.get("api_key")
    return isinstance(v, str) and bool(v.strip())

def clear_pending(state):
    state["pending_brand"] = None
    state["pending_check_count"] = 0

def safe_report_filename(ext):
    if not ext:
        ext = ".dat"
    if not ext.startswith("."):
        ext = "." + ext
    return f"geo_report_{uuid.uuid4().hex}{ext}"

def guess_ext_from_content_type(content_type):
    content_type = (content_type or "").split(";")[0].strip().lower()
    mapping = {
        "application/pdf": ".pdf",
        "text/markdown": ".md",
        "text/plain": ".txt",
        "application/json": ".json",
        "text/html": ".html",
        "application/octet-stream": ".bin",
    }
    if content_type in mapping:
        return mapping[content_type]
    return mimetypes.guess_extension(content_type) or ""

def save_bytes_to_temp(content, filename):
    out_path = Path("/tmp") / filename
    out_path.write_bytes(content)
    return str(out_path)

def build_auth_headers(api_key):
    return {"x-api-key": api_key}

def normalize_code(code):
    if code is None:
        return None
    try:
        return int(code)
    except Exception:
        return code

def get_backend_msg(data):
    if not isinstance(data, dict):
        return ""
    msg = data.get("msg")
    if isinstance(msg, str) and msg.strip():
        return msg.strip()
    message = data.get("message")
    if isinstance(message, str) and message.strip():
        return message.strip()
    return ""

def is_invalid_token_response(data):
    if not isinstance(data, dict):
        return False
    return normalize_code(data.get("code")) == 401 and "invalid token" in get_backend_msg(data).lower()

def is_processing_response(data):
    if not isinstance(data, dict):
        return False
    code = normalize_code(data.get("code"))
    msg = get_backend_msg(data).lower()
    return code == 200 and ("处理中" in msg or "processing" in msg or "请稍后" in msg)

def is_success_response(data):
    if not isinstance(data, dict):
        return False
    code = normalize_code(data.get("code"))
    return code in (None, 0, 200, "0", "200")

def raise_backend_error_if_any(data):
    if not isinstance(data, dict):
        return
    if is_invalid_token_response(data) or is_processing_response(data) or is_success_response(data):
        return
    msg = get_backend_msg(data)
    if msg:
        raise ValueError(format_backend_error_message(msg))
    raise ValueError(f"API 返回错误：{data}")

def parse_json_utf8(resp):
    raw = resp.content
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        pass
    try:
        return resp.json()
    except Exception:
        pass
    text = resp.text
    return json.loads(text)

def extract_file_url_from_json(data):
    if not isinstance(data, dict):
        return None
    data_field = data.get("data")
    if isinstance(data_field, str) and data_field.strip() and (data_field.startswith("http://") or data_field.startswith("https://")):
        return data_field.strip()
    if isinstance(data_field, dict):
        for key in ("url", "fileUrl", "downloadUrl", "mdUrl", "pdfUrl", "reportUrl"):
            v = data_field.get(key)
            if isinstance(v, str) and v.strip() and (v.startswith("http://") or v.startswith("https://")):
                return v.strip()
    return None

def infer_ext_from_url(url):
    try:
        path = unquote(urlparse(url).path)
        suffix = Path(path).suffix
        return suffix.lower() if suffix else ""
    except Exception:
        return ""

def looks_like_md_link(url):
    return infer_ext_from_url(url) == ".md"

def looks_like_pdf_link(url):
    return infer_ext_from_url(url) == ".pdf"

def fetch_url_response(url, auth_headers=None):
    attempts = []
    if auth_headers:
        attempts.append(auth_headers)
    attempts.append({})
    last_error = None
    for headers in attempts:
        try:
            resp = requests.get(url, headers=headers, timeout=60, allow_redirects=True)
            if resp.status_code == 200:
                return resp
            last_error = f"HTTP {resp.status_code}"
        except Exception as e:
            last_error = str(e)
    raise ValueError(f"获取文件失败：{last_error or '未知错误'}")

def download_remote_file(url, auth_headers=None):
    resp = fetch_url_response(url, auth_headers=auth_headers)
    text_ct = (resp.headers.get("Content-Type") or "").lower()
    text_sample = resp.text[:1000] if ("text" in text_ct or "json" in text_ct) else ""
    invalid_markers = ["NoSuchKey", "The specified key does not exist", '"Code":"NoSuchKey"', "'Code': 'NoSuchKey'"]
    if any(marker in text_sample for marker in invalid_markers):
        raise ValueError("下载报告文件失败：NoSuchKey")
    ext = guess_ext_from_content_type(text_ct) or infer_ext_from_url(url) or ".dat"
    filename = safe_report_filename(ext)
    local_path = save_bytes_to_temp(resp.content, filename)
    out_debug(f"[DEBUG] downloaded file path={local_path} exists={Path(local_path).exists()}")
    return local_path

def fetch_markdown_text(url, auth_headers=None):
    resp = fetch_url_response(url, auth_headers=auth_headers)
    text = resp.text.strip()
    if not text:
        raise ValueError("md 文件内容为空")
    invalid_markers = ["NoSuchKey", "The specified key does not exist", '"Code":"NoSuchKey"', "'Code': 'NoSuchKey'"]
    if any(marker in text[:1000] for marker in invalid_markers):
        raise ValueError("md 文件不存在：NoSuchKey")
    return text

def render_markdown_to_pdf(md_text):
    html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "toc"])
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>GEO诊断报告</title>
<style>{PDF_CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""
    out_path = str(Path("/tmp") / safe_report_filename(".pdf"))
    HTML(string=html).write_pdf(out_path)
    out_debug(f"[DEBUG] rendered pdf path={out_path} exists={Path(out_path).exists()}")
    return out_path

def extract_brand_from_message(message):
    message = message.strip()
    patterns = [
        r"帮我做一个(.+?)的GEO诊断报告",
        r"做一个(.+?)的GEO诊断报告",
        r"生成(.+?)的GEO诊断报告",
        r"(.+?)的GEO诊断报告",
    ]
    for p in patterns:
        m = re.search(p, message, flags=re.I)
        if m:
            brand = m.group(1).strip().strip("“”\"'")
            if brand:
                return brand
    return None

def looks_like_api_key(message):
    text = message.strip()
    if not text:
        return False
    if len(text) >= 16 and "\\n" not in text and " " not in text:
        return True
    if text.lower().startswith(("sk-", "aidso_", "api_")):
        return True
    return False

def request_report(brand, api_key):
    resp = requests.get(API_URL, params={"brandName": brand}, headers=build_auth_headers(api_key), timeout=180)
    resp.raise_for_status()
    content_type = (resp.headers.get("Content-Type") or "").lower()
    if "application/json" not in content_type:
        return {"kind": "raw", "content_type": content_type, "bytes": resp.content}
    return {"kind": "json", "data": parse_json_utf8(resp)}

def build_success_file(payload, api_key):
    headers = build_auth_headers(api_key)
    if payload.get("kind") == "raw":
        ext = guess_ext_from_content_type(payload.get("content_type") or "") or ".dat"
        return save_bytes_to_temp(payload["bytes"], safe_report_filename(ext))
    data = payload["data"]
    file_url = extract_file_url_from_json(data)
    if not file_url:
        backend_msg = get_backend_msg(data)
        if backend_msg:
            raise ValueError(format_backend_error_message(backend_msg))
        raise ValueError(f"接口未返回有效文件链接：{data}")
    if looks_like_pdf_link(file_url):
        return download_remote_file(file_url, auth_headers=headers)
    if looks_like_md_link(file_url):
        md_text = fetch_markdown_text(file_url, auth_headers=headers)
        return render_markdown_to_pdf(md_text)
    remote_resp = fetch_url_response(file_url, auth_headers=headers)
    remote_ct = (remote_resp.headers.get("Content-Type") or "").lower()
    if "markdown" in remote_ct or "text/plain" in remote_ct or infer_ext_from_url(file_url) == ".md":
        md_text = remote_resp.text.strip()
        return render_markdown_to_pdf(md_text)
    ext = guess_ext_from_content_type(remote_ct) or infer_ext_from_url(file_url) or ".dat"
    return save_bytes_to_temp(remote_resp.content, safe_report_filename(ext))

def handle_one_query(state):
    brand = state.get("pending_brand")
    api_key = state.get("api_key")
    if not brand:
        return ("text", "当前没有待查询的诊断任务，请重新发起品牌诊断请求。")
    if not api_key:
        state["awaiting_api_key"] = True
        clear_pending(state)
        return ("text", f"当前绑定的 API key 已失效，请重新输入你在后台创建的 API key 完成绑定。获取地址：{API_KEY_URL}")

    result = request_report(brand, api_key)
    if result["kind"] == "json":
        data = result["data"]
        if is_invalid_token_response(data):
            state["api_key"] = None
            state["awaiting_api_key"] = True
            clear_pending(state)
            return ("text", f"当前绑定的 API key 已失效，请重新输入你在后台创建的 API key 完成绑定。获取地址：{API_KEY_URL}")
        if is_processing_response(data):
            state["pending_check_count"] = int(state.get("pending_check_count") or 0) + 1
            msg = "诊断报告生成中，大约需要3~10分钟，请稍后..."
            if state["pending_check_count"] >= 3:
                msg += "\\n\\n" + pending_extra_tip()
            return ("text", msg)
        raise_backend_error_if_any(data)

    local_file = build_success_file(result, api_key)
    clear_pending(state)
    return ("media", local_file)

def main():
    if len(sys.argv) < 2:
        print("请输入你的请求内容。", file=sys.stderr)
        sys.exit(1)

    user_message = sys.argv[1].strip()
    if not user_message:
        print("请输入你的请求内容。", file=sys.stderr)
        sys.exit(1)

    all_state = load_state()
    user_id = get_user_id()
    state = get_user_state(all_state, user_id)
    lower_msg = user_message.lower()

    try:
        if lower_msg in {w.lower() for w in CANCEL_WORDS}:
            state["awaiting_confirmation"] = False
            clear_pending(state)
            save_state(all_state)
            out_text("已取消本次诊断。")
            return

        if state.get("awaiting_api_key"):
            if not looks_like_api_key(user_message):
                include_upgrade_note = not state.get("welcome_shown")
                state["welcome_shown"] = True
                save_state(all_state)
                out_text(binding_prompt(include_upgrade_note=include_upgrade_note))
                return
            state["api_key"] = user_message.strip()
            state["awaiting_api_key"] = False
            state["awaiting_confirmation"] = True if state.get("pending_brand") else False
            save_state(all_state)
            if state["awaiting_confirmation"]:
                out_text("绑定成功，以后可直接使用AIDSO 虾搜GEO品牌诊断技能，此次诊断将消耗20积分，是否确认？")
            else:
                out_text("绑定成功，以后可直接使用AIDSO 虾搜GEO品牌诊断技能。\\n\\n" + custom_need_tip())
            return

        if lower_msg in {w.lower() for w in CHECK_RESULT_WORDS} and state.get("pending_brand"):
            kind, payload = handle_one_query(state)
            save_state(all_state)
            if kind == "media":
                out_media(payload)
            else:
                out_text(payload)
            return

        if state.get("awaiting_confirmation"):
            if not has_api_key(state):
                state["awaiting_api_key"] = True
                state["awaiting_confirmation"] = False
                include_upgrade_note = not state.get("welcome_shown")
                state["welcome_shown"] = True
                save_state(all_state)
                out_text(binding_prompt(include_upgrade_note=include_upgrade_note))
                return
            if lower_msg in {w.lower() for w in CONFIRM_WORDS}:
                kind, payload = handle_one_query(state)
                state["awaiting_confirmation"] = False
                save_state(all_state)
                if kind == "media":
                    out_media(payload)
                else:
                    out_text(payload)
                return

            out_text("此次诊断将消耗20积分，是否确认？")
            return

        brand = extract_brand_from_message(user_message)
        if brand:
            state["pending_brand"] = brand
            state["pending_check_count"] = 0
            if not has_api_key(state):
                state["awaiting_api_key"] = True
                state["awaiting_confirmation"] = False
                include_upgrade_note = not state.get("welcome_shown")
                state["welcome_shown"] = True
                save_state(all_state)
                out_text(binding_prompt(include_upgrade_note=include_upgrade_note))
                return
            state["awaiting_confirmation"] = True
            save_state(all_state)
            out_text("此次诊断将消耗20积分，是否确认？")
            return

        if looks_like_api_key(user_message) and not has_api_key(state):
            state["api_key"] = user_message.strip()
            state["awaiting_api_key"] = False
            state["awaiting_confirmation"] = bool(state.get("pending_brand"))
            save_state(all_state)
            if state["awaiting_confirmation"]:
                out_text("绑定成功，以后可直接使用AIDSO 虾搜GEO品牌诊断技能，此次诊断将消耗20积分，是否确认？")
            else:
                out_text("绑定成功，以后可直接使用AIDSO 虾搜GEO品牌诊断技能。\\n\\n" + custom_need_tip())
            return

        if lower_msg in {"继续", "确认", "yes", "y", "ok"} and not has_api_key(state):
            state["awaiting_api_key"] = True
            include_upgrade_note = not state.get("welcome_shown")
            state["welcome_shown"] = True
            save_state(all_state)
            out_text(binding_prompt(include_upgrade_note=include_upgrade_note))
            return

        out_text("请输入类似“帮我做一个露露的GEO诊断报告”的请求。\\n\\n" + custom_need_tip())
    except ValueError as e:
        out_text(str(e))
        return
    except Exception as e:
        print(f"技能执行失败：{e}", file=sys.stderr, flush=True)
        sys.exit(2)

if __name__ == "__main__":
    main()
