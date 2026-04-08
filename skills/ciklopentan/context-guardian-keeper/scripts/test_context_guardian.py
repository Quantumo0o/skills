from __future__ import annotations

import json
import sys
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
        artifacts=[TaskArtifact(path=".context_guardian/task_state.json", kind="file", description="state")],
        last_action=LastAction(timestamp="2026-04-07T10:05:00Z", type="tool", summary="Checkpoint written", outcome="success"),
        next_action="Resume from the latest checkpoint",
        state_confidence=0.9,
    )


class ContextGuardianTests(unittest.TestCase):
    def test_checkpoint_creation(self) -> None:
        tmp_path = Path(self.id().replace(".", "_"))
        tmp_path.mkdir(exist_ok=True)
        config = ContextGuardianConfig(root_path=tmp_path, context_path=tmp_path)
        store = CheckpointStore(config)
        state = make_state()
        summary = Summarizer().summarize(state, [], config)
        checkpoint = store.write_checkpoint(state, summary, ["a.py"], ["assumption"], ["risk"], state.next_action)
        self.assertTrue(checkpoint.exists())
        self.assertTrue(store.task_state_json.exists())
        self.assertTrue(store.task_state_md.exists())
        self.assertTrue(store.events_path.exists())

    def test_summary_generation(self) -> None:
        config = ContextGuardianConfig(root_path=Path("."), context_path=Path("."))
        summary = Summarizer().summarize(make_state(), [], config)
        self.assertIn("# Context Guardian Summary", summary)
        self.assertIn("## Goal", summary)
        self.assertIn("## Next Action", summary)

    def test_restart_recovery(self) -> None:
        tmp_path = Path(self.id().replace(".", "_"))
        tmp_path.mkdir(exist_ok=True)
        config = ContextGuardianConfig(root_path=tmp_path, context_path=tmp_path)
        store = CheckpointStore(config)
        state = make_state()
        store.write_checkpoint(state, "summary", [], [], [], state.next_action)
        recovered = load_task_state(store)
        self.assertIsNotNone(recovered)
        self.assertEqual(recovered.task_id, state.task_id)
        self.assertEqual(recovered.next_action, state.next_action)

    def test_critical_threshold_stop_behavior(self) -> None:
        tmp_path = Path(self.id().replace(".", "_"))
        tmp_path.mkdir(exist_ok=True)
        config = ContextGuardianConfig(root_path=tmp_path, context_path=tmp_path, max_history_chars=100)
        store = CheckpointStore(config)
        gate = SafetyGate(ContextMonitor(0.55, 0.70, 0.85, max_history_chars=100), store, Summarizer())
        state = make_state()
        state.state_confidence = 0.5
        result = gate.evaluate(["x" * 500], state, [], [])
        self.assertFalse(result["allow"])
        self.assertEqual(result["pressure"]["risk_level"], "critical")

    def test_trimming_policy(self) -> None:
        self.assertTrue(should_trim_context("warning"))
        self.assertTrue(should_trim_context("compress"))
        self.assertTrue(should_trim_context("critical"))
        self.assertFalse(should_trim_context("normal"))

    def test_memory_assembler(self) -> None:
        state = make_state()
        bundle = MemoryAssembler().build_bundle("sys", state, "summary", ["file.py"], "last action")
        self.assertIn("# Working Context Bundle", bundle)
        self.assertIn("## Latest Durable State", bundle)
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
