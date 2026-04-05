#!/usr/bin/env python3
"""
reg-browser-bot - 浏览器自动化工具包

统一模块导出
Phase 5 版本新增：BrowserManager 单例、Pipeline 流水线、TaskScheduler 调度器、数据模型

向后兼容性：Phase 1-4 的所有导出保持不变
"""

from browser_config import BrowserConfig, get_config
from exceptions import (
    BrowserBotException,
    BrowserInitError,
    ElementNotFoundError,
    LoginError,
    CookieError,
    CaptchaError,
    AccountError,
    ConfigError,
    ValidationError
)
from browser import Browser
from captcha import CaptchaSolver
from collector import DataCollector
from account import AccountManager
from poster import AutoPoster

# Phase 5 新增模块
from browser_manager import BrowserManager, BrowserContext, get_browser_manager
from pipeline import (
    Pipeline,
    PipelineState,
    PipelineResult,
    LoginPipeline,
    CollectPipeline,
    PostPipeline,
    create_pipeline,
)
from task_scheduler import (
    TaskScheduler,
    ScheduledTask,
    TriggerType,
    get_scheduler,
    schedule_task,
    remove_scheduled_task,
    start_scheduler,
    stop_scheduler,
)
from models import (
    Account,
    Task,
    CollectedData,
    CaptchaRecord,
    Proxy,
    PipelineExecution,
    DatabaseManager,
    get_database,
)

__all__ = [
    # ========== Phase 1-4 配置 ==========
    'BrowserConfig',
    'get_config',
    # ========== Phase 1-4 异常 ==========
    'BrowserBotException',
    'BrowserInitError',
    'ElementNotFoundError',
    'LoginError',
    'CookieError',
    'CaptchaError',
    'AccountError',
    'ConfigError',
    'ValidationError',
    # ========== Phase 1-4 核心类 ==========
    'Browser',
    'CaptchaSolver',
    'DataCollector',
    'AccountManager',
    'AutoPoster',
    # ========== Phase 5 浏览器管理 ==========
    'BrowserManager',
    'BrowserContext',
    'get_browser_manager',
    # ========== Phase 5 流水线 ==========
    'Pipeline',
    'PipelineState',
    'PipelineResult',
    'LoginPipeline',
    'CollectPipeline',
    'PostPipeline',
    'create_pipeline',
    # ========== Phase 5 任务调度 ==========
    'TaskScheduler',
    'ScheduledTask',
    'TriggerType',
    'get_scheduler',
    'schedule_task',
    'remove_scheduled_task',
    'start_scheduler',
    'stop_scheduler',
    # ========== Phase 5 数据模型 ==========
    'Account',
    'Task',
    'CollectedData',
    'CaptchaRecord',
    'Proxy',
    'PipelineExecution',
    'DatabaseManager',
    'get_database',
]

__version__ = '5.0.0'
