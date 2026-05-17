# 轻量级自主优化技能 V2 升级规范

## 升级目标

借鉴达尔文.skill的3大核心优势：
1. **独立评分机制** - 用子agent或子进程评分，避免自己改自己评
2. **人在回路** - 每个skill优化完后暂停，等待用户确认
3. **测试Prompt + 效果验证** - Phase 0.5设计测试prompt，维度8实测表现

---

## 新增模块

### 1. independent_scorer.py - 独立评分器

**职责**：
- 独立于主agent进行评分
- 使用子进程隔离环境
- 支持full_test和dry_run两种模式

**接口**：
```python
class IndependentScorer:
    def __init__(self, skill_path: str, test_prompts: List[Dict])
    
    def evaluate_with_baseline(self) -> Dict:
        """
        独立评估：带skill vs baseline对比
        
        Returns:
            {
                "with_skill": {"score": 85, "outputs": [...]},
                "baseline": {"score": 72, "outputs": [...]},
                "improvement": +13,
                "dimension_8_score": 8.5
            }
        """
```

---

### 2. human_in_loop.py - 人在回路控制器

**职责**：
- 管理优化暂停和继续
- 展示改动摘要
- 等待用户确认

**接口**：
```python
class HumanInLoopController:
    def pause_for_review(self, skill_name: str, modifications: Dict) -> str:
        """
        暂停优化，等待用户确认
        
        Args:
            skill_name: 技能名称
            modifications: 改动摘要
            
        Returns:
            用户决策：keep/revert/continue
        """
```

---

### 3. test_prompt_designer.py - 测试Prompt设计器

**职责**：
- 自动为技能设计测试prompt
- 覆盖happy path和复杂场景
- 生成test-prompts.json

**接口**：
```python
class TestPromptDesigner:
    def design_test_prompts(self, skill_md: str) -> List[Dict]:
        """
        为技能设计2-3个测试prompt
        
        Returns:
            [
                {
                    "id": 1,
                    "prompt": "用户会说的话",
                    "expected": "期望输出描述",
                    "scenario": "happy_path"
                }
            ]
        """
```

---

## 升级现有模块

### 4. evaluate.py V2 - 8维度评估

**升级内容**：
- 从4维度升级到8维度
- 加入维度8（实测表现）
- 调用IndependentScorer进行独立评分

**新接口**：
```python
class ComprehensiveEvaluatorV2:
    def evaluate(self) -> Dict:
        """综合评估技能（8维度）"""
        
        # 维度1-7：结构评分
        # 维度8：实测表现（调用IndependentScorer）
        
        return {
            "total_score": 76.6,
            "dimensions": {...},
            "weaknesses": [...],
            "suggestions": [...]
        }
```

---

## 升级后的完整流程

### Phase 0: 初始化
- 确认优化范围
- 创建git分支
- 初始化results.tsv

### Phase 0.5: 测试Prompt设计 ⭐ 新增
- 调用TestPromptDesigner
- 为每个skill设计2-3个测试prompt
- **展示给用户确认**

### Phase 1: 基线评估
- 结构评分（维度1-7）
- **效果评分（维度8：调用IndependentScorer）** ⭐ 新增
- **暂停等用户确认** ⭐ 新增

### Phase 2: 优化循环
- 找最低维度
- 针对性改进
- **调用IndependentScorer重新评分** ⭐ 新增
- 决策：keep/revert
- **HumanInLoopController暂停** ⭐ 新增

### Phase 3: 汇总报告
- 生成优化报告
- 记录改进统计

---

## 约束规则

1. **保持向后兼容** - V1接口仍然可用
2. **模块化设计** - 每个新模块独立
3. **可配置** - 可以关闭人在回路（自动化模式）
4. **评估模式标注** - 记录full_test或dry_run

---

## 实现优先级

**P0（必须）**：
1. ✅ test_prompt_designer.py - Phase 0.5依赖
2. ✅ independent_scorer.py - 维度8依赖
3. ✅ evaluate.py V2 - 8维度评估

**P1（重要）**：
4. ✅ human_in_loop.py - 人在回路

**P2（可选）**：
5. 升级run_loop.py整合所有模块

---

## 预期效果

升级后的轻量级版本将具备：
1. ✅ **独立评分** - 避免自己改自己评的偏差
2. ✅ **人在回路** - 关键决策由用户确认
3. ✅ **效果验证** - 实测表现占比25分
4. ✅ **测试Prompt** - 每个skill有明确的测试场景
5. ✅ **达尔文兼容** - 与达尔文.skill评估体系一致

---

*创建时间：2026-04-14 21:42*
*版本：V2规范*
