#!/usr/bin/env python3
"""
晚报生成脚本 v2 — 量化情绪指标 + 数据 + 推送
全自动：抓数据 → 计算情绪分 → 生成报告 → 推送
"""
import subprocess, json, sys, os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, /workspace)
from keys_loader import wx_push, get_webhook_url

NOW = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
TODAY = NOW.strftime("%Y年%m月%d日")
DATE_STR = NOW.strftime("%Y%m%d")
TS = NOW.strftime("%Y-%m-%d %H:%M")


def curl_get(url: str, encoding="gbk") -> str:
    try:
        req = __import__("urllib.request").request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with __import__("urllib.request").urlopen(req, timeout=10) as r:
            return r.read().decode(encoding, errors="replace")
    except Exception as e:
        return f"ERROR: {e}"


# ─────────────────────────────────────────────
# 数据获取
# ─────────────────────────────────────────────

def get_index_data():
    """六大指数实时数据"""
    codes = "sh000001,sz399001,sz399006,sh000688,sh000300,sh000905"
    raw = curl_get(f"https://qt.gtimg.cn/q={codes}")
    result = []
    for line in raw.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("~")
        if len(parts) < 32:
            continue
        result.append({
            "name": parts[1].strip(),
            "price": float(parts[3]) if parts[3] else 0,
            "pct": float(parts[32]) if parts[32] else 0,
        })
    return result


def get_market_stats():
    """涨跌停家数"""
    try:
        import akshare as ak
        zt = ak.stock_zt_pool_em(date=DATE_STR)
        zt_count = len(zt) if zt is not None else 0
        dt = ak.stock_zt_pool_em(date=DATE_STR, zt_pool_str="跌停")
        dt_count = len(dt) if dt is not None else 0
        return zt_count, dt_count
    except Exception:
        return None, None


def get_north_bound():
    """北向资金净流入"""
    try:
        import akshare as ak
        df = ak.stock_hsgt_north_net_flow_em(symbol="北向资金")
        if df is not None and len(df) > 0:
            net = df.iloc[-1].get("最新", 0)
            return float(net) if net else 0
    except Exception:
        return None


def get_sector_flow():
    """行业资金流向（净流入前三）"""
    try:
        import akshare as ak
        df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流向")
        if df is not None:
            cols = [c for c in df.columns if "净流入" in c]
            if cols:
                top = df.sort_values(cols[0], ascending=False).head(3)
                return [f"{r.iloc[0]} +{abs(r.iloc[1]):.0f}亿" for _, r in top.iterrows()]
    except Exception:
        return []


def get_top_sectors():
    """概念板块涨幅前五"""
    try:
        import akshare as ak
        df = ak.stock_board_concept_name_em()
        if df is not None:
            top = df.sort_values("涨跌幅", ascending=False).head(5)
            return [f"{r['板块名称']}（{r['涨跌幅']:+.2f}%）" for _, r in top.iterrows()]
    except Exception:
        return []


def get_market_net_flow():
    """获取全市场主力资金净流入（总计）"""
    try:
        import akshare as ak
        df = ak.stock_market_fund_flow()
        if df is not None and len(df) > 0:
            cols = df.columns.tolist()
            net_col = None
            for c in cols:
                if "净流入" in c and "超" not in c and "大单" not in c:
                    net_col = c
                    break
            if net_col is None:
                net_col = cols[-1]
            latest = df.iloc[-1]
            val = latest.get(net_col, 0)
            return float(val) if val else None
    except Exception:
        pass
    return None


def get_margin_balance():
    """获取两融余额（万元）"""
    try:
        import akshare as ak
        df = ak.stock_margin_detail_sz(date=DATE_STR)
        if df is not None and len(df) > 0:
            return float(df.iloc[-1].get("融资余额", 0))
    except Exception:
        pass
    return None


# ─────────────────────────────────────────────
# 量化情绪打分（核心）
# ─────────────────────────────────────────────

def calc_sentiment(zt_count, dt_count, north_net, mkt_flow, indices):
    """
    量化情绪打分（满分100）
    6个维度：
      1. 涨停数量（满分10）
      2. 涨跌停比（满分10）
      3. 北向资金（满分20）
      4. 全市场主力资金净流入（满分20）
      5. 两融余额（满分20）
      6. 沪深300（满分20）
    """
    score = 0

    # 1. 涨停数量（满分10）
    if zt_count is not None:
        if zt_count >= 100:
            s1, d1 = 10, f"涨停{sec_count}家，极度活跃"
        elif zt_count >= 60:
            s1, d1 = 8, f"涨停{sec_count}家，较活跃"
        elif zt_count >= 30:
            s1, d1 = 5, f"涨停{sec_count}家，活跃度一般"
        else:
            s1, d1 = 2, f"涨停仅{sec_count}家，活跃度低"
    else:
        s1, d1 = 5, "涨停数据暂缺"
    score += s1

    # 2. 涨跌停比（满分10）
    if zt_count is not None and dt_count is not None and dt_count > 0:
        ratio = zt_count / dt_count
        if ratio >= 5:
            s2, d2 = 10, f"涨跌停比={ratio:.1f}，极强多头"
        elif ratio >= 3:
            s2, d2 = 8, f"涨跌停比={ratio:.1f}，多头占优"
        elif ratio >= 1.5:
            s2, d2 = 5, f"涨跌停比={ratio:.1f}，多空僵持"
        else:
            s2, d2 = 2, f"涨跌停比={ratio:.1f}，空头占优"
    elif zt_count is not None and (dt_count == 0 or dt_count is None):
        s2, d2 = 9, "无跌停，极强多头格局"
    else:
        s2, d2 = 5, "涨跌停数据暂缺"
    score += s2

    # 3. 北向资金（满分20）
    if north_net is not None:
        abs_n = abs(north_net)
        if north_net >= 100:
            s3, d3 = 20, f"北向净流入{north_net:+.0f}亿，外资强势买入"
        elif north_net >= 50:
            s3, d3 = 15, f"北向净流入{north_net:+.0f}亿，外资买入"
        elif north_net >= 20:
            s3, d3 = 10, f"北向净流入{north_net:+.0f}亿，外资温和买入"
        elif north_net >= 0:
            s3, d3 = 6, f"北向净流入{north_net:+.0f}亿，外资观望"
        else:
            if abs_n >= 100:
                s3, d3 = 4, f"北向净流出{north_net:+.0f}亿，外资大幅卖出"
            elif abs_n >= 50:
                s3, d3 = 8, f"北向净流出{north_net:+.0f}亿，外资卖出"
            else:
                s3, d3 = 12, f"北向净流出{north_net:+.0f}亿，外资小幅减仓"
    else:
        s3, d3 = 10, "北向数据暂缺"
    score += s3

    # 4. 全市场主力资金净流入（满分20）
    if mkt_flow is not None:
        if mkt_flow >= 500:
            s4, d4 = 20, f"全市场主力净流入{mkt_flow:+.0f}亿，资金跑步入场"
        elif mkt_flow >= 200:
            s4, d4 = 16, f"全市场主力净流入{mkt_flow:+.0f}亿，机构积极入场"
        elif mkt_flow >= 50:
            s4, d4 = 12, f"全市场主力净流入{mkt_flow:+.0f}亿，温和净流入"
        elif mkt_flow >= 0:
            s4, d4 = 8, f"全市场主力净流入{mkt_flow:+.0f}亿，观望为主"
        else:
            if mkt_flow <= -500:
                s4, d4 = 4, f"全市场主力净流出{mkt_flow:+.0f}亿，机构大幅出逃"
            elif mkt_flow <= -200:
                s4, d4 = 8, f"全市场主力净流出{mkt_flow:+.0f}亿，机构减仓"
            else:
                s4, d4 = 10, f"全市场主力净流出{mkt_flow:+.0f}亿，轻微净流出"
    else:
        s4, d4 = 10, "全市场资金数据暂缺"
    score += s4

    # 5. 两融余额（满分20）— AKShare数据不稳定，默认10分
    s5, d5 = 10, "两融余额数据暂缺"

    # 6. 沪深300方向（满分20）
    csi300_pct = None
    if indices:
        for idx in indices:
            if "沪深300" in idx["name"]:
                csi300_pct = idx["pct"]
                break
    if csi300_pct is not None:
        if csi300_pct >= 2:
            s6, d6 = 20, f"沪深300 {csi300_pct:+.2f}%，大盘权重强势"
        elif csi300_pct >= 1:
            s6, d6 = 16, f"沪深300 {csi300_pct:+.2f}%，大盘稳健"
        elif csi300_pct >= 0:
            s6, d6 = 12, f"沪深300 {csi300_pct:+.2f}%，权重平稳"
        elif csi300_pct >= -1:
            s6, d6 = 8, f"沪深300 {csi300_pct:+.2f}%，权重偏弱"
        else:
            s6, d6 = 4, f"沪深300 {csi300_pct:+.2f}%，大盘重挫"
    else:
        s6, d6 = 10, "沪深300数据暂缺"
    score += s6

    if score >= 85:
        level, desc = "🟢 极强多头", "市场情绪高涨，赚钱效应极强，短线/波段积极做多"
    elif score >= 68:
        level, desc = "🟡 多头偏强", "市场氛围较好，涨停家数维持高位，可维持5-7成仓位"
    elif score >= 52:
        level, desc = "⚪ 中性震荡", "多空僵持，赚钱效应一般，控制仓位观望为主"
    elif score >= 36:
        level, desc = "🟠 偏空谨慎", "市场情绪转弱，涨停家数偏低，保持3-5成仓位防守"
    else:
        level, desc = "🔴 极弱空头", "市场恐慌情绪蔓延，涨停家数骤降，清仓或空仓防守为主"

    return {
        "总分": score,
        "等级": level,
        "描述": desc,
        "五维明细": [d1, d2, d3, d4, d5, d6]
    }


# ─────────────────────────────────────────────
# 报告生成
# ─────────────────────────────────────────────

def build_report(indices, zt_count, dt_count, north, mkt_flow, sectors, hot, sentiment, today_str):
    lines = [f"📋 【A股晚报】{today_str}\n"]

    # 指数
    lines.append("━━━ A股收盘 ━━━")
    if indices:
        for idx in indices:
            arrow = "▲" if idx["pct"] >= 0 else "▼"
            lines.append(f"  {idx['name']}：{idx['price']:.2f}（{arrow}{abs(idx['pct']):.2f}%）")
    else:
        lines.append("  指数数据获取失败")

    # 情绪
    s = sentiment
    lines.append(f"\n━━━ 市场情绪 ━━━")
    lines.append(f"  综合评分：{s['总分']}/100 {s['等级']}")
    # 市场情绪（只显示总分，不显示逐维明细）
    lines.append("\n━━━ 市场情绪 ━━━")
    if zt_count is not None:
        lines.append(f"  涨停家数：约{zt_count}家（含ST）")
    else:
        lines.append("  涨停家数：暂无法获取")
    if dt_count is not None:
        lines.append(f"  跌停家数：约{dt_count}家")
    if north is not None:
        d = "净流入" if north >= 0 else "净流出"
        lines.append(f"  北向资金：{d}{abs(north):.2f}亿")
    if mkt_flow is not None:
        d = "净流入" if mkt_flow >= 0 else "净流出"
        lines.append(f"  全市场主力资金净流入：{d}{abs(mkt_flow):.0f}亿")

    lines.append(f"\n  量化情绪打分：综合评分 {s['总分']}/100 {s['等级']}")

    # 热点板块
    if sectors:
        lines.append("\n━━━ 行业资金净流入前三 ━━━")
        for i, s_item in enumerate(sectors, 1):
            lines.append(f"  {i}. {s_item}")
    if hot:
        lines.append("\n━━━ 概念板块涨幅前五 ━━━")
        for i, s_item in enumerate(hot, 1):
            lines.append(f"  {i}. {s_item}")

    lines.append(f"\n━━━━━━━━ {TS} ━━━━")
    lines.append("⚠️ 仅供参考，不构成投资建议。股市有风险，投资需谨慎。")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────

def main():
    print(f"\n[{TS}] 生成晚报...")

    indices = get_index_data()
    zt_count, dt_count = get_market_stats()
    north = get_north_bound()
    mkt_flow = get_market_net_flow()
    sectors = get_sector_flow()
    hot = get_top_sectors()

    # 计算情绪分
    sentiment = calc_sentiment(zt_count, dt_count, north, mkt_flow, indices)
    print(f"情绪打分：{sentiment['总分']}/100 {sentiment['等级']}")
    for d in sentiment["五维明细"]:
        print(f"  • {d}")

    # 生成报告
    report = build_report(indices, zt_count, dt_count, north, mkt_flow, sectors, hot, sentiment, TODAY)
    print("\n" + "="*40)
    print(report)
    print("="*40)

    # 推送
    err = wx_push(report)

    if err == 0:
        print("\n✅ 晚报已推送至企业微信")
    else:
        print(f"\n❌ 推送失败")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        indices = get_index_data()
        zt, dt = get_market_stats()
        north = get_north_bound()
        mkt = get_market_net_flow()
        sectors = get_sector_flow()
        hot = get_top_sectors()
        s = calc_sentiment(zt, dt, north, mkt, indices)
        print(f"SENTIMENT:{s['总分']}/100|{s['等级']}|{s['描述']}")
        print(f"ZTC:{zt}|DTC:{dt}|NORTH:{north}|MKT:{mkt}")
        if indices:
            for idx in indices:
                print(f"IDX:{idx['name']}|{idx['price']}|{idx['pct']}")
    else:
        main()
