#!/usr/bin/env python3
"""
🚀 Phase 1: 语义占据检索器 (Semantic Occupancy Retriever)
================================================
核心理念：借鉴特斯拉 Occupancy Network，将离散记忆节点映射为连续语义场。
解决问题：起点发现错误 (Transcription Failure)

机制：
1. 亲和力评分 (Affinity Score): 结合 TF-IDF, Jaccard, 节点中心性。
2. 能量扩散 (Energy Diffusion): 高亲和力节点激活其邻居，形成“语义占据块”。
3. 多启动子候选 (Multi-Promoter): 返回 Top-K 潜在起点，而非单一 Top-1。
"""

import math
import re
from collections import defaultdict
from typing import List, Dict, Tuple, Set

class OccupancyRetriever:
    def __init__(self, nodes: Dict, adj: Dict[str, List[str]]):
        self.nodes = nodes
        self.adj = adj
        self.inv_index = defaultdict(set)
        self.idf = defaultdict(float)
        self.page_rank = self._calculate_pagerank()
        self._build_index()
    
    def _build_index(self):
        N = len(self.nodes)
        doc_freq = defaultdict(int)
        
        for nid, node in self.nodes.items():
            text = f"{node.get('content', '')} {' '.join(node.get('tags', []))}".lower()
            tokens = set(re.findall(r'[\u4e00-\u9fff]{2,}|[a-zA-Z0-9]{3,}', text))
            for t in tokens:
                self.inv_index[t].add(nid)
                doc_freq[t] += 1
        
        for t, df in doc_freq.items():
            self.idf[t] = math.log((N + 1) / (df + 1)) + 1

    def _calculate_pagerank(self, damping=0.85, iterations=10):
        nodes_list = list(self.nodes.keys())
        pr = {n: 1.0 / len(nodes_list) for n in nodes_list}
        
        for _ in range(iterations):
            new_pr = {n: (1 - damping) / len(nodes_list) for n in nodes_list}
            for node in nodes_list:
                neighbors = self.adj.get(node, [])
                if not neighbors: continue
                share = pr[node] / len(neighbors)
                for neighbor in neighbors:
                    if neighbor in new_pr:
                        new_pr[neighbor] += damping * share
            pr = new_pr
        return pr

    def query_occupancy(self, keywords: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        查询语义占据空间
        返回: List of (NodeID, AffinityScore) 按得分降序排列
        """
        scores = defaultdict(float)
        kws = [k.lower() for k in keywords]
        
        # 1. 关键词匹配 (TF-IDF 加权)
        for kw in kws:
            # 精确匹配
            for token, nids in self.inv_index.items():
                if kw in token or token in kw:
                    idf_val = self.idf.get(token, 1.0)
                    for nid in nids:
                        scores[nid] += idf_val * 1.5  # 匹配权重
            
            # 模糊/字面匹配 (降级权重)
            for nid, node in self.nodes.items():
                content = node.get('content', '').lower()
                tags = " ".join(node.get('tags', [])).lower()
                if kw in content or kw in tags:
                    scores[nid] += self.idf.get(kw, 1.0) * 0.5

        # 2. 拓扑增强 (中心性加成)
        for nid in scores:
            scores[nid] *= (1.0 + self.page_rank.get(nid, 0.0))

        # 3. 邻居能量扩散 (Occupancy Spread)
        # 高得分节点会将其部分能量传递给邻居，填补局部空白
        spread_scores = defaultdict(float)
        spread_factor = 0.2
        
        for nid, score in scores.items():
            spread_scores[nid] += score  # 自身保留
            for neighbor in self.adj.get(nid, []):
                spread_scores[neighbor] += score * spread_factor
        
        # 排序
        ranked = sorted(spread_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def retrieve(self, keywords: List[str], top_k: int = 10) -> List[str]:
        ranked = self.query_occupancy(keywords, top_k)
        return [nid for nid, score in ranked]
