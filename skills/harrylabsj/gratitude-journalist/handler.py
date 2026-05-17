#!/usr/bin/env python3
import json
import os
import re
import sys
from typing import Any, Dict, List


def _load_skill_meta(slug):
    path = os.path.join(os.path.dirname(__file__), 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    meta = re.search(r'^---$(.*?)^---$', content, re.DOTALL | re.MULTILINE)
    return meta.group(1).strip() if meta else ''


def _normalize_inputs(inputs: Any) -> str:
    if inputs is None:
        return ''
    if isinstance(inputs, str):
        return inputs.strip()
    try:
        return json.dumps(inputs, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(inputs)


LENS_KEYWORDS = {
    'people': ['friend', 'partner', 'family', 'child', 'kid', 'parent', 'teacher', 'neighbor', 'someone'],
    'body': ['body', 'health', 'sleep', 'walk', 'breath', 'rest', 'energy', 'exercise'],
    'environment': ['sun', 'rain', 'home', 'window', 'quiet', 'tea', 'coffee', 'tree', 'weather', 'room'],
    'luck': ['lucky', 'unexpected', 'chance', 'timing', 'helped', 'worked out'],
    'learning': ['learn', 'book', 'read', 'lesson', 'insight', 'practice'],
    'self-kindness': ['rest', 'pause', 'gentle', 'forgave', 'kind to myself', 'slow down'],
}

DEFAULT_LENS_ORDER = ['people', 'body', 'environment', 'learning', 'self-kindness']

WHY_BY_LENS = {
    'people': 'it reminded me that support often arrives through ordinary gestures.',
    'body': 'it showed me that my body is still helping me, even in small ways.',
    'environment': 'it gave the day texture, steadiness, or beauty instead of pure rush.',
    'luck': 'it lowered friction at the right moment and made the day feel a little lighter.',
    'learning': 'it gave me something useful to carry forward, not just consume and forget.',
    'self-kindness': 'it interrupted self-pressure and created a little more room to breathe.',
}

FEELING_BY_LENS = {
    'people': 'Warmth and connection.',
    'body': 'Relief and appreciation.',
    'environment': 'Calm and steadiness.',
    'luck': 'Surprise and gratitude.',
    'learning': 'Hope and grounded confidence.',
    'self-kindness': 'Gentleness and self-respect.',
}

FOLLOW_UP_BY_LENS = {
    'people': 'Send a short thank-you note or mention it next time you talk.',
    'body': 'Protect one tiny behavior that supported this moment.',
    'environment': 'Notice how to recreate this setting tomorrow.',
    'luck': 'Write down what made the good timing possible, if anything.',
    'learning': 'Capture the lesson in one line so it sticks.',
    'self-kindness': 'Repeat the same gentle move when stress rises again.',
}

FALLBACK_MOMENTS = {
    'people': 'a small moment of support from someone close to me',
    'body': 'one sign my body kept carrying me today',
    'environment': 'a calm detail in my environment that softened the day',
    'learning': 'one thing I learned that made me a little wiser or steadier',
    'self-kindness': 'one moment I treated myself with less pressure than usual',
}


class GratitudeJournalist:
    def __init__(self, inputs: Any):
        self.raw = _normalize_inputs(inputs)
        self.lower = self.raw.lower()
        self.hard_day = any(word in self.lower for word in ['hard', 'heavy', 'grief', 'angry', 'tired', 'exhausted', 'rough'])
        self.entries = self._build_entries()
        self.pattern = self._detect_pattern()

    def _chunks(self) -> List[str]:
        text = self.raw.replace('\n', ';')
        pieces = re.split(r'[;•]+', text)
        if len(pieces) <= 1:
            pieces = re.split(r'(?<=[.!?])\s+', text)
        cleaned = []
        for piece in pieces:
            piece = re.sub(r'^\s*(\d+[.)-]?|[-*])\s*', '', piece).strip()
            if piece:
                cleaned.append(piece)
        return cleaned[:5]

    def _infer_lens(self, chunk: str) -> str:
        lower = chunk.lower()
        for lens, keywords in LENS_KEYWORDS.items():
            if any(keyword in lower for keyword in keywords):
                return lens
        return 'environment'

    def _fallback_entries(self) -> List[Dict[str, str]]:
        entries: List[Dict[str, str]] = []
        for lens in DEFAULT_LENS_ORDER[:3]:
            entries.append({
                'lens': lens,
                'item': FALLBACK_MOMENTS[lens],
                'why': WHY_BY_LENS[lens],
                'feeling': 'Small relief and honesty.' if self.hard_day else FEELING_BY_LENS[lens],
                'follow_up': FOLLOW_UP_BY_LENS[lens],
            })
        return entries

    def _build_entries(self) -> List[Dict[str, str]]:
        chunks = self._chunks()
        if len(chunks) < 2:
            return self._fallback_entries()
        entries: List[Dict[str, str]] = []
        for chunk in chunks[:5]:
            lens = self._infer_lens(chunk)
            item = chunk[:1].upper() + chunk[1:]
            entries.append({
                'lens': lens,
                'item': item,
                'why': WHY_BY_LENS[lens],
                'feeling': 'Relief and steadiness.' if self.hard_day and lens != 'people' else FEELING_BY_LENS[lens],
                'follow_up': FOLLOW_UP_BY_LENS[lens],
            })
        return entries

    def _detect_pattern(self) -> str:
        if self.hard_day:
            return 'Even on a hard day, small supports and brief moments of relief still counted.'
        lenses = [entry['lens'] for entry in self.entries]
        if lenses.count('people') >= 2:
            return 'Support is showing up through ordinary people and small gestures.'
        if any(lens in lenses for lens in ['environment', 'body']):
            return 'Small steady details are carrying more of the day than dramatic events.'
        return 'Ordinary moments are becoming easier to notice when you slow down long enough to name them.'

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Gratitude Entry')
        lines.append('')
        lines.append('## Today I am grateful for')
        for index, entry in enumerate(self.entries, 1):
            lines.append(f"{index}. {entry['item']}")
            lines.append(f"   - Why it mattered: {entry['why']}")
            lines.append(f"   - Feeling it created: {entry['feeling']}")
            lines.append(f"   - Follow-up action, if any: {entry['follow_up']}")
            lines.append('')
        lines.append('## Pattern to Notice')
        lines.append(f'- {self.pattern}')
        return '\n'.join(lines)


def handle(inputs):
    _load_skill_meta('gratitude-journalist')
    journal = GratitudeJournalist(inputs)
    return journal.render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
