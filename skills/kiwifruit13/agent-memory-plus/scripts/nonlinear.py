"""
Agent Memory System - 非线性记忆模块

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

import uuid
from datetime import datetime, timedelta
from typing import Any

from .types import (
    LongTermMemoryContainer,
    SituationAwareness,
    ActivatedMemory,
    ActivationResult,
    ReconstructedContext,
    TaskContextLayer,
    UserStateLayer,
    ActivatedExperiencesLayer,
    KnowledgeContextLayer,
    EmotionalContextLayer,
    NarrativeAnchorLayer,
    TriggerDimension,
    MemoryType,
    HeatLevel,
    ActivationSource,
    UserProfileMemory,
    ProceduralMemory,
    NarrativeMemory,
    SemanticMemory,
    EmotionalMemory,
    TaskType,
    ResolutionMode,
)


class MemoryActivator:
    """
    记忆激活器基类

    所有维度激活器的基类
    """

    dimension: TriggerDimension = TriggerDimension.TEMPORAL

    def activate(
        self,
        situation: SituationAwareness,
        memories: LongTermMemoryContainer,
    ) -> list[ActivationSource]:
        """
        激活相关记忆

        Args:
            situation: 当前情境
            memories: 长期记忆容器

        Returns:
            激活来源列表
        """
        raise NotImplementedError


class TemporalActivator(MemoryActivator):
    """
    时间激活器

    基于时间窗口激活近期相关记忆
    """

    dimension = TriggerDimension.TEMPORAL

    def __init__(self) -> None:
        """初始化时间激活器"""
        self._time_windows: dict[str, tuple[float, float]] = {
            "immediate": (0, 1),
            "recent": (1, 24),
            "weekly": (24, 168),
            "monthly": (168, 720),
            "archived": (720, float("inf")),
        }
        self._window_weights: dict[str, float] = {
            "immediate": 1.0,
            "recent": 0.85,
            "weekly": 0.70,
            "monthly": 0.55,
            "archived": 0.35,
        }

    def activate(
        self,
        situation: SituationAwareness,
        memories: LongTermMemoryContainer,
    ) -> list[ActivationSource]:
        """
        基于时间激活记忆

        Args:
            situation: 当前情境
            memories: 长期记忆容器

        Returns:
            激活来源列表
        """
        sources: list[ActivationSource] = []

        # 检查各记忆类型的时间相关性
        if memories.user_profile:
            hours_since: float = self._hours_since(
                memories.user_profile.timestamp.updated_at
            )
            weight: float = self._get_window_weight(hours_since)
            if weight > 0.5:
                sources.append(
                    ActivationSource(
                        dimension=self.dimension,
                        score=weight,
                    )
                )

        if memories.procedural:
            hours_since_p: float = self._hours_since(
                memories.procedural.timestamp.updated_at
            )
            weight_p: float = self._get_window_weight(hours_since_p)
            if weight_p > 0.5:
                sources.append(
                    ActivationSource(
                        dimension=self.dimension,
                        score=weight_p,
                    )
                )

        return sources

    def _hours_since(self, timestamp: datetime) -> float:
        """计算距今小时数"""
        delta = datetime.now() - timestamp
        return delta.total_seconds() / 3600

    def _get_window_weight(self, hours: float) -> float:
        """获取时间窗口权重"""
        for window_name, (low, high) in self._time_windows.items():
            if low <= hours < high:
                return self._window_weights.get(window_name, 0.5)
        return 0.35


class SemanticActivator(MemoryActivator):
    """
    语义激活器

    基于概念关联激活语义相关记忆
    """

    dimension = TriggerDimension.SEMANTIC

    def __init__(self) -> None:
        """初始化语义激活器"""
        self._match_weights: dict[str, float] = {
            "direct": 1.0,
            "synonym": 0.85,
            "hyponym": 0.75,
            "hypernym": 0.70,
            "causal": 0.65,
        }

    def activate(
        self,
        situation: SituationAwareness,
        memories: LongTermMemoryContainer,
    ) -> list[ActivationSource]:
        """
        基于语义激活记忆

        Args:
            situation: 当前情境
            memories: 长期记忆容器

        Returns:
            激活来源列表
        """
        sources: list[ActivationSource] = []

        # 从情境中提取关键词
        task_keywords: list[str] = self._extract_keywords(situation)

        # 匹配语义记忆中的概念
        if memories.semantic:
            match_score: float = self._match_concepts(
                task_keywords, memories.semantic
            )
            if match_score > 0.5:
                sources.append(
                    ActivationSource(
                        dimension=self.dimension,
                        score=match_score,
                    )
                )

        return sources

    def _extract_keywords(self, situation: SituationAwareness) -> list[str]:
        """从情境提取关键词"""
        keywords: list[str] = []

        # 从任务上下文提取
        task_desc: str = situation.current_task.task_type.value
        keywords.extend(task_desc.split("_"))

        return keywords

    def _match_concepts(
        self, keywords: list[str], semantic: SemanticMemory
    ) -> float:
        """匹配概念"""
        if not semantic.data.core_concepts:
            return 0.0

        match_count: int = 0
        for concept in semantic.data.core_concepts:
            if concept.concept.lower() in [kw.lower() for kw in keywords]:
                match_count += 1

        return min(1.0, match_count / 3.0)


class ContextualActivator(MemoryActivator):
    """
    情境激活器

    基于任务情境激活相似场景记忆
    """

    dimension = TriggerDimension.CONTEXTUAL

    def activate(
        self,
        situation: SituationAwareness,
        memories: LongTermMemoryContainer,
    ) -> list[ActivationSource]:
        """
        基于情境激活记忆

        Args:
            situation: 当前情境
            memories: 长期记忆容器

        Returns:
            激活来源列表
        """
        sources: list[ActivationSource] = []

        # 匹配程序性记忆中的问题解决策略
        if memories.procedural:
            context_score: float = self._match_context(
                situation, memories.procedural
            )
            if context_score > 0.5:
                sources.append(
                    ActivationSource(
                        dimension=self.dimension,
                        score=context_score,
                    )
                )

        return sources

    def _match_context(
        self, situation: SituationAwareness, procedural: ProceduralMemory
    ) -> float:
        """匹配情境"""
        task_type: str = situation.current_task.task_type.value

        for strategy in procedural.data.problem_solving_strategies:
            if strategy.problem_type.lower() in task_type.lower():
                return 0.8

        return 0.0


class EmotionalActivator(MemoryActivator):
    """
    情感激活器

    基于情感共鸣激活相似情感记忆
    """

    dimension = TriggerDimension.EMOTIONAL

    def activate(
        self,
        situation: SituationAwareness,
        memories: LongTermMemoryContainer,
    ) -> list[ActivationSource]:
        """
        基于情感激活记忆

        Args:
            situation: 当前情境
            memories: 长期记忆容器

        Returns:
            激活来源列表
        """
        sources: list[ActivationSource] = []

        # 检测当前情感
        current_emotion: str = situation.context_anchors.emotional

        # 匹配情感记忆
        if memories.emotional:
            emotion_score: float = self._match_emotion(
                current_emotion, memories.emotional
            )
            if emotion_score > 0.3:
                sources.append(
                    ActivationSource(
                        dimension=self.dimension,
                        score=emotion_score,
                    )
                )

        return sources

    def _match_emotion(
        self, current: str, emotional: EmotionalMemory
    ) -> float:
        """匹配情感"""
        if not emotional.data.emotion_states:
            return 0.0

        # 获取最近的情感状态
        recent_states = emotional.data.emotion_states[-5:]
        for state in recent_states:
            if state.emotion_type in current or current in state.emotion_type:
                return 0.7 * state.intensity

        return 0.0


class CausalActivator(MemoryActivator):
    """
    因果激活器

    基于因果链激活相关经验
    """

    dimension = TriggerDimension.CAUSAL

    def activate(
        self,
        situation: SituationAwareness,
        memories: LongTermMemoryContainer,
    ) -> list[ActivationSource]:
        """
        基于因果激活记忆

        Args:
            situation: 当前情境
            memories: 长期记忆容器

        Returns:
            激活来源列表
        """
        sources: list[ActivationSource] = []

        # 检查程序性记忆中的成功/失败模式
        if memories.procedural:
            causal_score: float = self._match_causal_patterns(
                situation, memories.procedural
            )
            if causal_score > 0.5:
                sources.append(
                    ActivationSource(
                        dimension=self.dimension,
                        score=causal_score,
                    )
                )

        return sources

    def _match_causal_patterns(
        self, situation: SituationAwareness, procedural: ProceduralMemory
    ) -> float:
        """匹配因果模式"""
        # 检查决策模式的成功/失败率
        if procedural.data.decision_patterns:
            avg_success: float = sum(
                p.success_rate for p in procedural.data.decision_patterns
            ) / len(procedural.data.decision_patterns)
            return avg_success

        return 0.0


class IdentityActivator(MemoryActivator):
    """
    身份激活器

    基于身份关联激活相关成长记忆
    """

    dimension = TriggerDimension.IDENTITY

    def activate(
        self,
        situation: SituationAwareness,
        memories: LongTermMemoryContainer,
    ) -> list[ActivationSource]:
        """
        基于身份激活记忆

        Args:
            situation: 当前情境
            memories: 长期记忆容器

        Returns:
            激活来源列表
        """
        sources: list[ActivationSource] = []

        # 匹配用户身份
        if memories.user_profile and memories.narrative:
            identity_score: float = self._match_identity(
                situation, memories.user_profile, memories.narrative
            )
            if identity_score > 0.5:
                sources.append(
                    ActivationSource(
                        dimension=self.dimension,
                        score=identity_score,
                    )
                )

        return sources

    def _match_identity(
        self,
        situation: SituationAwareness,
        profile: UserProfileMemory,
        narrative: NarrativeMemory,
    ) -> float:
        """匹配身份"""
        # 检查身份标签与当前任务的关联
        task_focus: str = situation.current_task.task_type.value

        for identity in profile.data.identity:
            if identity.lower() in task_focus.lower():
                return 0.8

        return 0.0


class NonlinearMemoryActivator:
    """
    非线性记忆激活器

    核心模块：负责多维激活、记忆网络、区间管理、上下文重构
    """

    def __init__(self) -> None:
        """初始化非线性记忆激活器"""
        # 初始化六维激活器
        self._activators: list[MemoryActivator] = [
            TemporalActivator(),
            SemanticActivator(),
            ContextualActivator(),
            EmotionalActivator(),
            CausalActivator(),
            IdentityActivator(),
        ]

        # 激活配置
        self._max_activated_memories: int = 15
        self._relevance_threshold: float = 0.5

    def activate_memories(
        self,
        situation: SituationAwareness,
        long_term_memory: LongTermMemoryContainer,
    ) -> ActivationResult:
        """
        激活相关记忆

        Args:
            situation: 当前情境
            long_term_memory: 长期记忆容器

        Returns:
            激活结果
        """
        activated_memories: list[ActivatedMemory] = []
        activation_coverage: list[TriggerDimension] = []

        # 1. 并行执行六维激活
        all_sources: dict[str, list[ActivationSource]] = {}
        for activator in self._activators:
            sources: list[ActivationSource] = activator.activate(
                situation, long_term_memory
            )
            if sources:
                all_sources[activator.dimension.value] = sources
                activation_coverage.append(activator.dimension)

        # 2. 为每个记忆类型构建激活记录
        memory_items: list[tuple[str, MemoryType, Any, HeatLevel]] = []

        if long_term_memory.user_profile:
            memory_items.append(
                (
                    long_term_memory.user_profile.memory_id,
                    MemoryType.USER_PROFILE,
                    long_term_memory.user_profile,
                    long_term_memory.user_profile.heat.heat_level,
                )
            )

        if long_term_memory.procedural:
            memory_items.append(
                (
                    long_term_memory.procedural.memory_id,
                    MemoryType.PROCEDURAL,
                    long_term_memory.procedural,
                    long_term_memory.procedural.heat.heat_level,
                )
            )

        if long_term_memory.narrative:
            memory_items.append(
                (
                    long_term_memory.narrative.memory_id,
                    MemoryType.NARRATIVE,
                    long_term_memory.narrative,
                    long_term_memory.narrative.heat.heat_level,
                )
            )

        if long_term_memory.semantic:
            memory_items.append(
                (
                    long_term_memory.semantic.memory_id,
                    MemoryType.SEMANTIC,
                    long_term_memory.semantic,
                    long_term_memory.semantic.heat.heat_level,
                )
            )

        if long_term_memory.emotional:
            memory_items.append(
                (
                    long_term_memory.emotional.memory_id,
                    MemoryType.EMOTIONAL,
                    long_term_memory.emotional,
                    long_term_memory.emotional.heat.heat_level,
                )
            )

        # 3. 计算综合激活分数
        for memory_id, memory_type, memory_obj, heat_level in memory_items:
            triggered_by: list[TriggerDimension] = []
            activation_sources: list[ActivationSource] = []
            total_score: float = 0.0

            for dim, sources_list in all_sources.items():
                for source in sources_list:
                    total_score += source.score
                    dim_enum: TriggerDimension = TriggerDimension(dim)
                    if dim_enum not in triggered_by:
                        triggered_by.append(dim_enum)
                    activation_sources.append(source)

            relevance_score: float = min(1.0, total_score / 3.0)

            if relevance_score >= self._relevance_threshold:
                activated_memories.append(
                    ActivatedMemory(
                        memory_id=memory_id,
                        memory_type=memory_type,
                        content_summary=self._summarize_memory(memory_obj),
                        triggered_by=triggered_by,
                        relevance_score=relevance_score,
                        heat_level=heat_level,
                        conflicts=[],
                        activation_sources=activation_sources,
                    )
                )

        # 4. 按相关性排序并限制数量
        activated_memories.sort(
            key=lambda x: x.relevance_score, reverse=True
        )
        activated_memories = activated_memories[: self._max_activated_memories]

        # 5. 去重统计
        unique_count: int = len(activated_memories)

        return ActivationResult(
            activated_memories=activated_memories,
            total_count=len(activated_memories),
            unique_count=unique_count,
            conflicts_detected=0,
            activation_coverage=activation_coverage,
        )

    def _summarize_memory(self, memory: Any) -> str:
        """生成记忆摘要"""
        if hasattr(memory, "data"):
            if hasattr(memory.data, "identity"):
                return f"用户画像: {', '.join(memory.data.identity[:3])}"
            elif hasattr(memory.data, "decision_patterns"):
                patterns_count: int = len(memory.data.decision_patterns)
                return f"程序性记忆: {patterns_count} 个决策模式"
            elif hasattr(memory.data, "growth_milestones"):
                milestones_count: int = len(memory.data.growth_milestones)
                return f"叙事记忆: {milestones_count} 个成长节点"
            elif hasattr(memory.data, "core_concepts"):
                concepts_count: int = len(memory.data.core_concepts)
                return f"语义记忆: {concepts_count} 个核心概念"
            elif hasattr(memory.data, "emotion_states"):
                emotions_count: int = len(memory.data.emotion_states)
                return f"情感记忆: {emotions_count} 个情绪状态"
        return "记忆内容"

    def reconstruct_context(
        self, activation_result: ActivationResult
    ) -> ReconstructedContext:
        """
        重构上下文

        Args:
            activation_result: 激活结果

        Returns:
            重构后的上下文
        """
        activated: list[ActivatedMemory] = activation_result.activated_memories

        # 构建各层上下文
        task_context: TaskContextLayer = self._build_task_context(activated)
        user_state: UserStateLayer = self._build_user_state(activated)
        experiences: ActivatedExperiencesLayer = self._build_experiences(activated)
        knowledge: KnowledgeContextLayer = self._build_knowledge(activated)
        emotional: EmotionalContextLayer = self._build_emotional(activated)
        narrative: NarrativeAnchorLayer = self._build_narrative(activated)

        return ReconstructedContext(
            task_context=task_context,
            user_state=user_state,
            activated_experiences=experiences,
            knowledge_context=knowledge,
            emotional_context=emotional,
            narrative_anchor=narrative,
            conflicts_handled=[],
            metadata={
                "total_memories_used": len(activated),
                "activation_coverage": [d.value for d in activation_result.activation_coverage],
                "reconstruction_timestamp": datetime.now().isoformat(),
            },
        )

    def _build_task_context(
        self, activated: list[ActivatedMemory]
    ) -> TaskContextLayer:
        """构建任务上下文层"""
        return TaskContextLayer(
            current_task="基于激活记忆推断的任务",
            task_phase="探索阶段",
            implicit_requirements=["需要记忆支持"],
        )

    def _build_user_state(
        self, activated: list[ActivatedMemory]
    ) -> UserStateLayer:
        """构建用户状态层"""
        # 从激活记忆中提取用户状态信息
        profile_data: dict[str, Any] = {}
        for mem in activated:
            if mem.memory_type == MemoryType.USER_PROFILE:
                profile_data["identity"] = mem.content_summary

        return UserStateLayer(
            user_profile_core=profile_data,
            current_focus="当前任务焦点",
            decision_style="balanced",
            neuroticism_tendency=0.0,
        )

    def _build_experiences(
        self, activated: list[ActivatedMemory]
    ) -> ActivatedExperiencesLayer:
        """构建激活经验层"""
        patterns: list[dict[str, Any]] = []
        success_stories: list[dict[str, Any]] = []
        failure_lessons: list[dict[str, Any]] = []
        tool_recommendations: list[dict[str, Any]] = []

        for mem in activated:
            if mem.memory_type == MemoryType.PROCEDURAL:
                patterns.append(
                    {
                        "memory_id": mem.memory_id,
                        "relevance": mem.relevance_score,
                        "summary": mem.content_summary,
                    }
                )

        return ActivatedExperiencesLayer(
            relevant_patterns=patterns,
            success_stories=success_stories,
            failure_lessons=failure_lessons,
            tool_recommendations=tool_recommendations,
        )

    def _build_knowledge(
        self, activated: list[ActivatedMemory]
    ) -> KnowledgeContextLayer:
        """构建知识上下文层"""
        concepts: list[dict[str, Any]] = []

        for mem in activated:
            if mem.memory_type == MemoryType.SEMANTIC:
                concepts.append(
                    {
                        "memory_id": mem.memory_id,
                        "summary": mem.content_summary,
                    }
                )

        return KnowledgeContextLayer(
            key_concepts=concepts,
            concept_relations=[],
            principles=[],
        )

    def _build_emotional(
        self, activated: list[ActivatedMemory]
    ) -> EmotionalContextLayer:
        """构建情感上下文层"""
        current_emotion: str = "中性"
        intensity: float = 0.5

        for mem in activated:
            if mem.memory_type == MemoryType.EMOTIONAL:
                current_emotion = mem.content_summary
                break

        return EmotionalContextLayer(
            current_emotion=current_emotion,
            emotional_trend="稳定",
            satisfaction_level=intensity,
        )

    def _build_narrative(
        self, activated: list[ActivatedMemory]
    ) -> NarrativeAnchorLayer:
        """构建叙事锚点层"""
        milestones: list[dict[str, Any]] = []
        identity_evolution: list[str] = []
        concerns: list[str] = []

        for mem in activated:
            if mem.memory_type == MemoryType.NARRATIVE:
                milestones.append(
                    {
                        "memory_id": mem.memory_id,
                        "summary": mem.content_summary,
                    }
                )

        return NarrativeAnchorLayer(
            growth_milestones=milestones,
            identity_evolution=identity_evolution,
            continuous_concerns=concerns,
        )

    def get_tool_recommendation(
        self,
        task_type: str,
        constraints: list[str] | None = None,
        procedural: ProceduralMemory | None = None,
    ) -> dict[str, Any]:
        """
        获取工具推荐

        Args:
            task_type: 任务类型
            constraints: 约束条件
            procedural: 程序性记忆

        Returns:
            工具推荐结果
        """
        if procedural is None:
            return {
                "tool": "代码解释器",
                "confidence": 0.5,
                "reasons": ["无历史记录"],
                "combination_opportunity": None,
                "cautions": [],
            }

        # 统计工具效果
        tool_scores: dict[str, float] = {}
        tool_reasons: dict[str, list[str]] = {}

        for record in procedural.data.tool_effectiveness_records:
            tool: str = record.tool_name
            if tool not in tool_scores:
                tool_scores[tool] = 0.0
                tool_reasons[tool] = []

            score: float = record.effectiveness_score
            if record.outcome == "success":
                score += 0.2
            if record.user_feedback and record.user_feedback > 4.0:
                score += 0.1
                tool_reasons[tool].append(f"用户反馈: {record.user_feedback:.1f}")

            tool_scores[tool] = max(tool_scores[tool], score)

        if not tool_scores:
            return {
                "tool": "代码解释器",
                "confidence": 0.5,
                "reasons": ["无有效历史记录"],
                "combination_opportunity": None,
                "cautions": [],
            }

        # 选择最佳工具
        best_tool: str = max(tool_scores, key=tool_scores.get)
        best_score: float = tool_scores[best_tool]

        # 检查工具组合机会
        combination: str | None = None
        for pattern in procedural.data.tool_combination_patterns:
            if best_tool in pattern.sequence:
                combination = " → ".join(pattern.sequence)
                break

        return {
            "tool": best_tool,
            "confidence": min(0.95, best_score),
            "reasons": tool_reasons.get(best_tool, ["历史使用记录"]),
            "combination_opportunity": combination,
            "cautions": [],
        }


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    "MemoryActivator",
    "TemporalActivator",
    "SemanticActivator",
    "ContextualActivator",
    "EmotionalActivator",
    "CausalActivator",
    "IdentityActivator",
    "NonlinearMemoryActivator",
]
