import log from '@apify/log';
import { screenSanctions } from './sanctions.js';

/**
 * Quick decision: can we proceed with this entity?
 * Fast OFAC-only check, returns YES/NO
 */
export async function canWeProceed({ entity, type = 'transaction' }) {
    const name = (entity || '').trim();
    if (!name) throw new Error('entity is required');

    log.info(`Can Proceed: "${name}" (type=${type})`);

    try {
        const sanctionsData = await screenSanctions({ query: name, threshold: 70 });

        if (sanctionsData.sanctioned) {
            return {
                entity: name,
                proceed: false,
                reason: `OFAC sanctions match: ${sanctionsData.matches?.[0]?.program || 'OFAC SDN List'}`,
                riskLevel: 'CRITICAL',
                action: `BLOCK — Do not proceed. Legal review required. Sanctions program: ${sanctionsData.matches?.[0]?.program || 'unknown'}.`,
                checkedAt: new Date().toISOString(),
            };
        }

        return {
            entity: name,
            proceed: true,
            reason: 'No OFAC sanctions match found',
            riskLevel: 'LOW',
            action: 'PROCEED — Entity cleared for transaction/vendor relationship.',
            checkedAt: new Date().toISOString(),
        };
    } catch (e) {
        log.error(`Can Proceed check failed: ${e.message}`);
        return {
            entity: name,
            proceed: null,
            reason: `OFAC screening unavailable: ${e.message}`,
            riskLevel: 'UNKNOWN',
            action: 'MANUAL REVIEW REQUIRED — OFAC screening temporarily offline. Check again or contact legal.',
            checkedAt: new Date().toISOString(),
        };
    }
}
