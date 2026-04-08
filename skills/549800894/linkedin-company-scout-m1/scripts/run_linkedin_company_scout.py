#!/usr/bin/env python3
"""
Automate LinkedIn company collection with Chrome, website email enrichment,
and Google Maps email fallback.

This script is designed for macOS with the normal Google Chrome app installed.
It attaches Selenium to a Chrome instance started with a remote debugging port
so Chrome remains the real browser the user can observe.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import socket
import sqlite3
import subprocess
import sys
import time
import urllib.parse
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


DEFAULT_CHROME_APP = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEFAULT_DB_PATH = str(Path.home() / ".linkedin-company-scout" / "results.db")
EMAIL_RE = re.compile(r"([A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,})", re.IGNORECASE)
CONTACT_PATH_HINTS = (
    "/contact",
    "/contact-us",
    "/about",
    "/about-us",
    "/company",
    "/support",
    "/imprint",
    "/legal",
)
CHINA_MARKERS = (
    "china",
    "beijing",
    "shanghai",
    "shenzhen",
    "guangzhou",
    "hangzhou",
    "chengdu",
    "wuhan",
    "hong kong",
    "taiwan",
    "macau",
    "zhongguo",
    "中国",
)
ALLOWED_INDUSTRY_MARKERS = ("设计服务", "design services")


@dataclass
class CompanyRecord:
    keyword: str
    company_name: str
    company_website: str
    company_intro: str
    industry: str
    location: str
    linkedin_url: str
    email: str
    email_source: str
    notes: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect LinkedIn company profiles and contact emails.")
    parser.add_argument(
        "--keywords",
        required=True,
        help="Comma-separated keywords, for example: 'industrial design,hardware design,smart wearable'",
    )
    parser.add_argument("--count", type=int, default=5, help="Accepted companies per keyword")
    parser.add_argument("--output-dir", default="output", help="Directory for JSON and CSV results")
    parser.add_argument("--chrome-binary", default=DEFAULT_CHROME_APP, help="Path to the Google Chrome binary")
    parser.add_argument("--debug-port", type=int, default=9222, help="Chrome remote debugging port")
    parser.add_argument(
        "--chrome-profile-dir",
        default=str(Path.home() / ".linkedin-company-scout" / "chrome-profile"),
        help="Chrome user data directory for the automation session",
    )
    parser.add_argument(
        "--linkedin-wait-seconds",
        type=int,
        default=180,
        help="How long to wait for the user to log in if LinkedIn shows a login wall",
    )
    parser.add_argument(
        "--page-timeout",
        type=int,
        default=20,
        help="Browser and HTTP timeout in seconds",
    )
    parser.add_argument(
        "--max-search-pages",
        type=int,
        default=50,
        help="Maximum LinkedIn result pages to scan per keyword",
    )
    parser.add_argument(
        "--linkedin-search-origin",
        default="FACETED_SEARCH",
        help="LinkedIn search origin query value",
    )
    parser.add_argument(
        "--industry-company-vertical-id",
        default="99",
        help="LinkedIn industryCompanyVertical numeric id (99=Design Services)",
    )
    parser.add_argument(
        "--no-heartbeat",
        action="store_true",
        help="Skip OpenClaw heartbeat enablement",
    )
    parser.add_argument(
        "--exclude-json",
        default="",
        help="Existing result JSON file used for deduplication across runs",
    )
    parser.add_argument(
        "--db-path",
        default=DEFAULT_DB_PATH,
        help="SQLite database path used for deduplication and resume state",
    )
    parser.add_argument(
        "--disable-db-resume",
        action="store_true",
        help="Do not resume from the last stored page in the database",
    )
    return parser.parse_args()


def run_command(argv: Sequence[str], check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(argv, check=check, capture_output=True, text=True)


def enable_heartbeat(skip: bool) -> Tuple[bool, str]:
    if skip:
        return False, "heartbeat skipped by flag"
    try:
        result = run_command(["openclaw", "system", "heartbeat", "enable"], check=False)
    except FileNotFoundError:
        return False, "openclaw not installed"
    if result.returncode == 0:
        return True, "heartbeat enabled"
    reason = result.stderr.strip() or result.stdout.strip() or f"heartbeat failed with exit {result.returncode}"
    return False, reason


def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def ensure_chrome_debuggable(chrome_binary: str, profile_dir: str, port: int) -> bool:
    if is_port_open(port):
        return False
    profile = Path(profile_dir)
    profile.mkdir(parents=True, exist_ok=True)
    launch_cmd = [
        chrome_binary,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={str(profile)}",
        "--no-first-run",
        "--no-default-browser-check",
        "about:blank",
    ]
    subprocess.Popen(launch_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.time() + 20
    while time.time() < deadline:
        if is_port_open(port):
            return True
        time.sleep(0.5)
    raise RuntimeError("Chrome remote debugging port did not open. Check Chrome launch permissions.")


def create_driver(port: int, timeout: int) -> webdriver.Chrome:
    addresses = (f"127.0.0.1:{port}", f"[::1]:{port}")
    errors: List[str] = []
    for addr in addresses:
        options = Options()
        options.add_experimental_option("debuggerAddress", addr)
        options.page_load_strategy = "eager"
        service = Service(ChromeDriverManager().install())
        try:
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_page_load_timeout(timeout)
            return driver
        except Exception as exc:
            errors.append(f"{addr}: {exc}")
    raise RuntimeError("Unable to attach Chrome debugging session. " + " | ".join(errors))


def ensure_primary_window(driver: webdriver.Chrome) -> None:
    if not driver.window_handles:
        driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[0])


def new_tab(driver: webdriver.Chrome, url: str) -> str:
    driver.switch_to.window(driver.window_handles[0])
    driver.execute_script(f"window.open({json.dumps(url)}, '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    return driver.current_window_handle


def close_current_tab(driver: webdriver.Chrome) -> None:
    if len(driver.window_handles) <= 1:
        return
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def stop_driver_service(driver: webdriver.Chrome) -> None:
    try:
        driver.service.stop()
    except Exception:
        pass


def wait_for_login_if_needed(driver: webdriver.Chrome, wait_seconds: int) -> None:
    current_url = driver.current_url.lower()
    login_markers = ("linkedin.com/uas/login", "linkedin.com/login", "authwall", "checkpoint/challenge")
    if not any(marker in current_url for marker in login_markers):
        return
    print("LinkedIn login required. Complete login in Chrome, then wait for the search page to load.", file=sys.stderr)
    deadline = time.time() + wait_seconds
    while time.time() < deadline:
        url = driver.current_url
        if "search/results/companies" in url or "/company/" in url:
            return
        time.sleep(2)
    raise RuntimeError("Timed out waiting for LinkedIn login.")


def compact_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def reject_china_location(location: str) -> bool:
    value = (location or "").lower()
    return any(marker in value for marker in CHINA_MARKERS)


def is_allowed_industry(industry: str) -> bool:
    value = compact_whitespace(industry).lower()
    if not value:
        return False
    return any(marker in value for marker in ALLOWED_INDUSTRY_MARKERS)


def wait_for_any(driver: webdriver.Chrome, selectors: Sequence[Tuple[str, str]], timeout: int) -> None:
    wait = WebDriverWait(driver, timeout)
    for by, value in selectors:
        try:
            wait.until(EC.presence_of_element_located((by, value)))
            return
        except TimeoutException:
            continue
    raise TimeoutException("None of the expected selectors appeared.")


def safe_get(driver: webdriver.Chrome, url: str, timeout: int) -> None:
    original_timeout = timeout
    driver.set_page_load_timeout(original_timeout)
    try:
        driver.get(url)
        return
    except TimeoutException:
        try:
            driver.execute_script("window.stop();")
        except Exception:
            pass
        time.sleep(1)
    except WebDriverException:
        try:
            driver.execute_script("window.stop();")
        except Exception:
            pass
        time.sleep(1)


def build_linkedin_search_url(
    keyword: str,
    page: int = 1,
    origin: str = "FACETED_SEARCH",
    industry_company_vertical_id: str = "99",
) -> str:
    query = urllib.parse.quote(keyword)
    base = (
        "https://www.linkedin.com/search/results/companies/"
        f"?keywords={query}&origin={urllib.parse.quote(origin)}"
        f"&industryCompanyVertical=%5B%22{urllib.parse.quote(str(industry_company_vertical_id))}%22%5D"
    )
    if page > 1:
        return f"{base}&page={page}"
    return base


def linkedin_company_search_page(
    driver: webdriver.Chrome,
    keyword: str,
    page: int,
    timeout: int,
    login_wait: int,
    search_origin: str,
    industry_company_vertical_id: str,
) -> List[Dict[str, str]]:
    safe_get(
        driver,
        build_linkedin_search_url(
            keyword,
            page,
            origin=search_origin,
            industry_company_vertical_id=industry_company_vertical_id,
        ),
        timeout,
    )
    wait_for_login_if_needed(driver, login_wait)
    wait_for_any(driver, ((By.TAG_NAME, "body"),), timeout)
    time.sleep(2)
    js = """
    const anchors = Array.from(document.querySelectorAll('a[href*="/company/"]'));
    const seen = new Set();
    const rows = [];
    for (const a of anchors) {
      const href = a.href.split('?')[0];
      if (!href.includes('/company/') || seen.has(href)) continue;
      const title = (a.innerText || a.textContent || '').trim();
      const card = a.closest('li, .reusable-search__result-container, .search-results-container, div[data-view-name]');
      const cardText = ((card && (card.innerText || card.textContent)) || title || '').trim();
      if (!title && !cardText) continue;
      seen.add(href);
      rows.push({name: title, url: href, card_text: cardText});
    }
    return rows;
    """
    results = driver.execute_script(js) or []
    filtered: List[Dict[str, str]] = []
    seen_urls = set()
    for row in results:
        url = row.get("url", "")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        filtered.append(
            {
                "name": compact_whitespace(row.get("name", "")),
                "url": url,
                # Keep original line breaks so we can reliably read the line below company name.
                "card_text": (row.get("card_text", "") or "").strip(),
            }
        )
    return filtered


def parse_search_card_text(card_text: str) -> Dict[str, str]:
    lines = [compact_whitespace(line) for line in card_text.splitlines() if compact_whitespace(line)]
    cleaned = [line for line in lines if line not in {"关注", "下一步", "这些结果有用吗？"}]
    # Keep only the leading, meaningful card header block.
    header: List[str] = []
    stop_tokens = ("关注", "发消息", "主页", "关于", "动态", "职位", "会员", "显示全部详情", "详情")
    for line in cleaned:
        lower = line.lower()
        if line in stop_tokens:
            break
        if any(tok in lower for tok in ("位关注者", "followers")):
            break
        header.append(line)
        if len(header) >= 8:
            break

    company_name = header[0] if header else ""
    # Rule: industry comes from the line directly below the company name in list results.
    industry = header[1] if len(header) > 1 else ""
    location = ""
    intro = ""
    for idx, line in enumerate(header[2:], start=2):
        lower = line.lower()
        if not location and "个关注者" not in line and "followers" not in lower and len(line) < 80:
            location = line
            continue
        if "个关注者" in line or "followers" in lower:
            continue
        intro = line
        break
    return {
        "company_name": company_name,
        "industry": industry,
        "location": location,
        "company_intro": intro,
    }


def extract_about_overview_dom(driver: webdriver.Chrome) -> str:
    try:
        text = driver.execute_script(
            """
            function compact(s){ return (s || '').replace(/\\s+/g, ' ').trim(); }
            const stopLabels = new Set([
              '网站','website','电话','phone','行业','industry','规模','size',
              '总部','headquarters','创立','founded','领域','specialties',
              '地点','location','locations'
            ]);
            const heads = Array.from(document.querySelectorAll('h2,h3,dt,span'));
            for (const h of heads) {
              const label = compact(h.innerText).toLowerCase();
              if (label !== '概览' && label !== 'overview') continue;
              let root = h.closest('section,div');
              for (let depth = 0; depth < 5 && root; depth++) {
                const chunks = [];
                const cands = Array.from(root.querySelectorAll('p,div,span'));
                for (const c of cands) {
                  const t = compact(c.innerText);
                  if (!t || t.toLowerCase() === label) continue;
                  if (stopLabels.has(t.toLowerCase())) break;
                  if (t.length >= 20 && !t.includes('显示全部详情') && !t.includes('... 展开')) {
                    chunks.push(t);
                  }
                  if (chunks.length >= 3) break;
                }
                if (chunks.length) return chunks.join(' ');
                root = root.parentElement;
              }
            }
            return '';
            """
        )
        return compact_whitespace(str(text or ""))
    except Exception:
        return ""


def extract_overview_intro(page_text: str) -> str:
    lines = [compact_whitespace(line) for line in page_text.splitlines() if compact_whitespace(line)]
    if not lines:
        return ""
    markers = ("概览", "overview")
    stop_labels = {
        "网站",
        "website",
        "电话",
        "phone",
        "行业",
        "industry",
        "规模",
        "size",
        "总部",
        "headquarters",
        "创立",
        "founded",
        "领域",
        "specialties",
        "地点",
        "location",
        "locations",
    }
    for i, line in enumerate(lines):
        lower = line.lower()
        if lower in markers:
            parts: List[str] = []
            for candidate in lines[i + 1 : i + 12]:
                c_lower = candidate.lower()
                if c_lower in stop_labels:
                    break
                if any(x in c_lower for x in ("关注者", "followers", "显示全部详情", "... 展开")):
                    continue
                if len(candidate) < 12:
                    continue
                parts.append(candidate)
                if len(parts) >= 3:
                    break
            if parts:
                return compact_whitespace(" ".join(parts))
    return ""


def text_or_empty(driver: webdriver.Chrome, selector: str) -> str:
    try:
        return compact_whitespace(driver.find_element(By.CSS_SELECTOR, selector).text)
    except NoSuchElementException:
        return ""


def parse_linkedin_company_page(driver: webdriver.Chrome, company_url: str, timeout: int) -> Dict[str, str]:
    normalized_company_url = company_url.split("?", 1)[0].rstrip("/")
    about_url = f"{normalized_company_url}/about/"
    safe_get(driver, about_url, timeout)
    wait_for_any(driver, ((By.TAG_NAME, "body"),), timeout)
    time.sleep(1.5)
    page_text_raw = driver.find_element(By.TAG_NAME, "body").text
    page_text_compact = compact_whitespace(page_text_raw)
    company_name = text_or_empty(driver, "h1")
    website = ""
    industry = ""
    location = ""
    intro = ""

    try:
        dt_dd = driver.execute_script(
            """
            const out = {};
            const dts = Array.from(document.querySelectorAll('dt'));
            for (const dt of dts) {
              const key = (dt.innerText || '').trim();
              if (!key) continue;
              const dd = dt.nextElementSibling;
              const value = ((dd && (dd.innerText || dd.textContent)) || '').trim();
              if (value) out[key] = value;
            }
            return out;
            """
        ) or {}
    except Exception:
        dt_dd = {}
    for key, value in dt_dd.items():
        norm_key = compact_whitespace(str(key)).lower()
        norm_value = compact_whitespace(str(value))
        if not norm_value:
            continue
        if not website and norm_key in {"网站", "website"}:
            for part in re.split(r"\s+", norm_value):
                if part.startswith("http"):
                    website = part.split("?")[0]
                    break
            if not website and "." in norm_value and " " not in norm_value:
                website = normalize_url(norm_value).split("?")[0]
        if not industry and norm_key in {"行业", "industry"}:
            industry = norm_value
        if not location and norm_key in {"总部", "headquarters", "locations", "地点", "location"}:
            location = norm_value

    # Rule: intro must come from the company detail About page overview.
    intro = extract_about_overview_dom(driver)
    if not intro:
        intro = extract_overview_intro(page_text_raw)
    if not intro:
        try:
            intro = compact_whitespace(
                driver.execute_script(
                    """
                    const selectors = [
                      '[data-test-id="about-us__description"]',
                      'section p.break-words',
                      'p.break-words',
                      'section p'
                    ];
                    for (const sel of selectors) {
                      const el = document.querySelector(sel);
                      if (el) {
                        const t = (el.innerText || '').trim();
                        if (t.length >= 20) return t;
                      }
                    }
                    const hs = Array.from(document.querySelectorAll('h2,h3,span'));
                    for (const h of hs) {
                      const label = (h.innerText || '').trim().toLowerCase();
                      if (label === '概览' || label === 'overview') {
                        let node = h.parentElement;
                        for (let depth = 0; depth < 4 && node; depth++) {
                          const cands = Array.from(node.querySelectorAll('p,div,span'));
                          for (const c of cands) {
                            const t = (c.innerText || '').trim();
                            if (t && t !== (h.innerText || '').trim() && t.length >= 20) return t;
                          }
                          node = node.parentElement;
                        }
                      }
                    }
                    return '';
                    """
                )
            )
        except Exception:
            pass
    if not intro:
        intro = text_or_empty(driver, "section p")
    if not intro:
        meta = driver.execute_script("const m=document.querySelector('meta[name=\"description\"]'); return m ? m.content : '';")
        intro = compact_whitespace(meta)

    if not industry or not location:
        patterns = [
            (r"Industry\s+([^\n]+)", "industry"),
            (r"Headquarters\s+([^\n]+)", "location"),
            (r"Locations\s+([^\n]+)", "location"),
        ]
        for pattern, field in patterns:
            match = re.search(pattern, page_text_compact, re.IGNORECASE)
            if match:
                value = compact_whitespace(match.group(1))
                if field == "industry" and not industry:
                    industry = value
                if field == "location" and not location:
                    location = value

    return {
        "company_name": company_name,
        "company_website": website,
        "company_intro": intro,
        "industry": industry,
        "location": location,
        "linkedin_url": normalized_company_url,
    }


def normalize_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return "https://" + url.lstrip("/")


def fetch_url(url: str, timeout: int) -> Tuple[str, str]:
    effective_timeout = max(3, min(timeout, 5))
    cmd = [
        "curl",
        "-L",
        "--max-time",
        str(effective_timeout),
        "--connect-timeout",
        str(min(effective_timeout, 4)),
        "-A",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0 Safari/537.36",
        "-w",
        "\n__FINAL_URL__:%{url_effective}",
        url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=effective_timeout + 2)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"curl timeout: {url}") from exc
    if result.returncode != 0 and not result.stdout:
        raise RuntimeError(result.stderr.strip() or f"curl failed with exit {result.returncode}")
    stdout = result.stdout
    marker = "\n__FINAL_URL__:"
    if marker in stdout:
        body, final_url = stdout.rsplit(marker, 1)
    else:
        body, final_url = stdout, url
    return body, final_url.strip()


def score_email(email: str) -> Tuple[int, int]:
    local = email.split("@", 1)[0].lower()
    preferred = ("hello", "info", "contact", "support", "studio", "team", "business", "sales")
    score = 0
    for idx, prefix in enumerate(preferred):
        if local.startswith(prefix):
            score = 100 - idx
            break
    return score, -len(email)


def choose_best_email(emails: Iterable[str]) -> str:
    cleaned = []
    for email in emails:
        item = email.strip(" .,:;()[]<>\"'")
        if item.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".webp")):
            continue
        if "example.com" in item.lower():
            continue
        cleaned.append(item)
    if not cleaned:
        return ""
    deduped = sorted(set(cleaned), key=score_email, reverse=True)
    return deduped[0]


def html_to_text(markup: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", markup)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return compact_whitespace(html.unescape(text))


def discover_contact_links(base_url: str, markup: str) -> List[str]:
    links = set()
    for match in re.finditer(r'href=["\']([^"\']+)["\']', markup, re.IGNORECASE):
        href = html.unescape(match.group(1).strip())
        if href.startswith("mailto:") or href.startswith("javascript:") or href.startswith("#"):
            continue
        absolute = urllib.parse.urljoin(base_url, href)
        parsed = urllib.parse.urlparse(absolute)
        if not parsed.scheme.startswith("http"):
            continue
        path = parsed.path.lower()
        if any(hint in path for hint in CONTACT_PATH_HINTS):
            links.add(absolute)
    parsed_base = urllib.parse.urlparse(base_url)
    for hint in CONTACT_PATH_HINTS:
        links.add(urllib.parse.urljoin(f"{parsed_base.scheme}://{parsed_base.netloc}", hint))
    return list(links)


def find_email_on_website(website_url: str, timeout: int) -> Tuple[str, str]:
    url = normalize_url(website_url)
    if not url:
        return "", "no website"
    checked_pages = []
    try:
        home_markup, final_home = fetch_url(url, timeout)
    except Exception as exc:
        return "", f"website fetch failed: {exc}"
    checked_pages.append(final_home)
    emails = EMAIL_RE.findall(home_markup)
    if emails:
        return choose_best_email(emails), f"official site page: {final_home}"

    # Limit deep crawling for high-volume runs to keep throughput acceptable.
    for link in discover_contact_links(final_home, home_markup)[:2]:
        try:
            markup, final_url = fetch_url(link, timeout)
        except Exception:
            continue
        checked_pages.append(final_url)
        emails = EMAIL_RE.findall(markup)
        if emails:
            return choose_best_email(emails), f"official site page: {final_url}"

    return "", "checked: " + ", ".join(checked_pages[:6])


def search_google_maps_for_email(driver: webdriver.Chrome, company_name: str, location: str, timeout: int) -> Tuple[str, str]:
    query = urllib.parse.quote(f"{company_name} {location}")
    tab = new_tab(driver, f"https://www.google.com/maps/search/{query}")
    try:
        wait_for_any(driver, ((By.TAG_NAME, "body"),), timeout)
        time.sleep(3)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        emails = EMAIL_RE.findall(body_text)
        if emails:
            return choose_best_email(emails), "google maps visible listing"
        page_html = driver.page_source
        emails = EMAIL_RE.findall(page_html)
        if emails:
            return choose_best_email(emails), "google maps page source"
        return "", "google maps searched, no email found"
    finally:
        try:
            handles = driver.window_handles
        except Exception:
            handles = []
        if tab in handles:
            try:
                close_current_tab(driver)
            except Exception:
                pass


def ensure_minimum_fields(data: Dict[str, str]) -> Dict[str, str]:
    required = (
        "company_name",
        "company_website",
        "company_intro",
        "industry",
        "location",
        "linkedin_url",
    )
    for key in required:
        data.setdefault(key, "")
    return data


def build_identity_key(company_name: str, company_website: str, linkedin_url: str) -> Tuple[str, str, str]:
    return (company_name.lower().strip(), company_website.lower().strip(), linkedin_url.lower().strip())


def load_excluded_identities(exclude_json: str) -> set:
    if not exclude_json:
        return set()
    path = Path(exclude_json)
    if not path.exists():
        return set()
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    identities = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        identities.add(
            build_identity_key(
                str(row.get("company_name", "")),
                str(row.get("company_website", "")),
                str(row.get("linkedin_url", "")),
            )
        )
    return identities


def build_identity_key_string(identity_key: Tuple[str, str, str]) -> str:
    return "||".join(identity_key)


def init_db(db_path: str) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            company_name TEXT NOT NULL,
            company_website TEXT NOT NULL,
            company_intro TEXT NOT NULL,
            industry TEXT NOT NULL,
            location TEXT NOT NULL,
            linkedin_url TEXT NOT NULL,
            email TEXT NOT NULL,
            email_source TEXT NOT NULL,
            notes TEXT NOT NULL,
            identity_key TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_records_keyword_identity ON records(keyword, identity_key)"
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS crawl_state (
            keyword TEXT PRIMARY KEY,
            last_page INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    return conn


def load_excluded_identities_from_db(conn: sqlite3.Connection) -> set:
    rows = conn.execute(
        "SELECT company_name, company_website, linkedin_url FROM records"
    ).fetchall()
    identities = set()
    for company_name, company_website, linkedin_url in rows:
        identities.add(build_identity_key(str(company_name), str(company_website), str(linkedin_url)))
    return identities


def get_resume_start_page(conn: sqlite3.Connection, keyword: str) -> int:
    row = conn.execute("SELECT last_page FROM crawl_state WHERE keyword = ?", (keyword,)).fetchone()
    if not row:
        return 1
    last_page = int(row[0] or 0)
    return max(1, last_page + 1)


def upsert_resume_page(conn: sqlite3.Connection, keyword: str, last_page: int) -> None:
    conn.execute(
        """
        INSERT INTO crawl_state(keyword, last_page, updated_at)
        VALUES (?, ?, datetime('now'))
        ON CONFLICT(keyword) DO UPDATE SET
            last_page = excluded.last_page,
            updated_at = excluded.updated_at
        """,
        (keyword, int(last_page)),
    )
    conn.commit()


def insert_records_to_db(conn: sqlite3.Connection, records: List[CompanyRecord]) -> int:
    inserted = 0
    for record in records:
        identity = build_identity_key_string(
            build_identity_key(record.company_name, record.company_website, record.linkedin_url)
        )
        cur = conn.execute(
            """
            INSERT OR IGNORE INTO records(
                keyword, company_name, company_website, company_intro, industry, location,
                linkedin_url, email, email_source, notes, identity_key
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.keyword,
                record.company_name,
                record.company_website,
                record.company_intro,
                record.industry,
                record.location,
                record.linkedin_url,
                record.email,
                record.email_source,
                record.notes,
                identity,
            ),
        )
        inserted += int(cur.rowcount or 0)
    conn.commit()
    return inserted


def collect_for_keyword(
    driver: webdriver.Chrome,
    keyword: str,
    target_count: int,
    timeout: int,
    login_wait: int,
    max_search_pages: int,
    excluded_identities: set,
    start_page: int = 1,
    search_origin: str = "FACETED_SEARCH",
    industry_company_vertical_id: str = "99",
) -> Tuple[List[CompanyRecord], int]:
    records: List[CompanyRecord] = []
    seen_companies = set(excluded_identities)
    max_page = max(start_page, start_page + max_search_pages - 1)
    last_page_visited = max(0, start_page - 1)
    for page in range(start_page, max_page + 1):
        last_page_visited = page
        if len(records) >= target_count:
            break
        candidates = linkedin_company_search_page(
            driver,
            keyword,
            page,
            timeout,
            login_wait,
            search_origin,
            industry_company_vertical_id,
        )
        if not candidates:
            continue
        page_added = 0
        for candidate in candidates:
            if len(records) >= target_count:
                break
            card_fields = parse_search_card_text(candidate.get("card_text", ""))
            # Fast filter: only keep list cards whose line-below-name industry matches design services.
            if not is_allowed_industry(card_fields.get("industry", "")):
                continue
            company_name_hint = card_fields["company_name"] or candidate["name"]
            pre_identity_key = build_identity_key(company_name_hint, "", candidate.get("url", ""))
            if pre_identity_key in seen_companies:
                continue
            try:
                data = ensure_minimum_fields(parse_linkedin_company_page(driver, candidate["url"], timeout))
            except Exception as exc:
                data = ensure_minimum_fields({"linkedin_url": candidate["url"]})
                data["company_intro"] = ""
                data["notes"] = f"linkedin page parse failed: {exc}"
            company_name = data["company_name"] or company_name_hint
            # Rule: always use list-card line below company name as industry source.
            if card_fields["industry"]:
                data["industry"] = card_fields["industry"]
            elif not data["industry"]:
                data["industry"] = ""
            if not is_allowed_industry(data["industry"]):
                continue
            if not data["location"]:
                data["location"] = card_fields["location"]
            if not data["company_intro"]:
                data["company_intro"] = card_fields["company_intro"]
            identity_key = build_identity_key(company_name, data["company_website"], data["linkedin_url"])
            if identity_key in seen_companies:
                continue
            seen_companies.add(pre_identity_key)
            seen_companies.add(identity_key)
            if reject_china_location(data["location"]):
                continue

            email = ""
            email_source = "not_found"
            notes = ""

            if data["company_website"]:
                email, website_note = find_email_on_website(data["company_website"], timeout)
                if email:
                    email_source = "official_website"
                    notes = website_note
                else:
                    notes = website_note

            if not email:
                email, maps_note = search_google_maps_for_email(driver, company_name, data["location"], timeout)
                if email:
                    email_source = "google_maps"
                    notes = maps_note
                elif maps_note:
                    notes = f"{notes}; {maps_note}".strip("; ")

            record = CompanyRecord(
                keyword=keyword,
                company_name=company_name,
                company_website=data["company_website"],
                company_intro=data["company_intro"],
                industry=data["industry"],
                location=data["location"],
                linkedin_url=data["linkedin_url"],
                email=email,
                email_source=email_source,
                notes=notes,
            )
            records.append(record)
            page_added += 1
    return records, last_page_visited


def write_outputs(output_dir: Path, records: List[CompanyRecord], metadata: Dict[str, str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "linkedin_company_scout_results.json"
    csv_path = output_dir / "linkedin_company_scout_results.csv"
    meta_path = output_dir / "run_metadata.json"

    with json_path.open("w", encoding="utf-8") as fh:
        json.dump([asdict(r) for r in records], fh, ensure_ascii=False, indent=2)

    fieldnames = list(asdict(records[0]).keys()) if records else [
        "keyword",
        "company_name",
        "company_website",
        "company_intro",
        "industry",
        "location",
        "linkedin_url",
        "email",
        "email_source",
        "notes",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))

    with meta_path.open("w", encoding="utf-8") as fh:
        json.dump(metadata, fh, ensure_ascii=False, indent=2)


def main() -> int:
    args = parse_args()
    keywords = [compact_whitespace(item) for item in args.keywords.split(",") if compact_whitespace(item)]
    if not keywords:
        print("No valid keywords provided.", file=sys.stderr)
        return 2

    heartbeat_enabled, heartbeat_note = enable_heartbeat(args.no_heartbeat)
    try:
        launched_chrome = ensure_chrome_debuggable(args.chrome_binary, args.chrome_profile_dir, args.debug_port)
        driver = create_driver(args.debug_port, args.page_timeout)
    except Exception as exc:
        print(f"Failed to prepare Chrome automation: {exc}", file=sys.stderr)
        return 1

    ensure_primary_window(driver)
    original_handle = driver.current_window_handle
    automation_handle = new_tab(driver, "about:blank")
    all_records: List[CompanyRecord] = []
    shortfalls: Dict[str, int] = {}
    last_pages: Dict[str, int] = {}
    db_conn = init_db(args.db_path)
    excluded_identities = load_excluded_identities(args.exclude_json)
    excluded_identities.update(load_excluded_identities_from_db(db_conn))
    try:
        for keyword in keywords:
            driver.switch_to.window(automation_handle)
            start_page = 1
            if not args.disable_db_resume:
                start_page = get_resume_start_page(db_conn, keyword)
            rows, last_page = collect_for_keyword(
                driver=driver,
                keyword=keyword,
                target_count=args.count,
                timeout=args.page_timeout,
                login_wait=args.linkedin_wait_seconds,
                max_search_pages=args.max_search_pages,
                excluded_identities=excluded_identities,
                start_page=start_page,
                search_origin=args.linkedin_search_origin,
                industry_company_vertical_id=args.industry_company_vertical_id,
            )
            all_records.extend(rows)
            for row in rows:
                excluded_identities.add(build_identity_key(row.company_name, row.company_website, row.linkedin_url))
            inserted_count = insert_records_to_db(db_conn, rows)
            upsert_resume_page(db_conn, keyword, last_page)
            last_pages[keyword] = last_page
            shortfalls[keyword] = max(args.count - len(rows), 0)
    except (TimeoutException, WebDriverException, RuntimeError) as exc:
        print(f"Collection interrupted: {exc}", file=sys.stderr)
    finally:
        try:
            if automation_handle in driver.window_handles:
                driver.switch_to.window(automation_handle)
                close_current_tab(driver)
            if original_handle in driver.window_handles:
                driver.switch_to.window(original_handle)
        except Exception:
            pass
        stop_driver_service(driver)
        try:
            db_conn.close()
        except Exception:
            pass

    metadata = {
        "keywords": keywords,
        "target_per_keyword": args.count,
        "accepted_total": len(all_records),
        "heartbeat_enabled": heartbeat_enabled,
        "heartbeat_note": heartbeat_note,
        "chrome_launched_by_script": launched_chrome,
        "shortfalls": shortfalls,
        "db_path": args.db_path,
        "last_pages": last_pages,
    }
    write_outputs(Path(args.output_dir), all_records, metadata)

    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
