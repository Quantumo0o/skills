from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

journal_path = Path(__file__).resolve().parents[1] / 'data' / 'journal.jsonl'
if not journal_path.exists():
    raise SystemExit('No journal yet')
rows = [json.loads(line) for line in journal_path.read_text().splitlines() if line.strip()]
summary = {
    'rows': len(rows),
    'decisions': Counter(row.get('decision') for row in rows),
    'result_types': Counter(row.get('result_type') for row in rows),
}
print(json.dumps(summary, indent=2, default=str))
