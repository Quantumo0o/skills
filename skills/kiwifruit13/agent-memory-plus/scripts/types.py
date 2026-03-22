"""
Agent Memory System - 核心类型定义

=== 依赖与环境声明 ===
- 运行环境：Python >=3.9
- 直接依赖:
  * pydantic: >=2.0.0
    - 用途：数据模型验证和序列化
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

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ============================================================================
# 枚举类型
# ============================================================================


class MemoryType(str, Enum):
    """记忆类型枚举"""

    USER_PROFILE = "user_profile"
    PROCEDURAL = "procedural"
    NARRATIVE = "narrative"
    SEMANTIC = "semantic"
    EMOTIONAL = "emotional"


class HeatLevel(str, Enum):
    """冷热度层级"""

    HOT = "hot"
    WARM = "warm"
    COLD = "cold"


class ConflictType(str, Enum):
    """冲突类型"""

    FACTUAL_CONTRADICTION = "factual_contradiction"
    TEMPORAL_EVOLUTION = "temporal_evolution"
    CONTEXT_DEPENDENCY = "context_dependency"
    CONFIDENCE_CONFLICT = "confidence_conflict"


class ResolutionMode(str, Enum):
    """冲突解决模式"""

    LOGIC_DOMINANT = "logic_dominant"
    BALANCED = "balanced"
    NEUROTICISM_DOMINANT = "neuroticism_dominant"


class TriggerDimension(str, Enum):
    """激活器维度"""

    TEMPORAL = "temporal"
    SEMANTIC = "semantic"
    CONTEXTUAL = "contextual"
    EMOTIONAL = "emotional"
    CAUSAL = "causal"
    IDENTITY = "identity"


class SignalType(str, Enum):
    """洞察信号类型"""

    DECISION_SUPPORT = "decision_support"
    PROACTIVE_SUGGESTION = "proactive_suggestion"
    RISK_ALERT = "risk_alert"
    TIMING_HINT = "timing_hint"
    TOOL_RECOMMENDATION = "tool_recommendation"


class TaskType(str, Enum):
    """任务类型"""

    TECHNICAL_IMPLEMENTATION = "technical_implementation"
    CODE_DEBUGGING = "code_debugging"
    PRECISE_CALCULATION = "precise_calculation"
    CREATIVE_DESIGN = "creative_design"
    PROBLEM_SOLVING = "problem_solving"
    BRAINSTORMING = "brainstorming"
    DATA_ANALYSIS = "data_analysis"


# ============================================================================
# 基础数据结构
# ============================================================================


class TimestampMixin(BaseModel):
    """时间戳混入"""

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ConfidenceMixin(BaseModel):
    """置信度混入"""

    confidence: float = Field(ge=0.0, le=1.0, default=0.5)


class HeatMixin(BaseModel):
    """热度混入"""

    heat_score: float = Field(ge=0.0, le=100.0, default=50.0)
    heat_level: HeatLevel = Field(default=HeatLevel.WARM)
    last_accessed_at: datetime = Field(default_factory=datetime.now)
    access_count: int = Field(default=0)


# ============================================================================
# 用户画像类型
# ============================================================================


class TechnicalBackground(BaseModel):
    """技术背景"""

    domains: list[str] = Field(default_factory=list)
    expertise_level: str = Field(default="intermediate")


class CommunicationStyle(BaseModel):
    """沟通风格"""

    style: str = Field(default="balanced")
    preference: str = Field(default="detailed")
    dislike: list[str] = Field(default_factory=list)


class DecisionPattern(BaseModel):
    """决策模式"""

    type: str = Field(default="balanced")
    requires: str = Field(default="sufficient_evidence")
    focus: str = Field(default="balanced")


class UserProfileData(BaseModel):
    """用户画像数据"""

    identity: list[str] = Field(default_factory=list)
    technical_background: TechnicalBackground = Field(default_factory=TechnicalBackground)
    communication_style: CommunicationStyle = Field(default_factory=CommunicationStyle)
    decision_pattern: DecisionPattern = Field(default_factory=DecisionPattern)
    knowledge_blindspots: list[str] = Field(default_factory=list)
    version: int = Field(default=1)


class UserProfileMemory(BaseModel):
    """用户画像记忆"""

    memory_id: str
    memory_type: MemoryType = MemoryType.USER_PROFILE
    user_id: str
    data: UserProfileData
    heat: HeatMixin = Field(default_factory=HeatMixin)
    timestamp: TimestampMixin = Field(default_factory=TimestampMixin)


# ============================================================================
# 程序性记忆类型
# ============================================================================


class DecisionPatternRecord(BaseModel):
    """决策模式记录"""

    pattern_id: str
    trigger_condition: str
    workflow: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    usage_count: int = Field(default=0)
    success_rate: float = Field(ge=0.0, le=1.0, default=0.5)


class ProblemSolvingStrategy(BaseModel):
    """问题解决策略"""

    problem_type: str
    preferred_approach: str
    tools_preferred: list[str] = Field(default_factory=list)


class ToolUsageRecord(BaseModel):
    """工具使用记录"""

    record_id: str
    timestamp: datetime
    task_type: str
    tool_name: str
    effectiveness_score: float = Field(ge=0.0, le=1.0)
    outcome: str
    user_feedback: Optional[float] = None


class ToolOptimalContext(BaseModel):
    """工具最优场景"""

    optimal_scenarios: list[dict[str, Any]]
    avoid_scenarios: list[dict[str, Any]]


class ToolCombinationPattern(BaseModel):
    """工具组合模式"""

    sequence: list[str]
    task_pattern: str
    effectiveness_avg: float
    usage_count: int


class NeuroticismTendency(BaseModel):
    """神经质倾向"""

    score: float = Field(ge=-1.0, le=1.0, default=0.0)
    derived_from: list[str] = Field(default_factory=list)


class ProceduralMemoryData(BaseModel):
    """程序性记忆数据"""

    decision_patterns: list[DecisionPatternRecord] = Field(default_factory=list)
    problem_solving_strategies: list[ProblemSolvingStrategy] = Field(default_factory=list)
    tool_usage_patterns: dict[str, Any] = Field(default_factory=dict)
    tool_effectiveness_records: list[ToolUsageRecord] = Field(default_factory=list)
    tool_optimal_contexts: dict[str, ToolOptimalContext] = Field(default_factory=dict)
    tool_combination_patterns: list[ToolCombinationPattern] = Field(default_factory=list)
    operation_preferences: dict[str, Any] = Field(default_factory=dict)
    neuroticism_tendency: NeuroticismTendency = Field(default_factory=NeuroticismTendency)
    cross_category_insights: list[dict[str, Any]] = Field(default_factory=list)


class ProceduralMemory(BaseModel):
    """程序性记忆"""

    memory_id: str
    memory_type: MemoryType = MemoryType.PROCEDURAL
    user_id: str
    data: ProceduralMemoryData
    heat: HeatMixin = Field(default_factory=HeatMixin)
    timestamp: TimestampMixin = Field(default_factory=TimestampMixin)


# ============================================================================
# 叙事记忆类型
# ============================================================================


class GrowthMilestone(BaseModel):
    """成长节点"""

    timestamp: datetime
    event: str
    significance: str
    importance_score: float = Field(ge=0.0, le=1.0)


class IdentityEvolution(BaseModel):
    """身份演化"""

    timestamp: datetime
    from_identity: str
    to_identity: str
    trigger: str


class NarrativeMemoryData(BaseModel):
    """叙事记忆数据"""

    current_identity: list[str] = Field(default_factory=list)
    growth_milestones: list[GrowthMilestone] = Field(default_factory=list)
    identity_evolution: list[IdentityEvolution] = Field(default_factory=list)
    continuous_concerns: list[dict[str, Any]] = Field(default_factory=list)
    narrative_content: str = Field(default="")


class NarrativeMemory(BaseModel):
    """叙事记忆"""

    memory_id: str
    memory_type: MemoryType = MemoryType.NARRATIVE
    user_id: str
    data: NarrativeMemoryData
    heat: HeatMixin = Field(default_factory=HeatMixin)
    timestamp: TimestampMixin = Field(default_factory=TimestampMixin)


# ============================================================================
# 语义记忆类型
# ============================================================================


class ConceptDefinition(BaseModel):
    """概念定义"""

    concept: str
    definition: str
    attributes: dict[str, str]
    related_concepts: list[str]
    usage_count: int = Field(default=0)
    confidence: float = Field(ge=0.0, le=1.0)


class KnowledgeEntity(BaseModel):
    """知识实体"""

    entity: str
    entity_type: str
    relationships: list[dict[str, Any]]


class Principle(BaseModel):
    """原则"""

    principle: str
    applicability: str
    evidence_support: float


class SemanticMemoryData(BaseModel):
    """语义记忆数据"""

    core_concepts: list[ConceptDefinition] = Field(default_factory=list)
    knowledge_entities: list[KnowledgeEntity] = Field(default_factory=list)
    principles: list[Principle] = Field(default_factory=list)


class SemanticMemory(BaseModel):
    """语义记忆"""

    memory_id: str
    memory_type: MemoryType = MemoryType.SEMANTIC
    user_id: str
    data: SemanticMemoryData
    heat: HeatMixin = Field(default_factory=HeatMixin)
    timestamp: TimestampMixin = Field(default_factory=TimestampMixin)


# ============================================================================
# 情感记忆类型
# ============================================================================


class EmotionState(BaseModel):
    """情绪状态"""

    timestamp: datetime
    emotion_type: str
    intensity: float = Field(ge=0.0, le=1.0)
    trigger_context: str
    topic: str
    decay_factor: float = Field(default=0.98)


class AttitudeTendency(BaseModel):
    """态度倾向"""

    topic: str
    attitude: str
    direction: str
    confidence: float


class SatisfactionRecord(BaseModel):
    """满意度记录"""

    timestamp: datetime
    satisfaction_level: float = Field(ge=0.0, le=1.0)
    trigger_factors: list[str]
    concerns: list[str]
    overall_progress: str


class EmotionalMemoryData(BaseModel):
    """情感记忆数据"""

    emotion_states: list[EmotionState] = Field(default_factory=list)
    attitude_tendencies: list[AttitudeTendency] = Field(default_factory=list)
    satisfaction_records: list[SatisfactionRecord] = Field(default_factory=list)


class EmotionalMemory(BaseModel):
    """情感记忆"""

    memory_id: str
    memory_type: MemoryType = MemoryType.EMOTIONAL
    user_id: str
    data: EmotionalMemoryData
    heat: HeatMixin = Field(default_factory=HeatMixin)
    timestamp: TimestampMixin = Field(default_factory=TimestampMixin)


# ============================================================================
# 感知记忆类型
# ============================================================================


class ConversationTurn(BaseModel):
    """对话轮次"""

    role: str
    content: str
    timestamp: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class TaskState(BaseModel):
    """任务状态"""

    current_topic: str = Field(default="")
    pending_questions: list[str] = Field(default_factory=list)
    context_anchors: list[str] = Field(default_factory=list)


class TemporaryContext(BaseModel):
    """临时上下文"""

    mentioned_concepts: list[str] = Field(default_factory=list)
    implicit_assumptions: list[str] = Field(default_factory=list)


class PerceptionMemoryData(BaseModel):
    """感知记忆数据"""

    session_id: str
    conversation_history: list[ConversationTurn] = Field(default_factory=list)
    task_state: TaskState = Field(default_factory=TaskState)
    temporary_context: TemporaryContext = Field(default_factory=TemporaryContext)


class PerceptionMemory(BaseModel):
    """感知记忆"""

    memory_id: str
    user_id: str
    data: PerceptionMemoryData
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None


# ============================================================================
# 情境感知类型
# ============================================================================


class CurrentTask(BaseModel):
    """当前任务"""

    task_type: TaskType
    task_complexity: str = Field(default="medium")
    task_phase: str = Field(default="exploration")
    implicit_requirements: list[str] = Field(default_factory=list)


class UserCurrentState(BaseModel):
    """用户当前状态"""

    technical_level: str = Field(default="intermediate")
    current_focus: str = Field(default="")
    mental_model: str = Field(default="")
    decision_style: str = Field(default="balanced")


class ContextAnchors(BaseModel):
    """上下文锚点"""

    temporal: str = Field(default="")
    semantic: str = Field(default="")
    narrative: str = Field(default="")
    emotional: str = Field(default="")


class SituationAwareness(BaseModel):
    """情境感知"""

    timestamp: datetime = Field(default_factory=datetime.now)
    current_task: CurrentTask
    user_current_state: UserCurrentState
    context_anchors: ContextAnchors


# ============================================================================
# 激活相关类型
# ============================================================================


class ActivationSource(BaseModel):
    """激活来源"""

    dimension: TriggerDimension
    score: float = Field(ge=0.0, le=1.0)


class ActivatedMemory(BaseModel):
    """激活的记忆"""

    memory_id: str
    memory_type: MemoryType
    content_summary: str
    triggered_by: list[TriggerDimension]
    relevance_score: float = Field(ge=0.0, le=1.0)
    heat_level: HeatLevel
    conflicts: list[str] = Field(default_factory=list)
    activation_sources: list[ActivationSource] = Field(default_factory=list)


class ActivationResult(BaseModel):
    """激活结果"""

    activated_memories: list[ActivatedMemory]
    total_count: int
    unique_count: int
    conflicts_detected: int
    activation_coverage: list[TriggerDimension]


# ============================================================================
# 上下文重构类型
# ============================================================================


class TaskContextLayer(BaseModel):
    """任务上下文层"""

    current_task: str
    task_phase: str
    implicit_requirements: list[str]


class UserStateLayer(BaseModel):
    """用户状态层"""

    user_profile_core: dict[str, Any]
    current_focus: str
    decision_style: str
    neuroticism_tendency: float


class ActivatedExperiencesLayer(BaseModel):
    """激活经验层"""

    relevant_patterns: list[dict[str, Any]]
    success_stories: list[dict[str, Any]]
    failure_lessons: list[dict[str, Any]]
    tool_recommendations: list[dict[str, Any]]


class KnowledgeContextLayer(BaseModel):
    """知识上下文层"""

    key_concepts: list[dict[str, Any]]
    concept_relations: list[dict[str, Any]]
    principles: list[str]


class EmotionalContextLayer(BaseModel):
    """情感上下文层"""

    current_emotion: str
    emotional_trend: str
    satisfaction_level: float


class NarrativeAnchorLayer(BaseModel):
    """叙事锚点层"""

    growth_milestones: list[dict[str, Any]]
    identity_evolution: list[str]
    continuous_concerns: list[str]


class ReconstructedContext(BaseModel):
    """重构上下文"""

    task_context: TaskContextLayer
    user_state: UserStateLayer
    activated_experiences: ActivatedExperiencesLayer
    knowledge_context: KnowledgeContextLayer
    emotional_context: EmotionalContextLayer
    narrative_anchor: NarrativeAnchorLayer
    conflicts_handled: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# 洞察信号类型
# ============================================================================


class FitScores(BaseModel):
    """契合度分数"""

    user_profile: float = Field(ge=0.0, le=1.0)
    procedural: float = Field(ge=0.0, le=1.0)
    context: float = Field(ge=0.0, le=1.0)
    emotional: float = Field(ge=0.0, le=1.0)
    overall: float = Field(ge=0.0, le=1.0)


class DecisionSupportSignal(BaseModel):
    """决策支持信号"""

    signal_id: str
    signal_type: SignalType = SignalType.DECISION_SUPPORT
    decision_point: str
    options: list[str]
    recommendation: str
    trade_offs: str
    confidence: float = Field(ge=0.0, le=1.0)
    fit_scores: FitScores


class ToolRecommendationSignal(BaseModel):
    """工具推荐信号"""

    signal_id: str
    signal_type: SignalType = SignalType.TOOL_RECOMMENDATION
    recommended_tool: str
    reasons: list[str]
    combination_opportunity: Optional[str] = None
    cautions: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    fit_scores: FitScores


class RiskAlertSignal(BaseModel):
    """风险提示信号"""

    signal_id: str
    signal_type: SignalType = SignalType.RISK_ALERT
    risk_type: str
    risk_description: str
    potential_impact: str
    mitigation: str
    urgency: str
    confidence: float = Field(ge=0.0, le=1.0)
    fit_scores: FitScores


class TimingHintSignal(BaseModel):
    """时机提示信号"""

    signal_id: str
    signal_type: SignalType = SignalType.TIMING_HINT
    timing_type: str
    hint: str
    reason: str
    confidence: float = Field(ge=0.0, le=1.0)
    fit_scores: FitScores


class InsightSignalUnion(BaseModel):
    """洞察信号联合类型"""

    signal: (
        DecisionSupportSignal
        | ToolRecommendationSignal
        | RiskAlertSignal
        | TimingHintSignal
    )


class ContextEnhancement(BaseModel):
    """上下文增强"""

    insight_signals: list[InsightSignalUnion]
    total_signals: int
    total_fit_score: float


# ============================================================================
# 冲突解决类型
# ============================================================================


class MemoryConflict(BaseModel):
    """记忆冲突"""

    conflict_id: str
    conflict_type: ConflictType
    memory_ids: list[str]
    description: str
    detected_at: datetime = Field(default_factory=datetime.now)


class ConflictResolution(BaseModel):
    """冲突解决结果"""

    conflict: MemoryConflict
    resolution_mode: ResolutionMode
    logic_score: float
    neuroticism_score: float
    winner_memory_id: str
    alternative_memory_id: Optional[str] = None
    reasoning: str


# ============================================================================
# 状态捕捉类型
# ============================================================================


class ModuleState(BaseModel):
    """模块状态"""

    module_name: str
    status: str
    last_update: datetime = Field(default_factory=datetime.now)
    metrics: dict[str, Any] = Field(default_factory=dict)


class GlobalState(BaseModel):
    """全局状态"""

    state_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: str
    module_states: dict[str, ModuleState]
    cross_module_signals: dict[str, Any] = Field(default_factory=dict)


class AsyncTask(BaseModel):
    """异步任务"""

    task_id: str
    task_type: str
    payload: dict[str, Any]
    priority: str = Field(default="medium")
    submitted_at: datetime = Field(default_factory=datetime.now)
    retry_count: int = Field(default=0)
    max_retries: int = Field(default=3)


# ============================================================================
# 长期记忆统一容器
# ============================================================================


class LongTermMemoryContainer(BaseModel):
    """长期记忆统一容器"""

    user_id: str
    user_profile: Optional[UserProfileMemory] = None
    procedural: Optional[ProceduralMemory] = None
    narrative: Optional[NarrativeMemory] = None
    semantic: Optional[SemanticMemory] = None
    emotional: Optional[EmotionalMemory] = None
    last_updated: datetime = Field(default_factory=datetime.now)


# ============================================================================
# 导出类型
# ============================================================================


__all__ = [
    # 枚举
    "MemoryType",
    "HeatLevel",
    "ConflictType",
    "ResolutionMode",
    "TriggerDimension",
    "SignalType",
    "TaskType",
    # 混入
    "TimestampMixin",
    "ConfidenceMixin",
    "HeatMixin",
    # 用户画像
    "TechnicalBackground",
    "CommunicationStyle",
    "DecisionPattern",
    "UserProfileData",
    "UserProfileMemory",
    # 程序性记忆
    "DecisionPatternRecord",
    "ProblemSolvingStrategy",
    "ToolUsageRecord",
    "ToolOptimalContext",
    "ToolCombinationPattern",
    "NeuroticismTendency",
    "ProceduralMemoryData",
    "ProceduralMemory",
    # 叙事记忆
    "GrowthMilestone",
    "IdentityEvolution",
    "NarrativeMemoryData",
    "NarrativeMemory",
    # 语义记忆
    "ConceptDefinition",
    "KnowledgeEntity",
    "Principle",
    "SemanticMemoryData",
    "SemanticMemory",
    # 情感记忆
    "EmotionState",
    "AttitudeTendency",
    "SatisfactionRecord",
    "EmotionalMemoryData",
    "EmotionalMemory",
    # 感知记忆
    "ConversationTurn",
    "TaskState",
    "TemporaryContext",
    "PerceptionMemoryData",
    "PerceptionMemory",
    # 情境感知
    "CurrentTask",
    "UserCurrentState",
    "ContextAnchors",
    "SituationAwareness",
    # 激活
    "ActivationSource",
    "ActivatedMemory",
    "ActivationResult",
    # 上下文重构
    "TaskContextLayer",
    "UserStateLayer",
    "ActivatedExperiencesLayer",
    "KnowledgeContextLayer",
    "EmotionalContextLayer",
    "NarrativeAnchorLayer",
    "ReconstructedContext",
    # 洞察信号
    "FitScores",
    "DecisionSupportSignal",
    "ToolRecommendationSignal",
    "RiskAlertSignal",
    "TimingHintSignal",
    "InsightSignalUnion",
    "ContextEnhancement",
    # 冲突
    "MemoryConflict",
    "ConflictResolution",
    # 状态
    "ModuleState",
    "GlobalState",
    "AsyncTask",
    # 容器
    "LongTermMemoryContainer",
]
