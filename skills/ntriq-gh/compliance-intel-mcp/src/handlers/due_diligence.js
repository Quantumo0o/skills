import log from '@apify/log';
import { safeFetchJSON, fetchJSON, truncate, formatDate } from './utils.js';

// GLEIF — Global LEI database (international org, commercial use permitted)
const GLEIF_BASE = 'https://api.gleif.org/api/v1';
// SEC EDGAR — US government public data
const EDGAR_BASE = 'https://efts.sec.gov/LATEST/search-index';
const EDGAR_COMPANY = 'https://www.sec.gov/cgi-bin/browse-edgar';
// SAM.gov — US government procurement (public data)
const SAM_BASE = 'https://api.sam.gov/entity-information/v3/entities';

/**
 * Company due diligence via GLEIF + SEC EDGAR + SAM.gov
 */
export async function companyDueDiligence({ company, country, limit = 5 }) {
    const name = (company || '').trim();
    if (!name) throw new Error('company name is required');

    log.info(`Due Diligence: "${name}" (country=${country || 'any'})`);

    const [gleifData, edgarData, samData] = await Promise.allSettled([
        searchGLEIF(name, country, limit),
        searchEDGAR(name, limit),
        searchSAM(name, limit),
    ]);

    const gleif = gleifData.status === 'fulfilled' ? gleifData.value : null;
    const edgar = edgarData.status === 'fulfilled' ? edgarData.value : null;
    const sam = samData.status === 'fulfilled' ? samData.value : null;

    const riskScore = calcRiskScore(gleif, edgar, sam);

    return {
        company: name,
        riskScore,
        riskLevel: riskScore >= 70 ? 'HIGH' : riskScore >= 40 ? 'MEDIUM' : 'LOW',
        gleif: gleif ? {
            found: gleif.length > 0,
            count: gleif.length,
            entities: gleif.slice(0, 3),
        } : { found: false, error: 'GLEIF unavailable' },
        sec: edgar ? {
            found: edgar.filings > 0,
            filings: edgar.filings,
            latestFiling: edgar.latest,
            cik: edgar.cik,
        } : { found: false, error: 'SEC EDGAR unavailable' },
        sam: sam ? {
            found: sam.length > 0,
            count: sam.length,
            contractors: sam.slice(0, 3),
        } : { found: false, error: 'SAM.gov unavailable' },
        screenedAt: new Date().toISOString(),
        report: buildDDReport(name, gleif, edgar, sam, riskScore),
    };
}

async function searchGLEIF(name, country, limit) {
    let url = `${GLEIF_BASE}/fuzzycompletions?field=entity.legalName&q=${encodeURIComponent(name)}&page[size]=${limit}`;
    if (country) url += `&filter[entity.legalAddress.country]=${country}`;

    const data = await safeFetchJSON(url, 15000);
    if (!data?.data) return [];

    return data.data.map(d => ({
        lei: d.lei || null,
        legalName: d.attributes?.value || name,
        country: d.attributes?.country || null,
        status: 'ACTIVE',
    }));
}

async function searchEDGAR(name, limit) {
    const url = `https://efts.sec.gov/LATEST/search-index?q=%22${encodeURIComponent(name)}%22&dateRange=custom&startdt=2020-01-01&forms=10-K,10-Q,8-K&hits.hits._source=period_of_report,file_date,form_type,display_names,entity_name`;
    const data = await safeFetchJSON(url, 15000);

    if (!data?.hits?.hits) {
        // Fallback: try company search
        const companyUrl = `https://efts.sec.gov/LATEST/search-index?q=%22${encodeURIComponent(name)}%22&hits.hits.total.value=1`;
        const fallback = await safeFetchJSON(companyUrl, 10000);
        return {
            filings: fallback?.hits?.total?.value || 0,
            latest: null,
            cik: null,
        };
    }

    const hits = data.hits.hits;
    const latest = hits[0]?._source;
    return {
        filings: data.hits.total?.value || hits.length,
        latest: latest ? {
            date: latest.file_date,
            form: latest.form_type,
            entity: latest.entity_name || latest.display_names?.[0],
        } : null,
        cik: hits[0]?._source?.ciks?.[0] || null,
    };
}

async function searchSAM(name, limit) {
    const url = `${SAM_BASE}?legalBusinessName=${encodeURIComponent(name)}&includeSections=entityRegistration&pageSize=${limit}`;
    const data = await safeFetchJSON(url, 15000);

    if (!data?.entityData) return [];

    return data.entityData.slice(0, limit).map(e => ({
        uei: e.entityRegistration?.ueiSAM || null,
        name: e.entityRegistration?.legalBusinessName || name,
        status: e.entityRegistration?.registrationStatus || 'Unknown',
        expirationDate: formatDate(e.entityRegistration?.registrationExpirationDate),
        country: e.entityRegistration?.physicalAddress?.countryCode || null,
    }));
}

function calcRiskScore(gleif, edgar, sam) {
    let score = 0;
    if (!gleif || gleif.length === 0) score += 20; // No LEI = less transparent
    if (!edgar || edgar.filings === 0) score += 10; // No SEC filings (may be private, not necessarily risk)
    if (!sam || sam.length === 0) score += 5;
    // If SAM found with expired registration
    if (sam?.some(s => s.status === 'Expired')) score += 15;
    return Math.min(score, 100);
}

function buildDDReport(name, gleif, edgar, sam, riskScore) {
    const lines = [
        `COMPANY DUE DILIGENCE REPORT`,
        `Company: ${name}`,
        `Risk Score: ${riskScore}/100 — ${riskScore >= 70 ? 'HIGH' : riskScore >= 40 ? 'MEDIUM' : 'LOW'}`,
        `Screened: ${new Date().toISOString()}`,
        '',
        '── GLEIF (Global Legal Entity Identifier) ──',
    ];

    if (gleif && gleif.length > 0) {
        gleif.slice(0, 3).forEach(e => {
            lines.push(`  LEI: ${e.lei || 'N/A'} | Name: ${e.legalName} | Country: ${e.country || 'N/A'}`);
        });
    } else {
        lines.push('  No LEI registration found (entity may not require one)');
    }

    lines.push('', '── SEC EDGAR (US Securities Filings) ──');
    if (edgar && edgar.filings > 0) {
        lines.push(`  Filings Found: ${edgar.filings}`);
        if (edgar.latest) lines.push(`  Latest: ${edgar.latest.form} on ${edgar.latest.date}`);
        if (edgar.cik) lines.push(`  CIK: ${edgar.cik}`);
    } else {
        lines.push('  No SEC filings found (private company or non-US entity)');
    }

    lines.push('', '── SAM.gov (US Federal Contractor Registry) ──');
    if (sam && sam.length > 0) {
        sam.slice(0, 3).forEach(s => {
            lines.push(`  UEI: ${s.uei || 'N/A'} | ${s.name} | Status: ${s.status} | Country: ${s.country || 'N/A'}`);
        });
    } else {
        lines.push('  No SAM.gov registration (not a US federal contractor)');
    }

    return lines.join('\n');
}
