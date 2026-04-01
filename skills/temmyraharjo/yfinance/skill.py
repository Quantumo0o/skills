"""
yfinance AgentSkill - price, technical, and fundamental snapshot for stocks (IDX-aware)
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import re

IDX_SUFFIX = ".JK"
IDX_TICKER_RE = re.compile(r"^[A-Z]{2,5}$")
SOUL_EMOJI = {
    'fundamental': '📊',
    'technical': '📉',
    'insight': '💡',
    'risk': '⚠️',
    'teaching': '🧠',
    'up': '📈',
    'down': '📉',
    'sideways': '🟡',
    'strong': '🔥',
    'weak': '❄️'
}

# ---- Ticker handling ----
def format_ticker(ticker):
    ticker = ticker.strip().upper()
    if IDX_TICKER_RE.match(ticker) and not ticker.endswith(IDX_SUFFIX):
        return ticker + IDX_SUFFIX
    return ticker

def prepare_tickers(tickers):
    if isinstance(tickers, str):
        tickers = [t.strip() for t in re.split(r'[ ,]+', tickers) if t.strip()]
    return [format_ticker(t) for t in tickers]

# ---- Snapshots ----
def get_snapshot(tickers):
    out = []
    for t in prepare_tickers(tickers):
        try:
            info = yf.Ticker(t).info
        except Exception:
            info = None
        if not info or 'regularMarketPrice' not in info:
            out.append(f"{SOUL_EMOJI['teaching']} Ticker '{t}': 🚫 Data unavailable or ticker invalid.")
            continue
        price = info.get('regularMarketPrice')
        prev = info.get('regularMarketPreviousClose')
        diff = None if price is None or prev is None else price - prev
        pct = None if price is None or prev is None or prev == 0 else 100.0 * diff/prev
        symbol = t
        # Basic structure
        output = [f"{symbol}", f"Last Price: {price if price else '-'}"]
        if diff is not None and pct is not None:
            trend = (SOUL_EMOJI['up'] if diff > 0 else (SOUL_EMOJI['down'] if diff < 0 else SOUL_EMOJI['sideways']))
            output.append(f"Change: {diff:+.2f} ({pct:+.2f}%) {trend}")
        # Fundamental
        fundamentals = []
        for field,label in [
            ('marketCap','Market Cap'),
            ('trailingPE','P/E'),
            ('dividendYield','Div Yield'),
            ('trailingEps','EPS'),
            ('bookValue','Book Value'),
            ('returnOnEquity','ROE'),
        ]:
            val = info.get(field)
            fundamentals.append(f"{label}: {val if val is not None else '-'}")
        output.append(f"{SOUL_EMOJI['fundamental']} Fundamentals: " + ", ".join(fundamentals))
        # Technicals
        tfields = [
            ('fiftyDayAverage','50D Avg'),
            ('twoHundredDayAverage','200D Avg'),
            ('averageVolume','Avg Vol')
        ]
        techs = [f"{label}: {info.get(field) if info.get(field) is not None else '-'}" for field, label in tfields]
        output.append(f"{SOUL_EMOJI['technical']} Technicals: " + ", ".join(techs))
        out.append("\n".join(output))
    return "\n\n".join(out)

# ---- History ----
def get_history(tickers, period='3mo', interval='1d'):
    res = {}
    for t in prepare_tickers(tickers):
        try:
            df = yf.Ticker(t).history(period=period, interval=interval)
        except Exception:
            df = None
        if df is None or df.empty:
            res[t] = None
        else:
            res[t] = df.reset_index().to_dict(orient='records')
    return res

# ---- Entrypoints for AgentSkill framework ----
def agent_entry_snapshot(args):
    """
    args: {'tickers': str or list}
    """
    return get_snapshot(args["tickers"])

def agent_entry_history(args):
    """
    args: {'tickers': str or list, 'period': str, 'interval': str}
    """
    return get_history(args["tickers"], args.get("period", '3mo'), args.get("interval", '1d'))

# For local/manual testing
if __name__ == '__main__':
    print(agent_entry_snapshot({'tickers': "ADRO,BBCA"}))
    print(agent_entry_history({'tickers': ["ADRO","AAPL"]}))
