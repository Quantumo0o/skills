#!/usr/bin/env python3
"""
🚀 Module 3: Structured Path Injector (结构化图注入)
================================================
解决痛点：全量原文注入导致信噪比 (SNR) 骤降和 Token 爆炸。
机制：
- **骨架提取 (Skeleton Extraction)**: 不注入大段原文，只保留 `[Node] --(relation)--> [Node]` 路径。
- **延迟加载 (Lazy Loading)**: 仅注入摘要，除非明确需要，否则不加载完整 Content。
- **Token 估算**: 精确计算结构化字符串的 Token 消耗。
"""

import re

class StructuredPathInjector:
    def __init__(self, tokenizer_name="cl100k_base"):
        self.tokenizer_name = tokenizer_name
        # 尝试加载 tiktoken，如果失败则使用估算器
        try:
            import tiktoken
            self.tokenizer = tiktoken.get_encoding(tokenizer_name)
            self.use_tiktoken = True
        except ImportError:
            self.use_tiktoken = False

    def estimate_tokens(self, text: str) -> int:
        if self.use_tiktoken:
            return len(self.tokenizer.encode(text))
        return int(len(text) * 0.4)  # 估算回退

    def inject(self, path: list[dict], load_full: bool = False) -> tuple[str, int]:
        """
        构建结构化的路径字符串
        Args:
            path: List of node dicts in order
            load_full: If True, append full content of the final node
        Returns:
            (formatted_string, token_count)
        """
        if not path: return "", 0
        
        # 1. 构建骨架
        parts = []
        for i, node in enumerate(path):
            # 提取核心摘要 (前 100 字)
            summary = node.get('content', '')[:80].replace('\n', ' ')
            parts.append(f"[{node['id']}] ({node.get('type', 'unknown')}) {summary}")
            
            # 关系链接
            if i < len(path) - 1:
                next_node = path[i+1]
                parts.append(f" --(relates_to)--> ")
        
        structure_text = "".join(parts)
        
        # 2. 延迟加载 (Lazy Load Final Node)
        final_token_cost = 0
        final_text = ""
        
        if load_full and path:
            final_content = path[-1].get('content', '')
            final_text = f"\n\n>>> [Target Deep Read] {final_content}"
            final_token_cost = self.estimate_tokens(final_text)
            
        structure_token_cost = self.estimate_tokens(structure_text)
        total_cost = structure_token_cost + final_token_cost
        
        return structure_text + final_text, total_cost
