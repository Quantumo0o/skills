#!/usr/bin/env python3
"""
collectors/base.py - 统一数据结构定义
金融数据采集器统一数据格式：股票行情、基金净值、指数、资金流向、讨论帖、热门股票
"""

import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class StructuredItem:
    """
    统一数据结构 - 适用于所有采集器

    金融相关字段：price, change_pct, volume, raw_id
    内容相关字段：author, tags, content
    元数据：checksum, quality_score
    """
    title: str
    url: str
    platform: str
    timestamp: datetime = field(default_factory=datetime.now)

    price: Optional[float] = None
    change_pct: Optional[float] = None
    volume: Optional[int] = None
    raw_id: Optional[str] = None

    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    content: Optional[str] = None

    checksum: Optional[str] = None
    quality_score: Optional[float] = None

    def __post_init__(self):
        if self.checksum is None:
            self.checksum = self._generate_checksum()

    def _generate_checksum(self) -> str:
        content = f"{self.raw_id or ''}{self.title}{self.price}{self.timestamp.isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['timestamp'] = self.timestamp.isoformat()
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StructuredItem':
        if isinstance(data.get('timestamp'), str):
            data = dict(data)
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


@dataclass
class StockQuote(StructuredItem):
    """股票行情数据"""
    symbol: Optional[str] = None
    name: Optional[str] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    prev_close: Optional[float] = None
    amount: Optional[float] = None
    market_cap: Optional[float] = None
    float_cap: Optional[float] = None

    def __post_init__(self):
        super().__post_init__()
        if self.price and self.close is None:
            self.close = self.price


@dataclass
class FundNAV(StructuredItem):
    """基金净值数据"""
    fund_code: Optional[str] = None
    fund_name: Optional[str] = None
    nav: Optional[float] = None
    accum_nav: Optional[float] = None
    daily_growth: Optional[float] = None
    subscribe_status: Optional[str] = None
    redeem_status: Optional[str] = None

    @property
    def change_pct(self) -> Optional[float]:
        return self.daily_growth

    @change_pct.setter
    def change_pct(self, value):
        self.daily_growth = value


@dataclass
class IndexQuote(StructuredItem):
    """指数行情数据"""
    index_code: Optional[str] = None
    index_name: Optional[str] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    prev_close: Optional[float] = None

    def __post_init__(self):
        super().__post_init__()
        if self.price and self.close is None:
            self.close = self.price


@dataclass
class MoneyFlow(StructuredItem):
    """资金流向数据"""
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    net_amount: Optional[float] = None
    net_inflow: Optional[float] = None
    retail_inflow: Optional[float] = None
    main_inflow_rate: Optional[float] = None


@dataclass
class LimitUpDown(StructuredItem):
    """涨跌停数据"""
    symbol: Optional[str] = None
    name: Optional[str] = None
    turnover: Optional[float] = None
    amount: Optional[float] = None
    limit_diff: Optional[float] = None
    direction: Optional[str] = None
    market: Optional[str] = None

    @property
    def raw_id(self) -> Optional[str]:
        return self.symbol

    @raw_id.setter
    def raw_id(self, value):
        self.symbol = value


@dataclass
class Discussion(StructuredItem):
    """讨论帖/帖子数据"""
    post_id: Optional[str] = None
    user_id: Optional[str] = None
    username: Optional[str] = None
    avatar: Optional[str] = None
    comment_count: Optional[int] = None
    like_count: Optional[int] = None
    share_count: Optional[int] = None
    sentiment: Optional[str] = None

    @property
    def author(self) -> Optional[str]:
        return self.username

    @author.setter
    def author(self, value):
        self.username = value


@dataclass
class HotStock(StructuredItem):
    """热门股票数据"""
    rank: Optional[int] = None
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    hot_score: Optional[float] = None

    @property
    def raw_id(self) -> Optional[str]:
        return self.stock_code

    @raw_id.setter
    def raw_id(self, value):
        self.stock_code = value


def items_to_dict_list(items: List[StructuredItem]) -> List[Dict[str, Any]]:
    """将 StructuredItem 列表转换为字典列表"""
    return [item.to_dict() for item in items]


# 基类
class BaseCollector:
    """采集器基类"""
    
    name = "base"
    description = "基础采集器"
    
    def __init__(self):
        self.enabled = True
    
    def collect(self, **kwargs):
        """采集数据"""
        raise NotImplementedError
    
    def login_required(self) -> bool:
        """是否需要登录"""
        return False
    
    def get_status(self) -> dict:
        """获取采集器状态"""
        return {
            "name": self.name,
            "enabled": self.enabled,
            "description": self.description,
        }


def items_to_dict_list(items: List[StructuredItem]) -> List[Dict[str, Any]]:
    """将StructuredItem列表转换为字典列表"""
    return [item.to_dict() for item in items]
