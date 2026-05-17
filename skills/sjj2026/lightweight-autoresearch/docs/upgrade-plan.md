# 轻量级自主优化技能升级计划

## 对比分析：达尔文 vs 我们的轻量级版本

### 达尔文的核心优势（需要学习）

| 特性 | 达尔文 | 我们的轻量级 | 升级必要性 |
|------|--------|-------------|-----------|
| **独立评分** | ✅ 用子agent评分 | ❌ 自己改自己评 | ⭐⭐⭐ 核心 |
| **人在回路** | ✅ 每个skill优化完暂停 | ❌ 全自动 | ⭐⭐⭐ 核心 |
| **测试Prompt** | ✅ Phase 0.5设计 | ❌ 没有 | ⭐⭐⭐ 核心 |
| **效果验证** | ✅ 实测表现25分 | ❌ 只有结构分 | ⭐⭐⭐ 核心 |
| 棘轮机制 | ✅ | ✅ | - |
| 可视化 | ❌ | ✅ HTML报告 | 我们的优势 |

---

## 升级方案

### Phase 1: 测试Prompt设计模块

**借鉴达尔文Phase 0.5**

```python
# 新增模块：test_prompt_designer.py

class TestPromptDesigner:
    """测试Prompt设计器"""
    
    def design_test_prompts(self, skill_md: str) -> List[Dict]:
        """
        为技能设计2-3个测试prompt
        
        Args:
            skill_md: SKILL.md内容
            
        Returns:
            [
                {
                    "id": 1,
                    "prompt": "用户会说的话",
                    "expected": "期望输出的简短描述",
                    "scenario": "happy_path"  # 或 complex_case
                }
            ]
        """
        # 1. 理解skill做什么
        skill_intent = self._parse_intent(skill_md)
        
        # 2. 设计测试场景
        test_prompts = []
        
        # 场景1: 最典型的使用场景（happy path）
        test_prompts.append({
            "id": 1,
            "prompt": self._design_happy_path(skill_intent),
            "expected": self._define_expectation(skill_intent, "happy"),
            "scenario": "happy_path"
        })
        
        # 场景2: 稍复杂或有歧义的场景
        test_prompts.append({
            "id": 2,
            "prompt": self._design_complex_case(skill_intent),
            "expected": self._define_expectation(skill_intent, "complex"),
            "scenario": "complex_case"
        })
        
        return test_prompts
```

**使用流程**：
1. 读取SKILL.md，理解它做什么
2. 自动生成2-3个测试prompt
3. 展示给用户确认（人在回路）
4. 确认后保存到 `skill目录/test-prompts.json`

---

### Phase 2: 独立评分机制

**借鉴达尔文的"独立评分"原则**

```python
# 升级模块：independent_scorer.py

class IndependentScorer:
    """独立评分器"""
    
    def __init__(self, skill_path: str, test_prompts: List[Dict]):
        self.skill_path = skill_path
        self.test_prompts = test_prompts
        
    def evaluate_with_baseline(self) -> Dict:
        """
        独立评估：带skill vs baseline对比
        
        Returns:
            {
                "with_skill": {"score": 85, "outputs": [...]},
                "baseline": {"score": 72, "outputs": [...]},
                "improvement": +13,
                "dimension_8_score": 8.5  # 实测表现维度分数
            }
        """
        # 1. 带skill执行测试prompt
        with_skill_results = self._run_with_skill()
        
        # 2. 不带skill执行测试prompt（baseline）
        baseline_results = self._run_baseline()
        
        # 3. 对比输出质量
        comparison = self._compare_outputs(with_skill_results, baseline_results)
        
        # 4. 计算维度8分数（实测表现，25分权重）
        dimension_8_score = self._calculate_dimension_8(comparison)
        
        return {
            "with_skill": with_skill_results,
            "baseline": baseline_results,
            "improvement": comparison["improvement"],
            "dimension_8_score": dimension_8_score
        }
    
    def _run_with_skill(self) -> Dict:
        """
        带skill执行测试prompt
        
        关键：这个方法应该调用独立的子进程或子agent
        避免在同一上下文中修改和评分
        """
        # 实现方式1：调用子进程
        # 实现方式2：调用外部API（如果有）
        # 实现方式3：使用subprocess隔离环境
        
        results = []
        for test_prompt in self.test_prompts:
            # 调用独立评分脚本
            output = self._call_independent_evaluator(
                skill_path=self.skill_path,
                prompt=test_prompt["prompt"],
                mode="with_skill"
            )
            results.append(output)
        
        return {"score": self._score_outputs(results), "outputs": results}
    
    def _run_baseline(self) -> Dict:
        """不带skill执行测试prompt（baseline）"""
        results = []
        for test_prompt in self.test_prompts:
            output = self._call_independent_evaluator(
                skill_path=None,  # 不带skill
                prompt=test_prompt["prompt"],
                mode="baseline"
            )
            results.append(output)
        
        return {"score": self._score_outputs(results), "outputs": results}
```

**关键设计**：
- 使用子进程或外部调用实现独立评分
- 避免在同一上下文中修改和评分
- 记录评估模式（`full_test` 或 `dry_run`）

---

### Phase 3: 人在回路机制

**借鉴达尔文的"每个skill优化完暂停"**

```python
# 升级模块：human_in_loop.py

class HumanInLoopController:
    """人在回路控制器"""
    
    def __init__(self):
        self.paused = False
        self.current_skill = None
        self.modifications = []
        
    def pause_for_review(self, skill_name: str, modifications: Dict):
        """
        暂停优化，等待用户确认
        
        Args:
            skill_name: 技能名称
            modifications: 改动摘要
                {
                    "git_diff": "...",
                    "score_change": {"before": 72, "after": 85},
                    "test_outputs_comparison": "...",
                    "suggestions": ["保留", "回滚", "继续优化"]
                }
        """
        self.paused = True
        self.current_skill = skill_name
        self.modifications = modifications
        
        # 展示给用户
        self._display_modifications()
        
        # 等待用户输入
        user_decision = self._wait_for_user_input()
        
        return user_decision
    
    def _display_modifications(self):
        """展示改动摘要"""
        print(f"\n{'='*60}")
        print(f"技能优化完成：{self.current_skill}")
        print(f"{'='*60}\n")
        
        print("📊 分数变化：")
        before = self.modifications["score_change"]["before"]
        after = self.modifications["score_change"]["after"]
        delta = after - before
        print(f"  改前：{before}分")
        print(f"  改后：{after}分")
        print(f"  提升：+{delta}分 ({delta/before*100:.1f}%)\n")
        
        print("📝 改动内容：")
        print(self.modifications["git_diff"][:500] + "...\n")
        
        print("🧪 测试对比：")
        print(self.modifications["test_outputs_comparison"][:300] + "...\n")
        
        print("💡 建议：")
        for i, suggestion in enumerate(self.modifications["suggestions"], 1):
            print(f"  {i}. {suggestion}")
        
        print(f"\n{'='*60}")
    
    def _wait_for_user_input(self) -> str:
        """等待用户输入"""
        while self.paused:
            decision = input("\n请选择操作（保留/回滚/继续优化）：").strip()
            
            if decision in ["保留", "keep", "1"]:
                self.paused = False
                return "keep"
            elif decision in ["回滚", "revert", "2"]:
                self.paused = False
                return "revert"
            elif decision in ["继续优化", "continue", "3"]:
                self.paused = False
                return "continue"
            else:
                print("无效输入，请选择：保留/回滚/继续优化")
        
        return "keep"
```

---

### Phase 4: 整合到评估体系

**借鉴达尔文的8维度评分**

```python
# 升级 evaluate.py

class ComprehensiveEvaluatorV2:
    """综合评估器 V2 - 借鉴达尔文8维度"""
    
    def evaluate(self) -> Dict:
        """综合评估技能（8维度）"""
        results = {
            "total_score": 0,
            "dimensions": {},
            "weaknesses": [],
            "suggestions": []
        }
        
        # === 结构维度（60分）===
        
        # 维度1: Frontmatter质量（8分）
        results["dimensions"]["frontmatter"] = self._evaluate_frontmatter()
        
        # 维度2: 工作流清晰度（15分）
        results["dimensions"]["workflow_clarity"] = self._evaluate_workflow()
        
        # 维度3: 边界条件覆盖（10分）
        results["dimensions"]["boundary_conditions"] = self._evaluate_boundaries()
        
        # 维度4: 检查点设计（7分）
        results["dimensions"]["checkpoints"] = self._evaluate_checkpoints()
        
        # 维度5: 指令具体性（15分）
        results["dimensions"]["instruction_specificity"] = self._evaluate_instructions()
        
        # 维度6: 资源整合度（5分）
        results["dimensions"]["resource_integration"] = self._evaluate_resources()
        
        # === 效果维度（40分）===
        
        # 维度7: 整体架构（15分）
        results["dimensions"]["architecture"] = self._evaluate_architecture()
        
        # 维度8: 实测表现（25分）⭐ 最高权重
        results["dimensions"]["actual_performance"] = self._evaluate_performance()
        
        # 计算总分
        total = sum(d["score"] for d in results["dimensions"].values())
        results["total_score"] = total
        
        return results
    
    def _evaluate_performance(self) -> Dict:
        """
        维度8：实测表现（25分）
        
        关键：使用独立评分器
        """
        # 调用独立评分器
        scorer = IndependentScorer(self.skill_path, self.test_prompts)
        performance_results = scorer.evaluate_with_baseline()
        
        # 计算分数
        score = performance_results["dimension_8_score"] * 2.5  # 转换为25分制
        
        return {
            "score": score,
            "max_score": 25,
            "details": {
                "with_skill_score": performance_results["with_skill"]["score"],
                "baseline_score": performance_results["baseline"]["score"],
                "improvement": performance_results["improvement"],
                "eval_mode": "full_test"  # 或 "dry_run"
            }
        }
```

---

## 升级后的完整流程

### Phase 0: 初始化
1. 确认优化范围
2. 创建git分支
3. 初始化results.tsv

### Phase 0.5: 测试Prompt设计 ⭐ 新增
1. 为每个skill设计2-3个测试prompt
2. **展示给用户确认**
3. 保存到 `test-prompts.json`

### Phase 1: 基线评估
1. 结构评分（维度1-7）
2. **效果评分（维度8：独立评分）** ⭐ 新增
3. 计算加权总分
4. 记录到results.tsv

### Phase 2: 优化循环
1. 找得分最低维度
2. 针对性改进
3. **独立子进程重新评分** ⭐ 新增
4. 决策：保留或回滚
5. 记录到results.tsv

### Phase 2.5: **人在回路检查点** ⭐ 新增
- 展示git diff
- 展示分数变化
- 展示测试输出对比
- **等待用户确认**

### Phase 3: 汇总报告
- 生成优化报告
- 记录改进统计

---

## 实现计划

### 第一阶段：测试Prompt设计（1天）
- [ ] 创建 `test_prompt_designer.py`
- [ ] 实现自动生成测试prompt
- [ ] 实现用户确认机制

### 第二阶段：独立评分（1天）
- [ ] 创建 `independent_scorer.py`
- [ ] 实现子进程隔离评分
- [ ] 实现baseline对比

### 第三阶段：人在回路（1天）
- [ ] 创建 `human_in_loop.py`
- [ ] 实现暂停和等待机制
- [ ] 实现用户交互界面

### 第四阶段：整合测试（1天）
- [ ] 升级 `evaluate.py`
- [ ] 整合所有模块
- [ ] 测试完整流程

---

## 预期效果

升级后的轻量级版本将具备：

1. ✅ **独立评分** - 避免自己改自己评的偏差
2. ✅ **人在回路** - 关键决策由用户确认
3. ✅ **效果验证** - 实测表现占比25分
4. ✅ **测试Prompt** - 每个skill有明确的测试场景
5. ✅ **可视化** - 保留HTML报告优势

---

*创建时间：2026-04-14 17:36*
*借鉴来源：达尔文.skill (alchaincyf/darwin-skill)*
