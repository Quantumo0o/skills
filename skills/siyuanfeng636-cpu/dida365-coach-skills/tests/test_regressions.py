"""回归测试：覆盖已修复的滴答字段语义问题。"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.dida_semantics import is_current_task_completed, priority_to_numeric
from tools.task_parser import extract_priority, parse_timebox_input


class PrioritySemanticsTest(unittest.TestCase):
    def test_priority_symbols_follow_dida_semantics(self) -> None:
        self.assertEqual(extract_priority("!1"), "low")
        self.assertEqual(extract_priority("!2"), "medium")
        self.assertEqual(extract_priority("!3"), "high")
        self.assertEqual(priority_to_numeric("low"), 1)
        self.assertEqual(priority_to_numeric("medium"), 3)
        self.assertEqual(priority_to_numeric("high"), 5)


class TimeboxParsingTest(unittest.TestCase):
    def test_parse_timebox_with_reminder_priority_and_list(self) -> None:
        parsed = parse_timebox_input(
            "去江南沟通，今天下午3点，提前30分钟提醒，工作行动清单，中优先级"
        )
        self.assertEqual(parsed["task_description"], "去江南沟通")
        self.assertEqual(parsed["deadline"], "2026-03-17T15:00")
        self.assertEqual(parsed["priority"], "medium")
        self.assertEqual(parsed["reminder_offset_minutes"], 30)
        self.assertEqual(parsed["list_name"], "工作行动清单")


class CompletionStatusTest(unittest.TestCase):
    def test_completed_time_does_not_override_pending_status(self) -> None:
        task = {
            "title": "布置配网微应用系统建设工作",
            "status": "pending",
            "completedTime": "2026-02-04T09:00:00",
        }
        self.assertFalse(is_current_task_completed(task))


if __name__ == "__main__":
    unittest.main()
