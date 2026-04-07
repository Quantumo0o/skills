import log from '@apify/log';
import { screenSanctions } from './sanctions.js';
import { govContractHistory } from './gov_contracts.js';
import { safeFetchJSON } from './utils.js';

/**
 * Fetch OSHA establishment data from public API
 */
async function fetchOSHAData(companyName, state) {
    try {
        // OSHA uses HTML form search, so we'll use a simple approximation
        // by searching for inspection records via public data
        const url = new URL('https://www.osha.gov/ords/imis/establishment.search');
        url.searchParams.set('p_company', companyName);
        if (state) url.searchParams.set('p_state', state);

        const res = await fetch(url, { signal: AbortSignal.timeout(15000) });
        if (!res.ok) return null;

        const text = await res.text();
        // Simplified: count inspection mentions in page
        const inspectionMatches = (text.match(/inspection/gi) || []).length;
        const violationMatches = (text.match(/violation/gi) || []).length;

        return {
            inspectionCount: Math.min(inspectionMatches, 100),
            violationCount: violationMatches,
        };
    } catch (e) {
        log.debug(`OSHA fetch failed: ${e.message}`);
        return null;
    }
}

/**
 * Fetch EPA facility data using ECHO API
 */
async function fetchEPAData(companyName, state) {
    try {
        const params = { p_fn: companyName };
        if (state) params.p_st = state;

        const url = new URL('https://echodata.epa.gov/echo/echo_rest_services.get_facilities');
        url.searchParams.set('output', 'JSON');
        for (const [k, v] of Object.entries(params)) {
            if (v) url.searchParams.set(k, v);
        }

        const data = await safeFetchJSON(url.toString(), 20000);
        if (!data || !data.Results) return null;

        const queryId = data.Results.QueryID;
        if (!queryId) return null;

        // Get actual facilities
        const qidUrl = new URL('https://echodata.epa.gov/echo/echo_rest_services.get_qid');
        qidUrl.searchParams.set('output', 'JSON');
        qidUrl.searchParams.set('qid', queryId);
        qidUrl.searchParams.set('pageno', '1');

        const facilityData = await safeFetchJSON(qidUrl.toString(), 15000);
        if (!facilityData || !facilityData.Facilities) return null;

        const facilities = facilityData.Facilities || [];
        const withViolations = facilities.filter(f => {
            const status = (f.FacComplianceStatus || '').toLowerCase();
            return status.includes('violation') || status.includes('noncompliance');
        });

        return {
            facilityCount: facilities.length,
            violationCount: withViolations.length,
            facilitiesWithViolations: withViolations.map(f => ({
                name: f.FacName,
                status: f.FacComplianceStatus,
            })),
        };
    } catch (e) {
        log.debug(`EPA fetch failed: ${e.message}`);
        return null;
    }
}

/**
 * Calculate overall compliance scores based on all data sources
 */
function calculateScores(sanctionsData, oshaData, epaData, govData) {
    // OFAC Sanctions score (0-100, 100 = clean)
    let sanctionsScore = 100;
    if (!sanctionsData) {
        sanctionsScore = 50; // Unavailable = medium caution
    } else if (sanctionsData.sanctioned) {
        sanctionsScore = 0; // Sanctioned = block
    }

    // Safety score (OSHA) - based on inspection/violation counts
    let safetyScore = 100;
    if (oshaData) {
        const inspectionPenalty = Math.min((oshaData.inspectionCount || 0) / 5, 40);
        const violationPenalty = Math.min((oshaData.violationCount || 0) * 10, 40);
        safetyScore = Math.max(0, 100 - inspectionPenalty - violationPenalty);
    }

    // Environmental score (EPA) - based on violation facilities
    let environmentalScore = 100;
    if (epaData) {
        const facilityCount = epaData.facilityCount || 0;
        const violationCount = epaData.violationCount || 0;
        if (facilityCount > 0) {
            const violationRate = violationCount / facilityCount;
            const violationPenalty = violationRate * 50;
            const facilityPenalty = Math.min(facilityCount / 2, 15);
            environmentalScore = Math.max(0, 100 - violationPenalty - facilityPenalty);
        }
    }

    // Government contractor score (bonus if good contractor, penalty if issues)
    let contractorScore = 70; // baseline
    if (govData) {
        if ((govData.awards || []).length > 0) {
            contractorScore = Math.min(90, 70 + (govData.awards.length * 5));
        }
    }

    // Calculate overall score (weighted average)
    const overall = Math.round(
        (sanctionsScore * 0.4) +
        (safetyScore * 0.25) +
        (environmentalScore * 0.25) +
        (contractorScore * 0.1)
    );

    return { sanctions: sanctionsScore, safety: safetyScore, environmental: environmentalScore, contractor: contractorScore, overall };
}

/**
 * Calculate verdict from scores
 */
function calcVerdict(scores) {
    if (scores.sanctions === 0) return 'BLOCK';
    if (scores.overall < 30) return 'BLOCK';
    if (scores.overall < 60) return 'CAUTION';
    return 'GO';
}

function calcRiskLevel(verdict) {
    return { GO: 'LOW', CAUTION: 'MEDIUM', BLOCK: 'CRITICAL' }[verdict];
}

/**
 * Assess vendor: full due diligence with GO/CAUTION/BLOCK verdict
 */
export async function assessVendor({ company, state }) {
    const name = (company || '').trim();
    if (!name) throw new Error('company is required');

    log.info(`Assess Vendor: "${name}" (state=${state || 'all'})`);

    // Parallel data collection
    const [sanctionsResult, oshaResult, epaResult, govResult] = await Promise.all([
        screenSanctions({ query: name, threshold: 70 }).catch(e => {
            log.debug(`Sanctions error: ${e.message}`);
            return null;
        }),
        fetchOSHAData(name, state).catch(e => {
            log.debug(`OSHA error: ${e.message}`);
            return null;
        }),
        fetchEPAData(name, state).catch(e => {
            log.debug(`EPA error: ${e.message}`);
            return null;
        }),
        govContractHistory({ company: name, limit: 10 }).catch(e => {
            log.debug(`Gov contracts error: ${e.message}`);
            return null;
        }),
    ]);

    // Calculate scores
    const scores = calculateScores(sanctionsResult, oshaResult, epaResult, govResult);
    const verdict = calcVerdict(scores);
    const riskLevel = calcRiskLevel(verdict);

    // Build risk factors
    const riskFactors = [];
    if (sanctionsResult && sanctionsResult.sanctioned) {
        riskFactors.push(`OFAC sanctions match: ${sanctionsResult.matches?.[0]?.program || 'unknown program'}`);
    }
    if (oshaResult && (oshaResult.inspectionCount || 0) > 50) {
        riskFactors.push(`${oshaResult.inspectionCount} OSHA inspections since 2020`);
    }
    if (oshaResult && (oshaResult.violationCount || 0) > 5) {
        riskFactors.push(`${oshaResult.violationCount} OSHA safety violations on record`);
    }
    if (epaResult && (epaResult.violationCount || 0) > 0) {
        riskFactors.push(`${epaResult.violationCount} EPA facility violations (${epaResult.facilityCount} regulated facilities)`);
    }
    if (!riskFactors.length) {
        riskFactors.push('No significant risk factors identified');
    }

    // Build summary
    let summary = '';
    if (verdict === 'BLOCK') {
        summary = `${name} has critical compliance issues. ${riskFactors[0] || 'OFAC sanctions or critical violations detected.'} Do not proceed.`;
    } else if (verdict === 'CAUTION') {
        const topFactor = riskFactors[0] || 'Minor compliance concerns';
        summary = `${name} shows ${topFactor}. Compliance score: ${scores.overall}/100.`;
    } else {
        summary = `${name} is a low-risk vendor. Compliance score: ${scores.overall}/100. No critical issues identified.`;
    }

    // Build recommendation
    let recommendation = '';
    if (verdict === 'BLOCK') {
        recommendation = 'BLOCK — Do not proceed. Legal review required immediately.';
    } else if (verdict === 'CAUTION') {
        recommendation = `Proceed with enhanced monitoring. ${riskFactors.length > 0 ? `Key concerns: ${riskFactors.slice(0, 2).join(', ')}. ` : ''}Request compliance documentation before contract signing.`;
    } else {
        recommendation = 'Proceed with standard due diligence protocols.';
    }

    return {
        company: name,
        verdict,
        confidence: scores.overall > 75 || scores.overall < 25 ? 'HIGH' : 'MEDIUM',
        summary,
        recommendation,
        riskFactors,
        scores,
        decidedAt: new Date().toISOString(),
    };
}
