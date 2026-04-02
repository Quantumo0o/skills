from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from simmer_sdk import SimmerClient

ROOT = Path(__file__).resolve().parent
MODULES = ROOT / 'modules'
if str(MODULES) not in sys.path:
    sys.path.insert(0, str(MODULES))

from btc_heartbeat import build_heartbeat
from btc_position_manager import enforce_risk_limits
from btc_regime_filter import evaluate_regime
from btc_self_learn import build_learning_snapshot
from btc_sprint_executor import execute_trade
from btc_sprint_signal import build_signal
from btc_trade_journal import append_journal, read_journal


DATA_DIR = ROOT / 'data'
JOURNAL_PATH = DATA_DIR / 'journal.jsonl'
LEARNING_PATH = DATA_DIR / 'learning.json'
DEFAULTS_PATH = ROOT / 'config' / 'defaults.json'


def load_config() -> dict:
    config = json.loads(DEFAULTS_PATH.read_text())
    env_map = {
        'BTC_SPRINT_DRY_RUN': ('dry_run', lambda v: v == '1'),
        'BTC_SPRINT_VALIDATE_REAL_PATH': ('validate_real_path', lambda v: v == '1'),
        'BTC_SPRINT_WINDOWS': ('windows', lambda v: [item.strip() for item in v.split(',') if item.strip()]),
        'TRADING_VENUE': ('trading_venue', str),
        'BINANCE_SYMBOL': ('binance_symbol', str),
        'BINANCE_INTERVAL': ('binance_interval', str),
    }
    for env_key, (cfg_key, caster) in env_map.items():
        if env_key in os.environ and os.environ[env_key]:
            config[cfg_key] = caster(os.environ[env_key])
    config.setdefault('dry_run', True)
    config.setdefault('validate_real_path', True)
    config.setdefault('binance_symbol', 'BTCUSDT')
    config.setdefault('binance_interval', '1m')
    return config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='BTC sprint bot for Simmer')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--dry-run', action='store_true', help='Never submit a live trade')
    mode.add_argument('--live', action='store_true', help='Submit real trades when approved')
    parser.add_argument('--once', action='store_true', help='Run one cycle')
    parser.add_argument('--loop', action='store_true', help='Run continuously')
    parser.add_argument('--validate-real-path', action='store_true', help='Call prepare_real_trade during dry-run')
    return parser.parse_args()


def get_client(config: dict, dry_run: bool) -> SimmerClient:
    api_key = os.environ.get('SIMMER_API_KEY')
    if not api_key:
        raise SystemExit('SIMMER_API_KEY is required')
    return SimmerClient(api_key=api_key, venue=config['trading_venue'], live=not dry_run)


def market_window_from_tags(tags: list[str]) -> str:
    if 'fast-5m' in tags:
        return '5m'
    if 'fast-15m' in tags:
        return '15m'
    return 'unknown'


def run_cycle(config: dict, *, dry_run: bool, validate_real_path: bool) -> dict:
    client = get_client(config, dry_run=dry_run)
    settings = client.get_settings()
    positions = client.get_positions(venue=config['trading_venue'])
    journal_rows = read_journal(JOURNAL_PATH)

    decisions = []
    latest_risk_state = {}
    fast_markets = client.get_fast_markets(asset=config['asset'], limit=20)
    for market in fast_markets:
        tags = getattr(market, 'tags', []) or []
        window = market_window_from_tags(tags)
        if window not in config['windows']:
            continue
        context = client.get_market_context(market.id)
        signal = build_signal(
            window=window,
            context=context,
            symbol=config['binance_symbol'],
            interval=config['binance_interval'],
            min_edge=config['min_edge'],
        )
        regime = evaluate_regime(context, signal, config)
        risk_state = enforce_risk_limits(settings, positions, config, config['skill_slug'], journal_rows)
        latest_risk_state = risk_state

        row = {
            'ts': datetime.now(timezone.utc).isoformat(),
            'market_id': market.id,
            'question': getattr(market, 'question', ''),
            'window': window,
            'decision': 'skipped',
            'signal_action': signal.action,
            'signal_data': signal.to_signal_data(),
            'regime': regime,
            'risk_state': risk_state,
            'result_type': 'skip',
        }

        if regime['approved'] and risk_state['allowed'] and signal.action in {'yes', 'no'}:
            execution = execute_trade(
                client,
                market_id=market.id,
                side=signal.action,
                amount=risk_state['trade_amount_usd'],
                signal=signal,
                regime=regime,
                live=not dry_run,
                source='btc_sprint_stack.binance_momentum',
                skill_slug=config['skill_slug'],
                venue=config['trading_venue'],
                validate_real_path=validate_real_path,
            )
            row['decision'] = 'candidate'
            row.update(execution)
        append_journal(JOURNAL_PATH, row)
        decisions.append(row)

    learning_snapshot = build_learning_snapshot(journal_rows + decisions, config)
    LEARNING_PATH.write_text(json.dumps(learning_snapshot, indent=2, sort_keys=True))
    heartbeat = build_heartbeat(client, decisions, latest_risk_state, learning_snapshot)
    output = {
        'ts': datetime.now(timezone.utc).isoformat(),
        'dry_run': dry_run,
        'validate_real_path': validate_real_path,
        'decisions': decisions,
        'heartbeat': heartbeat,
    }
    print(json.dumps(output, indent=2, default=str))
    return output


def main() -> None:
    args = parse_args()
    config = load_config()
    dry_run = True
    if args.live:
        dry_run = False
    elif args.dry_run:
        dry_run = True
    elif 'dry_run' in config:
        dry_run = bool(config['dry_run'])

    validate_real_path = args.validate_real_path or bool(config.get('validate_real_path'))
    if args.loop:
        while True:
            run_cycle(config, dry_run=dry_run, validate_real_path=validate_real_path)
            time.sleep(config['cycle_interval_minutes'] * 60)
    else:
        run_cycle(config, dry_run=dry_run, validate_real_path=validate_real_path)


if __name__ == '__main__':
    main()
