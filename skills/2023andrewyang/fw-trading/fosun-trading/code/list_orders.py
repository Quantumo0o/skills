#!/usr/bin/env python3
"""查询订单列表（支持港/美/A 股），可按状态分组快捷筛选。

用法:
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py                                       # 查询最近订单
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --stock 00700                         # 按股票筛选
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --status 20 40                        # 按状态筛选（待报 + 已报）
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --status-group pending                # 快捷: 未成交订单
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --status-group filled                 # 快捷: 已成交订单
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --status-group cancelled              # 快捷: 已撤销订单
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --from-date 2025-01-01 --to-date 2025-01-31
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --direction buy --market hk
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python list_orders.py --market sh sz                        # A 股订单
"""

import argparse
import sys
from _client import get_client, get_sub_account_id, dump_json, add_common_args

STATUS_GROUPS = {
    "pending":   [10, 20, 21, 40, 60],
    "filled":    [50],
    "cancelled": [70, 80, 90, 100],
}


def main():
    parser = argparse.ArgumentParser(description="查询订单列表（港/美/A 股）")
    add_common_args(parser)

    parser.add_argument("--start", type=int, default=0, help="分页偏移（默认 0）")
    parser.add_argument("--count", type=int, default=20, help="返回数量（默认 20）")
    parser.add_argument("--stock", help="按股票代码筛选，如 00700")
    parser.add_argument("--status", nargs="*", type=int,
                        help="按状态筛选: 10=未报 20=待报 21=条件单待触发 40=已报 50=全成 60=部成 70=已撤 80=部撤 90=废单 100=已失效")
    parser.add_argument("--status-group", choices=["pending", "filled", "cancelled"],
                        help="快捷状态分组: pending=未成交 / filled=已成交 / cancelled=已撤销（与 --status 互斥）")
    parser.add_argument("--from-date", help="开始日期 yyyy-mm-dd")
    parser.add_argument("--to-date", help="结束日期 yyyy-mm-dd")
    parser.add_argument("--direction", choices=["buy", "sell"], help="方向筛选")
    parser.add_argument("--market", nargs="*", help="市场筛选: hk / us / sh / sz")
    parser.add_argument("--sort", default="desc", choices=["desc", "asc"], help="排序（默认 desc）")

    args = parser.parse_args()

    if args.status and args.status_group:
        print("错误: --status 与 --status-group 不可同时使用", file=sys.stderr)
        sys.exit(1)

    status_arr = args.status
    if args.status_group:
        status_arr = STATUS_GROUPS[args.status_group]

    client = get_client(args.api_key, args.base_url)
    sub_id = args.sub_account_id or get_sub_account_id(client)

    direction = None
    if args.direction:
        direction = 1 if args.direction == "buy" else 2

    result = client.trade.list_orders(
        sub_account_id=sub_id,
        start=args.start,
        count=args.count,
        stock_code=args.stock,
        status_arr=status_arr,
        from_date=args.from_date,
        to_date=args.to_date,
        direction=direction,
        market=args.market,
        sort=args.sort,
    )
    dump_json(result)


if __name__ == "__main__":
    main()
