#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.cwd()
REPORT = WORKSPACE / 'runtime-doctor-report.json'

CHECKS = [
    ('workspace-memory', WORKSPACE / 'memory'),
    ('continuity-state', WORKSPACE / 'projects/xzenia/state/continuity-state.json'),
    ('autofallback-state', WORKSPACE / 'projects/xzenia/state/autofallback-state.json'),
]


def run():
    results = []
    for name, path in CHECKS:
        results.append({
            'check': name,
            'path': str(path),
            'exists': path.exists()
        })
    out = {
        'generatedAt': datetime.now().astimezone().isoformat(),
        'safe': True,
        'destructiveActions': [],
        'checks': results,
        'summary': 'non-destructive runtime diagnosis complete'
    }
    REPORT.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    run()
