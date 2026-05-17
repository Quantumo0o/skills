#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, List, Tuple

SKILL_SLUG = 'boardgame-picker'
PROMPT_TEMPLATE = """Match the user's group to the best board game style.
Read player count, available time, newcomer level, competition appetite, and table mood. Recommend the best 1 to 2 categories, one backup category, one type to avoid, and one fast-start suggestion. Do not pretend to have live catalog data."""

TYPE_LIBRARY = {
    'party': {
        'label': 'Party / Icebreaker',
        'best_for': 'Large or lively groups that need fast rules and frequent laughter.',
        'keywords': 'word play, drawing, clueing, reaction, fast rounds',
        'examples': 'Codenames, Just One, Telestrations',
        'avoid_when': 'the table wants deep planning or a very serious competitive arc',
    },
    'coop': {
        'label': 'Cooperative / Team Challenge',
        'best_for': 'Groups that want shared wins, teamwork, and lower direct conflict.',
        'keywords': 'cooperation, crisis management, shared puzzle, team communication',
        'examples': 'Pandemic, The Crew, Forbidden Desert',
        'avoid_when': 'alpha-player behavior is likely or the group wants strong rivalry',
    },
    'deduction': {
        'label': 'Deduction / Bluff / Mystery',
        'best_for': 'Players who enjoy reading people, hidden information, and social tension.',
        'keywords': 'hidden roles, bluffing, accusations, logic clues',
        'examples': 'Avalon, Deception: Murder in Hong Kong, Coup',
        'avoid_when': 'the table has low trust, low energy, or large experience gaps',
    },
    'family': {
        'label': 'Family / Gateway',
        'best_for': 'Mixed ages, newcomers, and groups that want low explanation cost.',
        'keywords': 'set collection, tile laying, route building, light drafting',
        'examples': 'Ticket to Ride, Azul, Kingdomino',
        'avoid_when': 'the table specifically wants a heavy brain-burn challenge',
    },
    'strategy': {
        'label': 'Strategy / Planning',
        'best_for': 'Smaller tables with time, focus, and appetite for deeper decisions.',
        'keywords': 'engine building, worker placement, area control, long-term planning',
        'examples': 'Splendor, Everdell, 7 Wonders Duel',
        'avoid_when': 'the room is impatient, very new, or only has a short time window',
    },
}


def _load_skill_meta(skill_name: str) -> Dict[str, str]:
    path = os.path.join(os.path.dirname(__file__), 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as handle:
        content = handle.read()
    match = re.search(r'^---\s*\n(.*?)\n---\s*', content, re.DOTALL | re.MULTILINE)
    meta: Dict[str, str] = {}
    if match:
        for line in match.group(1).splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip()] = value.strip()
    meta['skill_name'] = skill_name or meta.get('name', SKILL_SLUG)
    return meta


def _load_prompt_template(skill_name: str) -> str:
    del skill_name
    return PROMPT_TEMPLATE


def _normalize_key(key: Any) -> str:
    return re.sub(r'[^a-z0-9_\u4e00-\u9fff]+', '_', str(key).strip().lower()).strip('_')


def _clean_text(value: Any) -> str:
    if value is None:
        return ''
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def _normalize_map(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in data.items():
        normalized[_normalize_key(key)] = value
    return normalized


def _parse_text_map(raw: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    for line in raw.splitlines():
        if re.search(r'[:：]', line):
            key, value = re.split(r'[:：]', line, maxsplit=1)
            data[_normalize_key(key)] = value.strip()
    return data


def _coerce_input(user_input: Any) -> Tuple[str, Dict[str, Any]]:
    if isinstance(user_input, dict):
        return json.dumps(user_input, ensure_ascii=False), _normalize_map(user_input)
    raw = _clean_text(user_input)
    if raw.startswith('{') and raw.endswith('}'):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return raw, _normalize_map(parsed)
        except json.JSONDecodeError:
            pass
    return raw, _parse_text_map(raw)


def _pick(data: Dict[str, Any], keys: List[str], default: str = '') -> str:
    for key in keys:
        normalized = _normalize_key(key)
        if normalized in data:
            text = _clean_text(data[normalized])
            if text:
                return text
    return default


def _to_int(value: Any, default: int = 0) -> int:
    if isinstance(value, int):
        return value
    text = _clean_text(value)
    match = re.search(r'(\d+)', text)
    return int(match.group(1)) if match else default


def _contains_any(text: str, keywords: List[str]) -> bool:
    lowered = text.lower()
    return any(word in lowered for word in keywords)


def _infer_players(text: str) -> int:
    match = re.search(r'(\d+)\s*(?:players?|ppl|people|人)', text.lower())
    return int(match.group(1)) if match else 0


def _infer_minutes(text: str) -> int:
    match = re.search(r'(\d+)\s*(?:min|mins|minute|minutes|分钟)', text.lower())
    return int(match.group(1)) if match else 0


def _score_profiles(raw: str, data: Dict[str, Any]) -> Tuple[Dict[str, int], int, int, str]:
    scores = {name: 0 for name in TYPE_LIBRARY}
    players = _to_int(_pick(data, ['players', 'player_count', '人数']), 0) or _infer_players(raw)
    minutes = _to_int(_pick(data, ['duration', 'minutes', 'time', '时长']), 0) or _infer_minutes(raw)
    experience = _pick(data, ['experience', 'newbie', 'skill_level', '是否新手', '新手'])
    competition = _pick(data, ['competition', 'competitive', 'intensity', '竞争强度'])
    mood = _pick(data, ['mood', 'vibe', 'atmosphere', '氛围'])
    age_mix = _pick(data, ['age_mix', 'age', 'ages', '年龄层'])
    tolerance = _pick(data, ['tolerance', 'fault_tolerance', 'rules_tolerance', '容错度'])
    context = ' '.join([raw, experience, competition, mood, age_mix, tolerance]).lower()

    if players >= 6:
        scores['party'] += 4
        scores['deduction'] += 2
        scores['coop'] += 1
        scores['strategy'] -= 2
    elif 4 <= players <= 5:
        scores['family'] += 2
        scores['coop'] += 2
        scores['deduction'] += 1
    elif 2 <= players <= 3:
        scores['strategy'] += 3
        scores['family'] += 1
        scores['coop'] += 1
        scores['party'] -= 1

    if minutes:
        if minutes <= 30:
            scores['party'] += 3
            scores['family'] += 2
            scores['coop'] += 1
            scores['strategy'] -= 2
        elif minutes <= 60:
            scores['family'] += 2
            scores['coop'] += 1
            scores['deduction'] += 1
        else:
            scores['strategy'] += 3
            scores['coop'] += 2
            scores['party'] -= 1

    if _contains_any(context, ['new', 'newbie', 'beginner', 'first time', 'family', 'kids', 'children', 'mixed ages', '亲子', '新手']):
        scores['family'] += 4
        scores['party'] += 2
        scores['coop'] += 1
        scores['strategy'] -= 3
        scores['deduction'] -= 1
    if _contains_any(context, ['cooperate', 'co-op', 'cooperative', 'team', 'together', 'help each other', 'teamwork', '合作']):
        scores['coop'] += 4
    if _contains_any(context, ['mystery', 'bluff', 'detective', 'deduction', 'hidden role', 'social deduction', '推理', '狼人']):
        scores['deduction'] += 4
    if _contains_any(context, ['lively', 'laugh', 'party', 'icebreaker', 'social', 'noisy', '欢乐', '热闹']):
        scores['party'] += 4
    if _contains_any(context, ['strategy', 'planning', 'deep', 'thinky', 'heavy', 'brain burn', '规划', '烧脑']):
        scores['strategy'] += 3
    if _contains_any(context, ['low competition', 'gentle', 'casual', 'light pressure', 'friendly', '不想太卷', '低竞争']):
        scores['coop'] += 3
        scores['family'] += 2
        scores['deduction'] -= 1
    if _contains_any(context, ['high competition', 'duel', 'cutthroat', 'intense', '想赢', '高竞争']):
        scores['strategy'] += 2
        scores['deduction'] += 1
    if _contains_any(context, ['easy mistakes', 'low rules friction', 'forgiving', '容错', '轻松']):
        scores['family'] += 2
        scores['party'] += 1
        scores['strategy'] -= 1

    return scores, players, minutes, context


def _sorted_types(scores: Dict[str, int]) -> List[Tuple[str, int]]:
    return sorted(scores.items(), key=lambda item: (item[1], TYPE_LIBRARY[item[0]]['label']), reverse=True)


def _table_tempo(players: int, minutes: int, context: str) -> str:
    tempo_bits: List[str] = []
    if players:
        tempo_bits.append(f'{players} players')
    else:
        tempo_bits.append('player count not fully specified')
    if minutes:
        tempo_bits.append(f'about {minutes} minutes')
    else:
        tempo_bits.append('time window not fully specified')
    if _contains_any(context, ['new', 'newbie', 'family', 'kids', 'mixed ages', '新手', '亲子']):
        tempo_bits.append('newcomer-friendly table')
    if _contains_any(context, ['lively', 'party', 'social', 'laugh', '欢乐', '热闹']):
        tempo_bits.append('high social energy')
    elif _contains_any(context, ['calm', 'gentle', 'cozy', '合作', 'friendly']):
        tempo_bits.append('gentle room energy')
    return ', '.join(tempo_bits)


def _recommended_reason(profile_id: str, players: int, minutes: int, context: str) -> str:
    reason_bits = [TYPE_LIBRARY[profile_id]['best_for']]
    if profile_id == 'party' and players >= 6:
        reason_bits.append('The table is large enough that quick turns and easy laughter matter more than deep optimization.')
    if profile_id == 'coop' and _contains_any(context, ['low competition', 'team', 'co-op', 'cooperative', '合作']):
        reason_bits.append('Shared wins lower social friction and keep mixed skill players engaged.')
    if profile_id == 'family' and _contains_any(context, ['new', 'family', 'kids', 'mixed ages', '新手', '亲子']):
        reason_bits.append('The room likely benefits from low explanation cost and forgiving decisions.')
    if profile_id == 'deduction' and _contains_any(context, ['mystery', 'bluff', 'deduction', 'hidden role', '推理']):
        reason_bits.append('The group seems to enjoy reading people and talking through uncertainty.')
    if profile_id == 'strategy' and minutes >= 60:
        reason_bits.append('The time window is long enough to reward planning instead of rushing through rules.')
    return ' '.join(reason_bits)


def _avoid_reason(profile_id: str, context: str) -> str:
    del context
    return f"Avoid this style if {TYPE_LIBRARY[profile_id]['avoid_when']}."


def _quick_start(top_profile: str, context: str) -> str:
    if top_profile == 'party':
        return 'Explain only the win condition, run one demo round, and keep the first teach under 3 minutes.'
    if top_profile == 'coop':
        return 'Name one shared objective out loud, assign a first move to the least experienced player, and treat round one as a learning turn.'
    if top_profile == 'family':
        return 'Lead with the easiest scoring rule first, then add the optional detail only after one visible turn.'
    if top_profile == 'deduction':
        return 'Before the first round, tell the table whether this session should feel playful or competitive so bluff tension stays fun.'
    return 'Show the scoring arc first, then let players touch components before explaining every edge case.'


def _build_result(raw: str, data: Dict[str, Any], template: str) -> str:
    scores, players, minutes, context = _score_profiles(raw, data)
    ranked = _sorted_types(scores)
    top_ids = [item[0] for item in ranked[:2]]
    backup_id = ranked[2][0] if len(ranked) > 2 else ranked[0][0]
    avoid_id = ranked[-1][0]

    lines: List[str] = []
    lines.append('# Boardgame Match Card')
    lines.append('')
    lines.append('## Table Snapshot')
    lines.append(f'- Situation read: {_table_tempo(players, minutes, context)}')
    lines.append(f"- Decision frame: {template.splitlines()[0]}")
    lines.append(f"- Strongest fit right now: {TYPE_LIBRARY[top_ids[0]]['label']}")
    lines.append('')
    lines.append('## Recommended Types')
    for idx, profile_id in enumerate(top_ids, start=1):
        profile = TYPE_LIBRARY[profile_id]
        lines.append(f"### {idx}. {profile['label']}")
        lines.append(f"- Why it fits: {_recommended_reason(profile_id, players, minutes, context)}")
        lines.append(f"- Mechanism keywords: {profile['keywords']}")
        lines.append(f"- Example direction: classic titles like {profile['examples']} can help, but this is not a live catalog lookup.")
        lines.append('')
    lines.append('## Backup Type')
    lines.append(f"- {TYPE_LIBRARY[backup_id]['label']} — useful if the room energy shifts after the first game.")
    lines.append(f"- Why keep it in reserve: {_recommended_reason(backup_id, players, minutes, context)}")
    lines.append('')
    lines.append('## Avoid This Round')
    lines.append(f"- {TYPE_LIBRARY[avoid_id]['label']} — {_avoid_reason(avoid_id, context)}")
    lines.append('')
    lines.append('## Quick Start')
    lines.append(f"- {_quick_start(top_ids[0], context)}")
    return '\n'.join(lines)


def handle(args: Dict[str, Any]) -> Dict[str, str]:
    skill_name = args.get('skill_name', SKILL_SLUG) or SKILL_SLUG
    user_input = args.get('input', '')
    mode = args.get('mode', 'guide')
    meta = _load_skill_meta(skill_name)
    template = _load_prompt_template(skill_name)
    if mode == 'meta':
        return {'result': json.dumps(meta, ensure_ascii=False, indent=2)}
    if mode == 'prompt':
        return {'result': template}
    raw, data = _coerce_input(user_input)
    return {'result': _build_result(raw, data, template)}


if __name__ == '__main__':
    print(json.dumps(handle({'skill_name': SKILL_SLUG, 'input': 'Players: 6\nTime: 30 minutes\nMood: lively and social', 'mode': 'guide'}), ensure_ascii=False, indent=2))
