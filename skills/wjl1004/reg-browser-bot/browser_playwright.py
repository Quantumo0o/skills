#!/usr/bin/env python3
"""
Playwright 浏览器自动化模块
与 Selenium 版本并行，提供更好的反爬隐身能力
Phase D: Playwright替换Selenium

主要优势:
- 原生隐身模式，更难被检测
- 更快的页面加载和操作
- 内置，等待机制
- 无需 WebDriver
"""

import os
import sys
import time
import random
import argparse
from typing import Optional, List

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

from browser_config import get_config, BrowserConfig
from exceptions import BrowserInitError


class BrowserPlaywright:
    """
    Playwright 浏览器控制类
    与 Selenium Browser 类接口兼容（部分）
    提供更隐蔽的浏览器自动化
    """

    def __init__(self, headless: bool = True, config: Optional[BrowserConfig] = None):
        """
        初始化 Playwright 浏览器

        Args:
            headless: 是否使用无头模式
            config: 配置对象，None 时使用全局单例
        """
        self.config = config or get_config()
        self.headless = headless
        self.pw = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        self._init_browser()

    def _init_browser(self):
        """初始化 Playwright 浏览器"""
        try:
            self.pw = sync_playwright().start()

            # 创建 Chromium
            self.browser = self.pw.chromium.launch(
                headless=self.headless,
                args=self._get_chrome_args()
            )

            # 创建上下文（隐身模式）
            context_options = self._get_context_options()
            self.context = self.browser.new_context(**context_options)

            # 创建页面
            self.page = self.context.new_page()

            # 设置默认超时
            self.page.set_default_timeout(10000)

            self.config.info(
                f"Playwright浏览器启动成功 (headless={self.headless}, "
                f"UA池={self.config.ua_pool_enabled})"
            )

        except Exception as e:
            self.config.error(f"Playwright浏览器启动失败: {e}")
            raise BrowserInitError("Playwright浏览器初始化失败", str(e))

    def _get_chrome_args(self) -> List[str]:
        """获取 Chromium 启动参数（隐身优化）"""
        args = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--allow-running-insecure-content',
            # 隐身参数
            '--incognito',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-default-apps',
            '--disable-background-networking',
            '--disable-sync',
            '--disable-translate',
            '--metrics-recording-only',
            '--mute-audio',
            '--no-first-run',
        ]

        # 代理设置
        if self.config.proxy_enabled and self.config.proxy_host and self.config.proxy_port:
            proxy_str = self.config.get_proxy_string()
            if proxy_str:
                args.append(f'--proxy-server={proxy_str}')

        return args

    def _get_context_options(self) -> dict:
        """获取浏览器上下文选项"""
        options = {
            'viewport': {
                'width': 1920,
                'height': 1080
            },
            'ignore_https_errors': True,
            'java_script_enabled': True,
        }

        # User-Agent
        if self.config.ua_pool_enabled:
            ua = self.config.get_random_user_agent()
        else:
            ua = self.config.user_agent
        options['user_agent'] = ua

        # 指纹伪装：设置 locale
        if self.config.fingerprint_enabled:
            options['locale'] = self.config.fingerprint.language.replace('_', '-')

        return options

    @property
    def current_url(self) -> str:
        """获取当前 URL"""
        return self.page.url if self.page else ""

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
        if not self.page:
            return False

        # 请求前延迟
        if use_delay and self.config.delay.enabled:
            self.config.wait_delay()

        try:
            self.page.goto(url, wait_until='networkidle', timeout=30000)
            if wait_time > 0:
                time.sleep(wait_time * 0.3)
            self.config.info(f"已打开: {url}")
            return True
        except Exception as e:
            self.config.error(f"导航失败: {e}")
            return False

    def click(self, selector: str, by: str = 'css', timeout: float = 10,
              use_delay: bool = True) -> bool:
        """
        点击元素

        Args:
            selector: 选择器
            by: 选择器类型 (css/xpath)
            timeout: 超时时间
            use_delay: 是否使用随机延迟

        Returns:
            bool: 是否成功
        """
        if not self.page:
            return False

        # 操作前延迟
        if use_delay and self.config.delay.enabled:
            self.config.wait_delay()

        try:
            if by == 'xpath':
                self.page.click(f'xpath={selector}', timeout=int(timeout * 1000))
            else:
                self.page.click(selector, timeout=int(timeout * 1000))

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
        if not self.page:
            return False

        # 操作前延迟
        if use_delay and self.config.delay.enabled:
            self.config.wait_delay()

        try:
            if by == 'xpath':
                elem = self.page.locator(f'xpath={selector}')
            else:
                elem = self.page.locator(selector)

            elem.wait_for(timeout=int(timeout * 1000))

            if clear_first:
                elem.fill('')
                time.sleep(0.1)

            # 模拟人类输入（逐字输入）
            if self.config.delay.enabled:
                for char in text:
                    elem.press(char)
                    time.sleep(random.uniform(0.05, 0.15))
            else:
                elem.fill(text)

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
        if not self.page:
            return False

        try:
            if by == 'xpath':
                self.page.locator(f'xpath={selector}').press('Enter')
            else:
                self.page.locator(selector).press('Enter')
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
        if not self.page:
            return False

        try:
            if by == 'xpath':
                self.page.wait_for_selector(f'xpath={selector}', timeout=int(timeout * 1000))
            else:
                self.page.wait_for_selector(selector, timeout=int(timeout * 1000))
            return True
        except Exception:
            return False

    def wait_and_click(self, selector: str, by: str = 'css', timeout: float = 10) -> bool:
        """等待元素并点击"""
        if self.wait_element(selector, by, timeout):
            return self.click(selector, by)
        return False

    def wait_and_input(self, selector: str, text: str, by: str = 'css',
                       timeout: float = 10, clear_first: bool = True) -> bool:
        """等待元素并输入"""
        if self.wait_element(selector, by, timeout):
            return self.input(selector, text, by, clear_first)
        return False

    def wait_seconds(self, seconds: float = 1):
        """等待指定秒数"""
        time.sleep(seconds)
        self.config.debug(f"等待了 {seconds} 秒")

    def find_elements(self, selector: str, by: str = 'css') -> List:
        """
        查找多个元素

        Args:
            selector: 选择器
            by: 选择器类型

        Returns:
            元素列表
        """
        if not self.page:
            return []

        try:
            if by == 'xpath':
                return list(self.page.locator(f'xpath={selector}').all())
            else:
                return list(self.page.locator(selector).all())
        except Exception:
            return []

    def screenshot(self, name: str = "screenshot.png", full: bool = True) -> Optional[str]:
        """
        截图

        Args:
            name: 文件名
            full: 是否全屏截图

        Returns:
            文件路径 或 None
        """
        if not self.page:
            return None

        try:
            path = os.path.join(self.config.screenshot_dir, name)
            self.page.screenshot(path=path, full_page=full)
            self.config.info(f"截图已保存: {path}")
            return path
        except Exception as e:
            self.config.error(f"截图失败: {e}")
            return None

    def get_html(self) -> str:
        """获取页面源码"""
        return self.page.content() if self.page else ""

    def execute_script(self, script: str):
        """执行 JavaScript"""
        if self.page:
            return self.page.evaluate(script)
        return None

    def get_cookies(self) -> List[dict]:
        """获取所有 Cookies"""
        if not self.context:
            return []
        try:
            return self.context.cookies()
        except Exception:
            return []

    def add_cookie(self, cookie_dict: dict) -> bool:
        """添加 Cookie"""
        if not self.context:
            return False
        try:
            self.context.add_cookies([cookie_dict])
            return True
        except Exception as e:
            self.config.warning(f"添加Cookie失败: {e}")
            return False

    def refresh(self):
        """刷新页面"""
        if self.page:
            self.page.reload()

    def back(self):
        """返回上一页"""
        if self.page:
            self.page.go_back()

    def forward(self):
        """前进到下一页"""
        if self.page:
            self.page.go_forward()

    def close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.pw:
            self.pw.stop()
            self.pw = None
        self.context = None
        self.page = None
        self.config.info("Playwright浏览器已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


# ==================== 滑块拖动（Playwright版） ====================

def slider_drag(page: Page, slider_selector: str, distance: float,
                duration: float = 0.8, steps: int = 30,
                by: str = 'css') -> bool:
    """
    Playwright 版滑块拖动（带轨迹防检测）

    Args:
        page: Playwright Page 对象
        slider_selector: 滑块选择器
        distance: 缺口距离（像素）
        duration: 拖动总时长（秒）
        steps: 轨迹步数
        by: 选择器类型

    Returns:
        bool: 是否成功
    """
    try:
        # 生成带缓动的轨迹
        from utils import generate_slider_track, ease_out_quad
        track = generate_slider_track(distance, steps=steps, ease_func=ease_out_quad)

        # 获取滑块元素
        if by == 'xpath':
            slider = page.locator(f'xpath={slider_selector}')
        else:
            slider = page.locator(slider_selector)

        # 获取初始位置
        box = slider.bounding_box()
        if not box:
            return False

        start_x = box['x'] + box['width'] / 2
        start_y = box['y'] + box['height'] / 2

        # 开始拖动
        page.mouse.move(start_x, start_y)
        page.mouse.down()

        # 按轨迹移动
        for x, y in track:
            page.mouse.move(start_x + x, start_y + y)
            time.sleep(duration / steps)

        # 松开鼠标
        page.mouse.up()

        return True

    except Exception as e:
        return False


def slider_drag_slow(page: Page, slider_selector: str, distance: float,
                     by: str = 'css') -> bool:
    """
    Playwright 版滑块拖动（慢速版，更像人类）

    Args:
        page: Playwright Page 对象
        slider_selector: 滑块选择器
        distance: 缺口距离（像素）
        by: 选择器类型

    Returns:
        bool: 是否成功
    """
    try:
        from utils import generate_slider_track, ease_out_quad
        track = generate_slider_track(distance, steps=50, ease_func=ease_out_quad)

        if by == 'xpath':
            slider = page.locator(f'xpath={slider_selector}')
        else:
            slider = page.locator(slider_selector)

        box = slider.bounding_box()
        if not box:
            return False

        start_x = box['x'] + box['width'] / 2
        start_y = box['y'] + box['height'] / 2

        page.mouse.move(start_x, start_y)
        page.mouse.down()

        for x, y in track:
            page.mouse.move(start_x + x, start_y + y)
            time.sleep(0.015 + (hash(x) % 15) / 1000)

        page.mouse.up()

        return True

    except Exception:
        return False


# ==================== CLI ====================

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='Playwright 浏览器自动化控制工具',
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
                        choices=['css', 'xpath'],
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

    try:
        browser = BrowserPlaywright(headless=args.headless)
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
