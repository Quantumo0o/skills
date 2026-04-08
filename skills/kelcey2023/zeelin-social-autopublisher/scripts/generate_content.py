#!/usr/bin/env python3
"""
THUQX AutoOps for OpenClaw 0.5 — 根据主题生成四平台文案，输出 JSON 到 stdout（供 run_social_ops_v5.sh 解析）。
与 OpenClaw skill zeelin-social-autopublisher 内脚本保持一致。

通义千问：设置环境变量 DASHSCOPE_API_KEY 或 QWEN_API_KEY（阿里云 DashScope）。
可选：QWEN_API_BASE（默认 DashScope 兼容模式）、QWEN_MODEL（默认 qwen-turbo）。
未配置 Key 时回退为本地模板文案。
"""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

topic = sys.argv[1] if len(sys.argv) > 1 else "AI认知债务"

_SCRIPT_DIR = Path(__file__).resolve().parent
_HANDBOOK_NAME = "四大平台内容生产提示词手册.md"


def _load_prompt_handbook() -> str:
    """Load bundled 四大平台手册；与 generate_content.py 同目录。"""
    path = _SCRIPT_DIR / _HANDBOOK_NAME
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""

# 千问 / DashScope（兼容 OpenAI Chat Completions）
QWEN_API_BASE = os.environ.get(
    "QWEN_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1"
).rstrip("/")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen-turbo")
DASHSCOPE_API_KEY = (
    os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("QWEN_API_KEY") or ""
).strip()
# 若系统 CA 不完整（如 macOS 自带 Python），设为 1 时在意图错误校验失败回退到不校验证书（仅建议本机调试）
QWEN_INSECURE_SSL = os.environ.get("QWEN_INSECURE_SSL", "").strip() in ("1", "true", "yes")


def _https_open(req: urllib.request.Request, timeout: int):
    def ctx_default():
        try:
            import certifi  # type: ignore

            return ssl.create_default_context(cafile=certifi.where())
        except Exception:
            return ssl.create_default_context()

    try:
        return urllib.request.urlopen(req, timeout=timeout, context=ctx_default())
    except urllib.error.URLError as e:
        reason = getattr(e, "reason", e)
        ssl_bad = isinstance(reason, ssl.SSLError) and (
            "CERTIFICATE_VERIFY_FAILED" in str(reason)
            or "certificate verify failed" in str(reason).lower()
        )
        if ssl_bad and QWEN_INSECURE_SSL:
            ctx = ssl._create_unverified_context()
            return urllib.request.urlopen(req, timeout=timeout, context=ctx)
        if ssl_bad and not QWEN_INSECURE_SSL:
            print(
                "[generate_content] SSL 证书校验失败，已回退模板。"
                "可安装 certifi、运行 Python「Install Certificates」"
                "或临时设置 QWEN_INSECURE_SSL=1。",
                file=sys.stderr,
            )
        raise


def web_search_materials(q: str, max_items: int = 5) -> list[dict]:
    """
    Basic web search step for reference materials (no key required).
    Tries DuckDuckGo HTML endpoint and extracts top result titles/urls.
    Returns [] on failure.
    """
    try:
        url = "https://duckduckgo.com/html/?" + urllib.parse.urlencode({"q": q})
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode("utf-8", errors="ignore")

        items: list[dict] = []
        for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html):
            href = m.group(1)
            title = re.sub(r"<.*?>", "", m.group(2)).strip()
            if not title:
                continue
            items.append({"title": title[:140], "url": href[:300]})
            if len(items) >= max_items:
                break
        return items
    except Exception:
        return []


materials = web_search_materials(topic)
extra = web_search_materials(f"{topic} 选手 赛果", max_items=3)
seen = {m["url"] for m in materials}
for it in extra:
    if it["url"] not in seen:
        materials.append(it)
        seen.add(it["url"])
    if len(materials) >= 8:
        break

materials_text = ""
if materials:
    bullets = [f"- {it['title']} ({it['url']})" for it in materials]
    materials_text = "参考素材（公开网页摘要，写作时请核对；与主题冲突则以可验证事实为准）：\n" + "\n".join(
        bullets
    )

REQUIRED_KEYS = (
    "twitter",
    "weibo",
    "xhs_title",
    "xhs_body",
    "wechat_title",
    "wechat_body",
)

_ALLOW_TEMPLATE = os.environ.get("THUQX_ALLOW_TEMPLATE_FALLBACK", "").strip() in (
    "1",
    "true",
    "yes",
)

_BAD_PHRASE = re.compile(
    r"Auto\s*Ops|自动发布|本推文由|本文由|本条由",
    re.IGNORECASE,
)

# 核心约束（与《四大平台内容生产提示词手册》叠加；手册在同名 .md 文件中）
_QWEN_SYSTEM_CORE = """你是资深全媒体主编。只输出一个 JSON 对象，不要 Markdown、不要代码围栏、不要解释性文字。
JSON 必须包含且仅包含这六个字符串键：twitter, weibo, xhs_title, xhs_body, wechat_title, wechat_body。
每个键对应一条「最终可发布」的定稿（不是多组 A/B/C，从中各选一个最佳写法即可）。

【事实与人称】
- 紧扣用户「主题」与「参考素材」。素材充足时写清事件、队伍、赛果节点；不足时保守表述，不捏造比分/时间/奖项。
- 主题涉及真实人物：以参考素材为准判断性别与身份；素材未明示时禁止凭名字猜「她/他」，优先「选手+姓名」、重复姓名或省略代词。

【禁止】所有字段严禁：「Auto Ops」「自动发布」「本推文由」「本文由」等脚注；严禁「我觉得」「我相信」等空洞开头；手册要求各平台一律不用表情符号（不要用 emoji）。

【按手册落实 — 与各字段对应关系】
- twitter：全英文。严格用手册「推特」节的钩子公式（反认知/提问/数字极限/对比对立/损失厌恶至少一种）+「模式A｜单条金句」结构（钩子+事实或画面支撑+互动反问）；1-3 个 #Hashtag#；总长 ≤ 280 字符；禁止中文。
- weibo：全中文。用手册「微博」开篇钩子 +「模式A｜热搜体短微博」取向，300-800 字；多短段；含传播型金句；结尾有互动（反问/评论区召唤）；2-3 个 #话题#（双井号格式）。
- xhs_title + xhs_body：全中文。标题用手册「封面标题公式」（数字/反认知/痛点+实用信号等）；正文 500-1000 字，用手册「干货清单型」或「知识科普型」取向之一（痛点→方案→步骤/类比具象）；结尾带 5-10 个搜索向 #标签#（空格或换行分隔均可）。
- wechat_title + wechat_body：全中文。标题用手册公众号「标题公式」之一（反认知/警告价值/数字等）；正文 1500-3000 字，「观点型深度」或「故事型深度」取向：分段清晰、有画面与类比、至少 2 句可截图传播的金句、末段可自然引导转发（勿出现手册禁止的脚注）。"""


def _build_system_prompt() -> str:
    hb = _load_prompt_handbook()
    max_chars = int(os.environ.get("THUQX_PROMPT_HANDBOOK_MAX_CHARS", "0") or 0)
    if max_chars > 0 and len(hb) > max_chars:
        hb = hb[:max_chars] + "\n\n…（手册已截断，可提高 THUQX_PROMPT_HANDBOOK_MAX_CHARS 或去掉截断）"
    if hb.strip():
        return (
            _QWEN_SYSTEM_CORE
            + "\n\n【《四大平台内容生产提示词手册》全文 — 你必须遵守其中公式、结构、禁忌，除上文「每条一键出稿」约束外不另生成多组模式】\n\n"
            + hb.strip()
        )
    return (
        _QWEN_SYSTEM_CORE
        + "\n\n（未找到同目录 "
        + _HANDBOOK_NAME
        + "，请将该文件放在 scripts 目录以获得完整爆款公式。）"
    )


def _parse_llm_json_block(text: str):
    text = (text or "").strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence:
        text = fence.group(1).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    out = {}
    for k in REQUIRED_KEYS:
        if k not in data or not str(data[k]).strip():
            return None
        out[k] = str(data[k]).strip()
    return out


def _sanitize_platform_text(s: str) -> str:
    s = _BAD_PHRASE.sub("", s or "")
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def generate_with_qwen() -> dict | None:
    if not DASHSCOPE_API_KEY:
        return None
    url = f"{QWEN_API_BASE}/chat/completions"
    user_block = f"""用户主题：{topic}

{materials_text if materials_text else "（当前无可用网页摘要：请仅根据主题做合理、克制的推断，避免捏造具体事实；人物性别不明时请用中性称呼。）"}

请严格按 system 规则，为主题生成六个平台稿件，输出单个 JSON 对象（仅该对象，无其它字符）。"""
    payload = json.dumps(
        {
            "model": QWEN_MODEL,
            "messages": [
                {"role": "system", "content": _build_system_prompt()},
                {"role": "user", "content": user_block},
            ],
            "temperature": 0.65,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        },
        method="POST",
    )
    try:
        with _https_open(req, 180) as resp:
            raw = json.loads(resp.read().decode("utf-8", errors="ignore"))
        reply = raw["choices"][0]["message"]["content"]
        parsed = _parse_llm_json_block(reply)
        if parsed:
            for k in REQUIRED_KEYS:
                parsed[k] = _sanitize_platform_text(parsed[k])
            return parsed
        return None
    except Exception as e:
        if os.environ.get("THUQX_DEBUG_LLM", "").strip() in ("1", "true", "yes"):
            print(f"[generate_content] LLM error: {e}", file=sys.stderr)
        return None


def _trim_for_twitter(text: str, max_len: int = 280) -> str:
    text = (text or "").strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


content = generate_with_qwen()

if not content and DASHSCOPE_API_KEY and not _ALLOW_TEMPLATE:
    print(
        "[generate_content] 通义千问生成失败或解析失败。请检查 API Key、网络与 QWEN_INSECURE_SSL；"
        "或临时设置 THUQX_ALLOW_TEMPLATE_FALLBACK=1 使用本地模板。",
        file=sys.stderr,
    )
    sys.exit(1)

if not content and not DASHSCOPE_API_KEY and not _ALLOW_TEMPLATE:
    print(
        "[generate_content] 未配置 DASHSCOPE_API_KEY / QWEN_API_KEY。"
        "请配置 ~/.openclaw/zeelin-qwen.env 或导出变量；"
        "调试可设 THUQX_ALLOW_TEMPLATE_FALLBACK=1。",
        file=sys.stderr,
    )
    sys.exit(1)

if content is None:
    content = {}

if not content:
    # 仅当 THUQX_ALLOW_TEMPLATE_FALLBACK=1 且千问不可用时启用；与主题弱相关占位，生产环境请用千问
    mt = (materials_text or "").strip()
    content["twitter"] = _trim_for_twitter(
        f"Quick note on «{topic}»: context matters—tell me what stood out to you. "
        f"(Template fallback — enable Qwen for real copy.) #News #Discussion"
    )
    content["weibo"] = _sanitize_platform_text(
        f"【{topic}】一条模板备用帖：请开启通义千问生成正式微博稿。摘要参考：\n{mt}"[:800]
    )
    content["xhs_title"] = f"{topic}｜模板占位（请用千问）"
    content["xhs_body"] = _sanitize_platform_text(
        f"这是「{topic}」的小红书模板占位正文，用于在无 API 时的兜底；请配置 DashScope 后重试以获得笔记风长文。\n\n{mt}"[
            :1200
        ]
    )
    content["wechat_title"] = f"{topic}：模板占位（建议启用内容生成）"
    content["wechat_body"] = _sanitize_platform_text(
        f"本文为系统模板占位，主题为「{topic}」。正式群发前请使用千问生成长文。\n\n{mt}"[:2500]
    )

if content.get("twitter"):
    content["twitter"] = _trim_for_twitter(_sanitize_platform_text(content["twitter"]))
for _k in ("weibo", "xhs_title", "xhs_body", "wechat_title", "wechat_body"):
    if content.get(_k):
        content[_k] = _sanitize_platform_text(content[_k])

print(json.dumps(content, ensure_ascii=False))
