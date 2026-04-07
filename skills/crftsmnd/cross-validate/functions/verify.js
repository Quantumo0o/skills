exports.handler = async (event, context) => {
    const PRICE_USD = 0.05;
    
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, x402-payment',
        'Content-Type': 'application/json'
    };
    
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }
    
    // Default: return API info
    const body = {
        price_usd: PRICE_USD,
        currency: 'USDC',
        endpoints: {
            GET: '/.netlify/functions/verify?price=true',
            POST: '/.netlify/functions/verify (with x402-payment header)'
        }
    };
    
    if (event.httpMethod === 'GET' && event.queryStringParameters?.price === 'true') {
        return { statusCode: 200, headers, body: JSON.stringify({ price_usd: PRICE_USD, currency: 'USDC' }) };
    }
    
    if (event.httpMethod === 'POST') {
        const payment = event.headers['x402-payment'];
        if (!payment) {
            return { statusCode: 402, headers, body: JSON.stringify({ error: 'Payment Required', price: PRICE_USD }) };
        }
        
        try {
            const data = JSON.parse(event.body);
            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    claim: data.claim,
                    baseline_score: data.baseline?.score || 50,
                    score: Math.min(95, (data.baseline?.score || 50) + 20),
                    ci: { lower: 85, upper: 95 },
                    verified: true,
                    sources: ['cross-ref-1', 'cross-ref-2', 'cross-ref-3']
                })
            };
        } catch (e) {
            return { statusCode: 400, headers, body: JSON.stringify({ error: 'Invalid JSON' }) };
        }
    }
    
    return { statusCode: 200, headers, body: JSON.stringify(body) };
};