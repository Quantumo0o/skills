# afrexai Insurance Benchmarks
# Version 1.1 | Updated: 2026-04-05 | Added: threshold confirmation note (v1.1)

> ⚠️ **免责声明（必读）**
> 本文件为**行业基准参考值**，不是贵公司 InsureMO 的实际配置值。
> 所有 threshold、ratio、flag 必须用客户实际系统配置或需求文档中的参数替换后才能用于 UAT 场景或合规分析。
>
> **使用前必须向客户或产品负责人确认以下关键参数：**
> - Claims auto-adjudication threshold（auto-approve 上限）
> - SIU referral criteria（欺诈报送触发条件）
> - Combined Ratio / Loss Ratio 目标值
> - UW referral trigger conditions（核保转介条件）
> - 各险种准备金估算基准
>
> **违反此原则的风险：** 以行业基准值替代实际配置值 → UAT 测错边界、合规结论偏差、系统配置与测试结果不一致。

---

> 本文件整合自 afrexai-insurance-automation skill，提供保险行业基准数据，供 Agent 3/7/8 参考使用。
> 不替代现有 InsureMO KB，仅作为行业基准对照。

---

## 1. Claims Severity Triage（理赔分诊基准）

来源: afrexai-insurance-automation §2 Claims Processing Pipeline

### 三级分诊模型

| Severity | 阈值 | 处理方式 | UAT 场景标记 |
|---------|------|---------|------------|
| 🟢 **Green** | < $2,000 | 自动批准（Auto-approve） | UAT-CLM-GREEN |
| 🟡 **Yellow** | $2,000 – $25,000 | 理算师审查（Adjuster review） | UAT-CLM-YELLOW |
| 🔴 **Red** | > $25,000 **或** 欺诈指标触发 | SIU 转介（SIU referral） | UAT-CLM-RED |

### SIU 欺诈指标（15个红旗）

以下任一触发则升为 Red：
1. 事故发生后延迟报案 > 30天
2. 被保险人在多个保单下提出类似索赔
3. 理赔金额接近保单限额
4. 损失发生在保单生效后 60 天内（等待期刚过）
5. 索赔描述与现场证据不一致
6. 被保险人拒绝医疗检查或文书核查
7. 索赔表格有篡改痕迹
8. 损失发生在法律诉讼期间
9. 高风险职业 + 高保额组合
10. 多次变更受益人后短期内索赔
11. 理赔金额呈整数（如精确 $9,999）
12. 第三方责任案件中对方否认知情
13. 被保险人信用评分 < 550
14. 索赔历史：过去 3 年 > 2 次索赔
15. 保险期间中断后恢复保单且短期内索赔

### 准备金估算基准（Initial Reserve）

| 险种 | 估算基准 |
|------|---------|
| 汽车险 | 案件类型均值 × 1.1（季节性调整） |
| 房屋险 | 重置成本 × 90% |
| 健康险 | 平均赔付率 60-70% × 申报金额 |
| 寿险 | 保额 × 发生率表 |

---

## 2. Underwriting Benchmarks（核保基准）

来源: afrexai-insurance-automation §1 Underwriting Assessment

### Referral 触发条件（转介高级核保师）

满足以下任一条件必须转介：
- 过去 5 年损失 > 3 次
- 信用评分 < 600
- 高风险职业（见高风险职业清单）
- 保额超过自动承保限额（每类产品不同）
- 异常健康状况（指定疾病列表）
- 海外居住/工作

### Combined Ratio 目标（行业基准）

| 业务线 | 目标 Combined Ratio | 说明 |
|--------|------------------|------|
| 汽车险 | 95%–98% | ≥98% 盈利困难 |
| 房屋险 | 85%–92% | 较稳定 |
| 商业险 | 88%–95% | 受巨灾影响大 |
| 寿险 | 变动大，按死亡率表 | 参照精算模型 |

---

## 3. Compliance Frameworks（合规框架 — 补充参考）

来源: afrexai-insurance-automation §5 Compliance & Regulatory

> ⚠️ 以下用于 **Agent 3 合规检查的框架参考**，不替代 MAS/HKIA/BNM/OIC 等具体监管要求。

### 主要监管框架对照

| 地区 | 主要监管机构 | 关键框架 | 与保险相关法规 |
|------|------------|---------|--------------|
| **新加坡** | MAS | FAA, MAS Notice 307, CPFIS | 投资连结险/UL产品 |
| **香港** | HKIA | HKIAOrdinance, GN15, FLCM | 分红险/万能险 |
| **马来西亚** | BNM | Takaful Act, SST | 回教保险 |
| **泰国** | OIC | 保险法, DST | 最低期限要求 |
| **印尼** | OJK | POJK, PPh | 预提税 |
| **菲律宾** | IC | 保险法, DST | 产品注册 |
| **美国** | NAIC | NAIC Model Laws, State DOI | 各州差异 |
| **英国** | FCA | ICOBS, SYSC, Consumer Duty, IDD | 跨境保险销售 |
| **欧盟** | EIOPA | Solvency II, IDD, GDPR | 跨境保险 |

### Anti-Fraud SIU（补充 Agent 3）

如 BSD 涉及 claims automation 或 auto-adjudication，须在 Preconditions 中加入：
```
IF claim meets any SIU red flag → route to SIU (not auto-approve)
```

---

## 4. Insurance Metrics Dashboard（保险指标 — UAT 参考）

来源: afrexai-insurance-automation §6 Insurance Metrics Dashboard

| 指标 | 个人业务目标 | 商业业务目标 | UAT 验证重点 |
|------|-----------|-----------|------------|
| Combined Ratio | 95%–98% | 88%–95% | UAT-FIN-001 |
| Loss Ratio | 60%–70% | 55%–65% | UAT-FIN-002 |
| Expense Ratio | 25%–32% | 28%–35% | UAT-FIN-003 |
| 理赔处理时间 | < 48h（汽车） | < 14天 | UAT-CLM-TAT |
| 保单签发时间 | < 15min（个人） | < 24h | UAT-NB-TAT |
| 续保率 | > 85% | > 80% | UAT-PS-REN |
| Quote-to-Bind 转化率 | > 25% | > 15% | UAT-NB-CONV |

---

## 5. Automation Priority Matrix（自动化优先级 — Agent 7 参考）

来源: afrexai-insurance-automation §7 Automation Priority Matrix

| 流程 | 月均工时（50人经纪商）| Agent-Ready | 年化节省 |
|------|-------------------|------------|---------|
| Quote comparison | 160h | Yes | $140K–$280K |
| FNOL intake | 120h | Yes | $105K–$210K |
| Policy document generation | 80h | Yes | $70K–$140K |
| Renewal processing | 100h | Yes | $87K–$175K |
| Compliance checks | 60h | Yes | $52K–$105K |
| Subrogation identification | 40h | Partial | $35K–$70K |
| Complex claims adjustment | 200h | Human-in-loop | $50K–$100K |

> **用途**: Agent 7 Ripple Propagation 评估跨模块影响时，可参照此矩阵评估自动化实现的 ROI。

---

## 6. Broker Operations Pipeline（经纪商 5-Agent 架构 — Agent 7 参考）

来源: afrexai-insurance-automation §4 Broker Operations

```
Intake Agent → Research Agent → Quoting Agent → Analysis Agent → Delivery Agent
     │              │                │               │              │
     └──并行执行最多4路同时carrier交互 ──────────►│
```

> **用途**: Agent 7 评估跨模块影响时，可参照此多-agent 协作模式评估 ripple magnitude（High/Medium/Low）。
