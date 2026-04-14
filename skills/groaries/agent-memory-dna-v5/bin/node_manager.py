#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Memory DNA v5 — 原子节点管理器 (Node Manager)
====================================================
核心功能:
- 最小语义原子节点 CRUD
- 唯一 ID 分配 (RULE-*, MEM-*, EXE-*, CTX-*, POL-*, BUG-*, CONFIG-*)
- 硬件级只读保护 (L0 基因组不可修改)
- 节点分类管理
"""

import json
import os
import time
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional
from pathlib import Path


class NodeType(Enum):
    """节点类型枚举"""
    RULE = "rule"           # 风控铁律 (L0 只读)
    CONFIG = "config"       # 系统配置 (L0 只读)
    MEMORY = "memory"       # 经验记忆 (L1 原子)
    EXECUTION = "trade"         # 交易记录 (L1 原子)
    CONTEXT = "market"       # 行情数据 (L1 原子)
    POLICY = "strategy"   # 策略定义 (L1 原子)
    BUGFIX = "bugfix"       # Bug修复 (L1 原子)
    SKILL = "skill"         # 技能定义 (L1 原子)


@dataclass
class AtomicNode:
    """最小语义原子节点"""
    id: str                 # 唯一ID: TYPE-YYYYMMDD-SEQ
    node_type: str          # 节点类型 (NodeType.value)
    content: str            # 节点内容 (最小语义单元)
    created_at: float       # 创建时间戳
    tags: list              # 分类标签
    source_ref: str = ""    # 来源引用 (原始文件/对话ID)
    is_readonly: bool = False  # 是否只读 (L0 基因组强制为 True)
    weight: float = 1.0     # 节点权重 (调用正确率动态调整)
    call_count: int = 0     # 调用次数
    success_count: int = 0  # 成功调用次数

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "AtomicNode":
        return cls(**d)


class NodeManager:
    """原子节点管理器"""

    # 类型前缀映射
    TYPE_PREFIX = {
        NodeType.RULE: "RULE",
        NodeType.CONFIG: "CONFIG",
        NodeType.MEMORY: "MEM",
        NodeType.EXECUTION: "EXE",
        NodeType.CONTEXT: "CTX",
        NodeType.POLICY: "STR",
        NodeType.BUGFIX: "BUG",
        NodeType.SKILL: "SKL",
    }

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = Path(data_dir)
        self.nodes_dir = self.data_dir / "nodes"
        self.logs_dir = self.data_dir / "logs"

        # 确保目录存在 (L0/L1 物理隔离: NodeManager 只管理 nodes/)
        self.nodes_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # 节点索引 (内存缓存)
        self._index: dict[str, AtomicNode] = {}
        self._load_index()

    def _load_index(self):
        """从磁盘加载所有节点到内存索引"""
        for node_file in self.nodes_dir.glob("*.json"):
            try:
                with open(node_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    node = AtomicNode.from_dict(data)
                    self._index[node.id] = node
            except Exception as e:
                print(f"[WARN] Failed to load node {node_file.name}: {e}")

        # L0 基因组由 GenomeCore 独占管理，NodeManager 不扫描 genome/ 目录
        # (遵循 v5 设计：L0/L1 物理隔离，职责单一)

    def _next_id(self, node_type: NodeType) -> str:
        """生成下一个节点ID"""
        prefix = self.TYPE_PREFIX[node_type]
        date_str = time.strftime("%Y%m%d")

        # 统计同类型同日期数量
        count = 0
        for nid in self._index:
            if nid.startswith(f"{prefix}-{date_str}"):
                count += 1

        seq = count + 1
        return f"{prefix}-{date_str}-{seq:04d}"

    def add_node(self, node_type: NodeType, content: str,
                 tags: list = None, source_ref: str = "",
                 force_id: str = None, is_readonly: bool = False) -> AtomicNode:
        """创建新原子节点"""
        if tags is None:
            tags = []

        if force_id:
            node_id = force_id
        else:
            node_id = self._next_id(node_type)

        # 检查ID冲突
        if node_id in self._index:
            raise ValueError(f"Node ID conflict: {node_id}")

        node = AtomicNode(
            id=node_id,
            node_type=node_type.value,
            content=content.strip(),
            created_at=time.time(),
            tags=tags,
            source_ref=source_ref,
            is_readonly=is_readonly or (node_type in (NodeType.RULE, NodeType.CONFIG)),
        )

        # 保存到磁盘
        self._save_node(node)
        self._index[node_id] = node

        return node

    def _save_node(self, node: AtomicNode):
        """保存节点到磁盘 (所有 AtomicNode 统一存到 nodes/ 目录)"""
        # L0/L1 物理隔离: GenomeCore 独占 genome/, NodeManager 独占 nodes/
        file_path = self.nodes_dir / f"{node.id}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(node.to_dict(), f, ensure_ascii=False, indent=2)

    def get_node(self, node_id: str) -> Optional[AtomicNode]:
        """通过ID获取节点"""
        return self._index.get(node_id)

    def update_node(self, node_id: str, **kwargs) -> AtomicNode:
        """更新节点 (只读节点拒绝修改)"""
        node = self._index.get(node_id)
        if not node:
            raise ValueError(f"Node not found: {node_id}")

        if node.is_readonly:
            raise PermissionError(
                f"[BLOCKED] Node {node_id} is READ-ONLY (L0 Genome). "
                f"Modification rejected. Content: {node.content[:50]}"
            )

        # 更新字段
        for key, value in kwargs.items():
            if hasattr(node, key):
                setattr(node, key, value)

        self._save_node(node)
        return node

    def record_call(self, node_id: str, success: bool = True):
        """记录节点调用 (用于权重动态调整)"""
        node = self._index.get(node_id)
        if not node:
            return

        node.call_count += 1
        if success:
            node.success_count += 1

        # 动态权重: 成功率 * 调用频率
        if node.call_count > 0:
            success_rate = node.success_count / node.call_count
            node.weight = 0.7 * success_rate + 0.3 * min(node.call_count / 100, 1.0)
            self._save_node(node)

    def query_nodes(self, node_type: NodeType = None, tags: list = None,
                    min_weight: float = 0.0, limit: int = 100) -> list[AtomicNode]:
        """查询节点"""
        results = []
        for node in self._index.values():
            if node_type and node.node_type != node_type.value:
                continue
            if tags and not any(t in node.tags for t in tags):
                continue
            if node.weight < min_weight:
                continue
            results.append(node)

        # 按权重排序
        results.sort(key=lambda n: n.weight, reverse=True)
        return results[:limit]

    def search_content(self, keyword: str, node_type: NodeType = None) -> list[AtomicNode]:
        """全文搜索节点内容"""
        results = []
        keyword_lower = keyword.lower()
        for node in self._index.values():
            if node_type and node.node_type != node_type.value:
                continue
            if keyword_lower in node.content.lower() or \
               any(keyword_lower in t.lower() for t in node.tags):
                results.append(node)
        return results

    def delete_node(self, node_id: str) -> bool:
        """软删除节点 (只读节点拒绝删除)"""
        node = self._index.get(node_id)
        if not node:
            return False

        if node.is_readonly:
            raise PermissionError(
                f"[BLOCKED] Node {node_id} is READ-ONLY. Deletion rejected."
            )

        # 软删除: 标记为已删除
        node.tags.append("deleted")
        self._save_node(node)
        del self._index[node_id]
        return True

    def export_all(self) -> dict:
        """导出所有节点 (用于迁移/备份)"""
        return {
            node.id: node.to_dict()
            for node in self._index.values()
        }

    def stats(self) -> dict:
        """统计信息"""
        type_counts = {}
        total_calls = 0
        total_weight = 0.0

        for node in self._index.values():
            t = node.node_type
            type_counts[t] = type_counts.get(t, 0) + 1
            total_calls += node.call_count
            total_weight += node.weight

        return {
            "total_nodes": len(self._index),
            "by_type": type_counts,
            "total_calls": total_calls,
            "avg_weight": total_weight / len(self._index) if self._index else 0,
            "readonly_count": sum(1 for n in self._index.values() if n.is_readonly),
        }


if __name__ == "__main__":
    # 快速测试
    mgr = NodeManager()
    node = mgr.add_node(NodeType.RULE, "单仓上限10%", tags=["risk", "position"])
    print(f"Created: {node.id} → {node.content}")

    node2 = mgr.add_node(NodeType.MEMORY, "腾讯财经API是实时行情首选", tags=["data", "api"])
    print(f"Created: {node2.id} → {node2.content}")

    print(f"\nStats: {json.dumps(mgr.stats(), ensure_ascii=False, indent=2)}")
