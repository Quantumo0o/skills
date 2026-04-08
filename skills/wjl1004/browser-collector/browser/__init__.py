"""
browser/ - 浏览器自动化模块
"""

from browser.playwright import BrowserPlaywright, slider_drag, slider_drag_slow
from browser.captcha import CaptchaSolver, SliderCaptcha

__all__ = [
    'BrowserPlaywright',
    'slider_drag',
    'slider_drag_slow',
    'CaptchaSolver',
    'SliderCaptcha',
]
