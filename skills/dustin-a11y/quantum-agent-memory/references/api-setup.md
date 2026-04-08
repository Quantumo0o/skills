# API Server Setup

## Requirements

- Python 3.10+
- Qiskit 2.0+, Qiskit Aer 0.15+
- FastAPI, uvicorn, requests, numpy
- A running Mem0 instance

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `QUANTUM_API_TOKEN` | (none) | Bearer token for auth. Leave empty for no auth |
| `MEM0_URL` | `http://localhost:8500` | Mem0 API base URL |

## Run Directly

```bash
pip install fastapi uvicorn requests numpy qiskit qiskit-aer
QUANTUM_API_TOKEN=your-secret MEM0_URL=http://your-mem0:8500 python scripts/quantum_api.py
```

## Systemd Service

```ini
[Unit]
Description=Quantum Memory API Server
After=network.target

[Service]
Type=simple
User=root
Environment="PATH=/path/to/venv/bin:/usr/bin:/bin"
Environment="QUANTUM_API_TOKEN=your-secret-token"
Environment="MEM0_URL=http://localhost:8500"
ExecStart=/path/to/venv/bin/python /path/to/quantum_api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable quantum-memory-api
sudo systemctl start quantum-memory-api
```

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/` | No | Health check |
| POST | `/quantum-recall` | Yes | QAOA-optimized memory selection for a query |
| POST | `/quantum-compact` | Yes | QAOA-optimized keep/archive decision |
| GET | `/docs` | No | Swagger UI |

## IBM Hardware Cron

For scheduled IBM quantum hardware runs, use `scripts/ibm_cron.py`:

```bash
# Add to crontab — 5x daily
0 15,18,21,0,3 * * * /path/to/venv/bin/python /path/to/ibm_cron.py
```

Requires `qiskit-ibm-runtime` and an IBM Quantum token stored at
`~/.ibm_quantum_token` or in the `IBM_QUANTUM_TOKEN` env var.

Free tier: 10 min QPU/month. Each run uses ~1 second. 5x daily = ~2.5 min/month.
