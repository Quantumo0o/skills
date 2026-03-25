---
name: mock
version: "1.0.0"
description: "Generate mock data and simulate API endpoints using CLI tools. Use when prototyping APIs or testing integrations."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: [mock, api, testing, data-generation, prototyping]
---

# Mock — Mock Data & API Simulation Tool

Generate realistic mock data, define API endpoints, record and replay HTTP interactions, and manage response schemas — all from the command line. Perfect for frontend developers prototyping without a backend, QA engineers needing test fixtures, or anyone who needs fake-but-realistic data fast.

## Prerequisites

- Python 3.8+
- `bash` shell
- `jq` (for JSON formatting, optional but recommended)
- `curl` (for server testing)

## Data Storage

All mock data is stored in `~/.mock/data.jsonl` as newline-delimited JSON. Each record has a unique `id`, a `type` field (endpoint, response, schema, seed, recording), and a `created_at` timestamp.

Configuration is stored in `~/.mock/config.json`.

## Commands

### `server`
Start a mock HTTP server on a specified port. Serves all defined endpoints with their configured responses.

```
MOCK_PORT=8080 bash scripts/script.sh server
```

### `endpoint`
Create, list, or delete API endpoint definitions. Each endpoint has a method, path, status code, and response body reference.

```
MOCK_METHOD=GET MOCK_PATH="/api/users" MOCK_STATUS=200 MOCK_RESPONSE_ID=resp_abc bash scripts/script.sh endpoint
```

### `response`
Define a response body template. Supports static JSON and dynamic field placeholders for mock data generation.

```
MOCK_BODY='{"id":"{{uuid}}","name":"{{name}}","email":"{{email}}"}' MOCK_NAME="user-response" bash scripts/script.sh response
```

### `record`
Record an HTTP interaction (request + response) for later replay. Stores method, URL, headers, and response.

```
MOCK_URL="https://api.example.com/users" MOCK_METHOD=GET bash scripts/script.sh record
```

### `replay`
Replay a previously recorded HTTP interaction by its record ID.

```
MOCK_RECORD_ID=rec_123 bash scripts/script.sh replay
```

### `schema`
Define or validate a JSON schema for mock data. Used to generate type-safe mock responses.

```
MOCK_SCHEMA_NAME="User" MOCK_SCHEMA='{"type":"object","properties":{"id":{"type":"string"},"name":{"type":"string"}}}' bash scripts/script.sh schema
```

### `seed`
Generate seed data from a schema. Produces N records of realistic fake data matching the schema definition.

```
MOCK_SCHEMA_ID=sch_123 MOCK_COUNT=10 bash scripts/script.sh seed
```

### `list`
List all stored items (endpoints, responses, schemas, seeds, recordings) with optional type filtering.

```
MOCK_TYPE=endpoint bash scripts/script.sh list
```

### `export`
Export all mock data or a filtered subset to a JSON file for sharing or backup.

```
MOCK_OUTPUT=/tmp/mock-export.json MOCK_TYPE=all bash scripts/script.sh export
```

### `config`
View or update configuration settings (default port, data directory, response delay, CORS settings).

```
MOCK_KEY=port MOCK_VALUE=3000 bash scripts/script.sh config
```

### `help`
Show usage information and available commands.

```
bash scripts/script.sh help
```

### `version`
Display the current version of the mock skill.

```
bash scripts/script.sh version
```

## Examples

```bash
# Create a response template
MOCK_BODY='{"users":[{"id":1,"name":"Alice"}]}' MOCK_NAME="users-list" bash scripts/script.sh response

# Create an endpoint using that response
MOCK_METHOD=GET MOCK_PATH="/api/users" MOCK_STATUS=200 MOCK_RESPONSE_ID=<id> bash scripts/script.sh endpoint

# Generate 50 seed records from a schema
MOCK_SCHEMA_ID=<id> MOCK_COUNT=50 bash scripts/script.sh seed

# Export everything
MOCK_OUTPUT=./backup.json bash scripts/script.sh export
```

## Notes

- The mock server is a lightweight Python HTTP server — not intended for production use.
- All data persists across sessions in JSONL format.
- Use `list` with `MOCK_TYPE` to filter by record type.
- The `seed` command generates deterministic data when given the same schema and count.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
