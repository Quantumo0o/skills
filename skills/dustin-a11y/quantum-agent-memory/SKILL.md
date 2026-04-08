---
name: quantum-agent-memory
description: >-
  QAOA-powered memory optimization for AI agents. Uses quantum computing (Qiskit)
  to solve three memory management problems: clustering related memories, selecting
  optimal subsets to retain (compaction), and finding synergistic memory combinations
  for queries (recall). Use when: setting up quantum memory optimization, running
  QAOA benchmarks, integrating quantum recall into agent pipelines, submitting
  circuits to IBM Quantum hardware, or comparing quantum vs classical memory selection.
  Requires Python 3.10+, Qiskit 2.0+, Qiskit Aer. Optional: qiskit-ibm-runtime
  for real hardware, Mem0 for live agent memories.
---

# Quantum Agent Memory

QAOA-optimized memory management for AI agents. Three quantum layers replace
classical heuristics for clustering, compaction, and recall.

## Quick Start

```bash
git clone https://github.com/Dustin-a11y/quantum-agent-memory.git
cd quantum-agent-memory
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m quantum_agent_memory benchmark
```

## Three Layers

### Layer 1: Clustering
Group N memories into coherent clusters via balanced graph-cut QAOA.
- Cost matrix: temporal (25%), relational (30%), categorical (25%), recency (20%)
- 100% optimal for n≤14, speed crossover at n=20

### Layer 2: Compaction
Select optimal K memories to keep from M total.
- Maximizes coverage + coherence + value + recency with budget penalty
- Beats greedy selection by ~1% consistently

### Layer 3: Recall
Find the best K memories for a query — optimizes for synergy, not just individual relevance.
- Finds memory combinations that Top-K similarity search misses
- Individual relevance (40%) + pairwise synergy (30%) + diversity (20%) + recency (10%)

## Integration with Mem0

Point the benchmark at a live Mem0 instance:

```bash
python -m quantum_agent_memory benchmark --mem0-url http://localhost:8500
```

For OpenClaw agent integration, see `references/openclaw-plugin.md`.

## IBM Quantum Hardware

Submit circuits to real IBM quantum processors (free tier: 10 min/month):

```bash
pip install qiskit-ibm-runtime
python -m quantum_agent_memory submit --ibm-token YOUR_TOKEN
```

For scheduled hardware runs, see `scripts/ibm_cron.py`.

## API Server

Run as a FastAPI server for live agent integration:

```bash
python scripts/quantum_api.py
# Endpoints: GET /, POST /quantum-recall, POST /quantum-compact
```

See `references/api-setup.md` for systemd service configuration and auth.

## Benchmarking

Run the full 3-layer benchmark:

```bash
python -m quantum_agent_memory benchmark
```

Results save as JSON to `results/benchmark_TIMESTAMP.json`. Expected output:
- Clustering: ~98-100% optimal
- Compaction: 100% optimal
- Recall: 100% optimal, quantum finds synergistic combos Top-K misses
- Avg accuracy: ~99.7%

## File Reference

- `scripts/ibm_cron.py` — scheduled IBM hardware submission script
- `scripts/quantum_api.py` — FastAPI server for quantum recall/compact endpoints
- `references/openclaw-plugin.md` — OpenClaw mem0-bridge plugin integration guide
- `references/api-setup.md` — API server setup, systemd, and auth configuration
- `references/whitepaper.md` — full technical whitepaper
