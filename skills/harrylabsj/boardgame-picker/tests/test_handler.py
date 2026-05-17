#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_large_social_group_prefers_party():
    result = handle({
        'skill_name': 'boardgame-picker',
        'input': {
            'players': 7,
            'duration': 25,
            'experience': 'mostly new players',
            'mood': 'lively and social',
            'competition': 'low',
        },
    })['result']
    assert 'Party / Icebreaker' in result
    assert 'Quick Start' in result
    assert 'Avoid This Round' in result


def test_mixed_age_table_gets_safe_option():
    result = handle({
        'skill_name': 'boardgame-picker',
        'input': 'Players: 4\nTime: 40 minutes\nAge mix: parent and kids\nCompetition: low\nMood: teamwork and light pressure',
    })['result']
    assert 'Table Snapshot' in result
    assert 'Recommended Types' in result
    assert ('Cooperative / Team Challenge' in result) or ('Family / Gateway' in result)


def test_prompt_mode_returns_template():
    result = handle({'skill_name': 'boardgame-picker', 'mode': 'prompt'})['result']
    assert 'board game style' in result.lower()
    assert 'backup category' in result.lower()


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
