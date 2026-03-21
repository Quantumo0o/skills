#!/usr/bin/env python3
"""CLI tool to query gold, USD index, and oil prices."""

import json
import re
import sys
from datetime import datetime

try:
    import akshare as ak
    import requests
except ImportError:
    print(json.dumps({"error": "Missing dependencies. Please run: pip install akshare requests"}))
    sys.exit(1)

_SINA_HEADERS = {"Referer": "https://finance.sina.com.cn"}


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _parse_sina_hq(code: str) -> list:
    resp = requests.get(
        f"https://hq.sinajs.cn/list={code}",
        headers=_SINA_HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    m = re.search(r'"(.+)"', resp.text)
    if not m or not m.group(1):
        raise ValueError(f"Sina quote {code} returned empty data")
    return m.group(1).split(",")


def _calc_change(price: float, prev: float) -> tuple:
    change = round(price - prev, 2)
    change_pct = round(change / prev * 100, 2) if prev else 0.0
    return change, change_pct


def get_china_gold() -> dict:
    try:
        df = ak.futures_zh_spot(symbol="AU0", market="CF", adjust="0")
        if df is None or df.empty:
            raise ValueError("Empty data from akshare")
        row = df.iloc[-1]
        price = float(row["current_price"])
        prev = float(row["last_settle_price"]) or float(row["last_close"])
        change, change_pct = _calc_change(price, prev)
        return {
            "name": "中国黄金 Au99.99",
            "symbol": "AU9999",
            "price": price,
            "change": change,
            "change_pct": change_pct,
            "unit": "元/克",
            "update_time": _now_str(),
        }
    except Exception as e:
        return {"symbol": "AU9999", "error": str(e)}


def get_international_gold() -> dict:
    try:
        fields = _parse_sina_hq("hf_GC")
        price = float(fields[0])
        prev = float(fields[3]) if fields[3] else price
        change, change_pct = _calc_change(price, prev)
        return {
            "name": "国际黄金 COMEX",
            "symbol": "XAUUSD",
            "price": price,
            "change": change,
            "change_pct": change_pct,
            "unit": "USD/oz",
            "update_time": _now_str(),
        }
    except Exception as e:
        return {"symbol": "XAUUSD", "error": str(e)}


def get_usd_index() -> dict:
    try:
        fields = _parse_sina_hq("DINIW")
        price = float(fields[8])
        prev = float(fields[3]) if fields[3] else price
        change, change_pct = _calc_change(price, prev)
        return {
            "name": "美元指数 DXY",
            "symbol": "USIDX",
            "price": price,
            "change": change,
            "change_pct": change_pct,
            "unit": "",
            "update_time": _now_str(),
        }
    except Exception as e:
        return {"symbol": "USIDX", "error": str(e)}


def get_oil_price() -> dict:
    try:
        fields = _parse_sina_hq("hf_CL")
        price = float(fields[0])
        prev = float(fields[3]) if fields[3] else price
        change, change_pct = _calc_change(price, prev)
        return {
            "name": "WTI 原油",
            "symbol": "WTI",
            "price": price,
            "change": change,
            "change_pct": change_pct,
            "unit": "USD/桶",
            "update_time": _now_str(),
        }
    except Exception as e:
        return {"symbol": "WTI", "error": str(e)}


_FETCHERS = {
    "AU9999": get_china_gold,
    "XAUUSD": get_international_gold,
    "USIDX": get_usd_index,
    "WTI": get_oil_price,
}


def main():
    symbol = sys.argv[1].upper() if len(sys.argv) > 1 else "ALL"

    if symbol == "ALL":
        result = [fn() for fn in _FETCHERS.values()]
    elif symbol in _FETCHERS:
        result = _FETCHERS[symbol]()
    else:
        result = {"error": f"Unknown symbol: {symbol}", "valid_symbols": list(_FETCHERS.keys()) + ["ALL"]}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
