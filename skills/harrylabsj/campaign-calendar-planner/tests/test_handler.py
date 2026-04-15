#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import CampaignCalendarPlanner, handle


def test_window_detection_q1():
    planner = CampaignCalendarPlanner('Build a Q1 campaign calendar across Shopify and Amazon')
    assert planner.window == 'Q1'
    assert "New Year's Day" in planner.key_dates or "Lunar New Year" in planner.key_dates


def test_window_detection_q4():
    planner = CampaignCalendarPlanner('Plan our holiday campaign for Q4')
    assert planner.window == 'Q4'
    assert "11.11 Singles Day" in planner.key_dates or "Black Friday" in planner.key_dates


def test_goal_detection_conversion():
    planner = CampaignCalendarPlanner('Q2 campaign focused on direct sales and revenue')
    assert planner.goal == 'Conversion'


def test_channel_detection_amazon_tiktok():
    planner = CampaignCalendarPlanner('Plan our Amazon Prime Day and TikTok Shop promotion')
    assert 'Amazon' in planner.channels
    assert 'TikTok Shop' in planner.channels


def test_render_contains_sections():
    output = handle('Create a Q2 campaign calendar for our Shopify store targeting conversion')
    assert output.startswith('# Campaign Calendar Planner')
    assert '## Seasonal Key Dates' in output
    assert '## Channel-Timing Matrix' in output
    assert '## Campaign Cards' in output


def test_dict_input_supported():
    output = handle({
        'window': 'Q4',
        'goal': 'Revenue',
        'channels': ['Shopify', 'Amazon', 'TikTok Shop'],
        'notes': 'Focus on holiday season'
    })
    assert '# Campaign Calendar Planner' in output
    assert 'Q4' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
