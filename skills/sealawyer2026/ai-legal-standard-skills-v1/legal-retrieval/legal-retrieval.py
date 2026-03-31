#!/usr/bin/env python3
"""
法律检索技能 (Legal Retrieval Skill)
基于 PossibLaw possiblaw-legal 设计理念

功能：
- 多数据源搜索（知识库 + 外部API）
- 混合排名算法（语义 + 关键词 + 来源优先级）
- 带引用的证据包输出
- 降级模式支持
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import Counter
import argparse


@dataclass
class Evidence:
    """证据项"""
    rank: int
    title: str
    source_type: str
    source_url: str
    score: float
    excerpt: str
    keywords: List[str]
    tags: List[str]
    metadata: Dict[str, Any] = None

    def to_dict(self):
        return asdict(self)


@dataclass
class RetrievalResult:
    """检索结果"""
    query: str
    timestamp: str
    sources: List[str]
    mode: str
    summary: str
    evidence: List[Evidence]
    total: int
    retrieved: int
    degraded_notes: Optional[str] = None

    def to_dict(self):
        return asdict(self)


class KnowledgeBaseAdapter:
    """知识库适配器"""

    def __init__(self, kb_path: str):
        self.kb_path = Path(kb_path)
        self.source_priority = {
            "regulations": 0.95,  # 法规库
            "cases": 0.95,         # 案例库
            "contracts": 0.95,     # 合同库
            "documents": 0.90,     # 文书库
            "reference": 0.90      # 参考库
        }

    def search(self, query: str, limit: int = 10) -> List[Evidence]:
        """在知识库中搜索"""
        evidence_list = []
        query_keywords = self._extract_keywords(query)

        # 遍历知识库目录
        for category_dir in self.kb_path.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith('.'):
                continue

            # 确定来源类型
            source_type = self._get_source_type(category_dir.name)
            if source_type not in self.source_priority:
                continue

            # 递归搜索文档
            evidence_list.extend(
                self._search_directory(category_dir, query, query_keywords, source_type)
            )

        # 排序和限制结果数量
        evidence_list.sort(key=lambda x: x.score, reverse=True)
        return evidence_list[:limit]

    def _search_directory(
        self,
        directory: Path,
        query: str,
        query_keywords: List[str],
        source_type: str
    ) -> List[Evidence]:
        """递归搜索目录"""
        evidence_list = []

        for item in directory.iterdir():
            if item.is_dir():
                # 递归子目录
                evidence_list.extend(
                    self._search_directory(item, query, query_keywords, source_type)
                )
            elif item.suffix in ['.md', '.txt']:
                # 处理文档文件
                evidence = self._search_file(item, query, query_keywords, source_type)
                if evidence:
                    evidence_list.append(evidence)

        return evidence_list

    def _search_file(
        self,
        file_path: Path,
        query: str,
        query_keywords: List[str],
        source_type: str
    ) -> Optional[Evidence]:
        """搜索单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取标题（第一行）
            lines = content.split('\n')
            title = lines[0].replace('#', '').strip()
            if not title:
                title = file_path.stem

            # 计算语义相似度（简化版，基于关键词重叠）
            semantic_score = self._calculate_semantic_similarity(query, content)

            # 计算关键词匹配分数
            keyword_score = self._calculate_keyword_score(query_keywords, content)

            # 来源优先级
            source_priority = self.source_priority.get(source_type, 0.85)

            # 混合评分
            final_score = (
                0.55 * semantic_score +
                0.30 * keyword_score +
                0.15 * source_priority
            )

            # 最低分数过滤
            if final_score < 0.3:
                return None

            # 提取摘要
            excerpt = self._extract_excerpt(content, query_keywords, max_length=200)

            # 提取标签
            tags = self._extract_tags(content)

            # 相对路径
            relative_path = file_path.relative_to(self.kb_path.parent.parent)
            source_url = f"/{relative_path}"

            return Evidence(
                rank=0,  # 稍后设置
                title=title,
                source_type=source_type,
                source_url=str(source_url),
                score=final_score,
                excerpt=excerpt,
                keywords=query_keywords[:5],  # 最多保留5个关键词
                tags=tags,
                metadata={"file_path": str(file_path), "file_size": len(content)}
            )

        except Exception as e:
            print(f"警告: 无法读取文件 {file_path}: {e}")
            return None

    def _extract_keywords(self, query: str) -> List[str]:
        """提取查询关键词"""
        # 简单分词（实际应该使用jieba等中文分词库）
        keywords = re.findall(r'[\w]+', query.lower())
        # 过滤常见停用词
        stopwords = {'的', '和', '或', '是', '在', '有', '了', 'for', 'and', 'or', 'the', 'is'}
        return [k for k in keywords if k not in stopwords and len(k) > 1]

    def _calculate_semantic_similarity(self, query: str, content: str) -> float:
        """计算语义相似度（简化版）"""
        query_lower = query.lower()
        content_lower = content.lower()

        # 简单的词重叠度计算
        query_words = set(self._extract_keywords(query))
        content_words = set(self._extract_keywords(content))

        if not query_words:
            return 0.0

        intersection = query_words.intersection(content_words)
        return len(intersection) / len(query_words) if query_words else 0.0

    def _calculate_keyword_score(self, keywords: List[str], content: str) -> float:
        """计算关键词匹配分数"""
        if not keywords:
            return 0.0

        content_lower = content.lower()
        matches = sum(1 for kw in keywords if kw.lower() in content_lower)
        return matches / len(keywords)

    def _extract_excerpt(self, content: str, keywords: List[str], max_length: int = 200) -> str:
        """提取包含关键词的摘要"""
        if not keywords:
            return content[:max_length]

        # 查找包含关键词的段落
        paragraphs = content.split('\n\n')
        keyword_lower = [kw.lower() for kw in keywords]

        for paragraph in paragraphs:
            paragraph_lower = paragraph.lower()
            if any(kw in paragraph_lower for kw in keyword_lower):
                if len(paragraph) <= max_length:
                    return paragraph
                else:
                    return paragraph[:max_length] + "..."

        # 如果没有找到，返回第一段
        return paragraphs[0][:max_length] + "..." if len(paragraphs[0]) > max_length else paragraphs[0]

    def _extract_tags(self, content: str) -> List[str]:
        """提取标签"""
        tags = []

        # 从元数据中提取标签（如果有）
        metadata_match = re.search(r'Tags:\s*\[([^\]]+)\]', content)
        if metadata_match:
            tags_str = metadata_match.group(1)
            tags = [tag.strip().strip('"\'') for tag in tags_str.split(',')]

        return tags

    def _get_source_type(self, dir_name: str) -> Optional[str]:
        """根据目录名确定来源类型"""
        mapping = {
            "01-案例库": "cases",
            "02-法规库": "regulations",
            "03-合同库": "contracts",
            "04-文书库": "documents",
            "05-指引库": "guide",
            "06-参考库": "reference",
            "07-行业规范库": "reference"
        }
        return mapping.get(dir_name)


class LegalRetrieval:
    """法律检索引擎"""

    def __init__(self, kb_path: str = None):
        self.kb_path = kb_path or os.environ.get(
            'KNOWLEDGE_BASE_PATH',
            '/workspace/projects/agents/legal-ai-team/knowledge-base'
        )
        self.kb_adapter = KnowledgeBaseAdapter(self.kb_path)
        self.cache = {}  # 简单的内存缓存

    def search(
        self,
        query: str,
        sources: Optional[List[str]] = None,
        limit: int = 10,
        output_format: str = "json"
    ) -> RetrievalResult:
        """
        执行法律检索

        Args:
            query: 查询字符串
            sources: 数据源列表（如 ['regulations', 'cases']），None 表示所有
            limit: 返回结果数量限制
            output_format: 输出格式（'json' 或 'human'）

        Returns:
            RetrievalResult 检索结果
        """
        # 检查缓存
        cache_key = self._get_cache_key(query, sources, limit)
        if cache_key in self.cache:
            return self.cache[cache_key]

        # 执行检索
        evidence = self.kb_adapter.search(query, limit)

        # 如果需要，按来源过滤
        if sources:
            evidence = [e for e in evidence if e.source_type in sources]

        # 设置排名
        for i, ev in enumerate(evidence, 1):
            ev.rank = i

        # 构建结果
        result = RetrievalResult(
            query=query,
            timestamp=datetime.now().isoformat(),
            sources=sources or ["all"],
            mode="full",
            summary=f"找到 {len(evidence)} 条相关文档，按相关性排序",
            evidence=evidence,
            total=len(evidence),
            retrieved=min(limit, len(evidence))
        )

        # 缓存结果
        self.cache[cache_key] = result

        return result

    def batch_search(
        self,
        queries: List[str],
        sources: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[RetrievalResult]:
        """批量检索"""
        results = []
        for query in queries:
            result = self.search(query, sources, limit)
            results.append(result)
        return results

    def _get_cache_key(self, query: str, sources: Optional[List[str]], limit: int) -> str:
        """生成缓存键"""
        key_str = f"{query}:{sources}:{limit}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()


def format_human(result: RetrievalResult) -> str:
    """格式化为人性化输出"""
    lines = [
        "📋 检索结果",
        "",
        f"查询: {result.query}",
        f"来源: {', '.join(result.sources)}",
        f"找到: {result.total} 条相关文档",
        f"显示: 前 {result.retrieved} 条",
        "",
        "---"
    ]

    for ev in result.evidence:
        lines.extend([
            "",
            f"🥇 第{ev.rank}条 [相关性: {ev.score:.2f}]",
            "",
            f"**{ev.title}**",
            f"📂 {ev.source_type}",
            f"🔗 {ev.source_url}",
            "",
            f"📝 摘要:",
            f"{ev.excerpt}",
            "",
            f"🏷️ 标签: {', '.join(ev.tags)}" if ev.tags else "",
            f"🔑 关键词: {', '.join(ev.keywords)}" if ev.keywords else "",
            ""
        ])

    return "\n".join(lines)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="法律检索技能")
    parser.add_argument("query", nargs="?", help="查询字符串")
    parser.add_argument("--sources", nargs="+", help="数据源列表（如 regulations cases）")
    parser.add_argument("--limit", type=int, default=10, help="返回结果数量限制")
    parser.add_argument("--output", choices=["json", "human"], default="json", help="输出格式")
    parser.add_argument("--kb-path", help="知识库路径")
    parser.add_argument("--clear-cache", action="store_true", help="清空缓存")

    args = parser.parse_args()

    # 初始化检索引擎
    retriever = LegalRetrieval(args.kb_path)

    # 清空缓存
    if args.clear_cache:
        retriever.clear_cache()
        print("缓存已清空")
        return

    # 检查查询参数
    if not args.query:
        parser.print_help()
        return

    # 执行检索
    result = retriever.search(
        query=args.query,
        sources=args.sources,
        limit=args.limit,
        output_format=args.output
    )

    # 输出结果
    if args.output == "json":
        # 转换 Evidence 对象为字典
        result_dict = result.to_dict()
        result_dict["evidence"] = [ev.to_dict() for ev in result.evidence]
        print(json.dumps(result_dict, ensure_ascii=False, indent=2))
    else:
        print(format_human(result))


if __name__ == "__main__":
    main()
