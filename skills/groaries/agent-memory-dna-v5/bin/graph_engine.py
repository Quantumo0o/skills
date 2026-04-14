#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Memory DNA v5 — 图谱关联引擎 (Graph Engine)
==================================================
核心功能:
- 显式图谱边管理 (替代向量相似度)
- 确定性路径查询 (非概率匹配)
- 边权重动态调整 (调用正确率驱动)
- 路径完整性校验 (负反馈拦截)
"""

import json
import os
import time
from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False


@dataclass
class GraphEdge:
    """显式图谱边"""
    id: str                     # EDGE-SEQ
    source: str                 # 源节点ID
    target: str                 # 目标节点ID
    edge_type: str              # 边类型: triggers/validates/causes/belongs_to/depends_on/conflicts_with
    weight: float = 1.0        # 边权重 (初始1.0, 随调用正确率调整)
    created_at: float = 0.0    # 创建时间
    call_count: int = 0        # 调用次数
    success_count: int = 0     # 成功次数
    metadata: dict = None      # 附加元数据

    def __post_init__(self):
        if self.created_at == 0:
            self.created_at = time.time()
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "GraphEdge":
        return cls(**d)


class GraphEngine:
    """图谱关联引擎"""

    # 合法的边类型
    VALID_EDGE_TYPES = {
        "triggers",        # A 触发 B
        "validates",       # A 校验通过 B
        "causes",          # A 导致 B
        "belongs_to",      # A 属于 B
        "depends_on",      # A 依赖 B
        "conflicts_with",  # A 与 B 冲突
        "references",      # A 引用 B
        "replaces",        # A 替代 B
        "precedes",        # A 在 B 之前
    }

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = Path(data_dir)
        self.edges_dir = self.data_dir / "edges"
        self.edges_dir.mkdir(parents=True, exist_ok=True)

        # 内存图
        if HAS_NETWORKX:
            self._graph = nx.DiGraph()
        else:
            self._graph = None

        # 边索引
        self._edges: dict[str, GraphEdge] = {}
        self._load_edges()

    def _load_edges(self):
        """从磁盘加载所有边"""
        edge_file = self.edges_dir / "edges.json"
        if edge_file.exists():
            try:
                with open(edge_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for edge_id, edge_data in data.items():
                        edge = GraphEdge.from_dict(edge_data)
                        self._edges[edge_id] = edge
                        if self._graph is not None:
                            self._graph.add_edge(
                                edge.source, edge.target,
                                edge_type=edge.edge_type,
                                weight=edge.weight,
                                edge_id=edge.id
                            )
            except Exception as e:
                print(f"[WARN] Failed to load edges: {e}")

    def _next_edge_id(self) -> str:
        """生成下一个边ID"""
        seq = len(self._edges) + 1
        return f"EDGE-{seq:05d}"

    def add_edge(self, source: str, target: str,
                 edge_type: str, weight: float = 1.0,
                 metadata: dict = None) -> GraphEdge:
        """添加图谱边"""
        if edge_type not in self.VALID_EDGE_TYPES:
            raise ValueError(
                f"Invalid edge type: {edge_type}. "
                f"Valid types: {self.VALID_EDGE_TYPES}"
            )

        edge_id = self._next_edge_id()
        edge = GraphEdge(
            id=edge_id,
            source=source,
            target=target,
            edge_type=edge_type,
            weight=weight,
            metadata=metadata or {},
        )

        self._edges[edge_id] = edge

        if self._graph is not None:
            self._graph.add_edge(
                source, target,
                edge_type=edge_type,
                weight=weight,
                edge_id=edge_id
            )

        self._save_edges()
        return edge

    def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        """获取指定边"""
        return self._edges.get(edge_id)

    def find_path(self, source: str, target: str,
                  edge_types: list = None) -> list[dict]:
        """查询两点之间的所有路径"""
        if not self._graph:
            return []

        paths = []
        try:
            if edge_types:
                # 过滤特定边类型的路径
                for path in nx.all_simple_paths(self._graph, source, target):
                    valid = True
                    for i in range(len(path) - 1):
                        edge_data = self._graph[path[i]][path[i + 1]]
                        if edge_types and edge_data.get("edge_type") not in edge_types:
                            valid = False
                            break
                    if valid:
                        paths.append({
                            "path": path,
                            "length": len(path) - 1,
                            "edge_ids": [
                                self._graph[path[i]][path[i + 1]].get("edge_id")
                                for i in range(len(path) - 1)
                            ]
                        })
            else:
                for path in nx.all_simple_paths(self._graph, source, target, cutoff=5):
                    paths.append({
                        "path": path,
                        "length": len(path) - 1,
                        "edge_ids": [
                            self._graph[path[i]][path[i + 1]].get("edge_id")
                            for i in range(len(path) - 1)
                        ]
                    })
        except nx.NetworkXNoPath:
            pass
        except nx.NodeNotFound:
            pass

        return paths

    def validate_path(self, source: str, required_targets: list,
                      edge_types: list = None) -> dict:
        """
        路径完整性校验 (负反馈拦截)
        用于Action执行前: 必须有完整路径 POLICY→RULE 才能放行
        """
        result = {
            "source": source,
            "pass": True,
            "missing": [],
            "found": [],
            "paths": [],
        }

        for target in required_targets:
            paths = self.find_path(source, target, edge_types)
            if paths:
                result["found"].append(target)
                result["paths"].extend(paths)
            else:
                result["missing"].append(target)
                result["pass"] = False

        return result

    def get_neighbors(self, node_id: str, direction: str = "both",
                      edge_types: list = None) -> list[dict]:
        """获取节点的邻居"""
        if not self._graph:
            return []

        neighbors = []
        try:
            if direction in ("out", "both"):
                for neighbor in self._graph.successors(node_id):
                    edge_data = self._graph[node_id][neighbor]
                    if edge_types and edge_data.get("edge_type") not in edge_types:
                        continue
                    neighbors.append({
                        "direction": "out",
                        "target": neighbor,
                        "edge_type": edge_data.get("edge_type"),
                        "weight": edge_data.get("weight", 1.0),
                        "edge_id": edge_data.get("edge_id"),
                    })

            if direction in ("in", "both"):
                for neighbor in self._graph.predecessors(node_id):
                    edge_data = self._graph[neighbor][node_id]
                    if edge_types and edge_data.get("edge_type") not in edge_types:
                        continue
                    neighbors.append({
                        "direction": "in",
                        "source": neighbor,
                        "edge_type": edge_data.get("edge_type"),
                        "weight": edge_data.get("weight", 1.0),
                        "edge_id": edge_data.get("edge_id"),
                    })
        except (nx.NetworkXError, KeyError):
            pass

        return neighbors

    def update_edge_weight(self, edge_id: str, success: bool):
        """更新边权重 (调用成功/失败驱动)"""
        edge = self._edges.get(edge_id)
        if not edge:
            return

        edge.call_count += 1
        if success:
            edge.success_count += 1
            # 成功: 权重 +0.05
            edge.weight = min(edge.weight + 0.05, 2.0)
        else:
            # 失败: 权重 -0.1
            edge.weight = max(edge.weight - 0.1, 0.0)
            if edge.weight < 0.3:
                edge.metadata["low_weight_warning"] = True

        # 同步图权重
        if self._graph is not None:
            try:
                self._graph[edge.source][edge.target]["weight"] = edge.weight
            except (nx.NetworkXError, KeyError):
                pass

        self._save_edges()

    def _save_edges(self):
        """保存边到磁盘"""
        edge_file = self.edges_dir / "edges.json"
        data = {eid: edge.to_dict() for eid, edge in self._edges.items()}
        with open(edge_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def export_graph(self) -> dict:
        """导出图谱 (用于迁移/备份)"""
        if self._graph is not None:
            return nx.node_link_data(self._graph)
        return {
            "edges": [e.to_dict() for e in self._edges.values()]
        }

    def stats(self) -> dict:
        """统计信息"""
        type_counts = {}
        low_weight_edges = 0

        for edge in self._edges.values():
            t = edge.edge_type
            type_counts[t] = type_counts.get(t, 0) + 1
            if edge.weight < 0.5:
                low_weight_edges += 1

        result = {
            "total_edges": len(self._edges),
            "by_type": type_counts,
            "low_weight_edges": low_weight_edges,
        }

        if self._graph is not None:
            result["graph_nodes"] = self._graph.number_of_nodes()
            result["is_connected"] = nx.is_weakly_connected(self._graph) if self._graph.number_of_nodes() > 0 else True

        return result


if __name__ == "__main__":
    # 快速测试
    engine = GraphEngine()
    edge = engine.add_edge("TRD-20260409-0001", "RULE-20260409-0001", "validates")
    print(f"Created: {edge.id} ({edge.source} --[{edge.edge_type}]--> {edge.target})")

    print(f"\nStats: {json.dumps(engine.stats(), ensure_ascii=False, indent=2)}")
