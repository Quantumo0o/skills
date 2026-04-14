#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Memory DNA v5 — 契约传递路由器 (Contract Router)
=====================================================
核心功能:
- 结构化 Schema 校验 (替代自由文本传递)
- ID 化极简传递 (只传节点ID, 不传内容)
- 多轮传递保真 (每轮校验, 冲突拦截)
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path


@dataclass
class Contract:
    """结构化契约"""
    id: str                     # CONTRACT-SEQ
    contract_type: str          # 契约类型
    schema_version: str         # Schema 版本
    fields: dict                # 固定字段 (key → 节点ID)
    created_at: float = 0.0     # 创建时间
    status: str = "active"      # active/validated/blocked
    validation_log: list = None # 校验日志

    def __post_init__(self):
        if self.created_at == 0:
            self.created_at = time.time()
        if self.validation_log is None:
            self.validation_log = []

    def to_dict(self) -> dict:
        return asdict(self)


# 预定义的契约 Schema
CONTRACT_SCHEMAS = {
    "trade_order": {
        "description": "交易指令契约",
        "required": ["signal", "symbol", "price_ref", "risk_pass"],
        "fields": {
            "signal": {"description": "策略信号节点ID", "type": "str", "prefix": "STR-"},
            "symbol": {"description": "股票代码", "type": "str"},
            "price_ref": {"description": "行情参考节点ID", "type": "str", "prefix": "MKT-"},
            "risk_pass": {"description": "风控校验通过的规则节点ID列表", "type": "list", "prefix": "RULE-"},
            "position_pct": {"description": "仓位比例", "type": "float"},
            "direction": {"description": "交易方向", "type": "str", "enum": ["buy", "sell"]},
        }
    },
    "strategy_analysis": {
        "description": "策略分析契约",
        "required": ["strategy", "data_ref", "conclusion"],
        "fields": {
            "strategy": {"description": "策略节点ID", "type": "str", "prefix": "STR-"},
            "data_ref": {"description": "数据参考节点ID", "type": "str", "prefix": "MKT-"},
            "conclusion": {"description": "分析结论节点ID", "type": "str", "prefix": "MEM-"},
            "confidence": {"description": "信心评分", "type": "float"},
        }
    },
    "bug_report": {
        "description": "Bug 报告契约",
        "required": ["bug_id", "description", "fix_ref"],
        "fields": {
            "bug_id": {"description": "Bug节点ID", "type": "str", "prefix": "BUG-"},
            "description": {"description": "Bug描述", "type": "str"},
            "fix_ref": {"description": "修复方案节点ID", "type": "str", "prefix": "BUG-"},
            "impact": {"description": "影响等级", "type": "str", "enum": ["low", "medium", "high", "critical"]},
        }
    },
}


class ContractRouter:
    """契约传递路由器"""

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = Path(data_dir)
        self.contracts_dir = self.data_dir / "contracts"
        self.contracts_dir.mkdir(parents=True, exist_ok=True)

        self._contracts: dict[str, Contract] = {}
        self._seq = 0
        self._load()

    def _load(self):
        """加载契约"""
        contract_file = self.contracts_dir / "contracts.json"
        if contract_file.exists():
            try:
                with open(contract_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for cid, cdata in data.items():
                        self._contracts[cid] = Contract(**cdata)
                        seq_num = int(cid.split("-")[-1])
                        self._seq = max(self._seq, seq_num)
            except Exception as e:
                print(f"[WARN] Failed to load contracts: {e}")

    def _save(self):
        """保存契约"""
        contract_file = self.contracts_dir / "contracts.json"
        data = {cid: c.to_dict() for cid, c in self._contracts.items()}
        with open(contract_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _next_id(self) -> str:
        self._seq += 1
        return f"CONTRACT-{self._seq:05d}"

    def create_contract(self, contract_type: str, fields: dict) -> Contract:
        """创建结构化契约"""
        if contract_type not in CONTRACT_SCHEMAS:
            raise ValueError(
                f"Unknown contract type: {contract_type}. "
                f"Valid types: {list(CONTRACT_SCHEMAS.keys())}"
            )

        schema = CONTRACT_SCHEMAS[contract_type]

        # 校验必填字段
        missing = [f for f in schema["required"] if f not in fields]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")

        # 校验字段格式
        for field_name, value in fields.items():
            if field_name not in schema["fields"]:
                raise ValueError(f"Unknown field: {field_name}")

            field_def = schema["fields"][field_name]
            prefix = field_def.get("prefix")
            if prefix and isinstance(value, str) and not value.startswith(prefix):
                raise ValueError(
                    f"Field '{field_name}' expects ID starting with '{prefix}', got '{value}'"
                )

        contract = Contract(
            id=self._next_id(),
            contract_type=contract_type,
            schema_version="1.0",
            fields=fields,
        )

        self._contracts[contract.id] = contract
        self._save()
        return contract

    def validate_contract(self, contract_id: str) -> dict:
        """校验契约完整性"""
        contract = self._contracts.get(contract_id)
        if not contract:
            return {"pass": False, "reason": "Contract not found"}

        schema = CONTRACT_SCHEMAS.get(contract.contract_type)
        if not schema:
            return {"pass": False, "reason": "Unknown schema"}

        # 校验必填字段
        missing = [f for f in schema["required"] if f not in contract.fields]
        if missing:
            result = {"pass": False, "reason": f"Missing required fields: {missing}"}
            contract.validation_log.append({"action": "validate", **result, "time": time.time()})
            contract.status = "blocked"
            self._save()
            return result

        # 校验字段内容有效性 (列表不为空, 前缀匹配等)
        for field_name, field_def in schema["fields"].items():
            if field_name not in contract.fields:
                continue
            value = contract.fields[field_name]
            field_type = field_def.get("type", "str")
            
            # 列表字段: 必填字段不能为空
            if field_type == "list" and field_name in schema["required"]:
                if not value or len(value) == 0:
                    result = {"pass": False, "reason": f"Required list field '{field_name}' is empty"}
                    contract.validation_log.append({"action": "validate", **result, "time": time.time()})
                    contract.status = "blocked"
                    self._save()
                    return result
                
                # 检查前缀匹配
                prefix = field_def.get("prefix")
                if prefix:
                    for item in value:
                        if not str(item).startswith(prefix):
                            result = {"pass": False, "reason": f"Field '{field_name}' item '{item}' doesn't match prefix '{prefix}'"}
                            contract.validation_log.append({"action": "validate", **result, "time": time.time()})
                            contract.status = "blocked"
                            self._save()
                            return result
            
            # 字符串字段: 检查前缀匹配
            elif field_type == "str":
                prefix = field_def.get("prefix")
                if prefix and not str(value).startswith(prefix):
                    result = {"pass": False, "reason": f"Field '{field_name}' value '{value}' doesn't match prefix '{prefix}'"}
                    contract.validation_log.append({"action": "validate", **result, "time": time.time()})
                    contract.status = "blocked"
                    self._save()
                    return result

        result = {"pass": True, "reason": "All required fields present and valid"}
        contract.validation_log.append({"action": "validate", **result, "time": time.time()})
        contract.status = "validated"
        self._save()
        return result

    def get_contract_json(self, contract_id: str) -> Optional[str]:
        """获取契约的JSON表示 (用于跨Agent传递)"""
        contract = self._contracts.get(contract_id)
        if not contract:
            return None
        return json.dumps(contract.fields, ensure_ascii=False, indent=2)

    def parse_contract_json(self, contract_type: str, json_str: str) -> Contract:
        """从JSON解析契约 (接收方使用)"""
        fields = json.loads(json_str)
        return self.create_contract(contract_type, fields)

    def stats(self) -> dict:
        """统计信息"""
        type_counts = {}
        status_counts = {}
        for c in self._contracts.values():
            t = c.contract_type
            type_counts[t] = type_counts.get(t, 0) + 1
            s = c.status
            status_counts[s] = status_counts.get(s, 0) + 1

        return {
            "total_contracts": len(self._contracts),
            "by_type": type_counts,
            "by_status": status_counts,
        }


import os  # For __init__ reference fix

if __name__ == "__main__":
    # 快速测试
    router = ContractRouter()

    # 创建交易指令契约
    contract = router.create_contract("trade_order", {
        "signal": "STR-20260409-0001",
        "symbol": "600519.SH",
        "price_ref": "MKT-20260409-0001",
        "risk_pass": ["RULE-20260409-0001", "RULE-20260409-0002"],
        "position_pct": 0.10,
        "direction": "buy",
    })
    print(f"Created: {contract.id}")
    print(f"JSON: {router.get_contract_json(contract.id)}")

    # 校验
    result = router.validate_contract(contract.id)
    print(f"Validate: {result}")

    print(f"\nStats: {json.dumps(router.stats(), ensure_ascii=False, indent=2)}")
