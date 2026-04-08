#!/usr/bin/env python3
import argparse
import json
import random
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = BASE_DIR / "selectors.json"
DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
PRICE_RE = re.compile(r"(?<!\d)(\d{1,3}(?:[,.]\d{3})*(?:[.,]\d{2})|\d+(?:[.,]\d{2})?)(?!\d)")
CURRENCY_RE = re.compile(r"\b([A-Z]{3})\b")
JSON_LD_PRODUCT_TYPES = {"product"}


def load_config(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def text_from_node(node) -> Optional[str]:
    if node is None:
        return None
    if getattr(node, "name", None) == "meta":
        return node.get("content")
    if getattr(node, "name", None) == "link":
        return node.get("href")
    return node.get_text(" ", strip=True)


def clean_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = re.sub(r"\s+", " ", value).strip()
    return value or None


def parse_price(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = clean_text(str(value))
    if not text:
        return None
    match = PRICE_RE.search(text.replace("\xa0", " "))
    if not match:
        return None
    number = match.group(1)
    if number.count(",") > 0 and number.count(".") > 0:
        if number.rfind(",") > number.rfind("."):
            number = number.replace(".", "").replace(",", ".")
        else:
            number = number.replace(",", "")
    elif number.count(",") > 0 and number.count(".") == 0:
        if number.count(",") == 1 and len(number.split(",")[-1]) == 2:
            number = number.replace(",", ".")
        else:
            number = number.replace(",", "")
    return float(number)


def detect_currency(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    symbol_map = {"$": "USD", "€": "EUR", "£": "GBP", "¥": "JPY", "￥": "CNY"}
    for symbol, code in symbol_map.items():
        if symbol in value:
            return code
    match = CURRENCY_RE.search(value)
    if match:
        return match.group(1)
    return None


def normalize_availability(value: Optional[str]) -> Optional[str]:
    text = clean_text(value)
    if not text:
        return None
    lowered = text.lower()
    if "instock" in lowered or "in stock" in lowered:
        return "InStock"
    if "outofstock" in lowered or "out of stock" in lowered:
        return "OutOfStock"
    return text


def parse_json_ld(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    products: List[Dict[str, Any]] = []
    for tag in soup.select("script[type='application/ld+json']"):
        raw = tag.string or tag.get_text(strip=True)
        if not raw:
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for item in flatten_jsonld(payload):
            item_type = item.get("@type")
            if isinstance(item_type, list):
                types = {str(t).lower() for t in item_type}
            else:
                types = {str(item_type).lower()} if item_type else set()
            if types & JSON_LD_PRODUCT_TYPES:
                products.append(item)
    return products


def flatten_jsonld(payload: Any) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    if isinstance(payload, list):
        for entry in payload:
            items.extend(flatten_jsonld(entry))
    elif isinstance(payload, dict):
        if "@graph" in payload and isinstance(payload["@graph"], list):
            for entry in payload["@graph"]:
                items.extend(flatten_jsonld(entry))
        items.append(payload)
    return items


def first_selector_value(soup: BeautifulSoup, selectors: List[str]) -> Tuple[Optional[str], Optional[str]]:
    for selector in selectors:
        try:
            node = soup.select_one(selector)
        except Exception:
            continue
        value = clean_text(text_from_node(node))
        if value:
            if selector == "html" and node is not None:
                value = node.get("lang") or value
                value = clean_text(value)
            if value:
                return value, selector
    return None, None


def record_from_jsonld(product: Dict[str, Any], url: str) -> Dict[str, Any]:
    offers = product.get("offers")
    offer = None
    if isinstance(offers, list) and offers:
        offer = offers[0]
    elif isinstance(offers, dict):
        offer = offers

    price = None
    currency = None
    availability = None
    price_source = None
    currency_source = None
    availability_source = None

    if offer:
        price = parse_price(offer.get("price"))
        currency = clean_text(offer.get("priceCurrency"))
        availability = normalize_availability(offer.get("availability"))
        if price is not None:
            price_source = "jsonld.offers.price"
        if currency:
            currency_source = "jsonld.offers.priceCurrency"
        if availability:
            availability_source = "jsonld.offers.availability"

    return {
        "url": url,
        "title": clean_text(product.get("name")),
        "currency": currency,
        "price": price,
        "original_price": None,
        "availability": availability,
        "source": {
            "title": "jsonld.name" if product.get("name") else None,
            "price": price_source,
            "currency": currency_source,
            "availability": availability_source,
        },
    }


def enrich_from_dom(record: Dict[str, Any], soup: BeautifulSoup, config: Dict[str, Any]) -> Dict[str, Any]:
    if not record.get("title"):
        title, source = first_selector_value(soup, config["title_selectors"])
        record["title"] = title
        record["source"]["title"] = source

    if record.get("price") is None:
        raw_price, source = first_selector_value(soup, config["price_selectors"])
        record["price"] = parse_price(raw_price)
        record["source"]["price"] = source if record["price"] is not None else None
        if not record.get("currency"):
            record["currency"] = detect_currency(raw_price)
            if record["currency"]:
                record["source"]["currency"] = f"derived-from:{source}"

    raw_original_price, source = first_selector_value(soup, config["original_price_selectors"])
    original_price = parse_price(raw_original_price)
    if original_price is not None and original_price != record.get("price"):
        record["original_price"] = original_price
        record["source"]["original_price"] = source

    if not record.get("currency"):
        raw_currency, source = first_selector_value(soup, config["currency_selectors"])
        currency = detect_currency(raw_currency)
        if not currency and raw_currency and len(raw_currency) == 3:
            currency = raw_currency.upper()
        if currency:
            record["currency"] = currency
            record["source"]["currency"] = source

    if not record.get("availability"):
        raw_availability, source = first_selector_value(soup, config["availability_selectors"])
        availability = normalize_availability(raw_availability)
        if availability:
            record["availability"] = availability
            record["source"]["availability"] = source

    return record


def fetch(url: str, config: Dict[str, Any], delay_override: Optional[float], timeout_override: Optional[float]) -> requests.Response:
    request_cfg = config["request"]
    delay = request_cfg["base_delay_seconds"] if delay_override is None else delay_override
    timeout = request_cfg["timeout_seconds"] if timeout_override is None else timeout_override
    headers = dict(DEFAULT_HEADERS)
    headers["User-Agent"] = request_cfg["user_agent"]
    retry_codes = set(request_cfg["retry_on_status_codes"])
    last_error = None

    for attempt in range(request_cfg["max_retries"]):
        if delay > 0:
            time.sleep(delay + random.uniform(0, 0.75))
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code in retry_codes:
                last_error = requests.HTTPError(f"retryable status {response.status_code}")
            else:
                response.raise_for_status()
                return response
        except requests.RequestException as exc:
            last_error = exc
        backoff = delay * (2 ** attempt) if delay > 0 else 0
        if attempt < request_cfg["max_retries"] - 1 and backoff > 0:
            time.sleep(backoff)

    raise RuntimeError(f"request failed for {url}: {last_error}")


def scrape_url(url: str, config: Dict[str, Any], delay_override: Optional[float], timeout_override: Optional[float]) -> Dict[str, Any]:
    try:
        response = fetch(url, config, delay_override, timeout_override)
    except Exception as exc:
        return {
            "url": url,
            "title": None,
            "currency": None,
            "price": None,
            "original_price": None,
            "availability": None,
            "source": {},
            "error": str(exc),
        }

    soup = BeautifulSoup(response.text, "html.parser")
    jsonld_products = parse_json_ld(soup)

    if jsonld_products:
        record = record_from_jsonld(jsonld_products[0], url)
    else:
        record = {
            "url": url,
            "title": None,
            "currency": None,
            "price": None,
            "original_price": None,
            "availability": None,
            "source": {},
        }

    record = enrich_from_dom(record, soup, config)
    record["http_status"] = response.status_code
    return record


def load_urls(value: str, from_file: bool) -> List[str]:
    if from_file:
        path = Path(value)
        return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")]
    return [value]


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape normalized product pricing data from ecommerce pages")
    parser.add_argument("input", help="A URL, or a text file path when --input-file is set")
    parser.add_argument("--input-file", action="store_true", help="Treat input as a file containing one URL per line")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to selectors config JSON")
    parser.add_argument("--delay", type=float, default=None, help="Override base delay between requests in seconds")
    parser.add_argument("--timeout", type=float, default=None, help="Override request timeout in seconds")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    urls = load_urls(args.input, args.input_file)
    results = [scrape_url(url, config, args.delay, args.timeout) for url in urls]
    json.dump(results, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
