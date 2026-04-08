#!/usr/bin/env python3
"""
core/exceptions.py - 统一异常定义
"""


class BrowserBotException(Exception):
    """浏览器机器人基础异常"""

    def __init__(self, message: str = "", details: str = ""):
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self):
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class BrowserInitError(BrowserBotException):
    """浏览器初始化失败"""
    pass


class ElementNotFoundError(BrowserBotException):
    """元素未找到"""
    pass


class LoginError(BrowserBotException):
    """登录失败"""
    pass


class CookieError(BrowserBotException):
    """Cookie操作失败"""
    pass


class CaptchaError(BrowserBotException):
    """验证码识别失败"""
    pass


class AccountError(BrowserBotException):
    """账号操作失败"""
    pass


class ConfigError(BrowserBotException):
    """配置错误"""
    pass


class ValidationError(BrowserBotException):
    """数据验证失败"""
    pass
