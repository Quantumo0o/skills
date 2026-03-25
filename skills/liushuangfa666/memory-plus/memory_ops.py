#!/usr/bin/env python3
"""
Memory Workflow Operations

功能：
1. 搜索记忆：向量 + BM25 混合检索 + HyDE + Query Rewriting + RRF 重排 + rerank
2. 存储记忆：自动存入 Milvus / 文件系统
3. 外部对接：Ollama embedding、rerank 服务、MiniMax HyDE/Query改写
"""

import json
import os
import sys
import re
import math
import argparse
import threading
import time
import requests
from datetime import datetime
from typing import Optional, List, Dict, Tuple
from collections import Counter

# ==================== 配置 ====================
WORKSPACE = os.getenv("WORKSPACE", "/home/node/.openclaw/workspace")

# 加载 secrets 配置
OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
ENV_FILE = os.path.join(OPENCLAW_DIR, ".env")
if os.path.exists(ENV_FILE):
    for line in open(ENV_FILE):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()

# 数据存储目录（与 skill 代码分离，用户可自定义）
MEMORY_WORKFLOW_DATA = os.getenv(
    "MEMORY_WORKFLOW_DATA",
    os.path.join(os.path.expanduser("~/.openclaw"), "memory-workflow-data")
)
os.makedirs(MEMORY_WORKFLOW_DATA, exist_ok=True)

MEMORY_DIR = os.path.join(MEMORY_WORKFLOW_DATA, "memories")
STATE_FILE = os.path.join(MEMORY_WORKFLOW_DATA, "memory_state.json")
HOT_SESSIONS_FILE = os.path.join(MEMORY_WORKFLOW_DATA, "hot_sessions.json")

# Ollama 配置（必须：embedding 服务）
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "bge-m3:latest")
QUERY_PREFIX = "query: "

# Rerank 配置（可选）
RERANK_SERVICE_URL = os.getenv("RERANK_SERVICE_URL", "http://172.17.0.1:18778")

# Milvus 配置
MILVUS_URI = os.getenv("MILVUS_URI", "http://host.docker.internal:19530")
USE_MILVUS = os.getenv("USE_MILVUS", "").lower() == "true"

# MiniMax API（用于 HyDE + Query Rewriting）
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")

# MiniMax 限速器：40次/分钟
class RateLimiter:
    """简单的时间窗口限速器"""
    def __init__(self, calls_per_minute=40):
        self.interval = 60.0 / calls_per_minute
        self.last_call = 0.0
        self.lock = threading.Lock()

    def wait(self):
        """等待直到可以发起下一次请求"""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_call
            if elapsed < self.interval:
                time.sleep(self.interval - elapsed)
            self.last_call = time.time()

_minimax_limiter = RateLimiter(calls_per_minute=40)
MINIMAX_BASE_URL = os.getenv("MINIMAX_BASE_URL", "https://api.minimaxi.com/v1")

# 阈值配置
HOT_SESSION_LIMIT = 10
IDLE_THRESHOLD_MINUTES = 10
AUTO_STORE_INTERVAL = 600  # 10分钟

# 搜索配置
RRF_K = 60
OVERSEARCH_MULTIPLIER = 8
KEYWORD_WEIGHT = 0.3

# 分块配置
CHUNK_TOKEN_LIMIT = 500       # 每块最大 token 数
CHUNK_OVERLAP_TOKENS = 50    # 相邻块重叠 token 数
MIN_CHUNK_TOKENS = 100        # 低于此值不单独分块（太短的片段不切）

# ==================== 单例模式 ====================
_memory_workflow = None
_init_lock = threading.Lock()


def get_instance():
    global _memory_workflow
    if _memory_workflow is None:
        with _init_lock:
            if _memory_workflow is None:
                _memory_workflow = MemoryWorkflow()
    return _memory_workflow


# ==================== 工具函数 ====================

def cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def normalize_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """将分数归一化到 [0, 1]"""
    if not scores:
        return scores
    values = list(scores.values())
    max_s, min_s = max(values), min(values)
    if max_s == min_s:
        return {k: 0.5 for k in scores}
    return {k: (v - min_s) / (max_s - min_s) for k, v in scores.items()}


# ==================== MemoryWorkflow ====================

class MemoryWorkflow:
    def __init__(self):
        self.ollama_url = OLLAMA_URL
        self.ollama_model = OLLAMA_MODEL
        self.use_milvus = USE_MILVUS

        os.makedirs(MEMORY_DIR, exist_ok=True)

        # 检测 Ollama 是否可用（启动时检查一次，不反复探测）
        self._ollama_available = self._detect_ollama()
        if not self._ollama_available:
            print("⚠️ Ollama 不可用，记忆搜索降级为轻量模式（BM25）")

        self._store_thread = None
        self._stop_event = threading.Event()
        self._start_auto_store()

    def _detect_ollama(self) -> bool:
        """检测 Ollama 服务是否可用"""
        try:
            r = requests.get(f"{self.ollama_url}/api/tags", timeout=3)
            return r.status_code == 200
        except Exception:
            return False

    def _start_auto_store(self):
        if self._store_thread is None or not self._store_thread.is_alive():
            self._stop_event.clear()
            self._store_thread = threading.Thread(target=self._auto_store_worker, daemon=True)
            self._store_thread.start()

    def _auto_store_worker(self):
        while not self._stop_event.is_set():
            try:
                self._stop_event.wait(AUTO_STORE_INTERVAL)
                if self._stop_event.is_set():
                    break

                state = self.check()
                if state.get("idle_minutes", 0) >= IDLE_THRESHOLD_MINUTES:
                    self.store(topic="auto")
            except Exception as e:
                print(f"⚠️ 自动存储失败: {e}", file=sys.stderr)

    def stop(self):
        self._stop_event.set()
        if self._store_thread:
            self._store_thread.join(timeout=5)

    # ==================== Ollama Embedding ====================

    def get_embedding(self, text: str) -> Optional[List[float]]:
        """调用 Ollama embedding 服务，获取文本向量（Ollama 不可用时返回 None）"""
        if not self._ollama_available:
            return None
        try:
            response = requests.post(
                f"{self.ollama_url}/api/embed",
                json={"model": self.ollama_model, "input": QUERY_PREFIX + text},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                embeddings = data.get("embeddings", [])
                if embeddings:
                    return embeddings[0]
        except Exception as e:
            print(f"⚠️ Embedding 失败: {e}", file=sys.stderr)
        return None

    # ==================== Rerank ====================

    def rerank(self, query: str, candidates: List[Dict], top_n: int = 5) -> List[Dict]:
        """调用 rerank 服务重新排序
        
        Args:
            query: 原始查询
            candidates: 候选文档列表 [{"id": ..., "content": ...}, ...]
            top_n: 返回前 n 条
        
        Returns:
            重排后的结果 [{"id": ..., "content": ..., "rerank_score": ...}, ...]
        """
        if not RERANK_SERVICE_URL or not candidates:
            return candidates[:top_n]

        try:
            documents = [c.get("content", "") for c in candidates]
            response = requests.post(
                f"{RERANK_SERVICE_URL}/rerank",
                json={"query": query, "documents": documents, "top_k": top_n},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                
                reranked = []
                for item in results:
                    idx = item.get("index", 0)
                    score = item.get("relevance_score", 0.0)
                    if 0 <= idx < len(candidates):
                        candidate = dict(candidates[idx])
                        candidate["rerank_score"] = score
                        reranked.append(candidate)
                return reranked
        except Exception as e:
            print(f"⚠️ Rerank 失败: {e}", file=sys.stderr)
        
        return candidates[:top_n]

    # ==================== BM25 ====================

    def tokenize(self, text: str) -> List[str]:
        """中文 2-gram + 英文分词"""
        text = text.lower()
        chinese = re.findall(r'[\u4e00-\u9fff]', text)
        chinese_words = [''.join(chinese[i:i+2]) for i in range(len(chinese)-1)]
        english = re.findall(r'[a-z0-9]+', text)
        return chinese_words + english

    def _estimate_tokens(self, text: str) -> int:
        """估算中英混合文本的 token 数（保守估算）"""
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        non_chinese = len(text) - chinese_chars
        return int(chinese_chars * 0.5 + non_chinese * 0.25)

    def _chunk_text(self, text: str) -> List[Dict]:
        """将长文本切分为重叠的语义块

        Returns:
            [{"content": str, "start": int, "end": int}, ...]
            start/end 为字符偏移量
        """
        total_tokens = self._estimate_tokens(text)
        if total_tokens <= MIN_CHUNK_TOKENS:
            return [{"content": text, "start": 0, "end": len(text)}]

        chunks = []
        char_pos = 0
        text_len = len(text)

        # 句子分隔符（优先在这里切）
        sentence_delimiters = re.compile(r'[。！？；\n]')

        while char_pos < text_len:
            # 取 CHUNK_TOKEN_LIMIT tokens 对应的字符数（约2倍）
            # 保守估计：每个token约0.5个中文字符
            chunk_end = min(char_pos + CHUNK_TOKEN_LIMIT * 2, text_len)

            if chunk_end < text_len:
                # 找最近的自然断点
                search_start = max(char_pos, chunk_end - 100)
                delimiters_found = list(sentence_delimiters.finditer(text, search_start, chunk_end))
                if delimiters_found:
                    last_delim = delimiters_found[-1]
                    chunk_end = last_delim.end()

            chunk_text = text[char_pos:chunk_end].strip()
            if chunk_text:
                chunks.append({"content": chunk_text, "start": char_pos, "end": chunk_end})

            # 重叠：如果已经是最后一块则不再继续
            if chunk_end >= text_len:
                break

            # 计算下一块起始位置（去除重叠部分）
            # 先找到重叠区的断点
            overlap_start = chunk_end - CHUNK_OVERLAP_TOKENS * 2
            if overlap_start > char_pos:
                # 重叠区内找句子断点作为下一块起始
                search_start = max(char_pos, overlap_start)
                delimiters_in_overlap = list(sentence_delimiters.finditer(text, search_start, chunk_end))
                if delimiters_in_overlap:
                    char_pos = delimiters_in_overlap[-1].end()
                else:
                    char_pos = max(char_pos + (CHUNK_TOKEN_LIMIT - CHUNK_OVERLAP_TOKENS) * 2,
                                  chunk_end - CHUNK_OVERLAP_TOKENS * 2)
            else:
                char_pos = chunk_end

        return chunks

    def calc_bm25(self, query_tokens: List[str], candidates: List[Dict]) -> Dict[str, float]:
        """计算 BM25 分数"""
        if not query_tokens:
            return {}

        doc_freqs = Counter()
        doc_lens = {}
        all_tokens = {}

        for mem in candidates:
            tokens = self.tokenize(mem.get("content", ""))
            mem_id = mem["id"]
            doc_lens[mem_id] = len(tokens)
            all_tokens[mem_id] = tokens
            for t in set(tokens):
                doc_freqs[t] += 1

        N = len(candidates)
        avg_len = sum(doc_lens.values()) / N if N > 0 else 1

        scores = {}
        k1, b = 1.5, 0.75

        for mem_id, tokens in all_tokens.items():
            score = 0.0
            tf = Counter(tokens)

            for token in query_tokens:
                if token not in tf:
                    continue
                df = doc_freqs.get(token, 0)
                if df == 0:
                    continue

                idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
                tf_val = tf[token]
                numerator = tf_val * (k1 + 1)
                denominator = tf_val + k1 * (1 - b + b * doc_lens[mem_id] / avg_len)
                score += idf * numerator / denominator

            if score > 0:
                scores[mem_id] = score

        return normalize_scores(scores)

    # ==================== HyDE + Query Rewriting ====================

    def _call_minimax(self, prompt: str, temperature: float = 0.8) -> Optional[str]:
        """调用 MiniMax API（用于 HyDE + Query Rewriting）"""
        if not MINIMAX_API_KEY:
            return None

        _minimax_limiter.wait()  # 限速：40次/分钟

        try:
            response = requests.post(
                f"{MINIMAX_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {MINIMAX_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "M2-her",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 200,
                    "temperature": temperature,
                    "thinking": {"type": "off"}
                },
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                return content.strip() if content else None
            else:
                print(f"⚠️ MiniMax API 错误: {response.status_code}", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ MiniMax API 调用失败: {e}", file=sys.stderr)
        return None

    def _call_ollama_chat(self, prompt: str, temperature: float = 0.8) -> Optional[str]:
        """调用 Ollama chat（备用）"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": "qwen3.5:latest",
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "options": {"temperature": temperature} if temperature > 0 else {}
                },
                timeout=60
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("message", {}).get("content", "").strip()
        except Exception as e:
            print(f"⚠️ Ollama chat 失败: {e}", file=sys.stderr)
        return None

    def _call_llm(self, prompt: str, temperature: float = 0.8) -> Optional[str]:
        """统一 LLM 调用，优先 MiniMax，fallback Ollama"""
        result = self._call_minimax(prompt, temperature)
        if result:
            return result
        return self._call_ollama_chat(prompt, temperature)

    def _clean_thinking(self, text: str) -> str:
        """移除 LLM 的思考块"""
        return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

    def generate_hypothetical_doc(self, query: str) -> Optional[str]:
        """HyDE: 根据查询生成假设文档"""
        prompt = f"请根据以下查询生成一段假设性的回答，该回答用于检索增强。请用中文生成一段50字左右的假设答案，直接输出答案内容，不需要前缀说明。\n\n查询：{query}"
        result = self._call_llm(prompt, temperature=0.8)
        return self._clean_thinking(result) if result else None

    def rewrite_query(self, query: str) -> List[str]:
        """Query Rewriting: 生成多个查询变体"""
        rewrites = [query]
        
        prompt = f"请为以下查询生成3个同义或相关的查询变体，用换行分隔。不要加编号或说明，直接输出查询词，每行一个。\n\n查询：{query}"
        result = self._call_llm(prompt, temperature=0.8)
        
        if result:
            result = self._clean_thinking(result)
            lines = [l.strip() for l in result.split('\n') if l.strip()]
            
            skip_patterns = ["查询", "同义", "变体", "答案", "如下", "包括"]
            
            for line in lines:
                if any(p in line for p in skip_patterns):
                    continue
                line = line.lstrip('0123456789.-*））#* ').strip()
                line = line.rstrip('。.,;:、，；')
                if line and line not in rewrites and 2 < len(line) < 40:
                    rewrites.append(line)
        
        return rewrites[:4]

    def query_expansion(self, query: str) -> Dict[str, any]:
        """Query Expansion: 生成多个查询向量（Ollama 不可用时跳过）"""
        if not self._ollama_available:
            return {"original": None, "hyde": None, "rewrites": []}

        embeddings = {"original": None, "hyde": None, "rewrites": []}

        # 原始查询
        emb = self.get_embedding(query)
        if emb:
            embeddings["original"] = emb

        # HyDE
        hyde_doc = self.generate_hypothetical_doc(query)
        if hyde_doc:
            hyde_emb = self.get_embedding(hyde_doc)
            if hyde_emb:
                embeddings["hyde"] = hyde_emb

        # Query Rewriting
        rewrites = self.rewrite_query(query)
        for rewrite in rewrites[1:]:
            rewrite_emb = self.get_embedding(rewrite)
            if rewrite_emb:
                embeddings["rewrites"].append(rewrite_emb)

        return embeddings

    # ==================== 存储 ====================

    def store(self, session_content: str = None, topic: str = "general") -> Dict:
        """存储记忆到向量数据库（支持分块）

        Returns:
            {"success": True, "memory_id": <parent_id>, "chunks": <num_chunks>}
        """
        if not session_content:
            session_content = f"[{datetime.now().isoformat()}] 新对话开始"

        chunks = self._chunk_text(session_content)
        num_chunks = len(chunks)

        if num_chunks == 1:
            # 短内容：直接存，不走分块逻辑
            embedding = self.get_embedding(session_content)
            if self.use_milvus:
                memory_id = self._save_to_milvus(session_content, topic, embedding)
            else:
                memory_id = self._save_to_filesystem(session_content, topic, embedding)
        else:
            # 长内容：先存 parent，再存各 chunk
            # parent 的 content 就是完整原文（用于回溯和展示）
            parent_id = str(time.time()) + "_p"
            if self.use_milvus:
                self._save_to_milvus(session_content, topic,
                                     self.get_embedding(session_content),
                                     parent_id=parent_id, chunk_index=0)
                memory_id = parent_id
            else:
                self._save_to_filesystem(session_content, topic,
                                         self.get_embedding(session_content),
                                         parent_id=parent_id, chunk_index=0)

            # 存各个 chunk
            for i, chunk in enumerate(chunks):
                chunk_emb = self.get_embedding(chunk["content"])
                if self.use_milvus:
                    self._save_to_milvus(chunk["content"], topic, chunk_emb,
                                        parent_id=parent_id, chunk_index=i + 1)
                else:
                    self._save_to_filesystem(chunk["content"], topic, chunk_emb,
                                            parent_id=parent_id, chunk_index=i + 1)

        self._update_hot_sessions(memory_id if num_chunks > 1 else memory_id,
                                  session_content[:200])
        return {"success": True, "memory_id": parent_id if num_chunks > 1 else memory_id,
                "chunks": num_chunks}

    def _save_to_filesystem(self, content: str, topic: str, embedding: List[float],
                            parent_id: str = None, chunk_index: int = 0) -> str:
        memory_id = str(datetime.now().timestamp())
        if parent_id:
            memory_id = f"{parent_id}_c{chunk_index}"

        memory_file = os.path.join(MEMORY_DIR, f"{memory_id}.json")

        with open(memory_file, "w", encoding="utf-8") as f:
            json.dump({
                "id": memory_id,
                "content": content,
                "topic": topic,
                "timestamp": datetime.now().isoformat(),
                "embedding": embedding or [],
                "parent_id": parent_id,   # None 表示是顶层记忆
                "chunk_index": chunk_index  # 0=顶层记忆，1+=分块
            }, f, ensure_ascii=False)

        self._update_state()
        return memory_id

    def _save_to_milvus(self, content: str, topic: str, embedding: List[float],
                         parent_id: str = None, chunk_index: int = 0) -> str:
        from pymilvus import Collection, connections

        connections.connect(host='host.docker.internal', port='19530', alias='default')
        collection = Collection('memory_workflow')
        collection.load()

        memory_id = str(time.time())
        if parent_id:
            memory_id = f"{parent_id}_c{chunk_index}"

        collection.insert(data=[{
            "vector": embedding or [0] * 1024,
            "content": content,
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "parent_id": parent_id or "",
            "chunk_index": chunk_index
        }])
        collection.flush()
        connections.disconnect('default')

        self._update_state()
        return memory_id

    def _update_state(self):
        state = {
            "last_store_time": datetime.now().isoformat(),
            "total_memories": self.count_memories()
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False)

    def count_memories(self) -> int:
        if self.use_milvus:
            from pymilvus import Collection, connections
            try:
                connections.connect(host='host.docker.internal', port='19530', alias='default')
                collection = Collection('memory_workflow')
                collection.load()
                count = collection.num_entities
                connections.disconnect('default')
                return count
            except:
                return 0
        else:
            return len([f for f in os.listdir(MEMORY_DIR) if f.endswith('.json')])

    def _update_hot_sessions(self, memory_id: str, content: str):
        hot_sessions = self.get_hot_sessions()
        new_session = {"id": memory_id, "content": content, "timestamp": datetime.now().isoformat()}
        hot_sessions.insert(0, new_session)
        if len(hot_sessions) > HOT_SESSION_LIMIT:
            hot_sessions = hot_sessions[:HOT_SESSION_LIMIT]
        with open(HOT_SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(hot_sessions, f, ensure_ascii=False)

    # ==================== 搜索 ====================

    def search(self, query: str, limit: int = 5) -> Dict:
        """混合搜索主流程：
        1. Query Expansion（HyDE + Query Rewriting）
        2. 向量 + BM25 混合检索（RRF 融合）
        3. Rerank 重新排序
        """
        if not query:
            return {"results": [], "count": 0}

        # 1. Query Expansion
        expansions = self.query_expansion(query)
        expansion_info = {
            "original": expansions["original"] is not None,
            "hyde": expansions["hyde"] is not None,
            "rewrites": len(expansions["rewrites"])
        }

        # 2. 获取候选（oversearch 扩大候选池）
        candidates = self._get_candidates(limit * OVERSEARCH_MULTIPLIER)
        if not candidates:
            return {"results": [], "count": 0, "expansion_info": expansion_info}

        # 3. 构建多向量列表
        all_embeddings = []
        if expansions["original"]:
            all_embeddings.append(("original", expansions["original"]))
        if expansions["hyde"]:
            all_embeddings.append(("hyde", expansions["hyde"]))
        for i, emb in enumerate(expansions["rewrites"]):
            all_embeddings.append((f"rewrite_{i}", emb))

        # 4. 两阶段精排搜索
        if not self._ollama_available:
            # 轻量模式：无 Ollama，仅用 BM25 + 关键词匹配
            results = self._bm25_only_search(query, candidates, limit=limit)
            search_type = "bm25_only"
        else:
            results = self._two_stage_search(query, candidates, all_embeddings, limit=limit)
            search_type = "two_stage_rerank"

        return {
            "results": results,
            "count": len(results),
            "search_type": search_type,
            "expansion_info": expansion_info
        }

    def _get_candidates(self, limit: int) -> List[Dict]:
        if self.use_milvus:
            return self._get_candidates_milvus(limit)
        return self._get_candidates_filesystem(limit)

    def _get_candidates_milvus(self, limit: int) -> List[Dict]:
        from pymilvus import Collection, connections

        try:
            connections.connect(host='host.docker.internal', port='19530', alias='default')
            collection = Collection('memory_workflow')
            collection.load()

            # 获取所有记录（按时间降序）
            results = collection.query(
                expr="id >= 0",
                limit=1000,  # 先多取一些
                output_fields=["id", "content", "topic", "timestamp", "vector", "parent_id", "chunk_index"]
            )
            connections.disconnect('default')

            # 按 timestamp 降序排序
            candidates = []
            for r in results:
                entity = r.get("entity", {})
                if entity:
                    candidates.append({
                        "id": str(entity.get("id", "")),
                        "content": entity.get("content", ""),
                        "topic": entity.get("topic", "unknown"),
                        "timestamp": entity.get("timestamp", ""),
                        "embedding": entity.get("vector", []),
                        "parent_id": entity.get("parent_id") or None,
                        "chunk_index": entity.get("chunk_index") or 0
                    })
                else:
                    candidates.append({
                        "id": str(r.get("id", "")),
                        "content": r.get("content", ""),
                        "topic": r.get("topic", "unknown"),
                        "timestamp": r.get("timestamp", ""),
                        "embedding": r.get("vector", []),
                        "parent_id": r.get("parent_id") or None,
                        "chunk_index": r.get("chunk_index") or 0
                    })

            # 按时间降序
            candidates.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            return candidates[:limit]

        except Exception as e:
            print(f"⚠️ Milvus 查询失败: {e}", file=sys.stderr)
            return self._get_candidates_filesystem(limit)

    def _get_candidates_filesystem(self, limit: int) -> List[Dict]:
        memories = []
        if os.path.exists(MEMORY_DIR):
            for fname in os.listdir(MEMORY_DIR):
                if fname.endswith(".json"):
                    try:
                        with open(os.path.join(MEMORY_DIR, fname)) as f:
                            m = json.load(f)
                            m.setdefault("parent_id", None)
                            m.setdefault("chunk_index", 0)
                            memories.append(m)
                    except:
                        pass

        memories.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return memories[:limit]

    def _hybrid_search(self, query: str, candidates: List[Dict], all_embeddings: List[Tuple[str, List[float]]]) -> List[Dict]:
        """混合检索：向量搜索 + BM25，结果用 RRF 融合"""
        query_tokens = self.tokenize(query)

        # ---- 向量搜索排名 ----
        vector_rankings = []
        vector_scores = {}  # {mem_id: {emb_name: score}}
        for emb_name, query_emb in all_embeddings:
            similarities = []
            for mem in candidates:
                emb = mem.get("embedding", [])
                if emb and query_emb and len(emb) == len(query_emb):
                    sim = cosine_similarity(query_emb, emb)
                else:
                    sim = 0.0
                similarities.append((mem["id"], sim))
                if mem["id"] not in vector_scores:
                    vector_scores[mem["id"]] = {}
                vector_scores[mem["id"]][emb_name] = sim

            similarities.sort(key=lambda x: x[1], reverse=True)
            rankings = [(mid, rank + 1) for rank, (mid, _) in enumerate(similarities)]
            vector_rankings.append((emb_name, rankings))

        # ---- BM25 ----
        bm25_scores = self.calc_bm25(query_tokens, candidates)
        sorted_by_bm25 = sorted(bm25_scores.items(), key=lambda x: x[1], reverse=True)
        bm25_rankings = [(mid, rank + 1) for rank, (mid, _) in enumerate(sorted_by_bm25)]

        # ---- RRF 融合 ----
        rrf_scores = {}
        for mem in candidates:
            mem_id = mem["id"]
            score = 0.0

            # 向量排名贡献
            for emb_name, rankings in vector_rankings:
                for mid, rank in rankings:
                    if mid == mem_id:
                        score += 1.0 / (RRF_K + rank)
                        break

            # BM25 排名贡献
            for mid, rank in bm25_rankings:
                if mid == mem_id:
                    score += KEYWORD_WEIGHT * (1.0 / (RRF_K + rank))
                    break

            rrf_scores[mem_id] = score

        # 构建结果（带多维度分数）
        results = []
        for mem in candidates:
            mem_id = mem["id"]
            results.append({
                "id": mem_id,
                "content": mem["content"],
                "topic": mem.get("topic", "unknown"),
                "timestamp": mem.get("timestamp", ""),
                "keyword_score": round(bm25_scores.get(mem_id, 0), 4),
                "bm25_rank": next((r for m, r in bm25_rankings if m == mem_id), 999),
                "rrf_score": round(rrf_scores.get(mem_id, 0), 4),
                "vector_score": vector_scores.get(mem_id, {}).get("original", 0.0),
                "embedding": mem.get("embedding", [])
            })

        results.sort(key=lambda x: x["rrf_score"], reverse=True)
        return results

    def _bm25_only_search(self, query: str, candidates: List[Dict], limit: int = 5) -> List[Dict]:
        """轻量模式搜索：仅用 BM25 + 关键词匹配，无 Ollama 依赖"""
        # 关键词匹配分数
        keyword_scores = self.calc_bm25(self.tokenize(query), candidates)

        # 构建结果
        results = []
        for mem in candidates:
            mem_id = mem["id"]
            results.append({
                "id": mem_id,
                "content": mem["content"],
                "topic": mem.get("topic", "unknown"),
                "timestamp": mem.get("timestamp", ""),
                "bm25_score": round(keyword_scores.get(mem_id, 0.0), 4),
                "rrf_score": round(keyword_scores.get(mem_id, 0.0), 4),
                "embedding": mem.get("embedding", []),
                "parent_id": mem.get("parent_id"),
                "chunk_index": mem.get("chunk_index", 0)
            })

        results.sort(key=lambda x: x["bm25_score"], reverse=True)
        return results[:limit]

    def _two_stage_search(self, query: str, candidates: List[Dict], all_embeddings: List[Tuple[str, List[float]]], limit: int = 5) -> List[Dict]:
        """两阶段精排搜索（改进版）：
        Stage 1: 向量排名 + BM25排名 -> RRF融合 -> rerank精排 -> 取前1/3
        Stage 2: 从原始向量排名取top-N + BM25排名取top-N，与rerank结果一起二次RRF融合
        """
        query_tokens = self.tokenize(query)
        TOP_N = 5  # Stage2 各取前5

        # ========== Stage 1: 预排序和打分 ==========
        # 向量排名（使用 original embedding）
        original_emb_name = "original"
        original_emb = next((emb for name, emb in all_embeddings if name == original_emb_name), None)

        vector_scores = {}
        if original_emb:
            for mem in candidates:
                emb = mem.get("embedding", [])
                if emb and len(emb) == len(original_emb):
                    sim = cosine_similarity(original_emb, emb)
                else:
                    sim = 0.0
                vector_scores[mem["id"]] = sim

        # 向量排名
        sorted_by_vector = sorted(vector_scores.items(), key=lambda x: x[1], reverse=True)
        vector_rankings = [(mid, rank + 1) for rank, (mid, _) in enumerate(sorted_by_vector)]

        # BM25 排名
        bm25_scores = self.calc_bm25(query_tokens, candidates)
        sorted_by_bm25 = sorted(bm25_scores.items(), key=lambda x: x[1], reverse=True)
        bm25_rankings = [(mid, rank + 1) for rank, (mid, _) in enumerate(sorted_by_bm25)]

        # Stage1 RRF 粗排
        rrf_scores = {}
        for mem in candidates:
            mem_id = mem["id"]
            score = 0.0
            for mid, rank in vector_rankings:
                if mid == mem_id:
                    score += 1.0 / (RRF_K + rank)
                    break
            for mid, rank in bm25_rankings:
                if mid == mem_id:
                    score += KEYWORD_WEIGHT * (1.0 / (RRF_K + rank))
                    break
            rrf_scores[mem_id] = score

        # 构建 Stage1 候选
        stage1 = []
        for mem in candidates:
            mem_id = mem["id"]
            stage1.append({
                "id": mem_id,
                "content": mem["content"],
                "topic": mem.get("topic", "unknown"),
                "timestamp": mem.get("timestamp", ""),
                "keyword_score": round(bm25_scores.get(mem_id, 0), 4),
                "bm25_rank": next((r for m, r in bm25_rankings if m == mem_id), 999),
                "vector_rank": next((r for m, r in vector_rankings if m == mem_id), 999),
                "rrf_score": round(rrf_scores.get(mem_id, 0), 4),
                "vector_score": round(vector_scores.get(mem_id, 0.0), 4),
                "embedding": mem.get("embedding", [])
            })

        stage1.sort(key=lambda x: x["rrf_score"], reverse=True)

        # Stage1: rerank 取前 1/3
        stage1_top_n = max(len(stage1) // 3, 1)
        stage1_candidates = stage1[:stage1_top_n]

        # 调用 rerank
        reranked = self.rerank(query, stage1_candidates, top_n=stage1_top_n)

        # 构建 rerank 排名
        rerank_rankings = [(r["id"], rank + 1) for rank, r in enumerate(reranked)]
        rerank_score_map = {r["id"]: r.get("rerank_score", 0.0) for r in reranked}

        # ========== Stage 2: 候选融合 ==========
        # 从原始向量排名取 top-N（基于 stage1_candidates 范围内的排名）
        stage1_ids = set(c["id"] for c in stage1)
        vector_top_ids = [mid for mid, _ in vector_rankings if mid in stage1_ids][:TOP_N]

        # 从 BM25 排名取 top-N
        bm25_top_ids = [mid for mid, _ in bm25_rankings if mid in stage1_ids][:TOP_N]

        # rerank 排名也取 top-N
        rerank_top_ids = [mid for mid, _ in rerank_rankings][:TOP_N]

        # 合并候选
        stage2_ids = set(vector_top_ids) | set(bm25_top_ids) | set(rerank_top_ids)

        # Stage2 二次 RRF（向量排名 + BM25排名 + rerank排名）
        final_scores = {}
        for mem_id in stage2_ids:
            score = 0.0
            # 向量排名贡献
            for mid, rank in vector_rankings:
                if mid == mem_id:
                    score += 1.0 / (RRF_K + rank)
                    break
            # BM25 排名贡献
            for mid, rank in bm25_rankings:
                if mid == mem_id:
                    score += KEYWORD_WEIGHT * (1.0 / (RRF_K + rank))
                    break
            # rerank 排名贡献
            for mid, rank in rerank_rankings:
                if mid == mem_id:
                    score += 2.0 / (RRF_K + rank)  # rerank 权重更高
                    break
            final_scores[mem_id] = score

        # 构建最终结果
        results = []
        for mem in candidates:
            mem_id = mem["id"]
            if mem_id not in stage2_ids:
                continue
            results.append({
                "id": mem_id,
                "content": mem["content"],
                "topic": mem.get("topic", "unknown"),
                "timestamp": mem.get("timestamp", ""),
                "keyword_score": round(bm25_scores.get(mem_id, 0), 4),
                "vector_score": round(vector_scores.get(mem_id, 0.0), 4),
                "rrf_score": round(final_scores.get(mem_id, 0), 4),
                "rerank_score": rerank_score_map.get(mem_id),
                "from_vector_top": mem_id in vector_top_ids,
                "from_bm25_top": mem_id in bm25_top_ids,
                "from_rerank_top": mem_id in rerank_top_ids,
                "parent_id": mem.get("parent_id"),     # 父记忆ID，None=顶层记忆
                "chunk_index": mem.get("chunk_index", 0)  # 0=顶层，1+=分块
            })

        results.sort(key=lambda x: x["rrf_score"], reverse=True)

        # ===== Chunk 自动拼上下文 =====
        # 按 parent_id 分组，构建 {parent_id: [chunks...]} 的 map
        parent_chunks = {}
        for mem in candidates:
            pid = mem.get("parent_id")
            if pid:
                parent_chunks.setdefault(pid, []).append(mem)

        # 对每个 chunk 结果，用同 parent 的所有 chunks 拼出完整上下文
        for r in results:
            pid = r.get("parent_id")
            if pid and r.get("chunk_index", 0) > 0 and pid in parent_chunks:
                sibling_chunks = sorted(parent_chunks[pid],
                                        key=lambda x: x.get("chunk_index", 0))
                expanded = "\n".join(c.get("content", "") for c in sibling_chunks)
                r["chunk_content"] = r["content"]          # 原 chunk 内容
                r["content"] = expanded                    # 替换为完整上下文
                r["is_chunk"] = True
                r["chunk_count"] = len(sibling_chunks)
            else:
                r["is_chunk"] = False

        return results

    # ==================== 分块上下文 ====================

    def get_parent_context(self, parent_id: str) -> Dict:
        """根据 parent_id 获取完整上下文（parent + 相邻 chunks）

        Args:
            parent_id: 父记忆 ID

        Returns:
            {"parent": {...}, "chunks": [{...}, ...], "full_text": "..."}
        """
        candidates = self._get_candidates(1000)
        parent = None
        chunks = []

        for m in candidates:
            if m.get("parent_id") == parent_id:
                chunks.append(m)
            elif m.get("id") == parent_id:
                parent = m

        # 按 chunk_index 排序
        chunks.sort(key=lambda x: x.get("chunk_index", 0))

        # 重建完整文本（parent 的 content 已经是完整的）
        full_text = parent["content"] if parent else ""
        if chunks and full_text:
            # 如果 chunks 内容和 parent 不一致，用 chunks 拼接
            chunk_texts = "".join(c["content"] for c in chunks if c.get("chunk_index", 0) > 0)
            if chunk_texts and len(chunk_texts) > len(full_text):
                full_text = chunk_texts

        return {
            "parent": parent,
            "chunks": chunks,
            "full_text": full_text
        }

    # ==================== 状态 ====================

    def check(self) -> Dict:
        state = {"total_memories": 0, "idle_minutes": 0}

        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE) as f:
                    state.update(json.load(f))
            except:
                pass

        if state.get("last_store_time"):
            try:
                last_time = datetime.fromisoformat(state["last_store_time"])
                state["idle_minutes"] = int((datetime.now() - last_time).total_seconds() / 60)
            except:
                pass

        hot = self.get_hot_sessions()
        state["hot_sessions_count"] = len(hot)
        state["total_memories"] = self.count_memories()

        return state

    def get_hot_sessions(self) -> List[Dict]:
        if os.path.exists(HOT_SESSIONS_FILE):
            try:
                with open(HOT_SESSIONS_FILE) as f:
                    return json.load(f)
            except:
                pass
        return []


# ==================== CLI 接口 ====================

def main():
    parser = argparse.ArgumentParser(description="Memory Workflow Operations")
    parser.add_argument("action", choices=["check", "store", "search", "get_hot"],
                        help="操作类型")
    parser.add_argument("--query", "-q", type=str, help="搜索查询")
    parser.add_argument("--limit", "-l", type=int, default=5, help="返回数量")
    parser.add_argument("--content", type=str, help="记忆内容")
    parser.add_argument("--topic", type=str, default="general", help="话题标签")

    args = parser.parse_args()

    wf = get_instance()

    if args.action == "check":
        result = wf.check()
    elif args.action == "store":
        result = wf.store(args.content, args.topic)
    elif args.action == "search":
        if not args.query:
            print("错误: search 需要 --query 参数", file=sys.stderr)
            sys.exit(1)
        result = wf.search(args.query, args.limit)
    elif args.action == "get_hot":
        result = {"sessions": wf.get_hot_sessions()}
    else:
        result = {"error": "未知操作"}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
