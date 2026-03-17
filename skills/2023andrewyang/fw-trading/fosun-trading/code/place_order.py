#!/usr/bin/env python3
"""股票下单，支持限价单、增强限价单、特别限价单、竞价单、竞价限价单和市价单，覆盖港/美/A 股市场。

订单类型:
  auction_limit (1)  竞价限价单（港股）
  auction       (2)  竞价单（港股）
  limit         (3)  限价单（默认）
  enhanced_limit(4)  增强限价单
  special_limit (5)  特别限价单
  market        (9)  市价单

用法:
  # 港股限价买入（默认 order_type=limit）
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 00700 --direction buy --quantity 100 --price 350.000

  # 港股市价买入
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 00700 --direction buy --quantity 100 --order-type market

  # 美股市价买入（盘中，不需要 price）
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock AAPL --market us --direction buy --quantity 5 --order-type market

  # 美股限价卖出
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock AAPL --market us --direction sell --quantity 5 --price 180.00 --currency USD

  # A 股（港股通）限价买入
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 600519 --market sh --direction buy --quantity 100 --price 1800.00

  # 下单前校验（不实际下单）
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python place_order.py --stock 00700 --direction buy --quantity 100 --price 350.000 --check-only
"""

import argparse
import sys
from _client import get_client, get_sub_account_id, dump_json, add_common_args


DIRECTION_MAP = {"buy": 1, "sell": 2, "1": 1, "2": 2}

MARKET_CURRENCY = {"hk": "HKD", "us": "USD", "sh": "CNH", "sz": "CNH"}

ORDER_TYPE_MAP = {
    "auction_limit": 1,
    "auction": 2,
    "limit": 3,
    "enhanced_limit": 4,
    "special_limit": 5,
    "market": 9,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "9": 9,
}

ORDER_TYPE_LABELS = {
    1: "竞价限价单",
    2: "竞价单",
    3: "限价单",
    4: "增强限价单",
    5: "特别限价单",
    9: "市价单",
}

PRICE_NOT_REQUIRED = {2, 9}


def main():
    parser = argparse.ArgumentParser(
        description="股票下单（支持限价单/增强限价单/特别限价单/竞价单/竞价限价单/市价单）",
    )
    add_common_args(parser)

    parser.add_argument("--stock", required=True, help="股票代码（不含市场前缀），如 00700 / AAPL / 600519")
    parser.add_argument("--direction", required=True, help="方向: buy / sell（或 1 / 2）")
    parser.add_argument("--quantity", required=True, help="委托数量")
    parser.add_argument(
        "--order-type", default="limit",
        help="订单类型: auction_limit(1) / auction(2) / limit(3,默认) / enhanced_limit(4) / special_limit(5) / market(9)",
    )
    parser.add_argument("--price", help="委托价格（市价单可不传；港股 3 位小数，美股 2 位小数，A 股 2 位小数）")
    parser.add_argument("--market", default="hk", choices=["hk", "us", "sh", "sz"],
                        help="市场: hk(默认) / us / sh / sz")
    parser.add_argument("--currency", help="币种（默认根据市场自动选择: HKD/USD/CNH）")
    parser.add_argument("--check-only", action="store_true", help="仅查询买卖信息，不实际下单")
    parser.add_argument("--exp-type", type=int, help="订单时效: 1=当日有效（默认），2=撤单前有效（GTC）")

    args = parser.parse_args()

    direction = DIRECTION_MAP.get(args.direction.lower())
    if direction is None:
        print(f"错误: 无效方向 '{args.direction}'，请使用 buy/sell 或 1/2", file=sys.stderr)
        sys.exit(1)

    order_type = ORDER_TYPE_MAP.get(args.order_type.lower() if args.order_type else "limit")
    if order_type is None:
        print(f"错误: 无效订单类型 '{args.order_type}'，可选: auction_limit/auction/limit/enhanced_limit/special_limit/market 或 1/2/3/4/5/9",
              file=sys.stderr)
        sys.exit(1)

    if order_type not in PRICE_NOT_REQUIRED and not args.price:
        print(f"错误: {ORDER_TYPE_LABELS[order_type]}必须提供 --price 参数", file=sys.stderr)
        sys.exit(1)

    currency = args.currency or MARKET_CURRENCY.get(args.market, "HKD")

    client = get_client(args.api_key, args.base_url)
    sub_id = args.sub_account_id or get_sub_account_id(client)

    if args.check_only:
        kwargs = dict(
            sub_account_id=sub_id,
            stock_code=args.stock,
            order_type=order_type,
            market_code=args.market,
            direction=direction,
        )
        if args.quantity:
            kwargs["quantity"] = args.quantity
        if args.price:
            kwargs["price"] = args.price
        result = client.trade.get_bid_ask_info(**kwargs)
        dump_json(result)
        return

    kwargs = dict(
        sub_account_id=sub_id,
        stock_code=args.stock,
        direction=direction,
        order_type=order_type,
        quantity=args.quantity,
        market_code=args.market,
        currency=currency,
    )
    if args.price:
        kwargs["price"] = args.price
    if args.exp_type is not None:
        kwargs["exp_type"] = args.exp_type
    kwargs["allow_pre_post"] = 0

    order = client.trade.create_order(**kwargs)
    dump_json(order)


if __name__ == "__main__":
    main()
