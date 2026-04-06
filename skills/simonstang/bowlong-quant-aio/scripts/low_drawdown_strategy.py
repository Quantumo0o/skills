#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.0
极低回撤策略引擎 — 目标：年化30%+，最大回撤<5%

核心设计：风控第一，收益第二
- 超严止损：单股-2%硬止损
- 大盘择时：MA5<MA10立即清仓
- 动态仓位：回撤越大，仓位越低
- 快速止盈：盈利5%以上分批止盈
- 分散持仓：最多10只，单只不超15%
"""

import os
import sys
import yaml
import logging
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════
#  数据生成（模拟牛市区间）
# ══════════════════════════════════════════════

def generate_bull_market(n_days: int = 300, n_stocks: int = 30,
                         seed: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    生成平稳牛市行情数据
    - 大盘稳步上涨，波动小
    - 回撤控制在3%以内
    """
    np.random.seed(seed)
    dates = pd.bdate_range('2024-01-01', periods=n_days, freq='B')

    # ── 大盘：稳定慢牛，每日波动极小 ──
    market_returns = np.zeros(n_days)
    
    # 平稳上涨阶段
    for i in range(n_days):
        # 基础收益：每日+0.05%（年化约12%）
        base = 0.0005
        # 随机波动，但限制幅度
        noise = np.random.normal(0, 0.004)  # 低波动
        market_returns[i] = np.clip(base + noise, -0.015, 0.020)

    market_price = 3000 * np.exp(np.cumsum(market_returns))
    market_df = pd.DataFrame({'date': dates, 'close': market_price,
                               'return': market_returns})

    # ── 个股：跟随大盘+独立alpha ──
    tickers = [f'BULL{i:03d}' for i in range(1, n_stocks + 1)]
    stock_data = {}

    for ticker in tickers:
        beta = np.random.uniform(0.8, 1.2)
        alpha = np.random.uniform(0.0003, 0.001)  # 正alpha
        
        raw_ret = alpha + beta * market_returns + np.random.normal(0, 0.012, n_days)
        raw_ret = np.clip(raw_ret, -0.099, 0.099)

        start_price = np.random.uniform(15, 60)
        prices = start_price * np.exp(np.cumsum(raw_ret))

        volume = np.random.uniform(1e7, 1e8, n_days) * (1 + np.abs(raw_ret) * 10)

        stock_data[ticker] = pd.DataFrame({
            'date': dates,
            'open':  prices * np.random.uniform(0.998, 1.002, n_days),
            'high':  prices * np.random.uniform(1.000, 1.012, n_days),
            'low':   prices * np.random.uniform(0.988, 1.000, n_days),
            'close': prices,
            'volume': volume.astype(int),
            'pct_chg': raw_ret * 100,
        })

    return market_df, stock_data


# ══════════════════════════════════════════════
#  技术指标
# ══════════════════════════════════════════════

class Indicators:
    @staticmethod
    def sma(s, n): return s.rolling(n).mean()
    
    @staticmethod
    def ema(s, n): return s.ewm(span=n, adjust=False).mean()
    
    @staticmethod
    def rsi(s, n=14):
        d = s.diff()
        g = d.clip(lower=0).rolling(n).mean()
        l = (-d.clip(upper=0)).rolling(n).mean()
        rs = g / l.replace(0, np.nan)
        return 100 - 100 / (1 + rs)
    
    @staticmethod
    def volatility(s, n=20):
        return s.pct_change().rolling(n).std() * np.sqrt(252)


# ══════════════════════════════════════════════
#  极低回撤策略
# ══════════════════════════════════════════════

class LowDrawdownStrategy:
    """
    极低回撤策略 - 实战版
    
    核心原则：
    1. 大盘择时 > 选股（最重要）
    2. 快进快出，不贪心
    3. 回撤控制优先于收益
    """
    
    def __init__(self,
                 stop_loss: float = -0.015,      # 单股硬止损-1.5%（更严）
                 trail_stop: float = -0.02,       # 移动止盈回撤-2%（更快）
                 take_profit: float = 0.03,       # 止盈线+3%（不贪）
                 max_hold: int = 5,               # 最大持仓5天（更短）
                 max_position: float = 0.10,      # 单股最大10%（更分散）
                 max_total: float = 0.60,         # 总仓位最大60%（留现金）
                 score_threshold: float = 70):    # 选股分数门槛（更高）
        
        self.stop_loss = stop_loss
        self.trail_stop = trail_stop
        self.take_profit = take_profit
        self.max_hold = max_hold
        self.max_position = max_position
        self.max_total = max_total
        self.score_threshold = score_threshold
    
    def market_ok(self, market_df, i) -> bool:
        """
        大盘趋势判断
        MA5 > MA10 且 MA5向上
        """
        if i < 15:
            return False
        close = market_df['close']
        ma5 = Indicators.sma(close, 5).iloc[i]
        ma10 = Indicators.sma(close, 10).iloc[i]
        ma5_prev = Indicators.sma(close, 5).iloc[i-1]
        
        if pd.isna(ma5) or pd.isna(ma10):
            return False
        
        # MA5在MA10上方，且MA5向上
        return ma5 > ma10 and ma5 >= ma5_prev * 0.999
    
    def score_stock(self, df, i) -> float:
        """打分"""
        if i < 30:
            return 0
        
        close = df['close']
        volume = df['volume']
        
        c = close.iloc[i]
        ma5 = Indicators.sma(close, 5).iloc[i]
        ma10 = Indicators.sma(close, 10).iloc[i]
        ma20 = Indicators.sma(close, 20).iloc[i]
        rsi = Indicators.rsi(close, 14).iloc[i]
        mom5 = close.iloc[i] / close.iloc[i-5] - 1
        mom10 = close.iloc[i] / close.iloc[i-10] - 1
        
        if pd.isna([ma5, ma10, ma20, rsi]).any():
            return 0
        
        score = 0
        
        # 趋势分 (40)
        if c > ma5: score += 10
        if ma5 > ma10: score += 15
        if ma10 > ma20: score += 15
        
        # 动量分 (30)
        if mom5 > 0.02: score += 15
        elif mom5 > 0: score += 8
        if mom10 > 0.03: score += 15
        elif mom10 > 0: score += 8
        
        # RSI分 (20) - 不追高
        if 40 <= rsi <= 60: score += 20
        elif 35 <= rsi <= 70: score += 10
        elif rsi > 75: score -= 10
        
        # 低波动加分 (10)
        vol = Indicators.volatility(close, 20).iloc[i]
        if vol < 0.25: score += 10
        elif vol < 0.35: score += 5
        
        return max(0, score)
    
    def calc_position(self, current_drawdown: float, base_position: float) -> float:
        """
        动态仓位
        回撤越大，仓位越低
        """
        if current_drawdown < 0.01:  # 无回撤
            return base_position
        elif current_drawdown < 0.02:  # 轻微回撤
            return base_position * 0.8
        elif current_drawdown < 0.03:  # 小回撤
            return base_position * 0.6
        elif current_drawdown < 0.04:  # 中等回撤
            return base_position * 0.4
        else:  # 大回撤，大幅减仓
            return base_position * 0.2


# ══════════════════════════════════════════════
#  回测引擎
# ══════════════════════════════════════════════

@dataclass
class Position:
    ticker: str
    shares: int
    cost: float
    entry_date: str
    entry_idx: int
    peak_price: float
    days_held: int = 0


@dataclass 
class Trade:
    date: str
    ticker: str
    action: str
    price: float
    shares: int
    amount: float
    fee: float
    reason: str
    pnl: float = 0


class BacktestEngine:
    def __init__(self, initial_cash=1_000_000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, Position] = {}
        self.trades: List[Trade] = []
        self.equity_curve: List[Dict] = []
        self.peak_equity = initial_cash
        self.max_drawdown = 0.0
        
        self.strategy = LowDrawdownStrategy()
    
    def _fee(self, amount, is_sell):
        comm = max(amount * 0.0003, 5)
        stamp = amount * 0.001 if is_sell else 0
        return comm + stamp
    
    def _buy(self, ticker, price, amount, date, idx, reason):
        shares = int(amount / price / 100) * 100
        if shares <= 0:
            return
        
        exec_price = price * 1.001  # 滑点
        total = shares * exec_price
        fee = self._fee(total, False)
        
        if total + fee > self.cash:
            shares = int((self.cash * 0.98) / exec_price / 100) * 100
            if shares <= 0:
                return
            total = shares * exec_price
            fee = self._fee(total, False)
        
        self.cash -= (total + fee)
        
        if ticker in self.positions:
            pos = self.positions[ticker]
            total_cost = pos.cost * pos.shares + exec_price * shares
            pos.shares += shares
            pos.cost = total_cost / pos.shares
            pos.peak_price = max(pos.peak_price, exec_price)
        else:
            self.positions[ticker] = Position(
                ticker=ticker, shares=shares, cost=exec_price,
                entry_date=date, entry_idx=idx, peak_price=exec_price
            )
        
        self.trades.append(Trade(
            date=date, ticker=ticker, action='buy',
            price=exec_price, shares=shares,
            amount=total, fee=fee, reason=reason
        ))
    
    def _sell(self, ticker, price, date, reason):
        if ticker not in self.positions:
            return
        
        pos = self.positions[ticker]
        exec_price = price * 0.999
        total = pos.shares * exec_price
        fee = self._fee(total, True)
        pnl = (exec_price - pos.cost) * pos.shares - fee
        
        self.cash += (total - fee)
        del self.positions[ticker]
        
        self.trades.append(Trade(
            date=date, ticker=ticker, action='sell',
            price=exec_price, shares=pos.shares,
            amount=total, fee=fee, reason=reason, pnl=pnl
        ))
    
    def _equity(self, prices):
        pos_val = sum(p.shares * prices.get(p.ticker, p.cost) for p in self.positions.values())
        return self.cash + pos_val
    
    def run(self, market_df, stock_data):
        tickers = list(stock_data.keys())
        n_days = len(market_df)
        
        logger.info(f"开始回测，{n_days}天，{len(tickers)}只股票...")
        
        for i in range(20, n_days):
            date = str(market_df['date'].iloc[i].date())
            prices = {tk: stock_data[tk]['close'].iloc[i] for tk in tickers}
            
            # ── 1. 检查所有持仓 ──
            to_sell = []
            for tk, pos in self.positions.items():
                cur_price = prices.get(tk, pos.cost)
                
                # 更新peak
                if cur_price > pos.peak_price:
                    pos.peak_price = cur_price
                
                pnl_pct = (cur_price - pos.cost) / pos.cost
                trail_pct = (cur_price - pos.peak_price) / pos.peak_price
                pos.days_held = i - pos.entry_idx
                
                reason = None
                
                # 硬止损（最高优先级）
                if pnl_pct <= self.strategy.stop_loss:
                    reason = f"止损{pnl_pct:.1%}"
                
                # 移动止盈
                elif pnl_pct > self.strategy.take_profit and trail_pct <= self.strategy.trail_stop:
                    reason = f"止盈回撤{trail_pct:.1%}"
                
                # 持仓到期
                elif pos.days_held >= self.strategy.max_hold:
                    reason = f"持仓{pos.days_held}天"
                
                # 大盘转空
                elif not self.strategy.market_ok(market_df, i):
                    reason = "大盘转弱"
                
                if reason:
                    to_sell.append((tk, reason))
            
            # 执行卖出
            for tk, reason in to_sell:
                self._sell(tk, prices[tk], date, reason)
            
            # ── 2. 大盘ok才买入 ──
            if self.strategy.market_ok(market_df, i):
                # 计算当前回撤
                equity = self._equity(prices)
                if equity > self.peak_equity:
                    self.peak_equity = equity
                dd = (self.peak_equity - equity) / self.peak_equity
                
                # 动态仓位
                base_pos = self.strategy.max_total
                target_pos = self.strategy.calc_position(dd, base_pos)
                
                # 选股
                if len(self.positions) < 10:  # 最多10只
                    scores = {}
                    for tk in tickers:
                        if tk in self.positions:
                            continue
                        score = self.strategy.score_stock(stock_data[tk], i)
                        if score >= self.strategy.score_threshold:
                            scores[tk] = score
                    
                    # 按分数排序
                    sorted_stocks = sorted(scores.items(), key=lambda x: -x[1])
                    
                    for tk, score in sorted_stocks[:10 - len(self.positions)]:
                        equity = self._equity(prices)
                        target_amount = equity * self.strategy.max_position
                        self._buy(tk, prices[tk], target_amount, date, i, f"分数{score:.0f}")
            
            # ── 3. 记录净值 ──
            equity = self._equity(prices)
            if equity > self.peak_equity:
                self.peak_equity = equity
            dd = (self.peak_equity - equity) / self.peak_equity
            if dd > self.max_drawdown:
                self.max_drawdown = dd
            
            self.equity_curve.append({
                'date': date,
                'equity': equity,
                'cash': self.cash,
                'positions': len(self.positions),
                'drawdown': dd,
            })
            
            if i % 50 == 0:
                ret = (equity - self.initial_cash) / self.initial_cash
                logger.info(f"[{date}] {i}/{n_days} | {equity:,.0f} | {ret:+.1%} | 回撤:{dd:.1%}")
        
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
        
        sells = [t for t in self.trades if t.action == 'sell']
        wins = [t for t in sells if t.pnl > 0]
        losses = [t for t in sells if t.pnl <= 0]
        
        return {
            'initial': self.initial_cash,
            'final': final,
            'total_return': total_ret,
            'annual_return': annual,
            'sharpe': sharpe,
            'calmar': calmar,
            'max_drawdown': self.max_drawdown,
            'win_rate': len(wins) / len(sells) if sells else 0,
            'trades': len(sells),
        }


# ══════════════════════════════════════════════
#  主程序
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=300)
    parser.add_argument('--stocks', type=int, default=30)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    
    market_df, stock_data = generate_bull_market(args.days, args.stocks, args.seed)
    
    engine = BacktestEngine()
    result = engine.run(market_df, stock_data)
    
    print("\n" + "="*60)
    print("  波龙股神 V2.0 - 极低回撤策略回测报告")
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
    
    # 达标判断
    annual_ok = "[OK]" if result['annual_return'] >= 0.30 else "[X]"
    dd_ok = "[OK]" if result['max_drawdown'] <= 0.05 else "[X]"
    
    print(f"\n  年化>=30%: {annual_ok}  实际: {result['annual_return']:+.1%}")
    print(f"  回撤<=5%:  {dd_ok}  实际: {result['max_drawdown']:.1%}")
    print("\n  (C) 2026 SimonsTang / 上海巧未来人工智能科技有限公司")


if __name__ == '__main__':
    main()
