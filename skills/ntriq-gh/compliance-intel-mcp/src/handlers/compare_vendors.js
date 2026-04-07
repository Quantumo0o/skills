import log from '@apify/log';
import { assessVendor } from './assess_vendor.js';

/**
 * Compare multiple vendors and rank them
 */
export async function compareVendors({ vendors = [], criteria = 'overall' }) {
    if (!Array.isArray(vendors) || vendors.length === 0) {
        throw new Error('vendors array is required');
    }
    if (vendors.length > 10) {
        throw new Error('Maximum 10 vendors per comparison');
    }

    log.info(`Compare Vendors: ${vendors.length} candidates (criteria=${criteria})`);

    // Assess all vendors in parallel
    const results = await Promise.allSettled(
        vendors.map(v => assessVendor({ company: v }))
    );

    // Extract assessments
    const assessments = results.map((r, i) => ({
        company: vendors[i],
        status: r.status === 'fulfilled' ? 'assessed' : 'error',
        assessment: r.status === 'fulfilled' ? r.value : null,
        error: r.status === 'rejected' ? r.reason?.message : null,
    }));

    // Score mapping for sorting
    const verdictScore = { GO: 3, CAUTION: 1, BLOCK: 0 };
    const criteriaWeights = {
        overall: (a) => a.assessment.scores.overall,
        safety: (a) => a.assessment.scores.safety,
        compliance: (a) => a.assessment.scores.overall,
    };

    const getScore = (a) => {
        if (!a.assessment) return -1;
        const vScore = verdictScore[a.assessment.verdict] || 0;
        const criteriaScore = (criteriaWeights[criteria] || criteriaWeights.overall)(a) || 0;
        return vScore * 100 + criteriaScore;
    };

    // Rank vendors
    const ranked = assessments
        .filter(a => a.status === 'assessed')
        .sort((a, b) => getScore(b) - getScore(a))
        .map((a, idx) => ({
            rank: idx + 1,
            company: a.company,
            verdict: a.assessment.verdict,
            score: a.assessment.scores.overall,
            riskLevel: a.assessment.scores.overall > 75 ? 'LOW' : a.assessment.scores.overall > 50 ? 'MEDIUM' : 'CRITICAL',
        }));

    // Build recommendation
    let recommendation = '';
    if (ranked.length === 0) {
        recommendation = 'Unable to assess any vendors. Manual review required.';
    } else if (ranked[0].verdict === 'BLOCK') {
        recommendation = `All vendors show critical issues. Expand search or escalate to legal. Highest-scoring option: ${ranked[0].company} (${ranked[0].verdict}).`;
    } else {
        recommendation = `${ranked[0].company} is the lowest-risk vendor (${ranked[0].verdict}, score ${ranked[0].score}/100). Proceed with due diligence.`;
    }

    return {
        total: vendors.length,
        ranked,
        recommendation,
        comparedAt: new Date().toISOString(),
    };
}
