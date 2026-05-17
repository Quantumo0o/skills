#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件工具模块 - 订单读写和配置管理
"""

import os
import json
import hashlib
import platform


def get_orders_dir():
    """获取订单存储目录"""
    home_dir = os.path.expanduser("~")
    if platform.system() == "Windows":
        return os.path.join(home_dir, "openclaw", "skills", "orders")
    else:
        return os.path.join(home_dir, ".openclaw", "skills", "orders")


def get_config_path():
    """获取配置文件路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, '..', 'configs', 'config.json')


def load_config() -> dict:
    """加载配置文件"""
    config_path = get_config_path()
    
    # 如果配置文件不存在，创建默认配置
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        default_config = {
            "payTo": "",
            "amount": 1,
            "skillName": "baby-name",
            "description": "宝宝取名服务费用"
        }
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        return default_config
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_order(indicator: str, order_no: str, order_data: dict):
    """保存订单文件"""
    orders_dir = os.path.join(get_orders_dir(), indicator)
    os.makedirs(orders_dir, exist_ok=True)
    
    order_file = os.path.join(orders_dir, f'{order_no}.json')
    with open(order_file, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, ensure_ascii=False, indent=2)


def load_order(indicator: str, order_no: str) -> dict:
    """加载订单文件"""
    order_file = os.path.join(get_orders_dir(), indicator, f'{order_no}.json')
    
    if not os.path.exists(order_file):
        raise FileNotFoundError(f"订单文件不存在: {order_no}")
    
    with open(order_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def compute_indicator(skill_name: str) -> str:
    """计算indicator (MD5 hash of skill name)"""
    return hashlib.md5(skill_name.encode('utf-8')).hexdigest()
