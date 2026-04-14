from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from context_guardian import (
    CheckpointStore,
    ContextGuardianConfig,
    ContextMonitor,
    LastAction,
    MemoryAssembler,
    SafetyGate,
    Summarizer,
    TaskArtifact,
    TaskState,
    TaskStep,
    create_default_task_state,
    load_task_state,
    should_trim_context,
)



def make_state() -> TaskState:
    return TaskState(
        task_id="task-1",
        session_id="session-1",
        goal="Preserve task continuity",
        status="running",
        current_phase="implementation",
        plan=[TaskStep(id="step-1", title="Inspect loop", status="done")],
        completed_steps=["Inspect loop"],
        open_issues=["Need final host integration point"],
        decisions=[{"timestamp": "2026-04-07T10:00:00Z", "decision": "Use files", "reason": "Restart safe"}],
        constraints=["Never continue blindly after context loss"],
        important_facts=["Planner exists"],
        artifacts=[TaskArtifact(path="/var/lib/context-guardian/tasks/task-1.state.json", kind="file", description="state")],
        last_action=LastAction(timestamp="2026-04-07T10:05:00Z", type="tool", summary="Checkpoint written", outcome="success"),
        next_action="Resume from the latest checkpoint",
        state_confidence=0.9,
    )


class ContextGuardianTests(unittest.TestCase):
    def make_temp_path(self) -> Path:
        return Path(tempfile.mkdtemp(prefix="cg-test-"))

    def test_checkpoint_creation(self) -> None:
        root = self.make_temp_path()
        config = ContextGuardianConfig(root_path=root)
        store = CheckpointStore(config)
        state = make_state()
        summary = Summarizer().summarize(state, [], config)
        checkpoint = store.write_checkpoint(state, summary, ["a.py"], ["assumption"], ["risk"], state.next_action)
        self.assertTrue(checkpoint.exists())
        self.assertTrue(store.task_state_path(state.task_id).exists())
        self.assertTrue(store.events_path.exists())

    def test_summary_generation_and_alias(self) -> None:
        root = self.make_temp_path()
        config = ContextGuardianConfig(root_path=root)
        store = CheckpointStore(config)
        state = make_state()
        summary = Summarizer().summarize(state, [], config)
        summary_path = store.write_summary(state.task_id, summary)
        self.assertTrue(summary_path.exists())
        self.assertTrue(store.latest_summary_path().exists())
        self.assertIn("# Context Guardian Summary", summary)

    def test_restart_recovery(self) -> None:
        root = self.make_temp_path()
        config = ContextGuardianConfig(root_path=root)
        store = CheckpointStore(config)
        state = make_state()
        store.write_checkpoint(state, "summary", [], [], [], state.next_action)
        recovered = load_task_state(store, state.task_id)
        self.assertIsNotNone(recovered)
        self.assertEqual(recovered.task_id, state.task_id)
        self.assertEqual(recovered.next_action, state.next_action)

    def test_schema_version_persisted(self) -> None:
        root = self.make_temp_path()
        config = ContextGuardianConfig(root_path=root)
        store = CheckpointStore(config)
        state = make_state()
        store.write_checkpoint(state, "summary", [], [], [], state.next_action)
        payload = json.loads(store.task_state_path(state.task_id).read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], "2.0")

    def test_critical_threshold_stop_behavior(self) -> None:
        root = self.make_temp_path()
        config = ContextGuardianConfig(root_path=root, max_history_chars=100)
        store = CheckpointStore(config)
        gate = SafetyGate(ContextMonitor(0.55, 0.70, 0.85, max_history_chars=100), store, Summarizer())
        state = make_state()
        state.state_confidence = 0.95
        result = gate.evaluate(["x" * 500], state, [], [])
        self.assertFalse(result["allow"])
        self.assertEqual(result["pressure"]["risk_level"], "critical")
        self.assertEqual(result["reason"], "critical context pressure")

    def test_host_pressure_override_wins(self) -> None:
        root = self.make_temp_path()
        config = ContextGuardianConfig(root_path=root, max_history_chars=10000)
        store = CheckpointStore(config)
        gate = SafetyGate(ContextMonitor(0.55, 0.70, 0.85, max_history_chars=10000), store, Summarizer())
        state = make_state()
        result = gate.evaluate(["tiny"], state, [], [], pressure_override=0.9)
        self.assertFalse(result["allow"])
        self.assertEqual(result["pressure"]["risk_level"], "critical")
        self.assertEqual(result["pressure"]["source"], "host")

    def test_trimming_policy(self) -> None:
        self.assertTrue(should_trim_context("warning"))
        self.assertTrue(should_trim_context("compress"))
        self.assertTrue(should_trim_context("critical"))
        self.assertFalse(should_trim_context("normal"))

    def test_memory_assembler(self) -> None:
        state = make_state()
        bundle = MemoryAssembler().build_bundle("sys", state, "summary", ["file.py"], "last action")
        self.assertIn("# Working Context Bundle", bundle)
        self.assertIn("## Current Phase", bundle)
        self.assertIn("file.py", bundle)

    def test_create_default_task_state(self) -> None:
        state = create_default_task_state("t", "s", "g")
        self.assertEqual(state.task_id, "t")
        self.assertEqual(state.session_id, "s")
        self.assertEqual(state.goal, "g")

    def test_task_state_round_trip(self) -> None:
        state = make_state()
        payload = state.to_dict()
        round_tripped = TaskState.from_dict(json.loads(json.dumps(payload)))
        self.assertEqual(round_tripped.task_id, state.task_id)
        self.assertEqual(round_tripped.goal, state.goal)


if __name__ == "__main__":
    unittest.main()
