#!/usr/bin/env python3
"""查询股票买卖信息（每手股数、最大可买/可卖数量、购买力、可提现金等）。

调用 BidAskInfo 接口，返回下单前需要的关键参数。
响应包含：lotSize、maxQuantityBuy/maxQuantitySell、购买力、可用/可提现金、币种等。

用法:
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700                           # 港股（默认限价买入）
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --direction sell          # 港股卖出可卖数量
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock AAPL --market us                # 美股
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 600519 --market sh              # A 股（沪）
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --price 350.000           # 指定价格查询
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --order-type market          # 市价单
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --order-type enhanced_limit  # 增强限价单
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --order-type special_limit   # 特别限价单
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --order-type auction_limit   # 竞价限价单
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --order-type auction         # 竞价单
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_bidask.py --stock 00700 --lot-size-only           # 仅输出每手股数
"""

import argparse
import sys
from _client import get_client, get_sub_account_id, dump_json, add_common_args


DIRECTION_MAP = {"buy": 1, "sell": 2, "1": 1, "2": 2}

ORDER_TYPE_MAP = {
    "auction_limit": 1,
    "auction": 2,
    "limit": 3,
    "enhanced_limit": 4,
    "special_limit": 5,
    "market": 9,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "9": 9,
}


def main():
    parser = argparse.ArgumentParser(
        description="查询股票买卖信息（每手股数 lotSize、最大可买/可卖数量、购买力）",
    )
    add_common_args(parser)

    parser.add_argument("--stock", required=True, help="股票代码（不含市场前缀），如 00700 / AAPL / 600519")
    parser.add_argument("--market", default="hk", choices=["hk", "us", "sh", "sz"],
                        help="市场: hk(默认) / us / sh / sz")
    parser.add_argument("--direction", default="buy", help="方向: buy(默认) / sell（或 1 / 2）")
    parser.add_argument("--order-type", default="limit",
                        help="订单类型: auction_limit(1) / auction(2) / limit(3,默认) / enhanced_limit(4) / special_limit(5) / market(9)")
    parser.add_argument("--price", help="委托价格（可选，传入可得到更精确的可买数量）")
    parser.add_argument("--quantity", help="委托数量（可选）")
    parser.add_argument("--lot-size-only", action="store_true", help="仅输出每手股数（lotSize）")

    args = parser.parse_args()

    direction = DIRECTION_MAP.get(args.direction.lower())
    if direction is None:
        print(f"错误: 无效方向 '{args.direction}'，请使用 buy/sell 或 1/2", file=sys.stderr)
        sys.exit(1)

    order_type = ORDER_TYPE_MAP.get(args.order_type.lower() if args.order_type else "limit")
    if order_type is None:
        print(f"错误: 无效订单类型 '{args.order_type}'", file=sys.stderr)
        sys.exit(1)

    client = get_client(args.api_key, args.base_url)
    sub_id = args.sub_account_id or get_sub_account_id(client)

    kwargs = dict(
        sub_account_id=sub_id,
        stock_code=args.stock,
        order_type=order_type,
        market_code=args.market,
        direction=direction,
    )
    if args.price:
        kwargs["price"] = args.price
    if args.quantity:
        kwargs["quantity"] = args.quantity

    result = client.trade.get_bid_ask_info(**kwargs)

    if args.lot_size_only:
        data = result.get("data", result)
        lot_size = data.get("lotSize", "N/A")
        print(lot_size)
        return

    dump_json(result)


if __name__ == "__main__":
    main()
