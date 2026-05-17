#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import GratitudeJournalist, handle


def test_entry_count_from_input():
    journal = GratitudeJournalist('My friend checked in on me; the quiet walk after dinner')
    assert len(journal.entries) >= 2


def test_people_lens_detection():
    journal = GratitudeJournalist('My friend checked in on me; a sunny window in the afternoon')
    assert journal.entries[0]['lens'] == 'people'


def test_output_structure():
    output = handle('My son laughed with me; I noticed a calm cup of tea after dinner')
    assert output.startswith('# Gratitude Entry')
    assert output.count('- Why it mattered:') >= 2
    assert '## Pattern to Notice' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
