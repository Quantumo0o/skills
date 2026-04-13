# InsureMO Gap Detection Rules (R1–R10)
# Version 2.0 | 2026-04-05

> **Purpose**: Supplementary rules for identifying gaps that cannot be derived from OOTB capability tables alone
> **Use when**: Analyzing client requirements documents during gap analysis

---

## 17. Supplementary Gap Detection Rules (R1–R9)

> **When to use**: Apply this section against every new client requirements document *before* finalizing a gap analysis. These rules surface gaps that are invisible from the capability tables alone — they only become detectable when client context is available.

### Rule Index

| # | Rule | Why Capability Tables Cannot Detect It |
|---|---|---|
| R1 | Non-Functional Requirements (NFR) | Tables describe features, not quality attributes |
| R2 | Missing Capability (Blind Spot) | Client needs something with no matching row anywhere in this document |
| R3 | OOTB Depth / Variant Overflow | Capability is ✅ OOTB but client's variant exceeds what OOTB actually supports |
| R4 | Integration Topology | Tables flag "Dev Gap" for integration without knowing target system, protocol, or SLA |
| R5 | Data Migration & Cutover | InsureMO has no migration tooling; scope is 100% client-specific |
| R6 | Regulatory & Compliance | Market-specific laws, submission formats, and deadlines require client/market context |
| R7 | UI/UX & Accessibility | Tables document logic; screen design and accessibility standards are not covered |
| R8 | Operational Batch & SLA | Batch processes exist OOTB; scheduling windows and failure-recovery are client-specific |
| R9 | Config Volume & Complexity | Config Gap label is correct but "1 product" vs "100 products" requires calibration |

---

### R1 — Non-Functional Requirements (NFR)

> Tables describe functional capabilities only. Performance, availability, security, and data residency are entirely absent.

| Detection Question | If Answer Is… | Gap Tag |
|---|---|---|
| Required response time for quotation / policy issue? | Explicit SLA stated | 🚫 NFR — Performance |
| Expected concurrent user count at peak? | Exceeds standard load | 🚫 NFR — Scalability |
| Required system uptime / availability SLA? | > 99.5% or has RPO/RTO | 🚫 NFR — Availability |
| Data residency requirement (data must stay in-country)? | Yes | 🚫 NFR — Data Residency |
| Encryption standards required (AES-256, TLS 1.3 minimum)? | Specific standard named | 🚫 NFR — Security |
| Disaster Recovery requirement (RPO / RTO)? | Yes | 🚫 NFR — DR |
| Penetration testing or security audit obligation? | Yes | 📋 Process — Security Governance |
| Audit log retention period (e.g. 7 years)? | Specific period stated | 🚫 NFR — Audit Retention |

**Output rule**: Tag as `🚫 NFR Gap`. Add dimension (Performance / Scalability / Security / DR / Residency) to Notes. Default effort: **Medium** unless platform re-architecture is implied.

---

### R2 — Missing Capability (Blind Spot)

> The capability tables only document what InsureMO is aware of. Client requirements may describe business needs with no corresponding row — positive or negative — anywhere in this document.

**Detection rule**: For every functional requirement in the client document, ask: *Can I find a matching row in Sections 1–16?* If NO → candidate Blind Spot.

**Common Blind Spot patterns across insurance clients**:

| Blind Spot Area | Default Tag | Notes |
|---|---|---|
| Agent mobile / field sales app | 🔧 Dev Gap | Channel data model OOTB; mobile UI is custom |
| Customer self-service portal | ⚙️ Config Gap + 🔧 Dev Gap | API surface OOTB; portal UI custom |
| Digital onboarding (OCR / eKYC) | 🔧 Dev Gap | Third-party integration required |
| MAS / OJK / BNM regulatory submissions | 🔧 Dev Gap | Market-specific formats; see R6 |
| Reinsurance treaty bordereau | 🔧 Dev Gap | RI cession OOTB; treaty reporting is not |
| Policy illustration / benefit projection | 🔧 Dev Gap | Separate actuarial projection engine typically needed |
| Group scheme member administration | 🔧 Dev Gap | Group billing config OOTB; scheme member admin is not |
| Surrender value quotation API for third parties | ⚙️ Config Gap + 🔧 Dev Gap | Calculation OOTB; API exposure may need BFF layer |
| WhatsApp / chatbot notification | 🔧 Dev Gap | Notice config covers email/SMS only |
| IFRS 17 reporting (PAA / BBA) | 🔧 Dev Gap | GL hooks OOTB; IFRS 17 engine is not |

**Output rule**: Add a new row to the relevant module section. Tag appropriately. Add **Source: R2** in Notes.

---

### R3 — OOTB Depth / Variant Overflow

> A capability is marked ✅ OOTB, but the client's specific variant exceeds what OOTB actually delivers. This is the most common source of hidden gaps.

**Detection rule**: For every ✅ OOTB match, apply the overflow test below.

| Matched OOTB Capability | Overflow Test | If Overflow → |
|---|---|---|
| Standard premium quotation | Requires real-time external actuarial call? | 🔧 Dev Gap — External calc engine |
| Rider-to-base binding | >3 benefit layers or cross-product linking? | 🔧 Dev Gap — Complex product structure |
| Multi-level agent hierarchy | >5 levels? Override commissions across non-direct nodes? | 🔧 Dev Gap — Complex commission |
| Claim rule engine (auto-assessment) | AI/ML scoring, fraud scoring, or hospital pre-auth required? | 🔧 Dev Gap — AI/ML integration |
| Payment method support | Local e-wallet (GrabPay, GoPay, Touch 'n Go, etc.)? | 🔧 Dev Gap — Payment gateway |
| Beneficiary setup | Trust / legal guardian / minor beneficiary with court approval? | 🔧 Dev Gap — Complex beneficiary rules |
| Multi-language product content | Clause-level versioning per language per product version? | 🔧 Dev Gap — Content management layer |
| Interest Settlement (Batch) | Intraday settlement required (not end-of-day)? | 🔧 Dev Gap — Real-time settlement |
| RB / CB Allocation (Batch) | Mid-year rate declaration or variable bonus rates per segment? | ⚙️ Config Gap + 🔧 Dev Gap |
| CS alteration workflow | Same-day reversal of completed alterations past T+0? | 🔧 Dev Gap — Extended reversal window |

**Output rule**: Do NOT relabel the existing ✅ OOTB row. Add a **new child row** beneath it for the overflow variant. Add **Source: R3** in Notes.

---

### R4 — Integration Topology

> The capability tables flag integration needs as generic 🔧 Dev Gap. The specific target system, protocol, data format, and SLA are only knowable from the client requirements document.

**For each integration requirement, capture all dimensions**:

| Dimension | Question | Impact |
|---|---|---|
| Target system | Which specific system? (SAP, Oracle, Salesforce, custom…) | Determines adapter complexity |
| Protocol | REST / SOAP / SFTP / Kafka / MQ? | Determines integration pattern |
| Direction | Outbound / Inbound / Bidirectional? | Bidirectional sync = higher effort |
| Trigger | Real-time / Near-real-time / Daily batch / On-demand? | Real-time = higher effort |
| Volume | Transactions or events per day? | Affects design pattern |
| Error handling | Retry / fallback / dead-letter strategy required? | Adds Dev effort |
| Authentication | OAuth 2.0 / mTLS / API key / SSO? | Security effort |

**Integration record template** (one per endpoint):
```
Integration : [Name]
Direction   : Outbound / Inbound / Bidirectional
Protocol    : REST / SOAP / SFTP / MQ
Target      : [Vendor / Custom]
Trigger     : Real-time / Near-real-time / Daily batch / On-demand
Data Domain : Policy / Payment / Party / Finance / Claim / Channel
Auth        : [Method]
Effort      : Low / Medium / High
Source      : R4
```

**Output rule**: Add one row per distinct integration endpoint. Tag as `🔧 Dev Gap`. Add **Source: R4** in Notes.

---

### R5 — Data Migration & Cutover

> InsureMO has no data migration tooling. Migration scope, legacy system complexity, and cutover strategy are 100% client-specific and entirely absent from the capability tables.

| Detection Question | Gap Implication |
|---|---|
| Greenfield or migration from a legacy system? | Legacy → migration gap module needed |
| How many in-force policies to migrate? | Volume → effort multiplier |
| Which legacy system? (Unisys, Majesco, in-house…) | Determines extract complexity |
| Historical transactions required (not just current status)? | Transaction history = much higher effort |
| Parallel run period (both systems live simultaneously)? | Reconciliation tooling needed |
| Cutover strategy (big-bang / phased / product-line-by-line)? | Affects design and rollback planning |
| Open claims, in-flight alterations, or unpaid premiums at cutover? | In-flight handling = Dev Gap |
| Customer / party data migrated separately from policy data? | Dedup and merge rules needed |

**Standard migration gap categories**:

| Gap | Tag | Default Effort |
|---|---|---|
| Data extract from legacy system | 🔧 Dev Gap | Medium |
| Data transformation / mapping layer | 🔧 Dev Gap | Medium–High |
| Policy master data load to InsureMO | 🔧 Dev Gap | Medium |
| Historical transaction load | 🔧 Dev Gap | High |
| Open items migration (claims, CS, billing) | 🔧 Dev Gap | High |
| Parallel run reconciliation tooling | 🔧 Dev Gap | Medium |
| Cutover runbook and rollback plan | 📋 Process Gap | Medium |
| Data quality validation framework | 🔧 Dev Gap | Medium |

**Output rule**: Add a standalone **Data Migration** module to the gap analysis if legacy migration is in scope. Tag rows `🔧 Dev Gap` or `📋 Process Gap`. Add **Source: R5** in Notes.

---

### R6 — Regulatory & Compliance

> The capability tables mention market-specific regulation generically. Specific laws, submission formats, deadlines, and penalties require client/market context.

**Regulatory gap matrix by market**:

| Market | Common Regulatory Gaps | Default Tag |
|---|---|---|
| Singapore (MAS) | MAS 123 par value reporting, MAS 319 group supervision, FATCA/CRS submission, SGFinDex integration, CPF investment link | 🔧 Dev Gap |
| Malaysia (BNM) | Takaful fund separation, PDPA Malaysia, BNM policy document submission, e-Cover Note | ⚙️ Config + 🔧 Dev Gap |
| Indonesia (OJK) | OJK SAPK/SIPO reporting, Surat Perintah Transfer format, local data residency | 🔧 Dev Gap |
| Thailand (OIC) | OIC annual filing, tax-deductible premium reporting, compulsory PA | ⚙️ Config + 🔧 Dev Gap |
| Philippines (IC) | IC actuarial valuation report, mandatory riders | ⚙️ Config Gap |
| Hong Kong (IA) | RBC reporting, ORSA, IA product filing approval | 🔧 Dev Gap |
| China (CBIRC) | CIRC reporting system, KPI 135 policy, silver-age product rules | 🔧 Dev Gap |
| Cross-market | IFRS 17 (PAA / BBA), FATCA/CRS, Solvency II equivalent | 🔧 Dev Gap |

**Detection questions**:

| Question | If Yes → |
|---|---|
| Regulatory submission obligation (MAS / OJK / BNM / OIC…)? | Add market-specific reporting gap |
| Takaful or Shariah-compliant product in scope? | Confirm Takaful Dev Gap scope (already flagged in Section 1) |
| Consumer data protection law beyond standard KYC (PDPA / GDPR)? | Add privacy compliance automation gap |
| Regulator-approved product filing workflow required? | Add regulatory approval workflow gap |
| IFRS 17 reporting in scope? | Add IFRS 17 engine gap |

**Output rule**: Add rows to the relevant module or create a standalone **Regulatory Compliance** section if ≥3 regulatory gaps. Tag `🔧 Dev Gap` unless purely config-driven. Add **Source: R6 + [Market]** in Notes.

---

### R7 — UI/UX & Accessibility

> The capability tables document business logic and data models, not screen layouts, user journeys, accessibility standards, or design system requirements.

| Detection Question | Gap Implication |
|---|---|
| Corporate design system or brand guideline the UI must follow? | UI customization / theming gap |
| Mobile app requirement (iOS / Android native or hybrid)? | Mobile app Dev Gap (BFF + native) |
| Web self-service portal for customers? | Portal UI Dev Gap |
| Accessibility requirements (WCAG 2.1 AA, local accessibility laws)? | Accessibility compliance Dev Gap |
| Language-first UI required (Arabic RTL, Thai, etc.)? | RTL / locale UI Dev Gap |
| Screen-by-screen UX wireframes specified in requirements? | Custom UI Dev Gap if deviating from OOTB screens |
| Agent mobile / tablet POS requirement? | Mobile POS Dev Gap |

**Output rule**: Tag custom UI components as `🔧 Dev Gap`; theme/color-only changes as `⚙️ Config Gap`. Add **Source: R7** in Notes.

---

### R8 — Operational Batch & SLA

> The capability tables confirm batch processes exist but do not specify when they run, what SLA they must meet, or what happens on failure.

| Detection Question | Gap Implication |
|---|---|
| End-of-day batch completion deadlines (e.g. by 06:00)? | Batch scheduling config + performance testing |
| Intraday settlement requirements (interest, fund prices)? | Real-time / near-real-time engine — 🔧 Dev Gap |
| Recovery time requirement if batch fails mid-run? | Batch retry / restart design — 🔧 Dev Gap or 📋 Process Gap |
| Non-standard working week (e.g. Fri–Sat weekend)? | Holiday calendar + batch schedule reconfiguration — ⚙️ Config Gap |
| Batch monitoring / alerting required (PagerDuty, email alerts)? | Monitoring integration — 🔧 Dev Gap |
| Regulatory deadline for batch output (e.g. monthly GL close by T+2)? | Batch SLA — 🔧 Dev Gap if tooling needed |

**Output rule**: Tag scheduling/timing as `⚙️ Config Gap`; monitoring, retry logic, or intraday processing as `🔧 Dev Gap`. Add **Source: R8** in Notes.

---

### R9 — Config Volume & Complexity

> Many items in the capability tables are correctly labeled ⚙️ Config Gap. However, the tables do not distinguish between configuring 1 product and configuring 100 products. This rule calibrates effort for high-volume configurations.

**Complexity multiplier table**:

| Config Area | Low | Medium | High |
|---|---|---|---|
| Product configuration | 1–5 products, standard types | 6–20 products, mixed types | 20+ products, complex hybrid |
| Commission rules | Flat % by product | Tier-based by channel + product | Multi-level overriding + clawback + contest |
| UW questionnaires | 1 standard template | 5–10 per product category | 20+ with conditional branching |
| CS alteration rules | Standard items only | Market-specific restrictions | Per-product per-alteration rules |
| Tax / GL mapping | 1 market, standard tax | Multi-tax types | Cross-market + multi-currency GL |
| Report configuration | Standard library only | 3–10 custom reports | 10+ reports with regulatory format |
| Holiday calendars | 1 market | 2–3 markets | 4+ markets with fund-level calendars |

**Detection rule**: When a ⚙️ Config Gap item is found, determine scope from the client requirements, apply the multiplier table, and if result is **High** — escalate to `⚙️ Config Gap (High)` or add a 🔧 Dev Gap flag if configuration tooling itself becomes a bottleneck.

**Output rule**: Do not change the ⚙️ Config Gap label. Append complexity rating `(Low / Medium / High)` to the Notes field. Flag all High-complexity configs for dedicated estimation.

---

### R10 — Cross-System Semantic Detection (Auto-Elevate Rule)

> Every feature whose requirement text contains cross-system, cross-policy, or third-party integration keywords
> must be pre-classified as **Dev Gap** before any OOTB lookup is performed.
> Override is possible only if Agent 1 can cite specific InsureMO documentation proving native support.

#### Trigger Condition
This rule fires **automatically and mandatorily** at the start of Agent 1 Gap Classification,
before any ps-* lookup or OOTB capability check. It cannot be skipped.

#### R10 Keyword Scanner (case-insensitive, full match required)

| Keyword(s) | Semantic Class | Default Elevation |
|---|---|---|
| `per life`, `lifetime`, `across all policies`, `any existing policy`, `all policies` | Cross-policy aggregation | **Dev Gap** — override requires cited proof of native cross-policy support |
| `cumulative`, `aggregate`, `total across`, `combined`, `combined limit` | Aggregation logic | **Dev Gap** — override requires cited proof |
| `custodian`, `custody` | Third-party data dependency | **Dev Gap** — override requires confirmed OOTB custodian integration |
| `reinsurer`, `quota share`, `ceding`, `ceding company`, `retrocession` | RI system integration | **Dev Gap** — override requires confirmed OOTB RI module |
| `listed securities`, `exchange`, `trading`, `market data` | Financial market integration | **Dev Gap** — override requires confirmed exchange feed integration |
| `real-time`, `on-the-fly`, `dynamic calculation` | Runtime external computation | **Dev Gap** — override requires confirmed formula builder support |
| `regulatory filing`, `submission to [authority]` | Regulatory state reporting | **Dev Gap** — override requires confirmed regulatory workflow |

#### R10 Scan Logic

```
FOR each feature F in the Gap Matrix:
  FOR each keyword K in R10_KEYWORD_LIST:
    IF K appears in F.raw_text OR F.description:
      IF F.gap_type != "Dev Gap":
        ELEVATE F.gap_type → "Dev Gap"
        SET F.R10_Flag = "YES"
        ADD to F.notes: "R10 triggered — [K]. Override requires cited proof of native
                         InsureMO cross-policy/cross-system support."
```

#### Override Conditions (all FOUR must be met to avoid Dev Gap)

1. InsureMO natively supports cross-policy lookups for this specific pattern
2. A documented OOTB config path exists (cite exact Product Factory path from ps-*.md)
3. The capability is confirmed in the relevant `ps-*.md` module guide
4. Agent 1 records override justification in Gap Matrix notes with R10 citation

**If any R10 keyword is matched but no override proof exists → Dev Gap classification stands.**

#### R10 Pre-Submission Checklist Item

```markdown
- [ ] **R10** — Scanned all features against R10 keyword list?
  □ Any keyword match that did NOT elevate to Dev Gap has written override justification
  □ Override justification cites specific InsureMO documentation (file + section)
  □ No R10 keyword matches were silently ignored
```

---

### Pre-Submission Checklist

Run this checklist against every client requirements document before finalizing any gap analysis:

- [ ] **R1** — Captured all NFR requirements? (Performance / SLA / Security / DR / Data Residency)
- [ ] **R2** — Any client requirements with NO matching row in Sections 1–16?
- [ ] **R3** — For every ✅ OOTB match, tested whether the client's variant overflows it?
- [ ] **R4** — Catalogued each integration endpoint (system, protocol, direction, real-time vs batch)?
- [ ] **R5** — If legacy migration is in scope, added a Data Migration module?
- [ ] **R6** — Checked for market-specific regulatory obligations (MAS / OJK / BNM / OIC / IA…)?
- [ ] **R7** — Identified any UI/UX, mobile, or accessibility requirements?
- [ ] **R8** — Identified any batch scheduling windows, SLAs, or failure-recovery requirements?
- [ ] **R9** — For every ⚙️ Config Gap, estimated volume/complexity and flagged High items?
- [ ] **R10** — Scanned all features against R10 keyword list? Any keyword match that did NOT elevate to Dev Gap has written override justification with specific KB citation?

---

### Supplementary Gap Table Template

Use this format to record gaps discovered via Rules R1–R9 (add as rows in the relevant module above, or as a standalone appendix):

| Capability / Requirement | Module | Status | Source | Config Path | Complexity | Notes |
|---|---|---|---|---|---|---|
| *(example)* Intraday interest settlement | Loan & Deposit | 🔧 Dev Gap | R8 | — | High | Client requires T+4h SLA |
| *(example)* Agent mobile POS app | Channel | 🔧 Dev Gap | R7 | — | High | iOS + Android; syncs with OOTB Channel API |
| *(example)* MAS 123 par value report | Regulatory | 🔧 Dev Gap | R6-SG | — | Medium | Annual XML submission |
| *(example)* 50-product commission config | Channel | ⚙️ Config Gap | R9 | Channel → Commission Rules | High | 50 products × 3 channel types = 150 rule sets |

