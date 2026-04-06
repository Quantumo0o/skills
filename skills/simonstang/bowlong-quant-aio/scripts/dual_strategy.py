#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.0
优化双策略系统 — 震荡保本，趋势赚钱

核心原则：
1. 震荡市：保本优先，小盈即走
2. 趋势市：让利润奔跑，移动止盈
3. 行业龙头：每行业只选1-2名
4. 马丁加仓：下跌>10%才加，反弹保本/小盈出
5. 支撑上车：下车后在支撑位敢于重新上车
"""

import os
import sys
import logging
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════
#  股票池：10个行业 × 前2名龙头 = 20只
# ══════════════════════════════════════════════

STOCK_POOL = {
    '银行': ['600036', '601288'],      # 招商、农行
    '新能源': ['002594', '300750'],    # 比亚迪、宁德
    '白酒': ['600519', '000858'],      # 茅台、五粮液
    '家电': ['000333', '000651'],      # 美的、格力
    '医药': ['300760', '600276'],      # 迈瑞、恒瑞
    '科技': ['000063', '002415'],      # 中兴、海康
    '有色': ['601899', '000831'],      # 紫金、中国稀土
    '金融': ['601318', '600030'],      # 平安、中信
    '基建': ['601668', '600585'],      # 中建、海螺
    '军工': ['600893', '000768'],      # 航发、西飞
}

STOCK_NAMES = {
    '600036': '招商银行', '601288': '农业银行',
    '002594': '比亚迪', '300750': '宁德时代',
    '600519': '贵州茅台', '000858': '五粮液',
    '000333': '美的集团', '000651': '格力电器',
    '300760': '迈瑞医疗', '600276': '恒瑞医药',
    '000063': '中兴通讯', '002415': '海康威视',
    '601899': '紫金矿业', '000831': '中国稀土',
    '601318': '中国平安', '600030': '中信证券',
    '601668': '中国建筑', '600585': '海螺水泥',
    '600893': '航发动力', '000768': '中航西飞',
}


# ══════════════════════════════════════════════
#  工具函数
# ══════════════════════════════════════════════

def sma(s, n): return s.rolling(n).mean()
def rsi(s, n=14):
    d = s.diff()
    g = d.clip(lower=0).rolling(n).mean()
    l = (-d.clip(upper=0)).rolling(n).mean()
    return 100 - 100 / (1 + g / l.replace(0, np.nan))


def fetch_stock_data(code, start, end):
    try:
        import akshare as ak
        df = ak.stock_zh_a_hist(symbol=code, period="daily",
                                 start_date=start.replace('-', ''),
                                 end_date=end.replace('-', ''),
                                 adjust="qfq")
        df = df.rename(columns={'日期': 'date', '开盘': 'open', '最高': 'high',
                                 '最低': 'low', '收盘': 'close', '成交量': 'volume'})
        df['date'] = pd.to_datetime(df['date'])
        return df.sort_values('date').reset_index(drop=True)
    except:
        return None


# ══════════════════════════════════════════════
#  市场状态判断
# ══════════════════════════════════════════════

class MarketState(Enum):
    TREND = "trend"       # 趋势市
    OSCILLATE = "oscillate"  # 震荡市


def detect_market(df, idx) -> MarketState:
    """判断市场状态"""
    if idx < 30:
        return MarketState.OSCILLATE
    
    close = df['close']
    ma5 = sma(close, 5).iloc[idx]
    ma10 = sma(close, 10).iloc[idx]
    ma20 = sma(close, 20).iloc[idx]
    
    if pd.isna(ma5) or pd.isna(ma10) or pd.isna(ma20):
        return MarketState.OSCILLATE
    
    # 均线发散程度
    spread = abs(ma5 - ma20) / ma20
    
    # MA5与MA20偏离>3%，视为趋势
    if spread > 0.03:
        return MarketState.TREND
    
    return MarketState.OSCILLATE


# ══════════════════════════════════════════════
#  震荡策略：保本优先
# ══════════════════════════════════════════════

class OscillateStrategy:
    """
    震荡策略：保本优先，小盈即走
    
    买入条件：
    - RSI < 25 超卖
    - 价格在 MA20 附近（±5%）
    - 不追高
    
    卖出条件：
    - 盈利 3% 以上
    - RSI > 70 超买
    - 亏损 > 5% 止损
    """
    
    @staticmethod
    def should_buy(df, idx) -> Tuple[bool, str]:
        if idx < 30:
            return False, ""
        
        close = df['close']
        c = close.iloc[idx]
        ma20 = sma(close, 20).iloc[idx]
        rsi_val = rsi(close, 14).iloc[idx]
        
        if pd.isna(ma20) or pd.isna(rsi_val):
            return False, ""
        
        # 支撑位附近（MA20附近）
        if 0.95 * ma20 < c < 1.05 * ma20:
            # RSI超卖
            if rsi_val < 25:
                return True, f"RSI超卖{rsi_val:.0f}+支撑位"
            # RSI金叉上30
            if idx > 0:
                rsi_prev = rsi(close, 14).iloc[idx-1]
                if pd.notna(rsi_prev) and rsi_prev < 30 and rsi_val >= 30:
                    return True, f"RSI金叉{rsi_val:.0f}"
        
        return False, ""
    
    @staticmethod
    def should_sell(df, idx, pos) -> Tuple[bool, str]:
        close = df['close']
        c = close.iloc[idx]
        cost = pos['cost']
        rsi_val = rsi(close, 14).iloc[idx]
        
        pnl = (c - cost) / cost
        
        # 止损
        if pnl < -0.05:
            return True, f"止损{pnl:.1%}"
        
        # 小盈即走（保本优先）
        if pnl > 0.03:
            return True, f"震荡止盈{pnl:.1%}"
        
        # RSI超买
        if pd.notna(rsi_val) and rsi_val > 70:
            return True, f"RSI超买{rsi_val:.0f}"
        
        return False, ""


# ══════════════════════════════════════════════
#  趋势策略：让利润奔跑
# ══════════════════════════════════════════════

class TrendStrategy:
    """
    趋势策略：让利润奔跑，移动止盈
    
    买入条件：
    - 均线多头排列（MA5 > MA10 > MA20）
    - 放量突破
    - 价格在 MA5 上方
    
    卖出条件：
    - 盈利10%后，回撤8%止盈
    - 盈利20%后，回撤10%止盈
    - 趋势破坏（跌破MA10）
    - 亏损>8%止损
    """
    
    @staticmethod
    def should_buy(df, idx) -> Tuple[bool, str]:
        if idx < 30:
            return False, ""
        
        close = df['close']
        volume = df['volume']
        c = close.iloc[idx]
        
        ma5 = sma(close, 5).iloc[idx]
        ma10 = sma(close, 10).iloc[idx]
        ma20 = sma(close, 20).iloc[idx]
        
        if pd.isna(ma5) or pd.isna(ma10) or pd.isna(ma20):
            return False, ""
        
        # 多头排列
        if c > ma5 and ma5 > ma10 and ma10 > ma20:
            # 放量确认
            vol = volume.iloc[idx]
            vol_ma = volume.iloc[idx-5:idx].mean()
            if vol > vol_ma * 1.2:
                return True, f"趋势突破+放量{vol/vol_ma:.1f}倍"
        
        return False, ""
    
    @staticmethod
    def should_sell(df, idx, pos) -> Tuple[bool, str]:
        close = df['close']
        c = close.iloc[idx]
        cost = pos['cost']
        peak = pos.get('peak', c)
        
        ma5 = sma(close, 5).iloc[idx]
        ma10 = sma(close, 10).iloc[idx]
        
        pnl = (c - cost) / cost
        trail = (c - peak) / peak if peak > 0 else 0
        
        # 止损
        if pnl < -0.08:
            return True, f"趋势止损{pnl:.1%}"
        
        # 移动止盈
        if pnl > 0.20 and trail < -0.10:
            return True, f"移动止盈{pnl:.1%}回撤{trail:.1%}"
        
        if pnl > 0.10 and trail < -0.08:
            return True, f"移动止盈{pnl:.1%}回撤{trail:.1%}"
        
        # 趋势破坏（跌破MA10）
        if pd.notna(ma5) and pd.notna(ma10) and c < ma10 and ma5 < ma10:
            if pnl > 0:
                return True, f"趋势破坏+止盈{pnl:.1%}"
            else:
                return True, f"趋势破坏"
        
        return False, ""


# ══════════════════════════════════════════════
#  回测引擎
# ══════════════════════════════════════════════

@dataclass
class Position:
    shares: int
    cost: float
    entry_idx: int
    peak: float
    strategy: str
    sector: str
    martin_added: bool = False
    martin_cost: float = 0.0  # 马丁加仓成本


class BacktestEngine:
    def __init__(self, initial_cash=1_000_000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        self.peak_equity = initial_cash
        self.max_drawdown = 0.0
        
        self.osc_strategy = OscillateStrategy()
        self.trend_strategy = TrendStrategy()
    
    def _fee(self, amount, is_sell):
        return max(amount * 0.0003, 5) + (amount * 0.001 if is_sell else 0)
    
    def _buy(self, code, price, pct, date, idx, reason, strategy, sector):
        target = self.cash * pct
        shares = int(target / price / 100) * 100
        if shares <= 0:
            return
        
        exec_price = price * 1.001
        total = shares * exec_price
        fee = self._fee(total, False)
        
        if total + fee > self.cash:
            shares = int((self.cash * 0.95) / exec_price / 100) * 100
            if shares <= 0:
                return
            total = shares * exec_price
            fee = self._fee(total, False)
        
        self.cash -= (total + fee)
        
        if code in self.positions:
            pos = self.positions[code]
            total_cost = pos.cost * pos.shares + exec_price * shares
            pos.shares += shares
            pos.cost = total_cost / pos.shares
            pos.peak = max(pos.peak, exec_price)
        else:
            self.positions[code] = Position(
                shares=shares, cost=exec_price, entry_idx=idx,
                peak=exec_price, strategy=strategy, sector=sector
            )
        
        self.trades.append({
            'date': date, 'code': code, 'action': 'buy',
            'price': exec_price, 'shares': shares,
            'reason': reason, 'strategy': strategy, 'sector': sector
        })
        
        name = STOCK_NAMES.get(code, code)
        logger.info(f"  [买入] {name} {shares}股 @ {exec_price:.2f} | {strategy} | {reason}")
    
    def _sell(self, code, price, date, reason):
        if code not in self.positions:
            return
        
        pos = self.positions[code]
        exec_price = price * 0.999
        total = pos.shares * exec_price
        fee = self._fee(total, True)
        pnl = (exec_price - pos.cost) * pos.shares - fee
        pnl_pct = (exec_price - pos.cost) / pos.cost
        
        self.cash += (total - fee)
        del self.positions[code]
        
        self.trades.append({
            'date': date, 'code': code, 'action': 'sell',
            'price': exec_price, 'shares': pos.shares,
            'reason': reason, 'pnl': pnl, 'pnl_pct': pnl_pct,
            'strategy': pos.strategy, 'sector': pos.sector
        })
        
        name = STOCK_NAMES.get(code, code)
        logger.info(f"  [卖出] {name} {pos.shares}股 @ {exec_price:.2f} | {reason} | {pnl:+,.0f} ({pnl_pct:+.1%})")
    
    def _equity(self, prices):
        pos_val = sum(p.shares * prices.get(c, p.cost) for c, p in self.positions.items())
        return self.cash + pos_val
    
    def _get_support(self, df, idx):
        """获取支撑位"""
        close = df['close']
        ma20 = sma(close, 20).iloc[idx]
        low_20 = df['low'].iloc[max(0, idx-20):idx].min() if idx >= 20 else df['low'].iloc[:idx].min()
        return max(ma20 * 0.98, low_20)
    
    def run(self, stock_data, sector_map):
        codes = list(stock_data.keys())
        all_dates = sorted(set(d for df in stock_data.values() for d in df['date'].tolist()))
        
        logger.info(f"\n开始回测，{len(all_dates)}天，{len(codes)}只股票")
        logger.info("="*60)
        
        for i, date in enumerate(all_dates):
            date_str = str(date.date()) if hasattr(date, 'date') else str(date)
            
            # 当日价格
            prices = {c: stock_data[c].set_index('date').loc[date, 'close']
                      for c in codes if date in stock_data[c]['date'].values}
            
            if not prices:
                continue
            
            # ── 1. 检查持仓 ──
            to_sell = []
            for code, pos in list(self.positions.items()):
                if code not in prices:
                    continue
                
                cur_price = prices[code]
                if cur_price > pos.peak:
                    pos.peak = cur_price
                
                df = stock_data[code]
                idx = df[df['date'] <= date].index[-1]
                
                # 根据策略判断
                if pos.strategy == 'oscillate':
                    should, reason = self.osc_strategy.should_sell(df, idx, pos.__dict__)
                else:
                    should, reason = self.trend_strategy.should_sell(df, idx, pos.__dict__)
                
                if should:
                    to_sell.append((code, reason))
            
            for code, reason in to_sell:
                self._sell(code, prices[code], date_str, reason)
            
            # ── 2. 马丁加仓（下跌>10%时）──
            for code, pos in list(self.positions.items()):
                if code not in prices or pos.martin_added:
                    continue
                
                cur_price = prices[code]
                pnl = (cur_price - pos.cost) / pos.cost
                
                # 下跌超过10%才加仓
                if pnl < -0.10 and self.cash > 50000:
                    df = stock_data[code]
                    idx = df[df['date'] <= date].index[-1]
                    
                    # 判断支撑位
                    support = self._get_support(df, idx)
                    if cur_price <= support * 1.02:  # 接近支撑位
                        self._buy(code, cur_price, 0.15, date_str, i, 
                                 f"马丁加仓{pnl:.1%}", pos.strategy, pos.sector)
                        pos.martin_added = True
            
            # ── 3. 支撑位重新上车（刚卖出又在支撑位的）──
            # 最近5天卖出但又在支撑位的股票
            recent_sells = [t for t in self.trades[-20:] if t['action'] == 'sell' and 
                          (datetime.strptime(date_str, '%Y-%m-%d') - 
                           datetime.strptime(t['date'], '%Y-%m-%d')).days <= 5]
            
            # ── 4. 新开仓 ──
            if len(self.positions) < 8:
                candidates = []
                
                for code in codes:
                    if code in self.positions:
                        continue
                    
                    df = stock_data[code]
                    idx_list = df[df['date'] <= date].index
                    if len(idx_list) < 30:
                        continue
                    idx = idx_list[-1]
                    
                    state = detect_market(df, idx)
                    
                    if state == MarketState.TREND:
                        should, reason = self.trend_strategy.should_buy(df, idx)
                        if should:
                            candidates.append((code, 'trend', reason, idx))
                    else:
                        should, reason = self.osc_strategy.should_sell(df, idx, 
                            {'cost': df['close'].iloc[idx], 'peak': df['close'].iloc[idx]})
                        should, reason = self.osc_strategy.should_buy(df, idx)
                        if should:
                            candidates.append((code, 'oscillate', reason, idx))
                
                # 选最高分的
                for code, strategy, reason, idx in candidates[:2]:
                    if len(self.positions) >= 8:
                        break
                    if self.cash < 50000:
                        break
                    
                    sector = sector_map.get(code, 'unknown')
                    self._buy(code, prices[code], 0.20, date_str, i, reason, strategy, sector)
            
            # ── 5. 记录净值 ──
            equity = self._equity(prices)
            if equity > self.peak_equity:
                self.peak_equity = equity
            dd = (self.peak_equity - equity) / self.peak_equity
            if dd > self.max_drawdown:
                self.max_drawdown = dd
            
            self.equity_curve.append({'date': date_str, 'equity': equity, 'drawdown': dd})
        
        return self._calc()
    
    def _calc(self):
        eq = pd.Series([e['equity'] for e in self.equity_curve])
        final = eq.iloc[-1]
        total_ret = (final - self.initial_cash) / self.initial_cash
        n_years = len(eq) / 252
        annual = (1 + total_ret) ** (1/n_years) - 1 if n_years > 0 else 0
        
        daily = eq.pct_change().dropna()
        sharpe = (daily.mean() - 0.025/252) / daily.std() * np.sqrt(252) if daily.std() > 0 else 0
        calmar = annual / self.max_drawdown if self.max_drawdown > 0 else 0
        
        sells = [t for t in self.trades if t['action'] == 'sell']
        wins = [t for t in sells if t.get('pnl', 0) > 0]
        
        return {
            'initial': self.initial_cash, 'final': final,
            'total_return': total_ret, 'annual_return': annual,
            'sharpe': sharpe, 'calmar': calmar,
            'max_drawdown': self.max_drawdown,
            'win_rate': len(wins) / len(sells) if sells else 0,
            'trades': len(sells), 'trades_list': self.trades
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', default='2024-01-01')
    parser.add_argument('--end', default='2025-03-28')
    args = parser.parse_args()
    
    # 构建股票池
    all_codes = []
    sector_map = {}
    for sector, codes in STOCK_POOL.items():
        for code in codes:
            all_codes.append(code)
            sector_map[code] = sector
    
    print("\n" + "="*60)
    print("  波龙股神 V2.0 - 优化双策略系统")
    print("="*60)
    print(f"  股票池: {len(all_codes)}只（10行业 × 前2龙头）")
    print(f"  时间: {args.start} ~ {args.end}")
    print("="*60)
    print("\n  行业龙头:")
    for sector, codes in STOCK_POOL.items():
        names = [STOCK_NAMES.get(c, c) for c in codes]
        print(f"    {sector}: {', '.join(names)}")
    
    # 获取数据
    print("\n  获取数据...")
    stock_data = {}
    for code in all_codes:
        df = fetch_stock_data(code, args.start, args.end)
        if df is not None and len(df) > 50:
            stock_data[code] = df
            ret = (df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100
            print(f"    {STOCK_NAMES.get(code, code)}: {ret:+.1f}%")
    
    if not stock_data:
        print("错误: 无法获取数据")
        return
    
    print("\n" + "-"*60)
    
    # 运行回测
    engine = BacktestEngine()
    result = engine.run(stock_data, sector_map)
    
    # 输出结果
    print("\n" + "="*60)
    print("  回测结果")
    print("="*60)
    print(f"  初始资金:     {result['initial']:>12,.0f} 元")
    print(f"  最终净值:     {result['final']:>12,.0f} 元")
    print(f"  总收益率:     {result['total_return']:>+11.1%}")
    print(f"  年化收益:     {result['annual_return']:>+11.1%}")
    print(f"  最大回撤:     {result['max_drawdown']:>11.1%}")
    print(f"  夏普比率:     {result['sharpe']:>12.2f}")
    print(f"  卡玛比率:     {result['calmar']:>12.2f}")
    print(f"  胜率:         {result['win_rate']:>11.1%}")
    print(f"  交易次数:     {result['trades']:>12}")
    print("="*60)
    
    annual_ok = "[OK]" if result['annual_return'] >= 0.30 else "[X]"
    dd_ok = "[OK]" if result['max_drawdown'] <= 0.05 else "[X]"
    
    print(f"\n  年化>=30%: {annual_ok}  实际: {result['annual_return']:+.1%}")
    print(f"  回撤<=5%:  {dd_ok}  实际: {result['max_drawdown']:.1%}")
    
    # 盈利交易
    if result['trades_list']:
        print("\n" + "-"*60)
        print("  盈利交易:")
        wins = [t for t in result['trades_list'] if t['action'] == 'sell' and t.get('pnl', 0) > 0]
        for t in wins[-8:]:
            name = STOCK_NAMES.get(t['code'], t['code'])
            print(f"  {t['date']} {name} | {t['strategy']} | {t['reason']} | +{t['pnl']:,.0f}")
    
    print("\n  (C) 2026 SimonsTang / 上海巧未来人工智能科技有限公司")


if __name__ == '__main__':
    main()
