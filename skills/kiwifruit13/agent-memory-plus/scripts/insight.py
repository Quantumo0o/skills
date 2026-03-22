"""
Agent Memory System - 洞察模块

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
from datetime import datetime
from typing import Any

from .types import (
    Insight,
    InsightSignal,
    InsightType,
    InsightPriority,
    SignalStrength,
    UserDecision,
    DecisionType,
    LongTermMemoryContainer,
    ReconstructedContext,
)


class InsightGenerator:
    """
    洞察生成器

    负责从记忆和上下文中提取洞察信号，生成有价值的洞察
    """

    def __init__(self) -> None:
        """初始化洞察生成器"""
        self._signal_thresholds: dict[InsightType, float] = {
            InsightType.USER_PREFERENCE: 0.6,
            InsightType.BEHAVIORAL_PATTERN: 0.7,
            InsightType.BEST_PRACTICE: 0.75,
            InsightType.EFFICIENCY_OPPORTUNITY: 0.5,
            InsightType.KNOWLEDGE_GAP: 0.65,
            InsightType.PROCESS_IMPROVEMENT: 0.6,
            InsightType.ERROR_PREVENTION: 0.7,
            InsightType.EMOTIONAL_PATTERN: 0.55,
            InsightType.IDENTITY_EVOLUTION: 0.65,
        }

    def generate_signals(
        self,
        long_term_memory: LongTermMemoryContainer,
        context: ReconstructedContext,
    ) -> list[InsightSignal]:
        """
        生成洞察信号

        Args:
            long_term_memory: 长期记忆
            context: 重构上下文

        Returns:
            洞察信号列表
        """
        signals: list[InsightSignal] = []

        # 1. 用户偏好信号
        preference_signals: list[InsightSignal] = self._detect_preferences(
            long_term_memory
        )
        signals.extend(preference_signals)

        # 2. 行为模式信号
        behavior_signals: list[InsightSignal] = self._detect_patterns(
            long_term_memory
        )
        signals.extend(behavior_signals)

        # 3. 最佳实践信号
        practice_signals: list[InsightSignal] = self._detect_best_practices(
            long_term_memory
        )
        signals.extend(practice_signals)

        # 4. 效率机会信号
        efficiency_signals: list[InsightSignal] = self._detect_efficiency_opportunities(
            long_term_memory
        )
        signals.extend(efficiency_signals)

        # 5. 知识缺口信号
        gap_signals: list[InsightSignal] = self._detect_knowledge_gaps(
            long_term_memory, context
        )
        signals.extend(gap_signals)

        # 6. 情感模式信号
        emotion_signals: list[InsightSignal] = self._detect_emotional_patterns(
            long_term_memory
        )
        signals.extend(emotion_signals)

        # 7. 身份演化信号
        identity_signals: list[InsightSignal] = self._detect_identity_evolution(
            long_term_memory
        )
        signals.extend(identity_signals)

        return signals

    def _detect_preferences(
        self, memory: LongTermMemoryContainer
    ) -> list[InsightSignal]:
        """检测用户偏好"""
        signals: list[InsightSignal] = []

        if memory.user_profile:
            profile: Any = memory.user_profile.data

            # 沟通风格偏好
            style: str = profile.communication_style.style
            if style:
                signals.append(
                    InsightSignal(
                        signal_id=f"sig_{uuid.uuid4().hex[:8]}",
                        signal_type=InsightType.USER_PREFERENCE,
                        confidence=0.85,
                        data={"communication_style": style},
                        raw_observation=f"用户偏好 {style} 的沟通方式",
                    )
                )

            # 决策模式偏好
            decision_type: str = profile.decision_pattern.type
            if decision_type:
                signals.append(
                    InsightSignal(
                        signal_id=f"sig_{uuid.uuid4().hex[:8]}",
                        signal_type=InsightType.USER_PREFERENCE,
                        confidence=0.75,
                        data={"decision_style": decision_type},
                        raw_observation=f"用户决策风格: {decision_type}",
                    )
                )

        return signals

    def _detect_patterns(
        self, memory: LongTermMemoryContainer
    ) -> list[InsightSignal]:
        """检测行为模式"""
        signals: list[InsightSignal] = []

        if memory.procedural:
            procedural: Any = memory.procedural.data

            # 决策模式检测
            for pattern in procedural.decision_patterns:
                if pattern.usage_count >= 3:
                    signals.append(
                        InsightSignal(
                            signal_id=f"sig_{uuid.uuid4().hex[:8]}",
                            signal_type=InsightType.BEHAVIORAL_PATTERN,
                            confidence=pattern.confidence,
                            data={
                                "pattern": pattern.workflow,
                                "trigger": pattern.trigger_condition,
                                "usage_count": pattern.usage_count,
                            },
                            raw_observation=f"发现重复决策模式: {' → '.join(pattern.workflow)}",
                        )
                    )

        return signals

    def _detect_best_practices(
        self, memory: LongTermMemoryContainer
    ) -> list[InsightSignal]:
        """检测最佳实践"""
        signals: list[InsightSignal] = []

        if memory.procedural:
            procedural: Any = memory.procedural.data

            # 检查成功的问题解决策略
            for strategy in procedural.problem_solving_strategies:
                if strategy.success_rate >= 0.8:
                    signals.append(
                        InsightSignal(
                            signal_id=f"sig_{uuid.uuid4().hex[:8]}",
                            signal_type=InsightType.BEST_PRACTICE,
                            confidence=strategy.success_rate,
                            data={
                                "strategy_id": strategy.strategy_id,
                                "problem_type": strategy.problem_type,
                                "approach": strategy.approach,
                            },
                            raw_observation=f"发现高效策略: {strategy.problem_type}",
                        )
                    )

            # 检查工具使用模式
            tool_scores: dict[str, dict[str, float]] = {}
            for record in procedural.tool_effectiveness_records:
                tool: str = record.tool_name
                if tool not in tool_scores:
                    tool_scores[tool] = {"total": 0.0, "success": 0.0}
                tool_scores[tool]["total"] += 1
                if record.outcome == "success":
                    tool_scores[tool]["success"] += 1

            for tool, stats in tool_scores.items():
                if stats["total"] >= 3 and stats["success"] / stats["total"] >= 0.8:
                    signals.append(
                        InsightSignal(
                            signal_id=f"sig_{uuid.uuid4().hex[:8]}",
                            signal_type=InsightType.BEST_PRACTICE,
                            confidence=stats["success"] / stats["total"],
                            data={
                                "tool": tool,
                                "success_rate": stats["success"] / stats["total"],
                            },
                            raw_observation=f"工具 {tool} 使用效果优秀",
                        )
                    )

        return signals

    def _detect_efficiency_opportunities(
        self, memory: LongTermMemoryContainer
    ) -> list[InsightSignal]:
        """检测效率提升机会"""
        signals: list[InsightSignal] = []

        if memory.procedural:
            procedural: Any = memory.procedural.data

            # 检查工具组合模式
            for pattern in procedural.tool_combination_patterns:
                if pattern.usage_count >= 2:
                    signals.append(
                        InsightSignal(
                            signal_id=f"sig_{uuid.uuid4().hex[:8]}",
                            signal_type=InsightType.EFFICIENCY_OPPORTUNITY,
                            confidence=0.7,
                            data={
                                "combination": pattern.sequence,
                                "context": pattern.context,
                            },
                            raw_observation=f"发现工具组合模式: {' → '.join(pattern.sequence)}",
                        )
                    )

        return signals

    def _detect_knowledge_gaps(
        self,
        memory: LongTermMemoryContainer,
        context: ReconstructedContext,
    ) -> list[InsightSignal]:
        """检测知识缺口"""
        signals: list[InsightSignal] = []

        # 检查语义记忆的覆盖度
        if memory.semantic:
            semantic: Any = memory.semantic.data

            # 如果核心概念较少，提示知识缺口
            if len(semantic.core_concepts) < 5:
                signals.append(
                    InsightSignal(
                        signal_id=f"sig_{uuid.uuid4().hex[:8]}",
                        signal_type=InsightType.KNOWLEDGE_GAP,
                        confidence=0.6,
                        data={"concept_count": len(semantic.core_concepts)},
                        raw_observation="语义知识覆盖度较低，可能存在知识缺口",
                    )
                )

        return signals

    def _detect_emotional_patterns(
        self, memory: LongTermMemoryContainer
    ) -> list[InsightSignal]:
        """检测情感模式"""
        signals: list[InsightSignal] = []

        if memory.emotional:
            emotional: Any = memory.emotional.data

            # 统计情感类型分布
            emotion_counts: dict[str, int] = {}
            for state in emotional.emotion_states[-20:]:
                emotion_type: str = state.emotion_type
                emotion_counts[emotion_type] = emotion_counts.get(emotion_type, 0) + 1

            # 检测主导情感
            if emotion_counts:
                dominant_emotion: str = max(emotion_counts, key=emotion_counts.get)
                dominant_ratio: float = emotion_counts[dominant_emotion] / sum(emotion_counts.values())

                if dominant_ratio >= 0.5 and dominant_emotion != "neutral":
                    signals.append(
                        InsightSignal(
                            signal_id=f"sig_{uuid.uuid4().hex[:8]}",
                            signal_type=InsightType.EMOTIONAL_PATTERN,
                            confidence=dominant_ratio,
                            data={
                                "dominant_emotion": dominant_emotion,
                                "ratio": dominant_ratio,
                            },
                            raw_observation=f"用户情感倾向: {dominant_emotion} ({dominant_ratio:.0%})",
                        )
                    )

        return signals

    def _detect_identity_evolution(
        self, memory: LongTermMemoryContainer
    ) -> list[InsightSignal]:
        """检测身份演化"""
        signals: list[InsightSignal] = []

        if memory.narrative:
            narrative: Any = memory.narrative.data

            # 检查成长节点
            if len(narrative.growth_milestones) >= 3:
                signals.append(
                    InsightSignal(
                        signal_id=f"sig_{uuid.uuid4().hex[:8]}",
                        signal_type=InsightType.IDENTITY_EVOLUTION,
                        confidence=0.7,
                        data={
                            "milestone_count": len(narrative.growth_milestones),
                        },
                        raw_observation=f"用户有 {len(narrative.growth_milestones)} 个成长节点",
                    )
                )

        return signals

    def generate_insights(
        self,
        signals: list[InsightSignal],
        context: ReconstructedContext,
    ) -> list[Insight]:
        """
        从信号生成洞察

        Args:
            signals: 洞察信号列表
            context: 重构上下文

        Returns:
            洞察列表
        """
        insights: list[Insight] = []

        # 按类型分组信号
        signals_by_type: dict[InsightType, list[InsightSignal]] = {}
        for signal in signals:
            signal_type: InsightType = signal.signal_type
            if signal_type not in signals_by_type:
                signals_by_type[signal_type] = []
            signals_by_type[signal_type].append(signal)

        # 为每种类型生成洞察
        for insight_type, type_signals in signals_by_type.items():
            threshold: float = self._signal_thresholds.get(insight_type, 0.5)

            # 筛选超过阈值的信号
            qualified_signals: list[InsightSignal] = [
                s for s in type_signals if s.confidence >= threshold
            ]

            if qualified_signals:
                # 合并相似信号
                merged_signal: InsightSignal = self._merge_signals(
                    qualified_signals, insight_type
                )

                # 确定优先级
                priority: InsightPriority = self._determine_priority(
                    merged_signal, insight_type
                )

                # 生成洞察
                insight: Insight = Insight(
                    insight_id=f"insight_{uuid.uuid4().hex[:12]}",
                    insight_type=insight_type,
                    title=self._generate_title(merged_signal),
                    content=self._generate_content(merged_signal),
                    priority=priority,
                    created_at=datetime.now(),
                    signal_strength=SignalStrength.STRONG
                    if merged_signal.confidence >= 0.8
                    else SignalStrength.MODERATE,
                    affected_memories=[s.signal_id for s in qualified_signals],
                    confidence=merged_signal.confidence,
                    actionable=self._is_actionable(insight_type),
                    actions=self._generate_actions(merged_signal, insight_type),
                    metadata={"signal_count": len(qualified_signals)},
                )
                insights.append(insight)

        # 按优先级排序
        insights.sort(key=lambda x: x.priority.value, reverse=True)

        return insights

    def _merge_signals(
        self, signals: list[InsightSignal], insight_type: InsightType
    ) -> InsightSignal:
        """合并相似信号"""
        if len(signals) == 1:
            return signals[0]

        # 计算平均置信度
        avg_confidence: float = sum(s.confidence for s in signals) / len(signals)

        # 合并数据
        merged_data: dict[str, Any] = {}
        for signal in signals:
            merged_data.update(signal.data)

        return InsightSignal(
            signal_id=f"merged_{uuid.uuid4().hex[:8]}",
            signal_type=insight_type,
            confidence=avg_confidence,
            data=merged_data,
            raw_observation=" | ".join(s.raw_observation for s in signals[:3]),
        )

    def _determine_priority(
        self, signal: InsightSignal, insight_type: InsightType
    ) -> InsightPriority:
        """确定洞察优先级"""
        if signal.confidence >= 0.85:
            return InsightPriority.HIGH
        elif signal.confidence >= 0.7:
            return InsightPriority.MEDIUM
        else:
            return InsightPriority.LOW

    def _generate_title(self, signal: InsightSignal) -> str:
        """生成洞察标题"""
        type_titles: dict[InsightType, str] = {
            InsightType.USER_PREFERENCE: "用户偏好发现",
            InsightType.BEHAVIORAL_PATTERN: "行为模式识别",
            InsightType.BEST_PRACTICE: "最佳实践建议",
            InsightType.EFFICIENCY_OPPORTUNITY: "效率提升机会",
            InsightType.KNOWLEDGE_GAP: "知识缺口提示",
            InsightType.PROCESS_IMPROVEMENT: "流程改进建议",
            InsightType.ERROR_PREVENTION: "错误预防提醒",
            InsightType.EMOTIONAL_PATTERN: "情感模式洞察",
            InsightType.IDENTITY_EVOLUTION: "身份演化追踪",
        }
        return type_titles.get(signal.signal_type, "洞察发现")

    def _generate_content(self, signal: InsightSignal) -> str:
        """生成洞察内容"""
        return signal.raw_observation

    def _is_actionable(self, insight_type: InsightType) -> bool:
        """判断是否可执行"""
        actionable_types: set[InsightType] = {
            InsightType.BEST_PRACTICE,
            InsightType.EFFICIENCY_OPPORTUNITY,
            InsightType.PROCESS_IMPROVEMENT,
            InsightType.ERROR_PREVENTION,
        }
        return insight_type in actionable_types

    def _generate_actions(
        self, signal: InsightSignal, insight_type: InsightType
    ) -> list[str]:
        """生成行动建议"""
        actions: list[str] = []

        if insight_type == InsightType.USER_PREFERENCE:
            if "communication_style" in signal.data:
                actions.append(f"采用 {signal.data['communication_style']} 沟通风格")
            if "decision_style" in signal.data:
                actions.append(f"决策时参考 {signal.data['decision_style']} 模式")

        elif insight_type == InsightType.BEST_PRACTICE:
            if "tool" in signal.data:
                actions.append(f"优先使用 {signal.data['tool']} 工具")
            if "strategy_id" in signal.data:
                actions.append("应用已验证的问题解决策略")

        elif insight_type == InsightType.EFFICIENCY_OPPORTUNITY:
            if "combination" in signal.data:
                actions.append(f"尝试工具组合: {' → '.join(signal.data['combination'])}")

        elif insight_type == InsightType.KNOWLEDGE_GAP:
            actions.append("主动补充相关知识")
            actions.append("询问用户是否需要详细解释")

        return actions[:3]  # 最多返回3个行动建议

    def update_from_decision(
        self,
        decision: UserDecision,
        long_term_memory: LongTermMemoryContainer,
    ) -> dict[str, Any]:
        """
        从用户决策更新记忆

        Args:
            decision: 用户决策
            long_term_memory: 长期记忆容器

        Returns:
            更新结果
        """
        result: dict[str, Any] = {"updated": False, "changes": []}

        if decision.decision_type == DecisionType.TOOL_CHOICE:
            # 更新工具使用记录
            if long_term_memory.procedural:
                long_term_memory.procedural.data.tool_effectiveness_records
                result["changes"].append("tool_usage_updated")
                result["updated"] = True

        elif decision.decision_type == DecisionType.APPROACH_SELECTION:
            # 更新决策模式
            if long_term_memory.procedural:
                result["changes"].append("decision_pattern_updated")
                result["updated"] = True

        elif decision.decision_type == DecisionType.PREFERENCE_EXPRESSION:
            # 更新用户偏好
            if long_term_memory.user_profile:
                result["changes"].append("user_preference_updated")
                result["updated"] = True

        return result


class InsightModule:
    """
    洞察模块

    核心模块：负责生成和管理洞察，支持智能决策辅助
    """

    def __init__(self) -> None:
        """初始化洞察模块"""
        self._generator: InsightGenerator = InsightGenerator()
        self._active_insights: list[Insight] = []
        self._insight_history: list[Insight] = []

    def process(
        self,
        long_term_memory: LongTermMemoryContainer,
        context: ReconstructedContext,
    ) -> list[Insight]:
        """
        处理记忆和上下文，生成洞察

        Args:
            long_term_memory: 长期记忆
            context: 重构上下文

        Returns:
            洞察列表
        """
        # 生成信号
        signals: list[InsightSignal] = self._generator.generate_signals(
            long_term_memory, context
        )

        # 生成洞察
        insights: list[Insight] = self._generator.generate_insights(
            signals, context
        )

        # 更新活跃洞察
        self._active_insights = insights

        # 添加到历史
        self._insight_history.extend(insights)
        self._insight_history = self._insight_history[-100:]  # 保留最近100条

        return insights

    def get_active_insights(self) -> list[Insight]:
        """
        获取当前活跃洞察

        Returns:
            活跃洞察列表
        """
        return self._active_insights

    def get_insights_by_type(
        self, insight_type: InsightType
    ) -> list[Insight]:
        """
        按类型获取洞察

        Args:
            insight_type: 洞察类型

        Returns:
            该类型的洞察列表
        """
        return [
            insight
            for insight in self._active_insights
            if insight.insight_type == insight_type
        ]

    def get_high_priority_insights(self) -> list[Insight]:
        """
        获取高优先级洞察

        Returns:
            高优先级洞察列表
        """
        return [
            insight
            for insight in self._active_insights
            if insight.priority == InsightPriority.HIGH
        ]

    def record_decision(
        self,
        decision: UserDecision,
        long_term_memory: LongTermMemoryContainer,
    ) -> dict[str, Any]:
        """
        记录用户决策

        Args:
            decision: 用户决策
            long_term_memory: 长期记忆容器

        Returns:
            更新结果
        """
        return self._generator.update_from_decision(
            decision, long_term_memory
        )


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    "InsightGenerator",
    "InsightModule",
]
