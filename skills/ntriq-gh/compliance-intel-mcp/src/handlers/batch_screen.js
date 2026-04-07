import log from '@apify/log';
import { canWeProceed } from './can_we_proceed.js';

/**
 * Batch screen multiple entities for quick GO/BLOCK decisions
 */
export async function batchScreen({ entities = [], screenType = 'sanctions' }) {
    if (!Array.isArray(entities) || entities.length === 0) {
        throw new Error('entities array is required');
    }
    if (entities.length > 100) {
        throw new Error('Maximum 100 entities per batch');
    }

    log.info(`Batch Screen: ${entities.length} entities (type=${screenType})`);

    // Screen all entities in parallel
    const results = await Promise.allSettled(
        entities.slice(0, 100).map(e => canWeProceed({ entity: e, type: screenType }))
    );

    const screenings = results.map((r, i) => ({
        entity: entities[i],
        status: r.status === 'fulfilled' ? 'screened' : 'error',
        proceed: r.status === 'fulfilled' ? r.value.proceed : null,
        riskLevel: r.status === 'fulfilled' ? r.value.riskLevel : 'UNKNOWN',
        reason: r.status === 'fulfilled' ? r.value.reason : r.reason?.message,
    }));

    const cleared = screenings.filter(s => s.proceed === true).length;
    const blocked = screenings.filter(s => s.proceed === false).length;
    const errors = screenings.filter(s => s.status === 'error').length;

    // Build summary
    const blockedEntities = screenings
        .filter(s => s.proceed === false)
        .map(s => `${s.entity} (${s.reason})`);

    let summary = `${cleared}/${entities.length} entities cleared`;
    if (blocked > 0) {
        summary += `. ${blocked} blocked: ${blockedEntities.slice(0, 3).join('; ')}${blockedEntities.length > 3 ? '; ...' : ''}.`;
    }
    if (errors > 0) {
        summary += ` ${errors} screening errors.`;
    }

    return {
        total: entities.length,
        cleared,
        blocked,
        errors,
        results: screenings,
        summary,
        screenedAt: new Date().toISOString(),
    };
}
