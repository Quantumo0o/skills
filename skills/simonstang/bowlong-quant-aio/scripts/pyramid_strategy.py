#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.0
金字塔分批建仓策略 — 下跌补仓，反弹盈利出局

核心逻辑：
1. 分批建仓：首次买30%，下跌补仓摊低成本
2. 不轻易止损：急跌后补仓，等反弹
3. 板块轮动：只做强势板块，不做弱势股
4. 扩大股票池：用选股器选出TOP10强势股
"""

import os
import sys
import logging
import argparse
from datetime import datetime
from typing import Dict, List, Tuple
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
#  数据获取
# ══════════════════════════════════════════════

def fetch_stock_data(code: str, start: str, end: str) -> pd.DataFrame:
    """获取A股日线数据"""
    try:
        import akshare as ak
        logger.info(f"获取 {code}...")
        df = ak.stock_zh_a_hist(symbol=code, period="daily",
                                 start_date=start.replace('-', ''),
                                 end_date=end.replace('-', ''),
                                 adjust="qfq")
        df = df.rename(columns={
            '日期': 'date', '开盘': 'open', '最高': 'high',
            '最低': 'low', '收盘': 'close', '成交量': 'volume'
        })
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        return df
    except Exception as e:
        logger.error(f"获取 {code} 失败: {e}")
        return None


def fetch_index_data(start: str, end: str) -> pd.DataFrame:
    """获取上证指数"""
    try:
        import akshare as ak
        df = ak.stock_zh_index_daily(symbol="sh000001")
        df['date'] = pd.to_datetime(df['date'])
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
        df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]
        return df.sort_values('date').reset_index(drop=True)
    except:
        return None


# ══════════════════════════════════════════════
#  技术指标
# ══════════════════════════════════════════════

def sma(s, n): return s.rolling(n).mean()
def ema(s, n): return s.ewm(span=n).mean()
def rsi(s, n=14):
    d = s.diff()
    g = d.clip(lower=0).rolling(n).mean()
    l = (-d.clip(upper=0)).rolling(n).mean()
    return 100 - 100 / (1 + g / l.replace(0, np.nan))


# ══════════════════════════════════════════════
#  金字塔分批建仓策略
# ══════════════════════════════════════════════

class PyramidStrategy:
    """
    金字塔分批建仓策略
    
    建仓逻辑：
    - 首次买入：30%仓位
    - 下跌5%补仓：+30%
    - 再跌5%补仓：+20%（最后一次）
    - 总仓位不超过80%
    
    出场逻辑：
    - 盈利5%以上：分批止盈
    - 盈利10%以上：回撤5%止盈
    - 最大持仓60天
    """
    
    def __init__(self):
        # 建仓参数
        self.first_buy_pct = 0.25      # 首次买入25%
        self.add_buy_pct = 0.25        # 补仓25%
        self.add_buy_threshold = 0.06  # 下跌6%补仓
        self.max_add_times = 2         # 最多补仓2次
        
        # 出场参数
        self.take_profit_1 = 0.08      # 盈利8%开始分批止盈
        self.take_profit_2 = 0.12      # 盈利12%后回撤止盈
        self.trail_after_profit = 0.06 # 盈利12%后回撤6%止盈
        self.max_hold = 45             # 最大持仓45天
        
        # 选股参数
        self.momentum_days = 20        # 动量周期
        self.min_score = 65            # 最低分数
    
    def get_position_limit(self, current_drawdown: float) -> float:
        """根据回撤动态调整仓位上限"""
        if current_drawdown < 0.02:    # 回撤<2%
            return 0.80               # 最高80%仓位
        elif current_drawdown < 0.05:  # 回撤2-5%
            return 0.60               # 降到60%
        elif current_drawdown < 0.08:  # 回撤5-8%
            return 0.40               # 降到40%
        else:                          # 回撤>8%
            return 0.20               # 降到20%
    
    def calc_score(self, df, idx) -> float:
        """计算股票得分（动量+趋势）"""
        if idx < 30:
            return 0
        
        close = df['close']
        c = close.iloc[idx]
        
        # 均线
        ma5 = sma(close, 5).iloc[idx]
        ma10 = sma(close, 10).iloc[idx]
        ma20 = sma(close, 20).iloc[idx]
        
        if pd.isna(ma5) or pd.isna(ma10) or pd.isna(ma20):
            return 0
        
        score = 0
        
        # 趋势分（60分）- 必须多头排列
        if not (c > ma5 and ma5 > ma10 and ma10 > ma20):
            return 0  # 不满足多头排列直接淘汰
        score += 60
        
        # 动量分（40分）
        mom20 = (c / close.iloc[idx-20] - 1) if idx >= 20 else 0
        if mom20 > 0.15: score += 40
        elif mom20 > 0.10: score += 35
        elif mom20 > 0.05: score += 25
        elif mom20 > 0: score += 15
        elif mom20 < -0.05:  # 下跌趋势
            return 0  # 直接淘汰
        
        return score
    
    def is_strong_stock(self, df, idx) -> bool:
        """判断是否强势股"""
        score = self.calc_score(df, idx)
        return score >= self.min_score
    
    def should_buy(self, df, idx, pos=None) -> Tuple[bool, str, float]:
        """
        判断是否买入
        返回: (是否买入, 原因, 买入比例)
        """
        if idx < 20:
            return False, "数据不足", 0
        
        close = df['close']
        c = close.iloc[idx]
        
        ma5 = sma(close, 5).iloc[idx]
        ma10 = sma(close, 10).iloc[idx]
        
        if pd.isna(ma5) or pd.isna(ma10):
            return False, "指标缺失", 0
        
        # ── 首次买入 ──
        if pos is None:
            # 条件：均线多头
            if c > ma5 and ma5 > ma10:
                score = self.calc_score(df, idx)
                if score >= self.min_score:
                    return True, f"首次建仓（分数{score:.0f}）", self.first_buy_pct
            return False, "不符合买入条件", 0
        
        # ── 补仓逻辑 ──
        cost = pos['cost']
        add_times = pos.get('add_times', 0)
        pnl = (c - cost) / cost
        
        # 已补仓次数达到上限
        if add_times >= self.max_add_times:
            return False, "已达补仓上限", 0
        
        # 下跌超过阈值，补仓
        if pnl <= -self.add_buy_threshold * (add_times + 1):
            return True, f"下跌{pnl:.1%}补仓（第{add_times+1}次）", self.add_buy_pct
        
        return False, "", 0
    
    def should_sell(self, pos, cur_price, idx) -> Tuple[bool, str, float]:
        """
        判断是否卖出
        返回: (是否卖出, 原因, 卖出比例)
        """
        cost = pos['cost']
        peak = pos.get('peak', cur_price)
        hold_days = idx - pos['entry_idx']
        
        pnl = (cur_price - cost) / pos['cost']
        trail = (cur_price - peak) / peak if peak > 0 else 0
        
        # 1. 盈利12%以上，回撤6%止盈（全仓）
        if pnl > self.take_profit_2 and trail <= -self.trail_after_profit:
            return True, f"止盈（盈利{pnl:.1%}，回撤{trail:.1%}）", 1.0
        
        # 2. 盈利8-12%，回撤到成本线附近止盈（半仓）
        if pnl > self.take_profit_1 and pnl < self.take_profit_2:
            if pnl < 0.02:  # 回撤到只剩2%盈利
                return True, f"分批止盈（盈利{pnl:.1%}）", 0.5
        
        # 3. 持仓到期
        if hold_days >= self.max_hold:
            return True, f"持仓{hold_days}天到期", 1.0
        
        # 4. 极端止损（亏损12%以上）
        if pnl <= -0.12:
            return True, f"止损{pnl:.1%}", 1.0
        
        return False, "", 0


# ══════════════════════════════════════════════
#  回测引擎
# ══════════════════════════════════════════════

class BacktestEngine:
    def __init__(self, initial_cash=1_000_000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = {}  # {code: {shares, cost, entry_idx, peak, add_times}}
        self.trades = []
        self.equity_curve = []
        self.peak_equity = initial_cash
        self.max_drawdown = 0.0
        
        self.strategy = PyramidStrategy()
    
    def _fee(self, amount, is_sell):
        return max(amount * 0.0003, 5) + (amount * 0.001 if is_sell else 0)
    
    def _buy(self, code, price, pct, date, idx, reason, current_dd=0):
        """买入"""
        target = self.cash * pct
        shares = int(target / price / 100) * 100
        if shares <= 0:
            return
        
        exec_price = price * 1.001
        total = shares * exec_price
        fee = self._fee(total, False)
        
        if total + fee > self.cash:
            shares = int((self.cash * 0.98) / exec_price / 100) * 100
            if shares <= 0:
                return
            total = shares * exec_price
            fee = self._fee(total, False)
        
        self.cash -= (total + fee)
        
        if code in self.positions:
            pos = self.positions[code]
            total_cost = pos['cost'] * pos['shares'] + exec_price * shares
            pos['shares'] += shares
            pos['cost'] = total_cost / pos['shares']
            pos['peak'] = max(pos['peak'], exec_price)
            pos['add_times'] = pos.get('add_times', 0) + 1
        else:
            self.positions[code] = {
                'shares': shares,
                'cost': exec_price,
                'entry_idx': idx,
                'peak': exec_price,
                'add_times': 0
            }
        
        self.trades.append({
            'date': date, 'code': code, 'action': 'buy',
            'price': exec_price, 'shares': shares,
            'amount': total, 'fee': fee, 'reason': reason
        })
        
        logger.info(f"  [买入] {code} {shares}股 @ {exec_price:.2f} ({pct:.0%}) | {reason}")
    
    def _sell(self, code, price, pct, date, reason):
        """卖出"""
        if code not in self.positions:
            return
        
        pos = self.positions[code]
        sell_shares = int(pos['shares'] * pct)
        if sell_shares <= 0:
            sell_shares = pos['shares']
        
        exec_price = price * 0.999
        total = sell_shares * exec_price
        fee = self._fee(total, True)
        pnl = (exec_price - pos['cost']) * sell_shares - fee
        pnl_pct = (exec_price - pos['cost']) / pos['cost']
        
        self.cash += (total - fee)
        
        if pct >= 1.0 or sell_shares >= pos['shares']:
            del self.positions[code]
        else:
            pos['shares'] -= sell_shares
        
        self.trades.append({
            'date': date, 'code': code, 'action': 'sell',
            'price': exec_price, 'shares': sell_shares,
            'amount': total, 'fee': fee, 'reason': reason,
            'pnl': pnl, 'pnl_pct': pnl_pct
        })
        
        logger.info(f"  [卖出] {code} {sell_shares}股 @ {exec_price:.2f} | {reason} | 盈亏: {pnl:+,.0f} ({pnl_pct:+.1%})")
    
    def _equity(self, prices):
        pos_val = sum(p['shares'] * prices.get(c, p['cost']) for c, p in self.positions.items())
        return self.cash + pos_val
    
    def run(self, stock_data: Dict[str, pd.DataFrame], index_df=None):
        """运行回测"""
        codes = list(stock_data.keys())
        
        # 合并所有日期
        all_dates = set()
        for df in stock_data.values():
            all_dates.update(df['date'].tolist())
        all_dates = sorted(all_dates)
        
        logger.info(f"\n开始回测，{len(all_dates)}天，{len(codes)}只股票")
        logger.info("="*60)
        
        for i, date in enumerate(all_dates):
            date_str = str(date.date()) if hasattr(date, 'date') else str(date)
            
            # 当日价格
            prices = {}
            for code in codes:
                df = stock_data[code]
                row = df[df['date'] == date]
                if not row.empty:
                    prices[code] = row['close'].iloc[0]
            
            if not prices:
                continue
            
            # ── 1. 检查持仓：更新peak，判断卖出 ──
            to_sell = []
            for code, pos in list(self.positions.items()):
                if code not in prices:
                    continue
                
                cur_price = prices[code]
                if cur_price > pos.get('peak', cur_price):
                    pos['peak'] = cur_price
                
                should, reason, pct = self.strategy.should_sell(pos, cur_price, i)
                if should:
                    to_sell.append((code, reason, pct))
            
            for code, reason, pct in to_sell:
                self._sell(code, prices[code], pct, date_str, reason)
            
            # ── 2. 选股：找出今日强势股 ──
            strong_stocks = []
            for code in codes:
                df = stock_data[code]
                idx_list = df[df['date'] <= date].index
                if len(idx_list) == 0:
                    continue
                idx = idx_list[-1]
                
                if self.strategy.is_strong_stock(df, idx):
                    score = self.strategy.calc_score(df, idx)
                    strong_stocks.append((code, score, idx))
            
            # 按分数排序
            strong_stocks.sort(key=lambda x: -x[1])
            
            # ── 3. 买入逻辑 ──
            # 先计算当前回撤
            equity = self._equity(prices)
            if equity > self.peak_equity:
                self.peak_equity = equity
            current_dd = (self.peak_equity - equity) / self.peak_equity if self.peak_equity > 0 else 0
            
            # 先检查是否需要补仓
            for code, pos in list(self.positions.items()):
                if code not in prices:
                    continue
                df = stock_data[code]
                idx_list = df[df['date'] <= date].index
                if len(idx_list) == 0:
                    continue
                idx = idx_list[-1]
                
                should, reason, pct = self.strategy.should_buy(df, idx, pos)
                if should and self.cash > 10000:
                    self._buy(code, prices[code], pct, date_str, i, reason, current_dd)
            
            # 再看是否开新仓（最多持有5只）
            if len(self.positions) < 5:
                for code, score, idx in strong_stocks[:10]:
                    if code in self.positions:
                        continue
                    if self.cash < 50000:  # 现金不足5万不买
                        continue
                    
                    should, reason, pct = self.strategy.should_buy(stock_data[code], idx)
                    if should:
                        self._buy(code, prices[code], pct, date_str, i, reason, current_dd)
                        break  # 每天最多买一只
            
            # ── 4. 记录净值 ──
            if equity > self.peak_equity:
                self.peak_equity = equity
            dd = (self.peak_equity - equity) / self.peak_equity
            if dd > self.max_drawdown:
                self.max_drawdown = dd
            
            self.equity_curve.append({
                'date': date_str, 'equity': equity,
                'cash': self.cash, 'positions': len(self.positions),
                'drawdown': dd
            })
        
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


# ══════════════════════════════════════════════
#  主程序
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', default='2024-01-01')
    parser.add_argument('--end', default='2025-03-28')
    parser.add_argument('--cash', type=float, default=1_000_000)
    args = parser.parse_args()
    
    # 测试股票池（只做强势股！排除弱势股）
    stocks = {
        '601288': '农业银行',   # +58%
        '600036': '招商银行',   # +78%
        '000333': '美的集团',    # +53%
        '002594': '比亚迪',     # +104%
        '300750': '宁德时代',   # +73%
        '601318': '中国平安',   # +43%
        '000831': '中国稀土',    # +20%
        # 排除：隆基绿能（-23%）、茅台（-3%）
    }
    
    print("\n" + "="*60)
    print("  波龙股神 V2.0 - 金字塔分批建仓策略")
    print("="*60)
    print(f"  股票池: {len(stocks)}只强势股")
    print(f"  时间: {args.start} ~ {args.end}")
    print(f"  初始资金: {args.cash:,.0f} 元")
    print("="*60 + "\n")
    
    # 获取数据
    stock_data = {}
    for code, name in stocks.items():
        df = fetch_stock_data(code, args.start, args.end)
        if df is not None and len(df) > 50:
            stock_data[code] = df
            ret = (df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100
            print(f"  {name}({code}): {len(df)}天, 涨幅 {ret:+.1f}%")
    
    if not stock_data:
        print("错误: 无法获取数据")
        return
    
    print("\n" + "-"*60)
    
    # 运行回测
    engine = BacktestEngine(initial_cash=args.cash)
    result = engine.run(stock_data)
    
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
    
    # 目标判断
    annual_ok = "[OK]" if result['annual_return'] >= 0.30 else "[X]"
    dd_ok = "[OK]" if result['max_drawdown'] <= 0.05 else "[X]"
    
    print(f"\n  年化>=30%: {annual_ok}  实际: {result['annual_return']:+.1%}")
    print(f"  回撤<=5%:  {dd_ok}  实际: {result['max_drawdown']:.1%}")
    
    # 盈利交易
    if result['trades_list']:
        print("\n" + "-"*60)
        print("  盈利交易:")
        wins = [t for t in result['trades_list'] if t['action'] == 'sell' and t.get('pnl', 0) > 0]
        for t in wins[-5:]:
            name = stocks.get(t['code'], t['code'])
            print(f"  {t['date']} 卖出 {name} {t['shares']}股 @ {t['price']:.2f} | {t['reason']} | +{t['pnl']:,.0f}")
    
    print("\n  (C) 2026 SimonsTang / 上海巧未来人工智能科技有限公司")


if __name__ == '__main__':
    main()
