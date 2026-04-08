# MBUSA Dealer & Inventory API / OpenClaw Skill

A dual-purpose Node.js application that serves as an LLM tool (OpenClaw Skill) and a standalone REST API for querying official Mercedes-Benz USA dealership locations and new vehicle inventory.

## Project Structure
* `src/tool.js`: Core logic that fetches and parses data from MBUSA APIs. Handles strict MBUSA enum mapping and price formatting.
* `schema.json`: Function definitions for OpenClaw LLM agent integration.
* `server.js`: Express wrapper exposing the tools as HTTP REST endpoints.

## Installation

1. Ensure you have Node.js (v18+ recommended) installed.
2. Clone this repository and install the Express dependency:

\`\`\`bash
npm install
\`\`\`

## Running the API Server

To start the standalone web server:

\`\`\`bash
npm start
\`\`\`
The server will listen on `http://localhost:3000`.

## API Documentation

### 1. Dealer Locator
Fetches a list of dealerships near a given zip code.

**Endpoint:** `GET /api/dealers`

**Parameters:**
* `zip` (string, **required**): 5-digit US zip code.
* `start` (integer, optional): Pagination offset (default: 0).
* `count` (integer, optional): Number of results to return (default: 10).

**Example Request:**
\`\`\`text
GET http://localhost:3000/api/dealers?zip=10019&count=3
\`\`\`

---

### 2. Vehicle Inventory Search
Fetches live new-vehicle inventory from dealerships near a given zip code.

**Endpoint:** `GET /api/inventory`

**Parameters:**
* `zip` (string, **required**): 5-digit US zip code.
* `dealerId` (string, optional): Specific 5-digit MBUSA dealer code.
* `distance` (integer, optional): Search radius (10, 25, 50, 100, 200, 500, 1000).
* `minPrice` / `maxPrice` (integer, optional): Filter by MSRP.
* `model` / `classId` / `bodyStyle` / `brand` (string, optional): Specific vehicle filters based on MBUSA enums.
* `exteriorColor` / `interiorColor` (string, optional): Filter by color enum (e.g., BLK, BLU).
* `fuelType` / `highwayFuelEconomy` (string, optional): Powertrain filters.
* `year` / `passengerCapacity` (integer, optional): Numeric vehicle traits.
* `start` / `count` (integer, optional): Pagination settings.

**Example Request:**
\`\`\`text
GET http://localhost:3000/api/inventory?zip=10019&classId=EQS&distance=25&maxPrice=110000&exteriorColor=BLK
\`\`\`