#!/usr/bin/env python3
"""
collectors/registry.py - 采集器自动发现机制
"""

import os
import sys
import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Type, List, Optional, Any

# 全局注册表
_COLLECTOR_REGISTRY: Dict[str, Type] = {}


def register_collector(name: str):
    """装饰器：注册采集器"""
    def decorator(cls):
        _COLLECTOR_REGISTRY[name] = cls
        return cls
    return decorator


def get_collector(name: str, **kwargs) -> Optional[Any]:
    """获取已注册的采集器实例"""
    cls = _COLLECTOR_REGISTRY.get(name)
    if cls is None:
        return None
    return cls(**kwargs)


def list_collectors() -> List[str]:
    """列出所有已注册的采集器名称"""
    return list(_COLLECTOR_REGISTRY.keys())


def auto_discover(builtin_dir: Path, plugins_dir: Optional[Path] = None):
    """
    自动发现并加载采集器

    扫描 builtin/ 和 plugins/ 目录，导入所有 .py 文件
    """
    discovered = []

    # 扫描 builtin 目录
    if builtin_dir.exists():
        for _, name, _ in pkgutil.iter_modules([str(builtin_dir)]):
            if name in ('__init__', '__pycache__'):
                continue
            try:
                module = importlib.import_module(f'collectors.builtin.{name}')
                discovered.append(name)
            except Exception as e:
                print(f"Warning: failed to import {name}: {e}")

    # 扫描 plugins 目录（可选）
    if plugins_dir and plugins_dir.exists():
        plugin_path = str(plugins_dir)
        if plugin_path not in sys.path:
            sys.path.insert(0, plugin_path)
        for _, name, _ in pkgutil.iter_modules([plugin_path]):
            if name.startswith('_') or name in discovered:
                continue
            try:
                module = importlib.import_module(name)
                discovered.append(name)
            except Exception as e:
                print(f"Warning: failed to import plugin {name}: {e}")

    return discovered


def load_builtin_collectors():
    """显式导入所有内置采集器"""
    from collectors.builtin import eastmoney, xueqiu
    return ['eastmoney', 'xueqiu']
