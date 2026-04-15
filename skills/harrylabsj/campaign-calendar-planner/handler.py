#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Union

WINDOW_RULES = {
    'Q1': ['q1', 'q1', 'january', 'february', 'march', 'new year', 'spring'],
    'Q2': ['q2', 'april', 'may', 'june', 'spring', 'easter', "mother's day"],
    'Q3': ['q3', 'july', 'august', 'september', 'summer', 'back to school'],
    'Q4': ['q4', 'october', 'november', 'december', 'holiday', 'black friday', 'christmas', '11.11'],
}

GOAL_RULES = {
    'Awareness': ['awareness', 'brand', 'reach', 'impression', 'brand campaign'],
    'Traffic': ['traffic', 'click', 'visit', 'landing page', 'ctr'],
    'Conversion': ['conversion', 'sales', 'orders', 'revenue', 'direct response'],
    'Revenue': ['revenue', 'gmv', 'sales', 'order value', 'aov'],
    'Retention': ['retention', 'loyalty', 'repeat', 'vip', 'lapsed', 'winback'],
    'New Launch': ['launch', 'new product', 'new sku', 'rollout', 'go live'],
}

CHANNEL_RULES = {
    'Shopify / DTC': ['shopify', 'dtc', 'storefront', 'pdp'],
    'Amazon': ['amazon'],
    'TikTok Shop': ['tiktok', 'douyin'],
    'Xiaohongshu': ['xiaohongshu', 'rednote', 'xhs'],
    'Meta Ads': ['meta', 'facebook', 'instagram', 'paid social'],
    'Google Ads': ['google', 'youtube'],
    'Email / CRM': ['email', 'crm', 'klaviyo', 'mailchimp'],
    'JD': ['jd', 'jingdong'],
    'Taobao': ['taobao', '1688'],
    'WeChat': ['wechat', 'weixin'],
}

SEASONAL_DATES = {
    "New Year's Day": "January 1",
    "Lunar New Year": "Late January – February",
    "Valentine's Day": "February 14",
    "International Women's Day": "March 8",
    "Easter": "March – April",
    "Q1 Sales Season": "January – March",
    "April Sale / Spring": "April",
    "May Day": "May 1",
    "Mother's Day (CN)": "Second Sunday of May",
    "618 Mid-Year Festival": "June 18",
    "Summer Sale": "June – August",
    "Back to School": "August – September",
    "Mid-Autumn Festival": "September – October",
    "National Day (CN)": "October 1",
    "11.11 Singles Day": "November 11",
    "Black Friday / Cyber Monday": "Fourth week of November",
    "Holiday Season": "December",
    "Christmas / Year End": "December 25",
}

CampaignInput = Union[str, Dict[str, Any]]


def _score_rules(text: str, rules: Dict[str, List[str]]) -> Dict[str, int]:
    return {name: sum(1 for kw in kws if kw in text) for name, kws in rules.items()}


def _join(items: List[str]) -> str:
    return ', '.join(items) if items else 'Not specified'


class CampaignCalendarPlanner:
    def __init__(self, user_input: CampaignInput):
        self.raw = user_input
        self.text = self._normalize_input(user_input)
        self.lower = self.text.lower()
        self.window = self._detect_window()
        self.goal = self._detect_goal()
        self.channels = self._detect_channels()
        self.key_dates = self._select_key_dates()

    def _normalize_input(self, user_input: CampaignInput) -> str:
        if isinstance(user_input, dict):
            chunks: List[str] = []
            for key in ['window', 'goal', 'channels', 'seasonal', 'budget', 'product', 'notes']:
                value = user_input.get(key)
                if not value:
                    continue
                if isinstance(value, list):
                    value = ', '.join(str(v) for v in value)
                chunks.append(f'{key}: {value}')
            return ' | '.join(chunks)
        return str(user_input or '').strip()

    def _detect_window(self) -> str:
        scores = _score_rules(self.lower, WINDOW_RULES)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'Q2'

    def _detect_goal(self) -> str:
        scores = _score_rules(self.lower, GOAL_RULES)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'Conversion'

    def _detect_channels(self) -> List[str]:
        matched = [name for name, kws in CHANNEL_RULES.items() if any(kw in self.lower for kw in kws)]
        return matched or ['Shopify / DTC', 'Email / CRM']

    def _select_key_dates(self) -> List[str]:
        window_map = {
            'Q1': ["New Year's Day", "Lunar New Year", "Valentine's Day", "Q1 Sales Season"],
            'Q2': ["April Sale / Spring", "May Day", "Mother's Day (CN)", "618 Mid-Year Festival"],
            'Q3': ["Summer Sale", "Back to School", "Mid-Autumn Festival", "National Day (CN)"],
            'Q4': ["11.11 Singles Day", "Black Friday / Cyber Monday", "Holiday Season", "Christmas / Year End"],
        }
        return window_map.get(self.window, list(SEASONAL_DATES.keys()))

    def _channel_timing_matrix(self) -> List[str]:
        lines = ['| Channel | Focus | Timing | Campaign Type |']
        lines.append('|---|---|---|---|')
        for ch in self.channels:
            timing = {
                'Shopify / DTC': 'Always-on + campaign peaks',
                'Amazon': 'Deal events + search campaigns',
                'TikTok Shop': 'Live streams + content spikes',
                'Xiaohongshu': 'Seeding 2–4 weeks pre-launch',
                'Meta Ads': 'Traffic + retargeting around key dates',
                'Google Ads': 'Intent-based around shopping festivals',
                'Email / CRM': 'Segmentation sequences around campaigns',
                'JD': 'Platform deal events (618, 11.11)',
                'Taobao': 'Live streaming + deal events',
                'WeChat': ' MOM and festival content pushes',
            }.get(ch, 'Campaign-driven')
            ctype = {
                'Awareness': 'Brand + video',
                'Traffic': 'Content + CTR',
                'Conversion': 'Direct response + deals',
                'Revenue': 'Bundles + upsell',
                'Retention': 'Email sequences + VIP',
                'New Launch': 'Launch-day push + UGC',
            }.get(self.goal, 'Mixed')
            lines.append(f'| {ch} | Always-on + peaks | {timing} | {ctype} |')
        return lines

    def _campaign_cards(self) -> List[str]:
        dates = self.key_dates[:3]
        cards = []
        for i, date in enumerate(dates, 1):
            cards.append(f'{i}. **{date}** — Theme: TBD | Channels: {_join(self.channels)} | Goal: {self.goal}')
        if self.goal == 'New Launch':
            cards.insert(0, f'1. **Launch Day** — Theme: New SKU Introduction | Channels: {_join(self.channels[:3])} | Goal: {self.goal}')
        elif self.goal == 'Retention':
            cards.insert(0, f'1. **VIP Loyalty Push** — Theme: Thank You + Exclusive | Channels: Email / CRM, WeChat | Goal: Retention')
        return cards

    def _cadence_notes(self) -> List[str]:
        return [
            'Space major campaigns 4–6 weeks apart to avoid audience fatigue and preserve margin.',
            'Use always-on retargeting at 20–30% of budget to sustain baseline conversion between campaign peaks.',
            'Front-load awareness and seeding (TikTok, Xiaohongshu) 2–3 weeks before conversion push.',
            'Align paid search and Amazon deal enrollment with content momentum, not in isolation.',
        ]

    def _execution_notes(self) -> List[str]:
        return [
            'Verify official festival and sale dates on each platform — they shift between China and Western calendars.',
            'Lock channel budgets and creative briefs at least 3 weeks before the campaign window opens.',
            'Set up weekly campaign performance check-ins starting 1 week before launch.',
            'Prepare a campaign retrospective template before launch so post-mortem is not an afterthought.',
        ]

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Campaign Calendar Planner')
        lines.append('')
        lines.append(f'**Planning window:** {self.window}')
        lines.append(f'**Primary goal:** {self.goal}')
        lines.append(f'**Channels in scope:** {_join(self.channels)}')
        lines.append('**Method note:** This is a heuristic planning brief. No live calendar, ad platform, or ERP system was accessed.')
        lines.append('')
        lines.append('## Campaign Thesis')
        lines.append(f'- Plan the {self.window} campaign calendar around {_join(self.key_dates)} as anchor dates.')
        lines.append(f'- Lead with a {self.goal.lower()} focus and sequence channel activations to support that goal.')
        lines.append('- Treat awareness channels as predecessors to conversion channels; do not activate everything at once.')
        lines.append('')
        lines.append('## Seasonal Key Dates')
        for date, period in SEASONAL_DATES.items():
            marker = ' ← anchor' if date in self.key_dates else ''
            lines.append(f'- **{date}**: {period}{marker}')
        lines.append('')
        lines.append('## Channel-Timing Matrix')
        for row in self._channel_timing_matrix():
            lines.append(row)
        lines.append('')
        lines.append('## Campaign Cards')
        for card in self._campaign_cards():
            lines.append(f'- {card}')
        lines.append('')
        lines.append('## Cadence Recommendations')
        for note in self._cadence_notes():
            lines.append(f'- {note}')
        lines.append('')
        lines.append('## Execution Notes')
        for note in self._execution_notes():
            lines.append(f'- {note}')
        return '\n'.join(lines)


def handle(user_input: CampaignInput) -> str:
    return CampaignCalendarPlanner(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
