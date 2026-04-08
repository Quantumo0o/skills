#!/usr/bin/env python3
"""
collectors/builtin/xueqiu.py - 雪球数据采集器
支持：股票讨论帖、热门股票、搜索

技术方案：雪球API + Cookie认证，支持浏览器模式降级
"""

import json
import time
import re
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from urllib.parse import urlencode

import sys
from pathlib import Path

try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from core.config import get_config
    from collectors.base import Discussion, HotStock, items_to_dict_list
except ImportError:
    from collectors.base import Discussion, HotStock, items_to_dict_list
    get_config = lambda: None


class XueqiuCollector:
    """
    雪球数据采集器

    Usage:
        # API模式
        collector = XueqiuCollector()
        discussions = collector.get_stock_discussions("SH600000", limit=20)

        # 浏览器模式
        from browser.playwright import BrowserPlaywright
        browser = BrowserPlaywright()
        collector = XueqiuCollector(browser=browser)
        discussions = collector.get_stock_discussions_browser("SH600000")
    """

    BASE_URL = "https://xueqiu.com"
    HOT_STOCKS_API = "https://stock.xueqiu.com/v5/stock/screener/quote/list.json"
    DISCUSSIONS_API = "https://xueqiu.com/statuses/stock_timeline.json"
    SEARCH_API = "https://xueqiu.com/query.json"

    def __init__(self, browser=None, cookies: Dict = None, config=None):
        self.browser = browser
        self._cookies = cookies
        self.config = config or get_config()
        self._token = None

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Origin': self.BASE_URL,
            'Referer': self.BASE_URL,
        }
        if self._cookies and isinstance(self._cookies, dict):
            token = self._cookies.get('xq_a_token')
            if token:
                headers['Cookie'] = f'xq_a_token={token}'
        return headers

    def _fetch_api(self, url: str, params: Dict[str, Any] = None, retry: int = 3) -> Optional[Dict]:
        for attempt in range(retry):
            try:
                query = urlencode(params) if params else ""
                full_url = f"{url}?{query}" if query else url
                req = urllib.request.Request(full_url, headers=self._get_headers())
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = resp.read().decode('utf-8')
                    if '"error_code":40100' in data or '"需要登录"' in data:
                        if self.config:
                            self.config.warning("雪球API需要登录Cookie")
                        return None
                    return json.loads(data)
            except Exception as e:
                if self.config:
                    self.config.debug(f"雪球API请求失败 (尝试 {attempt+1}/{retry}): {e}")
                if attempt < retry - 1:
                    time.sleep(1)
        return None

    def get_stock_discussions(self, symbol: str, limit: int = 20) -> List[Discussion]:
        """获取股票讨论帖"""
        params = {
            "symbol": symbol,
            "page": 1,
            "size": limit,
            "type": "status",
            "sort": "time",
        }
        data = self._fetch_api(self.DISCUSSIONS_API, params)
        if not data:
            return []
        try:
            discussions = []
            for item in data.get('list', []):
                try:
                    user = item.get('user', {})
                    created = item.get('created_at')
                    ts = datetime.fromtimestamp(created / 1000) if created else datetime.now()
                    raw_text = item.get('text', '')
                    clean = re.sub(r'<[^>]+>', '', raw_text).strip()

                    d = Discussion(
                        title=self._extract_title(clean),
                        url=f"https://xueqiu.com/{item.get('id', '')}",
                        platform="xueqiu",
                        timestamp=ts,
                        post_id=str(item.get('id', '')),
                        user_id=str(user.get('id', '')),
                        username=user.get('screen_name', ''),
                        avatar=user.get('profile_image_url', ''),
                        content=clean,
                        comment_count=item.get('reply_count', 0),
                        like_count=item.get('like_count', 0),
                        share_count=item.get('retweet_count', 0),
                        raw_id=str(item.get('id', '')),
                    )
                    d.sentiment = self._analyze_sentiment(clean)
                    d.quality_score = self._calc_quality(d)
                    discussions.append(d)
                except Exception:
                    continue
            return discussions
        except Exception as e:
            if self.config:
                self.config.error(f"获取股票讨论帖失败: {e}")
            return []

    def get_hot_stocks(self, market: str = "all", limit: int = 20) -> List[HotStock]:
        """获取热门股票"""
        market_map = {"all": "", "cn": "cn", "hk": "hk", "us": "us"}
        params = {
            "page": 1, "size": limit, "order": "desc",
            "orderby": "percent", "market": market_map.get(market, ""),
            "type": "sh_sz",
            "_": int(time.time() * 1000),
        }
        data = self._fetch_api(self.HOT_STOCKS_API, params)
        if not data:
            return []
        try:
            stocks = data.get('data', {}).get('quote', [])
            hot = []
            for rank, item in enumerate(stocks, 1):
                try:
                    s = HotStock(
                        title=f"{item.get('name', '')} 热度排名 #{rank}",
                        url=f"https://xueqiu.com/S/{item.get('symbol', '')}",
                        platform="xueqiu",
                        timestamp=datetime.now(),
                        rank=rank,
                        stock_code=item.get('symbol', ''),
                        stock_name=item.get('name', ''),
                        price=item.get('current_price'),
                        change_pct=item.get('percent'),
                        hot_score=item.get('follow_percent'),
                        raw_id=item.get('symbol', ''),
                    )
                    hot.append(s)
                except Exception:
                    continue
            return hot
        except Exception as e:
            if self.config:
                self.config.error(f"获取热门股票失败: {e}")
            return []

    def search_discussions(self, keyword: str, limit: int = 20) -> List[Discussion]:
        """搜索讨论帖"""
        params = {"q": keyword, "type": "status", "count": limit, "page": 1}
        data = self._fetch_api(self.SEARCH_API, params)
        if not data:
            return []
        try:
            discussions = []
            for item in data.get('statuses', []):
                try:
                    user = item.get('user', {})
                    created = item.get('created_at')
                    ts = datetime.fromtimestamp(created / 1000) if created else datetime.now()
                    raw_text = item.get('text', '')
                    clean = re.sub(r'<[^>]+>', '', raw_text)
                    d = Discussion(
                        title=self._extract_title(clean),
                        url=f"https://xueqiu.com/{item.get('id', '')}",
                        platform="xueqiu",
                        timestamp=ts,
                        post_id=str(item.get('id', '')),
                        user_id=str(user.get('id', '')),
                        username=user.get('screen_name', ''),
                        content=clean,
                        tags=[keyword],
                        raw_id=str(item.get('id', '')),
                    )
                    d.sentiment = self._analyze_sentiment(clean)
                    d.quality_score = self._calc_quality(d)
                    discussions.append(d)
                except Exception:
                    continue
            return discussions
        except Exception as e:
            if self.config:
                self.config.error(f"搜索讨论帖失败: {e}")
            return []

    # ==================== Playwright 浏览器模式 ====================

    def _is_playwright(self) -> bool:
        return self.browser and hasattr(self.browser, 'page')

    def get_hot_stocks_browser(self, market: str = 'cn', limit: int = 10) -> List[HotStock]:
        """使用Playwright获取热门股票"""
        if not self.browser or not self._is_playwright():
            if self.config:
                self.config.warning("browser不是Playwright类型，降级到API模式")
            return self.get_hot_stocks(market, limit)
        try:
            market_urls = {
                'cn': 'https://xueqiu.com/hq/#exchange=cn&type=all',
                'hk': 'https://xueqiu.com/hq/#exchange=hk&type=all',
                'us': 'https://xueqiu.com/hq/#exchange=us&type=all',
                'all': 'https://xueqiu.com/hq/#exchange=cn&type=all',
            }
            self.browser.navigate(market_urls.get(market, market_urls['all']), wait_time=5)
            time.sleep(3)
            for _ in range(3):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

            stocks = []
            rank = 1
            rows = self.browser.find_elements('table tbody tr')
            for row in rows[:limit]:
                try:
                    cells = list(row.locator('td').all())
                    if len(cells) >= 4:
                        name = cells[0].inner_text().strip()
                        code = cells[1].inner_text().strip()
                        price_text = cells[3].inner_text().strip()
                        change_text = cells[5].inner_text().strip() if len(cells) > 5 else ''
                        try:
                            price = float(price_text.replace(',', ''))
                        except:
                            price = None
                        try:
                            pct = float(change_text.replace('%', ''))
                        except:
                            pct = None
                        if name and code:
                            s = HotStock(
                                title=f"{name} 热度排名 #{rank}",
                                url=f"https://xueqiu.com/S/{code}",
                                platform="xueqiu",
                                timestamp=datetime.now(),
                                rank=rank, stock_code=code, stock_name=name,
                                price=price, change_pct=pct,
                            )
                            stocks.append(s)
                            rank += 1
                except Exception:
                    continue
            return stocks
        except Exception as e:
            if self.config:
                self.config.error(f"浏览器获取热门股票失败: {e}")
            return []

    def get_stock_discussions_browser(self, symbol: str, limit: int = 20) -> List[Discussion]:
        """使用Playwright获取股票讨论帖"""
        if not self.browser or not self._is_playwright():
            return self.get_stock_discussions(symbol, limit)
        try:
            self.browser.navigate(f"https://xueqiu.com/S/{symbol}", wait_time=5)
            time.sleep(3)
            for _ in range(3):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

            discussions = []
            timelines = self.browser.find_elements('[class*="timeline"]')
            time_patterns = ['秒前', '分钟前', '小时前', '天前', '前·']
            skip_patterns = ['转发', '讨论', '赞', '收藏', '分享']

            for item in timelines:
                try:
                    text = item.inner_text()
                    if not text or len(text) < 20:
                        continue
                    has_time = any(p in text for p in time_patterns)
                    if not has_time:
                        continue

                    username = ''
                    for pat in time_patterns:
                        idx = text.find(pat)
                        if idx > 0:
                            parts = text[:idx].split('\n')
                            if parts:
                                username = parts[-1].strip()
                            break

                    lines = text.split('\n')
                    content_lines = []
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        if any(p in line for p in skip_patterns):
                            continue
                        if any(p in line for p in time_patterns):
                            continue
                        if username and username in line:
                            continue
                        if len(line) < 5:
                            continue
                        content_lines.append(line)
                    clean = '\n'.join(content_lines)
                    clean = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s\n]', '', clean).strip()

                    if clean and len(clean) > 10:
                        d = Discussion(
                            title=self._extract_title(clean),
                            url=f"https://xueqiu.com/S/{symbol}",
                            platform="xueqiu",
                            timestamp=datetime.now(),
                            username=username, content=clean,
                        )
                        d.sentiment = self._analyze_sentiment(clean)
                        d.quality_score = self._calc_quality(d)
                        discussions.append(d)
                        if len(discussions) >= limit:
                            break
                except Exception:
                    continue
            return discussions
        except Exception as e:
            if self.config:
                self.config.error(f"浏览器获取股票讨论失败: {e}")
            return []

    # ==================== 辅助方法 ====================

    def _extract_title(self, content: str, max_len: int = 50) -> str:
        if not content:
            return "无标题"
        first = content.split('\n')[0].strip()
        if len(first) > max_len:
            return first[:max_len] + "..."
        return first or "无标题"

    def _analyze_sentiment(self, content: str) -> str:
        pos = ['涨', '多头', '买入', '看好', '盈利', '增长', '突破', '牛市', '机会', '增持', '优质']
        neg = ['跌', '空头', '卖出', '看空', '亏损', '减持', '风险', '暴雷', '熊市', '警示', '减配']
        c = content.lower()
        pc = sum(1 for w in pos if w in c)
        nc = sum(1 for w in neg if w in c)
        if pc > nc:
            return "positive"
        elif nc > pc:
            return "negative"
        return "neutral"

    def _calc_quality(self, d: Discussion) -> float:
        score = 0.0
        cl = len(d.content or "")
        score += 0.4 if cl > 500 else 0.3 if cl > 200 else 0.2 if cl > 50 else 0.1
        total = (d.comment_count or 0) + (d.like_count or 0)
        score += 0.4 if total > 100 else 0.3 if total > 50 else 0.2 if total > 10 else 0.1
        score += 0.2
        return min(1.0, score)

    def save_to_file(self, items: List, filename: str) -> str:
        import os
        data_dir = self.config.data_dir if self.config else Path.home() / ".openclaw" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        path = data_dir / filename
        data = [item.to_dict() for item in items] if items and hasattr(items[0], 'to_dict') else items
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        if self.config:
            self.config.info(f"数据已保存: {path}")
        return str(path)


# urllib is needed at module level for _fetch_api
import urllib.request
