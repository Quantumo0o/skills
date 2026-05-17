#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金经理观点分析 - 数据准备脚本

使用 mcporter 调用聚源 MCP 服务获取数据，生成 OpenClaw 语义分析提示词。

Usage:
    python3 analyze_viewpoints.py "新能源" "2025Q3" "2025Q4"
"""

import subprocess
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import sys


CONFIG = {
    "tool_server": "jy-financedata-tool",
    "api_server": "jy-financedata-api",
    "output_dir": Path("~/Desktop/jy-fund-manager-viewpoint/output").expanduser(),
    "timeout": 150,
    "max_funds": 15,
}
CONFIG["output_dir"].mkdir(parents=True, exist_ok=True)

INDUSTRY_ALIASES = {
    "新能源": ["新能源", "光伏", "锂电", "储能", "电池", "电动车", "风电", "电力设备"],
    "消费": ["消费", "白酒", "食品", "饮料", "零售", "旅游", "家电", "内需"],
    "医药": ["医药", "医疗", "生物", "创新药", "器械", "医保"],
    "科技": ["科技", "TMT", "电子", "通信", "计算机", "半导体", "AI", "人工智能"],
    "金融": ["金融", "银行", "保险", "证券", "券商"],
    "制造": ["制造", "机械", "汽车", "装备", "工业"],
    "周期": ["周期", "有色", "钢铁", "煤炭", "化工"],
    "房地产": ["房地产", "地产", "物业", "基建"],
}


def call_mcp_tool(server: str, tool: str, query: str, timeout: int = None) -> Optional[Dict]:
    """调用 MCP 工具"""
    if timeout is None:
        timeout = CONFIG["timeout"]
    print(f"  [MCP] {server}.{tool}: {query[:50]}...")
    try:
        cmd = ["mcporter", "call", f"{server}.{tool}", f"query={query}"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        output = result.stdout.strip()
        
        # 尝试直接解析整个输出
        try:
            data = json.loads(output)
            if data.get("code") == 0:
                return data
        except:
            pass
        
        # 尝试从输出中提取 JSON（处理多行格式）
        json_start = output.find('{')
        json_end = output.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = output[json_start:json_end]
            try:
                data = json.loads(json_str)
                if data.get("code") == 0:
                    return data
            except Exception as e:
                print(f"  [DEBUG] JSON 解析失败：{e}")
        
        return None
    except subprocess.TimeoutExpired:
        print(f"  [WARN] 超时 ({timeout}秒)")
        return None
    except Exception as e:
        print(f"  [ERR] {e}")
        return None


def select_funds(industry: str) -> List[Dict]:
    """筛选行业基金"""
    print(f"\n{'='*60}\n步骤 1: 筛选 {industry} 行业基金\n{'='*60}")
    funds = []
    for query in [f"{industry}基金", f"{industry}主题", industry]:
        result = call_mcp_tool(CONFIG["tool_server"], "FundMultipleFactorFilter", query)
        if result and result.get("results"):
            for r in result["results"]:
                md = r.get("table_markdown", "")
                if md:
                    lines = md.strip().split('\n')
                    for line in lines:
                        if '|---' in line or '证券代码' in line or not line.strip():
                            continue
                        if '|' in line:
                            parts = [p.strip() for p in line.split('|') if p.strip()]
                            if len(parts) >= 2:
                                code = parts[0]
                                name = parts[1] if len(parts) > 1 else ""
                                if code and code.isdigit() and len(code) == 6:
                                    funds.append({"code": code, "name": name})
                                    print(f"    [发现] {code} {name}")
        if len(funds) >= 10:
            break
    seen = set()
    unique = []
    for f in funds:
        if f["code"] not in seen:
            seen.add(f["code"])
            unique.append(f)
    print(f"\n  [OK] 找到 {len(unique)} 只基金")
    return unique[:CONFIG["max_funds"]]


def parse_quarter(quarter_str: str) -> tuple:
    """解析季度字符串"""
    patterns = [
        (r'(\d{4})\s*[Qq]\s*(\d)', lambda y, q: (int(y), int(q))),
        (r'(\d{4})\s*年\s*第？\s*([一二三四])\s*季度', lambda y, q: (int(y), {'一':1,'二':2,'三':3,'四':4}.get(q, 0))),
        (r'(\d{4})\s*年？\s*([1234])\s*季度', lambda y, q: (int(y), int(q))),
    ]
    for pattern, converter in patterns:
        match = re.search(pattern, quarter_str, re.IGNORECASE)
        if match:
            year, quarter = converter(match.group(1), match.group(2))
            if 1 <= quarter <= 4:
                return year, quarter
    raise ValueError(f"无法解析季度格式：{quarter_str}")


def get_fund_reports(fund: Dict, year: int, quarter: int) -> List[Dict]:
    """获取基金报告"""
    reports = []
    for query in [f"{fund['name']}", f"{fund['name']} {year}", f"{fund['code']}"]:
        result = call_mcp_tool(CONFIG["api_server"], "FundAnnouncement", query, timeout=60)
        if result and result.get("results"):
            for r in result["results"]:
                md = r.get("table_markdown", "")
                if md and '|公告 ID|' in md:
                    for line in md.strip().split('\n'):
                        if '|---' in line or '公告 ID' in line or not line.strip():
                            continue
                        if '|' in line:
                            parts = [p.strip() for p in line.split('|') if p.strip()]
                            if len(parts) >= 2 and str(year) in parts[1] and f'第{quarter}季度' in parts[1]:
                                reports.append({
                                    "fund_name": fund["name"], "fund_code": fund["code"],
                                    "title": parts[1], "content": md[:8000]
                                })
                                print(f"    [报告] {parts[1][:50]}")
        if reports:
            break
    return reports


def build_prompt(industry: str, q1_reports: List[Dict], q2_reports: List[Dict], q1_str: str, q2_str: str) -> str:
    """构建分析提示词"""
    aliases = INDUSTRY_ALIASES.get(industry, [industry])
    q1_text = "\n\n".join([f"### {r['fund_name']} ({r['fund_code']})\n{r['content'][:2500]}" for r in q1_reports[:5]])
    q2_text = "\n\n".join([f"### {r['fund_name']} ({r['fund_code']})\n{r['content'][:2500]}" for r in q2_reports[:5]])
    
    return f"""你是一位专业金融分析师。请分析{industry}行业（包括：{', '.join(aliases)}）基金经理在{q1_str}和{q2_str}的观点变化。

## {q1_str} 报告
{q1_text if q1_text else "无数据"}

## {q2_str} 报告
{q2_text if q2_text else "无数据"}

## 任务
输出 JSON 格式：
```json
{{
  "q1_analysis": {{
    "overall_sentiment": "乐观/中性/谨慎",
    "key_themes": ["主题 1", "主题 2"],
    "consensus": [{{"description": "共识", "supporting_funds": ["基金 A", "基金 B"]}}],
    "divergence": [{{"topic": "分歧", "view_a": {{"view": "A", "funds": ["X"]}}, "view_b": {{"view": "B", "funds": ["Y"]}}}}],
    "fund_viewpoints": [{{"fund_name": "基金", "fund_code": "代码", "sentiment": "情绪", "key_points": ["观点"], "themes": ["主题"], "risks": ["风险"]}}],
    "summary": "100 字总结"
  }},
  "q2_analysis": {{ 同上结构 }},
  "comparison": {{
    "sentiment_change": "情绪变化",
    "theme_shift": "主题转移",
    "new_concerns": ["新增担忧"],
    "new_opportunities": ["新增机会"],
    "strategy_change": "策略变化",
    "summary": "200 字核心结论"
  }}
}}
```

要求：1) 共识需至少 2 只基金支持  2) 基于报告内容，不编造  3) 未提及该行业的基金不包含"""


def main():
    if len(sys.argv) < 4:
        print("用法：python3 analyze_viewpoints.py <行业> <季度 1> <季度 2>")
        print("示例：python3 analyze_viewpoints.py 新能源 2025Q3 2025Q4")
        sys.exit(1)
    
    industry, q1_str, q2_str = sys.argv[1], sys.argv[2], sys.argv[3]
    
    print(f"\n{'='*60}\n📊 基金经理观点分析\n{'='*60}\n行业：{industry}\n季度：{q1_str} vs {q2_str}\n{'='*60}\n")
    
    try:
        y1, q1_num = parse_quarter(q1_str)
        y2, q2_num = parse_quarter(q2_str)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    funds = select_funds(industry)
    if not funds:
        print("❌ 未找到基金")
        sys.exit(1)
    
    print(f"\n{'='*60}\n步骤 2: 获取报告\n{'='*60}")
    q1_reports, q2_reports = [], []
    for fund in funds[:10]:
        q1_reports.extend(get_fund_reports(fund, y1, q1_num))
        q2_reports.extend(get_fund_reports(fund, y2, q2_num))
    print(f"\n  Q{q1_num}: {len(q1_reports)} 份 | Q{q2_num}: {len(q2_reports)} 份")
    
    if not q1_reports and not q2_reports:
        print("❌ 未找到报告")
        sys.exit(1)
    
    print(f"\n{'='*60}\n步骤 3: 准备 OpenClaw 语义分析\n{'='*60}")
    prompt = build_prompt(industry, q1_reports, q2_reports, q1_str, q2_str)
    
    # 保存分析请求
    req_file = CONFIG["output_dir"] / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    req_file.write_text(json.dumps({
        "prompt": prompt, 
        "industry": industry, 
        "q1": q1_str, 
        "q2": q2_str, 
        "q1_reports": q1_reports, 
        "q2_reports": q2_reports
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print(f"\n  [OK] 分析请求已保存：{req_file}")
    print(f"\n{'='*60}")
    print("下一步：使用 OpenClaw 进行语义分析")
    print(f"{'='*60}\n")
    print("方法 1 (推荐): 直接将下面的提示词发送给 OpenClaw")
    print("方法 2: 使用 sessions_spawn 创建分析任务\n")
    print("提示词已保存在上述 JSON 文件中，复制 prompt 字段内容即可。\n")
    print("分析完成后，将返回的 JSON 结果保存，然后运行:")
    print(f"  python3 scripts/generate_report.py {req_file.name} <result.json>\n")
    print("="*60)
    print("📋 提示词预览 (前 2000 字):")
    print("="*60)
    print(prompt[:2000])


if __name__ == "__main__":
    main()
