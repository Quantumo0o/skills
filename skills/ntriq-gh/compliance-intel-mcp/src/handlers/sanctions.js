import log from '@apify/log';
import { safeFetchJSON, truncate } from './utils.js';

// OFAC SDN list — US Treasury public data (commercial reuse permitted)
const OFAC_SDN_CSV = 'https://www.treasury.gov/ofac/downloads/sdn.csv';

/**
 * Fuzzy name matching score (0-100)
 */
function matchScore(query, target) {
    if (!query || !target) return 0;
    const q = query.toLowerCase().trim();
    const t = target.toLowerCase().trim();
    if (t === q) return 100;
    if (t.includes(q) || q.includes(t)) return 80;
    const qWords = q.split(/\s+/);
    const tWords = t.split(/\s+/);
    const overlap = qWords.filter(w => tWords.includes(w)).length;
    return Math.round((overlap / Math.max(qWords.length, tWords.length)) * 60);
}

/**
 * Screen entity against OFAC SDN list via Treasury CSV
 */
export async function screenSanctions({ query, type = 'all', threshold = 70, limit = 20 }) {
    const name = (query || '').trim();
    if (!name) throw new Error('query is required');

    log.info(`Sanctions: Screening "${name}" (type=${type}, threshold=${threshold})`);

    try {
        // Fetch Treasury SDN CSV
        const res = await fetch(OFAC_SDN_CSV, { signal: AbortSignal.timeout(60000) });
        if (!res.ok) {
            if (res.status === 429 || res.status >= 500) {
                throw new Error(`OFAC service temporarily unavailable (HTTP ${res.status}). Please retry in a few minutes.`);
            }
            throw new Error(`HTTP ${res.status} from Treasury SDN`);
        }

        const text = await res.text();
        const lines = text.split('\n');

        const matches = [];
        const nameQuery = name.toLowerCase();
        const regex = new RegExp(`\\b${nameQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i');

        // Parse CSV (skip header, columns: Entity ID, Name, Type, Program)
        // Early exit after collecting enough matches to reduce processing time
        for (let i = 1; i < lines.length; i++) {
            const line = lines[i].trim();
            if (!line) continue;

            // Simple CSV parsing (handle quotes)
            const cols = line.split(',').map(c => c.replace(/^"|"$/g, '').trim());
            const sdnName = (cols[1] || '').trim();
            const sdnType = (cols[2] || '').trim();
            const program = (cols[3] || '').trim();

            if (!sdnName || sdnName.length < 3) continue;

            const score = sdnName === nameQuery ? 100 :
                          regex.test(sdnName) ? 85 :
                          (sdnName.includes(nameQuery) || nameQuery.includes(sdnName)) ? 70 : 0;

            if (score >= threshold) {
                matches.push({ name: sdnName, score, type: sdnType, program });
                // Early exit: once we have plenty of matches, stop scanning
                if (matches.length >= limit * 3) break;
            }
        }

        const sanctioned = matches.length > 0;

        return {
            query: name,
            type,
            threshold,
            totalMatches: matches.length,
            sanctioned,
            highRisk: sanctioned,
            matches: matches.slice(0, limit),
            source: 'OFAC SDN List (US Treasury)',
            screenedAt: new Date().toISOString(),
            report: buildSanctionsReport(name, matches)
        };
    } catch (e) {
        log.error(`OFAC screening error: ${e.message}`);
        return {
            query: name,
            totalMatches: null,
            sanctioned: null,
            error: e.message,
            note: 'OFAC screening temporarily unavailable',
            source: 'OFAC SDN List (US Treasury)',
            screenedAt: new Date().toISOString()
        };
    }
}

/**
 * Batch screen multiple entities
 */
export async function batchScreenSanctions({ entities = [], threshold = 70 }) {
    if (!Array.isArray(entities) || entities.length === 0) {
        throw new Error('entities array is required');
    }
    if (entities.length > 50) throw new Error('Maximum 50 entities per batch');

    log.info(`Batch screening ${entities.length} entities`);

    const results = await Promise.allSettled(
        entities.slice(0, 50).map(e => screenSanctions({ query: e, threshold }))
    );

    const screenings = results.map((r, i) => ({
        entity: entities[i],
        status: r.status === 'fulfilled' ? 'screened' : 'error',
        sanctioned: r.status === 'fulfilled' ? r.value.sanctioned : null,
        highRisk: r.status === 'fulfilled' ? r.value.highRisk : null,
        matchCount: r.status === 'fulfilled' ? r.value.totalMatches : 0,
        error: r.status === 'rejected' ? r.reason?.message : null,
    }));

    const flagged = screenings.filter(s => s.highRisk);
    return {
        total: entities.length,
        flagged: flagged.length,
        clean: screenings.filter(s => !s.highRisk && s.status === 'screened').length,
        errors: screenings.filter(s => s.status === 'error').length,
        results: screenings,
        flaggedEntities: flagged.map(s => s.entity),
        screenedAt: new Date().toISOString(),
        report: buildBatchReport(entities.length, flagged, screenings)
    };
}

function buildSanctionsReport(name, matches) {
    const lines = [
        `SANCTIONS SCREENING REPORT`,
        `Query: ${name}`,
        `Total SDN Matches: ${matches.length}`,
        `Status: ${matches.some(m => m.score >= 90) ? '🚨 HIGH RISK — Strong SDN match found' : matches.some(m => m.score >= 70) ? '⚠️ REVIEW REQUIRED — Partial matches found' : '✅ CLEAR — No significant matches'}`,
        `Source: OFAC SDN List (US Treasury)`,
        `Screened: ${new Date().toISOString()}`,
    ];

    if (matches.length > 0) {
        lines.push('', 'TOP MATCHES:');
        matches.slice(0, 5).forEach(m => {
            lines.push(`  [${m.score}%] ${m.name} | Type: ${m.type} | Program: ${m.program || 'N/A'}`);
        });
    }

    return lines.join('\n');
}

function buildBatchReport(total, flagged, screenings) {
    return `BATCH SANCTIONS SCREENING\n\nTotal: ${total} | Flagged: ${flagged.length} | Clean: ${screenings.filter(s => !s.highRisk && s.status === 'screened').length}\n\n${flagged.length > 0 ? `FLAGGED ENTITIES:\n${flagged.map(s => `- ${s.entity} (${s.matchCount} matches)`).join('\n')}` : 'No entities flagged.'}`;
}
