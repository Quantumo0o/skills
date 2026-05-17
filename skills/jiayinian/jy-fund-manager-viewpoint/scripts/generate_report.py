#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成基金经理观点分析报告

Usage:
    python3 generate_report.py <analysis_request.json> <analysis_result.json>
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime


def generate_report(industry: str, q1_str: str, q2_str: str, result: dict, q1_reports: list, q2_reports: list) -> Path:
    """生成结构化报告"""
    output_dir = Path("~/Desktop/jy-fund-manager-viewpoint/output").expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    q1 = result.get("q1_analysis", {})
    q2 = result.get("q2_analysis", {})
    comp = result.get("comparison", {})
    
    def fmt_cons(lst):
        if not lst: return "无明显共识"
        return "<br>".join([f"• {c.get('description','')} _({'，'.join(c.get('supporting_funds',[])[:2])})_" for c in lst[:3]])
    
    def fmt_div(lst):
        if not lst: return "无明显分歧"
        return "<br>".join([f"• **{d.get('topic','')}**: {d.get('view_a',{}).get('view','')} vs {d.get('view_b',{}).get('view','')}" for d in lst[:2]])
    
    def fmt_vp(vps):
        if not vps: return "无数据"
        return "<br><br>".join([f"**{v.get('fund_name','')}** ({v.get('sentiment','')})<br>{'<br>'.join(v.get('key_points',[])[:2]) or '无具体观点'}" for v in vps[:5]])
    
    sources = [f"[{i}] {r['fund_name']} {r['title']} ({r['fund_code']})" for i, r in enumerate(q1_reports + q2_reports, 1)][:15]
    summary = comp.get("summary", "暂无分析") if comp else "暂无分析"
    
    lines = [
        f"# 📊 基金经理观点分析报告\n\n",
        f"**行业：** {industry} | **季度：** {q1_str} vs {q2_str} | **时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n",
        f"**数据源：** 恒生聚源 (OpenClaw 语义分析) | **基金数：** {len(q1_reports) + len(q2_reports)}\n\n",
        "---\n\n## 🎯 核心结论\n\n", f"{summary}\n\n", "---\n\n## 📈 季度对比\n\n",
        "| 维度 | " + q1_str + " | " + q2_str + " |\n|:-----|:-----|:-----|\n",
        f"| **情绪** | {q1.get('overall_sentiment', 'N/A')} | {q2.get('overall_sentiment', 'N/A')} |\n",
        f"| **主题** | {', '.join(q1.get('key_themes', [])[:3]) or '无'} | {', '.join(q2.get('key_themes', [])[:3]) or '无'} |\n",
        f"| **共识** | {fmt_cons(q1.get('consensus', []))} | {fmt_cons(q2.get('consensus', []))} |\n",
        f"| **分歧** | {fmt_div(q1.get('divergence', []))} | {fmt_div(q2.get('divergence', []))} |\n",
        f"| **观点** | {fmt_vp(q1.get('fund_viewpoints', []))} | {fmt_vp(q2.get('fund_viewpoints', []))} |\n\n",
        "---\n\n## 📋 来源\n\n",
    ]
    lines.extend([s + "\n" for s in sources])
    lines.append(f"\n*OpenClaw 语义分析，仅供参考*\n")
    
    content = "".join(lines)
    filename = f"{industry}_{q1_str}_vs_{q2_str}_OC.md"
    output_file = output_dir / filename
    output_file.write_text(content, encoding='utf-8')
    
    print(f"\n{'='*60}")
    print(f"✅ 报告已生成：{output_file}")
    print(f"{'='*60}\n")
    print(content)
    return output_file


def main():
    if len(sys.argv) < 3:
        print("用法：python3 generate_report.py <request.json> <result.json>")
        print("说明:")
        print("  analysis_request.json - 包含原始数据的请求文件")
        print("  analysis_result.json  - OpenClaw 返回的分析结果 JSON")
        sys.exit(1)
    
    req_file = Path(sys.argv[1]).expanduser()
    result_file = Path(sys.argv[2]).expanduser()
    
    if not req_file.exists():
        print(f"❌ 文件不存在：{req_file}")
        sys.exit(1)
    if not result_file.exists():
        print(f"❌ 文件不存在：{result_file}")
        sys.exit(1)
    
    with open(req_file, 'r', encoding='utf-8') as f:
        req = json.load(f)
    with open(result_file, 'r', encoding='utf-8') as f:
        result = json.load(f)
    
    # 处理可能的代码块包裹
    result_str = json.dumps(result, ensure_ascii=False)
    if '```json' in result_str:
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_str, re.DOTALL)
        if match:
            result = json.loads(match.group(1))
    
    generate_report(
        req.get('industry', '未知'),
        req.get('q1', 'Q1'),
        req.get('q2', 'Q2'),
        result,
        req.get('q1_reports', []),
        req.get('q2_reports', [])
    )


if __name__ == "__main__":
    main()
