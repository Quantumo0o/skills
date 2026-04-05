#!/usr/bin/env python3
"""
浏览器共享配置 - 单例模式
统一管理 Chrome Options、目录路径、日志配置、浏览器指纹、反爬对抗
Phase 4: UA池轮换、代理支持、指纹伪装、请求间隔随机化
"""

import os
import random
import time
import logging
from pathlib import Path
from typing import Optional, List, Callable
from selenium.webdriver.chrome.options import Options

try:
    from fake_useragent import UserAgent
    FAKE_USERAGENT_AVAILABLE = True
except ImportError:
    FAKE_USERAGENT_AVAILABLE = False

# ==================== fake-useragent 全局缓存 ====================

_fake_ua: Optional['UserAgent'] = None

def get_fake_ua():
    """获取 fake-useragent 实例（全局缓存，网络失败时返回 None）"""
    global _fake_ua
    if _fake_ua is None and FAKE_USERAGENT_AVAILABLE:
        try:
            # fallback 到现有 PC_UA_LIST，避免网络失败时完全失效
            _fake_ua = UserAgent(fallback=random.choice(PC_UA_LIST))
        except Exception:
            _fake_ua = None
    return _fake_ua


# ==================== UA 池 ====================

# 常见 PC User-Agent 列表 (20+)
PC_UA_LIST = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    # Firefox on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    # Safari on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    # Edge on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    # Opera
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
]

# 常见 Mobile User-Agent 列表
MOBILE_UA_LIST = [
    # iPhone Safari
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    # Android Chrome
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    # iPad
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
]

# 合并所有 UA
COMMON_UA_LIST = PC_UA_LIST + MOBILE_UA_LIST


# ==================== 指纹伪装配置 ====================

class FingerprintConfig:
    """浏览器指纹伪装配置"""
    
    # 预定义的 Canvas 噪声数据 (模拟不同显卡/驱动的渲染差异)
    CANVAS_NOISE_DATA = [
        "9ed2cbe80a840a6686da0f4d1bf78367",  # 预计算噪声1
        "8c4e9f2d1a7b3c6e0f5d8a9b2c4e6f1a",  # 预计算噪声2
        "3f7a9c1e4b8d2f6a0c5e3b7d9f1a4c8e",  # 预计算噪声3
    ]
    
    # 预定义的 WebGL 渲染器信息
    WEBGL_RENDERERS = [
        "ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0)",
        "Apple M1 Pro",
        "Intel Iris OpenGL Engine",
    ]
    
    # 预定义的 WebGL 厂商
    WEBGL_VENDORS = [
        "Google Inc. (Intel)",
        "Google Inc. (NVIDIA)",
        "Google Inc. (AMD)",
        "Apple Inc.",
        "Intel Inc.",
    ]
    
    def __init__(
        self,
        canvas_noise: bool = True,
        webgl_noise: bool = True,
        timezone: str = "Asia/Shanghai",  # 或 "America/New_York"
        language: str = "zh-CN",          # 或 "en-US"
        screen_resolution: str = "1920x1080",
        platform: str = "Win32",
    ):
        self.canvas_noise = canvas_noise
        self.webgl_noise = webgl_noise
        self.timezone = timezone
        self.language = language
        self.screen_resolution = screen_resolution
        self.platform = platform
    
    def randomize(self):
        """随机化指纹参数"""
        self.timezone = random.choice(["Asia/Shanghai", "America/New_York", "Europe/London", "Asia/Tokyo"])
        self.language = random.choice(["zh-CN", "en-US", "en-GB", "ja-JP"])
        self.screen_resolution = random.choice(["1920x1080", "1366x768", "1440x900", "2560x1440"])
        self.platform = random.choice(["Win32", "MacIntel", "Linux x86_64"])
    
    def get_timezone_offset(self) -> int:
        """获取时区偏移量（分钟）"""
        import datetime
        if self.timezone == "Asia/Shanghai":
            return -480  # UTC+8
        elif self.timezone == "America/New_York":
            return 300  # UTC-5 (EST)
        elif self.timezone == "Europe/London":
            return 0
        elif self.timezone == "Asia/Tokyo":
            return -540  # UTC+9
        return -480


# ==================== 延迟控制 ====================

class DelayConfig:
    """请求间隔配置"""
    
    def __init__(
        self,
        min_seconds: float = 3.0,
        max_seconds: float = 8.0,
        enabled: bool = True,
        on_action: Optional[Callable] = None,
    ):
        """
        Args:
            min_seconds: 最小延迟秒数
            max_seconds: 最大延迟秒数
            enabled: 是否启用随机延迟
            on_action: 每次操作后的回调函数
        """
        self.min_seconds = min_seconds
        self.max_seconds = max_seconds
        self.enabled = enabled
        self.on_action = on_action
    
    def wait(self) -> float:
        """
        执行随机延迟
        
        Returns:
            实际等待的秒数
        """
        if not self.enabled:
            return 0.0
        
        delay = random.uniform(self.min_seconds, self.max_seconds)
        
        if self.on_action:
            self.on_action(delay)
        
        time.sleep(delay)
        return delay
    
    def wait_fixed(self, seconds: float):
        """固定延迟"""
        time.sleep(seconds)
        return seconds


# ==================== BrowserConfig 主类 ====================

class BrowserConfig:
    """
    浏览器配置单例
    所有模块共享同一配置实例
    Phase 4 新增: UA池、代理支持、指纹伪装、延迟控制
    """
    
    _instance: Optional['BrowserConfig'] = None
    
    # 默认路径
    DEFAULT_BASE_DIR = Path.home() / ".openclaw"
    DEFAULT_SCREENSHOT_DIR = DEFAULT_BASE_DIR / "screenshots"
    DEFAULT_DATA_DIR = DEFAULT_BASE_DIR / "data"
    DEFAULT_ACCOUNTS_DIR = DEFAULT_BASE_DIR / "accounts"
    DEFAULT_LOGS_DIR = DEFAULT_BASE_DIR / "logs"
    
    # Chrome 路径（None 表示让 Selenium 自动检测）
    CHROME_BINARY = None
    
    # 默认 User-Agent (兼容旧代码)
    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        
        # 目录配置
        self.screenshot_dir = self.DEFAULT_SCREENSHOT_DIR
        self.data_dir = self.DEFAULT_DATA_DIR
        self.accounts_dir = self.DEFAULT_ACCOUNTS_DIR
        self.logs_dir = self.DEFAULT_LOGS_DIR
        
        # 确保目录存在
        self._ensure_directories()
        
        # Chrome 选项
        self.headless = True
        self.window_size = (1920, 1080)
        self.user_agent = self.DEFAULT_USER_AGENT
        self.disable_automation = True
        
        # === Phase 4: 反爬增强配置 ===
        
        # UA 池配置
        self.ua_pool_enabled = False  # 是否启用 UA 池轮换
        self.ua_pool: List[str] = COMMON_UA_LIST
        self.ua_mobile_ratio = 0.2    # Mobile UA 占比
        
        # 代理配置
        self.proxy_enabled = False
        self.proxy_host: Optional[str] = None
        self.proxy_port: Optional[int] = None
        self.proxy_type: str = "http"  # http, https, socks5
        self.proxy_username: Optional[str] = None
        self.proxy_password: Optional[str] = None
        
        # 指纹伪装
        self.fingerprint_enabled = True
        self.fingerprint = FingerprintConfig()
        
        # 延迟控制
        self.delay = DelayConfig(min_seconds=3.0, max_seconds=8.0, enabled=False)
        
        # undetected-chromedriver 支持
        self.use_undetected_chromedriver = False
        
        # 日志配置
        self._setup_logging()
    
    def _ensure_directories(self):
        """确保必要目录存在"""
        for dir_path in [self.screenshot_dir, self.data_dir, self.accounts_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self):
        """配置日志"""
        self.logger = logging.getLogger("BrowserBot")
        self.logger.setLevel(logging.INFO)
        
        # 避免重复添加handler
        if not self.logger.handlers:
            # 控制台输出
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            # 文件输出
            log_file = self.logs_dir / "browser_bot.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    # ==================== UA 池管理 ====================
    
    def set_user_agent(self, user_agent: str):
        """设置 User-Agent（手动指定）"""
        self.user_agent = user_agent
    
    def get_random_user_agent(self) -> str:
        """
        获取随机 User-Agent（优先使用 fake-useragent，失败时 fallback 到 UA 池）

        Returns:
            随机选择的 UA 字符串
        """
        fake = get_fake_ua()
        if fake:
            try:
                return fake.random
            except Exception:
                pass

        # fallback: 使用内置 UA 池
        if not self.ua_pool:
            return self.DEFAULT_USER_AGENT

        if random.random() < self.ua_mobile_ratio:
            mobile_ua = [ua for ua in self.ua_pool if "Mobile" in ua or "iPhone" in ua or "Android" in ua]
            if mobile_ua:
                return random.choice(mobile_ua)

        return random.choice(self.ua_pool)
    
    def enable_ua_pool(self, enabled: bool = True, mobile_ratio: float = 0.2):
        """
        启用/禁用 UA 池轮换
        
        Args:
            enabled: 是否启用
            mobile_ratio: Mobile UA 占比
        """
        self.ua_pool_enabled = enabled
        self.ua_mobile_ratio = mobile_ratio
        self.info(f"UA池轮换: {'启用' if enabled else '禁用'}, Mobile占比: {mobile_ratio:.0%}")
    
    def set_ua_pool(self, ua_list: List[str]):
        """设置自定义 UA 池"""
        self.ua_pool = ua_list
        self.info(f"UA池已更新，共 {len(ua_list)} 个UA")
    
    # ==================== 代理管理 ====================
    
    def set_proxy(
        self,
        host: str,
        port: int,
        proxy_type: str = "http",
        username: Optional[str] = None,
        password: Optional[str] = None,
        enabled: bool = True
    ):
        """
        设置代理配置
        
        Args:
            host: 代理主机
            port: 代理端口
            proxy_type: 代理类型 (http, https, socks5)
            username: 认证用户名（可选）
            password: 认证密码（可选）
            enabled: 是否启用
        """
        self.proxy_host = host
        self.proxy_port = port
        self.proxy_type = proxy_type
        self.proxy_username = username
        self.proxy_password = password
        self.proxy_enabled = enabled
        self.info(f"代理设置: {proxy_type}://{host}:{port}")
    
    def disable_proxy(self):
        """禁用代理"""
        self.proxy_enabled = False
        self.info("代理已禁用")
    
    def get_proxy_string(self) -> Optional[str]:
        """获取代理字符串"""
        if not self.proxy_enabled or not self.proxy_host or not self.proxy_port:
            return None
        
        auth = f"{self.proxy_username}:{self.proxy_password}@" if self.proxy_username else ""
        return f"{self.proxy_type}://{auth}{self.proxy_host}:{self.proxy_port}"
    
    # ==================== 指纹伪装 ====================
    
    def set_fingerprint(
        self,
        timezone: Optional[str] = None,
        language: Optional[str] = None,
        screen_resolution: Optional[str] = None,
        platform: Optional[str] = None,
    ):
        """设置指纹参数"""
        if timezone:
            self.fingerprint.timezone = timezone
        if language:
            self.fingerprint.language = language
        if screen_resolution:
            self.fingerprint.screen_resolution = screen_resolution
        if platform:
            self.fingerprint.platform = platform
    
    def enable_fingerprint_randomization(self, enabled: bool = True):
        """启用指纹随机化"""
        self.fingerprint_enabled = enabled
        if enabled:
            self.fingerprint.randomize()
        self.info(f"指纹随机化: {'启用' if enabled else '禁用'}")
    
    # ==================== 延迟控制 ====================
    
    def set_delay(self, min_seconds: float, max_seconds: float, enabled: bool = True):
        """
        设置延迟配置
        
        Args:
            min_seconds: 最小延迟
            max_seconds: 最大延迟
            enabled: 是否启用
        """
        self.delay.min_seconds = min_seconds
        self.delay.max_seconds = max_seconds
        self.delay.enabled = enabled
        self.info(f"延迟控制: {min_seconds:.1f}-{max_seconds:.1f}秒, 启用={enabled}")
    
    def enable_delay(self, enabled: bool = True):
        """启用/禁用延迟"""
        self.delay.enabled = enabled
    
    def wait_delay(self) -> float:
        """执行随机延迟，返回实际等待秒数"""
        return self.delay.wait()
    
    # ==================== Chrome Options ====================
    
    def get_chrome_options(self) -> Options:
        """
        获取 Chrome 配置选项
        
        Returns:
            Options: 配置好的 Chrome 选项
        """
        # 尝试导入 undetected_chromedriver
        use_uc = self.use_undetected_chromedriver
        
        options = Options()
        if self.CHROME_BINARY:
            options.binary_location = self.CHROME_BINARY
        
        if self.headless:
            options.add_argument('--headless=new')  # 新版 headless 模式
        
        # 基础参数
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        # 窗口大小（指纹伪装）
        window_size = self.fingerprint.screen_resolution if self.fingerprint_enabled else f"{self.window_size[0]}x{self.window_size[1]}"
        options.add_argument(f'--window-size={window_size}')
        
        # User-Agent（优先使用随机 UA）
        if self.ua_pool_enabled:
            ua = self.get_random_user_agent()
        else:
            ua = self.user_agent
        options.add_argument(f'user-agent={ua}')
        
        # 代理设置
        if self.proxy_enabled and self.proxy_host and self.proxy_port:
            proxy_str = self.get_proxy_string()
            if proxy_str:
                options.add_argument(f'--proxy-server={proxy_str}')
        
        # 反自动化检测
        if self.disable_automation:
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
        
        # 安全参数
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        
        # 随机化指纹参数
        if self.fingerprint_enabled:
            # 时区
            options.add_argument(f'--timezone={self.fingerprint.timezone}')
            # 语言
            options.add_argument(f'--lang={self.fingerprint.language}')
            # Platform
            options.add_experimental_option(
                'excludeSwitches', 
                ['enable-logging', 'disable-client-side-phishing-detection']
            )
        
        return options
    
    def get_fingerprint_script(self) -> str:
        """
        获取指纹伪装 JavaScript 脚本
        用于在页面加载后注入，进一步修改浏览器指纹
        
        Returns:
            JavaScript 代码字符串
        """
        fp = self.fingerprint
        
        # Canvas 噪声脚本
        canvas_script = ""
        if fp.canvas_noise:
            noise_key = random.choice(fp.CANVAS_NOISE_DATA)
            canvas_script = f"""
// Canvas 指纹噪声
const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;

HTMLCanvasElement.prototype.toDataURL = function() {{
    const ctx = this.getContext('2d');
    if (ctx) {{
        ctx.globalCompositeOperation = 'multiply';
        ctx.fillStyle = '{noise_key}';
        ctx.fillRect(0, 0, this.width, this.height);
    }}
    return originalToDataURL.apply(this, arguments);
}};
"""
        
        # WebGL 噪声脚本
        webgl_script = ""
        if fp.webgl_noise:
            renderer = random.choice(fp.WEBGL_RENDERERS)
            vendor = random.choice(fp.WEBGL_VENDORS)
            webgl_script = f"""
// WebGL 指纹伪装
const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
const originalGetExtension = WebGLRenderingContext.prototype.getExtension;

WebGLRenderingContext.prototype.getParameter = function(param) {{
    if (param === 37445) return '{vendor}';
    if (param === 37446) return '{renderer}';
    return originalGetParameter.apply(this, arguments);
}};
"""
        
        # Timezone 脚本
        timezone_script = f"""
// Timezone 伪装
const originalGetTimezoneOffset = Date.prototype.getTimezoneOffset;
const timezoneOffset = {fp.get_timezone_offset()};
Date.prototype.getTimezoneOffset = function() {{
    return timezoneOffset;
}};
Object.defineProperty(Date.prototype, 'getTimezoneOffset', {{
    value: Date.prototype.getTimezoneOffset,
    writable: true
}});
"""
        
        # 合并所有脚本
        full_script = f"""
(function() {{
    {canvas_script}
    {webgl_script}
    {timezone_script}
    
    // 移除 navigator.webdriver
    Object.defineProperty(navigator, 'webdriver', {{
        get: function() {{ return false; }}
    }});
    
    // 伪装 plugins
    Object.defineProperty(navigator, 'plugins', {{
        get: function() {{
            return [
                {{ name: 'Chrome PDF Plugin', description: 'Portable Document Format', filename: 'internal-pdf-viewer' }},
                {{ name: 'Chrome PDF Viewer', description: '', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' }},
                {{ name: 'Native Client', description: '', filename: 'internal-nacl-plugin' }}
            ];
        }}
    }});
    
    // 伪装 languages
    Object.defineProperty(navigator, 'languages', {{
        get: function() {{ return ['{fp.language}', 'zh-CN', 'zh', 'en-US', 'en']; }}
    }});
}})();
"""
        return full_script
    
    # ==================== 基础配置方法 ====================
    
    def set_headless(self, headless: bool):
        """设置是否无头模式"""
        self.headless = headless
    
    def set_window_size(self, width: int, height: int):
        """设置窗口大小"""
        self.window_size = (width, height)
    
    def use_undetected_uc(self, enabled: bool = True):
        """启用 undetected-chromedriver"""
        self.use_undetected_chromedriver = enabled
        self.info(f"undetected-chromedriver: {'启用' if enabled else '禁用'}")
    
    # ==================== 日志方法 ====================
    
    def info(self, message: str):
        """记录 Info 日志"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """记录 Warning 日志"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """记录 Error 日志"""
        self.logger.error(message)
    
    def debug(self, message: str):
        """记录 Debug 日志"""
        self.logger.debug(message)

    # ==================== 浏览器工厂 ====================

    def create_browser(self, use_playwright: bool = False):
        """
        创建浏览器实例（工厂方法）

        Args:
            use_playwright: 是否使用 Playwright（默认 False，使用 Selenium）

        Returns:
            Browser 或 BrowserPlaywright 实例

        Phase D: Playwright 替换 Selenium
        """
        if use_playwright:
            from browser_playwright import BrowserPlaywright
            return BrowserPlaywright(headless=self.headless, config=self)
        else:
            from browser import Browser
            return Browser(headless=self.headless, config=self)


# ==================== 全局单例访问函数 ====================

_config: Optional[BrowserConfig] = None

def get_config() -> BrowserConfig:
    """获取配置单例"""
    global _config
    if _config is None:
        _config = BrowserConfig()
    return _config


def get_logger():
    """获取日志器"""
    return get_config().logger


# ==================== 便捷函数 ====================

def random_delay(min_seconds: float = 3, max_seconds: float = 8) -> float:
    """
    随机延迟函数（兼容旧代码）
    
    Args:
        min_seconds: 最小秒数
        max_seconds: 最大秒数
        
    Returns:
        实际等待秒数
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay


# ==================== 测试代码 ====================

if __name__ == "__main__":
    config = BrowserConfig()
    
    print("=== BrowserConfig Phase 4 测试 ===\n")
    
    # 测试 UA 池
    print("1. UA池测试:")
    config.enable_ua_pool(enabled=True, mobile_ratio=0.3)
    for i in range(5):
        ua = config.get_random_user_agent()
        print(f"   [{i+1}] {ua[:60]}...")
    
    # 测试代理设置
    print("\n2. 代理设置测试:")
    config.set_proxy("127.0.0.1", 7890, "http")
    print(f"   代理字符串: {config.get_proxy_string()}")
    
    # 测试指纹
    print("\n3. 指纹配置测试:")
    config.set_fingerprint(
        timezone="America/New_York",
        language="en-US",
        screen_resolution="2560x1440"
    )
    print(f"   时区: {config.fingerprint.timezone}")
    print(f"   语言: {config.fingerprint.language}")
    print(f"   屏幕: {config.fingerprint.screen_resolution}")
    print(f"   时区偏移: {config.fingerprint.get_timezone_offset()}分钟")
    
    # 测试指纹随机化
    print("\n4. 指纹随机化测试:")
    config.enable_fingerprint_randomization(enabled=True)
    print(f"   时区: {config.fingerprint.timezone}")
    print(f"   语言: {config.fingerprint.language}")
    
    # 测试延迟配置
    print("\n5. 延迟配置测试:")
    config.set_delay(min_seconds=1, max_seconds=3, enabled=True)
    print(f"   延迟范围: {config.delay.min_seconds}-{config.delay.max_seconds}秒")
    
    # 测试 Chrome Options
    print("\n6. Chrome Options 测试:")
    opts = config.get_chrome_options()
    print(f"   headless: {config.headless}")
    print(f"   UA: {config.user_agent[:50]}...")
    
    # 测试指纹脚本
    print("\n7. 指纹脚本测试:")
    script = config.get_fingerprint_script()
    print(f"   脚本长度: {len(script)} 字符")
    
    print("\n=== 测试完成 ===")
