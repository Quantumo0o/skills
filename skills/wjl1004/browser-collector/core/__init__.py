"""
core/ - browser-collector 核心模块
"""

from core.config import BrowserConfig, get_config
from core.exceptions import (
    BrowserBotException,
    BrowserInitError,
    ElementNotFoundError,
    LoginError,
    CookieError,
    CaptchaError,
    AccountError,
    ConfigError,
    ValidationError,
)

__all__ = [
    'BrowserConfig',
    'get_config',
    'BrowserBotException',
    'BrowserInitError',
    'ElementNotFoundError',
    'LoginError',
    'CookieError',
    'CaptchaError',
    'AccountError',
    'ConfigError',
    'ValidationError',
]
