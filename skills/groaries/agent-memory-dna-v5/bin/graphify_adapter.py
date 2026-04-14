#!/usr/bin/env python3
"""
Graphify -> DNA v5 桥接适配器 (Bridge Adapter)
职责：
1. 解析 Graphify 输出的图谱数据
2. 转化为 DNA v5 原子节点
3. 执行 L0 基因组预校验 (Cybernetic Gatekeeping)
"""

import os
import sys
import json
import time

# 确保路径正确
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BACKEND_DIR)

from node_manager import NodeManager, NodeType
from graph_engine import GraphEngine
from genome_core import GenomeCore
from event_logger import EventLogger

class GraphifyAdapter:
    def __init__(self):
        self.node_mgr = NodeManager()
        self.graph_eng = GraphEngine()
        self.genome = GenomeCore()
        self.logger = EventLogger()

    def ingest_graphify_data(self, graphify_json_str):
        """
        核心入口：接收 Graphify 数据并入库
        """
        print(f"\n📥 [适配器] 正在解析 Graphify 数据包...")
        data = json.loads(graphify_json_str)
        
        nodes = data.get('nodes', [])
        edges = data.get('edges', [])
        
        created_nodes = []
        validated_count = 0
        blocked_count = 0

        # 1. 节点转化与校验
        for node in nodes:
            g_id = node.get('id')
            g_content = node.get('content', '')
            g_type = node.get('type', 'MEM')
            
            # 映射类型 (Graphify Type -> DNA Type)
            type_map = {
                'policy': NodeType.POLICY,
                'rule': NodeType.RULE,
                'market': NodeType.MARKET,
                'code': NodeType.SKILL,   # 代码映射为技能节点
                'bug': NodeType.BUGFIX     # Bug映射为修复节点
            }
            dna_type = type_map.get(g_type.lower(), NodeType.MEMORY)

            # === 🔒 控制论：网关校验 (Pre-Commit Validation) ===
            # 检查内容是否包含违反基因组的风险词汇或数值
            is_risky, reason = self._cybernetic_gate_check(g_content, dna_type)
            
            if not is_risky:
                # 存入 DNA v5
                node_obj = self.node_mgr.add_node(
                    node_type=dna_type,
                    content=g_content,
                    tags=[g_id] # 保留原始 ID 供追溯
                )
                created_nodes.append({'source': g_id, 'target': node_obj.id})
                validated_count += 1
                self.logger.log("INGEST", [node_obj.id], "Accepted")
            else:
                blocked_count += 1
                self.logger.log("SECURITY", [], "Rejected", result="blocked")
                print(f"🚫 [网关] 拒绝节点 {g_id}: {reason}")

        # 2. 边重建 (Mapping Old IDs to New IDs)
        print(f"\n🔗 [适配器] 正在重建图谱连接...")
        id_mapping = {c['source']: c['target'] for c in created_nodes}
        
        for edge in edges:
            src_old = edge.get('source')
            tgt_old = edge.get('target')
            rel = edge.get('label', 'references')
            
            # 映射到 DNA v5 合法边类型
            allowed_types = {'validates', 'references', 'precedes', 'belongs_to', 'conflicts_with', 'depends_on', 'causes', 'replaces', 'triggers'}
            if rel not in allowed_types:
                rel = 'references' # 默认为引用关系

            if src_old in id_mapping and tgt_old in id_mapping:
                self.graph_eng.add_edge(
                    source=id_mapping[src_old],
                    target=id_mapping[tgt_old],
                    edge_type=rel
                )
        
        print(f"\n✅ [适配器] 处理完成。")
        print(f"   - 成功入库: {validated_count} 个原子节点")
        print(f"   - 拦截风险: {blocked_count} 个风险节点")
        print(f"   - 图谱连接: {len(edges)} 条")

    def _cybernetic_gate_check(self, content, node_type):
        """
        内部网关：根据 L0 基因组拦截危险知识
        """
        # 模拟 L0 规则：禁止"无止损"、"满仓梭哈"等概念
        forbidden_concepts = ["无止损", "无风控", "满仓", "全仓梭哈", "no stop loss", "100% position"]
        
        for concept in forbidden_concepts:
            if concept in content.lower():
                return True, f"触犯基因组铁律: 禁止记录'{concept}'相关内容"
        
        return False, "Pass"

# === 模拟运行 ===
if __name__ == "__main__":
    # 模拟 Graphify 输出：关于 Oracle 策略的图谱
    # 其中包含一个正常的策略定义，和一个危险的错误规则（测试拦截）
    mock_graphify_output = json.dumps({
        "nodes": [
            {
                "id": "graphify_node_1",
                "content": "Oracle 动态动量策略 v2.0: 结合 MACD 和 ATR 进行趋势跟踪，基础仓位 30%。",
                "type": "strategy"
            },
            {
                "id": "graphify_node_2",
                "content": "当 MACD 金叉且 ATR 扩张时，建议买入。",
                "type": "rule"
            },
            {
                "id": "graphify_node_3",
                "content": "错误建议：遇到黑天鹅时不要止损，满仓死扛等待反弹。",
                "type": "rule" 
            }
        ],
        "edges": [
            {"source": "graphify_node_1", "target": "graphify_node_2", "label": "contains"},
            {"source": "graphify_node_1", "target": "graphify_node_3", "label": "contains"} 
        ]
    })

    adapter = GraphifyAdapter()
    adapter.ingest_graphify_data(mock_graphify_output)
