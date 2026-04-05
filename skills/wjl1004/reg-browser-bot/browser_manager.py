#!/usr/bin/env python3
"""
browser_manager.py - 浏览器管理器单例

Phase 5 新增:
- 引用计数管理浏览器生命周期
- 支持多Profile隔离（不同账号用不同浏览器实例）
- 全局共享复用，避免资源浪费
"""

import threading
import logging
from typing import Optional, Dict

from browser import Browser
from browser_config import BrowserConfig, get_config
from exceptions import BrowserInitError


class BrowserManager:
    """
    浏览器管理器 - 单例模式，全局共享
    
    功能：
    - 引用计数管理浏览器生命周期
    - 支持多Profile隔离（不同账号用不同浏览器实例）
    - 全局共享复用，避免重复初始化
    """
    
    _instance: Optional['BrowserManager'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # 双重检查锁定
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._browsers: Dict[str, Browser] = {}
                    cls._instance._ref_counts: Dict[str, int] = {}
                    cls._instance._browser_configs: Dict[str, BrowserConfig] = {}
                    cls._instance._init_lock = threading.Lock()
                    cls._instance._logger = logging.getLogger(cls.__name__)
        return cls._instance
    
    def __init__(self):
        """初始化（幂等）"""
        pass
    
    @classmethod
    def get_instance(cls) -> 'BrowserManager':
        """获取单例实例"""
        return cls()
    
    def get_browser(self, profile_id: str = "default", 
                    headless: Optional[bool] = None,
                    config: Optional[BrowserConfig] = None) -> Browser:
        """
        获取浏览器实例（引用计数管理）
        
        Args:
            profile_id: Profile标识符，用于隔离不同账号/任务
            headless: 是否使用无头模式，None时使用配置默认值
            config: 配置对象，None时使用全局单例
            
        Returns:
            Browser: 浏览器实例
            
        Note:
            每次调用 get_browser 后，必须在不再使用时调用 release_browser
        """
        with self._init_lock:
            # 初始化该profile的引用计数
            if profile_id not in self._ref_counts:
                self._ref_counts[profile_id] = 0
                self._browser_configs[profile_id] = config or get_config()
            
            # 如果浏览器不存在或已关闭，创建新的
            if profile_id not in self._browsers or self._browsers[profile_id] is None:
                try:
                    cfg = self._browser_configs[profile_id]
                    # 临时覆盖 headless 设置
                    if headless is not None:
                        original_headless = cfg.headless
                        cfg.set_headless(headless)
                        browser = Browser(headless=headless, config=cfg)
                        cfg.set_headless(original_headless)
                    else:
                        browser = Browser(config=cfg)
                    self._browsers[profile_id] = browser
                    self._logger.info(f"创建浏览器实例 (profile={profile_id})")
                except BrowserInitError as e:
                    self._logger.error(f"创建浏览器失败 (profile={profile_id}): {e}")
                    raise
            
            # 增加引用计数
            self._ref_counts[profile_id] += 1
            self._logger.debug(f"获取浏览器 (profile={profile_id}, ref={self._ref_counts[profile_id]})")
            
            return self._browsers[profile_id]
    
    def release_browser(self, profile_id: str = "default") -> bool:
        """
        释放浏览器（引用计数归零时关闭）
        
        Args:
            profile_id: Profile标识符
            
        Returns:
            bool: 是否成功
        """
        with self._init_lock:
            if profile_id not in self._ref_counts:
                self._logger.warning(f"尝试释放未分配的浏览器 (profile={profile_id})")
                return False
            
            # 减少引用计数
            self._ref_counts[profile_id] = max(0, self._ref_counts[profile_id] - 1)
            self._logger.debug(f"释放浏览器 (profile={profile_id}, ref={self._ref_counts[profile_id]})")
            
            # 引用计数归零时关闭浏览器
            if self._ref_counts[profile_id] == 0:
                self._close_browser_internal(profile_id)
            
            return True
    
    def _close_browser_internal(self, profile_id: str):
        """内部方法：关闭指定profile的浏览器"""
        if profile_id in self._browsers and self._browsers[profile_id] is not None:
            try:
                self._browsers[profile_id].close()
                self._logger.info(f"关闭浏览器 (profile={profile_id})")
            except Exception as e:
                self._logger.warning(f"关闭浏览器时出错 (profile={profile_id}): {e}")
            finally:
                self._browsers[profile_id] = None
    
    def close_browser(self, profile_id: str = "default") -> bool:
        """
        强制关闭指定profile的浏览器（立即关闭，不等引用计数）
        
        Args:
            profile_id: Profile标识符
            
        Returns:
            bool: 是否成功
        """
        with self._init_lock:
            self._ref_counts[profile_id] = 0
            self._close_browser_internal(profile_id)
            return True
    
    def close_all(self) -> int:
        """
        关闭所有浏览器
        
        Returns:
            int: 关闭的浏览器数量
        """
        with self._init_lock:
            count = 0
            profile_ids = list(self._browsers.keys())
            for profile_id in profile_ids:
                if self._browsers.get(profile_id) is not None:
                    self._close_browser_internal(profile_id)
                    count += 1
            self._logger.info(f"关闭了 {count} 个浏览器")
            return count
    
    def get_ref_count(self, profile_id: str = "default") -> int:
        """
        获取指定profile的引用计数
        
        Args:
            profile_id: Profile标识符
            
        Returns:
            int: 引用计数，未分配则返回 -1
        """
        return self._ref_counts.get(profile_id, -1)
    
    def get_active_profiles(self) -> list:
        """
        获取所有活跃的profile列表
        
        Returns:
            list: 活跃profile列表
        """
        return [pid for pid, browser in self._browsers.items() 
                if browser is not None]
    
    def is_browser_alive(self, profile_id: str = "default") -> bool:
        """
        检查浏览器是否存活
        
        Args:
            profile_id: Profile标识符
            
        Returns:
            bool: 浏览器是否存活
        """
        browser = self._browsers.get(profile_id)
        if browser is None or browser.driver is None:
            return False
        try:
            # 尝试获取当前URL，如果浏览器已关闭会抛异常
            _ = browser.current_url
            return True
        except Exception:
            return False


class BrowserContext:
    """
    浏览器上下文管理器（自动管理引用计数）
    
    用法:
        with BrowserContext("account1") as browser:
            browser.navigate("https://example.com")
        # 离开 with 块时自动 release
    """
    
    def __init__(self, profile_id: str = "default", 
                 headless: Optional[bool] = None,
                 config: Optional[BrowserConfig] = None):
        self.profile_id = profile_id
        self.headless = headless
        self.config = config
        self.browser: Optional[Browser] = None
        self._manager = BrowserManager.get_instance()
    
    def __enter__(self) -> Browser:
        self.browser = self._manager.get_browser(
            self.profile_id, 
            self.headless, 
            self.config
        )
        return self.browser
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._manager.release_browser(self.profile_id)
        return False


def get_browser_manager() -> BrowserManager:
    """获取浏览器管理器单例"""
    return BrowserManager.get_instance()
