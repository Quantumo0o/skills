---
name: "agent-memory-system"
slug: skylv-agent-memory-system
version: 1.0.0
description: "Agent 记忆系统设计助手。构建长期记忆、短期记忆、情景记忆架构。触发词：记忆、memory、上下文管理、上下文窗口。"
author: SKY-lv
license: MIT-0
tags: [agent, openclaw, agent]
---

# Agent Memory System

## 功能说明

设计 Agent 持久化记忆系统，优化上下文管理。

## 记忆分层架构

```
┌─────────────────────────────────────┐
│         Working Memory (上下文)        │  ← 当前对话，LLM直接访问
├─────────────────────────────────────┤
│      Short-Term (会话记忆)            │  ← 当前会话，SESSION
├─────────────────────────────────────┤
│      Long-Term (持久记忆)             │  ← 跨会话，数据库/文件
├─────────────────────────────────────┤
│      Semantic (向量记忆)               │  ← RAG，向量检索
├─────────────────────────────────────┤
│      Procedural (程序记忆)             │  ← 工具/Skill定义
└─────────────────────────────────────┘
```

## 完整实现

### 1. 记忆核心类

```typescript
interface MemoryEntry {
  id: string;
  type: 'episodic' | 'semantic' | 'procedural';
  content: string;
  timestamp: number;
  importance: number;        // 0-10，重要程度
  accessCount: number;      // 访问次数
  tags: string[];
  metadata: Record<string, any>;
}

class AgentMemory {
  private shortTerm: Map<string, MemoryEntry[]> = new Map();
  private longTerm: SQLiteDatabase;
  private vectorStore: ChromaClient;
  private sessionId: string;
  
  constructor(sessionId: string, dbPath: string) {
    this.sessionId = sessionId;
    this.longTerm = new SQLiteDatabase(dbPath);
    this.vectorStore = new ChromaClient({ path: './chroma' });
    this.initDatabase();
  }
  
  private initDatabase() {
    this.longTerm.exec(`
      CREATE TABLE IF NOT EXISTS memories (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        importance INTEGER DEFAULT 5,
        access_count INTEGER DEFAULT 0,
        tags TEXT,
        metadata TEXT
      );
      CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp);
      CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance);
      CREATE INDEX IF NOT EXISTS idx_type ON memories(type);
    `);
  }
  
  // 添加记忆
  async add(entry: Omit<MemoryEntry, 'id' | 'accessCount'>) {
    const id = crypto.randomUUID();
    const full: MemoryEntry = { ...entry, id, accessCount: 0 };
    
    // 短期记忆
    if (!this.shortTerm.has(this.sessionId)) {
      this.shortTerm.set(this.sessionId, []);
    }
    this.shortTerm.get(this.sessionId)!.push(full);
    
    // 持久化
    this.longTerm.prepare(
      `INSERT OR REPLACE INTO memories VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
    ).run(
      full.id, full.type, full.content, full.timestamp,
      full.importance, full.accessCount,
      JSON.stringify(full.tags), JSON.stringify(full.metadata)
    );
    
    // 向量化（重要记忆）
    if (full.importance >= 7) {
      await this.vectorStore.add({
        ids: [full.id],
        embeddings: [await this.embed(full.content)],
        documents: [full.content],
        metadatas: [{ type: full.type, tags: full.tags.join(',') }]
      });
    }
    
    return full;
  }
  
  // 检索记忆
  async retrieve(query: string, limit = 10): Promise<MemoryEntry[]> {
    // 1. 语义检索
    const queryEmbedding = await this.embed(query);
    const semantic = await this.vectorStore.search({
      query_embeddings: [queryEmbedding],
      n_results: limit
    });
    
    // 2. 关键词检索
    const keywords = query.toLowerCase().split(/\s+/);
    let sql = `SELECT * FROM memories WHERE `;
    sql += keywords.map(k => `content LIKE '%${k}%'`).join(' OR ');
    sql += ` ORDER BY importance DESC, timestamp DESC LIMIT ${limit}`;
    const keyword = this.longTerm.exec(sql).all() as MemoryEntry[];
    
    // 3. 去重合并
    const seen = new Set<string>();
    const results: MemoryEntry[] = [];
    [...semantic.results, ...keyword].forEach(m => {
      if (!seen.has(m.id)) {
        seen.add(m.id);
        m.accessCount++;
        results.push(m);
      }
    });
    
    // 更新访问计数
    results.forEach(m => {
      this.longTerm.prepare(
        `UPDATE memories SET access_count = ? WHERE id = ?`
      ).run(m.accessCount, m.id);
    });
    
    return results;
  }
  
  // 获取短期记忆（当前会话）
  getShortTerm(): MemoryEntry[] {
    return this.shortTerm.get(this.sessionId) || [];
  }
  
  // 压缩短期记忆到长期
  async consolidate() {
    const shortTerm = this.getShortTerm();
    
    // 保留最重要的记忆
    const important = shortTerm
      .filter(m => m.importance >= 6)
      .sort((a, b) => b.importance - a.importance)
      .slice(0, 50);
    
    // 合并重复
    const merged = this.mergeSimilar(important);
    
    // 更新短期记忆
    this.shortTerm.set(this.sessionId, merged);
  }
  
  // 遗忘低价值记忆
  async forget(threshold = 2) {
    // 遗忘低重要度、低访问的记忆
    this.longTerm.prepare(
      `DELETE FROM memories WHERE importance < ? AND access_count < ?`
    ).run(threshold, threshold);
    
    // 清理向量库
    await this.vectorStore.delete({
      where: { importance: { $lt: threshold } }
    });
  }
  
  // 构建上下文
  async buildContext(query: string, maxTokens = 6000): Promise<string> {
    const memories = await this.retrieve(query, 20);
    const shortTerm = this.getShortTerm();
    
    const parts: string[] = [];
    let totalTokens = 0;
    
    // 短期记忆优先
    for (const m of [...shortTerm.reverse(), ...memories]) {
      const text = `[${m.type}] ${m.content}`;
      const tokens = Math.ceil(text.length / 4);
      if (totalTokens + tokens > maxTokens) break;
      parts.unshift(text);
      totalTokens += tokens;
    }
    
    return `## 记忆上下文\n\n${parts.join('\n')}`;
  }
  
  private async embed(text: string): Promise<number[]> {
    // 调用 embedding API
    const response = await fetch('https://api.openai.com/v1/embeddings', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${process.env.OPENAI_API_KEY}` },
      body: JSON.stringify({ model: 'text-embedding-3-small', input: text })
    });
    const data = await response.json();
    return data.data[0].embedding;
  }
  
  private mergeSimilar(memories: MemoryEntry[]): MemoryEntry[] {
    const merged: MemoryEntry[] = [];
    for (const m of memories) {
      const similar = merged.find(g => 
        g.type === m.type && 
        this.similarity(g.content, m.content) > 0.8
      );
      if (similar) {
        // 合并，保留最新的时间戳和最高的importance
        similar.importance = Math.max(similar.importance, m.importance);
        similar.timestamp = Math.max(similar.timestamp, m.timestamp);
      } else {
        merged.push(m);
      }
    }
    return merged;
  }
  
  private similarity(a: string, b: string): number {
    const setA = new Set(a.toLowerCase());
    const setB = new Set(b.toLowerCase());
    const intersection = new Set([...setA].filter(x => setB.has(x)));
    const union = new Set([...setA, ...setB]);
    return intersection.size / union.size;
  }
}
```

### 2. 使用示例

```typescript
// 初始化
const memory = new AgentMemory(sessionId, './memory.db');

// 对话时注入记忆
async function chat(message: string) {
  const context = await memory.buildContext(message);
  
  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: '你是助手的记忆系统使用指南。' },
      { role: 'system', content: context },
      { role: 'user', content: message }
    ]
  });
  
  const answer = response.choices[0].message.content;
  
  // 自动存储重要信息
  if (containsActionableInfo(message, answer)) {
    await memory.add({
      type: 'semantic',
      content: extractKeyInfo(answer),
      timestamp: Date.now(),
      importance: 7,
      tags: ['用户问答'],
      metadata: { source: 'chat' }
    });
  }
  
  return answer;
}

// 定期压缩
setInterval(() => memory.consolidate(), 30 * 60 * 1000);  // 每30分钟
setInterval(() => memory.forget(), 24 * 60 * 60 * 1000);   // 每天
```

### 3. 重要性评估

```typescript
function evaluateImportance(text: string, context: string): number {
  let score = 5; // 基础分
  
  // 明确的重要词
  const importantKeywords = [
    '记住', '重要', '必须', '关键', '别忘了', '优先',
    'deadline', '截止', '紧急', '用户偏好', '账号', '密码'
  ];
  for (const kw of importantKeywords) {
    if (text.includes(kw)) score += 1;
  }
  
  // 用户明确要求记住
  if (text.match(/记住|remember|save|存储/)) score += 3;
  
  // 重复出现
  if (context.includes(text)) score += 2;
  
  // 限制范围
  return Math.min(10, Math.max(0, score));
}
```

## 存储策略

| 类型 | 存储 | 容量 | TTL |
|------|------|------|-----|
| 工作记忆 | 上下文窗口 | 128K tokens | 会话内 |
| 短期记忆 | Redis/Memory | 100条 | 24小时 |
| 长期记忆 | SQLite | 无限制 | 永久 |
| 向量记忆 | Chroma/Milvus | 按需 | 定期清理 |

## 最佳实践

1. **自动摘要**：长记忆定期压缩成摘要
2. **分层索引**：按类型、时间、重要性多维索引
3. **增量更新**：避免重复存储相似内容
4. **隐私保护**：敏感信息加密存储
5. **容量管理**：设置token预算，定期清理
