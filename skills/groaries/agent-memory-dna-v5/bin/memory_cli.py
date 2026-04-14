#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Memory DNA v5 — 统一命令行接口 (CLI)
=========================================
使用方式:
    python bin/memory_cli.py <command> [options]

Commands:
    node        原子节点操作
    edge        图谱边操作
    genome      基因组操作
    contract    契约操作
    trace       事件溯源查询
    validate    路径校验
    stats       系统统计
    heartbeat   心跳巡检
    migrate     从 v4 迁移记忆
"""

import argparse
import json
import os
import sys

# 确保 bin 目录在路径中
sys.path.insert(0, os.path.dirname(__file__))

from node_manager import NodeManager, NodeType
from graph_engine import GraphEngine
from genome_core import GenomeCore
from contract_router import ContractRouter
from event_logger import EventLogger
from auto_maintenance import AutoMaintenance
from voxel_engine import VoxelEngine


def get_data_dir():
    """获取数据目录"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def cmd_node_add(args):
    """添加节点"""
    mgr = NodeManager(get_data_dir())
    logger = EventLogger(get_data_dir())

    node_type_map = {
        "rule": NodeType.RULE,
        "config": NodeType.CONFIG,
        "memory": NodeType.MEMORY,
        "trade": NodeType.TRADE,
        "market": NodeType.MARKET,
        "strategy": NodeType.STRATEGY,
        "bugfix": NodeType.BUGFIX,
        "skill": NodeType.SKILL,
    }

    ntype = node_type_map.get(args.type, NodeType.MEMORY)
    tags = args.tags.split(",") if args.tags else []

    node = mgr.add_node(
        node_type=ntype,
        content=args.content,
        tags=tags,
        source_ref=args.source,
    )

    logger.log_node_create(node.id, node.content)
    print(f"✅ Created: {node.id}")
    print(f"   Type: {node.node_type}")
    print(f"   Content: {node.content[:100]}")
    if tags:
        print(f"   Tags: {', '.join(tags)}")


def cmd_node_query(args):
    """查询节点"""
    mgr = NodeManager(get_data_dir())

    if args.id:
        node = mgr.get_node(args.id)
        if node:
            print(json.dumps(node.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(f"❌ Node not found: {args.id}")
        return

    if args.search:
        results = mgr.search_content(args.search)
        print(f"🔍 Found {len(results)} nodes matching '{args.search}':")
    else:
        ntype = NodeType(args.type) if args.type else None
        results = mgr.query_nodes(node_type=ntype, limit=args.limit)
        print(f"📋 Found {len(results)} nodes:")

    for node in results:
        readonly_tag = " [RO]" if node.is_readonly else ""
        print(f"  {node.id}{readonly_tag} ({node.node_type}, w={node.weight:.2f}): {node.content[:80]}")


def cmd_edge_add(args):
    """添加图谱边"""
    engine = GraphEngine(get_data_dir())
    logger = EventLogger(get_data_dir())

    edge = engine.add_edge(
        source=args.source,
        target=args.target,
        edge_type=args.type,
        metadata={"note": args.note} if args.note else None,
    )

    logger.log_edge_create(edge.id, args.source, args.target, args.type)
    print(f"✅ Created: {edge.id}")
    print(f"   {args.source} --[{args.type}]--> {args.target}")


def cmd_edge_path(args):
    """查询路径"""
    engine = GraphEngine(get_data_dir())

    paths = engine.find_path(args.source, args.target)
    if paths:
        print(f"🔗 Found {len(paths)} path(s) from {args.source} to {args.target}:")
        for i, p in enumerate(paths):
            print(f"  Path {i + 1}: {' → '.join(p['path'])} (length: {p['length']})")
    else:
        print(f"❌ No path found from {args.source} to {args.target}")


def cmd_genome_add(args):
    """添加基因组规则"""
    genome = GenomeCore(get_data_dir())
    logger = EventLogger(get_data_dir())

    try:
        entry = genome.add_rule(args.key, args.value, args.desc, args.category)
        logger.log_node_create(entry.id, f"{entry.key} = {entry.value}")
        print(f"✅ Genome: {entry.id} {entry.key} = {entry.value}")
        print(f"   {entry.description}")
    except ValueError as e:
        print(f"❌ {e}")


def cmd_genome_validate(args):
    """校验基因组"""
    genome = GenomeCore(get_data_dir())
    logger = EventLogger(get_data_dir())

    result = genome.validate(args.key, args.value)
    logger.log_validation(args.key, result)

    if result["pass"]:
        print(f"✅ PASS: {result['reason']}")
    else:
        print(f"❌ BLOCKED: {result['reason']}")


def cmd_genome_list(args):
    """列出基因组规则"""
    genome = GenomeCore(get_data_dir())
    rules = genome.list_rules()
    print(f"# 核心基因组规则 ({len(rules)} rules)")
    for entry in sorted(rules, key=lambda e: e.key):
        print(f"- `{entry.key}` = `{entry.value}` — {entry.description}")


def cmd_contract_create(args):
    """创建契约"""
    router = ContractRouter(get_data_dir())
    logger = EventLogger(get_data_dir())

    # 解析字段
    fields = {}
    for field in args.fields:
        key, value = field.split("=", 1)
        # 尝试解析为 JSON 数组
        if value.startswith("["):
            fields[key] = json.loads(value)
        else:
            fields[key] = value

    contract = router.create_contract(args.type, fields)
    logger.log_contract(contract.id, args.type, fields)
    print(f"✅ Contract: {contract.id}")
    print(f"   Type: {args.type}")
    print(f"   Fields: {json.dumps(contract.fields, ensure_ascii=False, indent=4)}")


def cmd_validate(args):
    """路径校验"""
    engine = GraphEngine(get_data_dir())
    genome = GenomeCore(get_data_dir())

    targets = args.require.split(",")
    result = engine.validate_path(args.node, targets)

    if result["pass"]:
        print(f"✅ PASS: All required paths found for {args.node}")
        print(f"   Found: {', '.join(result['found'])}")
    else:
        print(f"❌ BLOCKED: Missing paths for {args.node}")
        print(f"   Missing: {', '.join(result['missing'])}")


def cmd_trace(args):
    """事件溯源查询"""
    logger = EventLogger(get_data_dir())
    events = logger.trace_node(args.node, days=args.days)

    if events:
        print(f"📜 Trace for {args.node} ({len(events)} events):")
        for e in events:
            time_str = os.path.basename(time.strftime("%Y-%m-%d", time.localtime(e.timestamp)))
            print(f"  [{e.result:8s}] {e.id} | {e.action}")
    else:
        print(f"No events found for {args.node}")


def cmd_stats(args):
    """系统统计"""
    mgr = NodeManager(get_data_dir())
    engine = GraphEngine(get_data_dir())
    genome = GenomeCore(get_data_dir())
    maint = AutoMaintenance(get_data_dir())

    print("# Agent Memory DNA v5 — 系统统计")
    print(f"\n## 节点 (Nodes)")
    stats = mgr.stats()
    for k, v in stats.items():
        print(f"  - {k}: {v}")

    print(f"\n## 图谱 (Graph)")
    stats = engine.stats()
    for k, v in stats.items():
        print(f"  - {k}: {v}")

    print(f"\n## 基因组 (Genome)")
    stats = genome.stats()
    for k, v in stats.items():
        print(f"  - {k}: {v}")

    print(f"\n## 系统健康 (Health)")
    health = maint.heartbeat()
    print(f"  - Overall: {health['overall']}")
    for comp, check in health["checks"].items():
        print(f"  - {comp}: {check.get('status', 'unknown')}")


def cmd_heartbeat(args):
    """心跳巡检"""
    maint = AutoMaintenance(get_data_dir())
    report = maint.generate_report()
    print(report)


def main():
    parser = argparse.ArgumentParser(
        description="Agent Memory DNA v5 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # node commands
    node_parser = subparsers.add_parser("node", help="Node operations")
    node_sub = node_parser.add_subparsers(dest="subcommand")

    node_add = node_sub.add_parser("add", help="Add node")
    node_add.add_argument("--type", "-t", default="memory", help="Node type")
    node_add.add_argument("--content", "-c", required=True, help="Node content")
    node_add.add_argument("--tags", help="Comma-separated tags")
    node_add.add_argument("--source", default="", help="Source reference")

    node_query = node_sub.add_parser("query", help="Query nodes")
    node_query.add_argument("--id", help="Node ID")
    node_query.add_argument("--search", help="Search content")
    node_query.add_argument("--type", help="Filter by type")
    node_query.add_argument("--limit", type=int, default=20, help="Max results")

    # edge commands
    edge_parser = subparsers.add_parser("edge", help="Edge operations")
    edge_sub = edge_parser.add_subparsers(dest="subcommand")

    edge_add = edge_sub.add_parser("add", help="Add edge")
    edge_add.add_argument("--from", dest="source", required=True, help="Source node ID")
    edge_add.add_argument("--to", dest="target", required=True, help="Target node ID")
    edge_add.add_argument("--type", "-t", required=True, help="Edge type")
    edge_add.add_argument("--note", help="Edge note")

    edge_path = edge_sub.add_parser("path", help="Find path")
    edge_path.add_argument("--from", dest="source", required=True)
    edge_path.add_argument("--to", dest="target", required=True)

    # genome commands
    genome_parser = subparsers.add_parser("genome", help="Genome operations")
    genome_sub = genome_parser.add_subparsers(dest="subcommand")

    genome_add = genome_sub.add_parser("add", help="Add genome rule")
    genome_add.add_argument("--key", "-k", required=True)
    genome_add.add_argument("--value", "-v", required=True)
    genome_add.add_argument("--desc", "-d", required=True)
    genome_add.add_argument("--category", default="risk")

    genome_validate = genome_sub.add_parser("validate", help="Validate value against genome")
    genome_validate.add_argument("--key", "-k", required=True)
    genome_validate.add_argument("--value", "-v", required=True)

    genome_sub.add_parser("list", help="List all genome rules")
    
    # shadow simulate
    genome_sim = genome_sub.add_parser("simulate", help="Simulate new rule in shadow mode")
    genome_sim.add_argument("--rule", required=True, help="Key=Value")
    genome_sim.add_argument("--desc", default="Shadow Test")
    genome_sim.add_argument("--days", type=int, default=7)

    # contract commands
    contract_parser = subparsers.add_parser("contract", help="Contract operations")
    contract_parser.add_argument("--type", "-t", required=True, help="Contract type")
    contract_parser.add_argument("--fields", "-f", nargs="+", required=True, help="Fields as key=value")

    # validate command
    validate_parser = subparsers.add_parser("validate", help="Validate node path")
    validate_parser.add_argument("--node", "-n", required=True)
    validate_parser.add_argument("--require", "-r", required=True, help="Required targets (comma-separated)")

    # trace command
    trace_parser = subparsers.add_parser("trace", help="Trace node events")
    trace_parser.add_argument("--node", "-n", required=True)
    trace_parser.add_argument("--days", type=int, default=7)

    # voxel commands (v5.1)
    voxel_parser = subparsers.add_parser("voxel", help="Semantic Voxel Operations")
    voxel_parser.add_argument("action", choices=["update", "query", "list"])
    voxel_parser.add_argument("--type", "-t", default="MARKET", help="Voxel type")

    # stats command
    subparsers.add_parser("stats", help="System statistics")

    # heartbeat command
    subparsers.add_parser("heartbeat", help="System health check")

    # agent loop command (v5.1 Integration)
    agent_parser = subparsers.add_parser("agent", help="Run Agent Main Decision Loop")
    agent_parser.add_argument("--prompt", "-p", default="当前应该交易吗？", help="User prompt for the agent")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Route commands
    if args.command == "node":
        if args.subcommand == "add":
            cmd_node_add(args)
        elif args.subcommand == "query":
            cmd_node_query(args)
        else:
            node_parser.print_help()
    elif args.command == "edge":
        if args.subcommand == "add":
            cmd_edge_add(args)
        elif args.subcommand == "path":
            cmd_edge_path(args)
        else:
            edge_parser.print_help()
    elif args.command == "genome":
        if args.subcommand == "add":
            cmd_genome_add(args)
        elif args.subcommand == "validate":
            cmd_genome_validate(args)
        elif args.subcommand == "list":
            cmd_genome_list(args)
        elif args.subcommand == "simulate":
            from shadow_genome import ShadowGenome
            key, val = args.rule.split("=")
            engine = ShadowGenome(get_data_dir())
            report = engine.simulate_rule(key, val, args.desc, args.days)
            print("\n📊 Shadow Report:")
            print(json.dumps(report, indent=4, ensure_ascii=False))
        else:
            genome_parser.print_help()
    elif args.command == "contract":
        cmd_contract_create(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "trace":
        cmd_trace(args)
    elif args.command == "voxel":
        engine = VoxelEngine(get_data_dir())
        if args.action == "update":
            engine.aggregate_voxels()
        elif args.action == "query":
            res = engine.get_latest_voxel(args.type)
            print(json.dumps(res, ensure_ascii=False, indent=4) if res else "No voxel found")
        elif args.action == "list":
            # Simple listing
            nodes = engine._scan_l1_nodes()
            voxels = [n for n in nodes if "voxel" in n.get("tags", [])]
            print(f"Found {len(voxels)} voxels:")
            for v in voxels[-5:]:
                print(f"  - {v['id']} ({v['tags']})")
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "heartbeat":
        cmd_heartbeat(args)
    elif args.command == "agent":
        from agent_loop import AgentBrain
        brain = AgentBrain(get_data_dir())
        brain.loop(args.prompt)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
