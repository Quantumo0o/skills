import log from '@apify/log';

const DEFAULT_TIMEOUT = 30000;

export function ft(url, ms = DEFAULT_TIMEOUT, options = {}) {
    const c = new AbortController();
    const t = setTimeout(() => c.abort(), ms);
    return fetch(url, { signal: c.signal, ...options }).finally(() => clearTimeout(t));
}

export async function retry(fn, times = 3) {
    for (let i = 0; i < times; i++) {
        try { return await fn(); }
        catch (e) {
            if (i === times - 1) throw e;
            const delay = 1000 * (i + 1);
            log.debug(`Retry ${i + 1}/${times} after ${delay}ms: ${e.message}`);
            await new Promise(r => setTimeout(r, delay));
        }
    }
}

export async function fetchJSON(url, ms = DEFAULT_TIMEOUT) {
    const res = await retry(() => ft(url, ms));
    if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText} for ${url}`);
    return res.json();
}

export async function safeFetchJSON(url, ms = DEFAULT_TIMEOUT) {
    try { return await fetchJSON(url, ms); }
    catch (e) { log.debug(`Safe fetch failed for ${url}: ${e.message}`); return null; }
}

export function formatDate(dateStr) {
    if (!dateStr) return null;
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    return d.toISOString().split('T')[0];
}

export function truncate(text, maxLen = 300) {
    if (!text) return '';
    return text.length > maxLen ? text.substring(0, maxLen) + '...' : text;
}
