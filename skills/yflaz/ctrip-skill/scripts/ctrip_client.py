#!/usr/bin/env python3
"""
携程 MCP Client v2 - 支持登录态的 Playwright 客户端

Usage:
    python ctrip_client.py <command> [options]

Commands:
    flight <from> <to> <date>     搜索机票
    train <from> <to> <date>      搜索火车票
    route <cities> <days>         行程规划
    compare <route1> <route2>     价格对比
    login                         执行登录

Options:
    --headless        无头模式（默认 True）
    --no-headless     可见浏览器
    --login           使用登录态（需要已登录）
"""

import json
import sys
import re
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class CtripClient:
    """携程 Playwright 客户端 v2 - 支持登录态和单例模式"""
    
    _instance = None
    _browser = None
    _context = None
    
    def __init__(self, headless=True, use_login=False, cookies_file="cookies.json"):
        self.headless = headless
        self.use_login = use_login
        self.cookies_file = Path(cookies_file)
        self.page = None
        self._launched = False
    
    @classmethod
    def get_instance(cls, **kwargs):
        """单例模式获取实例"""
        if cls._instance is None:
            cls._instance = cls(**kwargs)
        return cls._instance
    
    def launch(self):
        """启动浏览器（单例模式）"""
        if self._launched:
            print("✓ 浏览器已启动（复用实例）")
            return
        
        print("正在启动浏览器...")
        
        playwright = sync_playwright().start()
        
        # 浏览器参数
        browser_args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--disable-gpu',
            '--disable-blink-features=AutomationControlled'  # 反反爬
        ]
        
        self._browser = playwright.chromium.launch(
            headless=self.headless,
            args=browser_args
        )
        
        # 准备 context 选项
        context_options = {
            "viewport": {"width": 1920, "height": 1080},
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "locale": "zh-CN",
            "timezone_id": "Asia/Shanghai"
        }
        
        # 如果使用登录态，加载 cookies
        if self.use_login:
            if self.cookies_file.exists():
                try:
                    with open(self.cookies_file, "r", encoding="utf-8") as f:
                        cookies = json.load(f)
                    context_options["cookies"] = cookies
                    print(f"✓ 已加载 {len(cookies)} 个 cookies（登录态）")
                except Exception as e:
                    print(f"⚠ 加载 cookies 失败：{e}，将使用无登录模式")
                    self.use_login = False
            else:
                print(f"⚠ cookies 文件不存在：{self.cookies_file}，将使用无登录模式")
                self.use_login = False
        
        self._context = self._browser.new_context(**context_options)
        self.page = self._context.new_page()
        
        # 隐藏 webdriver 特征
        self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        self.page.set_default_timeout(60000)
        self._launched = True
        print("✓ 浏览器已启动")
    
    def search_flight(self, origin, dest, date):
        """
        搜索机票
        
        Args:
            origin: 出发城市
            dest: 目的城市
            date: 出发日期（YYYY-MM-DD）
        
        Returns:
            dict: {"route": "上海→曼谷", "date": "2026-10-01", "prices": [...], "flights": [...]}
        """
        print(f"✈ 搜索机票：{origin} → {dest}, 日期：{date}")
        
        if not self._launched:
            self.launch()
        
        # 构建搜索 URL
        url = f"https://flights.ctrip.com/international/search/{origin}-{dest}/{date}"
        
        try:
            # 导航到页面
            self.page.goto(url, wait_until="networkidle", timeout=30000)
            print(f"✓ 页面已加载")
            
            # 等待搜索结果（多种策略）
            self._wait_for_search_results()
            
            # 提取价格和航班信息
            prices = self._extract_prices()
            flights = self._extract_flight_info()
            
            result = {
                "route": f"{origin}→{dest}",
                "date": date,
                "prices": prices,
                "flights": flights,
                "min_price": self._parse_min_price(prices),
                "login_mode": self.use_login
            }
            
            if prices:
                print(f"✓ 找到 {len(prices)} 个价格选项，最低价：¥{result['min_price']}")
            else:
                print(f"⚠ 未找到价格信息（可能是页面结构变化或需要登录）")
            
            return result
            
        except PlaywrightTimeout as e:
            print(f"⚠ 等待超时：{e}")
            return {
                "route": f"{origin}→{dest}",
                "date": date,
                "prices": [],
                "flights": [],
                "min_price": 0,
                "error": f"Timeout: {str(e)}",
                "login_mode": self.use_login
            }
        except Exception as e:
            print(f"✗ 搜索失败：{str(e)}")
            return {
                "route": f"{origin}→{dest}",
                "date": date,
                "prices": [],
                "flights": [],
                "min_price": 0,
                "error": str(e),
                "login_mode": self.use_login
            }
    
    def search_train(self, origin, dest, date):
        """搜索火车票"""
        print(f"🚄 搜索火车票：{origin} → {dest}, 日期：{date}")
        
        if not self._launched:
            self.launch()
        
        url = f"https://trains.ctrip.com/TrainBooking/search/{origin}-{dest}/{date}"
        
        try:
            self.page.goto(url, wait_until="networkidle", timeout=30000)
            self._wait_for_search_results()
            
            trains = self._extract_train_info()
            
            result = {
                "route": f"{origin}→{dest}",
                "date": date,
                "trains": trains,
                "login_mode": self.use_login
            }
            
            print(f"✓ 找到 {len(trains)} 个车次")
            return result
            
        except Exception as e:
            print(f"✗ 搜索失败：{str(e)}")
            return {
                "route": f"{origin}→{dest}",
                "date": date,
                "trains": [],
                "error": str(e),
                "login_mode": self.use_login
            }
    
    def _wait_for_search_results(self, timeout=15):
        """等待搜索结果加载"""
        print(f"⏳ 等待搜索结果加载（最多{timeout}秒）...")
        
        # 多种等待策略
        selectors = [
            ".flight-card",
            ".search-result",
            "[class*='flight']",
            "[class*='result']",
            ".price",
            "text=¥",
            "text=起飞",
            "text=出发"
        ]
        
        for i in range(timeout):
            for selector in selectors:
                try:
                    element = self.page.query_selector(selector)
                    if element:
                        print(f"✓ 检测到搜索结果（{i+1}秒）")
                        return
                except:
                    pass
            self.page.wait_for_timeout(1000)
        
        print(f"⚠ 等待超时，继续执行（可能结果不完整）")
    
    def _extract_prices(self):
        """提取价格信息（增强版）"""
        prices = []
        
        try:
            # 尝试多种选择器
            selectors = [
                ".price",
                "[class*='price']",
                "[data-testid*='price']",
                ".c-price",
                ".flight-price",
                ".ticket-price",
                ".fare",
                "span:contains('¥')",
                "div:contains('￥')"
            ]
            
            for selector in selectors:
                try:
                    elements = self.page.query_selector_all(selector)
                    for el in elements[:30]:
                        try:
                            text = el.inner_text()
                            # 检查是否包含价格符号和数字
                            if ('¥' in text or '￥' in text) and any(c.isdigit() for c in text):
                                # 清理文本
                                price_text = text.strip()
                                if price_text and price_text not in prices:
                                    prices.append(price_text)
                        except:
                            pass
                    
                    if len(prices) >= 10:  # 找到足够多就停止
                        break
                        
                except Exception as e:
                    continue
            
            # 去重
            prices = list(dict.fromkeys(prices))
            
            # 如果还是没找到，尝试从页面文本中提取
            if not prices:
                try:
                    page_text = self.page.content()
                    # 使用正则提取价格
                    price_pattern = r'[¥￥]\s*(\d{3,}(?:,\d{3})*(?:\.\d{2})?)'
                    matches = re.findall(price_pattern, page_text)
                    for match in matches[:20]:
                        price_str = match.replace(',', '')
                        prices.append(f"¥{price_str}")
                except:
                    pass
            
        except Exception as e:
            print(f"⚠ 提取价格时出错：{str(e)}")
        
        return prices
    
    def _extract_flight_info(self):
        """提取航班详细信息"""
        flights = []
        
        try:
            cards = self.page.query_selector_all(".flight-card, [class*='flight'], [class*='card']")
            
            for card in cards[:10]:
                try:
                    text = card.inner_text()
                    if any(keyword in text for keyword in ['起飞', '到达', '航班', '航空', '直飞', '中转']):
                        flights.append({
                            "info": text[:300],  # 限制长度
                            "raw": text
                        })
                except:
                    pass
                    
        except Exception as e:
            print(f"⚠ 提取航班信息时出错：{str(e)}")
        
        return flights
    
    def _extract_train_info(self):
        """提取火车信息"""
        trains = []
        
        try:
            elements = self.page.query_selector_all(".train-item, [class*='train'], [class*='ticket'], [class*='result']")
            
            for el in elements[:10]:
                try:
                    text = el.inner_text()
                    if any(keyword in text for keyword in ['车次', '出发', '到达', '历时', '高铁', '动车']):
                        trains.append({
                            "info": text[:300]
                        })
                except:
                    pass
                    
        except Exception as e:
            print(f"⚠ 提取火车信息时出错：{str(e)}")
        
        return trains
    
    def _parse_min_price(self, prices):
        """解析最低价格"""
        min_p = float('inf')
        
        for p in prices:
            # 尝试多种价格格式
            patterns = [
                r'[¥￥]\s*([\d,]+(?:\.\d{2})?)',
                r'([\d,]+)\s*元',
                r'([\d,]+)\s*起'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, p)
                if match:
                    try:
                        price_str = match.group(1).replace(',', '')
                        price = float(price_str)
                        min_p = min(min_p, price)
                        break
                    except:
                        pass
        
        return int(min_p) if min_p != float('inf') else 0
    
    def close(self):
        """关闭浏览器（单例模式不真正关闭）"""
        if self._browser and not self._launched:
            # 只有非单例模式才关闭
            self._browser.close()
            print("✓ 浏览器已关闭")
        elif self._launched:
            print("ℹ 浏览器保持打开（单例模式）")
    
    @classmethod
    def close_all(cls):
        """关闭所有浏览器实例"""
        if cls._browser:
            cls._browser.close()
            cls._browser = None
            cls._instance = None
            print("✓ 所有浏览器实例已关闭")


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    # 解析参数
    headless = True
    use_login = False
    cookies_file = "cookies.json"
    
    args = sys.argv[2:]
    i = 0
    positional_args = [command]
    
    while i < len(args):
        arg = args[i]
        if arg == "--headless":
            headless = True
        elif arg == "--no-headless":
            headless = False
        elif arg == "--login":
            use_login = True
        elif arg.startswith("--cookies="):
            cookies_file = arg.split("=", 1)[1]
        elif not arg.startswith("-"):
            positional_args.append(arg)
        i += 1
    
    # 创建客户端
    client = CtripClient(headless=headless, use_login=use_login, cookies_file=cookies_file)
    
    try:
        if command == "flight" and len(positional_args) >= 4:
            origin = positional_args[1]
            dest = positional_args[2]
            date = positional_args[3]
            
            client.launch()
            result = client.search_flight(origin, dest, date)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif command == "train" and len(positional_args) >= 4:
            origin = positional_args[1]
            dest = positional_args[2]
            date = positional_args[3]
            
            client.launch()
            result = client.search_train(origin, dest, date)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif command == "login":
            # 调用登录脚本
            from ctrip_login import login
            login(cookies_file)
        
        else:
            print(f"未知命令或参数不足：{command}")
            print(__doc__)
    
    finally:
        client.close()
        CtripClient.close_all()


if __name__ == "__main__":
    main()
