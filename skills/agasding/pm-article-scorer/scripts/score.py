#!/usr/bin/env python3
"""
pm-article-scorer - 启发式评分脚本
基于关键词权重对文章进行评分，无需 API，适合批量初筛和离线使用。
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

# 评分关键词配置
HIGH_WEIGHT_KEYWORDS = [
    "AI", "大模型", "LLM", "Agent", "产品经理", "用户增长",
    "商业化", "开源模型", "编程工具", "ChatGPT", "GPT",
    "Claude", "Gemini", "RAG", "多模态", "向量数据库",
    "AI产品", "AI工具", "AI应用", "AIGC", "AGI"
]

MEDIUM_WEIGHT_KEYWORDS = [
    "产品", "用户", "需求", "定位", "策略", "增长",
    "竞品", "分析", "框架", "方法", "案例", "复盘",
    "PM", "产品设计", "用户体验", "UX", "UI",
    "留存", "转化", "DAU", "MAU", "ARR", "MRR",
    "商业模式", "变现", "定价", "B端", "C端", "SaaS"
]

INDUSTRY_KEYWORDS = [
    "融资", "估值", "平台", "生态", "监管", "出海",
    "竞争", "市场", "行业", "趋势", "投资", "独角兽",
    "上市", "并购", "战略", "壁垒", "护城河"
]

NEGATIVE_KEYWORDS = [
    "震惊", "必看", "深度好文", "刚刚", "突发",
    "99%", "100%", "绝了", "太牛了", "收藏",
    "转发", "扩散", "必读", "曝光", "内幕",
    "重磅", "刚刚宣布", "刚刚传来"
]

INFO_ROUNDUP_PATTERNS = [
    r"本周.{0,10}(速览|汇总|周报|一周)",
    r"今日.{0,10}(速览|汇总)",
    r"\d+条(新闻|资讯|消息)",
    r"(\u591a|\u5468)\u4e2a(\u6848\u4f8b|\u65b0\u95fb|\u5185\u5bb9)",
    r"(\u4e00|\u5468|\u4e07)\u5b57\u5173\u952e",
]

QUALITY_AUTHORS = [
    "赛博禅心", "AGENT橘", "真格基金", "经纬中国",
    "晚点LatePost", "极客公园", "小道消息", "乱翻书"
]

INFO_AUTHORS = [
    "机器之心", "量子位", "AI前线", "新智元",
    "大数据文摘", "BAT"
]


@dataclass
class ScoreResult:
    related_to_ai_pm: bool
    interest_level: str  # high/medium/low
    score: int
    recommendation: str  # 推荐阅读/可选阅读/无需关注
    dimension_scores: dict
    content_type: str
    author_style_preference_match: bool
    is_info_roundup: bool
    tags: list
    reason: list
    summary: str

    def to_dict(self) -> dict:
        return asdict(self)


def extract_title_and_content(text: str) -> tuple[str, str]:
    """从输入文本中分离标题和正文"""
    lines = text.strip().split("\n")
    title = ""
    content_lines = []
    in_content = False

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        # 尝试识别标题（JSON 格式或 Markdown 格式）
        if i == 0 and (len(line) < 80 or line.startswith("#")):
            title = line.lstrip("# ").strip()
            in_content = True
            continue
        if line.startswith("title") or line.startswith('"title"'):
            match = re.search(r'["\u201c](.+?)["\u201d]', line)
            if match:
                title = match.group(1)
            continue
        content_lines.append(line)

    content = " ".join(content_lines)
    return title, content


def detect_info_roundup(title: str, content: str) -> bool:
    """检测是否为资讯整合型内容"""
    combined = title + " " + content
    for pattern in INFO_ROUNDUP_PATTERNS:
        if re.search(pattern, combined):
            return True
    # 多案例拼盘检测
    sentences = re.split(r"[.。;；]", content)
    unique_sources = set()
    for s in sentences:
        if re.search(r"\u6765\u6e90[:：]\s*(\S+)", s):
            unique_sources.add(1)
    if len(unique_sources) >= 3 and len(sentences) > 10:
        return True
    return False


def score_heuristic(title: str, content: str) -> ScoreResult:
    """启发式评分"""
    combined = title + " " + content

    # 基础分
    score = 50

    # 高权重关键词
    high_matches = [kw for kw in HIGH_WEIGHT_KEYWORDS if kw in combined]
    score += min(len(high_matches) * 4, 20)

    # 中权重关键词
    medium_matches = [kw for kw in MEDIUM_WEIGHT_KEYWORDS if kw in combined]
    score += min(len(medium_matches) * 3, 15)

    # 行业关键词
    industry_matches = [kw for kw in INDUSTRY_KEYWORDS if kw in combined]
    score += min(len(industry_matches) * 3, 10)

    # 负面关键词
    neg_matches = [kw for kw in NEGATIVE_KEYWORDS if kw in combined]
    score -= len(neg_matches) * 5

    # 资讯整合型
    is_roundup = detect_info_roundup(title, content)
    if is_roundup:
        score -= 5

    # 优质作者
    author_match = any(author in combined for author in QUALITY_AUTHORS)
    if author_match:
        score += 10

    # 负面作者
    info_author_match = any(author in combined for author in INFO_AUTHORS)
    if info_author_match:
        score -= 5

    # 内容类型判断
    if author_match and len(high_matches) >= 2:
        content_type = "个人深度输出"
    elif industry_matches and medium_matches:
        content_type = "行业分析"
    elif "方法" in combined or "框架" in combined or "模型" in combined:
        content_type = "方法论文章"
    elif is_roundup:
        content_type = "资讯整合"
    elif neg_matches:
        content_type = "营销宣传"
    else:
        content_type = "其他"

    # 维度分估算
    topic_relevance = min(20, len(high_matches) * 4 + len(medium_matches) * 2)
    direct_work_value = min(20, len([k for k in MEDIUM_WEIGHT_KEYWORDS if k in combined]) * 3)
    transferable = min(20, 8 if "方法" in combined or "框架" in combined else 4)
    industry_value = min(15, len(industry_matches) * 3)
    insight = min(10, 6 if len(high_matches) >= 2 else 3)
    originality = min(10, 8 if author_match else (4 if not neg_matches else 2))
    format_adj = 3 if author_match else (-3 if neg_matches or is_roundup else 0)

    dimension_scores = {
        "topic_relevance": topic_relevance,
        "direct_work_value": direct_work_value,
        "transferable_method_value": transferable,
        "industry_business_value": industry_value,
        "insight_density": insight,
        "originality_personal_view": originality,
        "format_adjustment": format_adj
    }

    # 最终分
    score = min(100, max(0, score))

    # 推荐判断
    if score >= 80:
        recommendation = "推荐阅读"
        interest_level = "high"
    elif score >= 60:
        recommendation = "可选阅读"
        interest_level = "medium"
    else:
        recommendation = "无需关注"
        interest_level = "low"

    related_to_ai_pm = score >= 50

    # 生成标签
    tags = high_matches[:5] + medium_matches[:3]

    # 原因
    reasons = []
    if high_matches:
        reasons.append(f"命中高权重词：{', '.join(high_matches[:3])}")
    if author_match:
        reasons.append("优质原创作者")
    if is_roundup:
        reasons.append("内容为资讯整合型")
    if neg_matches:
        reasons.append(f"含营销/流量词：{', '.join(neg_matches[:2])}")
    if not reasons:
        reasons.append("未命中明确关键词")

    # 摘要
    summary = f"{content_type}，评分{score}分，{recommendation}"
    if high_matches:
        summary = f"{high_matches[0]}相关，{summary}"

    return ScoreResult(
        related_to_ai_pm=related_to_ai_pm,
        interest_level=interest_level,
        score=score,
        recommendation=recommendation,
        dimension_scores=dimension_scores,
        content_type=content_type,
        author_style_preference_match=author_match,
        is_info_roundup=is_roundup,
        tags=tags,
        reason=reasons,
        summary=summary
    )


def parse_input_file(path: str) -> tuple[str, str]:
    """解析输入文件"""
    path = Path(path)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    content = path.read_text(encoding="utf-8")

    # JSON 格式
    if path.suffix == ".json":
        try:
            data = json.loads(content)
            title = data.get("title", "")
            text = data.get("content", "") or data.get("text", "")
            return title, text
        except json.JSONDecodeError:
            pass

    # Markdown 或纯文本
    return extract_title_and_content(content)


def score_file(input_path: str) -> ScoreResult:
    """对单个文件评分"""
    title, content = parse_input_file(input_path)
    return score_heuristic(title, content)


def batch_score(input_dir: str, output_path: str, output_format: str = "jsonl"):
    """批量评分"""
    input_dir = Path(input_dir)
    results = []

    for path in input_dir.rglob("*"):
        if path.suffix.lower() in [".txt", ".json", ".md"]:
            try:
                result = score_file(str(path))
                result_dict = result.to_dict()
                result_dict["_file"] = str(path)
                results.append(result_dict)
            except Exception as e:
                print(f"Warning: Failed to score {path}: {e}", file=sys.stderr)

    if output_format == "csv":
        import csv
        if not results:
            return
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            for r in results:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Scored {len(results)} articles. Results saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="PM Article Scorer - 启发式评分脚本")
    parser.add_argument("--input", "-i", help="输入文章文件路径")
    parser.add_argument("--batch", "-b", help="批量评分目录")
    parser.add_argument("--output", "-o", default="scores.jsonl", help="输出文件路径")
    parser.add_argument("--format", "-f", choices=["jsonl", "csv"], default="jsonl", help="输出格式")
    parser.add_argument("--mode", "-m", choices=["heuristic"], default="heuristic", help="评分模式")

    args = parser.parse_args()

    if args.batch:
        batch_score(args.batch, args.output, args.format)
    elif args.input:
        result = score_file(args.input)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        # 交互模式：读取 stdin
        text = sys.stdin.read()
        if not text.strip():
            print("Usage: echo '文章内容' | python score.py")
            sys.exit(1)
        title, content = extract_title_and_content(text)
        result = score_heuristic(title, content)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
