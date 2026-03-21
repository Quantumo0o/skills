---
name: strider-kroger
description: Shop Kroger via Strider Labs MCP connector. Search groceries, clip digital coupons, manage cart, order pickup or delivery. Complete autonomous grocery shopping for your AI agent.
metadata:
  openclaw:
    requires:
      bins: ["npx"]
    category: "commerce"
    author: "Strider Labs"
    homepage: "https://striderlabs.ai"
---

# Strider Kroger Connector

MCP connector for shopping at Kroger — search products, clip digital coupons, manage cart, and order for pickup or delivery. Works with Kroger family stores (Ralphs, Fred Meyer, Fry's, King Soopers, etc.). Part of the Strider Labs action execution layer for AI agents.

## Installation

```bash
npm install @striderlabs/mcp-kroger
```

## MCP Configuration

Add to your MCP client configuration (Claude Desktop, Cursor, etc.):

```json
{
  "mcpServers": {
    "kroger": {
      "command": "npx",
      "args": ["-y", "@striderlabs/mcp-kroger"]
    }
  }
}
```

## Available Tools

### kroger.search_products
Search Kroger's catalog by keyword, category, or brand.

**Input Schema:**
```json
{
  "query": "string (search terms)",
  "category": "string (optional: produce, dairy, meat, etc.)",
  "store_id": "string (optional: for local pricing/inventory)",
  "brand": "string (optional: filter by brand)"
}
```

**Output:**
```json
{
  "products": [{
    "id": "string",
    "name": "string",
    "price": "number",
    "sale_price": "number (if on sale)",
    "coupon_available": "boolean",
    "in_stock": "boolean",
    "aisle": "string (store location)"
  }]
}
```

### kroger.add_to_cart
Add products to shopping cart with specified quantity.

### kroger.get_coupons
Get available digital coupons for your account.

**Output:**
```json
{
  "coupons": [{
    "id": "string",
    "title": "string",
    "discount": "string",
    "min_purchase": "number",
    "expires": "string (ISO date)"
  }]
}
```

### kroger.clip_coupon
Clip a digital coupon to your Kroger Plus card.

### kroger.checkout
Complete purchase with saved payment method.

**Input Schema:**
```json
{
  "fulfillment_type": "string (pickup, delivery)",
  "store_id": "string (for pickup)",
  "delivery_address": "object (for delivery)",
  "time_slot": "string (ISO datetime)"
}
```

### kroger.find_stores
Find nearby Kroger family stores by location.

## Authentication

First use triggers OAuth authorization flow. Works with Kroger Plus card for savings. Tokens stored encrypted per-user.

## Usage Examples

**Weekly grocery order:**
```
Order groceries from Kroger: milk, eggs, bread, bananas, chicken breasts, and broccoli
```

**Coupon hunting:**
```
Show me available Kroger digital coupons and clip any good ones for products on my shopping list
```

**Pickup scheduling:**
```
Schedule a Kroger pickup for Saturday morning with my weekly essentials
```

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| AUTH_EXPIRED | Session expired | Re-authenticate |
| OUT_OF_STOCK | Item unavailable | Suggest alternatives |
| SLOT_UNAVAILABLE | Time slot taken | Offer alternative times |
| COUPON_EXPIRED | Coupon no longer valid | Remove from cart |

## Use Cases

- Weekly grocery shopping: automate recurring orders
- Coupon optimization: maximize savings with digital coupons
- Meal planning: order ingredients for weekly meal prep
- Pickup scheduling: coordinate convenient pickup times

## Kroger Family Stores

This connector works with all Kroger-owned chains:
- Kroger, Ralphs, Fred Meyer, Fry's, King Soopers
- Smith's, QFC, Dillons, Harris Teeter, and more

## Links

- npm: https://npmjs.com/package/@striderlabs/mcp-kroger
- Strider Labs: https://striderlabs.ai
