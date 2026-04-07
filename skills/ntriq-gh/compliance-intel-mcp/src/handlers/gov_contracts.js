import log from '@apify/log';
import { formatDate, truncate } from './utils.js';

async function safeFetchJSON(url, ms, options) {
    try {
        const c = new AbortController();
        const t = setTimeout(() => c.abort(), ms || 30000);
        const res = await fetch(url, { signal: c.signal, ...options }).finally(() => clearTimeout(t));
        if (!res.ok) return null;
        return res.json();
    } catch (e) {
        return null;
    }
}

const USASPENDING = 'https://api.usaspending.gov/api/v2';

/**
 * Search US federal contract history via USASpending.gov
 */
export async function govContractHistory({ company, agency, minAmount, limit = 10 }) {
    const name = (company || '').trim();
    if (!name) throw new Error('company name is required');

    log.info(`Gov Contracts: "${name}" (agency=${agency || 'all'}, min=$${minAmount || 0})`);

    // Search awards
    const body = {
        filters: {
            recipient_search_text: [name],
            award_type_codes: ['A', 'B', 'C', 'D'], // contracts only
        },
        fields: ['Award ID', 'Recipient Name', 'Award Amount', 'Awarding Agency', 'Award Date', 'Period of Performance Start Date', 'Period of Performance Current End Date', 'Description'],
        page: 1,
        limit,
        sort: 'Award Amount',
        order: 'desc',
    };

    if (agency) body.filters.awarding_agency_names = [agency];
    if (minAmount) body.filters.award_amounts = [{ lower_bound: minAmount }];

    const data = await safeFetchJSON(`${USASPENDING}/search/spending_by_award/`, 20000, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });

    // Also get summary
    const summaryBody = {
        filters: body.filters,
        category: 'awarding_agency',
        limit: 5,
    };
    const summary = await safeFetchJSON(`${USASPENDING}/search/spending_by_category/awarding_agency/`, 15000, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(summaryBody),
    });

    const awards = data?.results || [];
    const totalAmount = awards.reduce((sum, a) => sum + (a['Award Amount'] || 0), 0);
    const topAgencies = summary?.results?.slice(0, 5).map(a => ({
        agency: a.name,
        amount: a.aggregated_amount,
    })) || [];

    return {
        company: name,
        totalAwards: data?.page_metadata?.total || awards.length,
        totalAmount,
        topAgencies,
        awards: awards.slice(0, limit).map(a => ({
            id: a['Award ID'],
            recipient: a['Recipient Name'],
            amount: a['Award Amount'],
            agency: a['Awarding Agency'],
            awardDate: formatDate(a['Award Date']),
            startDate: formatDate(a['Period of Performance Start Date']),
            endDate: formatDate(a['Period of Performance Current End Date']),
            description: truncate(a['Description'], 150),
        })),
        screenedAt: new Date().toISOString(),
        report: buildContractsReport(name, awards, totalAmount, topAgencies, data?.page_metadata?.total),
    };
}


function buildContractsReport(name, awards, totalAmount, topAgencies, total) {
    const fmt = (n) => n ? `$${Number(n).toLocaleString('en-US', { maximumFractionDigits: 0 })}` : '$0';
    const lines = [
        `US FEDERAL CONTRACT HISTORY`,
        `Contractor: ${name}`,
        `Total Awards Found: ${total || awards.length}`,
        `Total Value (shown): ${fmt(totalAmount)}`,
        `Source: USASpending.gov`,
        `Screened: ${new Date().toISOString()}`,
    ];

    if (topAgencies.length > 0) {
        lines.push('', 'TOP AWARDING AGENCIES:');
        topAgencies.forEach(a => lines.push(`  ${a.agency}: ${fmt(a.amount)}`));
    }

    if (awards.length > 0) {
        lines.push('', 'RECENT CONTRACTS:');
        awards.slice(0, 5).forEach(a => {
            lines.push(`  [${fmt(a['Award Amount'])}] ${a['Awarding Agency']} — ${a['Award Date'] || 'N/A'}`);
            if (a['Description']) lines.push(`    ${truncate(a['Description'], 100)}`);
        });
    } else {
        lines.push('', 'No federal contract awards found for this contractor.');
    }

    return lines.join('\n');
}
