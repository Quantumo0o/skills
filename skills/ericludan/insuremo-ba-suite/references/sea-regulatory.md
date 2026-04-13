# SEA Regulatory Framework Index

> Agent 3 quick reference file
> ⚠️ This file is an index, not regulatory source text.
> Always use web_search to retrieve the latest version before citing any requirement.

---

## Regulatory Authorities & Key Regulations by Market

### MY — Malaysia (BNM)
| Regulation / Guideline | Summary | Typical InsureMO Impact |
|---|---|---|
| Life Insurance and Family Takaful Framework | Product design, pricing, disclosure requirements | Product approval process, KFD format |
| BNM/RH/GL-003 | Key Features Document (KFD) format requirements | Document generation module |
| IFSA 2013 (Financial Services Act) | Overall insurance compliance framework | Contract terms, consumer protection |
| Takaful Operational Framework | Wakalah / Mudharabah structure | Premium calculation module needs separate handling |

### SG — Singapore (MAS)
| Regulation / Guideline | Summary | Typical InsureMO Impact |
|---|---|---|
| MAS Notice 307 | Life insurance product information disclosure | Product illustration format |
| FAA (Financial Advisers Act) | Sales process and advice requirements | NB entry compliance checks |
| MAS Notice 128 | Insurance product approval requirements | Pre-launch approval workflow |

### TH — Thailand (OIC)
| Regulation / Guideline | Summary | Typical InsureMO Impact |
|---|---|---|
| Life Insurance Act | Foundational legal framework | Contract term compliance |
| OIC Product Approval Guidelines | New product launch requirements | Product config approval workflow |
| Thai-language document requirement | All client documents must have a Thai version | Document generation multi-language support |

### PH — Philippines (IC)
| Regulation / Guideline | Summary | Typical InsureMO Impact |
|---|---|---|
| Insurance Code (as amended) | Overall insurance legal framework | Contract design, claims rules |
| IC Product Registration Requirement | Pre-launch registration with IC required | Product config must carry registration number |
| Documentary Stamp Tax (DST) | Insurance policies subject to stamp duty | Premium calculation must include DST component |

### ID — Indonesia (OJK)
| Regulation / Guideline | Summary | Typical InsureMO Impact |
|---|---|---|
| POJK 69/2016 | Life insurance product development and marketing | Product design standards |
| POJK 23/2023 | Latest insurance sector regulatory update | Verify via web_search for current requirements |
| PPh Withholding Tax | Income tax withholding on insurance proceeds | Claims calculation module |

---

## Cross-Market Universal Notes

**Rider vs Base Policy:**
All SEA market regulatory frameworks require that riders cannot remain active after the base policy lapses.
InsureMO's `INVARIANT: Rider_Term ≤ Base_Policy_Term` rule is compliant across all markets.

**Minimum Coverage Term:**
Most markets require a minimum coverage term for individual life insurance (typically 1–5 years).
Verify exact values via web_search — do not rely on this reference.

**Product Approval:**
All markets require pre-approval from the regulator before launching a new product (including significant amendments).
Whether an InsureMO product configuration change constitutes a "significant amendment" requires legal judgment.

---

> Search tip: Use `[regulator] [product type] regulation [year]` format
> Prefer official regulator websites (.gov / .org)
> Note your search date — results older than 6 months should be re-verified
