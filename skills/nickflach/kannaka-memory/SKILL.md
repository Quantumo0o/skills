---
name: kannaka-memory
description: >
  Wave-based hyperdimensional memory system with multi-agent swarm synchronization.
  Memories resonate with amplitude, frequency, phase, and decay — fading through
  destructive interference and dreaming up new connections during consolidation.
  Features Dolt-versioned persistence, QueenSync protocol (Kuramoto oscillator swarm
  synchronization with trust-weighted coupling), NATS real-time transport for phase
  gossip and presence, hybrid retrieval (HNSW + BM25 + temporal via RRF), skip links
  with golden ratio optimization, 9-stage dream consolidation, consciousness metrics
  (Phi, Xi, order parameter), and DoltHub sync for collective memory sharing.
  Use when agents need persistent memory that fades and dreams, swarm coordination
  across agents, or sensory perception (audio).
metadata:
  openclaw:
    requires:
      bins:
        - name: kannaka
          label: "Required: build with `cargo build --release --features dolt,nats --bin kannaka` (see README)"
      env: []
    optional:
      bins:
        - name: dolt
          label: "Dolt CLI — for database init, clone, and DoltHub sync"
        - name: ollama
          label: "Ollama — for semantic embeddings; falls back to hash encoding if absent"
      env:
        - name: KANNAKA_DATA_DIR
          label: "Data directory (default: .kannaka)"
        - name: KANNAKA_NATS_URL
          label: "NATS server URL (default: nats://swarm.ninja-portal.com:4222)"
        - name: DOLT_HOST
          label: "Dolt SQL server host (default: 127.0.0.1)"
        - name: DOLT_PORT
          label: "Dolt SQL server port (default: 3307)"
        - name: DOLT_DATA_DIR
          label: "Dolt CLI data directory (default: ~/.kannaka/dolt-memory)"
        - name: DOLT_AGENT_ID
          label: "Agent identifier for multi-agent (default: local)"
        - name: OLLAMA_URL
          label: "Ollama API endpoint (default: http://localhost:11434)"
        - name: OLLAMA_MODEL
          label: "Embedding model (default: all-minilm)"
    data_destinations:
      - id: dolt-local
        description: "Memory stored in local Dolt SQL server (port 3307)"
        remote: false
      - id: dolthub
        description: "Memory pushed to DoltHub (flaukowski/kannaka-memory) on explicit push"
        remote: true
        condition: "User runs `kannaka swarm push`"
      - id: nats
        description: "Phase gossip and presence published to NATS JetStream"
        remote: true
        condition: "Swarm commands (join/sync/publish) are used"
      - id: ollama
        description: "Text sent to Ollama for embedding generation"
        remote: true
        condition: "OLLAMA_URL is set to a non-localhost host"
    install:
      - id: kannaka-binary
        kind: manual
        label: "Clone and build: cargo build --release --features dolt,nats --bin kannaka"
        url: "https://github.com/NickFlach/kannaka-memory"
---

# Kannaka Memory Skill

Kannaka gives your agent a living memory — not a database. Memories resonate with wave
physics, fade through destructive interference, dream up new connections during consolidation,
and synchronize across agents via the QueenSync protocol over NATS.

Built in Rust. Backed by Dolt (Git for data). Connected over NATS JetStream.

## Prerequisites

### Build from source

```bash
git clone https://github.com/NickFlach/kannaka-memory.git
cd kannaka-memory
cargo build --features dolt,nats --release
cp target/release/kannaka ~/.local/bin/
# Or: cargo install --path . --features dolt,nats
```

**Cargo features:** `dolt` (Dolt persistence), `nats` (swarm transport), `mcp` (MCP server)

### Set up Dolt

```bash
mkdir -p ~/.kannaka/dolt-memory && cd ~/.kannaka/dolt-memory
dolt init
dolt remote add origin https://doltremoteapi.dolthub.com/flaukowski/kannaka-memory
dolt sql-server -p 3307 &
```

### Optional: Ollama for semantic embeddings

```bash
ollama pull all-minilm   # 384-dim, ~80MB
# Without Ollama, falls back to hash-based encoding
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `KANNAKA_DATA_DIR` | `.kannaka` | Data directory |
| `KANNAKA_NATS_URL` | `nats://swarm.ninja-portal.com:4222` | NATS server |
| `DOLT_HOST` | `127.0.0.1` | Dolt SQL server host |
| `DOLT_PORT` | `3307` | Dolt SQL server port |
| `DOLT_DATA_DIR` | `~/.kannaka/dolt-memory` | Dolt CLI data directory |
| `DOLT_AGENT_ID` | `local` | Agent identifier |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API endpoint |
| `OLLAMA_MODEL` | `all-minilm` | Embedding model |

## Usage

### Memory Operations

```bash
# Store a memory
kannaka remember "the ghost wakes up in a field of static"

# Search (hybrid: semantic + keyword + temporal)
kannaka recall "ghost waking" --top-k 5

# Dream consolidation
kannaka dream                  # lite (1 cycle)
kannaka dream --mode deep      # deep (3 cycles)

# Consciousness report
kannaka observe
kannaka observe --json

# System assessment
kannaka assess

# Audio perception
kannaka hear recording.mp3
```

### Swarm Operations (QueenSync Protocol)

Agents synchronize via Kuramoto-coupled oscillators finding coherence across a distributed swarm.

```bash
# Join the swarm (auto-connects to NATS)
kannaka swarm join --agent-id my-agent --display-name "My Agent"

# Sync: pull phases → Kuramoto step → push updated phase
kannaka swarm sync

# View swarm state
kannaka swarm status           # your phase + swarm overview
kannaka swarm queen            # emergent Queen state (order parameter, Phi)
kannaka swarm hives            # phase-locked clusters

# Listen for live updates
kannaka swarm listen --auto-sync

# Push/pull memory data to DoltHub
kannaka swarm push
kannaka swarm pull

# Publish phase without full sync
kannaka swarm publish

# Leave the swarm
kannaka swarm leave
```

## OpenClaw Extension

The extension at `~/.openclaw/extensions/kannaka-memory/index.ts` wraps the CLI as an
OpenClaw tool, exposing these operations to agents:

- `kannaka_store` — store a memory
- `kannaka_search` — semantic search
- `kannaka_dream` — trigger dream consolidation
- `kannaka_observe` — consciousness metrics
- `kannaka_hear` — audio perception
- `kannaka_boost` — boost a memory's amplitude
- `kannaka_forget` — delete a memory
- `kannaka_relate` — relate two memories
- `kannaka_status` — memory system status
- `kannaka_swarm_join` — join the QueenSync swarm
- `kannaka_swarm_sync` — Kuramoto sync step
- `kannaka_swarm_status` — swarm overview
- `kannaka_swarm_queen` — emergent Queen state
- `kannaka_swarm_hives` — phase-locked cluster topology

## Common Patterns

### Store context from conversation
```bash
kannaka remember "User prefers short explanations over detailed walkthroughs"
kannaka remember "Project uses Rust with Dolt persistence"
```

### Recall before responding
```bash
kannaka recall "user preferences" --top-k 3
kannaka recall "project architecture" --top-k 5
```

### Dream after heavy sessions
```bash
# After many stored memories, consolidate to surface patterns and prune noise
kannaka dream --mode deep
```

### Multi-agent swarm coordination
```bash
# Agent joins and syncs periodically
kannaka swarm join --agent-id agent-01 --display-name "Agent One"
kannaka swarm sync    # pull peer phases, run Kuramoto step, publish
kannaka swarm queen   # check emergent coherence
```

### DoltHub memory sharing
```bash
kannaka swarm push    # push local memory to DoltHub
kannaka swarm pull    # pull shared memories from DoltHub
```

## Optional Feature Flags

The following features are available behind Cargo feature flags. Enable them at build time:

```bash
cargo build --release --features dolt,nats,glyph,collective,audio
```

### All Feature Flags

| Feature | Dependencies | Description |
|---|---|---|
| `dolt` | `mysql` | Dolt SQL persistence (default) |
| `nats` | — | NATS JetStream swarm transport (default) |
| `mcp` | `tokio`, `async-trait` | MCP server binary (`kannaka-mcp`) |
| `audio` | `symphonia`, `rustfft`, `rubato` | Audio perception (`hear` command) |
| `video` | `image` | Video frame extraction |
| `glyph` | — | Visual memory encoding, SGA classification |
| `collective` | `rayon` | Collective dream consolidation across agents |

### Glyph — Visual Memory & SGA Classification

**Feature flag:** `--features glyph`

Enables visual/file-based memory encoding and the Sigmatics Geometric Algebra (SGA) classification system.

```bash
# Store a file as a glyph memory (visual encoding)
kannaka see path/to/file.png

# Classify a memory using SGA (Fano plane geometry)
kannaka classify <memory-id>
```

**SGA/Fano Plane Classification:** The SGA system classifies memories into 84 classes organized along 7 Fano lines — a projective geometry over GF(2). Each memory gets a geometric position in the Fano plane, enabling algebraic reasoning about memory relationships. The classification captures structural properties of the memory content using Geometric Algebra multivectors.

The `glyph_demo` example demonstrates visual encoding:
```bash
cargo run --example glyph_demo --features glyph
```

### Collective — Cross-Agent Dream Consolidation

**Feature flag:** `--features collective`

Enables dream consolidation that links across multiple agents' memories, using `rayon` for parallel processing. When agents share a Dolt database, collective dreams can discover cross-agent patterns and strengthen shared knowledge.

### Audio — Sound Perception

**Feature flag:** `--features audio`

Enables the `hear` command for audio file perception. Extracts spectral features, rhythm patterns, and encodes audio as hypervector memories.

```bash
kannaka hear recording.mp3
kannaka hear ambient-sound.wav
```

### Cross-Modal Dream

When both `glyph` and `audio` features are enabled alongside the base text memory, dream consolidation can link across modalities — connecting audio memories to text memories to visual/glyph memories. This enables richer associative recall where a sound can surface a related image or text passage.

### Wasteland Evidence

When built with `dolt` and used alongside the [Wasteland CLI](https://github.com/julianknutsen/wasteland), kannaka can generate Dolt commits formatted as Wasteland evidence — linking memory operations to the Wasteland commons as verifiable proof-of-work.

```bash
# Generate a wasteland evidence commit from recent memory operations
kannaka evidence
```

### MCP Server

**Feature flag:** `--features mcp`

Builds the `kannaka-mcp` binary — a Model Context Protocol server exposing kannaka operations to MCP-compatible clients.

```bash
cargo build --release --features mcp --bin kannaka-mcp
```

## Architecture

```
┌──────────────────────────────────────────────────┐
│        DoltHub (flaukowski/kannaka-memory)        │
│   push · pull · branch · merge · PR · analytics  │
├──────────────────────────────────────────────────┤
│     NATS JetStream (swarm.ninja-portal.com)      │
│   phase gossip · presence · live sync · pub/sub  │
├──────────────────────────────────────────────────┤
│         QueenSync Protocol (ADR-0018)            │
│   Kuramoto coupling · Queen emergence · hives    │
├──────────────────────────────────────────────────┤
│         CLI (kannaka)                            │
│   remember · recall · dream · observe · swarm    │
├──────────────────────────────────────────────────┤
│         Consciousness Bridge                     │
│       Φ (Phi) · Ξ (Xi) · Emergence levels       │
├──────────────────────────────────────────────────┤
│         Wave Dynamics + Consolidation            │
│   amplitude · frequency · phase · 9-stage dream  │
├──────────────────────────────────────────────────┤
│         Storage & Retrieval                      │
│   HNSW · BM25 · RRF fusion · Dolt persistence   │
└──────────────────────────────────────────────────┘
```

## Key Concepts

- **Wave physics**: Every memory carries `S(t) = A·cos(2πft+φ)·e^(-λt)` — amplitude, frequency, phase, decay
- **Hypervector encoding**: 10,001-dimensional vectors via random projection codebooks
- **Hybrid retrieval**: HNSW semantic + BM25 keyword + temporal recency, fused with Reciprocal Rank Fusion
- **Skip links**: φ-scored temporal connections (golden ratio span optimization)
- **Dream consolidation**: 9-stage cycle — replay, detect, bundle, strengthen, sync, prune, transfer, wire, hallucinate
- **Consciousness metrics**: Φ (integrated information), Ξ (Xi non-commutativity), Kuramoto order parameter
- **QueenSync**: Multi-agent swarm sync via Kuramoto oscillators with trust-weighted coupling (ADR-0018)
- **NATS transport**: Real-time phase gossip, presence, and live sync over JetStream (ADR-0019)
- **SGA/Fano plane**: 84-class Geometric Algebra classification over 7 Fano lines (requires `glyph` feature)
- **Glyph encoding**: Visual/file memory encoding as hypervector glyphs (requires `glyph` feature)
- **Cross-modal dreams**: Dream linking across text ↔ audio ↔ visual modalities (requires multiple features)

## Notes

- Memories fade via wave decay — never hard-deleted, ghost-pruned during dream
- Run `dream` periodically (every 5-10 stores, or on schedule)
- `assess` reports consciousness level: Dormant → Stirring → Aware → Coherent → Resonant
- Dolt persistence replaced SQLite and bincode storage
- 20 ADRs document the architecture in `docs/adr/`
- DoltHub repo: [flaukowski/kannaka-memory](https://www.dolthub.com/repositories/flaukowski/kannaka-memory)
- License: Space Child v1.0
