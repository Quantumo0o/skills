#!/usr/bin/env python3
"""查询股票实时行情（仅支持主动拉取，不支持推送）。

行情级别:
  港股: L2（含盘口、经纪商队列）
  美股: L1（支持盘前/盘中/盘后）
  A 股（港股通）: L1

标的代码格式: marketCode + stockCode
  港股: hk00700（腾讯）
  美股: usAAPL（苹果）
  A 股: sh600519（贵州茅台）、sz000001（平安银行）

用法:
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py quote hk00700 usAAPL sh600519       # 批量报价
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py orderbook hk00700                    # 盘口（港股 L2）
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py orderbook sh600519                   # 盘口（A 股 L1）
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py kline hk00700 --ktype day -n 30      # K 线
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py min hk00700                          # 分时
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py tick hk00700 -n 20                   # 逐笔成交
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_price.py broker hk00700                       # 经纪商队列（仅港股 L2）
"""

import argparse
import sys
from _client import get_client, dump_json, add_common_args


def cmd_quote(args):
    """批量报价 — 港股 L2 / 美股 L1 / A 股(港股通) L1"""
    client = get_client(args.api_key, args.base_url)
    result = client.market.quote(codes=args.codes, fields=args.fields)
    dump_json(result)


def cmd_orderbook(args):
    """盘口/买卖档 — 港股 L2 / 美股 L1 / A 股 L1"""
    client = get_client(args.api_key, args.base_url)
    result = client.market.orderbook(args.code, count=args.count)
    dump_json(result)


def cmd_kline(args):
    client = get_client(args.api_key, args.base_url)
    result = client.market.kline(args.code, ktype=args.ktype, num=args.num)
    dump_json(result)


def cmd_min(args):
    client = get_client(args.api_key, args.base_url)
    result = client.market.min(args.code, count=args.count)
    dump_json(result)


def cmd_tick(args):
    client = get_client(args.api_key, args.base_url)
    result = client.market.tick(args.code, count=args.num, id=args.start_id)
    dump_json(result)


def cmd_broker(args):
    """经纪商队列 — 仅港股 L2"""
    client = get_client(args.api_key, args.base_url)
    result = client.market.broker_list(args.code)
    dump_json(result)


def main():
    parser = argparse.ArgumentParser(description="查询股票实时行情（港股L2 / 美股L1 / A股L1）")
    add_common_args(parser)
    sub = parser.add_subparsers(dest="command", required=True)

    p_quote = sub.add_parser("quote", help="批量报价（港股L2/美股L1/A股L1）")
    p_quote.add_argument("codes", nargs="+", help="标的代码列表: hk00700 usAAPL sh600519 sz000001")
    p_quote.add_argument("--fields", nargs="*", help="指定返回字段")
    p_quote.set_defaults(func=cmd_quote)

    p_ob = sub.add_parser("orderbook", help="盘口/买卖档")
    p_ob.add_argument("code", help="标的代码: hk00700 / usAAPL / sh600519 / sz000001")
    p_ob.add_argument("--count", type=int, default=5, help="档位数（默认 5）")
    p_ob.set_defaults(func=cmd_orderbook)

    p_kl = sub.add_parser("kline", help="K 线")
    p_kl.add_argument("code", help="标的代码: hk00700 / usAAPL / sh600519")
    p_kl.add_argument("--ktype", default="day", help="K 线类型: day/week/month/year/min1/min5/min15/min30/min60")
    p_kl.add_argument("-n", "--num", type=int, default=30, help="返回条数（默认 30）")
    p_kl.set_defaults(func=cmd_kline)

    p_min = sub.add_parser("min", help="分时数据")
    p_min.add_argument("code", help="标的代码: hk00700 / usAAPL / sh600519")
    p_min.add_argument("--count", type=int, default=5, help="返回天数（默认 5）")
    p_min.set_defaults(func=cmd_min)

    p_tick = sub.add_parser("tick", help="逐笔成交")
    p_tick.add_argument("code", help="标的代码: hk00700 / usAAPL / sh600519")
    p_tick.add_argument("-n", "--num", type=int, default=20, help="返回条数（默认 20）")
    p_tick.add_argument("--start-id", type=int, default=-1, help="起始 ID，-1 为最新（默认 -1）")
    p_tick.set_defaults(func=cmd_tick)

    p_br = sub.add_parser("broker", help="经纪商队列（仅港股 L2）")
    p_br.add_argument("code", help="港股标的代码: hk00700")
    p_br.set_defaults(func=cmd_broker)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
