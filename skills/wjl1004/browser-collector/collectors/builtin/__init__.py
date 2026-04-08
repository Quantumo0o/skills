"""
collectors/builtin/ - 内置采集器
"""
from collectors.builtin.eastmoney import EastMoneyCollector
from collectors.builtin.xueqiu import XueqiuCollector
from collectors.builtin.akshare import AkshareCollector

__all__ = ['EastMoneyCollector', 'XueqiuCollector', 'AkshareCollector']
