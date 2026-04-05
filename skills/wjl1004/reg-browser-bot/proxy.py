#!/usr/bin/env python3
"""
代理管理器模块
支持 HTTP/HTTPS/SOCKS5 代理池配置和自动切换
"""

import random
import logging
from typing import Optional, List, Dict
from dataclasses import dataclass
from enum import Enum


class ProxyType(Enum):
    """代理类型"""
    HTTP = "http"
    HTTPS = "https"
    SOCKS5 = "socks5"


@dataclass
class Proxy:
    """代理配置"""
    host: str
    port: int
    proxy_type: ProxyType = ProxyType.HTTP
    username: Optional[str] = None
    password: Optional[str] = None
    enabled: bool = True
    
    def __str__(self) -> str:
        auth = f"{self.username}:{self.password}@" if self.username else ""
        return f"{self.proxy_type.value}://{auth}{self.host}:{self.port}"
    
    def to_dict(self) -> dict:
        return {
            "host": self.host,
            "port": self.port,
            "type": self.proxy_type.value,
            "username": self.username,
            "password": self.password,
            "enabled": self.enabled
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Proxy':
        return cls(
            host=data["host"],
            port=data["port"],
            proxy_type=ProxyType(data.get("type", "http")),
            username=data.get("username"),
            password=data.get("password"),
            enabled=data.get("enabled", True)
        )


class ProxyManager:
    """
    代理管理器
    支持代理池配置、自动切换、失败标记
    """
    
    def __init__(self, proxy_list: Optional[List[Dict]] = None):
        """
        初始化代理管理器
        
        Args:
            proxy_list: 代理配置列表，格式:
                [
                    {"host": "127.0.0.1", "port": 7890, "type": "http"},
                    {"host": "127.0.0.1", "port": 7891, "type": "socks5", "username": "user", "password": "pass"}
                ]
        """
        self.logger = logging.getLogger("ProxyManager")
        self.proxies: List[Proxy] = []
        self.current_index: int = 0
        self.failed_proxies: set = set()  # 存储失败代理的索引
        
        if proxy_list:
            for p in proxy_list:
                self.add_proxy(Proxy.from_dict(p))
        
        self.logger.info(f"代理管理器初始化，共 {len(self.proxies)} 个代理")
    
    def add_proxy(self, proxy: Proxy) -> None:
        """添加代理"""
        self.proxies.append(proxy)
        self.logger.debug(f"添加代理: {proxy}")
    
    def add_proxy_from_dict(self, proxy_dict: dict) -> None:
        """从字典添加代理"""
        self.add_proxy(Proxy.from_dict(proxy_dict))
    
    def get_proxy(self) -> Optional[Proxy]:
        """
        获取当前代理
        
        Returns:
            Proxy 或 None（无可用代理）
        """
        if not self.proxies:
            return None
        
        # 尝试找到一个可用的代理
        available = [i for i, p in enumerate(self.proxies) 
                     if p.enabled and i not in self.failed_proxies]
        
        if not available:
            self.logger.warning("所有代理都不可用，将使用默认代理")
            return self.proxies[self.current_index % len(self.proxies)]
        
        # 轮换到下一个可用代理
        for _ in range(len(available)):
            self.current_index = self.current_index % len(self.proxies)
            if self.current_index in available:
                return self.proxies[self.current_index]
            self.current_index += 1
        
        return self.proxies[available[0]]
    
    def get_random_proxy(self) -> Optional[Proxy]:
        """
        随机获取一个可用代理
        
        Returns:
            Proxy 或 None
        """
        if not self.proxies:
            return None
        
        available = [p for i, p in enumerate(self.proxies) 
                     if p.enabled and i not in self.failed_proxies]
        
        if not available:
            self.logger.warning("所有代理都不可用")
            return random.choice(self.proxies) if self.proxies else None
        
        return random.choice(available)
    
    def switch_proxy(self) -> Optional[Proxy]:
        """
        切换到下一个代理
        
        Returns:
            下一个 Proxy 或 None
        """
        if not self.proxies:
            return None
        
        self.current_index = (self.current_index + 1) % len(self.proxies)
        proxy = self.get_proxy()
        
        if proxy:
            self.logger.info(f"切换代理: {proxy}")
        
        return proxy
    
    def mark_proxy_failed(self, proxy: Optional[Proxy] = None) -> None:
        """
        标记当前代理或指定代理为失败
        
        Args:
            proxy: 要标记的代理，None 时标记当前代理
        """
        if proxy is None:
            proxy = self.get_proxy()
        
        if proxy:
            for i, p in enumerate(self.proxies):
                if p == proxy:
                    self.failed_proxies.add(i)
                    self.logger.warning(f"代理失败: {proxy} (索引: {i})")
                    break
    
    def mark_proxy_success(self, proxy: Optional[Proxy] = None) -> None:
        """
        标记代理为成功（从失败列表移除）
        
        Args:
            proxy: 要标记的代理，None 时处理当前代理
        """
        if proxy is None:
            # 获取当前索引对应的代理
            if self.current_index < len(self.proxies):
                proxy = self.proxies[self.current_index]
            else:
                return
        
        for i, p in enumerate(self.proxies):
            if p == proxy and i in self.failed_proxies:
                self.failed_proxies.discard(i)
                self.logger.info(f"代理恢复: {proxy} (索引: {i})")
                break
    
    def reset_failed(self) -> None:
        """重置失败列表"""
        count = len(self.failed_proxies)
        self.failed_proxies.clear()
        self.logger.info(f"已重置失败代理列表 ({count} 个)")
    
    def get_available_count(self) -> int:
        """获取可用代理数量"""
        return len([i for i, p in enumerate(self.proxies) 
                   if p.enabled and i not in self.failed_proxies])
    
    def list_proxies(self) -> List[Dict]:
        """列出所有代理状态"""
        result = []
        for i, p in enumerate(self.proxies):
            status = "OK" if i not in self.failed_proxies else "FAILED"
            result.append({
                "index": i,
                "proxy": str(p),
                "enabled": p.enabled,
                "status": status
            })
        return result
    
    def enable_proxy(self, index: int) -> bool:
        """启用指定索引的代理"""
        if 0 <= index < len(self.proxies):
            self.proxies[index].enabled = True
            return True
        return False
    
    def disable_proxy(self, index: int) -> bool:
        """禁用指定索引的代理"""
        if 0 <= index < len(self.proxies):
            self.proxies[index].enabled = False
            return True
        return False
    
    def get_chrome_proxy_args(self, proxy: Optional[Proxy] = None) -> List[str]:
        """
        获取 Chrome 代理参数
        
        Args:
            proxy: 代理对象，None 时自动获取
            
        Returns:
            Chrome proxy arguments
        """
        if proxy is None:
            proxy = self.get_proxy()
        
        if not proxy:
            return []
        
        proxy_str = f"{proxy.host}:{proxy.port}"
        
        if proxy.username and proxy.password:
            # 需要认证的代理
            return [
                f"--proxy-server={proxy.proxy_type.value}://{proxy_str}",
                f"--proxy-auth={proxy.username}:{proxy.password}"
            ]
        else:
            return [f"--proxy-server={proxy.proxy_type.value}://{proxy_str}"]


# 全局代理管理器实例
_proxy_manager: Optional[ProxyManager] = None

def get_proxy_manager() -> ProxyManager:
    """获取全局代理管理器"""
    global _proxy_manager
    if _proxy_manager is None:
        _proxy_manager = ProxyManager()
    return _proxy_manager

def init_proxy_manager(proxy_list: List[Dict]) -> ProxyManager:
    """初始化代理管理器"""
    global _proxy_manager
    _proxy_manager = ProxyManager(proxy_list)
    return _proxy_manager


if __name__ == "__main__":
    # 测试代码
    logging.basicConfig(level=logging.DEBUG)
    
    # 创建代理管理器
    pm = ProxyManager([
        {"host": "127.0.0.1", "port": 7890, "type": "http"},
        {"host": "127.0.0.1", "port": 7891, "type": "socks5"},
        {"host": "127.0.0.1", "port": 7892, "type": "https", "username": "user", "password": "pass"}
    ])
    
    print("=== 测试代理管理器 ===")
    print(f"可用代理数: {pm.get_available_count()}")
    
    # 获取当前代理
    proxy = pm.get_proxy()
    print(f"当前代理: {proxy}")
    
    # 列出所有代理
    print("\n所有代理:")
    for p in pm.list_proxies():
        print(f"  [{p['index']}] {p['proxy']} - {p['status']}")
    
    # 切换代理
    print("\n切换测试:")
    for i in range(4):
        proxy = pm.switch_proxy()
        print(f"  切换到: {proxy}")
    
    # 标记失败
    print("\n标记失败测试:")
    pm.mark_proxy_failed()
    print(f"  失败后可用: {pm.get_available_count()}")
    
    # Chrome 参数测试
    print("\nChrome 代理参数:")
    proxy = pm.get_proxy()
    args = pm.get_chrome_proxy_args(proxy)
    print(f"  {args}")
