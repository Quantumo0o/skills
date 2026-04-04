#!/usr/bin/env python3
"""
收盘小结脚本
--dry-run  计算情绪分并打印数据，不推送
默认       完整运行：抓数据+计算情绪分+生成报告→推送
"""
import sys, os, urllib.request, json
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from keys_loader import wx_push, get_webhook_url

NOW = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
TODAY = NOW.strftime("%Y年%m月%d日")
DATE_STR = NOW.strftime("%Y%m%d")
TS = NOW.strftime("%Y-%m-%d %H:%M")


def fetch(url, encoding="gbk"):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode(encoding, errors="replace")
    except Exception:
        return "ERROR"


def get_index_data():
    codes = "sh000001,sz399001,sz399006,sh000688,sh000300,sh000905"
    raw = fetch(f"https://qt.gtimg.cn/q={codes}")
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
    try:
        import akshare as ak
        zt = ak.stock_zt_pool_em(date=DATE_STR)
        dt = ak.stock_zt_pool_em(date=DATE_STR, zt_pool_str="跌停")
        return (len(zt) if zt is not None else 0,
                len(dt) if dt is not None else 0)
    except Exception:
        return None, None


def get_north_bound():
    try:
        import akshare as ak
        df = ak.stock_hsgt_north_net_flow_em(symbol="北向资金")
        if df is not None and len(df) > 0:
            net = df.iloc[-1].get("最新", 0)
            return float(net) if net else None
    except Exception:
        return None


def get_sector_flow():
    """行业资金流向：净流入前三 + 净流出前三"""
    try:
        import akshare as ak
        df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流向")
        if df is not None:
            col = next((c for c in df.columns if "净流入" in c and "超" not in c), None)
            if col is None:
                return [], []
            inflow = df.sort_values(col, ascending=False).head(3)
            outflow = df.sort_values(col, ascending=True).head(3)
            top = [f"{r.iloc[0]}: +{abs(r.iloc[1]):.0f}亿" for _, r in inflow.iterrows()]
            bot = [f"{r.iloc[0]}: -{abs(r.iloc[1]):.0f}亿" for _, r in outflow.iterrows()]
            return top, bot
    except Exception:
        return [], []


def get_concept_sectors():
    """概念板块涨幅前5 + 跌幅前5"""
    try:
        import akshare as ak
        df = ak.stock_board_concept_name_em()
        if df is not None:
            hot = df.sort_values("涨跌幅", ascending=False).head(5)
            cold = df.sort_values("涨跌幅", ascending=True).head(5)
            return (
                [f"{r['板块名称']}（{r['涨跌幅']:+.2f}%）" for _, r in hot.iterrows()],
                [f"{r['板块名称']}（{r['涨跌幅']:+.2f}%）" for _, r in cold.iterrows()],
            )
    except Exception:
        return [], []


def calc_sentiment(zt_count, dt_count, north_net, indices):
    """6维量化情绪打分，满分100"""
    score = 0

    # 1. 涨停数量（满分10）
    if zt_count is not None:
        s1 = 10 if zt_count >= 100 else 8 if zt_count >= 60 else 5 if zt_count >= 30 else 2
        d1 = f"涨停{sec_count}家"
    else:
        s1, d1 = 5, "涨停数据暂缺"
    score += s1

    # 2. 涨跌停比（满分10）
    if zt_count is not None and dt_count is not None and dt_count > 0:
        ratio = zt_count / dt_count
        s2 = 10 if ratio >= 5 else 8 if ratio >= 3 else 5 if ratio >= 1.5 else 2
        d2 = f"涨跌停比={ratio:.1f}倍"
    else:
        s2, d2 = 5, "数据暂缺"
    score += s2

    # 3. 北向资金（满分20）
    if north_net is not None:
        abs_n = abs(north_net)
        if north_net >= 100: s3 = 20
        elif north_net >= 50: s3 = 15
        elif north_net >= 20: s3 = 10
        elif north_net >= 0: s3 = 6
        elif abs_n >= 100: s3 = 4
        elif abs_n >= 50: s3 = 8
        else: s3 = 12
        d3 = f"北向{'净流入' if north_net >= 0 else '净流出'}{abs_n:.0f}亿"
    else:
        s3, d3 = 10, "北向数据暂缺"
    score += s3

    # 4. 沪深300（满分20）
    csi = next((x["pct"] for x in indices if "沪深300" in x["name"]), None)
    if csi is not None:
        s4 = 20 if csi >= 2 else 16 if csi >= 1 else 12 if csi >= 0 else 8
        d4 = f"沪深300 {csi:+.2f}%"
    else:
        s4, d4 = 10, "沪深300数据暂缺"
    score += s4

    # 5. 两融（满分20，默认10）
    s5, d5 = 10, "两融数据暂缺"
    # 6. 全市场主力（满分20，默认10）
    s6, d6 = 10, "全市场资金数据暂缺"

    total = s1 + s2 + s3 + s4 + s5 + s6
    if total >= 85: level, desc = "🟢 极强多头", "市场情绪高涨，赚钱效应极强"
    elif total >= 68: level, desc = "🟡 多头偏强", "市场氛围较好"
    elif total >= 52: level, desc = "⚪ 中性震荡", "多空僵持"
    elif total >= 36: level, desc = "🟠 偏空谨慎", "情绪转弱，防守为主"
    else: level, desc = "🔴 极弱空头", "恐慌情绪蔓延，清仓防守"

    return {"总分": total, "等级": level, "描述": desc, "明细": [d1, d2, d3, d4, d5, d6]}


def build_report(indices, zt, dt, north, top_s, bot_s, hot, cold, sentiment, today_str):
    """生成收盘小结完整报告"""
    # 整体走势判断
    avg_pct = sum(i["pct"] for i in indices) / len(indices) if indices else 0
    trend = "收涨" if avg_pct >= 0 else "收跌"

    lines = [f"📊 【A股收盘小结】{today_str}\n"]

    # 一、主要股指
    lines.append("【一，主要股指表现】")
    lines.append(f"{trend}：")
    for idx in indices:
        arrow = "↑" if idx["pct"] >= 0 else "↓"
        lines.append(f"• {idx['name']}：{idx['price']:.2f}，{arrow}{abs(idx['pct']):.2f}%")

    csi = next((i for i in indices if "沪深300" in i["name"]), None)
    csi_pct = csi["pct"] if csi else 0
    if avg_pct > 1:
        summary = f"主要股指全线上涨，市场做多情绪较强，沪深300 {csi_pct:+.2f}%"
    elif avg_pct > 0:
        summary = f"市场温和收涨，权重股表现较稳，沪深300 {csi_pct:+.2f}%"
    elif avg_pct > -1:
        summary = f"市场小幅收跌，整体表现平稳，沪深300 {csi_pct:+.2f}%"
    else:
        summary = f"主要股指全线下跌，沪深300 {csi_pct:+.2f}%，市场偏弱"
    lines.append(f"📍 {summary}")

    # 二、资金流向
    lines.append("\n【二，资金流向】")
    if north is not None:
        d = "净流入" if north >= 0 else "净流出"
        lines.append(f"北向资金：{d}{abs(north):.2f}亿")
    if top_s:
        lines.append("行业主力净流入前三：")
        for i, s in enumerate(top_s, 1): lines.append(f"  {i}. {s}")
    if bot_s:
        lines.append("行业主力流出前三：")
        for i, s in enumerate(bot_s, 1): lines.append(f"  {i}. {s}")

    # 三、板块表现
    lines.append("\n【三，板块表现】")
    if hot:
        lines.append("🚀 强势板块：")
        for i, s in enumerate(hot[:3], 1): lines.append(f"  ① {s}")
    if cold:
        lines.append("❄️ 弱势板块：")
        for i, s in enumerate(cold[:3], 1): lines.append(f"  ① {s}")

    # 四、量化情绪打分
    lines.append("\n【四，量化情绪打分】")
    if zt is not None:
        lines.append(f"• 涨停家数：约{sec_count}家")
    if dt is not None:
        lines.append(f"• 跌停家数：约{dt}家")
    s = sentiment
    lines.append(f"• 市场情绪：综合评分 {s['总分']}/100 {s['等级']}，{s['描述']}")

    # 五、概念板块
    if hot or cold:
        lines.append("\n【五，概念板块表现】")
        if hot:
            lines.append("涨幅前5：")
            for i, s_item in enumerate(hot, 1): lines.append(f"  {i}. {s_item}")
        if cold:
            lines.append("跌幅前5：")
            for i, s_item in enumerate(cold, 1): lines.append(f"  {i}. {s_item}")

    lines.append(f"\n━━━━━━━━ 数据来源：腾讯财经·东方财富AKShare ━━━━")
    lines.append("⚠️ 仅供参考，不构成投资建议。股市有风险，投资需谨慎。")
    return "\n".join(lines)


def main():
    indices = get_index_data()
    zt, dt = get_market_stats()
    north = get_north_bound()
    top_s, bot_s = get_sector_flow()
    hot, cold = get_concept_sectors()
    sentiment = calc_sentiment(zt, dt, north, indices)

    print(f"\n[{TS}] 收盘小结数据获取完成")
    for idx in indices:
        arrow = "↑" if idx["pct"] >= 0 else "↓"
        print(f"  {idx['name']}：{idx['price']:.2f}，{arrow}{abs(idx['pct']):.2f}%")
    print(f"  量化情绪：{sentiment['总分']}/100 {sentiment['等级']}")

    report = build_report(indices, zt, dt, north, top_s, bot_s, hot, cold, sentiment, TODAY)
    err = wx_push(report)
    if err == 0:
        print("\n✅ 收盘小结已推送至企业微信")
    else:
        print(f"\n❌ 推送失败，errcode={err}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        indices = get_index_data()
        zt, dt = get_market_stats()
        north = get_north_bound()
        top_s, bot_s = get_sector_flow()
        hot, cold = get_concept_sectors()
        sentiment = calc_sentiment(zt, dt, north, indices)
        print(f"SENTIMENT:{sentiment['总分']}/100|{sentiment['等级']}|{sentiment['描述']}")
        print(f"ZTC:{zt}|DTC:{dt}|NORTH:{north}")
        for s in top_s: print(f"INFLOW:{s}")
        for s in bot_s: print(f"OUTFLOW:{s}")
        for s in hot: print(f"HOT:{s}")
        for s in cold: print(f"COLD:{s}")
        for idx in indices: print(f"IDX:{idx['name']}|{idx['price']}|{idx['pct']}")
    else:
        main()
