# MBUSA Dealer & Inventory Skill

This OpenClaw skill enables AI agents to query Mercedes-Benz USA (MBUSA.com) data. This is not officially from MBUSA. It allows the agent to find local dealerships in USA and search for live, new-vehicle inventory.

## Tools Included

### 1. `get_mbusa_dealers`
Allows the agent to find official Mercedes-Benz dealerships using a US zip code.
* **Primary Use Case:** "Find a Mercedes dealer near 10019" or "Give me the service department number for the dealer in Bayside, NY."
* **Data Returned:** Dealership name, primary address, distance, main phone, service phone, website URL, and service scheduling URL.

### 2. `get_mbusa_inventory`
Allows the agent to search for new vehicle inventory on dealership lots near a specific zip code.
* **Primary Use Case:** "Are there any new EQS sedans under $100,000 near me?" or "Find a 2026 GLC within 50 miles of 30097."
* **Capabilities:** Supports strict enum-based filtering by model, class, body style, brand, interior/exterior colors, fuel type, passenger capacity, highway fuel economy, price range, year, and search radius.
* **Data Returned:** VIN, Stock ID, year, model name, MSRP, engine type, exterior/interior colors, the holding dealership's name, distance, and direct actionable URLs for images and dealer websites.

## Configuration & Output
Ensure the `schema.json` file is loaded into your agent's context window. The agent has been explicitly instructed to format the actionable URLs (Image, Dealer Website, Service Scheduling) as clickable Markdown links when responding to the user.



