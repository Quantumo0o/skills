#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.0
真实数据回测 — 使用 akshare 获取历史行情

测试股票：
- 农业银行 (601288)
- 中国稀土 (000831)
- 中国卫星 (600118)
"""

import os
import sys
import logging
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass

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
    """使用akshare获取A股日线数据"""
    try:
        import akshare as ak
        
        # akshare的股票代码格式
        logger.info(f"获取 {code} 数据...")
        
        # 使用 ak.stock_zh_a_hist 获取日线
        df = ak.stock_zh_a_hist(symbol=code, period="daily", 
                                 start_date=start.replace('-', ''), 
                                 end_date=end.replace('-', ''),
                                 adjust="qfq")  # 前复权
        
        if df is None or df.empty:
            logger.warning(f"无法获取 {code} 数据")
            return None
        
        # 重命名列
        df = df.rename(columns={
            '日期': 'date',
            '开盘': 'open',
            '最高': 'high',
            '最低': 'low',
            '收盘': 'close',
            '成交量': 'volume',
            '涨跌幅': 'pct_chg'
        })
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        
        logger.info(f"  获取到 {len(df)} 条记录 ({df['date'].min().date()} ~ {df['date'].max().date()})")
        
        return df
        
    except Exception as e:
        logger.error(f"获取 {code} 数据失败: {e}")
        return None


def fetch_index_data(start: str, end: str) -> pd.DataFrame:
    """获取上证指数作为大盘参考"""
    try:
        import akshare as ak
        
        logger.info("获取上证指数...")
        df = ak.stock_zh_index_daily(symbol="sh000001")
        
        df = df.rename(columns={'date': 'date', 'close': 'close'})
        df['date'] = pd.to_datetime(df['date'])
        
        # 筛选日期范围
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
        df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]
        df = df.sort_values('date').reset_index(drop=True)
        
        logger.info(f"  获取到 {len(df)} 条指数记录")
        
        return df
        
    except Exception as e:
        logger.error(f"获取指数失败: {e}")
        return None


# ══════════════════════════════════════════════
#  技术指标
# ══════════════════════════════════════════════

class Indicators:
    @staticmethod
    def sma(s, n): 
        return s.rolling(n).mean()
    
    @staticmethod
    def ema(s, n): 
        return s.ewm(span=n, adjust=False).mean()
    
    @staticmethod
    def rsi(s, n=14):
        d = s.diff()
        g = d.clip(lower=0).rolling(n).mean()
        l = (-d.clip(upper=0)).rolling(n).mean()
        rs = g / l.replace(0, np.nan)
        return 100 - 100 / (1 + rs)
    
    @staticmethod
    def macd(s, fast=12, slow=26, signal=9):
        ema_f = s.ewm(span=fast).mean()
        ema_s = s.ewm(span=slow).mean()
        dif = ema_f - ema_s
        dea = dif.ewm(span=signal).mean()
        return dif, dea, (dif - dea) * 2


# ══════════════════════════════════════════════
#  策略
# ══════════════════════════════════════════════

class Strategy:
    """趋势跟踪策略 - 让利润奔跑"""
    
    def __init__(self,
                 stop_loss=-0.08,       # 止损-8%（更宽）
                 trail_stop=-0.10,      # 移动止盈回撤-10%（让利润奔跑）
                 take_profit=0.15,      # 止盈+15%（不轻易止盈）
                 max_hold=60):          # 最大持仓60天（长期持有）
        
        self.stop_loss = stop_loss
        self.trail_stop = trail_stop
        self.take_profit = take_profit
        self.max_hold = max_hold
    
    def should_buy(self, df, idx, index_df=None) -> Tuple[bool, str]:
        """买入信号 - 趋势跟踪"""
        if idx < 20:
            return False, "数据不足"
        
        close = df['close']
        c = close.iloc[idx]
        c_prev = close.iloc[idx-1]
        
        ma5 = Indicators.sma(close, 5).iloc[idx]
        ma10 = Indicators.sma(close, 10).iloc[idx]
        ma20 = Indicators.sma(close, 20).iloc[idx]
        
        if pd.isna(ma5) or pd.isna(ma10) or pd.isna(ma20):
            return False, "指标缺失"
        
        reasons = []
        
        # 核心：均线多头排列 + 价格在均线上方
        if c > ma5 and ma5 > ma10:
            reasons.append("均线多头")
        else:
            return False, "均线空头发散"
        
        # 加分项
        if c > ma20:
            reasons.append("站稳MA20")
        
        # 突破信号
        if c > c_prev * 1.02:  # 当日涨幅>2%
            reasons.append("突破")
        
        return True, " + ".join(reasons) if reasons else "趋势向上"
    
    def should_sell(self, pos, cur_price, idx, index_df=None) -> Tuple[bool, str]:
        """卖出信号 - 让利润奔跑"""
        pnl = (cur_price - pos['cost']) / pos['cost']
        trail = (cur_price - pos['peak']) / pos['peak']
        hold_days = idx - pos['entry_idx']
        
        # 1. 硬止损（亏损8%才止损）
        if pnl <= self.stop_loss:
            return True, f"止损{pnl:.1%}"
        
        # 2. 移动止盈（盈利15%后，回撤10%才止盈）
        if pnl > self.take_profit and trail <= self.trail_stop:
            return True, f"止盈回撤{trail:.1%}（盈利{pnl:.1%})"
        
        # 3. 持仓到期
        if hold_days >= self.max_hold:
            return True, f"持仓{hold_days}天到期"
        
        return False, ""


# ══════════════════════════════════════════════
#  回测引擎
# ══════════════════════════════════════════════

class BacktestEngine:
    def __init__(self, initial_cash=1_000_000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = {}  # {code: {shares, cost, entry_idx, peak}}
        self.trades = []
        self.equity_curve = []
        self.peak_equity = initial_cash
        self.max_drawdown = 0.0
        
        self.strategy = Strategy()
    
    def _fee(self, amount, is_sell):
        comm = max(amount * 0.0003, 5)
        stamp = amount * 0.001 if is_sell else 0
        return comm + stamp
    
    def _buy(self, code, price, date, idx, reason, shares=None):
        if shares is None:
            # 默认买入资金的20%
            target = self.cash * 0.20
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
        else:
            self.positions[code] = {
                'shares': shares,
                'cost': exec_price,
                'entry_idx': idx,
                'peak': exec_price
            }
        
        self.trades.append({
            'date': date,
            'code': code,
            'action': 'buy',
            'price': exec_price,
            'shares': shares,
            'amount': total,
            'fee': fee,
            'reason': reason
        })
        
        logger.info(f"  [买入] {code} {shares}股 @ {exec_price:.2f} | {reason}")
    
    def _sell(self, code, price, date, reason):
        if code not in self.positions:
            return
        
        pos = self.positions[code]
        exec_price = price * 0.999
        total = pos['shares'] * exec_price
        fee = self._fee(total, True)
        pnl = (exec_price - pos['cost']) * pos['shares'] - fee
        pnl_pct = (exec_price - pos['cost']) / pos['cost']
        
        self.cash += (total - fee)
        del self.positions[code]
        
        self.trades.append({
            'date': date,
            'code': code,
            'action': 'sell',
            'price': exec_price,
            'shares': pos['shares'],
            'amount': total,
            'fee': fee,
            'reason': reason,
            'pnl': pnl,
            'pnl_pct': pnl_pct
        })
        
        logger.info(f"  [卖出] {code} {pos['shares']}股 @ {exec_price:.2f} | {reason} | 盈亏: {pnl:+,.0f} ({pnl_pct:+.1%})")
    
    def _equity(self, prices):
        pos_val = sum(p['shares'] * prices.get(c, p['cost']) for c, p in self.positions.items())
        return self.cash + pos_val
    
    def run(self, stock_data: Dict[str, pd.DataFrame], index_df: pd.DataFrame = None):
        """
        回测主循环
        stock_data: {code: DataFrame}
        """
        codes = list(stock_data.keys())
        
        # 找到所有日期的并集
        all_dates = set()
        for code, df in stock_data.items():
            all_dates.update(df['date'].tolist())
        
        if index_df is not None:
            all_dates.update(index_df['date'].tolist())
        
        all_dates = sorted(all_dates)
        n_days = len(all_dates)
        
        logger.info(f"\n开始回测，共 {n_days} 个交易日，{len(codes)} 只股票")
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
            
            # ── 1. 检查持仓 ──
            to_sell = []
            for code, pos in self.positions.items():
                if code not in prices:
                    continue
                
                cur_price = prices[code]
                
                # 更新peak
                if cur_price > pos['peak']:
                    pos['peak'] = cur_price
                
                should, reason = self.strategy.should_sell(pos, cur_price, i, index_df)
                if should:
                    to_sell.append((code, reason))
            
            for code, reason in to_sell:
                self._sell(code, prices[code], date_str, reason)
            
            # ── 2. 择时买入 ──
            if len(self.positions) < 5:  # 最多5只
                for code in codes:
                    if code in self.positions:
                        continue
                    if code not in prices:
                        continue
                    
                    df = stock_data[code]
                    idx_list = df[df['date'] <= date].index
                    if len(idx_list) == 0:
                        continue
                    idx = idx_list[-1]
                    
                    should, reason = self.strategy.should_buy(df, idx, index_df)
                    if should:
                        self._buy(code, prices[code], date_str, i, reason)
                        break  # 每天最多买一只
            
            # ── 3. 记录净值 ──
            equity = self._equity(prices)
            if equity > self.peak_equity:
                self.peak_equity = equity
            dd = (self.peak_equity - equity) / self.peak_equity
            if dd > self.max_drawdown:
                self.max_drawdown = dd
            
            self.equity_curve.append({
                'date': date_str,
                'equity': equity,
                'cash': self.cash,
                'positions': len(self.positions),
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
            'initial': self.initial_cash,
            'final': final,
            'total_return': total_ret,
            'annual_return': annual,
            'sharpe': sharpe,
            'calmar': calmar,
            'max_drawdown': self.max_drawdown,
            'win_rate': len(wins) / len(sells) if sells else 0,
            'trades': len(sells),
            'equity_curve': self.equity_curve,
            'trades_list': self.trades
        }


# ══════════════════════════════════════════════
#  主程序
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='真实数据回测')
    parser.add_argument('--start', default='2024-01-01', help='开始日期')
    parser.add_argument('--end', default='2025-03-28', help='结束日期')
    parser.add_argument('--cash', type=float, default=1_000_000, help='初始资金')
    args = parser.parse_args()
    
    # 测试股票
    stocks = {
        '601288': '农业银行',
        '000831': '中国稀土',
        '600118': '中国卫星',
    }
    
    print("\n" + "="*60)
    print("  波龙股神 V2.0 - 真实数据回测")
    print("="*60)
    print(f"  测试股票: {', '.join(stocks.values())}")
    print(f"  时间范围: {args.start} ~ {args.end}")
    print(f"  初始资金: {args.cash:,.0f} 元")
    print("="*60 + "\n")
    
    # 获取数据
    stock_data = {}
    for code, name in stocks.items():
        df = fetch_stock_data(code, args.start, args.end)
        if df is not None:
            stock_data[code] = df
            print(f"  {name}({code}): {len(df)}天, 价格 {df['close'].iloc[0]:.2f} -> {df['close'].iloc[-1]:.2f}")
    
    # 获取指数
    index_df = fetch_index_data(args.start, args.end)
    
    if not stock_data:
        print("错误: 无法获取任何股票数据")
        return
    
    print("\n" + "-"*60)
    
    # 运行回测
    engine = BacktestEngine(initial_cash=args.cash)
    result = engine.run(stock_data, index_df)
    
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
    
    # 交易明细
    if result['trades_list']:
        print("\n" + "-"*60)
        print("  交易明细:")
        print("-"*60)
        for t in result['trades_list'][-10:]:  # 最近10笔
            action = "买入" if t['action'] == 'buy' else "卖出"
            pnl_str = f"盈亏: {t.get('pnl', 0):+,.0f}" if 'pnl' in t else ""
            print(f"  {t['date']} {action} {stocks.get(t['code'], t['code'])} {t['shares']}股 @ {t['price']:.2f} | {t['reason']} {pnl_str}")
    
    print("\n  (C) 2026 SimonsTang / 上海巧未来人工智能科技有限公司")


if __name__ == '__main__':
    main()
