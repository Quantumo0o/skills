"""
Agent Memory System - 长期记忆模块

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
    LongTermMemoryContainer,
    UserProfileMemory,
    UserProfileData,
    ProceduralMemory,
    ProceduralMemoryData,
    NarrativeMemory,
    NarrativeMemoryData,
    SemanticMemory,
    SemanticMemoryData,
    EmotionalMemory,
    EmotionalMemoryData,
    HeatLevel,
    MemoryType,
    ToolUsageRecord,
    ToolOptimalContext,
    NeuroticismTendency,
    GrowthMilestone,
    EmotionState,
    ConceptDefinition,
)
from .heat_manager import HeatManager


class LongTermMemoryManager:
    """
    长期记忆管理器

    负责持久化的经验与知识仓库，包括：
    - 用户画像管理
    - 程序性记忆管理（含工具使用模式）
    - 叙事记忆管理
    - 语义记忆管理
    - 情感记忆管理
    - 冷热度分层管理
    """

    def __init__(
        self,
        user_id: str = "default_user",
        storage_path: str = "./memory_storage",
    ) -> None:
        """
        初始化长期记忆管理器

        Args:
            user_id: 用户ID
            storage_path: 存储路径
        """
        self.user_id: str = user_id
        self.storage_path: Path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self._container: LongTermMemoryContainer = LongTermMemoryContainer(
            user_id=user_id
        )
        self._heat_manager: HeatManager = HeatManager()

        # 尝试加载已有记忆
        self._load_from_storage()

    def _load_from_storage(self) -> None:
        """
        从存储加载记忆（内部方法）
        """
        storage_file: Path = self.storage_path / f"{self.user_id}_memory.json"

        if storage_file.exists():
            try:
                with open(storage_file, "r", encoding="utf-8") as f:
                    data: dict[str, Any] = json.load(f)
                    self._container = LongTermMemoryContainer.model_validate(data)
            except (json.JSONDecodeError, ValueError):
                # 加载失败，使用空容器
                pass

    def _save_to_storage(self) -> None:
        """
        保存记忆到存储（内部方法）
        """
        storage_file: Path = self.storage_path / f"{self.user_id}_memory.json"
        self._container.last_updated = datetime.now()

        with open(storage_file, "w", encoding="utf-8") as f:
            json.dump(self._container.model_dump(mode="json"), f, ensure_ascii=False, indent=2)

    def get_user_profile(self) -> UserProfileData | None:
        """
        获取用户画像

        Returns:
            用户画像数据，如果不存在返回 None
        """
        if self._container.user_profile:
            return self._container.user_profile.data
        return None

    def update_user_profile(self, profile_data: dict[str, Any]) -> str:
        """
        更新用户画像

        Args:
            profile_data: 用户画像数据

        Returns:
            记忆ID
        """
        if self._container.user_profile is None:
            # 创建新画像
            memory_id: str = f"profile_{uuid.uuid4().hex[:12]}"
            self._container.user_profile = UserProfileMemory(
                memory_id=memory_id,
                user_id=self.user_id,
                data=UserProfileData.model_validate(profile_data),
            )
        else:
            # 更新现有画像
            current_data: UserProfileData = self._container.user_profile.data

            # 合并身份标签
            if "identity" in profile_data:
                for identity in profile_data["identity"]:
                    if identity not in current_data.identity:
                        current_data.identity.append(identity)

            # 更新技术背景
            if "technical_background" in profile_data:
                tb: dict[str, Any] = profile_data["technical_background"]
                if "domains" in tb:
                    for domain in tb["domains"]:
                        if domain not in current_data.technical_background.domains:
                            current_data.technical_background.domains.append(domain)
                if "expertise_level" in tb:
                    current_data.technical_background.expertise_level = tb["expertise_level"]

            # 更新沟通风格
            if "communication_style" in profile_data:
                cs: dict[str, Any] = profile_data["communication_style"]
                if "style" in cs:
                    current_data.communication_style.style = cs["style"]
                if "preference" in cs:
                    current_data.communication_style.preference = cs["preference"]

            # 更新决策模式
            if "decision_pattern" in profile_data:
                dp: dict[str, Any] = profile_data["decision_pattern"]
                if "type" in dp:
                    current_data.decision_pattern.type = dp["type"]
                if "focus" in dp:
                    current_data.decision_pattern.focus = dp["focus"]

            current_data.version += 1

        self._save_to_storage()
        return self._container.user_profile.memory_id

    def get_procedural_memory(self) -> ProceduralMemoryData | None:
        """
        获取程序性记忆

        Returns:
            程序性记忆数据
        """
        if self._container.procedural:
            return self._container.procedural.data
        return None

    def update_procedural_memory(self, procedural_data: dict[str, Any]) -> str:
        """
        更新程序性记忆

        Args:
            procedural_data: 程序性记忆数据

        Returns:
            记忆ID
        """
        if self._container.procedural is None:
            memory_id: str = f"procedural_{uuid.uuid4().hex[:12]}"
            self._container.procedural = ProceduralMemory(
                memory_id=memory_id,
                user_id=self.user_id,
                data=ProceduralMemoryData.model_validate(procedural_data),
            )
        else:
            current_data: ProceduralMemoryData = self._container.procedural.data

            # 合并决策模式
            if "decision_patterns" in procedural_data:
                for pattern in procedural_data["decision_patterns"]:
                    current_data.decision_patterns.append(
                        {
                            "pattern_id": pattern.get("pattern_id", f"dp_{uuid.uuid4().hex[:8]}"),
                            "trigger_condition": pattern.get("trigger_condition", ""),
                            "workflow": pattern.get("workflow", []),
                            "confidence": pattern.get("confidence", 0.5),
                            "usage_count": pattern.get("usage_count", 1),
                            "success_rate": pattern.get("success_rate", 0.5),
                        }
                    )

            # 更新操作偏好
            if "operation_preferences" in procedural_data:
                current_data.operation_preferences.update(
                    procedural_data["operation_preferences"]
                )

        self._save_to_storage()
        return self._container.procedural.memory_id

    def update_tool_usage(
        self,
        tool_name: str,
        task_type: str,
        outcome: str,
        user_feedback: float | None = None,
        effectiveness_score: float = 0.5,
    ) -> str:
        """
        更新工具使用记忆

        Args:
            tool_name: 工具名称
            task_type: 任务类型
            outcome: 结果（success/failure）
            user_feedback: 用户反馈评分
            effectiveness_score: 有效度分数

        Returns:
            记录ID
        """
        if self._container.procedural is None:
            memory_id: str = f"procedural_{uuid.uuid4().hex[:12]}"
            self._container.procedural = ProceduralMemory(
                memory_id=memory_id,
                user_id=self.user_id,
                data=ProceduralMemoryData(),
            )

        record: ToolUsageRecord = ToolUsageRecord(
            record_id=f"tool_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now(),
            task_type=task_type,
            tool_name=tool_name,
            effectiveness_score=effectiveness_score,
            outcome=outcome,
            user_feedback=user_feedback,
        )

        self._container.procedural.data.tool_effectiveness_records.append(record)
        self._save_to_storage()

        return record.record_id

    def get_tool_recommendation(
        self, task_type: str, constraints: list[str] | None = None
    ) -> dict[str, Any]:
        """
        获取工具推荐

        Args:
            task_type: 任务类型
            constraints: 约束条件

        Returns:
            推荐结果
        """
        if self._container.procedural is None:
            return {
                "tool": "代码解释器",
                "confidence": 0.5,
                "reasons": ["无历史记录，使用默认推荐"],
            }

        # 统计各工具的成功率
        tool_stats: dict[str, dict[str, float]] = {}

        for record in self._container.procedural.data.tool_effectiveness_records:
            if record.task_type == task_type or task_type == "":
                tool: str = record.tool_name
                if tool not in tool_stats:
                    tool_stats[tool] = {"total": 0.0, "success": 0.0, "feedback": 0.0}

                tool_stats[tool]["total"] += 1
                if record.outcome == "success":
                    tool_stats[tool]["success"] += 1
                if record.user_feedback:
                    tool_stats[tool]["feedback"] += record.user_feedback

        if not tool_stats:
            return {
                "tool": "代码解释器",
                "confidence": 0.5,
                "reasons": ["无相关历史记录"],
            }

        # 计算综合分数
        best_tool: str = ""
        best_score: float = 0.0

        for tool, stats in tool_stats.items():
            success_rate: float = stats["success"] / stats["total"] if stats["total"] > 0 else 0
            avg_feedback: float = stats["feedback"] / stats["total"] if stats["total"] > 0 else 0

            score: float = success_rate * 0.5 + avg_feedback / 5.0 * 0.3 + stats["total"] / 10 * 0.2

            if score > best_score:
                best_score = score
                best_tool = tool

        return {
            "tool": best_tool,
            "confidence": min(0.95, best_score),
            "reasons": [
                f"历史成功率: {tool_stats[best_tool]['success'] / tool_stats[best_tool]['total']:.0%}" if tool_stats[best_tool]["total"] > 0 else "无历史记录",
                f"使用次数: {int(tool_stats[best_tool]['total'])}",
            ],
        }

    def update_neuroticism_tendency(
        self, adjustment: float, source: str
    ) -> float:
        """
        更新神经质倾向

        Args:
            adjustment: 调整值
            source: 来源描述

        Returns:
            更新后的分数
        """
        if self._container.procedural is None:
            self._container.procedural = ProceduralMemory(
                memory_id=f"procedural_{uuid.uuid4().hex[:12]}",
                user_id=self.user_id,
                data=ProceduralMemoryData(),
            )

        current_score: float = self._container.procedural.data.neuroticism_tendency.score
        new_score: float = max(-1.0, min(1.0, current_score + adjustment))

        self._container.procedural.data.neuroticism_tendency.score = new_score
        self._container.procedural.data.neuroticism_tendency.derived_from.append(source)

        self._save_to_storage()
        return new_score

    def get_neuroticism_tendency(self) -> float:
        """
        获取神经质倾向分数

        Returns:
            神经质倾向分数 (-1.0 ~ 1.0)
        """
        if self._container.procedural:
            return self._container.procedural.data.neuroticism_tendency.score
        return 0.0

    def update_narrative_memory(self, narrative_data: dict[str, Any]) -> str:
        """
        更新叙事记忆

        Args:
            narrative_data: 叙事记忆数据

        Returns:
            记忆ID
        """
        if self._container.narrative is None:
            memory_id: str = f"narrative_{uuid.uuid4().hex[:12]}"
            self._container.narrative = NarrativeMemory(
                memory_id=memory_id,
                user_id=self.user_id,
                data=NarrativeMemoryData.model_validate(narrative_data),
            )
        else:
            current_data: NarrativeMemoryData = self._container.narrative.data

            # 合并成长节点
            if "growth_milestones" in narrative_data:
                for milestone in narrative_data["growth_milestones"]:
                    current_data.growth_milestones.append(
                        GrowthMilestone(
                            timestamp=datetime.fromisoformat(milestone.get("timestamp", datetime.now().isoformat())),
                            event=milestone.get("event", ""),
                            significance=milestone.get("significance", ""),
                            importance_score=milestone.get("importance_score", 0.5),
                        )
                    )

            # 更新当前身份
            if "current_identity" in narrative_data:
                for identity in narrative_data["current_identity"]:
                    if identity not in current_data.current_identity:
                        current_data.current_identity.append(identity)

        self._save_to_storage()
        return self._container.narrative.memory_id

    def update_semantic_memory(self, semantic_data: dict[str, Any]) -> str:
        """
        更新语义记忆

        Args:
            semantic_data: 语义记忆数据

        Returns:
            记忆ID
        """
        if self._container.semantic is None:
            memory_id: str = f"semantic_{uuid.uuid4().hex[:12]}"
            self._container.semantic = SemanticMemory(
                memory_id=memory_id,
                user_id=self.user_id,
                data=SemanticMemoryData.model_validate(semantic_data),
            )
        else:
            current_data: SemanticMemoryData = self._container.semantic.data

            # 合并核心概念
            if "core_concepts" in semantic_data:
                for concept in semantic_data["core_concepts"]:
                    existing: bool = False
                    for existing_concept in current_data.core_concepts:
                        if existing_concept.concept == concept.get("concept"):
                            existing_concept.usage_count += 1
                            existing = True
                            break

                    if not existing:
                        current_data.core_concepts.append(
                            ConceptDefinition(
                                concept=concept.get("concept", ""),
                                definition=concept.get("definition", ""),
                                attributes=concept.get("attributes", {}),
                                related_concepts=concept.get("related_concepts", []),
                                usage_count=1,
                                confidence=concept.get("confidence", 0.5),
                            )
                        )

        self._save_to_storage()
        return self._container.semantic.memory_id

    def update_emotional_memory(self, emotional_data: dict[str, Any]) -> str:
        """
        更新情感记忆

        Args:
            emotional_data: 情感记忆数据

        Returns:
            记忆ID
        """
        if self._container.emotional is None:
            memory_id: str = f"emotional_{uuid.uuid4().hex[:12]}"
            self._container.emotional = EmotionalMemory(
                memory_id=memory_id,
                user_id=self.user_id,
                data=EmotionalMemoryData.model_validate(emotional_data),
            )
        else:
            current_data: EmotionalMemoryData = self._container.emotional.data

            # 添加情绪状态
            if "emotion_states" in emotional_data:
                for state in emotional_data["emotion_states"]:
                    current_data.emotion_states.append(
                        EmotionState(
                            timestamp=datetime.fromisoformat(state.get("timestamp", datetime.now().isoformat())),
                            emotion_type=state.get("emotion_type", "neutral"),
                            intensity=state.get("intensity", 0.5),
                            trigger_context=state.get("trigger_context", ""),
                            topic=state.get("topic", ""),
                            decay_factor=state.get("decay_factor", 0.98),
                        )
                    )

        self._save_to_storage()
        return self._container.emotional.memory_id

    def update_from_extractions(self, extractions: dict[str, Any]) -> dict[str, str]:
        """
        从提炼结果更新记忆

        Args:
            extractions: 提炼结果

        Returns:
            更新的记忆ID映射
        """
        result: dict[str, str] = {}

        if extractions.get("user_profile"):
            result["user_profile"] = self.update_user_profile(
                extractions["user_profile"]
            )

        if extractions.get("procedural"):
            result["procedural"] = self.update_procedural_memory(
                extractions["procedural"]
            )

        if extractions.get("narrative"):
            result["narrative"] = self.update_narrative_memory(
                extractions["narrative"]
            )

        if extractions.get("semantic"):
            result["semantic"] = self.update_semantic_memory(
                extractions["semantic"]
            )

        if extractions.get("emotional"):
            result["emotional"] = self.update_emotional_memory(
                extractions["emotional"]
            )

        return result

    def get_all_memories(self) -> LongTermMemoryContainer:
        """
        获取所有长期记忆

        Returns:
            长期记忆容器
        """
        return self._container

    def apply_heat_policy(self) -> dict[str, Any]:
        """
        应用冷热度策略

        Returns:
            应用结果统计
        """
        result: dict[str, Any] = {
            "total_processed": 0,
            "migrations": [],
        }

        # 处理用户画像（通常保持热状态）
        if self._container.user_profile:
            self._container.user_profile.heat.heat_level = HeatLevel.HOT
            self._container.user_profile.heat.heat_score = 100.0
            result["total_processed"] += 1

        # 处理程序性记忆
        if self._container.procedural:
            memory: ProceduralMemory = self._container.procedural
            new_score: float = self._heat_manager.calculate_heat_score(
                days_since_access=self._days_since(memory.heat.last_accessed_at),
                access_count=memory.heat.access_count,
                importance=0.8,
                user_interaction=0.0,
            )
            new_level: HeatLevel = self._heat_manager.determine_level(new_score)

            if new_level != memory.heat.heat_level:
                result["migrations"].append(
                    {
                        "memory_id": memory.memory_id,
                        "from": memory.heat.heat_level.value,
                        "to": new_level.value,
                    }
                )
                memory.heat.heat_score = new_score
                memory.heat.heat_level = new_level

            result["total_processed"] += 1

        # 处理叙事记忆
        if self._container.narrative:
            memory_n: NarrativeMemory = self._container.narrative
            new_score_n: float = self._heat_manager.calculate_heat_score(
                days_since_access=self._days_since(memory_n.heat.last_accessed_at),
                access_count=memory_n.heat.access_count,
                importance=0.6,
                user_interaction=0.0,
            )
            new_level_n: HeatLevel = self._heat_manager.determine_level(new_score_n)

            memory_n.heat.heat_score = new_score_n
            memory_n.heat.heat_level = new_level_n
            result["total_processed"] += 1

        # 处理情感记忆
        if self._container.emotional:
            memory_e: EmotionalMemory = self._container.emotional
            new_score_e: float = self._heat_manager.calculate_heat_score(
                days_since_access=self._days_since(memory_e.heat.last_accessed_at),
                access_count=memory_e.heat.access_count,
                importance=0.5,
                user_interaction=0.0,
            )
            new_level_e: HeatLevel = self._heat_manager.determine_level(new_score_e)

            memory_e.heat.heat_score = new_score_e
            memory_e.heat.heat_level = new_level_e
            result["total_processed"] += 1

            # 情感衰减
            self._apply_emotion_decay()

        self._save_to_storage()
        return result

    def _days_since(self, timestamp: datetime) -> float:
        """
        计算距今天数（内部方法）

        Args:
            timestamp: 时间戳

        Returns:
            天数
        """
        delta = datetime.now() - timestamp
        return delta.total_seconds() / 86400

    def _apply_emotion_decay(self) -> None:
        """
        应用情感衰减（内部方法）
        """
        if self._container.emotional is None:
            return

        now: datetime = datetime.now()
        updated_states: list[EmotionState] = []

        for state in self._container.emotional.data.emotion_states:
            days_passed: float = (now - state.timestamp).total_seconds() / 86400
            new_intensity: float = state.intensity * (state.decay_factor**days_passed)

            # 保留强度大于 0.1 的情绪
            if new_intensity > 0.1:
                state.intensity = new_intensity
                updated_states.append(state)

        self._container.emotional.data.emotion_states = updated_states[
            -50:
        ]  # 保留最近 50 条

    def get_memory_by_type(self, memory_type: MemoryType) -> Any | None:
        """
        按类型获取记忆

        Args:
            memory_type: 记忆类型

        Returns:
            记忆数据
        """
        mapping: dict[MemoryType, Any] = {
            MemoryType.USER_PROFILE: self._container.user_profile,
            MemoryType.PROCEDURAL: self._container.procedural,
            MemoryType.NARRATIVE: self._container.narrative,
            MemoryType.SEMANTIC: self._container.semantic,
            MemoryType.EMOTIONAL: self._container.emotional,
        }
        return mapping.get(memory_type)

    def clear_all_memories(self) -> None:
        """
        清除所有记忆

        警告：此操作不可逆
        """
        self._container = LongTermMemoryContainer(user_id=self.user_id)
        self._save_to_storage()


# ============================================================================
# 导出
# ============================================================================

__all__ = ["LongTermMemoryManager"]
