#!/usr/bin/env python3
"""
Quantum Memory API Server
Exposes quantum clustering, compaction, and recall as REST endpoints.
Set QUANTUM_API_TOKEN env var to require Bearer auth.

Usage: python quantum_api.py
Endpoints: GET /, POST /quantum-recall, POST /quantum-compact

Copyright 2026 Coinkong (Chef's Attraction). MIT License.
"""

import os
from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
import numpy as np
import uvicorn
import requests
import re

API_TOKEN = os.environ.get("QUANTUM_API_TOKEN", "")
MEM0_URL = os.environ.get("MEM0_URL", "http://localhost:8500")

async def verify_token(request: Request):
    if request.url.path in ("/", "/docs", "/openapi.json"):
        return
    if not API_TOKEN:
        return
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer ") or auth[7:] != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

app = FastAPI(
    title="Quantum Memory API",
    version="1.1.0",
    dependencies=[Depends(verify_token)]
)

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def build_cost_matrix(memories):
    n = len(memories)
    cost = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            mi = memories[i].get("memory", "")
            mj = memories[j].get("memory", "")
            wi = set(re.findall(r'\w+', mi.lower()))
            wj = set(re.findall(r'\w+', mj.lower()))
            overlap = len(wi & wj) / max(len(wi | wj), 1)
            ai = memories[i].get("agent_id", "")
            aj = memories[j].get("agent_id", "")
            categorical = 1.0 if ai == aj else 0.3
            score = 0.30 * overlap + 0.25 * 0.5 + 0.25 * categorical + 0.20 * 0.5
            cost[i][j] = score
            cost[j][i] = score
    return cost


def run_qaoa(n_qubits, cost_matrix, budget_k=None, shots=1024):
    gamma_vals = np.linspace(0, np.pi, 8)
    beta_vals = np.linspace(0, np.pi, 8)
    simulator = AerSimulator()
    best_cost = -float('inf')
    best_bitstring = "0" * n_qubits
    for gamma_val in gamma_vals:
        for beta_val in beta_vals:
            qc = QuantumCircuit(n_qubits)
            for i in range(n_qubits):
                qc.h(i)
            for i in range(n_qubits):
                for j in range(i + 1, n_qubits):
                    if cost_matrix[i][j] > 0.01:
                        qc.rzz(2 * gamma_val * cost_matrix[i][j], i, j)
            if budget_k is not None:
                penalty = 2.0
                for i in range(n_qubits):
                    qc.rz(penalty * (2 * budget_k / n_qubits - 1) * gamma_val, i)
            for i in range(n_qubits):
                qc.rx(2 * beta_val, i)
            qc.measure_all()
            result = simulator.run(qc, shots=shots).result()
            counts = result.get_counts()
            for bitstring, count in counts.items():
                bits = [int(b) for b in bitstring[::-1]]
                if budget_k is not None and sum(bits) != budget_k:
                    continue
                c = sum(cost_matrix[i][j] for i in range(n_qubits)
                        for j in range(i + 1, n_qubits) if bits[i] == bits[j])
                if c > best_cost:
                    best_cost = c
                    best_bitstring = bitstring[::-1]
    return best_bitstring, best_cost


@app.get("/")
async def health():
    return {"status": "operational", "service": "Quantum Memory API",
            "version": "1.1.0", "auth": "enabled" if API_TOKEN else "disabled"}


class RecallRequest(BaseModel):
    query: str
    user_id: str = "dustin"
    k: int = 5
    max_candidates: int = 12


@app.post("/quantum-recall")
async def quantum_recall(req: RecallRequest):
    try:
        resp = requests.post(f"{MEM0_URL}/recall", json={
            "query": req.query, "agent_id": "all",
            "user_id": req.user_id, "limit": req.max_candidates
        }, timeout=15)
        candidates = resp.json().get("memories", [])
        if len(candidates) <= req.k:
            return {"ok": True, "memories": candidates, "method": "all_fit"}
        n = min(len(candidates), 14)
        candidates = candidates[:n]
        cost = build_cost_matrix(candidates)
        query_words = set(re.findall(r'\w+', req.query.lower()))
        for i in range(n):
            mem_words = set(re.findall(r'\w+', candidates[i].get("memory", "").lower()))
            relevance = len(query_words & mem_words) / max(len(query_words), 1)
            cost[i][i] = relevance * 0.4
        bitstring, score = run_qaoa(n, cost, budget_k=req.k)
        selected = [candidates[i] for i, b in enumerate(bitstring) if b == "1"]
        return {"ok": True, "memories": selected, "score": float(score),
                "method": "qaoa", "qubits": n,
                "selected_indices": [i for i, b in enumerate(bitstring) if b == "1"]}
    except Exception as e:
        resp = requests.post(f"{MEM0_URL}/recall", json={
            "query": req.query, "agent_id": "all",
            "user_id": req.user_id, "limit": req.k
        }, timeout=15)
        return {"ok": True, "memories": resp.json().get("memories", []),
                "method": "fallback", "error": str(e)}


class CompactRequest(BaseModel):
    user_id: str = "dustin"
    keep: int = 15


@app.post("/quantum-compact")
async def quantum_compact(req: CompactRequest):
    try:
        resp = requests.get(f"{MEM0_URL}/memories/{req.user_id}", timeout=15)
        all_memories = resp.json().get("memories", [])
        if len(all_memories) <= req.keep:
            return {"ok": True, "keep": all_memories, "archive": [], "method": "all_fit"}
        n = min(len(all_memories), 14)
        subset = all_memories[:n]
        k = min(req.keep, n - 1)
        cost = build_cost_matrix(subset)
        bitstring, score = run_qaoa(n, cost, budget_k=k)
        keep = [subset[i] for i, b in enumerate(bitstring) if b == "1"]
        archive = [subset[i] for i, b in enumerate(bitstring) if b == "0"]
        return {"ok": True, "keep": keep, "archive": archive,
                "score": float(score), "method": "qaoa"}
    except Exception as e:
        return {"ok": False, "error": str(e), "method": "failed"}


if __name__ == "__main__":
    print("⚛️ Quantum Memory API starting on port 8501...")
    uvicorn.run(app, host="0.0.0.0", port=8501)
