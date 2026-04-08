#!/usr/bin/env python3
"""
IBM Quantum Hardware Cron Runner 🦍
Submits all 3 QAOA circuit types to IBM hardware and logs results.

Schedule: 5x daily (8 AM, 11 AM, 2 PM, 5 PM, 8 PM PDT)
Budget: ~5 sec QPU/month out of 10 min free tier

By: DK — Coinkong (Chef's Attraction)
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RESULTS_DIR = Path("/home/dt/Projects/quantum-agent-memory/results/ibm_hardware")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

TOKEN_FILE = Path("/home/dt/.ibm_quantum_token")
LOG_FILE = RESULTS_DIR / "cron.log"


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def get_token():
    # Try env first, then file
    token = os.environ.get("IBM_QUANTUM_TOKEN")
    if token:
        return token.strip()
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    return None


def build_clustering_circuit(n=8):
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(n)
    gamma, beta = 1.2, 0.8
    for i in range(n):
        qc.h(i)
    for i in range(n):
        for j in range(i + 1, n):
            weight = 0.3 + 0.2 * ((i * 7 + j * 3) % 5) / 5.0
            qc.cx(i, j)
            qc.rz(2 * gamma * weight, j)
            qc.cx(i, j)
    for i in range(n):
        for j in range(i + 1, n):
            qc.cx(i, j)
            qc.rz(2 * gamma * 0.15, j)
            qc.cx(i, j)
    for i in range(n):
        qc.rx(2 * beta, i)
    qc.measure_all()
    return qc


def build_compaction_circuit(n=12, K=6):
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(n)
    gamma, beta = 0.9, 0.6
    for i in range(n):
        qc.h(i)
    for i in range(n):
        val = 0.2 + 0.6 * ((i * 11 + 3) % 7) / 7.0
        qc.rz(gamma * val, i)
    for i in range(n):
        for j in range(i + 1, n):
            pair = 0.1 + 0.3 * ((i * 5 + j * 13) % 9) / 9.0
            if pair > 0.15:
                qc.cx(i, j)
                qc.rz(gamma * pair / 2, j)
                qc.cx(i, j)
    pen = 6.0 * (1 - 2 * K)
    for i in range(n):
        qc.rz(-gamma * pen / 2, i)
    pen_q = 12.0
    for i in range(n):
        for j in range(i + 1, n):
            qc.cx(i, j)
            qc.rz(-gamma * pen_q / 2, j)
            qc.cx(i, j)
    for i in range(n):
        qc.rx(2 * beta, i)
    qc.measure_all()
    return qc


def build_recall_circuit(n=12, K=5):
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(n)
    gamma, beta = 1.0, 0.7
    for i in range(n):
        qc.h(i)
    for i in range(n):
        rel = 0.1 + 0.5 * ((i * 7 + 2) % 6) / 6.0
        rec = 0.3 + 0.5 * i / n
        qc.rz(gamma * (0.4 * rel + 0.1 * rec), i)
    for i in range(n):
        for j in range(i + 1, n):
            syn = 0.05 + 0.2 * ((i * 3 + j * 7) % 11) / 11.0
            div = 0.3 + 0.4 * ((i * 13 + j * 5) % 8) / 8.0
            pair = 0.3 * syn + 0.2 * div
            if pair > 0.05:
                qc.cx(i, j)
                qc.rz(gamma * pair / 2, j)
                qc.cx(i, j)
    pen = 6.0 * (1 - 2 * K)
    for i in range(n):
        qc.rz(-gamma * pen / 2, i)
    pen_q = 12.0
    for i in range(n):
        for j in range(i + 1, n):
            qc.cx(i, j)
            qc.rz(-gamma * pen_q / 2, j)
            qc.cx(i, j)
    for i in range(n):
        qc.rx(2 * beta, i)
    qc.measure_all()
    return qc


def main():
    token = get_token()
    if not token:
        log("ERROR: No IBM Quantum token found. Set IBM_QUANTUM_TOKEN or write to ~/.ibm_quantum_token")
        sys.exit(1)

    try:
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
        from qiskit import transpile
    except ImportError:
        log("ERROR: qiskit-ibm-runtime not installed")
        sys.exit(1)

    log("Starting IBM Quantum hardware run...")

    try:
        QiskitRuntimeService.save_account(
            channel="ibm_quantum", token=token, overwrite=True,
        )
        service = QiskitRuntimeService(channel="ibm_quantum")

        from qiskit_ibm_runtime import least_busy
        backends = service.backends()
        suitable = [b for b in backends if b.num_qubits >= 12 and b.status().operational]
        if not suitable:
            suitable = [b for b in backends if b.status().operational]
        backend = least_busy(suitable)
        log(f"Backend: {backend.name} ({backend.num_qubits} qubits)")

        circuits = {
            "clustering": build_clustering_circuit(8),
            "compaction": build_compaction_circuit(12, 6),
            "recall": build_recall_circuit(12, 5),
        }

        run_results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "backend": backend.name,
            "qubits": backend.num_qubits,
            "layers": {},
        }

        for name, qc in circuits.items():
            log(f"Submitting {name}...")
            transpiled = transpile(qc, backend=backend, optimization_level=2)
            sampler = SamplerV2(backend)
            job = sampler.run([transpiled], shots=1024)
            job_id = job.job_id()
            log(f"  Job ID: {job_id} — waiting...")

            result = job.result()
            counts = result[0].data.meas.get_counts()
            top = sorted(counts.items(), key=lambda x: -x[1])[:5]

            run_results["layers"][name] = {
                "job_id": job_id,
                "depth": transpiled.depth(),
                "gates": transpiled.size(),
                "top_bitstrings": {bs: cnt for bs, cnt in top},
                "total_shots": 1024,
            }

            log(f"  {name} done: depth={transpiled.depth()}, top={top[0][0]}({top[0][1]}/1024)")

        # Save results
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = RESULTS_DIR / f"ibm_run_{ts}.json"
        with open(out_file, "w") as f:
            json.dump(run_results, f, indent=2)

        log(f"Results saved to {out_file}")
        log("IBM Quantum hardware run complete ✅")

    except Exception as e:
        log(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
