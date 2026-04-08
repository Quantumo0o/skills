#!/usr/bin/env python3
"""
collectors/cli.py - 统一命令行入口
用法：
    python collectors/cli.py --collector eastmoney --action quote 600000
    python collectors/cli.py --collector eastmoney --action fund 000001
    python collectors/cli.py --collector eastmoney --action limit-up --limit 50
    python collectors/cli.py --collector xueqiu --action hot --limit 20
    python collectors/cli.py --list
"""

import argparse
import sys
import json
import os
from pathlib import Path

# 添加 skill 根目录到 path
sys.path.insert(0, str(Path(__file__).parent.parent))


def cmd_list(args):
    """列出所有可用的采集器和动作"""
    print("=" * 50)
    print("browser-collector 采集器列表")
    print("=" * 50)

    collectors = {
        "eastmoney": {
            "class": "EastMoneyCollector",
            "actions": {
                "quote": "get_stock_quote <code> - 股票实时行情",
                "fund": "get_fund_nav <code> - 基金净值",
                "index": "get_index_quote [code=000001] - 指数行情",
                "flow": "get_money_flow <code> - 资金流向",
                "top-flow": "get_top_money_flow - 主力资金排行",
                "limit-up": "get_limit_up - 涨停股",
                "limit-down": "get_limit_down - 跌停股",
                "turnover": "get_top_turnover - 换手率排行",
            }
        },
        "xueqiu": {
            "class": "XueqiuCollector",
            "actions": {
                "discussions": "get_stock_discussions <symbol> - 股票讨论帖",
                "hot": "get_hot_stocks - 热门股票",
                "search": "search_discussions <keyword> - 搜索讨论帖",
            }
        }
    }

    for name, info in collectors.items():
        print(f"\n{name} ({info['class']})")
        print("-" * 40)
        for action, desc in info['actions'].items():
            print(f"  {action:15s} {desc}")

    print("\n" + "=" * 50)
    return 0


def cmd_eastmoney(args):
    """东方财富采集器"""
    from collectors.builtin.eastmoney import EastMoneyCollector

    collector = EastMoneyCollector()

    if args.action == "quote":
        if not args.code:
            print("错误: 需要指定股票代码")
            return 1
        quote = collector.get_stock_quote(args.code)
        if quote:
            print(json.dumps(quote.to_dict(), ensure_ascii=False, indent=2))
        else:
            print("获取行情失败")
            return 1

    elif args.action == "fund":
        if not args.code:
            print("错误: 需要指定基金代码")
            return 1
        fund = collector.get_fund_nav(args.code)
        if fund:
            print(json.dumps(fund.to_dict(), ensure_ascii=False, indent=2))
        else:
            print("获取基金净值失败")
            return 1

    elif args.action == "index":
        code = args.code or "000001"
        idx = collector.get_index_quote(code)
        if idx:
            print(json.dumps(idx.to_dict(), ensure_ascii=False, indent=2))
        else:
            print("获取指数行情失败")
            return 1

    elif args.action == "flow":
        if not args.code:
            print("错误: 需要指定股票代码")
            return 1
        flow = collector.get_money_flow(args.code)
        if flow:
            print(json.dumps(flow.to_dict(), ensure_ascii=False, indent=2))
        else:
            print("获取资金流向失败")
            return 1

    elif args.action == "top-flow":
        flows = collector.get_top_money_flow(limit=args.limit)
        print(f"获取到 {len(flows)} 条资金流向数据")
        for f in flows[:5]:
            print(f"  {f.stock_name}: 净流入 {f.net_inflow:.2f}万" if f.net_inflow else "")

    elif args.action == "limit-up":
        items = collector.get_limit_up(direction="up", limit=args.limit)
        print(f"获取到 {len(items)} 只涨停股")
        for item in items[:10]:
            print(f"  {item.name}: {item.change_pct:.2f}%")

    elif args.action == "limit-down":
        items = collector.get_limit_up(direction="down", limit=args.limit)
        print(f"获取到 {len(items)} 只跌停股")
        for item in items[:10]:
            print(f"  {item.name}: {item.change_pct:.2f}%")

    elif args.action == "turnover":
        items = collector.get_top_turnover(limit=args.limit)
        print(f"获取到 {len(items)} 只高换手率股")
        for item in items[:10]:
            print(f"  {item.name}: 换手率 {item.turnover:.2f}%")

    else:
        print(f"未知动作: {args.action}")
        return 1

    return 0


def cmd_xueqiu(args):
    """雪球采集器"""
    from collectors.builtin.xueqiu import XueqiuCollector

    collector = XueqiuCollector()

    if args.action == "discussions":
        if not args.code:
            print("错误: 需要指定股票代码 (格式: SH600000)")
            return 1
        discussions = collector.get_stock_discussions(args.code, limit=args.limit)
        print(f"获取到 {len(discussions)} 条讨论")
        for d in discussions[:5]:
            print(f"  [{d.sentiment}] {d.title[:40]}... (赞: {d.like_count})")

    elif args.action == "hot":
        stocks = collector.get_hot_stocks(limit=args.limit)
        print(f"获取到 {len(stocks)} 只热门股票")
        for s in stocks[:10]:
            print(f"  #{s.rank} {s.stock_name}: {s.change_pct}%")

    elif args.action == "search":
        if not args.code:
            print("错误: 需要指定搜索关键词")
            return 1
        results = collector.search_discussions(args.code, limit=args.limit)
        print(f"搜索到 {len(results)} 条讨论")
        for d in results[:5]:
            print(f"  [{d.sentiment}] {d.title[:40]}...")

    else:
        print(f"未知动作: {args.action}")
        return 1

    return 0


def main():
    parser = argparse.ArgumentParser(
        description='browser-collector 统一CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --list
  %(prog)s --collector eastmoney --action quote 600000
  %(prog)s --collector eastmoney --action fund 000001
  %(prog)s --collector eastmoney --action limit-up --limit 50
  %(prog)s --collector xueqiu --action hot --limit 20
  %(prog)s --collector xueqiu --action discussions SH600000
        """
    )
    parser.add_argument('--list', action='store_true', help='列出所有采集器和动作')
    parser.add_argument('--collector', '-c', choices=['eastmoney', 'xueqiu'],
                        help='选择采集器')
    parser.add_argument('--action', '-a', help='采集动作')
    parser.add_argument('code', nargs='?', help='股票/基金代码或关键词')
    parser.add_argument('--limit', type=int, default=20, help='结果数量限制')

    args = parser.parse_args()

    if args.list:
        return cmd_list(args)

    if not args.collector or not args.action:
        parser.print_help()
        return 1

    args.code = args.code  # may be None for some actions

    if args.collector == 'eastmoney':
        return cmd_eastmoney(args)
    elif args.collector == 'xueqiu':
        return cmd_xueqiu(args)
    else:
        print(f"未知采集器: {args.collector}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
