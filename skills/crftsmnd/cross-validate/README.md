# Cross-Validate API

**Base URL:** https://clawskills.netlify.app

## Endpoints

### GET /price
```bash
curl https://clawskills.netlify.app/price
```

### POST /api/v1/verify
```bash
curl -X POST https://clawskills.netlify.app/api/v1/verify \
  -H "Content-Type: application/json" \
  -H "x402-payment: true" \
  -d '{"claim":"Coffee causes cancer","baseline":{"score":78}}'
```

## Payment
- Price: $0.05 USDC
- Header: `x402-payment: true`
- Without payment: Returns 402 Payment Required