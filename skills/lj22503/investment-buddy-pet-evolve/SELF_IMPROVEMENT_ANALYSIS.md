# investment-buddy-pet 自我进化改善空间分析

**分析时间**: 2026-04-14  
**分析对象**: investment-buddy-pet skill  
**当前版本**: v1.0.4

---

## 📊 当前状态评估

| 维度 | 得分 | 说明 |
|------|------|------|
| **功能性** | 28/30 | ✅ 核心功能完整 |
| **可靠性** | 25/30 | ⚠️ 数据准确性待优化 |
| **可用性** | 22/25 | ✅ 文档完整 |
| **安全性** | 14/15 | ✅ 合规检查完善 |
| **自我进化** | 15/30 | ⚠️ 缺少自动进化机制 |
| **总计** | **104/130** | ✅ 优秀，但有进化空间 |

---

## 🔍 自我进化改善空间

### P0: 数据准确性（影响用户体验）

**问题**: 茅台涨跌幅显示 `+1448.6%`（异常值）

**根因**:
1. data_layer 缓存数据可能过期
2. 缺少数据校验逻辑
3. 缺少异常值检测

**改进方案**:

```python
# scripts/master_summon.py
def _validate_quote(self, quote) -> bool:
    """验证行情数据是否合理"""
    change_pct = getattr(quote, 'change_pct', 0)
    
    # A 股涨跌幅限制：±10%（科创板/创业板 ±20%）
    if abs(change_pct) > 25:  # 留一些缓冲
        return False
    
    price = getattr(quote, 'price', 0)
    if price <= 0 or price > 100000:
        return False
    
    return True

def _invoke_master_skill(self, master, question, context):
    # 获取数据后验证
    if stock_codes:
        for code in stock_codes:
            quote = _api.get_quote(code)
            if self._validate_quote(quote):
                market_data["stocks"][code] = quote
            else:
                # 数据异常，尝试刷新缓存
                _api.clear_cache()
                quote = _api.get_quote(code)
                market_data["stocks"][code] = quote
```

**优先级**: P0（立即修复）

---

### P1: 用户反馈循环（缺少进化燃料）

**问题**: 没有收集用户反馈，无法从失败中学习

**改进方案**:

```python
# scripts/feedback_collector.py
class FeedbackCollector:
    """用户反馈收集器"""
    
    def __init__(self, feedback_dir: str = "data/feedback"):
        self.feedback_dir = Path(feedback_dir)
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
    
    def log_interaction(self, user_id: str, pet_type: str, 
                       question: str, response: str, 
                       feedback: str = None):
        """记录用户交互"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "pet_type": pet_type,
            "question": question,
            "response": response,
            "feedback": feedback,  # 用户评分/评价
            "helpful": None  # 用户是否觉得有用
        }
        
        # 写入日志文件
        log_file = self.feedback_dir / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def analyze_feedback(self, days: int = 7) -> Dict:
        """分析反馈数据，找出改进点"""
        # 读取最近 N 天的反馈
        feedback_logs = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            log_file = self.feedback_dir / f"{date}.jsonl"
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        feedback_logs.append(json.loads(line))
        
        # 分析模式
        patterns = {
            "low_helpful_count": 0,
            "common_questions": [],
            "pet_performance": {}
        }
        
        for log in feedback_logs:
            if log.get('helpful') == False:
                patterns["low_helpful_count"] += 1
            
            # 统计常见问题
            patterns["common_questions"].append(log['question'])
            
            # 统计宠物表现
            pet = log['pet_type']
            if pet not in patterns["pet_performance"]:
                patterns["pet_performance"][pet] = {"helpful": 0, "not_helpful": 0}
            
            if log.get('helpful') == True:
                patterns["pet_performance"][pet]["helpful"] += 1
            elif log.get('helpful') == False:
                patterns["pet_performance"][pet]["not_helpful"] += 1
        
        return patterns
```

**使用场景**:
1. 每次宠物消息后询问"这条消息对你有帮助吗？👍/👎"
2. 每周分析反馈数据，找出改进点
3. 自动更新 pet-configs.md 中的话术模板

**优先级**: P1（本周完成）

---

### P1: A/B 测试框架（优化话术）

**问题**: 无法确定哪种话术更有效

**改进方案**:

```python
# scripts/ab_test.py
class ABTestFramework:
    """A/B 测试框架"""
    
    def __init__(self):
        self.variants = {
            "greeting_morning": [
                "早上好！今天也是存坚果的一天！☀️",  # A
                "早安！新的一天，新的机会！🌰",  # B
                "早上好！一起变富的一天开始了！☀️"  # C
            ],
            "market_down_comfort": [
                "跌了 {pct}%... 我知道你有点担心。但历史上每次都涨回来了！",  # A
                "市场波动正常。坚持定投，时间会奖励耐心。",  # B
            ]
        }
    
    def get_variant(self, template_name: str, user_id: str) -> str:
        """根据用户 ID 分配变体"""
        variants = self.variants[template_name]
        # 使用用户 ID 的哈希值分配
        variant_idx = hash(user_id) % len(variants)
        return variants[variant_idx]
    
    def track_performance(self, template_name: str, variant_idx: int, 
                         is_helpful: bool):
        """追踪变体表现"""
        # 记录到文件
        pass
    
    def get_best_variant(self, template_name: str) -> int:
        """获取表现最好的变体"""
        # 分析数据，返回最佳变体索引
        pass
```

**使用场景**:
1. 不同用户看到不同话术
2. 追踪哪种话术更受用户欢迎
3. 自动切换到表现最好的话术

**优先级**: P1（本周完成）

---

### P2: 自动话术优化（基于反馈）

**问题**: 话术模板手动更新，效率低

**改进方案**:

```python
# scripts/speech_optimizer.py
class SpeechOptimizer:
    """话术自动优化器"""
    
    def __init__(self):
        self.feedback_collector = FeedbackCollector()
        self.ab_test = ABTestFramework()
    
    def optimize_template(self, template_name: str, pet_type: str):
        """自动优化话术模板"""
        # 1. 收集反馈数据
        patterns = self.feedback_collector.analyze_feedback(days=7)
        
        # 2. 找出低评分的话术
        low_helpful_threshold = 0.6  # 60% 以下认为需要优化
        
        # 3. 生成新话术（使用 LLM）
        # 4. A/B 测试新旧话术
        # 5. 自动切换到表现更好的话术
        pass
```

**优先级**: P2（下周完成）

---

### P2: 宠物人格自动调优

**问题**: 宠物人格参数（proactivity_level, verbosity_level 等）手动设置

**改进方案**:

```python
# scripts/personality_optimizer.py
class PersonalityOptimizer:
    """宠物人格自动调优"""
    
    def analyze_user_preference(self, user_id: str, pet_type: str) -> Dict:
        """分析用户偏好"""
        # 分析用户与宠物的交互历史
        # 找出用户喜欢的沟通风格
        
        return {
            "prefers_data": True,  # 喜欢数据
            "prefers_stories": False,  # 不喜欢故事
            "prefers_direct": True,  # 喜欢直接
            "morning_person": True,  # 早上活跃
        }
    
    def adjust_pet_personality(self, pet_type: str, user_preferences: Dict):
        """根据用户偏好调整宠物人格"""
        # 动态调整宠物的 proactivity_level, verbosity_level 等
        pass
```

**优先级**: P2（下周完成）

---

### P3: 技能自文档化

**问题**: 文档手动更新，容易过时

**改进方案**:

```python
# scripts/auto_doc.py
class AutoDocumenter:
    """技能自文档化"""
    
    def generate_usage_stats(self) -> Dict:
        """生成使用统计"""
        # 统计每个功能的使用频率
        # 统计常见错误
        # 统计用户反馈
        
        return {
            "most_used_feature": "宠物匹配",
            "least_used_feature": "召唤大师",
            "common_errors": ["数据库路径错误", "心跳重复启动"],
            "user_satisfaction": 0.85
        }
    
    def update_readme(self):
        """自动更新 README.md"""
        # 基于使用统计更新文档
        pass
```

**优先级**: P3（可选）

---

## 📋 改进优先级清单

| 优先级 | 改进项 | 预计工时 | 影响 |
|--------|-------|---------|------|
| **P0** | 数据准确性修复 | 1 小时 | 🔴 高 |
| **P1** | 用户反馈循环 | 4 小时 | 🟡 中 |
| **P1** | A/B 测试框架 | 4 小时 | 🟡 中 |
| **P2** | 自动话术优化 | 8 小时 | 🟡 中 |
| **P2** | 宠物人格自动调优 | 8 小时 | 🟢 低 |
| **P3** | 技能自文档化 | 4 小时 | 🟢 低 |

---

## 🎯 下一步行动

### 立即执行（今天）
- [ ] 修复数据准确性问题（P0）

### 本周完成
- [ ] 实现用户反馈循环（P1）
- [ ] 实现 A/B 测试框架（P1）

### 下周完成
- [ ] 实现自动话术优化（P2）
- [ ] 实现宠物人格自动调优（P2）

---

**分析者**: ant  
**分析时间**: 2026-04-14  
**下次分析**: 2026-04-21（一周后复查）
