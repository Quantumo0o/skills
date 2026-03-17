#!/usr/bin/env python3
"""查询资金流水（港/美/A 股）。

用法:
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_cashflows.py                                    # 查询全部资金流水
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_cashflows.py --from-date 2025-01-01 --to-date 2025-01-31
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_cashflows.py --date 2025-03-15                  # 查询指定日期
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_cashflows.py --flow-type 1                      # 按流水类型筛选
  /Users/admin/.openclaw/workspace/.venv-fosun/bin/python query_cashflows.py --business-type 1 2                # 按业务类型筛选
"""

import argparse
import sys
from _client import get_client, get_sub_account_id, dump_json, add_common_args


def main():
    parser = argparse.ArgumentParser(description="查询资金流水（港/美/A 股）")
    add_common_args(parser)

    parser.add_argument("--from-date", help="开始日期 yyyy-mm-dd")
    parser.add_argument("--to-date", help="结束日期 yyyy-mm-dd")
    parser.add_argument("--date", help="指定日期 yyyy-mm-dd（查询单日流水）")
    parser.add_argument("--flow-type", type=int, help="流水类型")
    parser.add_argument("--business-type", nargs="*", type=int, help="业务类型（可多个）")

    args = parser.parse_args()

    client = get_client(args.api_key, args.base_url)
    sub_id = args.sub_account_id or get_sub_account_id(client)

    result = client.trade.get_cash_flows(
        sub_account_id=sub_id,
        trade_date_from=args.from_date,
        trade_date_to=args.to_date,
        flow_type=args.flow_type,
        business_type=args.business_type,
        date=args.date,
    )
    dump_json(result)


if __name__ == "__main__":
    main()
