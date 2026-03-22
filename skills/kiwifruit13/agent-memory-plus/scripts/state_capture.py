"""
Agent Memory System - 全局状态捕捉器

=== 依赖与环境声明 ===
- 运行环境：Python >=3.9
- 直接依赖:
  * pydantic: >=2.0.0
    - 用途：数据模型验证
  * typing-extensions: >=4.0.0
    - 用途：类型扩展支持
- 标准配置文件:
  ```text
  # requirements.txt
  pydantic>=2.0.0
  typing-extensions>=4.0.0
  ```
=== 声明结束 ===

安全提醒：定期运行 pip audit 进行安全审计
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from .types import (
    GlobalStateSnapshot,
    SituationAwareness,
    LongTermMemoryContainer,
    ReconstructedContext,
    TaskType,
)


class GlobalStateCapture:
    """
    全局状态捕捉器

    负责：
    - 捕捉全局上下文快照
    - 追踪多任务上下文
    - 识别任务切换
    - 维护状态快照历史
    """

    def __init__(
        self,
        user_id: str = "default_user",
        storage_path: str = "./state_snapshots",
    ) -> None:
        """
        初始化全局状态捕捉器

        Args:
            user_id: 用户ID
            storage_path: 状态快照存储路径
        """
        self.user_id: str = user_id
        self.storage_path: Path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # 当前状态
        self._current_snapshot: GlobalStateSnapshot | None = None

        # 状态历史
        self._snapshot_history: list[GlobalStateSnapshot] = []

        # 最大历史记录数
        self._max_history: int = 50

        # 任务切换检测配置
        self._switch_detection_window: int = 300  # 5分钟窗口（秒）

    def capture(
        self,
        situation: SituationAwareness,
        memory: LongTermMemoryContainer,
        context: ReconstructedContext,
        conversation_turn: dict[str, Any] | None = None,
    ) -> GlobalStateSnapshot:
        """
        捕捉当前全局状态

        Args:
            situation: 情境感知结果
            memory: 长期记忆容器
            context: 重构上下文
            conversation_turn: 当前对话轮次信息

        Returns:
            全局状态快照
        """
        # 生成快照ID
        snapshot_id: str = f"snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        # 提取关键信息
        current_task: str = self._extract_current_task(situation)
        task_phase: str = situation.current_task.task_phase
        user_intent: str = self._extract_user_intent(situation)
        active_memories: list[str] = self._extract_active_memories(memory)
        decision_context: dict[str, Any] = self._build_decision_context(context)
        emotion_state: str = situation.context_anchors.emotional
        mental_model: str = situation.user_current_state.mental_model

        # 创建快照
        snapshot: GlobalStateSnapshot = GlobalStateSnapshot(
            snapshot_id=snapshot_id,
            user_id=self.user_id,
            timestamp=datetime.now(),
            current_task=current_task,
            task_phase=task_phase,
            user_intent=user_intent,
            active_memories=active_memories,
            decision_context=decision_context,
            emotion_state=emotion_state,
            mental_model=mental_model,
            conversation_turn=conversation_turn,
        )

        # 检测任务切换
        if self._current_snapshot is not None:
            is_task_switch: bool = self._detect_task_switch(
                self._current_snapshot, snapshot
            )
            if is_task_switch:
                self._handle_task_switch(self._current_snapshot, snapshot)

        # 更新当前状态
        self._current_snapshot = snapshot

        # 添加到历史
        self._snapshot_history.append(snapshot)
        if len(self._snapshot_history) > self._max_history:
            self._snapshot_history = self._snapshot_history[-self._max_history :]

        # 持久化快照
        self._persist_snapshot(snapshot)

        return snapshot

    def _extract_current_task(self, situation: SituationAwareness) -> str:
        """
        提取当前任务描述

        Args:
            situation: 情境感知

        Returns:
            任务描述
        """
        task_type: TaskType = situation.current_task.task_type

        task_descriptions: dict[TaskType, str] = {
            TaskType.PROBLEM_SOLVING: "问题解决",
            TaskType.TECHNICAL_IMPLEMENTATION: "技术实现",
            TaskType.CODE_DEBUGGING: "代码调试",
            TaskType.PRECISE_CALCULATION: "精确计算",
            TaskType.CREATIVE_DESIGN: "创意设计",
            TaskType.BRAINSTORMING: "头脑风暴",
            TaskType.DATA_ANALYSIS: "数据分析",
            TaskType.KNOWLEDGE_QUERY: "知识查询",
        }

        return task_descriptions.get(task_type, "未知任务")

    def _extract_user_intent(self, situation: SituationAwareness) -> str:
        """
        提取用户意图

        Args:
            situation: 情境感知

        Returns:
            用户意图描述
        """
        requirements: list[str] = situation.current_task.implicit_requirements
        if requirements:
            return " | ".join(requirements[:3])
        return situation.current_task.task_type.value

    def _extract_active_memories(
        self, memory: LongTermMemoryContainer
    ) -> list[str]:
        """
        提取活跃记忆ID列表

        Args:
            memory: 长期记忆容器

        Returns:
            活跃记忆ID列表
        """
        active: list[str] = []

        if memory.user_profile:
            active.append(memory.user_profile.memory_id)

        if memory.procedural:
            active.append(memory.procedural.memory_id)

        if memory.narrative:
            active.append(memory.narrative.memory_id)

        if memory.semantic:
            active.append(memory.semantic.memory_id)

        if memory.emotional:
            active.append(memory.emotional.memory_id)

        return active

    def _build_decision_context(
        self, context: ReconstructedContext
    ) -> dict[str, Any]:
        """
        构建决策上下文

        Args:
            context: 重构上下文

        Returns:
            决策上下文字典
        """
        return {
            "task_context": context.task_context.model_dump(mode="json"),
            "user_state": context.user_state.model_dump(mode="json"),
            "experiences": context.activated_experiences.model_dump(mode="json"),
            "knowledge": context.knowledge_context.model_dump(mode="json"),
            "emotional": context.emotional_context.model_dump(mode="json"),
            "narrative": context.narrative_anchor.model_dump(mode="json"),
        }

    def _detect_task_switch(
        self,
        previous: GlobalStateSnapshot,
        current: GlobalStateSnapshot,
    ) -> bool:
        """
        检测任务切换

        Args:
            previous: 上一个快照
            current: 当前快照

        Returns:
            是否发生任务切换
        """
        # 任务类型变化
        if previous.current_task != current.current_task:
            return True

        # 时间间隔超过窗口
        time_diff: float = (
            current.timestamp - previous.timestamp
        ).total_seconds()
        if time_diff > self._switch_detection_window:
            return True

        # 用户意图显著变化
        if previous.user_intent != current.user_intent:
            prev_keywords: set[str] = set(previous.user_intent.split())
            curr_keywords: set[str] = set(current.user_intent.split())
            overlap: float = len(prev_keywords & curr_keywords) / max(
                len(prev_keywords | curr_keywords), 1
            )
            if overlap < 0.3:
                return True

        return False

    def _handle_task_switch(
        self,
        previous: GlobalStateSnapshot,
        current: GlobalStateSnapshot,
    ) -> None:
        """
        处理任务切换

        Args:
            previous: 上一个快照
            current: 当前快照
        """
        # 标记上一个任务的状态
        previous.metadata["task_ended"] = True
        previous.metadata["end_reason"] = "task_switch"

        # 记录任务切换
        switch_record: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "from_task": previous.current_task,
            "to_task": current.current_task,
            "time_in_previous": (
                current.timestamp - previous.timestamp
            ).total_seconds(),
        }

        current.metadata["task_switch_from"] = switch_record

    def _persist_snapshot(self, snapshot: GlobalStateSnapshot) -> None:
        """
        持久化快照

        Args:
            snapshot: 状态快照
        """
        snapshot_file: Path = (
            self.storage_path
            / f"{self.user_id}_{snapshot.snapshot_id}.json"
        )

        with open(snapshot_file, "w", encoding="utf-8") as f:
            json.dump(snapshot.model_dump(mode="json"), f, ensure_ascii=False, indent=2)

    def get_current_state(self) -> GlobalStateSnapshot | None:
        """
        获取当前状态快照

        Returns:
            当前状态快照，如果不存在返回 None
        """
        return self._current_snapshot

    def get_state_history(
        self, limit: int = 10
    ) -> list[GlobalStateSnapshot]:
        """
        获取状态历史

        Args:
            limit: 返回的最大数量

        Returns:
            状态快照历史列表
        """
        return self._snapshot_history[-limit:]

    def get_task_history(self) -> list[dict[str, Any]]:
        """
        获取任务历史

        Returns:
            任务历史记录列表
        """
        tasks: list[dict[str, Any]] = []

        for snapshot in self._snapshot_history:
            if snapshot.metadata.get("task_ended"):
                tasks.append(
                    {
                        "task": snapshot.current_task,
                        "phase": snapshot.task_phase,
                        "start_time": snapshot.timestamp.isoformat(),
                        "end_reason": snapshot.metadata.get("end_reason"),
                        "memories_used": len(snapshot.active_memories),
                    }
                )

        return tasks

    def restore_state(
        self, snapshot_id: str
    ) -> GlobalStateSnapshot | None:
        """
        恢复指定快照状态

        Args:
            snapshot_id: 快照ID

        Returns:
            恢复的状态快照，如果不存在返回 None
        """
        snapshot_file: Path = (
            self.storage_path
            / f"{self.user_id}_{snapshot_id}.json"
        )

        if not snapshot_file.exists():
            # 从历史中查找
            for snapshot in self._snapshot_history:
                if snapshot.snapshot_id == snapshot_id:
                    return snapshot
            return None

        try:
            with open(snapshot_file, "r", encoding="utf-8") as f:
                data: dict[str, Any] = json.load(f)
                return GlobalStateSnapshot.model_validate(data)
        except (json.JSONDecodeError, ValueError):
            return None

    def compare_states(
        self,
        snapshot_id1: str,
        snapshot_id2: str,
    ) -> dict[str, Any]:
        """
        比较两个状态快照

        Args:
            snapshot_id1: 第一个快照ID
            snapshot_id2: 第二个快照ID

        Returns:
            比较结果
        """
        snap1: GlobalStateSnapshot | None = self.restore_state(snapshot_id1)
        snap2: GlobalStateSnapshot | None = self.restore_state(snapshot_id2)

        if snap1 is None or snap2 is None:
            return {"error": "一个或多个快照不存在"}

        comparison: dict[str, Any] = {
            "snapshot1": snapshot_id1,
            "snapshot2": snapshot_id2,
            "task_changed": snap1.current_task != snap2.current_task,
            "intent_changed": snap1.user_intent != snap2.user_intent,
            "emotion_changed": snap1.emotion_state != snap2.emotion_state,
            "time_difference_seconds": (
                snap2.timestamp - snap1.timestamp
            ).total_seconds(),
            "memory_overlap": len(
                set(snap1.active_memories) & set(snap2.active_memories)
            ),
            "memory_difference": len(
                set(snap1.active_memories) ^ set(snap2.active_memories)
            ),
        }

        return comparison

    def get_task_switch_events(self) -> list[dict[str, Any]]:
        """
        获取任务切换事件

        Returns:
            任务切换事件列表
        """
        events: list[dict[str, Any]] = []

        for snapshot in self._snapshot_history:
            if "task_switch_from" in snapshot.metadata:
                events.append(snapshot.metadata["task_switch_from"])

        return events

    def cleanup_old_snapshots(
        self,
        max_age_days: int = 30,
    ) -> int:
        """
        清理过期快照

        Args:
            max_age_days: 最大保留天数

        Returns:
            清理的快照数量
        """
        cutoff: datetime = datetime.now()
        cutoff = cutoff.replace(
            day=cutoff.day - max_age_days
        )

        cleaned: int = 0

        # 清理文件
        for snapshot_file in self.storage_path.glob(f"{self.user_id}_*.json"):
            try:
                with open(snapshot_file, "r", encoding="utf-8") as f:
                    data: dict[str, Any] = json.load(f)
                    snapshot_time: datetime = datetime.fromisoformat(
                        data.get("timestamp", "")
                    )
                    if snapshot_time < cutoff:
                        snapshot_file.unlink()
                        cleaned += 1
            except (json.JSONDecodeError, ValueError, KeyError):
                pass

        # 清理内存历史
        original_len: int = len(self._snapshot_history)
        self._snapshot_history = [
            s for s in self._snapshot_history if s.timestamp >= cutoff
        ]
        cleaned += original_len - len(self._snapshot_history)

        return cleaned


# ============================================================================
# 导出
# ============================================================================

__all__ = ["GlobalStateCapture"]
