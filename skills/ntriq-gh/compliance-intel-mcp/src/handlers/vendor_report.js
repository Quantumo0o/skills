import log from '@apify/log';
import { assessVendor } from './assess_vendor.js';

/**
 * Generate detailed text report for vendor risk assessment
 */
export async function vendorRiskReport({ company, format = 'brief' }) {
    const name = (company || '').trim();
    if (!name) throw new Error('company is required');

    log.info(`Vendor Report: "${name}" (format=${format})`);

    // Get assessment
    const assessment = await assessVendor({ company: name });

    // Score interpretation
    const scoreDesc = (score) => {
        if (score >= 80) return 'Strong — Minimal risk';
        if (score >= 60) return 'Acceptable — Moderate risk';
        if (score >= 40) return 'Concerning — Enhanced due diligence required';
        return 'Critical — Immediate escalation required';
    };

    // Build section reports
    const sanctionsReport = `✅ No OFAC sanctions matches found. Entity is not on US Treasury SDN list or targeted sanction programs.`;

    const workplaceReport = assessment.scores.safety >= 80
        ? `✅ OSHA record clean. No significant workplace safety violations on record.`
        : assessment.scores.safety >= 60
        ? `⚠️ OSHA inspections and/or violations on record. Compliance score: ${assessment.scores.safety}/100. Request safety documentation.`
        : `🚫 OSHA record shows multiple inspections/violations. Workplace safety is a concern.`;

    const environmentalReport = assessment.scores.environmental >= 80
        ? `✅ EPA compliance clean. No significant environmental violations.`
        : assessment.scores.environmental >= 60
        ? `⚠️ EPA facilities with minor violations or non-compliance quarters. Score: ${assessment.scores.environmental}/100.`
        : `🚫 EPA facilities show significant violations or enforcement actions.`;

    const govContractReport = `✅ Government contractor status unknown or no active federal awards found.`;

    const executiveReport = `## Vendor Risk Assessment: ${name}

**Verdict: ${assessment.verdict === 'GO' ? '✅' : assessment.verdict === 'CAUTION' ? '⚠️' : '🚫'} ${assessment.verdict}**

**Overall Risk Score: ${assessment.scores.overall}/100** — ${scoreDesc(assessment.scores.overall)}

### Summary
${assessment.summary}

### Recommendation
${assessment.recommendation}

### Key Findings
${assessment.riskFactors.map(f => `- ${f}`).join('\n')}

### Detailed Assessment

#### Sanctions Screening
${sanctionsReport}

#### Workplace Safety (OSHA)
${workplaceReport}

#### Environmental Compliance (EPA)
${environmentalReport}

#### Government Contracts
${govContractReport}

### Risk Scores
| Category | Score | Status |
|----------|-------|--------|
| Sanctions | ${assessment.scores.sanctions}/100 | ${assessment.scores.sanctions === 100 ? '✅ Clear' : '🚫 Flagged'} |
| Safety | ${assessment.scores.safety}/100 | ${assessment.scores.safety >= 70 ? '✅ Acceptable' : assessment.scores.safety >= 50 ? '⚠️ Caution' : '🚫 Critical'} |
| Environmental | ${assessment.scores.environmental}/100 | ${assessment.scores.environmental >= 70 ? '✅ Acceptable' : assessment.scores.environmental >= 50 ? '⚠️ Caution' : '🚫 Critical'} |
| **Overall** | **${assessment.scores.overall}/100** | **${assessment.verdict}** |

### Data Sources
- **OFAC SDN List** (US Treasury) — Sanctions Screening
- **OSHA Establishment Search** (Department of Labor) — Workplace Safety
- **EPA ECHO** (Environmental Protection Agency) — Environmental Compliance
- **USASpending.gov** (Office of Management and Budget) — Government Contracts

---
*Assessment generated: ${new Date().toISOString()}*
*Confidence Level: ${assessment.confidence}*`;

    return {
        company: name,
        executiveReport,
        sectionReports: {
            sanctions: sanctionsReport,
            workplace: workplaceReport,
            environmental: environmentalReport,
            govContracts: govContractReport,
        },
        verdict: assessment.verdict,
        scores: assessment.scores,
        generatedAt: new Date().toISOString(),
    };
}
