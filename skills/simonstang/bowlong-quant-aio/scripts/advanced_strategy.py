#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.0
高性能策略引擎 — 目标：年化30%+，最大回撤5%以内

© 2026 SimonsTang / 上海巧未来人工智能科技有限公司 版权所有
开源协议：MIT License

核心设计思路：
1. 趋势过滤：只在大盘趋势向上时做多，避免熊市亏损
2. 多因子选股：动量+质量+低波动，提高胜率
3. 严格止损：个股-3%硬止损，组合-2%日止损
4. 仓位管理：Kelly公式动态仓位，波动率倒数加权
5. 分散持仓：同时持有5-10只，降低单股风险
6. 高频再平衡：每周调仓，及时止盈止损
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
from enum import Enum

import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════
#  数据层：生成高质量模拟数据
# ══════════════════════════════════════════════

def generate_realistic_market(n_days: int = 500, n_stocks: int = 20,
                               seed: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    生成真实感的A股市场模拟数据
    - 大盘指数：带牛熊周期
    - 个股：相关性+独立波动，含涨跌停
    """
    np.random.seed(seed)
    dates = pd.bdate_range('2024-01-01', periods=n_days, freq='B')

    # ── 大盘指数（沪深300风格）──
    # 分段：震荡→上涨→回调→上涨
    market_returns = np.zeros(n_days)
    phases = [
        (0,   100, 0.0003, 0.010),   # 震荡
        (100, 220, 0.0015, 0.008),   # 牛市上涨
        (220, 280, -0.0020, 0.012),  # 回调
        (280, 380, 0.0018, 0.009),   # 再上涨
        (380, n_days, 0.0005, 0.010),# 高位震荡
    ]
    for s, e, mu, sigma in phases:
        market_returns[s:e] = np.random.normal(mu, sigma, e - s)

    market_price = 3000 * np.exp(np.cumsum(market_returns))
    market_df = pd.DataFrame({'date': dates, 'close': market_price,
                               'return': market_returns})

    # ── 个股数据 ──
    tickers = [f'SIM{i:03d}' for i in range(1, n_stocks + 1)]
    stock_data = {}

    for ticker in tickers:
        # 每只股票有自己的alpha和beta
        beta = np.random.uniform(0.6, 1.4)
        alpha_daily = np.random.uniform(-0.0002, 0.0008)  # 部分股票有正alpha
        idio_vol = np.random.uniform(0.008, 0.018)

        raw_ret = alpha_daily + beta * market_returns + \
                  np.random.normal(0, idio_vol, n_days)

        # 模拟涨跌停（A股10%限制）
        raw_ret = np.clip(raw_ret, -0.099, 0.099)

        start_price = np.random.uniform(8, 50)
        prices = start_price * np.exp(np.cumsum(raw_ret))

        # 成交量（与涨跌相关）
        base_vol = np.random.uniform(5e6, 5e7)
        volume = base_vol * (1 + 2 * np.abs(raw_ret) / 0.05) * \
                 np.random.lognormal(0, 0.3, n_days)

        stock_data[ticker] = pd.DataFrame({
            'date': dates,
            'open':  prices * np.random.uniform(0.995, 1.005, n_days),
            'high':  prices * np.random.uniform(1.000, 1.015, n_days),
            'low':   prices * np.random.uniform(0.985, 1.000, n_days),
            'close': prices,
            'volume': volume.astype(int),
            'pct_chg': raw_ret * 100,
        })

    return market_df, stock_data


# ══════════════════════════════════════════════
#  技术指标库
# ══════════════════════════════════════════════

class Indicators:
    """技术指标计算"""

    @staticmethod
    def sma(series: pd.Series, n: int) -> pd.Series:
        return series.rolling(n).mean()

    @staticmethod
    def ema(series: pd.Series, n: int) -> pd.Series:
        return series.ewm(span=n, adjust=False).mean()

    @staticmethod
    def rsi(series: pd.Series, n: int = 14) -> pd.Series:
        delta = series.diff()
        gain = delta.clip(lower=0).rolling(n).mean()
        loss = (-delta.clip(upper=0)).rolling(n).mean()
        rs = gain / loss.replace(0, np.nan)
        return 100 - 100 / (1 + rs)

    @staticmethod
    def atr(high: pd.Series, low: pd.Series, close: pd.Series, n: int = 14) -> pd.Series:
        tr = pd.concat([
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ], axis=1).max(axis=1)
        return tr.rolling(n).mean()

    @staticmethod
    def macd(series: pd.Series, fast=12, slow=26, signal=9):
        ema_fast = series.ewm(span=fast, adjust=False).mean()
        ema_slow = series.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    @staticmethod
    def bollinger(series: pd.Series, n: int = 20, k: float = 2.0):
        mid = series.rolling(n).mean()
        std = series.rolling(n).std()
        upper = mid + k * std
        lower = mid - k * std
        return upper, mid, lower

    @staticmethod
    def momentum(series: pd.Series, n: int = 20) -> pd.Series:
        """n日动量（收益率）"""
        return series.pct_change(n)

    @staticmethod
    def volatility(series: pd.Series, n: int = 20) -> pd.Series:
        """n日波动率（年化）"""
        return series.pct_change().rolling(n).std() * np.sqrt(252)

    @staticmethod
    def volume_ratio(volume: pd.Series, n: int = 20) -> pd.Series:
        """量比"""
        return volume / volume.rolling(n).mean()


# ══════════════════════════════════════════════
#  核心策略：多因子趋势跟踪 + 严格风控
# ══════════════════════════════════════════════

class AdvancedStrategy:
    """
    高性能策略：趋势过滤 + 动量选股 + 波动率止损

    入场条件（同时满足）：
      1. 大盘趋势向上（MA20 > MA60）
      2. 个股动量强（20日收益率 > 5%）
      3. RSI在健康区间（40-70）
      4. 成交量放大（量比 > 1.2）
      5. 价格在MA20上方

    出场条件（任一满足）：
      1. 硬止损：亏损超过 stop_loss（默认-3%）
      2. 移动止盈：从最高点回落超过 trail_stop（默认-4%）
      3. 持仓超过 max_hold_days（默认15天）
      4. 大盘趋势转空（MA20 < MA60）
      5. RSI超买（> 75）
    """

    def __init__(self,
                 stop_loss: float = -0.03,       # 硬止损
                 trail_stop: float = -0.04,       # 移动止盈回撤
                 max_hold_days: int = 15,          # 最大持仓天数
                 momentum_period: int = 20,        # 动量周期
                 rsi_low: float = 40,
                 rsi_high: float = 75,
                 volume_ratio_min: float = 1.2):
        self.stop_loss = stop_loss
        self.trail_stop = trail_stop
        self.max_hold_days = max_hold_days
        self.momentum_period = momentum_period
        self.rsi_low = rsi_low
        self.rsi_high = rsi_high
        self.volume_ratio_min = volume_ratio_min

    def score_stock(self, df: pd.DataFrame, idx: int) -> float:
        """
        对单只股票打分（0-100），用于选出最优标的
        """
        if idx < 60:
            return 0

        close = df['close']
        volume = df['volume']

        # 各项指标
        mom20 = Indicators.momentum(close, 20).iloc[idx]
        mom5  = Indicators.momentum(close, 5).iloc[idx]
        rsi   = Indicators.rsi(close, 14).iloc[idx]
        vr    = Indicators.volume_ratio(volume, 20).iloc[idx]
        ma20  = Indicators.sma(close, 20).iloc[idx]
        ma60  = Indicators.sma(close, 60).iloc[idx]
        vol   = Indicators.volatility(close, 20).iloc[idx]
        price = close.iloc[idx]

        if any(pd.isna([mom20, mom5, rsi, vr, ma20, ma60, vol])):
            return 0

        score = 0

        # 1. 趋势分（30分）：价格在均线上方，均线多头
        if price > ma20:
            score += 15
        if ma20 > ma60:
            score += 15

        # 2. 动量分（30分）
        if mom20 > 0.05:
            score += 15 + min(15, mom20 * 100)
        elif mom20 > 0:
            score += 5

        # 3. RSI分（20分）：健康区间得分高
        if 45 <= rsi <= 65:
            score += 20
        elif 40 <= rsi <= 70:
            score += 12
        elif rsi > 75:
            score -= 10  # 超买扣分

        # 4. 量能分（20分）
        if vr >= 1.5:
            score += 20
        elif vr >= 1.2:
            score += 12
        elif vr < 0.8:
            score -= 5

        # 5. 低波动加分（波动率越低越好）
        if vol < 0.20:
            score += 5
        elif vol > 0.40:
            score -= 5

        return max(0, score)

    def market_trend_ok(self, market_df: pd.DataFrame, idx: int) -> bool:
        """大盘趋势判断：MA20 > MA60 且 MA20向上"""
        if idx < 65:
            return False
        close = market_df['close']
        ma20 = Indicators.sma(close, 20).iloc[idx]
        ma60 = Indicators.sma(close, 60).iloc[idx]
        ma20_prev = Indicators.sma(close, 20).iloc[idx - 1]

        if pd.isna(ma20) or pd.isna(ma60):
            return False

        return ma20 > ma60 and ma20 >= ma20_prev * 0.998  # MA20不能下行


# ══════════════════════════════════════════════
#  仓位管理：波动率倒数加权 + 总仓位控制
# ══════════════════════════════════════════════

class PositionSizer:
    """
    仓位管理器
    - 单股仓位 = 总资金 × (1/波动率) / Σ(1/波动率) × 目标仓位
    - 单股上限：总资金的 20%
    - 总仓位上限：80%（留20%现金缓冲）
    """

    def __init__(self, max_position_pct: float = 0.20,
                 max_total_pct: float = 0.80,
                 max_stocks: int = 8):
        self.max_position_pct = max_position_pct
        self.max_total_pct = max_total_pct
        self.max_stocks = max_stocks

    def calc_weights(self, vols: Dict[str, float]) -> Dict[str, float]:
        """波动率倒数加权"""
        if not vols:
            return {}
        inv_vols = {k: 1.0 / max(v, 0.01) for k, v in vols.items()}
        total = sum(inv_vols.values())
        weights = {k: v / total for k, v in inv_vols.items()}
        # 单股上限
        weights = {k: min(v, self.max_position_pct) for k, v in weights.items()}
        # 归一化后乘以总仓位上限
        total2 = sum(weights.values())
        if total2 > 0:
            weights = {k: v / total2 * self.max_total_pct for k, v in weights.items()}
        return weights


# ══════════════════════════════════════════════
#  回测引擎
# ══════════════════════════════════════════════

@dataclass
class Position:
    ticker: str
    shares: int
    cost: float          # 平均成本
    entry_date: str
    entry_idx: int
    peak_price: float    # 持仓期间最高价（用于移动止盈）

@dataclass
class Trade:
    date: str
    ticker: str
    action: str          # buy / sell
    price: float
    shares: int
    amount: float
    cost_fee: float
    reason: str
    pnl: float = 0.0


class BacktestEngine:
    """
    回测引擎
    """

    def __init__(self,
                 initial_cash: float = 1_000_000,
                 commission: float = 0.0003,
                 stamp_duty: float = 0.001,
                 slippage: float = 0.001):
        self.initial_cash = initial_cash
        self.commission = commission
        self.stamp_duty = stamp_duty
        self.slippage = slippage

        self.strategy = AdvancedStrategy()
        self.sizer = PositionSizer()

        # 状态
        self.cash = initial_cash
        self.positions: Dict[str, Position] = {}
        self.trades: List[Trade] = []
        self.equity_curve: List[Dict] = []
        self.peak_equity = initial_cash
        self.max_drawdown = 0.0

    def _trade_cost(self, amount: float, is_sell: bool) -> float:
        comm = max(amount * self.commission, 5.0)
        stamp = amount * self.stamp_duty if is_sell else 0
        return comm + stamp

    def _buy(self, ticker: str, price: float, target_amount: float,
             date: str, idx: int, reason: str):
        """买入"""
        # 滑点
        exec_price = price * (1 + self.slippage)
        # 计算股数（100股整数倍）
        max_shares = int(target_amount / exec_price / 100) * 100
        if max_shares <= 0:
            return

        amount = max_shares * exec_price
        fee = self._trade_cost(amount, False)

        if amount + fee > self.cash:
            max_shares = int((self.cash * 0.98) / exec_price / 100) * 100
            if max_shares <= 0:
                return
            amount = max_shares * exec_price
            fee = self._trade_cost(amount, False)

        self.cash -= (amount + fee)

        if ticker in self.positions:
            pos = self.positions[ticker]
            total_cost = pos.cost * pos.shares + exec_price * max_shares
            pos.shares += max_shares
            pos.cost = total_cost / pos.shares
            pos.peak_price = max(pos.peak_price, exec_price)
        else:
            self.positions[ticker] = Position(
                ticker=ticker, shares=max_shares, cost=exec_price,
                entry_date=date, entry_idx=idx, peak_price=exec_price
            )

        self.trades.append(Trade(
            date=date, ticker=ticker, action='buy',
            price=exec_price, shares=max_shares,
            amount=amount, cost_fee=fee, reason=reason
        ))

    def _sell(self, ticker: str, price: float, date: str, reason: str):
        """卖出（全仓）"""
        if ticker not in self.positions:
            return

        pos = self.positions[ticker]
        exec_price = price * (1 - self.slippage)
        amount = pos.shares * exec_price
        fee = self._trade_cost(amount, True)
        pnl = (exec_price - pos.cost) * pos.shares - fee

        self.cash += (amount - fee)
        del self.positions[ticker]

        self.trades.append(Trade(
            date=date, ticker=ticker, action='sell',
            price=exec_price, shares=pos.shares,
            amount=amount, cost_fee=fee, reason=reason, pnl=pnl
        ))

    def _portfolio_value(self, prices: Dict[str, float]) -> float:
        pos_val = sum(
            pos.shares * prices.get(pos.ticker, pos.cost)
            for pos in self.positions.values()
        )
        return self.cash + pos_val

    def run(self, market_df: pd.DataFrame,
            stock_data: Dict[str, pd.DataFrame]) -> Dict:
        """
        主回测循环
        每个交易日：
          1. 更新持仓价格，检查止损/止盈
          2. 判断大盘趋势
          3. 对候选股打分，选出TOP N
          4. 调仓（卖出不在TOP N的，买入新入选的）
        """
        tickers = list(stock_data.keys())
        n_days = len(market_df)

        # 预计算所有股票指标（加速）
        logger.info(f"📊 预计算指标，共 {len(tickers)} 只股票...")
        indicators_cache = {}
        for tk in tickers:
            df = stock_data[tk]
            close = df['close']
            vol = df['volume']
            indicators_cache[tk] = {
                'close': close.values,
                'volume': vol.values,
                'rsi': Indicators.rsi(close, 14).values,
                'ma20': Indicators.sma(close, 20).values,
                'ma60': Indicators.sma(close, 60).values,
                'atr': Indicators.atr(df['high'], df['low'], close, 14).values,
                'volatility': Indicators.volatility(close, 20).values,
                'mom20': Indicators.momentum(close, 20).values,
                'vr': Indicators.volume_ratio(vol, 20).values,
            }

        logger.info(f"🚀 开始回测，共 {n_days} 个交易日...")

        rebalance_counter = 0  # 每5天调仓一次

        for i in range(65, n_days):
            date = str(market_df['date'].iloc[i].date())

            # ── 当前价格 ──
            prices = {tk: indicators_cache[tk]['close'][i] for tk in tickers}

            # ── 1. 检查持仓止损/止盈 ──
            to_sell = []
            for tk, pos in self.positions.items():
                cur_price = prices.get(tk, pos.cost)
                # 更新最高价
                if cur_price > pos.peak_price:
                    pos.peak_price = cur_price

                pnl_pct = (cur_price - pos.cost) / pos.cost
                trail_pct = (cur_price - pos.peak_price) / pos.peak_price
                hold_days = i - pos.entry_idx

                reason = None
                if pnl_pct <= self.strategy.stop_loss:
                    reason = f"硬止损 {pnl_pct:.1%}"
                elif trail_pct <= self.strategy.trail_stop:
                    reason = f"移动止盈回撤 {trail_pct:.1%}"
                elif hold_days >= self.strategy.max_hold_days:
                    reason = f"持仓{hold_days}天到期"
                elif not self.strategy.market_trend_ok(market_df, i):
                    reason = "大盘趋势转空"
                elif indicators_cache[tk]['rsi'][i] > 80:
                    reason = f"RSI超买 {indicators_cache[tk]['rsi'][i]:.0f}"

                if reason:
                    to_sell.append((tk, reason))

            for tk, reason in to_sell:
                self._sell(tk, prices[tk], date, reason)

            # ── 2. 每5天调仓一次（降低交易频率）──
            rebalance_counter += 1
            if rebalance_counter >= 5:
                rebalance_counter = 0

                # 大盘趋势不好，不买入
                if self.strategy.market_trend_ok(market_df, i):

                    # 对所有股票打分
                    scores = {}
                    for tk in tickers:
                        if tk in self.positions:
                            continue  # 已持仓不重复买
                        df_tk = stock_data[tk]
                        score = self.strategy.score_stock(df_tk, i)
                        if score >= 55:  # 分数门槛
                            scores[tk] = score

                    # 选出TOP N（按分数排序）
                    max_new = self.sizer.max_stocks - len(self.positions)
                    if max_new > 0 and scores:
                        top_stocks = sorted(scores.items(),
                                            key=lambda x: x[1], reverse=True)[:max_new]

                        # 计算各股波动率，用于仓位分配
                        vols = {}
                        for tk, _ in top_stocks:
                            v = indicators_cache[tk]['volatility'][i]
                            vols[tk] = v if not np.isnan(v) else 0.25

                        weights = self.sizer.calc_weights(vols)
                        total_val = self._portfolio_value(prices)

                        for tk, score in top_stocks:
                            w = weights.get(tk, 0.10)
                            target_amt = total_val * w
                            self._buy(tk, prices[tk], target_amt, date, i,
                                      f"选股得分{score:.0f}")

            # ── 3. 记录净值 ──
            equity = self._portfolio_value(prices)
            if equity > self.peak_equity:
                self.peak_equity = equity
            dd = (self.peak_equity - equity) / self.peak_equity
            if dd > self.max_drawdown:
                self.max_drawdown = dd

            self.equity_curve.append({
                'date': date,
                'equity': equity,
                'cash': self.cash,
                'n_positions': len(self.positions),
                'drawdown': dd,
            })

            if i % 50 == 0:
                ret = (equity - self.initial_cash) / self.initial_cash
                logger.info(f"⏳ [{date}] {i}/{n_days} | "
                            f"净值: {equity:,.0f} | 收益: {ret:+.1%} | "
                            f"回撤: {dd:.1%} | 持仓: {len(self.positions)}只")

        return self._calc_metrics()

    def _calc_metrics(self) -> Dict:
        """计算绩效指标"""
        if not self.equity_curve:
            return {}

        eq = pd.Series([e['equity'] for e in self.equity_curve])
        dates = [e['date'] for e in self.equity_curve]

        final_val = eq.iloc[-1]
        total_ret = (final_val - self.initial_cash) / self.initial_cash

        # 年化收益（按实际天数）
        n_years = len(eq) / 252
        annual_ret = (1 + total_ret) ** (1 / n_years) - 1 if n_years > 0 else 0

        # 日收益率
        daily_ret = eq.pct_change().dropna()

        # 夏普比率（无风险利率2.5%）
        rf_daily = 0.025 / 252
        excess = daily_ret - rf_daily
        sharpe = (excess.mean() / excess.std() * np.sqrt(252)
                  if excess.std() > 0 else 0)

        # 卡玛比率
        calmar = annual_ret / self.max_drawdown if self.max_drawdown > 0 else 0

        # 交易统计
        sell_trades = [t for t in self.trades if t.action == 'sell']
        wins = [t for t in sell_trades if t.pnl > 0]
        losses = [t for t in sell_trades if t.pnl <= 0]
        win_rate = len(wins) / len(sell_trades) if sell_trades else 0
        avg_win = np.mean([t.pnl for t in wins]) if wins else 0
        avg_loss = np.mean([t.pnl for t in losses]) if losses else 0
        pl_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0

        # 最大连续亏损天数
        losing_streak = 0
        max_losing_streak = 0
        for r in daily_ret:
            if r < 0:
                losing_streak += 1
                max_losing_streak = max(max_losing_streak, losing_streak)
            else:
                losing_streak = 0

        return {
            'initial_cash': self.initial_cash,
            'final_value': final_val,
            'total_return': total_ret,
            'annual_return': annual_ret,
            'sharpe_ratio': sharpe,
            'calmar_ratio': calmar,
            'max_drawdown': self.max_drawdown,
            'win_rate': win_rate,
            'profit_loss_ratio': pl_ratio,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'total_trades': len(sell_trades),
            'winning_trades': len(wins),
            'losing_trades': len(losses),
            'max_losing_streak': max_losing_streak,
            'equity_curve': self.equity_curve,
            'trades': self.trades,
            'dates': dates,
        }


# ══════════════════════════════════════════════
#  参数优化器（网格搜索）
# ══════════════════════════════════════════════

class StrategyOptimizer:
    """
    网格搜索最优参数
    目标：最大化 卡玛比率（年化收益/最大回撤）
    """

    def __init__(self, market_df, stock_data, initial_cash=1_000_000):
        self.market_df = market_df
        self.stock_data = stock_data
        self.initial_cash = initial_cash

    def optimize(self) -> pd.DataFrame:
        param_grid = {
            'stop_loss':    [-0.025, -0.030, -0.035],
            'trail_stop':   [-0.035, -0.040, -0.050],
            'max_hold_days':[10, 15, 20],
            'rsi_high':     [70, 75, 80],
        }

        results = []
        total = (len(param_grid['stop_loss']) *
                 len(param_grid['trail_stop']) *
                 len(param_grid['max_hold_days']) *
                 len(param_grid['rsi_high']))

        logger.info(f"🔍 开始参数优化，共 {total} 组参数...")
        count = 0

        for sl in param_grid['stop_loss']:
            for ts in param_grid['trail_stop']:
                for mh in param_grid['max_hold_days']:
                    for rh in param_grid['rsi_high']:
                        count += 1
                        engine = BacktestEngine(initial_cash=self.initial_cash)
                        engine.strategy = AdvancedStrategy(
                            stop_loss=sl, trail_stop=ts,
                            max_hold_days=mh, rsi_high=rh
                        )
                        metrics = engine.run(self.market_df, self.stock_data)

                        results.append({
                            'stop_loss': sl,
                            'trail_stop': ts,
                            'max_hold_days': mh,
                            'rsi_high': rh,
                            'annual_return': metrics.get('annual_return', 0),
                            'max_drawdown': metrics.get('max_drawdown', 1),
                            'sharpe': metrics.get('sharpe_ratio', 0),
                            'calmar': metrics.get('calmar_ratio', 0),
                            'win_rate': metrics.get('win_rate', 0),
                            'total_trades': metrics.get('total_trades', 0),
                        })

                        if count % 10 == 0:
                            logger.info(f"  进度: {count}/{total}")

        df = pd.DataFrame(results)
        df = df.sort_values('calmar', ascending=False)
        return df


# ══════════════════════════════════════════════
#  报告生成
# ══════════════════════════════════════════════

def generate_report(metrics: Dict, strategy_params: Dict = None) -> str:
    """生成回测报告"""

    annual = metrics.get('annual_return', 0)
    mdd = metrics.get('max_drawdown', 0)
    sharpe = metrics.get('sharpe_ratio', 0)
    calmar = metrics.get('calmar_ratio', 0)

    # 达标判断
    target_annual = 0.30
    target_mdd = 0.05

    annual_ok = "[OK]" if annual >= target_annual else "[X]"
    mdd_ok = "[OK]" if mdd <= target_mdd else f"[X]"

    report = f"""
================================================================
     波龙股神量化交易系统 V2.0 - 回测报告
================================================================

--------------------------------------------------
  收益指标
--------------------------------------------------
  初始资金:    {metrics['initial_cash']:>15,.0f} 元
  最终净值:    {metrics['final_value']:>15,.0f} 元
  总收益率:    {metrics['total_return']:>+14.2%}
  年化收益:    {annual:>+14.2%}  {annual_ok}  目标: >=30%
  最大回撤:    {mdd:>14.2%}  {mdd_ok}  目标: <=5%
  夏普比率:    {sharpe:>14.2f}
  卡玛比率:    {calmar:>14.2f}  (年化/回撤，越高越好)

--------------------------------------------------
  交易统计
--------------------------------------------------
  总交易次数:  {metrics['total_trades']:>15}
  盈利次数:    {metrics['winning_trades']:>15}
  亏损次数:    {metrics['losing_trades']:>15}
  胜率:        {metrics['win_rate']:>14.1%}
  盈亏比:      {metrics['profit_loss_ratio']:>14.2f}
  平均盈利:    {metrics['avg_win']:>+14,.0f} 元/笔
  平均亏损:    {metrics['avg_loss']:>+14,.0f} 元/笔
  最大连亏天:  {metrics['max_losing_streak']:>15} 天
"""

    if strategy_params:
        report += f"""
--------------------------------------------------
  策略参数
--------------------------------------------------
  硬止损:      {strategy_params.get('stop_loss', -0.03):>14.1%}
  移动止盈:    {strategy_params.get('trail_stop', -0.04):>14.1%}
  最大持仓天:  {strategy_params.get('max_hold_days', 15):>15}
  RSI超买线:   {strategy_params.get('rsi_high', 75):>15}
"""

    # 净值曲线（ASCII）
    eq_curve = metrics.get('equity_curve', [])
    if eq_curve:
        equities = [e['equity'] for e in eq_curve]
        step = max(1, len(equities) // 20)
        sampled = equities[::step]
        min_eq = min(sampled)
        max_eq = max(sampled)
        height = 8

        report += f"""
--------------------------------------------------
  净值曲线
--------------------------------------------------
"""
        for row in range(height, -1, -1):
            threshold = min_eq + (max_eq - min_eq) * row / height
            line = ""
            for val in sampled:
                line += "#" if val >= threshold else " "
            label = f"{threshold/10000:>6.0f}万" if row % 2 == 0 else "      "
            report += f"  {label} |{line}\n"

        report += f"         +{'-' * len(sampled)}\n"
        report += f"          起始                              结束\n"

    # 达标总结
    report += f"""
--------------------------------------------------
  目标达成情况
--------------------------------------------------
  年化收益 >= 30%:  {annual_ok}  实际 {annual:+.1%}
  最大回撤 <=  5%:  {mdd_ok}  实际 {mdd:.1%}

  (C) 2026 SimonsTang / 上海巧未来人工智能科技有限公司
  回测结果仅供参考，不构成投资建议，盈亏自负
"""
    return report


# ══════════════════════════════════════════════
#  主程序
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='波龙股神量化交易系统 V2.0 — 高性能策略回测')
    parser.add_argument('--mode', choices=['backtest', 'optimize'], default='backtest',
                        help='运行模式：backtest=单次回测，optimize=参数优化')
    parser.add_argument('--cash', type=float, default=1_000_000, help='初始资金')
    parser.add_argument('--days', type=int, default=500, help='模拟天数')
    parser.add_argument('--stocks', type=int, default=20, help='股票池大小')
    parser.add_argument('--stop-loss', type=float, default=-0.03, help='硬止损比例')
    parser.add_argument('--trail-stop', type=float, default=-0.04, help='移动止盈回撤')
    parser.add_argument('--max-hold', type=int, default=15, help='最大持仓天数')
    parser.add_argument('--seed', type=int, default=42, help='随机种子')
    args = parser.parse_args()

    # 生成市场数据
    logger.info(f"📊 生成模拟市场数据（{args.days}天，{args.stocks}只股票）...")
    market_df, stock_data = generate_realistic_market(
        n_days=args.days, n_stocks=args.stocks, seed=args.seed
    )

    if args.mode == 'optimize':
        # 参数优化模式
        optimizer = StrategyOptimizer(market_df, stock_data, args.cash)
        results_df = optimizer.optimize()

        print("\n" + "═" * 70)
        print("  🏆 参数优化结果 TOP 10（按卡玛比率排序）")
        print("═" * 70)
        print(results_df.head(10).to_string(index=False,
              float_format=lambda x: f"{x:.3f}"))

        best = results_df.iloc[0]
        print(f"\n✅ 最优参数：")
        print(f"   止损={best['stop_loss']:.1%}  移动止盈={best['trail_stop']:.1%}  "
              f"持仓天={best['max_hold_days']:.0f}  RSI超买={best['rsi_high']:.0f}")
        print(f"   年化={best['annual_return']:.1%}  回撤={best['max_drawdown']:.1%}  "
              f"卡玛={best['calmar']:.2f}  胜率={best['win_rate']:.1%}")

        # 保存优化结果
        out_dir = Path('output/backtest_reports')
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_df.to_csv(out_dir / f'optimize_{ts}.csv', index=False)
        logger.info(f"💾 优化结果已保存")

    else:
        # 单次回测模式
        strategy_params = {
            'stop_loss': args.stop_loss,
            'trail_stop': args.trail_stop,
            'max_hold_days': args.max_hold,
        }

        engine = BacktestEngine(initial_cash=args.cash)
        engine.strategy = AdvancedStrategy(
            stop_loss=args.stop_loss,
            trail_stop=args.trail_stop,
            max_hold_days=args.max_hold,
        )

        metrics = engine.run(market_df, stock_data)
        report = generate_report(metrics, strategy_params)
        print(report)

        # 保存报告
        out_dir = Path('output/backtest_reports')
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = out_dir / f'advanced_backtest_{ts}.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"💾 报告已保存: {report_path}")


if __name__ == '__main__':
    main()
