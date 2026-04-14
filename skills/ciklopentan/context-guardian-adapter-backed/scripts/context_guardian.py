"""Context Guardian reference runtime.

Deterministic reference implementation for adapter-backed durable task continuity.
This file is the reference behavior for storage, summaries, checkpoints, and bundles.
It is framework-agnostic and does not patch OpenClaw core.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol
import json
import math
import os
import tempfile


SCHEMA_VERSION = "2.0"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as handle:
        handle.write(content)
        temp_name = handle.name
    os.replace(temp_name, path)


@dataclass
class ContextGuardianConfig:
    root_path: Path
    warning_threshold: float = 0.55
    compress_threshold: float = 0.70
    critical_threshold: float = 0.85
    max_history_chars: int = 12000
    dry_run: bool = False
    debug: bool = False

    def tasks_dir(self) -> Path:
        return Path(self.root_path) / "tasks"

    def summaries_dir(self) -> Path:
        return Path(self.root_path) / "summaries"

    def snapshots_dir(self) -> Path:
        return Path(self.root_path) / "snapshots"

    def logs_dir(self) -> Path:
        return Path(self.root_path) / "logs"

    def tests_dir(self) -> Path:
        return Path(self.root_path) / "tests"

    def config_path(self) -> Path:
        return Path(self.root_path) / "config.yaml"


@dataclass
class TaskArtifact:
    path: str
    kind: str
    description: str


@dataclass
class TaskStep:
    id: str
    title: str
    status: str = "pending"
    notes: str = ""


@dataclass
class LastAction:
    timestamp: str
    type: str
    summary: str
    outcome: str


@dataclass
class TaskState:
    task_id: str
    session_id: str
    goal: str
    status: str = "idle"
    current_phase: str = "initial"
    plan: list[TaskStep] = field(default_factory=list)
    completed_steps: list[str] = field(default_factory=list)
    open_issues: list[str] = field(default_factory=list)
    decisions: list[dict[str, str]] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    important_facts: list[str] = field(default_factory=list)
    artifacts: list[TaskArtifact] = field(default_factory=list)
    last_action: LastAction | None = None
    next_action: str = ""
    recovery_instructions: list[str] = field(default_factory=lambda: [
        "Read the latest durable task state.",
        "Read the latest durable summary.",
        "Verify files before editing.",
        "Resume from next_action only if constraints still hold.",
    ])
    state_confidence: float = 0.0
    updated_at: str = field(default_factory=iso_now)
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["artifacts"] = [asdict(artifact) for artifact in self.artifacts]
        payload["plan"] = [asdict(step) for step in self.plan]
        payload["last_action"] = asdict(self.last_action) if self.last_action else None
        payload["schema_version"] = self.schema_version or SCHEMA_VERSION
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TaskState":
        plan = [TaskStep(**step) for step in payload.get("plan", [])]
        artifacts = [TaskArtifact(**artifact) for artifact in payload.get("artifacts", [])]
        last_action_payload = payload.get("last_action")
        last_action = LastAction(**last_action_payload) if last_action_payload else None
        return cls(
            task_id=payload["task_id"],
            session_id=payload["session_id"],
            goal=payload["goal"],
            status=payload.get("status", "idle"),
            current_phase=payload.get("current_phase", "initial"),
            plan=plan,
            completed_steps=list(payload.get("completed_steps", [])),
            open_issues=list(payload.get("open_issues", [])),
            decisions=list(payload.get("decisions", [])),
            constraints=list(payload.get("constraints", [])),
            important_facts=list(payload.get("important_facts", [])),
            artifacts=artifacts,
            last_action=last_action,
            next_action=payload.get("next_action", ""),
            recovery_instructions=list(payload.get("recovery_instructions", [])),
            state_confidence=float(payload.get("state_confidence", 0.0)),
            updated_at=payload.get("updated_at", iso_now()),
            schema_version=payload.get("schema_version", SCHEMA_VERSION),
        )


class SummaryBackend(Protocol):
    def summarize(self, task_state: TaskState, stale_history: list[str], config: ContextGuardianConfig) -> str: ...


class ContextMonitor:
    """Reference/demo pressure estimator.

    Production adapters must provide explicit numeric pressure.
    This estimator exists only for reference environments and tests.
    """

    def __init__(self, warning_threshold: float, compress_threshold: float, critical_threshold: float, max_history_chars: int = 12000):
        self.warning_threshold = warning_threshold
        self.compress_threshold = compress_threshold
        self.critical_threshold = critical_threshold
        self.max_history_chars = max_history_chars

    def estimate_usage(self, messages: list[str], durable_state_chars: int = 0) -> dict[str, Any]:
        char_count = sum(len(message) for message in messages) + durable_state_chars
        estimated_tokens = max(1, math.ceil(char_count / 4))
        current_usage_ratio = min(1.0, char_count / max(1, self.max_history_chars))
        if current_usage_ratio >= self.critical_threshold:
            risk_level = "critical"
        elif current_usage_ratio >= self.compress_threshold:
            risk_level = "compress"
        elif current_usage_ratio >= self.warning_threshold:
            risk_level = "warning"
        else:
            risk_level = "normal"
        return {
            "current_usage_ratio": current_usage_ratio,
            "estimated_tokens": estimated_tokens,
            "risk_level": risk_level,
            "char_count": char_count,
            "source": "reference-estimator",
        }


class CheckpointStore:
    def __init__(self, config: ContextGuardianConfig):
        self.config = config
        self.events_path = self.config.logs_dir() / "events.ndjson"

    def ensure_dirs(self) -> None:
        if self.config.dry_run:
            return
        for path in (
            self.config.root_path,
            self.config.tasks_dir(),
            self.config.summaries_dir(),
            self.config.snapshots_dir(),
            self.config.logs_dir(),
            self.config.tests_dir(),
        ):
            path.mkdir(parents=True, exist_ok=True)

    def task_state_path(self, task_id: str) -> Path:
        return self.config.tasks_dir() / f"{task_id}.state.json"

    def summary_path(self, task_id: str) -> Path:
        return self.config.summaries_dir() / f"{task_id}.summary.md"

    def latest_summary_path(self) -> Path:
        return self.config.summaries_dir() / "latest-summary.md"

    def write_checkpoint(self, task_state: TaskState, summary: str, exact_files_touched: list[str], assumptions: list[str], risks: list[str], next_action: str) -> Path:
        self.ensure_dirs()
        checkpoint = {
            "timestamp": iso_now(),
            "schema_version": task_state.schema_version,
            "task_id": task_state.task_id,
            "session_id": task_state.session_id,
            "goal": task_state.goal,
            "status": task_state.status,
            "current_phase": task_state.current_phase,
            "done": list(task_state.completed_steps),
            "remaining": [step.title for step in task_state.plan if step.status not in {"done", "skipped"}],
            "files_touched": exact_files_touched,
            "assumptions": assumptions,
            "risks": risks,
            "next_action": next_action or task_state.next_action,
            "state_confidence": task_state.state_confidence,
            "summary": summary,
        }
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        checkpoint_path = self.config.snapshots_dir() / f"{task_state.task_id}-{timestamp}.json"
        if not self.config.dry_run:
            atomic_write_text(checkpoint_path, json.dumps(checkpoint, indent=2, ensure_ascii=False) + "\n")
            atomic_write_text(self.task_state_path(task_state.task_id), json.dumps(task_state.to_dict(), indent=2, ensure_ascii=False) + "\n")
        self.append_event(task_state.task_id, "checkpoint", f"checkpoint written: {timestamp}", exact_files_touched, True, task_state.state_confidence)
        return checkpoint_path

    def append_event(self, task_id: str, event_type: str, summary: str, files_changed: list[str], success: bool, confidence: float) -> None:
        self.ensure_dirs()
        record = {
            "timestamp": iso_now(),
            "task_id": task_id,
            "event_type": event_type,
            "summary": summary,
            "files_changed": files_changed,
            "success": success,
            "confidence": confidence,
        }
        if self.config.dry_run:
            return
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def latest_task_state(self, task_id: str) -> TaskState | None:
        path = self.task_state_path(task_id)
        if not path.exists():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        return TaskState.from_dict(payload)

    def latest_summary(self, task_id: str) -> str | None:
        specific = self.summary_path(task_id)
        if specific.exists():
            return specific.read_text(encoding="utf-8")
        alias = self.latest_summary_path()
        if alias.exists():
            return alias.read_text(encoding="utf-8")
        return None

    def write_summary(self, task_id: str, summary: str) -> Path:
        self.ensure_dirs()
        summary_path = self.summary_path(task_id)
        alias_path = self.latest_summary_path()
        if not self.config.dry_run:
            atomic_write_text(summary_path, summary)
            atomic_write_text(alias_path, summary)
        return summary_path


class Summarizer:
    def __init__(self, backend: SummaryBackend | None = None):
        self.backend = backend

    def summarize(self, task_state: TaskState, stale_history: list[str], config: ContextGuardianConfig) -> str:
        if self.backend is not None:
            return self.backend.summarize(task_state, stale_history, config)
        completed = "\n".join(f"- {item}" for item in task_state.completed_steps) or "- none"
        decisions = "\n".join(
            f"- Decision: {item.get('decision', '')}\n  Reason: {item.get('reason', '')}" for item in task_state.decisions
        ) or "- none"
        artifacts = "\n".join(
            f"- path: {artifact.path}\n  role: {artifact.kind}"
            for artifact in task_state.artifacts
        ) or "- none"
        issues = "\n".join(f"- {issue}" for issue in task_state.open_issues) or "- none"
        return (
            "# Context Guardian Summary\n\n"
            f"## Goal\n{task_state.goal}\n\n"
            f"## Current Phase\n{task_state.current_phase}\n\n"
            f"## Completed\n{completed}\n\n"
            f"## Decisions\n{decisions}\n\n"
            f"## Constraints\n" + ("\n".join(f"- {item}" for item in task_state.constraints) or "- none") + "\n\n"
            f"## Artifacts\n{artifacts}\n\n"
            f"## Open Issues\n{issues}\n\n"
            f"## Last Successful Action\n{task_state.last_action.summary if task_state.last_action else 'none'}\n\n"
            f"## Next Action\n{task_state.next_action or 'none'}\n\n"
            "## Recovery Notes\n"
            "- Resume from the latest durable state.\n"
            "- Re-check important files before editing.\n"
            "- Do not redo completed work without validation.\n"
            "- Do not overwrite durable state without a fresh checkpoint.\n"
        )


class MemoryAssembler:
    def build_bundle(self, system_instructions: str, task_state: TaskState, summary: str | None, relevant_files: list[str], last_successful_action: str) -> str:
        bundle_parts = [
            "# Working Context Bundle",
            "## System Instructions",
            system_instructions.strip(),
            "## Current User Task",
            task_state.goal,
            "## Current Phase",
            task_state.current_phase,
            "## Active Constraints",
            "\n".join(f"- {item}" for item in task_state.constraints) or "- none",
            "## Current Plan",
            "\n".join(f"- {step.id}: {step.title} [{step.status}]" for step in task_state.plan) or "- none",
            "## Last Successful Action",
            last_successful_action or (task_state.last_action.summary if task_state.last_action else "none"),
            "## Next Action",
            task_state.next_action or "none",
            "## Relevant Files",
            "\n".join(f"- {path}" for path in relevant_files) or "- none",
        ]
        if summary:
            bundle_parts.extend(["## Latest Structured Summary", summary.strip()])
        return "\n\n".join(bundle_parts)


class SafetyGate:
    def __init__(self, monitor: ContextMonitor, store: CheckpointStore, summarizer: Summarizer):
        self.monitor = monitor
        self.store = store
        self.summarizer = summarizer

    def evaluate(self, messages: list[str], task_state: TaskState, stale_history: list[str], exact_files_touched: list[str], pressure_override: float | None = None) -> dict[str, Any]:
        if pressure_override is None:
            pressure = self.monitor.estimate_usage(messages, durable_state_chars=len(json.dumps(task_state.to_dict(), ensure_ascii=False)))
        else:
            current_usage_ratio = max(0.0, min(1.0, float(pressure_override)))
            if current_usage_ratio >= self.monitor.critical_threshold:
                risk_level = "critical"
            elif current_usage_ratio >= self.monitor.compress_threshold:
                risk_level = "compress"
            elif current_usage_ratio >= self.monitor.warning_threshold:
                risk_level = "warning"
            else:
                risk_level = "normal"
            pressure = {
                "current_usage_ratio": current_usage_ratio,
                "estimated_tokens": None,
                "risk_level": risk_level,
                "char_count": None,
                "source": "host",
            }
        should_refresh_summary = pressure["risk_level"] in {"compress", "critical", "warning"}
        summary = None
        if should_refresh_summary:
            summary = self.summarizer.summarize(task_state, stale_history, self.store.config)
            self.store.write_summary(task_state.task_id, summary)
        if pressure["risk_level"] == "critical":
            self.store.write_checkpoint(
                task_state=task_state,
                summary=summary or "",
                exact_files_touched=exact_files_touched,
                assumptions=task_state.constraints,
                risks=task_state.open_issues,
                next_action=task_state.next_action,
            )
            return {
                "allow": False,
                "reason": "critical context pressure",
                "pressure": pressure,
                "summary": summary,
            }
        checkpoint_path = self.store.write_checkpoint(
            task_state=task_state,
            summary=summary or "",
            exact_files_touched=exact_files_touched,
            assumptions=task_state.constraints,
            risks=task_state.open_issues,
            next_action=task_state.next_action,
        )
        return {
            "allow": True,
            "reason": "state is sufficiently recoverable",
            "pressure": pressure,
            "summary": summary,
            "checkpoint_path": str(checkpoint_path),
        }


def load_task_state(store: CheckpointStore, task_id: str, fallback: TaskState | None = None) -> TaskState | None:
    state = store.latest_task_state(task_id)
    if state is not None:
        return state
    return fallback


def should_trim_context(risk_level: str) -> bool:
    return risk_level in {"warning", "compress", "critical"}


def create_default_task_state(task_id: str, session_id: str, goal: str) -> TaskState:
    return TaskState(task_id=task_id, session_id=session_id, goal=goal)
