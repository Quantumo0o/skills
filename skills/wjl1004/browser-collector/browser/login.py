#!/usr/bin/env python3
"""
browser/login.py - 简化版登录管理
负责雪球等平台的 Cookie 登录流程
"""

import os
import json
import time
from typing import Optional, Dict
from pathlib import Path

try:
    from core.config import get_config
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.config import get_config


class LoginManager:
    """
    简化版登录管理器
    负责从文件加载/保存 Cookie，处理登录流程

    Usage:
        manager = LoginManager()
        cookies = manager.load_cookies("xueqiu")
        if not cookies:
            cookies = manager.login_xueqiu(username, password)
            manager.save_cookies("xueqiu", cookies)
    """

    COOKIE_DIR = Path.home() / ".openclaw" / "cookies"
    COOKIE_EXT = ".json"

    def __init__(self, config=None):
        self.config = config or get_config()
        self.COOKIE_DIR.mkdir(parents=True, exist_ok=True)

    def _get_cookie_path(self, platform: str) -> Path:
        return self.COOKIE_DIR / f"{platform}{self.COOKIE_EXT}"

    def load_cookies(self, platform: str) -> Optional[Dict]:
        """从文件加载 Cookie"""
        path = self._get_cookie_path(platform)
        if not path.exists():
            return None
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.config.warning(f"加载Cookie失败 {platform}: {e}")
            return None

    def save_cookies(self, platform: str, cookies: Dict) -> str:
        """保存 Cookie 到文件"""
        path = self._get_cookie_path(platform)
        with open(path, 'w') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        self.config.info(f"Cookie已保存: {path}")
        return str(path)

    def login_xueqiu(self, username: str, password: str,
                      browser=None) -> Optional[Dict]:
        """
        雪球登录

        Args:
            username: 用户名/手机号
            password: 密码
            browser: BrowserPlaywright 实例（如果为None，使用浏览器获取）

        Returns:
            Cookie 字典，失败返回 None
        """
        if browser is None:
            from browser.playwright import BrowserPlaywright
            browser = BrowserPlaywright(headless=False)

        try:
            self.config.info(f"开始雪球登录: {username}")
            browser.navigate("https://xueqiu.com/", wait_time=3)

            # 点击登录按钮
            browser.wait_and_click(".login-btn", timeout=5)
            time.sleep(1)

            # 切换到密码登录
            browser.wait_and_click(".tab-password", timeout=5)
            time.sleep(0.5)

            # 输入用户名密码
            browser.wait_and_input("input[name='username']", username, timeout=5)
            browser.input("input[name='password']", password, timeout=5)

            # 点击登录
            browser.click(".btn-login", timeout=5)
            time.sleep(3)

            # 获取 Cookie
            cookies = browser.get_cookies()
            cookie_dict = {c['name']: c['value'] for c in cookies if c['domain'] == '.xueqiu.com'}

            if cookie_dict:
                self.config.info("雪球登录成功")
                self.save_cookies("xueqiu", cookie_dict)
                return cookie_dict
            else:
                self.config.error("雪球登录失败: 未获取到Cookie")
                return None

        except Exception as e:
            self.config.error(f"雪球登录异常: {e}")
            return None
        finally:
            browser.close()

    def has_valid_cookies(self, platform: str, max_age_hours: int = 24) -> bool:
        """检查 Cookie 是否存在且未过期"""
        cookies = self.load_cookies(platform)
        if not cookies:
            return False
        cookie_file = self._get_cookie_path(platform)
        age_hours = (time.time() - cookie_file.stat().st_mtime) / 3600
        return age_hours < max_age_hours
