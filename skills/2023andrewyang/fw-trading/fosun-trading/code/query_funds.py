#!/usr/bin/env python3
"""查询账户资金和持仓（港/美/A 股）。

用法:
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py summary                              # 资金汇总（可用资金/冻结资金/总资产）
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py summary --currency HKD               # 按币种筛选
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py summary --currency CNH               # A 股人民币资金
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py holdings                             # 持仓列表（持仓数量/当前市值/成本价）
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py holdings --symbols hk00700           # 按标的筛选
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py holdings --symbols sh600519          # A 股持仓
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py holdings --currencies CNH            # 按人民币筛选
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_funds.py accounts                             # 账户列表
"""

import argparse
import sys
from _client import get_client, get_sub_account_id, dump_json, add_common_args


def cmd_summary(args):
    """查询资金汇总: 可用资金(cashPurchasingPower) / 冻结资金(frozenBalance) / 总资产(ledgerBalance)"""
    client = get_client(args.api_key, args.base_url)
    sub_id = args.sub_account_id or get_sub_account_id(client)
    result = client.portfolio.get_assets_summary(
        sub_account_id=sub_id,
        currency=args.currency,
    )
    dump_json(result)


def cmd_holdings(args):
    """查询持仓: 持仓数量(quantity) / 当前市值(price*quantity) / 成本价(avgCost/dilutedCost)"""
    client = get_client(args.api_key, args.base_url)
    sub_id = args.sub_account_id or get_sub_account_id(client)
    result = client.portfolio.get_holdings(
        sub_account_id=sub_id,
        start=args.start,
        count=args.count,
        currencies=args.currencies,
        symbols=args.symbols,
    )
    dump_json(result)


def cmd_accounts(args):
    client = get_client(args.api_key, args.base_url)
    result = client.account.list_accounts()
    dump_json(result)


def main():
    parser = argparse.ArgumentParser(description="查询账户资金和持仓（港/美/A 股）")
    add_common_args(parser)
    sub = parser.add_subparsers(dest="command", required=True)

    p_sum = sub.add_parser("summary", help="资金汇总（可用资金/冻结资金/总资产）")
    p_sum.add_argument("--currency", help="币种筛选: HKD / USD / CNH")
    p_sum.set_defaults(func=cmd_summary)

    p_hold = sub.add_parser("holdings", help="持仓列表（持仓数量/当前市值/成本价）")
    p_hold.add_argument("--start", type=int, default=0, help="分页偏移（默认 0）")
    p_hold.add_argument("--count", type=int, default=100, help="返回数量（默认 100）")
    p_hold.add_argument("--currencies", nargs="*", help="币种筛选: HKD USD CNH")
    p_hold.add_argument("--symbols", nargs="*", help="标的筛选: hk00700 usAAPL sh600519 sz000001")
    p_hold.set_defaults(func=cmd_holdings)

    p_acct = sub.add_parser("accounts", help="账户列表")
    p_acct.set_defaults(func=cmd_accounts)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
