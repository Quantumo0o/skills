---
name: ntriq-compliance-intel-mcp
description: "Regulatory compliance analysis. Checks GDPR, SOX, HIPAA, PCI-DSS requirements and flags violations."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [compliance,regulatory,risk]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Compliance Intel MCP

Regulatory compliance gap analysis for GDPR, SOX, HIPAA, and PCI-DSS. Submit policies, contracts, or code descriptions and receive framework-specific requirement checks with violation flags and remediation guidance.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | ✅ | Policy text, contract clause, or system description |
| `frameworks` | array | ✅ | Compliance frameworks: `gdpr`, `sox`, `hipaa`, `pci_dss` |
| `industry` | string | ❌ | Sector context: `healthcare`, `finance`, `retail` |
| `jurisdiction` | string | ❌ | `us`, `eu`, `uk` (default: `us`) |

## Example Response

```json
{
  "frameworks_checked": ["gdpr", "hipaa"],
  "violations": [
    {
      "framework": "GDPR",
      "article": "Art. 13",
      "severity": "high",
      "finding": "No data retention period disclosed to data subjects",
      "remediation": "Add explicit retention schedule to privacy notice"
    }
  ],
  "passed": ["HIPAA Minimum Necessary Rule", "HIPAA Encryption at Rest"],
  "compliance_score": 74
}
```

## Use Cases

- Privacy policy automated audit before launch
- Third-party vendor contract compliance review
- DevOps security control gap analysis

## Access

```bash
# Service catalog
curl https://x402.ntriq.co.kr/services
```

Available on [Apify Store](https://apify.com/ntriqpro/compliance-intel-mcp) · [x402 micropayments](https://x402.ntriq.co.kr)
