#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Voxel (Occupancy-inspired)
===================================
借鉴特斯拉的 Occupancy Network (占用网络)。
放弃存储原始数据，改为计算"空间是否被占据、状态是什么"的张量表示。

功能：
1. 扫描 L1 节点，按时间窗或类型聚合为"语义体素 (Voxel)"。
2. 输出轻量化的 State Tensor (状态特征)。
3. 用于 Agent 快速获取环境/系统的"当前状态快照"，而无需遍历海量日志。

核心逻辑：
- 遍历 nodes/*.json
- 计算各类别的密度 (Density)
- 计算最新状态 (State)
- 计算活跃度 (Activity)
"""

import json
import os
import glob
import time
from collections import Counter, defaultdict

class SemanticVoxel:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.nodes_dir = os.path.join(data_dir, "nodes")
        self.voxel_map = defaultdict(dict) # 按类别或时间窗存储体素

    def scan_and_aggregate(self, window_hours: int = 24) -> dict:
        """
        扫描节点并生成体素。
        
        Returns:
            Dict[str, dict] -> { category: { density, latest_state, active_count } }
        """
        if not os.path.exists(self.nodes_dir):
            return {}

        # 过滤最近的节点 (模拟短期记忆窗口)
        cutoff_time = time.time() - (window_hours * 3600)
        
        categories = defaultdict(list)
        
        node_files = glob.glob(os.path.join(self.nodes_dir, "*.json"))
        
        recent_count = 0
        for f in node_files:
            try:
                # 快速读取元数据
                with open(f, 'r') as fh:
                    node = json.load(fh)
                
                created_at = node.get("created_at", 0)
                if created_at >= cutoff_time:
                    n_type = node.get("node_type", "unknown")
                    categories[n_type].append(node)
                    recent_count += 1
            except Exception:
                continue

        # 生成体素
        voxels = {}
        for n_type, nodes in categories.items():
            # 密度 (Density)
            density = len(nodes)
            
            # 活跃度 (Activity - 假设有 tag 或 content 长度作为指标)
            avg_len = sum(len(str(n.get("content", ""))) for n in nodes) / len(nodes) if nodes else 0
            
            # 最新状态 (Latest State - 取最新节点的摘要)
            latest_node = max(nodes, key=lambda x: x.get("created_at", 0))
            latest_summary = f"Latest: {latest_node.get('id')} ({latest_node.get('node_type')})"
            
            voxels[n_type] = {
                "density": density,
                "activity_score": avg_len,
                "latest_state": latest_summary,
                "window_hours": window_hours
            }

        # 全局系统状态体素
        voxels["SYSTEM_STATE"] = {
            "total_recent_nodes": recent_count,
            "status": "ACTIVE" if recent_count > 0 else "IDLE",
            "timestamp": time.time()
        }

        return voxels

if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    
    voxel = SemanticVoxel(data_path)
    voxels = voxel.scan_and_aggregate(window_hours=48) # 查看过去 48 小时
    
    print("📊 语义体素状态快照 (Semantic Voxel Snapshot):")
    print("-" * 40)
    for category, state in voxels.items():
        print(f"📦 [{category}]:")
        for k, v in state.items():
            if isinstance(v, float) and k != "timestamp":
                print(f"   {k}: {v:.2f}")
            else:
                print(f"   {k}: {v}")
