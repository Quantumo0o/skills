#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Predictive Planner (MPC-inspired)
=================================
借鉴特斯拉的 MPC (模型预测控制)。
通过分析历史图谱边 (Edges) 的转移概率，预测 Agent 的"下一步"需求。

功能：
1. 计算节点间的马尔可夫转移概率。
2. 给定当前节点，预测 Top-K 下一个可能访问的节点。
3. 提前触发"预热" (Prefetching)，将预测节点加载到热缓存。

核心逻辑：
- 读取 edges.json
- 构建 Adjacency Matrix (带权重)
- 计算 P(Next | Current)
"""

import json
import os
import sys
from collections import defaultdict, Counter

class PredictivePlanner:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.transitions = defaultdict(list) # source -> [target, target...]
        self._load_history()

    def _load_history(self):
        """加载历史边数据，构建转移记录"""
        edges_file = os.path.join(self.data_dir, "edges", "edges.json")
        if not os.path.exists(edges_file):
            return

        with open(edges_file, 'r') as f:
            try:
                data = json.load(f)
                # v5 edges.json format: { "EDGE-ID": { ... }, ... }
                for edge_id, edge in data.items():
                    src = edge.get("source")
                    tgt = edge.get("target")
                    if src and tgt:
                        self.transitions[src].append(tgt)
            except json.JSONDecodeError:
                pass

    def predict_next(self, current_node_id: str, top_k: int = 3) -> list:
        """
        预测从当前节点出发，最可能的 K 个后续节点。
        类似于自动驾驶预测车辆轨迹。
        
        Returns:
            List of {"node_id": str, "probability": float}
        """
        targets = self.transitions.get(current_node_id, [])
        
        if not targets:
            return []

        # 计算概率
        counts = Counter(targets)
        total = len(targets)
        probs = [{"node_id": t, "probability": c / total} for t, c in counts.most_common(top_k)]
        
        return probs

    def get_transition_map(self) -> dict:
        """获取完整的转移概率映射"""
        result = {}
        for src, tgts in self.transitions.items():
            counts = Counter(tgts)
            total = len(tgts)
            result[src] = {t: c / total for t, c in counts.items()}
        return result

if __name__ == "__main__":
    # 独立测试
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # 指向真实数据
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    
    planner = PredictivePlanner(data_path)
    print(f"✅ 已加载 {len(planner.transitions)} 个节点的转移记录")
    
    if planner.transitions:
        test_node = list(planner.transitions.keys())[0]
        preds = planner.predict_next(test_node, top_k=3)
        print(f"🎯 从节点 [{test_node}] 出发的预测路径:")
        for p in preds:
            print(f"   -> {p['node_id']} (概率: {p['probability']:.2f})")
