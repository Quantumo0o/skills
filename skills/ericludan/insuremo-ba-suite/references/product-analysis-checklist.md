# Product Spec Analysis Checklist

> 必须按顺序执行，确保分析完整性

## 分析流程

### Step 1: 提取 Features
- [ ] 读取产品文档所有章节 (Section 1-N)
- [ ] 提取每个章节的 feature list

### Step 2: 交叉验证 (Two-Pass)
**Pass 1**: 查询 ps-* 详细规则文档
```
references/InsureMO Knowledge/ps-new-business.md       - 新单规则
references/InsureMO Knowledge/ps-underwriting.md       - 核保规则
references/InsureMO Knowledge/ps-claims.md            - 理赔规则
references/InsureMO Knowledge/ps-customer-service.md  - 客服/保全规则
references/InsureMO Knowledge/ps-billing-collection-payment.md - 收费/支付规则
references/InsureMO Knowledge/ps-investment.md        - 投资规则
references/InsureMO Knowledge/ps-fund-administration.md - 账户管理规则
references/InsureMO Knowledge/ps-product-factory.md   - 产品工厂配置
```

**Pass 2**: 查询 OOTB 系统能力
```
references/InsureMO Knowledge/insuremo-ootb.md
```

### Step 3: 标记规则

| 状态 | 条件 | 标记 |
|------|------|------|
| ✅ OOTB | ps-* 和 OOTB 都确认支持 | OOTB |
| ⚠️ Config | ps-* 有规则，需配置 | Config |
| ❌ Dev Gap | ps-* 有明确规则，OOTB 不支持 | Dev Gap |
| ❓ Unknown | ps-* 没明确写 | **Unknown** (不是默认 Dev!) |

### Step 4: 输出
- [ ] 生成 Gap Matrix
- [ ] 标注 Unknown 项目待确认

---

## 禁止事项

- ❌ 不能只看 OOTB 就判断是 Dev Gap
- ❌ 不能假设 ps-* 没写的就是 Dev
- ❌ 不能跳过 ps-* 直接查 OOTB

---

*Created: 2026-03-15*
