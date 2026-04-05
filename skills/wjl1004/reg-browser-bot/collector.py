#!/usr/bin/env python3
"""
数据采集模块
功能：竞品监控、舆情监控、批量采集
使用统一的 BrowserConfig
"""

import os
import sys
import json
import time
import csv
import argparse
from datetime import datetime
from typing import Optional, List, Dict, Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser_config import get_config, BrowserConfig
from exceptions import BrowserInitError

# Phase B: SQLite 存储支持
try:
    from models import DatabaseManager, CollectedData, get_database
except ImportError:
    import sys as _sys
    _sys.path.insert(0, str(__file__).rsplit('/', 1)[0] if '/' in __file__ else '.')
    from models import DatabaseManager, CollectedData, get_database


class DataCollector:
    """数据采集器"""
    
    @property
    def db(self) -> DatabaseManager:
        """懒加载数据库管理器"""
        if self._db is None:
            self._db = get_database()
        return self._db

    def __init__(self, config: Optional[BrowserConfig] = None):
        """
        初始化采集器
        
        Args:
            config: 配置对象，None 时使用全局单例
        """
        self.config = config or get_config()
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        # Phase B: SQLite 数据库管理器
        self._db: Optional[DatabaseManager] = None
    
    def init_browser(self, headless: bool = True) -> bool:
        """
        初始化浏览器
        
        Args:
            headless: 是否使用无头模式
            
        Returns:
            bool: 是否成功
        """
        try:
            original_headless = self.config.headless
            self.config.set_headless(headless)
            
            options = self.config.get_chrome_options()
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 10)
            
            self.config.set_headless(original_headless)
            self.config.info("采集器浏览器启动成功")
            return True
        except Exception as e:
            self.config.error(f"采集器浏览器启动失败: {e}")
            return False
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.config.info("采集器浏览器已关闭")
    
    def navigate(self, url: str, wait_time: float = 2):
        """
        导航到 URL
        
        Args:
            url: 目标 URL
            wait_time: 等待秒数
        """
        if self.driver:
            self.driver.get(url)
            # 使用 WebDriverWait 等待页面加载完成
            try:
                WebDriverWait(self.driver, max(wait_time, 10)).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
            except Exception:
                pass  # 超时则继续
    
    def scroll_down(self, times: int = 3, interval: float = 1):
        """
        滚动页面
        
        Args:
            times: 滚动次数
            interval: 每次间隔秒数
        """
        if self.driver:
            for _ in range(times):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # 使用 WebDriverWait 等待滚动完成
                try:
                    WebDriverWait(self.driver, interval).until(lambda d: False)
                except Exception:
                    pass
    
    def get_elements(self, selector: str, by: str = 'css') -> List:
        """
        获取元素列表
        
        Args:
            selector: 选择器
            by: 选择器类型
            
        Returns:
            元素列表
        """
        if not self.driver:
            return []
        
        by_map = {'css': By.CSS_SELECTOR, 'xpath': By.XPATH, 'id': By.ID, 'name': By.NAME}
        by_type = by_map.get(by, By.CSS_SELECTOR)
        
        return self.driver.find_elements(by_type, selector)
    
    def extract_text(self, elements: List) -> List[str]:
        """
        提取文本列表
        
        Args:
            elements: 元素列表
            
        Returns:
            文本列表
        """
        return [e.text for e in elements if e.text.strip()]
    
    def save_json(self, data: Any, filename: str) -> str:
        """
        保存 JSON
        
        Args:
            data: 数据
            filename: 文件名
            
        Returns:
            文件路径
        """
        path = os.path.join(self.config.data_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.config.info(f"JSON已保存: {path}")
        return path
    
    def save_to_database(self, data: CollectedData) -> bool:
        """
        Phase B: 保存采集数据到 SQLite

        Args:
            data: CollectedData 数据对象

        Returns:
            bool: 是否成功
        """
        try:
            self.db.save_collected_data(data)
            self.config.debug(f"采集数据已保存SQLite: {data.id}")
            return True
        except Exception as e:
            self.config.warning(f"SQLite保存采集数据失败: {e}")
            return False

    def save_csv(self, data: List[Dict], filename: str, headers: Optional[List[str]] = None) -> str:
        """
        保存 CSV
        
        Args:
            data: 数据列表
            filename: 文件名
            headers: 表头
            
        Returns:
            文件路径
        """
        path = os.path.join(self.config.data_dir, filename)
        with open(path, 'w', encoding='utf-8', newline='') as f:
            if headers:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            else:
                writer = csv.writer(f)
                writer.writerows(data) if data and isinstance(data[0], list) else None
        
        self.config.info(f"CSV已保存: {path}")
        return path
    
    # ========== 预设采集器 ==========
    
    def collect_taobao_products(self, keyword: str, pages: int = 3) -> str:
        """
        采集淘宝商品
        
        Args:
            keyword: 搜索关键词
            pages: 页数
            
        Returns:
            保存的文件路径
        """
        results = []
        date_str = datetime.now().strftime('%Y%m%d')
        
        for page in range(1, pages + 1):
            url = (
                f"https://s.taobao.com/search?q={keyword}&imgfile=&js=1&stats_click="
                f"search_radio_all%3A1&initiative_id=staobaoz_{date_str}&ie=utf8&page={page}"
            )
            self.navigate(url)
            self.scroll_down(2)
            
            items = self.get_elements('.item')
            for item in items:
                try:
                    title = item.find_element(By.CSS_SELECTOR, '.title').text
                    price = item.find_element(By.CSS_SELECTOR, '.price').text
                    results.append({'标题': title, '价格': price})
                except Exception as e:
                    self.config.debug(f"解析商品失败: {e}")
        
        filename = f'taobao_{keyword}_{date_str}.csv'
        path = self.save_csv(results, filename)

        # Phase B: 同时保存到 SQLite
        import uuid
        data = CollectedData(
            id=str(uuid.uuid4()),
            task_id=f"taobao_{keyword}_{date_str}",
            account_name='default',
            platform='taobao',
            keyword=keyword,
            items=results,
            count=len(results),
            raw_data=None,
            created_at=datetime.now().isoformat()
        )
        self.save_to_database(data)

        return path
    
    def collect_jd_products(self, keyword: str, pages: int = 3) -> str:
        """
        采集京东商品
        
        Args:
            keyword: 搜索关键词
            pages: 页数
            
        Returns:
            保存的文件路径
        """
        results = []
        date_str = datetime.now().strftime('%Y%m%d')
        
        for page in range(1, pages + 1):
            url = f"https://search.jd.com/Search?keyword={keyword}&enc=utf-8&page={page}"
            self.navigate(url)
            self.scroll_down(2)
            
            items = self.get_elements('.gl-item')
            for item in items:
                try:
                    title = item.find_element(By.CSS_SELECTOR, '.p-name em').text
                    price = item.find_element(By.CSS_SELECTOR, '.p-price strong i').text
                    results.append({'标题': title, '价格': price})
                except Exception as e:
                    self.config.debug(f"解析商品失败: {e}")
        
        filename = f'jd_{keyword}_{date_str}.csv'
        path = self.save_csv(results, filename)

        # Phase B: 同时保存到 SQLite
        import uuid
        data = CollectedData(
            id=str(uuid.uuid4()),
            task_id=f"jd_{keyword}_{date_str}",
            account_name='default',
            platform='jd',
            keyword=keyword,
            items=results,
            count=len(results),
            raw_data=None,
            created_at=datetime.now().isoformat()
        )
        self.save_to_database(data)

        return path
    
    def collect_douyin_products(self, keyword: str) -> str:
        """
        采集抖音商品
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            保存的文件路径
        """
        results = []
        url = f"https://www.douyin.com/search/{keyword}"
        self.navigate(url)
        self.scroll_down(3)
        
        items = self.get_elements('[data-e2e="search-item"]')
        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, '[class*="title"]').text
                price = item.find_element(By.CSS_SELECTOR, '[class*="price"]').text
                results.append({'标题': title, '价格': price})
            except Exception as e:
                self.config.debug(f"解析商品失败: {e}")
        
        filename = f'douyin_{keyword}_{datetime.now().strftime("%Y%m%d")}.csv'
        path = self.save_csv(results, filename)

        # Phase B: 同时保存到 SQLite
        import uuid
        data = CollectedData(
            id=str(uuid.uuid4()),
            task_id=f"douyin_{keyword}_{datetime.now().strftime("%Y%m%d")}",
            account_name='default',
            platform='douyin',
            keyword=keyword,
            items=results,
            count=len(results),
            raw_data=None,
            created_at=datetime.now().isoformat()
        )
        self.save_to_database(data)

        return path
    
    def monitor_price(self, url: str, selector: str) -> Dict[str, Any]:
        """
        监控价格
        
        Args:
            url: 商品 URL
            selector: 价格选择器
            
        Returns:
            监控结果
        """
        self.navigate(url)
        try:
            price = self.driver.find_element(By.CSS_SELECTOR, selector).text
            result = {'url': url, 'price': price, 'time': datetime.now().isoformat()}
        except Exception as e:
            self.config.warning(f"价格监控失败: {e}")
            result = {'url': url, 'price': None, 'time': datetime.now().isoformat(), 'error': str(e)}
        
        return result
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='数据采集工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s taobao 白酒 3
  %(prog)s jd 白酒 5
  %(prog)s douyin 白酒
  %(prog)s monitor "https://item.jd.com/123.html" ".price"
        """
    )
    
    parser.add_argument('command', nargs='?', default='help',
                        help='命令: taobao, jd, douyin, monitor, help')
    parser.add_argument('keyword', nargs='?', help='搜索关键词')
    parser.add_argument('pages', nargs='?', type=int, default=3, help='采集页数')
    parser.add_argument('--url', help='监控URL')
    parser.add_argument('--selector', default='.price', help='价格选择器')
    parser.add_argument('--headless', action='store_true', default=True,
                        help='使用无头模式')
    
    args = parser.parse_args()
    
    if args.command == 'help':
        parser.print_help()
        print("""
命令说明:
  taobao <关键词> [页数]   采集淘宝商品
  jd <关键词> [页数]       采集京东商品
  douyin <关键词>          采集抖音商品
  monitor <URL> <选择器>   监控价格
        """)
        return 0
    
    collector = DataCollector()
    
    if not collector.init_browser(args.headless):
        print("错误: 浏览器初始化失败")
        return 1
    
    try:
        if args.command == "taobao":
            keyword = args.keyword or "白酒"
            path = collector.collect_taobao_products(keyword, args.pages)
            print(f"已保存: {path}")
        
        elif args.command == "jd":
            keyword = args.keyword or "白酒"
            path = collector.collect_jd_products(keyword, args.pages)
            print(f"已保存: {path}")
        
        elif args.command == "douyin":
            keyword = args.keyword or "白酒"
            path = collector.collect_douyin_products(keyword)
            print(f"已保存: {path}")
        
        elif args.command == "monitor":
            if not args.url:
                print("错误: 需要指定 --url")
                return 1
            result = collector.monitor_price(args.url, args.selector)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        else:
            print(f"未知命令: {args.command}")
            return 1
        
        return 0
    
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    finally:
        collector.close()


if __name__ == "__main__":
    sys.exit(main())
