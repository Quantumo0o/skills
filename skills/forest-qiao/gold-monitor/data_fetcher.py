"""数据获取模块 — akshare(中国金价) / 新浪财经(国际金价/美元指数/原油)"""

import logging
import re
from datetime import datetime
from typing import List

import akshare as ak
import requests

logger = logging.getLogger(__name__)

_SINA_HEADERS = {"Referer": "https://finance.sina.com.cn"}

# 内存缓存：最新价格 + 历史数据
_latest_prices: dict = {}
_history_data: dict = {}


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_china_gold() -> dict:
    """上期所黄金连续合约实时行情 (通过 akshare)"""
    try:
        df = ak.futures_zh_spot(symbol="AU0", market="CF", adjust="0")
        if df is None or df.empty:
            raise ValueError("akshare futures_zh_spot 返回空数据")
        row = df.iloc[-1]
        price = float(row["current_price"])
        prev = float(row["last_settle_price"]) or float(row["last_close"])
        change = round(price - prev, 2)
        change_pct = round(change / prev * 100, 2) if prev else 0.0
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
        logger.warning("获取中国黄金失败: %s", e)
        return _fallback("中国黄金 Au99.99", "AU9999", "元/克")


def _parse_sina_hq(code: str) -> List[str]:
    """从新浪财经获取实时行情，返回逗号分隔的字段列表"""
    resp = requests.get(
        f"https://hq.sinajs.cn/list={code}",
        headers=_SINA_HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    m = re.search(r'"(.+)"', resp.text)
    if not m or not m.group(1):
        raise ValueError(f"新浪行情 {code} 返回空数据")
    return m.group(1).split(",")


def get_international_gold() -> dict:
    """国际黄金 COMEX — 新浪财经 hf_GC"""
    try:
        # hf_GC 格式: 最新价,,今开,昨收,最高,最低,时间,买价,卖价,...,日期,名称,...
        fields = _parse_sina_hq("hf_GC")
        price = float(fields[0])
        prev = float(fields[3]) if fields[3] else price
        change = round(price - prev, 2)
        change_pct = round(change / prev * 100, 2) if prev else 0.0
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
        logger.warning("获取国际黄金失败: %s", e)
        return _fallback("国际黄金 COMEX", "XAUUSD", "USD/oz")


def get_usd_index() -> dict:
    """美元指数 DXY — 新浪财经 DINIW"""
    try:
        # DINIW 格式: 时间,最新价,开盘价,昨收,?,?,最高,最低,当前价,名称,日期
        fields = _parse_sina_hq("DINIW")
        price = float(fields[8])
        prev = float(fields[3]) if fields[3] else price
        change = round(price - prev, 2)
        change_pct = round(change / prev * 100, 2) if prev else 0.0
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
        logger.warning("获取美元指数失败: %s", e)
        return _fallback("美元指数 DXY", "USIDX", "")


def get_oil_price() -> dict:
    """WTI 原油 — 新浪财经 hf_CL"""
    try:
        fields = _parse_sina_hq("hf_CL")
        price = float(fields[0])
        prev = float(fields[3]) if fields[3] else price
        change = round(price - prev, 2)
        change_pct = round(change / prev * 100, 2) if prev else 0.0
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
        logger.warning("获取WTI原油失败: %s", e)
        return _fallback("WTI 原油", "WTI", "USD/桶")


def _fallback(name: str, symbol: str, unit: str) -> dict:
    cached = _latest_prices.get(symbol)
    if cached:
        return cached
    return {
        "name": name,
        "symbol": symbol,
        "price": 0,
        "change": 0,
        "change_pct": 0,
        "unit": unit,
        "update_time": _now_str(),
        "error": True,
    }


def fetch_all() -> List[dict]:
    """拉取所有品种最新价格，更新缓存"""
    results = []
    for fn in (get_china_gold, get_international_gold, get_usd_index, get_oil_price):
        item = fn()
        _latest_prices[item["symbol"]] = item
        results.append(item)
    return results


def get_cached_prices() -> List[dict]:
    if not _latest_prices:
        return fetch_all()
    return list(_latest_prices.values())


def get_history(symbol: str, period: str = "1mo") -> List[dict]:
    """获取历史K线数据 — 通过 akshare"""
    if symbol == "AU9999":
        return _get_china_gold_history()
    if symbol == "XAUUSD":
        return _get_sina_futures_history("AU0", "CF")
    if symbol == "WTI":
        return _get_sina_futures_history("CL0", "NYM")
    if symbol == "USIDX":
        return _get_usd_index_history()
    return []


def _get_china_gold_history() -> List[dict]:
    """获取中国黄金历史数据"""
    try:
        df = ak.spot_hist_sge(symbol="Au99.99")
        if df is None or df.empty:
            return []
        data = []
        for _, row in df.tail(30).iterrows():
            data.append({
                "date": str(row.get("日期", row.iloc[0])),
                "open": float(row.get("开盘价", 0)),
                "close": float(row.get("收盘价", 0)),
                "high": float(row.get("最高价", 0)),
                "low": float(row.get("最低价", 0)),
                "volume": int(row.get("成交量", 0)),
            })
        return data
    except Exception as e:
        logger.warning("获取中国黄金历史数据失败: %s", e)
        return []


def _get_sina_futures_history(symbol: str, market: str) -> List[dict]:
    """通过 akshare 获取期货历史数据"""
    try:
        df = ak.futures_zh_spot(symbol=symbol, market=market, adjust="0")
        if df is None or df.empty:
            return []
        data = []
        for _, row in df.iterrows():
            data.append({
                "date": str(row.get("time", "")),
                "open": round(float(row.get("open", 0)), 2),
                "close": round(float(row.get("current_price", 0)), 2),
                "high": round(float(row.get("high", 0)), 2),
                "low": round(float(row.get("low", 0)), 2),
                "volume": int(row.get("volume", 0)),
            })
        return data
    except Exception as e:
        logger.warning("获取期货历史数据失败 (%s): %s", symbol, e)
        return []


def _get_usd_index_history() -> List[dict]:
    """获取美元指数历史数据 — 通过 akshare spot_golden_benchmark_sge 的替代"""
    try:
        df = ak.index_global_spot_em()
        if df is None or df.empty:
            return []
        matched = df[df["名称"].str.contains("美元指数", na=False)]
        if matched.empty:
            return []
        row = matched.iloc[0]
        return [{
            "date": _now_str()[:10],
            "open": round(float(row.get("开盘价", 0)), 2),
            "close": round(float(row.get("最新价", 0)), 2),
            "high": round(float(row.get("最高价", 0)), 2),
            "low": round(float(row.get("最低价", 0)), 2),
            "volume": 0,
        }]
    except Exception as e:
        logger.warning("获取美元指数历史数据失败: %s", e)
        return []
