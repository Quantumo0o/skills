#!/usr/bin/env python3
"""
浏览器自动化核心模块
合并 browser.py 和 browser_auto.py
提供统一的浏览器控制接口
"""

import os
import sys
import time
import random
import argparse
from typing import Optional, List, Tuple

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser_config import get_config, BrowserConfig
from exceptions import BrowserInitError, ElementNotFoundError


class Browser:
    """
    统一浏览器控制类
    支持：导航、点击、输入、表单提交、截图、页面源码获取
    """
    
    def __init__(self, headless: Optional[bool] = None, config: Optional[BrowserConfig] = None):
        """
        初始化浏览器
        
        Args:
            headless: 是否使用无头模式，None 时使用配置默认值
            config: 配置对象，None 时使用全局单例
        """
        self.config = config or get_config()
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        
        # 临时覆盖 headless 设置
        if headless is not None:
            original_headless = self.config.headless
            self.config.set_headless(headless)
            self._init_driver()
            self.config.set_headless(original_headless)
        else:
            self._init_driver()
    
    def _init_driver(self):
        """初始化 WebDriver"""
        try:
            options = self.config.get_chrome_options()
            
            # 尝试使用 undetected-chromedriver
            if self.config.use_undetected_chromedriver:
                try:
                    import undetected_chromedriver as uc
                    self.driver = uc.Chrome(options=options, headless=self.config.headless)
                    self.config.info("使用 undetected-chromedriver 启动")
                except ImportError:
                    self.config.warning("undetected-chromedriver 未安装，使用原生 webdriver")
                    self.driver = webdriver.Chrome(options=options)
            else:
                self.driver = webdriver.Chrome(options=options)
            
            self.wait = WebDriverWait(self.driver, 10)
            
            # 注入指纹伪装脚本
            if self.config.fingerprint_enabled:
                fingerprint_script = self.config.get_fingerprint_script()
                self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": fingerprint_script
                })
                self.config.debug("指纹伪装脚本已注入")
            
            self.config.info(f"浏览器启动成功 (headless={self.config.headless}, UA池={self.config.ua_pool_enabled})")
        except Exception as e:
            self.config.error(f"浏览器启动失败: {e}")
            raise BrowserInitError("浏览器初始化失败", str(e))
    
    @property
    def current_url(self) -> str:
        """获取当前 URL"""
        return self.driver.current_url if self.driver else ""
    
    def navigate(self, url: str, wait_time: float = 2, use_delay: bool = True) -> bool:
        """
        打开 URL
        
        Args:
            url: 目标 URL
            wait_time: 等待秒数
            use_delay: 是否使用随机延迟
            
        Returns:
            bool: 是否成功
        """
        if not self.driver:
            return False
        
        # 请求前延迟（Phase 4 反爬增强）
        if use_delay and self.config.delay.enabled:
            self.config.wait_delay()
        
        try:
            self.driver.get(url)
            # 等待页面加载完成（WebDriverWait 替代固定 sleep）
            WebDriverWait(self.driver, max(wait_time, 10)).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            if wait_time > 0:
                time.sleep(wait_time * 0.3)  # 小缓冲，不影响速度
            self.config.info(f"已打开: {url}")
            return True
        except Exception as e:
            self.config.error(f"导航失败: {e}")
            return False
    
    def click(self, selector: str, by: str = 'css', timeout: float = 10, use_delay: bool = True) -> bool:
        """
        点击元素
        
        Args:
            selector: 选择器
            by: 选择器类型 (css/xpath/id/name)
            timeout: 超时时间
            use_delay: 是否使用随机延迟
            
        Returns:
            bool: 是否成功
        """
        if not self.driver:
            return False
        
        # 操作前延迟
        if use_delay and self.config.delay.enabled:
            self.config.wait_delay()
        
        try:
            elem = self._find_element(selector, by, timeout)
            elem.click()
            self.config.info(f"已点击: {selector}")
            
            # 操作后延迟
            if use_delay and self.config.delay.enabled:
                time.sleep(random.uniform(0.5, 1.5))
            
            return True
        except Exception as e:
            self.config.warning(f"点击失败 [{selector}]: {e}")
            return False
    
    def input(self, selector: str, text: str, by: str = 'css', clear_first: bool = True, 
              timeout: float = 10, use_delay: bool = True) -> bool:
        """
        输入文本
        
        Args:
            selector: 选择器
            text: 输入文本
            by: 选择器类型
            clear_first: 是否先清空
            timeout: 超时时间
            use_delay: 是否使用随机延迟
            
        Returns:
            bool: 是否成功
        """
        if not self.driver:
            return False
        
        # 操作前延迟
        if use_delay and self.config.delay.enabled:
            self.config.wait_delay()
        
        try:
            elem = self._find_element(selector, by, timeout)
            if clear_first:
                elem.clear()
            
            # 模拟人类输入（逐字输入，有随机间隔）
            if self.config.delay.enabled:
                for char in text:
                    elem.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
            else:
                elem.send_keys(text)
            
            self.config.info(f"已输入: {text[:20]}...")
            
            # 操作后延迟
            if use_delay and self.config.delay.enabled:
                time.sleep(random.uniform(0.3, 0.8))
            
            return True
        except Exception as e:
            self.config.warning(f"输入失败 [{selector}]: {e}")
            return False
    
    def submit(self, selector: str, by: str = 'css', timeout: float = 10) -> bool:
        """
        提交表单
        
        Args:
            selector: 选择器
            by: 选择器类型
            timeout: 超时时间
            
        Returns:
            bool: 是否成功
        """
        if not self.driver:
            return False
        
        try:
            elem = self._find_element(selector, by, timeout)
            elem.submit()
            self.config.info(f"已提交表单: {selector}")
            return True
        except Exception as e:
            self.config.warning(f"提交失败 [{selector}]: {e}")
            return False
    
    def wait_element(self, selector: str, by: str = 'css', timeout: float = 10) -> bool:
        """
        等待元素出现
        
        Args:
            selector: 选择器
            by: 选择器类型
            timeout: 超时时间
            
        Returns:
            bool: 元素是否出现
        """
        if not self.driver:
            return False
        
        try:
            by_map = {'css': By.CSS_SELECTOR, 'xpath': By.XPATH, 'id': By.ID, 'name': By.NAME}
            self.wait.until(EC.presence_of_element_located((by_map.get(by, By.CSS_SELECTOR), selector)))
            return True
        except Exception:
            return False
    
    def wait_and_click(self, selector: str, by: str = 'css', timeout: float = 10) -> bool:
        """
        等待元素并点击
        
        Args:
            selector: 选择器
            by: 选择器类型
            timeout: 超时时间
            
        Returns:
            bool: 是否成功
        """
        if self.wait_element(selector, by, timeout):
            return self.click(selector, by)
        return False
    
    def wait_and_input(self, selector: str, text: str, by: str = 'css', 
                       timeout: float = 10, clear_first: bool = True) -> bool:
        """
        等待元素并输入
        
        Args:
            selector: 选择器
            text: 输入文本
            by: 选择器类型
            timeout: 超时时间
            clear_first: 是否先清空
            
        Returns:
            bool: 是否成功
        """
        if self.wait_element(selector, by, timeout):
            return self.input(selector, text, by, clear_first)
        return False
    
    def wait_seconds(self, seconds: float = 1):
        """
        等待指定秒数
        
        Args:
            seconds: 秒数
        """
        # 使用 WebDriverWait 等待（可被中断），fallback 到 sleep
        try:
            WebDriverWait(self.driver, seconds).until(lambda d: False)
        except Exception:
            pass
        self.config.debug(f"等待了 {seconds} 秒")
    
    def _find_element(self, selector: str, by: str, timeout: float) -> Optional[webdriver.remote.webelement.WebElement]:
        """
        查找单个元素
        
        Args:
            selector: 选择器
            by: 选择器类型
            timeout: 超时时间
            
        Returns:
            WebElement 或 None
        """
        by_map = {'css': By.CSS_SELECTOR, 'xpath': By.XPATH, 'id': By.ID, 'name': By.NAME}
        by_type = by_map.get(by, By.CSS_SELECTOR)
        
        return self.driver.find_element(by_type, selector)
    
    def find_elements(self, selector: str, by: str = 'css') -> List:
        """
        查找多个元素
        
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
    
    def screenshot(self, name: str = "screenshot.png", full: bool = True) -> Optional[str]:
        """
        截图
        
        Args:
            name: 文件名
            full: 是否全屏截图
            
        Returns:
            文件路径 或 None
        """
        if not self.driver:
            return None
        
        try:
            path = os.path.join(self.config.screenshot_dir, name)
            self.driver.save_screenshot(path)
            self.config.info(f"截图已保存: {path}")
            return path
        except Exception as e:
            self.config.error(f"截图失败: {e}")
            return None
    
    def get_html(self) -> str:
        """获取页面源码"""
        return self.driver.page_source if self.driver else ""
    
    def execute_script(self, script: str, *args):
        """执行 JavaScript"""
        if self.driver:
            return self.driver.execute_script(script, *args)
        return None
    
    def get_cookies(self) -> List[dict]:
        """获取所有 Cookies"""
        return self.driver.get_cookies() if self.driver else []
    
    def add_cookie(self, cookie_dict: dict) -> bool:
        """添加 Cookie"""
        if not self.driver:
            return False
        try:
            self.driver.add_cookie(cookie_dict)
            return True
        except Exception as e:
            self.config.warning(f"添加Cookie失败: {e}")
            return False
    
    def refresh(self):
        """刷新页面"""
        if self.driver:
            self.driver.refresh()
    
    def back(self):
        """返回上一页"""
        if self.driver:
            self.driver.back()
    
    def forward(self):
        """前进到下一页"""
        if self.driver:
            self.driver.forward()
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.config.info("浏览器已关闭")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='浏览器自动化控制工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s navigate https://www.baidu.com
  %(prog)s click "#login-btn" --by css
  %(prog)s input "#username" "myuser" --by id
  %(prog)s screenshot
  %(prog)s screenshot --name myshot.png
  %(prog)s wait --seconds 3
        """
    )
    
    parser.add_argument('command', nargs='?', default='help',
                        help='命令: navigate, click, input, submit, screenshot, wait, html, help')
    parser.add_argument('selector', nargs='?', help='选择器')
    parser.add_argument('text', nargs='?', help='输入文本')
    parser.add_argument('--by', '-b', default='css', 
                        choices=['css', 'xpath', 'id', 'name'],
                        help='选择器类型 (默认: css)')
    parser.add_argument('--name', '-n', default='screenshot.png',
                        help='截图文件名')
    parser.add_argument('--seconds', '-s', type=float, default=1,
                        help='等待秒数')
    parser.add_argument('--headless', action='store_true', default=None,
                        help='使用无头模式')
    parser.add_argument('--no-headless', dest='headless', action='store_false',
                        help='不使用无头模式')
    
    args = parser.parse_args()
    
    # 处理 help 命令
    if args.command == 'help':
        parser.print_help()
        print("""
命令说明:
  navigate <URL>      打开网页
  click <selector>    点击元素 (默认CSS选择器)
  input <selector> <text>  输入文本
  submit <selector>   提交表单
  screenshot [name]   截图 (默认 screenshot.png)
  wait [seconds]      等待 (默认 1 秒)
  html                获取页面源码
        """)
        return 0
    
    # 执行命令
    try:
        browser = Browser(headless=args.headless)
    except BrowserInitError as e:
        print(f"错误: {e}")
        return 1
    
    try:
        if args.command == 'navigate':
            url = args.selector or 'https://www.baidu.com'
            browser.navigate(url)
        
        elif args.command == 'click':
            if not args.selector:
                print("错误: 需要指定选择器")
                return 1
            browser.click(args.selector, args.by)
        
        elif args.command == 'input':
            if not args.selector or not args.text:
                print("错误: 需要指定选择器和文本")
                return 1
            browser.input(args.selector, args.text, args.by)
        
        elif args.command == 'submit':
            if not args.selector:
                print("错误: 需要指定选择器")
                return 1
            browser.submit(args.selector, args.by)
        
        elif args.command == 'screenshot':
            path = browser.screenshot(args.name)
            if path:
                print(f"截图: {path}")
        
        elif args.command == 'wait':
            browser.wait_seconds(args.seconds)
        
        elif args.command == 'html':
            print(browser.get_html())
        
        else:
            print(f"未知命令: {args.command}")
            return 1
        
        return 0
    
    finally:
        browser.close()


if __name__ == "__main__":
    sys.exit(main())
