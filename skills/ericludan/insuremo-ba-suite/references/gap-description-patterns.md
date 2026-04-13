# Gap Description Writing Patterns
# Based on: HSBC Life Singapore MVP3 Gap List (gap_list_mvp3.xlsx)
# Date: 2026-03-19
# Source: 525 implemented Gaps (Day 1 / Day 2 categories)

---

## Gap Description 写作规范

### Client Requirement Description

**规范写法：**

1. **明确业务背景** — 说明是哪个产品线、哪个业务场景
2. **说清楚用户角色** — NB user / underwriter / claims handler
3. **说清楚触发条件** — 什么时候需要这个功能，为什么
4. **包含具体业务规则** — 不要只说"显示"，要说"显示什么值、按什么逻辑"

**示例：**

✅ 正确：
> "For shield product, some Life Assured won't provide the actual birthday's DD/MM, NB user will enter dummy DOB(YYYY/01/01) to calculate the premium for specific LA. But in CPF files, need to capture the MM/DD as 00/00"

> "Shield breakdown of Premiums — HSBC requires to show the Shield premium break down in New business and underwriting screen including CPF Withdraw Amount/ Cash Amount/Discount premium/etc."

> "Projection batch needs to check whether the policy age is crossed or will be crossed until next Monday. If the age crossed, system needs to regenerate the new projection and send to CPF."

❌ 常见错误：
- 只说"需要显示"不说显示什么
- 缺少业务上下文
- 没有说明用户是谁

---

### Current eBao System Function

**规范写法：**

1. **说明现状是什么** — 系统当前怎么做的
2. **简洁，不要过度描述** — 一两句话
3. **如果完全没有这个功能** — 写 "Not applicable"

**示例：**

✅ 正确：
> "eBao only show the total inforced premium instead of premium breakdown in data entry stage"

> "Not applicable"

---

### Gap Description

**规范写法：**

1. **以动词开头** — Add / Change / Configure / Extract / Update
2. **一句话概括** — 简洁，说明缺什么
3. **不要解释为什么** — 原因在 Client Requirement 里已经说清楚了

**示例：**

✅ 正确：
> "Need to add new indicator to identify the DOB is a dummy DOB"

> "Add a new table to show the premium breakdown in data entry and underwriting"

> "CPF Projection integration requirement"

❌ 常见错误：
- 以 "The system needs..." 开头（冗余）
- 包含业务背景（应该只在 Client Requirement 里）
- 超过一行

---

### Recommendation / High Level Solution

**规范写法：**

1. **以动词开头** — Add / Configure / Extract / Update / Change
2. **用编号列表** — 多个步骤时用 1. 2. 3.
3. **每个步骤具体** — 不要只说"修改"，要说"修改哪个表/字段/逻辑"
4. **包含具体参数值或枚举值** — 如果有的话
5. **引用相关Gap** — 如 "Use same table of NBU_SH_011"

**示例：**

✅ 正确：
> "1. Add new indicator to identify the DOB is a dummy DOB
> 2. Change the CPF file data logic for dummy DOB"

> "1. Add a new daily batch to trigger CPF projection
> 2. Configure the projection request template file
> 3. Extract the policy date which meet the projection extraction rules
> 4. Add a new NB menu for user to generate Ad-hoc projection request
> 5. During premium projection process stage, system needs to grey off most of party and policy information in verification"

> "Add a new table to show the premium breakdown in data entry and underwriting:
> -Discount Premium
> -CPF Premium
> -Cash Premium
> -etc."

> "Use same table of NBU_SH_011 to show the CPF return premium breakdown in data entry and underwriting"

❌ 常见错误：
- 只说"需要开发"不说具体做什么
- 没有编号，步骤混乱
- 缺少对现有功能的引用

---

## Gap Number 命名规范（HSBC MVP3参考）

格式：`{LOB_PREFIX}_{CATEGORY}_{SEQ}`

- CPF_S_XXX — CPF Shield 相关
- L_XXX — Life 相关
- SH_XXX — Shield & Health 相关
- CR_XXX — Change Request 编号

---

## 快速检查清单

输出 Gap Description 前，逐项确认：

- [ ] Client Requirement 包含业务背景（谁、什么时候、为什么）
- [ ] Client Requirement 有具体业务规则（值、条件、触发时机）
- [ ] Gap Description 以动词开头，一句话概括
- [ ] Solution 是编号列表，每个步骤具体可执行
- [ ] Solution 引用了相关功能或已有Gap（如适用）
- [ ] Solution 包含具体表名、字段名、参数值
