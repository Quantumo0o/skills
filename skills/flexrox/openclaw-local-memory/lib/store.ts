/**
 * LocalMemoryStore — TF-IDF based memory store (no external service required)
 * Uses Term Frequency-Inverse Document Frequency + cosine similarity for search.
 * Works out of the box, no Ollama, no API key needed.
 */

import { randomUUID } from "node:crypto";
import { resolve } from "node:path";
import { homedir } from "node:os";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";

// ─── Types ────────────────────────────────────────────────────────────────────

export interface MemoryEntry {
  id: string;
  content: string;
  tfidf: Record<string, number>; // term → TF-IDF weight vector
  metadata: {
    sessionKey?: string;
    category: "preference" | "fact" | "decision" | "entity" | "other";
    createdAt: string;
    source?: "user" | "assistant" | "system";
  };
}

export interface SearchResult {
  id: string;
  content: string;
  similarity: number;
  metadata: MemoryEntry["metadata"];
}

export interface StoreConfig {
  containerTag: string;
  debug: boolean;
}

// ─── TF-IDF Core ─────────────────────────────────────────────────────────────

/** Tokenize text into lowercase words */
function tokenize(text: string): string[] {
  return text
    .toLowerCase()
    .replace(/[^a-zäöüß0-9\s]/g, " ")
    .split(/\s+/)
    .filter((w) => w.length > 2);
}

/** Compute TF (term frequency) for a document */
function computeTF(tokens: string[]): Record<string, number> {
  const tf: Record<string, number> = {};
  for (const token of tokens) {
    tf[token] = (tf[token] ?? 0) + 1;
  }
  const len = tokens.length;
  for (const token in tf) {
    tf[token] /= len;
  }
  return tf;
}

/** Compute IDF from all documents */
function computeIDF(documents: string[][]): Record<string, number> {
  const idf: Record<string, number> = {};
  const N = documents.length;
  const docFreq: Record<string, number> = {};

  for (const doc of documents) {
    const seen = new Set(doc);
    for (const term of seen) {
      docFreq[term] = (docFreq[term] ?? 0) + 1;
    }
  }

  for (const term in docFreq) {
    idf[term] = Math.log((N + 1) / (docFreq[term] + 1)) + 1;
  }

  return idf;
}

/** Compute TF-IDF vector from tokens + IDF */
function computeTFIDF(tf: Record<string, number>, idf: Record<string, number>): Record<string, number> {
  const vec: Record<string, number> = {};
  for (const term in tf) {
    vec[term] = tf[term] * (idf[term] ?? 1);
  }
  return vec;
}

/** Cosine similarity between two TF-IDF vectors */
function cosineSimilarity(a: Record<string, number>, b: Record<string, number>): number {
  const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
  let dot = 0, normA = 0, normB = 0;
  for (const k of keys) {
    const av = a[k] ?? 0;
    const bv = b[k] ?? 0;
    dot += av * bv;
    normA += av * av;
    normB += bv * bv;
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB) + 1e-8);
}

// ─── Category Detection ───────────────────────────────────────────────────────

function detectCategory(text: string): MemoryEntry["metadata"]["category"] {
  const lower = text.toLowerCase();
  if (/prefer|like|love|hate|want|i (always|never)\b/i.test(lower)) return "preference";
  if (/decided|will use|going with|chose|selected/i.test(lower)) return "decision";
  if (/\+\d{10,}|@[\w.-]+\.\w+|is called|named/i.test(lower)) return "entity";
  if (/is |are |has |have |was |were /i.test(lower)) return "fact";
  return "other";
}

// ─── Store ───────────────────────────────────────────────────────────────────

export class LocalMemoryStore {
  private memories: MemoryEntry[] = [];
  private idf: Record<string, number> = {};
  private dirty = false;
  public readonly containerTag: string;
  private storePath: string;

  constructor(cfg: StoreConfig) {
    this.containerTag = cfg.containerTag;
    this.storePath = resolve(homedir(), ".openclaw", "memory", `${this.containerTag}.json`);
    this.load();
  }

  // ── Persistence ─────────────────────────────────────────────────────────

  private load() {
    try {
      const dir = resolve(homedir(), ".openclaw", "memory");
      if (!existsSync(dir)) mkdirSync(dir, { recursive: true });

      if (existsSync(this.storePath)) {
        const raw = readFileSync(this.storePath, "utf-8");
        const data = JSON.parse(raw) as MemoryEntry[];
        this.memories = Array.isArray(data) ? data : [];
        this.rebuildIDF();
      }
    } catch {
      this.memories = [];
    }
  }

  private save() {
    if (!this.dirty) return;
    try {
      const dir = resolve(homedir(), ".openclaw", "memory");
      if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
      writeFileSync(this.storePath, JSON.stringify(this.memories, null, 2), "utf-8");
      this.dirty = false;
    } catch (err) {
      console.error("[local-memory] save failed:", err);
    }
  }

  private rebuildIDF() {
    const docs = this.memories.map((m) => tokenize(m.content));
    this.idf = computeIDF(docs);
  }

  // ── CRUD ────────────────────────────────────────────────────────────────

  async add(
    content: string,
    metadata: Partial<MemoryEntry["metadata"]> = {},
  ): Promise<string> {
    const tokens = tokenize(content);
    const tf = computeTF(tokens);
    const tfidf = computeTFIDF(tf, this.idf);

    const id = randomUUID();
    const entry: MemoryEntry = {
      id,
      content,
      tfidf,
      metadata: {
        category: metadata.category ?? detectCategory(content),
        createdAt: metadata.createdAt ?? new Date().toISOString(),
        sessionKey: metadata.sessionKey,
        source: metadata.source,
      },
    };

    this.memories.push(entry);
    this.dirty = true;

    // Update IDF incrementally with new document
    const newDocs = [tokens];
    const newIDF = computeIDF(newDocs);
    for (const term in newIDF) {
      this.idf[term] = newIDF[term];
    }

    this.save();
    return id;
  }

  async search(
    query: string,
    limit = 10,
    threshold = 0.1,
  ): Promise<SearchResult[]> {
    const queryTokens = tokenize(query);
    const queryTF = computeTF(queryTokens);
    const queryTFIDF = computeTFIDF(queryTF, this.idf);

    const scored = this.memories.map((entry) => ({
      entry,
      similarity: cosineSimilarity(queryTFIDF, entry.tfidf),
    }));

    return scored
      .filter((s) => s.similarity >= threshold)
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, limit)
      .map((s) => ({
        id: s.entry.id,
        content: s.entry.content,
        similarity: s.similarity,
        metadata: s.entry.metadata,
      }));
  }

  async delete(id: string): Promise<void> {
    const idx = this.memories.findIndex((m) => m.id === id);
    if (idx !== -1) {
      this.memories.splice(idx, 1);
      this.dirty = true;
      this.save();
    }
  }

  async forgetByQuery(
    query: string,
    limit = 1,
  ): Promise<{ success: boolean; message: string }> {
    const results = await this.search(query, limit);
    if (results.length === 0) {
      return { success: false, message: "No matching memory found." };
    }
    await this.delete(results[0].id);
    const preview = results[0].content.slice(0, 100);
    return {
      success: true,
      message: `Forgot: "${preview}${results[0].content.length > 100 ? "…" : ""}"`,
    };
  }

  async wipeAll(): Promise<{ deletedCount: number }> {
    const count = this.memories.length;
    this.memories = [];
    this.idf = {};
    this.dirty = true;
    this.save();
    return { deletedCount: count };
  }

  async count(): Promise<number> {
    return this.memories.length;
  }

  /** Return all memories sorted by createdAt descending. */
  async listAll(limit = 100): Promise<MemoryEntry[]> {
    return [...this.memories]
      .sort(
        (a, b) =>
          new Date(b.metadata.createdAt).getTime() -
          new Date(a.metadata.createdAt).getTime()
      )
      .slice(0, limit);
  }
}
