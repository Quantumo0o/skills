"""
collectors/ - 浏览器数据采集器模块

Usage:
    # API模式（无需浏览器）
    from collectors import EastMoneyCollector, XueqiuCollector

    # 东方财富
    em = EastMoneyCollector()
    quote = em.get_stock_quote("600000")
    limit_up = em.get_limit_up(direction="up", limit=50)

    # 雪球
    xq = XueqiuCollector()
    discussions = xq.get_stock_discussions("SH600000")
    hot = xq.get_hot_stocks()

    # 浏览器模式（需Playwright）
    from browser.playwright import BrowserPlaywright
    browser = BrowserPlaywright()
    xq_browser = XueqiuCollector(browser=browser)
    hot = xq_browser.get_hot_stocks_browser()
    
    # 获取所有可用采集器
    from collectors import get_collectors
    collectors = get_collectors()
"""

from collectors.base import (
    StructuredItem,
    StockQuote,
    FundNAV,
    IndexQuote,
    MoneyFlow,
    LimitUpDown,
    Discussion,
    HotStock,
    items_to_dict_list,
)

from collectors.builtin import EastMoneyCollector, XueqiuCollector, AkshareCollector

# CLI 入口
from collectors.cli import main as cli_main

# 采集器注册表
def get_collectors():
    """获取所有注册的采集器"""
    return {
        'eastmoney': EastMoneyCollector(),
        'xueqiu': XueqiuCollector(),
        'akshare': AkshareCollector(),
    }

__all__ = [
    # 数据结构
    'StructuredItem',
    'StockQuote',
    'FundNAV',
    'IndexQuote',
    'MoneyFlow',
    'LimitUpDown',
    'Discussion',
    'HotStock',
    'items_to_dict_list',
    # 采集器
    'EastMoneyCollector',
    'XueqiuCollector',
    'AkshareCollector',
    # 注册函数
    'get_collectors',
    # CLI
    'cli_main',
]

__version__ = '1.0.0'
