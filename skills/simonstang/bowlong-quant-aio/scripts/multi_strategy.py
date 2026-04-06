#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.0
多策略轮动系统 — 50只股票池，趋势+震荡双策略

核心设计：
1. 50只股票池：10个行业 × 每行业前5龙头
2. 双策略切换：
   - 趋势市：均线跟踪策略
   - 震荡市：RSI区间策略
3. 马丁加仓：龙头回调只加仓一次
4. 条件进出：不一直持有，条件不符即出局
"""

import os
import sys
import logging
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional
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
#  股票池定义：10个行业 × 5只龙头 = 50只
# ══════════════════════════════════════════════

STOCK_POOL = {
    # 银行
    '银行': ['601288', '600036', '601166', '600000', '601398'],
    # 新能源
    '新能源': ['002594', '300750', '601012', '002129', '300014'],
    # 白酒
    '白酒': ['600519', '000858', '000568', '002304', '000596'],
    # 家电
    '家电': ['000333', '000651', '600690', '002050', '000100'],
    # 医药
    '医药': ['300760', '600276', '000538', '002007', '300122'],
    # 科技
    '科技': ['000063', '002415', '300059', '002230', '300033'],
    # 军工
    '军工': ['600118', '000768', '600893', '002179', '300034'],
    # 稀土有色
    '有色': ['000831', '600111', '601899', '002466', '600547'],
    # 保险券商
    '金融': ['601318', '601601', '600030', '601211', '600837'],
    # 基建
    '基建': ['601668', '601390', '600585', '601186', '002607'],
}

# 股票代码到名称映射
STOCK_NAMES = {
    # 银行
    '601288': '农业银行', '600036': '招商银行', '601166': '兴业银行',
    '600000': '浦发银行', '601398': '工商银行',
    # 新能源
    '002594': '比亚迪', '300750': '宁德时代', '601012': '隆基绿能',
    '002129': 'TCL中环', '300014': '亿纬锂能',
    # 白酒
    '600519': '贵州茅台', '000858': '五粮液', '000568': '泸州老窖',
    '002304': '洋河股份', '000596': '古井贡酒',
    # 家电
    '000333': '美的集团', '000651': '格力电器', '600690': '海尔智家',
    '002050': '三花智控', '000100': 'TCL科技',
    # 医药
    '300760': '迈瑞医疗', '600276': '恒瑞医药', '000538': '云南白药',
    '002007': '华兰生物', '300122': '智飞生物',
    # 科技
    '000063': '中兴通讯', '002415': '海康威视', '300059': '东方财富',
    '002230': '科大讯飞', '300033': '同花顺',
    # 军工
    '600118': '中国卫星', '000768': '中航西飞', '600893': '航发动力',
    '002179': '中航光电', '300034': '钢研高纳',
    # 有色
    '000831': '中国稀土', '600111': '北方稀土', '601899': '紫金矿业',
    '002466': '天齐锂业', '600547': '山东黄金',
    # 金融
    '601318': '中国平安', '601601': '中国太保', '600030': '中信证券',
    '601211': '国泰君安', '600837': '海通证券',
    # 基建
    '601668': '中国建筑', '601390': '中国中铁', '600585': '海螺水泥',
    '601186': '中国铁建', '002607': '中化岩土',
}


# ══════════════════════════════════════════════
#  数据获取
# ══════════════════════════════════════════════

def fetch_stock_data(code: str, start: str, end: str) -> Optional[pd.DataFrame]:
    """获取股票数据"""
    try:
        import akshare as ak
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
        logger.warning(f"获取 {code} 失败: {e}")
        return None


# ══════════════════════════════════════════════
#  市场状态判断
# ══════════════════════════════════════════════

class MarketState(Enum):
    TREND_UP = "trend_up"       # 上涨趋势
    TREND_DOWN = "trend_down"   # 下跌趋势
    OSCILLATE = "oscillate"     # 震荡
    UNKNOWN = "unknown"


def sma(s, n): return s.rolling(n).mean()
def ema(s, n): return s.ewm(span=n, adjust=False).mean()


def rsi(s, n=14):
    d = s.diff()
    g = d.clip(lower=0).rolling(n).mean()
    l = (-d.clip(upper=0)).rolling(n).mean()
    return 100 - 100 / (1 + g / l.replace(0, np.nan))


def atr(h, l, c, n=14):
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()


def detect_market_state(df, idx) -> MarketState:
    """判断市场状态"""
    if idx < 30:
        return MarketState.UNKNOWN
    
    close = df['close']
    c = close.iloc[idx]
    
    ma5 = sma(close, 5).iloc[idx]
    ma10 = sma(close, 10).iloc[idx]
    ma20 = sma(close, 20).iloc[idx]
    
    if pd.isna(ma5) or pd.isna(ma10) or pd.isna(ma20):
        return MarketState.UNKNOWN
    
    # 均线发散程度（判断趋势强度）
    ma_spread = abs(ma5 - ma20) / ma20
    
    # ADX替代：用均线角度
    ma5_slope = (ma5 - sma(close, 5).iloc[idx-5]) / ma5 if idx >= 5 else 0
    
    # 判断状态
    if ma5 > ma10 > ma20 and ma_spread > 0.02:
        return MarketState.TREND_UP
    elif ma5 < ma10 < ma20 and ma_spread > 0.02:
        return MarketState.TREND_DOWN
    elif ma_spread < 0.02:  # 均线粘合
        return MarketState.OSCILLATE
    else:
        return MarketState.OSCILLATE


# ══════════════════════════════════════════════
#  双策略系统
# ══════════════════════════════════════════════

class TrendStrategy:
    """趋势策略：均线跟踪"""
    
    @staticmethod
    def should_buy(df, idx) -> Tuple[bool, str]:
        """趋势买入信号"""
        if idx < 30:
            return False, ""
        
        close = df['close']
        c = close.iloc[idx]
        
        ma5 = sma(close, 5).iloc[idx]
        ma10 = sma(close, 10).iloc[idx]
        ma20 = sma(close, 20).iloc[idx]
        
        if pd.isna(ma5) or pd.isna(ma10) or pd.isna(ma20):
            return False, ""
        
        # 条件：均线多头 + 放量突破
        if c > ma5 and ma5 > ma10 and ma10 > ma20:
            # 放量确认
            vol = df['volume'].iloc[idx]
            vol_ma = df['volume'].iloc[idx-5:idx].mean()
            if vol > vol_ma * 1.3:
                return True, f"趋势突破 MA5={ma5:.2f}"
        
        return False, ""
    
    @staticmethod
    def should_sell(df, idx, pos) -> Tuple[bool, str]:
        """趋势卖出信号"""
        close = df['close']
        c = close.iloc[idx]
        
        ma5 = sma(close, 5).iloc[idx]
        ma10 = sma(close, 10).iloc[idx]
        
        if pd.isna(ma5) or pd.isna(ma10):
            return False, ""
        
        pnl = (c - pos['cost']) / pos['cost']
        
        # 止损
        if pnl < -0.08:
            return True, f"趋势止损{pnl:.1%}"
        
        # 趋势破坏
        if c < ma10 and ma5 < ma10:
            return True, f"趋势破坏"
        
        # 移动止盈（盈利10%后回撤5%）
        if pnl > 0.10 and c < pos.get('peak', c) * 0.95:
            return True, f"趋势止盈{pnl:.1%}"
        
        return False, ""


class OscillateStrategy:
    """震荡策略：RSI区间"""
    
    @staticmethod
    def should_buy(df, idx) -> Tuple[bool, str]:
        """震荡买入信号（超卖反弹）"""
        if idx < 30:
            return False, ""
        
        close = df['close']
        c = close.iloc[idx]
        
        rsi_val = rsi(close, 14).iloc[idx]
        ma20 = sma(close, 20).iloc[idx]
        
        if pd.isna(rsi_val) or pd.isna(ma20):
            return False, ""
        
        # 条件：RSI超卖 + 支撑位附近
        if rsi_val < 30 and c > ma20 * 0.95:  # 跌破MA20但不多
            return True, f"RSI超卖={rsi_val:.0f}"
        
        # RSI金叉
        if idx >= 1:
            rsi_prev = rsi(close, 14).iloc[idx-1]
            if pd.notna(rsi_prev) and rsi_val > 30 and rsi_prev < 30:
                return True, f"RSI金叉={rsi_val:.0f}"
        
        return False, ""
    
    @staticmethod
    def should_sell(df, idx, pos) -> Tuple[bool, str]:
        """震荡卖出信号"""
        close = df['close']
        c = close.iloc[idx]
        
        rsi_val = rsi(close, 14).iloc[idx]
        
        if pd.isna(rsi_val):
            return False, ""
        
        pnl = (c - pos['cost']) / pos['cost']
        
        # 止损
        if pnl < -0.06:
            return True, f"震荡止损{pnl:.1%}"
        
        # RSI超买
        if rsi_val > 70:
            return True, f"RSI超买={rsi_val:.0f}"
        
        # 盈利到位
        if pnl > 0.08:
            return True, f"震荡止盈{pnl:.1%}"
        
        return False, ""


# ══════════════════════════════════════════════
#  马丁加仓策略
# ══════════════════════════════════════════════

class MartinPosition:
    """马丁加仓管理"""
    
    @staticmethod
    def should_add(df, idx, pos) -> Tuple[bool, str]:
        """判断是否加仓（只加一次）"""
        # 已加过仓就不再加
        if pos.get('martin_added', False):
            return False, ""
        
        close = df['close']
        c = close.iloc[idx]
        cost = pos['cost']
        
        pnl = (c - cost) / cost
        
        # 条件：龙头股回调5-10%，但趋势未坏
        if -0.10 < pnl < -0.05:
            ma20 = sma(close, 20).iloc[idx]
            if pd.notna(ma20) and c > ma20 * 0.95:  # 还在MA20附近
                return True, f"马丁加仓{pnl:.1%}"
        
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
    martin_added: bool = False
    sector: str = ""


class BacktestEngine:
    def __init__(self, initial_cash=1_000_000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, Position] = {}
        self.trades = []
        self.equity_curve = []
        self.peak_equity = initial_cash
        self.max_drawdown = 0.0
        
        self.trend_strategy = TrendStrategy()
        self.oscillate_strategy = OscillateStrategy()
        self.martin = MartinPosition()
    
    def _fee(self, amount, is_sell):
        return max(amount * 0.0003, 5) + (amount * 0.001 if is_sell else 0)
    
    def _buy(self, code, price, pct, date, idx, reason, strategy, sector):
        """买入"""
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
            pos.martin_added = True  # 标记已加仓
        else:
            self.positions[code] = Position(
                shares=shares, cost=exec_price, entry_idx=idx,
                peak=exec_price, strategy=strategy, sector=sector
            )
        
        self.trades.append({
            'date': date, 'code': code, 'action': 'buy',
            'price': exec_price, 'shares': shares,
            'amount': total, 'fee': fee, 'reason': reason,
            'strategy': strategy, 'sector': sector
        })
        
        logger.info(f"  [买入] {STOCK_NAMES.get(code, code)} {shares}股 @ {exec_price:.2f} | {strategy} | {reason}")
    
    def _sell(self, code, price, date, reason):
        """卖出"""
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
            'amount': total, 'fee': fee, 'reason': reason,
            'pnl': pnl, 'pnl_pct': pnl_pct,
            'strategy': pos.strategy, 'sector': pos.sector
        })
        
        logger.info(f"  [卖出] {STOCK_NAMES.get(code, code)} {pos.shares}股 @ {exec_price:.2f} | {reason} | 盈亏: {pnl:+,.0f} ({pnl_pct:+.1%})")
    
    def _equity(self, prices):
        pos_val = sum(p.shares * prices.get(c, p.cost) for c, p in self.positions.items())
        return self.cash + pos_val
    
    def run(self, stock_data: Dict[str, pd.DataFrame], sector_map: Dict[str, str]):
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
            
            # ── 1. 检查持仓 ──
            to_sell = []
            for code, pos in list(self.positions.items()):
                if code not in prices:
                    continue
                
                cur_price = prices[code]
                if cur_price > pos.peak:
                    pos.peak = cur_price
                
                df = stock_data[code]
                idx_list = df[df['date'] <= date].index
                if len(idx_list) == 0:
                    continue
                idx = idx_list[-1]
                
                # 根据策略类型判断卖出
                if pos.strategy == 'trend':
                    should, reason = self.trend_strategy.should_sell(df, idx, pos.__dict__)
                else:
                    should, reason = self.oscillate_strategy.should_sell(df, idx, pos.__dict__)
                
                if should:
                    to_sell.append((code, reason))
            
            for code, reason in to_sell:
                self._sell(code, prices[code], date_str, reason)
            
            # ── 2. 马丁加仓检查 ──
            for code, pos in list(self.positions.items()):
                if code not in prices or pos.martin_added:
                    continue
                
                df = stock_data[code]
                idx_list = df[df['date'] <= date].index
                if len(idx_list) == 0:
                    continue
                idx = idx_list[-1]
                
                should, reason = self.martin.should_add(df, idx, pos.__dict__)
                if should and self.cash > 50000:
                    self._buy(code, prices[code], 0.20, date_str, i, reason, pos.strategy, pos.sector)
            
            # ── 3. 新开仓 ──
            if len(self.positions) < 10:  # 最多10只
                # 遍历所有股票，找到符合条件的
                candidates = []
                
                for code in codes:
                    if code in self.positions:
                        continue
                    
                    df = stock_data[code]
                    idx_list = df[df['date'] <= date].index
                    if len(idx_list) < 30:
                        continue
                    idx = idx_list[-1]
                    
                    # 判断市场状态
                    state = detect_market_state(df, idx)
                    
                    # 根据状态选择策略
                    if state == MarketState.TREND_UP:
                        should, reason = self.trend_strategy.should_buy(df, idx)
                        if should:
                            score = self._calc_score(df, idx)
                            candidates.append((code, 'trend', reason, score, idx))
                    
                    elif state == MarketState.OSCILLATE:
                        should, reason = self.oscillate_strategy.should_buy(df, idx)
                        if should:
                            score = self._calc_score(df, idx)
                            candidates.append((code, 'oscillate', reason, score, idx))
                
                # 按分数排序，选最高的
                candidates.sort(key=lambda x: -x[3])
                
                for code, strategy, reason, score, idx in candidates[:3]:
                    if len(self.positions) >= 10:
                        break
                    if self.cash < 50000:
                        break
                    
                    sector = sector_map.get(code, 'unknown')
                    self._buy(code, prices[code], 0.15, date_str, i, reason, strategy, sector)
            
            # ── 4. 记录净值 ──
            equity = self._equity(prices)
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
    
    def _calc_score(self, df, idx) -> float:
        """计算股票得分"""
        close = df['close']
        c = close.iloc[idx]
        
        ma5 = sma(close, 5).iloc[idx]
        ma10 = sma(close, 10).iloc[idx]
        ma20 = sma(close, 20).iloc[idx]
        
        score = 50
        
        if c > ma5: score += 10
        if ma5 > ma10: score += 10
        if ma10 > ma20: score += 10
        
        # 动量
        mom = (c / close.iloc[idx-20] - 1) if idx >= 20 else 0
        if mom > 0.10: score += 20
        elif mom > 0.05: score += 15
        elif mom > 0: score += 10
        
        return score
    
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
    
    # 构建股票池
    all_codes = []
    sector_map = {}
    for sector, codes in STOCK_POOL.items():
        for code in codes:
            all_codes.append(code)
            sector_map[code] = sector
    
    print("\n" + "="*60)
    print("  波龙股神 V2.0 - 多策略轮动系统")
    print("="*60)
    print(f"  股票池: {len(all_codes)}只（{len(STOCK_POOL)}个行业 × 5只龙头）")
    print(f"  时间: {args.start} ~ {args.end}")
    print(f"  初始资金: {args.cash:,.0f} 元")
    print("="*60)
    print("\n  行业分布:")
    for sector, codes in STOCK_POOL.items():
        print(f"    {sector}: {', '.join([STOCK_NAMES.get(c, c) for c in codes])}")
    print()
    
    # 获取数据
    logger.info("获取股票数据...")
    stock_data = {}
    for code in all_codes:
        df = fetch_stock_data(code, args.start, args.end)
        if df is not None and len(df) > 50:
            stock_data[code] = df
            ret = (df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100
            logger.info(f"  {STOCK_NAMES.get(code, code)}: {len(df)}天, {ret:+.1f}%")
    
    if not stock_data:
        print("错误: 无法获取数据")
        return
    
    print("\n" + "-"*60)
    
    # 运行回测
    engine = BacktestEngine(initial_cash=args.cash)
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
        for t in wins[-8:]:
            name = STOCK_NAMES.get(t['code'], t['code'])
            print(f"  {t['date']} {name} {t['shares']}股 @ {t['price']:.2f} | {t['strategy']} | {t['reason']} | +{t['pnl']:,.0f}")
    
    print("\n  (C) 2026 SimonsTang / 上海巧未来人工智能科技有限公司")


if __name__ == '__main__':
    main()
