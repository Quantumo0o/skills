#!/usr/bin/env python3
"""
core/config.py - 浏览器共享配置（精简版）
统一管理 Chrome Options、目录路径、日志配置、浏览器指纹、反爬对抗
"""

import os
import random
import time
import logging
from pathlib import Path
from typing import Optional, List, Callable
from dataclasses import dataclass, field


# ==================== UA 池 ====================

PC_UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
]

MOBILE_UA_LIST = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
]

COMMON_UA_LIST = PC_UA_LIST + MOBILE_UA_LIST

# ==================== 指纹配置 ====================

@dataclass
class FingerprintConfig:
    canvas_noise: bool = True
    webgl_noise: bool = True
    timezone: str = "Asia/Shanghai"
    language: str = "zh-CN"
    screen_resolution: str = "1920x1080"
    platform: str = "Win32"

    WEBGL_RENDERERS = [
        "ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0)",
        "Apple M1 Pro",
    ]
    WEBGL_VENDORS = ["Google Inc. (Intel)", "Google Inc. (NVIDIA)", "Apple Inc."]

    def randomize(self):
        self.timezone = random.choice(["Asia/Shanghai", "America/New_York", "Europe/London"])
        self.language = random.choice(["zh-CN", "en-US"])
        self.screen_resolution = random.choice(["1920x1080", "1366x768", "1440x900"])

    def get_timezone_offset(self) -> int:
        return {"Asia/Shanghai": -480, "America/New_York": 300, "Europe/London": 0}.get(self.timezone, -480)


# ==================== 延迟控制 ====================

@dataclass
class DelayConfig:
    min_seconds: float = 3.0
    max_seconds: float = 8.0
    enabled: bool = True

    def wait(self) -> float:
        if not self.enabled:
            return 0.0
        delay = random.uniform(self.min_seconds, self.max_seconds)
        time.sleep(delay)
        return delay


# ==================== BrowserConfig 主类 ====================

class BrowserConfig:
    """浏览器配置单例"""

    _instance: Optional['BrowserConfig'] = None

    DEFAULT_BASE_DIR = Path.home() / ".openclaw"
    DEFAULT_SCREENSHOT_DIR = DEFAULT_BASE_DIR / "screenshots"
    DEFAULT_DATA_DIR = DEFAULT_BASE_DIR / "data"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.screenshot_dir = self.DEFAULT_SCREENSHOT_DIR
        self.data_dir = self.DEFAULT_DATA_DIR
        self.headless = True
        self.user_agent = PC_UA_LIST[0]
        self.ua_pool_enabled = False
        self.ua_pool: List[str] = COMMON_UA_LIST
        self.ua_mobile_ratio = 0.2
        self.proxy_enabled = False
        self.proxy_host: Optional[str] = None
        self.proxy_port: Optional[int] = None
        self.fingerprint_enabled = True
        self.fingerprint = FingerprintConfig()
        self.delay = DelayConfig(min_seconds=3.0, max_seconds=8.0, enabled=False)
        self._ensure_directories()
        self._setup_logging()

    def _ensure_directories(self):
        for d in [self.screenshot_dir, self.data_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def _setup_logging(self):
        self.logger = logging.getLogger("browser-collector")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
            self.logger.addHandler(h)

    def get_random_user_agent(self) -> str:
        if not self.ua_pool:
            return self.user_agent
        if random.random() < self.ua_mobile_ratio:
            mobile = [u for u in self.ua_pool if "Mobile" in u or "iPhone" in u]
            if mobile:
                return random.choice(mobile)
        return random.choice(self.ua_pool)

    def enable_ua_pool(self, enabled: bool = True, mobile_ratio: float = 0.2):
        self.ua_pool_enabled = enabled
        self.ua_mobile_ratio = mobile_ratio

    def set_proxy(self, host: str, port: int, enabled: bool = True):
        self.proxy_host = host
        self.proxy_port = port
        self.proxy_enabled = enabled

    def get_proxy_string(self) -> Optional[str]:
        if not self.proxy_enabled or not self.proxy_host or not self.proxy_port:
            return None
        return f"http://{self.proxy_host}:{self.proxy_port}"

    def set_delay(self, min_seconds: float, max_seconds: float, enabled: bool = True):
        self.delay.min_seconds = min_seconds
        self.delay.max_seconds = max_seconds
        self.delay.enabled = enabled

    def wait_delay(self) -> float:
        return self.delay.wait()

    def get_fingerprint_script(self) -> str:
        fp = self.fingerprint
        renderer = random.choice(fp.WEBGL_RENDERERS)
        vendor = random.choice(fp.WEBGL_VENDORS)
        return f"""
(function() {{
    const _getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(p) {{
        if (p === 37445) return '{vendor}';
        if (p === 37446) return '{renderer}';
        return _getParameter.apply(this, arguments);
    }};
    Object.defineProperty(navigator, 'webdriver', {{ get: () => false }});
    Object.defineProperty(navigator, 'plugins', {{
        get: () => [{{ name: 'Chrome PDF Plugin' }}, {{ name: 'Chrome PDF Viewer' }}]
    }});
    Object.defineProperty(navigator, 'languages', {{
        get: () => ['{fp.language}', 'zh-CN', 'zh', 'en-US', 'en']
    }});
}})();
"""

    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    def debug(self, msg): self.logger.debug(msg)


_config: Optional[BrowserConfig] = None

def get_config() -> BrowserConfig:
    global _config
    if _config is None:
        _config = BrowserConfig()
    return _config
