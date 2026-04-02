from __future__ import annotations


def build_heartbeat(client, decisions: list[dict], risk_state: dict, learning_snapshot: dict) -> dict:
    briefing = client.get_briefing()
    return {
        'briefing': briefing,
        'decision_count': len(decisions),
        'accepted_candidates': sum(1 for row in decisions if row.get('decision') == 'candidate'),
        'risk_state': risk_state,
        'learning_snapshot': learning_snapshot,
    }
