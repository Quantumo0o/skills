#!/usr/bin/env python3
"""
browser/playwright.py - Playwright 浏览器控制
隐身模式、更快加载、内置等待、指纹伪装

Usage:
    from browser.playwright import BrowserPlaywright

    browser = BrowserPlaywright(headless=True)
    browser.navigate("https://www.baidu.com")
    browser.click("#login-btn")
    browser.input("#username", "user", "#password", "pass")
    screenshot = browser.screenshot("login.png")
    browser.close()
"""

import os
import sys
import time
import random
import argparse
from typing import Optional, List

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

# 尝试从 core 导入配置
try:
    from core.config import get_config, BrowserConfig
    from core.exceptions import BrowserInitError
except ImportError:
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.config import get_config, BrowserConfig
    from core.exceptions import BrowserInitError


class BrowserPlaywright:
    """
    Playwright 浏览器控制类
    提供更隐蔽的浏览器自动化能力
    """

    def __init__(self, headless: bool = True, config: Optional[BrowserConfig] = None):
        self.config = config or get_config()
        self.headless = headless
        self.pw = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._init_browser()

    def _init_browser(self):
        try:
            self.pw = sync_playwright().start()
            self.browser = self.pw.chromium.launch(
                headless=self.headless,
                args=self._get_chrome_args()
            )
            self.context = self.browser.new_context(**self._get_context_options())
            self.page = self.context.new_page()
            self.page.set_default_timeout(10000)
            self.config.info(f"Playwright浏览器启动成功 (headless={self.headless})")
        except Exception as e:
            raise BrowserInitError("Playwright浏览器初始化失败", str(e))

    def _get_chrome_args(self) -> List[str]:
        args = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--allow-running-insecure-content',
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
        if self.config.proxy_enabled and self.config.proxy_host and self.config.proxy_port:
            proxy_str = self.config.get_proxy_string()
            if proxy_str:
                args.append(f'--proxy-server={proxy_str}')
        return args

    def _get_context_options(self) -> dict:
        options = {
            'viewport': {'width': 1920, 'height': 1080},
            'ignore_https_errors': True,
            'java_script_enabled': True,
        }
        if self.config.ua_pool_enabled:
            options['user_agent'] = self.config.get_random_user_agent()
        else:
            options['user_agent'] = self.config.user_agent
        if self.config.fingerprint_enabled:
            options['locale'] = self.config.fingerprint.language.replace('_', '-')
        return options

    @property
    def current_url(self) -> str:
        return self.page.url if self.page else ""

    def navigate(self, url: str, wait_time: float = 2, use_delay: bool = True) -> bool:
        if not self.page:
            return False
        if use_delay and self.config.delay.enabled:
            self.config.wait_delay()
        try:
            self.page.goto(url, wait_until='networkidle', timeout=30000)
            if wait_time > 0:
                time.sleep(wait_time * 0.3)
            return True
        except Exception as e:
            self.config.error(f"导航失败: {e}")
            return False

    def click(self, selector: str, by: str = 'css', timeout: float = 10, use_delay: bool = True) -> bool:
        if not self.page:
            return False
        if use_delay and self.config.delay.enabled:
            self.config.wait_delay()
        try:
            if by == 'xpath':
                self.page.click(f'xpath={selector}', timeout=int(timeout * 1000))
            else:
                self.page.click(selector, timeout=int(timeout * 1000))
            if use_delay and self.config.delay.enabled:
                time.sleep(random.uniform(0.5, 1.5))
            return True
        except Exception as e:
            self.config.warning(f"点击失败 [{selector}]: {e}")
            return False

    def input(self, selector: str, text: str, by: str = 'css', clear_first: bool = True,
              timeout: float = 10, use_delay: bool = True) -> bool:
        if not self.page:
            return False
        if use_delay and self.config.delay.enabled:
            self.config.wait_delay()
        try:
            elem = self.page.locator(f'xpath={selector}') if by == 'xpath' else self.page.locator(selector)
            elem.wait_for(timeout=int(timeout * 1000))
            if clear_first:
                elem.fill('')
                time.sleep(0.1)
            if self.config.delay.enabled:
                for char in text:
                    elem.press(char)
                    time.sleep(random.uniform(0.05, 0.15))
            else:
                elem.fill(text)
            if use_delay and self.config.delay.enabled:
                time.sleep(random.uniform(0.3, 0.8))
            return True
        except Exception as e:
            self.config.warning(f"输入失败 [{selector}]: {e}")
            return False

    def submit(self, selector: str, by: str = 'css', timeout: float = 10) -> bool:
        if not self.page:
            return False
        try:
            if by == 'xpath':
                self.page.locator(f'xpath={selector}').press('Enter')
            else:
                self.page.locator(selector).press('Enter')
            return True
        except Exception as e:
            self.config.warning(f"提交失败 [{selector}]: {e}")
            return False

    def wait_element(self, selector: str, by: str = 'css', timeout: float = 10) -> bool:
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
        return self.wait_element(selector, by, timeout) and self.click(selector, by)

    def wait_and_input(self, selector: str, text: str, by: str = 'css',
                       timeout: float = 10, clear_first: bool = True) -> bool:
        return self.wait_element(selector, by, timeout) and self.input(selector, text, by, clear_first)

    def wait_seconds(self, seconds: float = 1):
        time.sleep(seconds)

    def find_elements(self, selector: str, by: str = 'css') -> List:
        if not self.page:
            return []
        try:
            if by == 'xpath':
                return list(self.page.locator(f'xpath={selector}').all())
            return list(self.page.locator(selector).all())
        except Exception:
            return []

    def screenshot(self, name: str = "screenshot.png", full: bool = True) -> Optional[str]:
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
        return self.page.content() if self.page else ""

    def execute_script(self, script: str):
        if self.page:
            return self.page.evaluate(script)
        return None

    def get_cookies(self) -> List[dict]:
        if not self.context:
            return []
        try:
            return self.context.cookies()
        except Exception:
            return []

    def add_cookie(self, cookie_dict: dict) -> bool:
        if not self.context:
            return False
        try:
            self.context.add_cookies([cookie_dict])
            return True
        except Exception as e:
            self.config.warning(f"添加Cookie失败: {e}")
            return False

    def refresh(self):
        if self.page:
            self.page.reload()

    def back(self):
        if self.page:
            self.page.go_back()

    def forward(self):
        if self.page:
            self.page.go_forward()

    def close(self):
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


# ==================== 滑块拖动 ====================

def slider_drag(page: Page, slider_selector: str, distance: float,
                duration: float = 0.8, steps: int = 30, by: str = 'css') -> bool:
    """带轨迹防检测的滑块拖动"""
    try:
        track = _generate_slider_track(distance, steps=steps)
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
            time.sleep(duration / steps)
        page.mouse.up()
        return True
    except Exception:
        return False


def slider_drag_slow(page: Page, slider_selector: str, distance: float, by: str = 'css') -> bool:
    """慢速滑块拖动，更像人类"""
    try:
        track = _generate_slider_track(distance, steps=50)
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


def _ease_out_quad(t: float) -> float:
    return t * (2 - t)


def _generate_slider_track(distance: float, steps: int = 30) -> List[tuple]:
    track = []
    for i in range(steps + 1):
        t = i / steps
        eased = _ease_out_quad(t)
        x = distance * eased
        y = random.uniform(-0.5, 0.5)
        if i > 0 and i < steps:
            prev = track[-1]
            x = x - prev[0]
        else:
            x = x if i == 0 else distance - track[-1][0] if i == steps else x
        track.append((x, y))
    return track
