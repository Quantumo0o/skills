#!/usr/bin/env python3
"""
collectors/builtin/eastmoney.py - 东方财富数据采集器
支持：股票实时行情、基金净值、指数行情、资金流向、涨跌停、换手率排行

API来源：东方财富公开API（push2delay.eastmoney.com）
"""

import json
import re
import time
import urllib.request
from datetime import datetime
from typing import Optional, List, Dict, Any
from urllib.parse import urlencode

import sys
from pathlib import Path

# 尝试从 core 导入配置（standalone模式下使用本地配置）
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from core.config import get_config
    from collectors.base import (
        StockQuote, FundNAV, IndexQuote, MoneyFlow, LimitUpDown, items_to_dict_list
    )
except ImportError:
    from collectors.base import (
        StockQuote, FundNAV, IndexQuote, MoneyFlow, LimitUpDown, items_to_dict_list
    )
    get_config = lambda: None


class EastMoneyCollector:
    """
    东方财富数据采集器

    Usage:
        collector = EastMoneyCollector()

        # 股票行情
        quote = collector.get_stock_quote("600000")

        # 基金净值
        fund = collector.get_fund_nav("000001")

        # 指数行情
        index = collector.get_index_quote("000001")

        # 资金流向
        flow = collector.get_money_flow("600000")

        # 涨停股
        limit_up = collector.get_limit_up(direction="up", limit=50)
    """

    BASE_URL = "https://push2delay.eastmoney.com/api/qt"
    FUND_API = "https://fundgz.1234567.com.cn/js/{fund_code}.js"

    def __init__(self, browser=None, config=None):
        self.browser = browser
        self.config = config or get_config()

    def _get_market_code(self, symbol: str) -> str:
        s = symbol.strip()
        if s.startswith(("600", "601", "603", "605", "688")):
            return "1"
        return "0"

    def _get_stock_id(self, symbol: str) -> str:
        clean = symbol.strip().upper()
        for p in ['SH', 'SZ', 'SHANGHAI', 'SHENZHEN']:
            if clean.startswith(p):
                clean = clean[len(p):]
                break
        return f"{self._get_market_code(clean)}.{clean}"

    def _fetch_api(self, url: str, params: Dict[str, Any], retry: int = 3) -> Optional[Dict]:
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        for attempt in range(retry):
            try:
                query = urlencode(params)
                full_url = f"{url}?{query}"
                req = urllib.request.Request(full_url, headers={
                    'User-Agent': ua,
                    'Referer': 'https://finance.eastmoney.com/',
                })
                with urllib.request.urlopen(req, timeout=10) as resp:
                    return json.loads(resp.read().decode('utf-8'))
            except Exception as e:
                if self.config:
                    self.config.debug(f"API请求失败 (尝试 {attempt+1}/{retry}): {e}")
                if attempt < retry - 1:
                    time.sleep(1)
        return None

    def get_stock_quote(self, code: str) -> Optional[StockQuote]:
        """获取股票实时行情"""
        stock_id = self._get_stock_id(code)
        params = {
            "secid": stock_id,
            "ut": "fa1fd462f804cd85e301045d00c8b903",
            "fields": "f43,f44,f45,f46,f47,f48,f57,f58,f50,f60,f116,f117,f169,f170",
        }
        data = self._fetch_api(f"{self.BASE_URL}/stock/get", params)
        if not data:
            return None
        try:
            r = data.get('data', {})
            if not r:
                return None
            return StockQuote(
                title=f"{r.get('f58', code)} ({r.get('f57', code)})",
                url=f"https://quote.eastmoney.com/{'sh' if stock_id.startswith('1') else 'sz'}{r.get('f57', code)}.html",
                platform="eastmoney",
                timestamp=datetime.now(),
                symbol=r.get('f57'),
                name=r.get('f58'),
                price=(r.get('f43') or 0) / 100,
                open=(r.get('f46') or 0) / 100,
                high=(r.get('f44') or 0) / 100,
                low=(r.get('f45') or 0) / 100,
                volume=int(r.get('f47') or 0),
                amount=(r.get('f50') or 0) / 100,
                change_pct=(r.get('f170') or 0) / 100,
                prev_close=(r.get('f60') or 0) / 100,
                market_cap=(r.get('f116') or 0) / 100,
                float_cap=(r.get('f117') or 0) / 100,
                raw_id=r.get('f57'),
            )
        except Exception as e:
            if self.config:
                self.config.error(f"解析股票行情失败: {e}")
            return None

    def get_fund_nav(self, fund_code: str) -> Optional[FundNAV]:
        """获取基金净值"""
        url = self.FUND_API.format(fund_code=fund_code)
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://fund.eastmoney.com/',
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read().decode('utf-8')
            match = re.search(r'jsonpgz\((.+)\)', data)
            if not match:
                return None
            fund_data = json.loads(match.group(1))
            gszf = fund_data.get('gszf', '0')
            return FundNAV(
                title=fund_data.get('name', fund_code),
                url=f"https://fund.eastmoney.com/{fund_code}.html",
                platform="eastmoney",
                timestamp=datetime.now(),
                fund_code=fund_code,
                fund_name=fund_data.get('name', ''),
                nav=float(fund_data.get('gsz', 0)),
                accum_nav=float(fund_data.get('dwjz', 0)),
                daily_growth=float(gszf.rstrip('%')) if gszf else None,
                subscribe_status=fund_data.get('sg', '未知'),
                redeem_status=fund_data.get('sh', '未知'),
                raw_id=fund_code,
            )
        except Exception as e:
            if self.config:
                self.config.error(f"获取基金净值失败: {e}")
            return None

    def get_index_quote(self, index_code: str = "000001") -> Optional[IndexQuote]:
        """获取指数行情"""
        if index_code.startswith("399"):
            secid = f"0{index_code[2:]}"
        else:
            secid = f"1{index_code}"
        params = {
            "secid": secid,
            "ut": "fa1fd462f804cd85e301045d00c8b903",
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18",
        }
        data = self._fetch_api(f"{self.BASE_URL}/stock/get", params)
        if not data:
            return None
        try:
            r = data.get('data', {})
            if not r:
                return None
            return IndexQuote(
                title=r.get('f14', index_code),
                url=f"https://quote.eastmoney.com/zs{index_code}.html",
                platform="eastmoney",
                timestamp=datetime.now(),
                index_code=r.get('f12', index_code),
                index_name=r.get('f14', ''),
                price=r.get('f2'),
                change_pct=r.get('f3'),
                open=r.get('f17'),
                high=r.get('f15'),
                low=r.get('f16'),
                prev_close=r.get('f18'),
                volume=int(r.get('f5', 0)),
                amount=r.get('f6'),
                raw_id=index_code,
            )
        except Exception as e:
            if self.config:
                self.config.error(f"解析指数行情失败: {e}")
            return None

    def get_money_flow(self, stock_code: str) -> Optional[MoneyFlow]:
        """获取资金流向"""
        secid = self._get_stock_id(stock_code)
        params = {
            "secid": secid,
            "ut": "fa1fd462f804cd85e301045d00c8b903",
            "fields": "f12,f14,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f64,f65",
        }
        data = self._fetch_api(f"{self.BASE_URL}/stock/fflow/get", params)
        if not data:
            return None
        try:
            r = data.get('data', {})
            if not r:
                return None
            net_inflow = (r.get('f62') or 0) / 100
            retail = (r.get('f64') or 0) / 100
            return MoneyFlow(
                title=f"{r.get('f14', stock_code)} 资金流向",
                url=f"https://quote.eastmoney.com/{'sh' if secid.startswith('1') else 'sz'}{stock_code}.html",
                platform="eastmoney",
                timestamp=datetime.now(),
                stock_code=stock_code,
                stock_name=r.get('f14', ''),
                net_amount=net_inflow,
                net_inflow=net_inflow,
                retail_inflow=retail,
                main_inflow_rate=(r.get('f71') or 0) / 100 if r.get('f71') else None,
                raw_id=stock_code,
            )
        except Exception as e:
            if self.config:
                self.config.error(f"解析资金流向失败: {e}")
            return None

    def get_top_money_flow(self, market: str = "all", limit: int = 20) -> List[MoneyFlow]:
        """获取行业资金流向（使用AKShare stock_fund_flow_industry）"""
        try:
            import akshare as ak
            # 使用正确的API获取行业资金流向
            df = ak.stock_fund_flow_industry()
            flows = []
            for _, row in df.head(limit).iterrows():
                try:
                    industry = str(row.get("行业", ""))
                    if not industry:
                        continue
                    inflow = float(row.get("流入资金", 0) or 0)
                    outflow = float(row.get("流出资金", 0) or 0)
                    net = float(row.get("净额", 0) or 0)
                    change_pct = float(row.get("行业-涨跌幅", 0) or 0)
                    leader_stock = str(row.get("领涨股", ""))
                    leader_change = float(row.get("领涨股-涨跌幅", 0) or 0)
                    
                    flows.append(MoneyFlow(
                        title=f"{industry} 行业资金流",
                        url="https://data.eastmoney.com/bkzj/hy.html",
                        platform="eastmoney",
                        timestamp=datetime.now(),
                        stock_code=industry,
                        stock_name=industry,
                        net_amount=net,
                        net_inflow=net,
                        change_pct=change_pct,
                        raw_id=industry,
                        content=f"流入:{inflow:.2f}亿 流出:{outflow:.2f}亿 净额:{net:.2f}亿 领涨股:{leader_stock}({leader_change}%)"
                    ))
                except Exception:
                    continue
            return flows
        except Exception as e:
            if self.config:
                self.config.debug(f"行业资金流获取失败: {e}")
            return []

    def get_limit_up(self, direction: str = "up", market: str = "all", limit: int = 100) -> List[LimitUpDown]:
        """获取涨跌停股（优先AKShare）"""
        try:
            import akshare as ak
            date_str = datetime.now().strftime("%Y%m%d")
            if direction == "up":
                df = ak.stock_zt_pool_em(date=date_str)
            else:
                df = ak.stock_zt_pool_dt_em(date=date_str)
            items = []
            for _, row in df.head(limit).iterrows():
                try:
                    sym = str(row.get("代码", ""))
                    name = str(row.get("名称", ""))
                    pct = float(row.get("涨跌幅", 0) or 0)
                    mkt = "sh" if sym.startswith(("6", "5", "4", "9")) else "sz"
                    turnover = float(row.get("换手率", 0) or 0) if row.get("换手率") is not None else None
                    amount = float(row.get("成交额", 0) or 0) if row.get("成交额") is not None else None
                    items.append(LimitUpDown(
                        title=f"{name} {'涨停' if direction == 'up' else '跌停'}",
                        url=f"https://quote.eastmoney.com/{mkt}{sym}.html",
                        platform="eastmoney",
                        timestamp=datetime.now(),
                        symbol=sym, name=name,
                        change_pct=pct,
                        turnover=turnover,
                        amount=amount,
                        direction=direction, market=mkt,
                        raw_id=sym,
                    ))
                except Exception:
                    continue
            return items
        except Exception as e:
            if self.config:
                self.config.debug(f"AKShare涨跌停失败: {e}")
            return []

    def get_top_turnover(self, market: str = "all", limit: int = 100) -> List[LimitUpDown]:
        """获取换手率排行（暂不可用，东方财富API被封）"""
        # 注意：东方财富push2接口已被封锁，换手率数据需通过AKShare或其他方式获取
        if self.config:
            self.config.warning("换手率排行暂不可用，请使用 limit-up 等其他功能")
        return []

    def save_to_file(self, items: List, filename: str) -> str:
        """保存采集结果到文件"""
        import os
        data_dir = self.config.data_dir if self.config else Path.home() / ".openclaw" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        path = data_dir / filename
        data = items_to_dict_list(items) if items and hasattr(items[0], 'to_dict') else items
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        if self.config:
            self.config.info(f"数据已保存: {path}")
        return str(path)

    def _ensure_browser(self):
        """确保浏览器已初始化"""
        if self.browser is None:
            from browser.playwright import BrowserPlaywright
            self.browser = BrowserPlaywright(headless=True)

    def get_limit_up_browser(self, direction: str = "up", market: str = "all", limit: int = 100) -> List[LimitUpDown]:
        """使用Playwright浏览器获取涨跌停数据"""
        try:
            self._ensure_browser()
            
            # 东方财富涨跌停页面
            if direction == "up":
                url = "https://data.eastmoney.com/ztb/"
            else:
                url = "https://data.eastmoney.com/ztb/"
            
            self.browser.navigate(url)
            self.browser.wait_element(".ztb-list", timeout=15000)
            
            # 等待数据加载
            time.sleep(2)
            
            # 执行JavaScript提取数据
            js_code = """
            () => {
                const items = document.querySelectorAll('.ztb-list tbody tr');
                const data = [];
                items.forEach(row => {
                    const cells = row.querySelectorAll('td');
                    if (cells.length >= 6) {
                        data.push({
                            code: cells[0].innerText,
                            name: cells[1].innerText,
                            price: cells[2].innerText,
                            pct: cells[3].innerText,
                            amount: cells[4].innerText,
                            time: cells[5].innerText
                        });
                    }
                });
                return data.slice(0, arguments[0]);
            }
            """
            result = self.browser.page.evaluate(js_code, limit)
            
            items = []
            for row in result:
                try:
                    sym = str(row.get('code', ''))
                    name = str(row.get('name', ''))
                    pct = float(str(row.get('pct', '0')).replace('%', '').replace('+', ''))
                    mkt = "sh" if sym.startswith(("6", "5", "4", "9")) else "sz"
                    items.append(LimitUpDown(
                        title=f"{name} {'涨停' if direction == 'up' else '跌停'}",
                        url=f"https://quote.eastmoney.com/{mkt}{sym}.html",
                        platform="eastmoney",
                        timestamp=datetime.now(),
                        symbol=sym, name=name,
                        change_pct=pct,
                        direction=direction, market=mkt,
                        raw_id=sym,
                    ))
                except Exception:
                    continue
            return items
        except Exception as e:
            if self.config:
                self.config.debug(f"浏览器涨跌停获取失败: {e}")
            return []

    def get_top_money_flow_browser(self, market: str = "all", limit: int = 20) -> List[MoneyFlow]:
        """使用Playwright浏览器获取行业资金流向"""
        try:
            self._ensure_browser()
            
            # 东方财富行业资金流页面
            url = "https://data.eastmoney.com/bkzj/hy.html"
            self.browser.navigate(url)
            self.browser.wait_element(".hy-rank", timeout=15000)
            
            time.sleep(2)
            
            # 提取数据
            js_code = """
            () => {
                const items = document.querySelectorAll('.hy-rank tbody tr');
                const data = [];
                items.forEach(row => {
                    const cells = row.querySelectorAll('td');
                    if (cells.length >= 6) {
                        data.push({
                            industry: cells[1].innerText,
                            inflow: cells[2].innerText,
                            outflow: cells[3].innerText,
                            net: cells[4].innerText,
                            change: cells[5].innerText
                        });
                    }
                });
                return data.slice(0, arguments[0]);
            }
            """
            result = self.browser.page.evaluate(js_code, limit)
            
            items = []
            for row in result:
                try:
                    industry = str(row.get('industry', ''))
                    net_text = str(row.get('net', '0')).replace('亿', '')
                    net = float(net_text) if net_text else 0
                    change_text = str(row.get('change', '0')).replace('%', '')
                    change = float(change_text) if change_text else 0
                    
                    items.append(MoneyFlow(
                        title=f"{industry} 行业资金流",
                        url="https://data.eastmoney.com/bkzj/hy.html",
                        platform="eastmoney",
                        timestamp=datetime.now(),
                        stock_code=industry,
                        stock_name=industry,
                        net_amount=net,
                        net_inflow=net,
                        change_pct=change,
                        raw_id=industry,
                        content=f"净流入:{net}亿 涨跌幅:{change}%"
                    ))
                except Exception:
                    continue
            return items
        except Exception as e:
            if self.config:
                self.config.debug(f"浏览器行业资金流获取失败: {e}")
            return []

    def get_stock_quote_browser(self, code: str) -> Optional[StockQuote]:
        """使用Playwright浏览器获取个股行情"""
        try:
            self._ensure_browser()
            
            # 清理代码
            clean_code = code.strip().upper()
            for prefix in ['SH', 'SZ', 'SHANGHAI', 'SHENZHEN']:
                if clean_code.startswith(prefix):
                    clean_code = clean_code[len(prefix):]
                    break
            
            # 确定市场
            if clean_code.startswith(("6", "5", "4", "9")):
                mkt = "sh"
            else:
                mkt = "sz"
            
            url = f"https://quote.eastmoney.com/{mkt}{clean_code}.html"
            self.browser.navigate(url)
            self.browser.wait_element(".stock-info", timeout=15000)
            
            time.sleep(1)
            
            # 提取数据
            js_code = """
            () => {
                const name = document.querySelector('.stock-name')?.innerText || '';
                const price = document.querySelector('.stock-price')?.innerText || '0';
                const pct = document.querySelector('.stock-pct')?.innerText || '0';
                const high = document.querySelector('.stock-high')?.innerText || '0';
                const low = document.querySelector('.stock-low')?.innerText || '0';
                const open = document.querySelector('.stock-open')?.innerText || '0';
                const prev = document.querySelector('.stock-prev')?.innerText || '0';
                const volume = document.querySelector('.stock-volume')?.innerText || '0';
                const amount = document.querySelector('.stock-amount')?.innerText || '0';
                return { name, price, pct, high, low, open, prev, volume, amount };
            }
            """
            result = self.browser.page.evaluate(js_code)
            
            price = float(result.get('price', 0) or 0)
            pct = float(str(result.get('pct', '0')).replace('%', '').replace('+', ''))
            
            return StockQuote(
                title=f"{result.get('name', code)} ({code})",
                url=url,
                platform="eastmoney",
                timestamp=datetime.now(),
                symbol=code,
                name=result.get('name', ''),
                price=price,
                change_pct=pct,
                open=float(result.get('open', 0) or 0),
                high=float(result.get('high', 0) or 0),
                low=float(result.get('low', 0) or 0),
                prev_close=float(result.get('prev', 0) or 0),
                raw_id=code,
            )
        except Exception as e:
            if self.config:
                self.config.debug(f"浏览器个股行情获取失败: {e}")
            return None
