#!/usr/bin/env python3
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Tuple, Optional

TZ = timezone(timedelta(hours=8))

# Portable path resolution (works across different assistants/users)
SCRIPT_PATH = Path(__file__).resolve()
# Expected install path: <workspace>/skills/token-stats-reporter/scripts/token-show.py
WORKSPACE = SCRIPT_PATH.parents[3] if len(SCRIPT_PATH.parents) >= 4 else Path.cwd()
OPENCLAW_HOME = WORKSPACE.parent if WORKSPACE.name == 'workspace' else (Path.home() / '.openclaw')
SESSIONS_DIR = OPENCLAW_HOME / 'agents' / 'main' / 'sessions'
COUNTER_FILE = WORKSPACE / 'memory' / 'token-counter.json'
STATE_FILE = WORKSPACE / 'memory' / 'token-agg-state.json'


def now_ym() -> str:
    return datetime.now(TZ).strftime('%Y-%m')


def _fmt_km(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)


def _fmt_cny(v: float) -> str:
    return f"¥{v:.4f}" if v < 1 else f"¥{v:.2f}"


def _parse_dt(v) -> Optional[datetime]:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        if v > 1e12:
            v = v / 1000.0
        try:
            return datetime.fromtimestamp(v, TZ)
        except Exception:
            return None
    if isinstance(v, str):
        try:
            s = v.replace('Z', '+00:00')
            dt = datetime.fromisoformat(s)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=TZ)
            return dt.astimezone(TZ)
        except Exception:
            return None
    return None


def _usage_tuple(usage: Dict) -> Tuple[int, int, int]:
    i = int(usage.get('input', usage.get('inputTokens', 0)) or 0)
    o = int(usage.get('output', usage.get('outputTokens', 0)) or 0)
    c = int(usage.get('cacheRead', usage.get('cacheReadTokens', 0)) or 0)
    return i, o, c


def _usage_cost(usage: Dict) -> float:
    try:
        total = (usage.get('cost') or {}).get('total')
        return float(total) if total is not None else 0.0
    except Exception:
        return 0.0


def _load_json(path: Path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        pass
    return default


def _save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')


def _load_counter(month: str):
    data = _load_json(COUNTER_FILE, {'month': month, 'count': 0})
    if data.get('month') != month:
        data = {'month': month, 'count': 0}
    data['count'] = int(data.get('count', 0)) + 1
    _save_json(COUNTER_FILE, data)


def _default_state(month: str):
    return {
        'month': month,
        'totals': {
            'in': 0,
            'out': 0,
            'cache': 0,
            'count': 0,
            'cost': 0.0,
        },
        'files': {},
        # 用于跨 reset/多文件去重（只保留当月）
        'seen_ids': [],
        # 最新一条 assistant 有效消息
        'latest': {
            'ts': '',
            'in': 0,
            'out': 0,
            'cache': 0,
            'cost': 0.0,
            'model': 'unknown',
        },
    }


def _load_state(month: str):
    s = _load_json(STATE_FILE, _default_state(month))
    if s.get('month') != month:
        return _default_state(month)
    s.setdefault('totals', {'in': 0, 'out': 0, 'cache': 0, 'count': 0, 'cost': 0.0})
    s.setdefault('files', {})
    s.setdefault('seen_ids', [])
    s.setdefault('latest', {'ts': '', 'in': 0, 'out': 0, 'cache': 0, 'cost': 0.0, 'model': 'unknown'})
    return s


def _update_latest(state: Dict, dt: datetime, i: int, o: int, c: int, cost: float, model: str):
    prev_ts = _parse_dt(state['latest'].get('ts'))
    if prev_ts is None or dt > prev_ts:
        state['latest'] = {
            'ts': dt.isoformat(),
            'in': i,
            'out': o,
            'cache': c,
            'cost': cost,
            'model': model or 'unknown',
        }


def incremental_aggregate(month: str):
    if not SESSIONS_DIR.exists():
        return _default_state(month)

    state = _load_state(month)
    seen_ids = set(state.get('seen_ids', []))

    files = sorted(SESSIONS_DIR.glob('*.jsonl*'))
    for fp in files:
        fkey = str(fp)
        fmeta = state['files'].get(fkey, {'offset': 0, 'size': 0})
        old_offset = int(fmeta.get('offset', 0))

        try:
            size = fp.stat().st_size
        except Exception:
            continue

        # 文件被截断或替换，回退到头部扫描（依赖 seen_ids 去重）
        if old_offset < 0 or old_offset > size:
            old_offset = 0

        try:
            with fp.open('r', encoding='utf-8') as f:
                if old_offset:
                    f.seek(old_offset)

                while True:
                    line = f.readline()
                    if not line:
                        break

                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue

                    if obj.get('type') != 'message':
                        continue

                    msg = obj.get('message', {})
                    if msg.get('role') != 'assistant':
                        continue

                    usage = msg.get('usage') or {}
                    if not usage:
                        continue

                    content = msg.get('content') or []
                    if not any(isinstance(c, dict) and c.get('type') == 'text' for c in content):
                        continue

                    dt = _parse_dt(msg.get('timestamp')) or _parse_dt(obj.get('timestamp'))
                    if dt is None:
                        continue

                    i, o, c = _usage_tuple(usage)
                    cost = _usage_cost(usage)
                    model = (msg.get('model') or 'unknown').strip()

                    # 过滤投递镜像等非真实推理记录
                    if model.lower() == 'delivery-mirror':
                        continue

                    # 最新值随时更新
                    _update_latest(state, dt, i, o, c, cost, model)

                    # 只累计当月
                    if dt.strftime('%Y-%m') != month:
                        continue

                    msg_id = obj.get('id')
                    dedup_key = msg_id or f"{fkey}:{dt.isoformat()}:{i}:{o}:{c}"
                    if dedup_key in seen_ids:
                        continue

                    seen_ids.add(dedup_key)
                    state['totals']['in'] += i
                    state['totals']['out'] += o
                    state['totals']['cache'] += c
                    state['totals']['count'] += 1
                    state['totals']['cost'] = float(state['totals'].get('cost', 0.0)) + cost

                new_offset = f.tell()
                state['files'][fkey] = {'offset': new_offset, 'size': size}
        except Exception:
            continue

    # 避免状态文件无限增长，seen_ids 做温和裁剪（保留最近 20 万）
    if len(seen_ids) > 200000:
        # set 无序，转 list 后截断即可（只影响极端重复扫描效率，不影响正确性）
        seen_ids = set(list(seen_ids)[-200000:])

    state['seen_ids'] = list(seen_ids)
    _save_json(STATE_FILE, state)
    return state


def main():
    month = now_ym()
    _load_counter(month)

    state = incremental_aggregate(month)

    si = int(state['latest'].get('in', 0))
    so = int(state['latest'].get('out', 0))
    sc = int(state['latest'].get('cache', 0))
    single_cost = float(state['latest'].get('cost', 0.0) or 0.0)
    model = state['latest'].get('model', 'unknown')

    mi = int(state['totals'].get('in', 0))
    mo = int(state['totals'].get('out', 0))
    mc = int(state['totals'].get('cache', 0))
    mcnt = int(state['totals'].get('count', 0))
    monthly_cost = float(state['totals'].get('cost', 0.0) or 0.0)

    single_total = si + so + sc
    single_billable = si + so
    monthly_total = mi + mo + mc

    single_cost_txt = _fmt_cny(single_cost) if single_cost > 0 else '¥0.00'
    monthly_cost_txt = _fmt_cny(monthly_cost) if monthly_cost > 0 else '¥0.00'

    print(
        f"📊 Token: {si} in / {so} out | cacheRead: {sc} | 本次总消耗: {_fmt_km(single_total)} | "
        f"本次计费token: {single_billable} | 本月: {mcnt} 次 | 月累计总消耗: {_fmt_km(monthly_total)} | "
        f"本次费用: {single_cost_txt} | 本月费用: {monthly_cost_txt} | 模型: {model}"
    )


if __name__ == '__main__':
    main()
