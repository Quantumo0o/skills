"""
AKShare 金融数据采集器
基于 AKShare 库获取A股、金融市场数据

依赖: pip install akshare
"""

import akshare as ak
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..base import BaseCollector, StructuredItem


class AkshareCollector(BaseCollector):
    """AKShare金融数据采集器"""
    
    name = "akshare"
    description = "AKShare金融数据 - A股、基金、期货、期权等"
    
    def __init__(self):
        self.enabled = True
    
    def collect(self, symbol: str = None, **kwargs) -> List[StructuredItem]:
        """
        采集金融数据
        
        Args:
            symbol: 股票代码，如 "000001"（平安银行）
            **kwargs: 其他参数，如 limit, date 等
        """
        result_type = kwargs.get("type", "stock")
        
        if result_type == "stock" or result_type == "quote":
            return self.collect_stock_quote(symbol, **kwargs)
        elif result_type == "fund":
            return self.collect_fund(symbol, **kwargs)
        elif result_type == "index":
            return self.collect_index(symbol, **kwargs)
        elif result_type == "money_flow":
            return self.collect_money_flow(symbol, **kwargs)
        else:
            return self.collect_stock_quote(symbol, **kwargs)
    
    def collect_stock_quote(self, symbol: str = None, **kwargs) -> List[StructuredItem]:
        """采集股票行情"""
        items = []
        try:
            if symbol:
                # 单只股票
                df = ak.stock_zh_a_spot_em()
                stock_df = df[df['代码'] == symbol]
                if len(stock_df) > 0:
                    row = stock_df.iloc[0]
                    items.append(StructuredItem(
                        raw_id=symbol,
                        title=f"{row['名称']} ({symbol})",
                        platform="akshare",
                        price=float(row['最新价']) if row['最新价'] != '-' else 0,
                        change_pct=float(row['涨跌幅']) if row['涨跌幅'] != '-' else 0,
                        volume=int(row['成交量']) if row['成交量'] != '-' else 0,
                        timestamp=datetime.now()
                    ))
            else:
                # 全市场行情
                df = ak.stock_zh_a_spot_em()
                limit = kwargs.get("limit", 20)
                for i, row in df.head(limit).iterrows():
                    items.append(StructuredItem(
                        raw_id=str(row['代码']),
                        title=f"{row['名称']} ({row['代码']})",
                        platform="akshare",
                        price=float(row['最新价']) if row['最新价'] != '-' else 0,
                        change_pct=float(row['涨跌幅']) if row['涨跌幅'] != '-' else 0,
                        volume=int(row['成交量']) if row['成交量'] != '-' else 0,
                        timestamp=datetime.now()
                    ))
        except Exception as e:
            print(f"采集股票行情失败: {e}")
        return items
    
    def collect_fund(self, symbol: str = None, **kwargs) -> List[StructuredItem]:
        """采集基金数据"""
        items = []
        try:
            if symbol:
                # 单只基金
                df = ak.fund_open_fund_info_em(fund=symbol, indicator="累计收益率走势")
                if len(df) > 0:
                    latest = df.iloc[-1]
                    items.append(StructuredItem(
                        raw_id=symbol,
                        title=f"基金 {symbol}",
                        platform="akshare",
                        price=float(latest.get('累计收益率', 0)) if latest.get('累计收益率') else 0,
                        timestamp=datetime.now()
                    ))
            else:
                # 基金列表
                df = ak.fund_individual_basic_info_xq(symbol="")
                limit = kwargs.get("limit", 20)
                for i, row in df.head(limit).iterrows():
                    items.append(StructuredItem(
                        raw_id=str(row.get('基金代码', '')),
                        title=row.get('基金名称', ''),
                        platform="akshare",
                        timestamp=datetime.now()
                    ))
        except Exception as e:
            print(f"采集基金数据失败: {e}")
        return items
    
    def collect_index(self, symbol: str = None, **kwargs) -> List[StructuredItem]:
        """采集指数行情"""
        items = []
        try:
            if symbol:
                # 单只指数
                df = ak.stock_zh_index_spot_em()
                index_df = df[df['代码'] == symbol]
                if len(index_df) > 0:
                    row = index_df.iloc[0]
                    items.append(StructuredItem(
                        raw_id=symbol,
                        title=f"{row['名称']} ({symbol})",
                        platform="akshare",
                        price=float(row['最新价']) if row['最新价'] != '-' else 0,
                        change_pct=float(row['涨跌幅']) if row['涨跌幅'] != '-' else 0,
                        volume=int(row['成交量']) if row['成交量'] != '-' else 0,
                        timestamp=datetime.now()
                    ))
            else:
                # 主要指数
                df = ak.stock_zh_index_spot_em()
                # 上证指数、深证成指、创业板指、沪深300
                main_indices = ['000001', '399001', '399006', '000300']
                for idx in main_indices:
                    index_df = df[df['代码'] == idx]
                    if len(index_df) > 0:
                        row = index_df.iloc[0]
                        items.append(StructuredItem(
                            raw_id=idx,
                            title=f"{row['名称']} ({idx})",
                            platform="akshare",
                            price=float(row['最新价']) if row['最新价'] != '-' else 0,
                            change_pct=float(row['涨跌幅']) if row['涨跌幅'] != '-' else 0,
                            volume=int(row['成交量']) if row['成交量'] != '-' else 0,
                            timestamp=datetime.now()
                        ))
        except Exception as e:
            print(f"采集指数行情失败: {e}")
        return items
    
    def collect_money_flow(self, symbol: str = None, **kwargs) -> List[StructuredItem]:
        """采集资金流向"""
        items = []
        try:
            if symbol:
                # 个股资金流向
                df = ak.stock_individual_fund_flow(stock=symbol)
                if len(df) > 0:
                    row = df.iloc[-1]
                    items.append(StructuredItem(
                        raw_id=symbol,
                        title=f"资金流向 {symbol}",
                        platform="akshare",
                        content=str(row.to_dict()),
                        timestamp=datetime.now()
                    ))
            else:
                # 行业资金流向排名
                df = ak.stock_sector_fund_flow_rank(indicator="今日")
                limit = kwargs.get("limit", 20)
                for i, row in df.head(limit).iterrows():
                    items.append(StructuredItem(
                        raw_id=str(row.get('名称', '')),
                        title=row.get('名称', ''),
                        platform="akshare",
                        change_pct=float(row.get('今日涨跌幅', 0)),
                        content=f"主力净流入: {row.get('今日主力净流入净额', 0)}",
                        timestamp=datetime.now()
                    ))
        except Exception as e:
            print(f"采集资金流向失败: {e}")
        return items
    
    def login_required(self) -> bool:
        """AKShare大部分数据不需要登录"""
        return False


# CLI支持
if __name__ == "__main__":
    import sys
    
    collector = AkshareCollector()
    
    if len(sys.argv) < 2:
        print("AKShare 金融数据采集器")
        print("用法:")
        print("  python akshare.py stock [代码]     # 股票行情")
        print("  python akshare.py index [代码]     # 指数行情")
        print("  python akshare.py fund [代码]      # 基金数据")
        print("  python akshare.py flow [代码]      # 资金流向")
        sys.exit(1)
    
    cmd = sys.argv[1]
    symbol = sys.argv[2] if len(sys.argv) > 2 else None
    
    if cmd == "stock":
        result = collector.collect_stock_quote(symbol)
    elif cmd == "index":
        result = collector.collect_index(symbol)
    elif cmd == "fund":
        result = collector.collect_fund(symbol)
    elif cmd == "flow":
        result = collector.collect_money_flow(symbol)
    else:
        result = collector.collect_stock_quote(symbol)
    
    print(f"获取到 {len(result)} 条数据")
    for item in result:
        print(f"  {item.title}: {item.price} ({item.change_pct}%)")
