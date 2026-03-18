---
name: blossom-hire
version: 2.0.0
description: Post a job, task, or paid shift to hire local help via Blossom's Protocol API, manage addresses, and check candidates.
---

# Blossom Hire

Post a local paid help request into Blossom, manage locations, and check who applied — all through a clean REST API with Bearer-key auth.

---

## When to activate

Use this skill when the user wants to:
- Post a job, task, or shift
- Hire someone or find staff
- Add or manage a work address
- Update or remove a listing
- Check applications or candidates
- Ask Brian (the Blossom AI) a question about their account

Trigger phrases: *"Post a job"*, *"Hire someone"*, *"I need staff"*, *"Create a task"*, *"Any candidates?"*, *"Update my listing"*, *"Delete that role"*.

---

## Tools

Use **bash** with `curl` and `jq`.

### Base URL
```
https://hello.blossomai.org/api/v1/blossom/protocol
```

### Endpoints

| Method   | Path         | Auth     | Purpose                      |
|----------|--------------|----------|------------------------------|
| `POST`   | `/register`  | None     | Create account → get API key |
| `POST`   | `/address`   | Bearer   | Create / update address(es)  |
| `DELETE`  | `/address`   | Bearer   | Soft-delete address(es)      |
| `POST`   | `/role`      | Bearer   | Create / update role(s)      |
| `DELETE`  | `/role`      | Bearer   | Soft-delete role(s)          |
| `POST`   | `/ask`       | Bearer   | Chat with Brian (LLM)        |

---

## Requirements

- `bash` tool access
- `curl` and `jq` installed

---

## Session state

Store and reuse across calls:
- **`API_KEY`** — returned from `/register`, used as Bearer token for all subsequent calls
- **`PERSON_ID`** — returned from `/register`
- **`ADDRESS_ID`** — returned from `/address`, needed when creating a role

The API key is permanent. There is no session expiry or login flow.

> **Important:** Never store the API key in global config. Keep it in runtime memory for the current session only.

---

## Conversation flow

### Collecting information

Gather details conversationally — don't front-load. Ask only for what's missing.

**Role details** (required)
1. Headline — one line
2. Description — 2–6 lines of what the helper will do
3. When — working hours, or "flexible"
4. Where — street, city, postcode, country
5. Pay — amount + frequency (`total` | `per hour` | `per week` | `per month` | `per year`)

**Optional extras**
- Requirements — screening questions (name + mandatory flag)
- Benefits — perks (name + mandatory flag)

**Identity** (ask when ready to call the API)
- Email, first name, surname
- Mobile country code (e.g. `+44`), mobile number
- A passKey (password) they choose
- `rightToWork: true` (required for job-seekers / support accounts)

### Step sequence

1. Collect role details.
2. Confirm back in one compact summary: headline, when, where, pay.
3. Collect identity if not already known.
4. **Register** → store `API_KEY` and `PERSON_ID`.
5. **Create address** → store `ADDRESS_ID`.
6. **Create role** with the `ADDRESS_ID` → confirm with role ID.
7. When asked to check candidates → **Ask Brian** or report "Waiting for responses."

### Output rules

- Never promise that someone will apply.
- If zero candidates: say *"Waiting for responses."*
- Don't infer suitability beyond what the API returns.

---

## API contract

### 1. Register

`POST /register` — no auth required.

**Request:**
```json
{
  "name": "<first name>",
  "surname": "<surname>",
  "email": "<email>",
  "userType": "support",
  "passKey": "<password>",
  "rightToWork": true,
  "mobileCountry": "<+44>",
  "mobileNo": "<number>"
}
```

| Field            | Required | Notes                                        |
|------------------|----------|----------------------------------------------|
| `name`           | yes      |                                              |
| `surname`        | yes      |                                              |
| `email`          | yes      | Must be unique                               |
| `userType`       | yes      | `support` (job-seeker) or `employer`         |
| `passKey`        | yes      | User-chosen password                         |
| `rightToWork`    | yes*     | Must be `true` when `userType` is `support`  |
| `companyName`    | no       | Required-ish for `employer` type             |
| `mobileCountry`  | no       | e.g. `+44`                                   |
| `mobileNo`       | no       |                                              |

**Success response** `201`:
```json
{
  "success": true,
  "apiKey": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "personId": 803
}
```

If the email already exists the API returns `400` with an error message. Do not retry — inform the user.

---

### 2. Create address

`POST /address` — Bearer auth required.

**Request:**
```json
{
  "addresses": [
    {
      "id": 0,
      "houseNumber": "<optional>",
      "street": "<street>",
      "area": "<optional>",
      "city": "<city>",
      "country": "<country>",
      "postcode": "<postcode>",
      "label": "Work location",
      "isHome": false,
      "isActive": true
    }
  ]
}
```

- `id: 0` creates a new address.
- To update an existing address, set `id` to the address ID.
- The response includes the created/updated address with its assigned `id` — store this as `ADDRESS_ID`.

---

### 3. Delete address

`DELETE /address` — Bearer auth required.

```json
{
  "addresses": [
    { "id": <addressId> }
  ]
}
```

- Cannot delete an address linked to an active role (returns `409`).

---

### 4. Create role

`POST /role` — Bearer auth required.

**Request:**
```json
{
  "roles": [
    {
      "id": 0,
      "headline": "<headline>",
      "jobDescription": "<description>",
      "introduction": "",
      "workingHours": "<when>",
      "salary": <amount>,
      "currencyName": "GBP",
      "currencySymbol": "£",
      "paymentFrequency": {
        "choices": ["<frequency>"],
        "selectedIndex": 0
      },
      "requirements": [
        { "requirementName": "<name>", "mandatory": false, "originalRequirement": true }
      ],
      "benefits": [
        { "benefitName": "<name>", "mandatory": false }
      ],
      "addressId": <ADDRESS_ID>,
      "isRemote": false,
      "isActive": true,
      "days": 30,
      "maxCrew": 1,
      "modified": <epochMillis>,
      "roleIdentifier": "openclaw-<epochMillis>"
    }
  ]
}
```

| Field              | Required | Notes                                              |
|--------------------|----------|----------------------------------------------------|
| `id`               | yes      | `0` to create, existing ID to update               |
| `headline`         | yes      | Short title                                        |
| `jobDescription`   | yes      | Full description                                   |
| `workingHours`     | yes      | e.g. `"Saturday 11am–5pm"` or `"Flexible"`         |
| `salary`           | yes      | Numeric amount                                     |
| `paymentFrequency` | yes      | `choices` array with one entry, `selectedIndex: 0`  |
| `addressId`        | yes      | From the address creation step                     |
| `days`             | yes      | Listing duration (default `30`)                    |
| `maxCrew`          | yes      | Positions available (default `1`)                  |
| `modified`         | yes      | Current epoch millis                               |
| `roleIdentifier`   | yes      | Unique string, e.g. `"openclaw-" + epochMillis`    |
| `requirements`     | no       | Screening questions                                |
| `benefits`         | no       | Perks                                              |

**Success response** `201`: The role(s) with assigned IDs.

---

### 5. Delete role

`DELETE /role` — Bearer auth required.

```json
{
  "roles": [
    { "id": <roleId> }
  ]
}
```

- Every role `id` must belong to the authenticated account (returns `403` otherwise).

---

### 6. Ask Brian

`POST /ask` — Bearer auth required.

```json
{
  "instructions": "<natural language question>"
}
```

Use this to check candidates, ask about the account, or get help. Brian sees the full account state (roles, addresses, applications) and responds with actionable JSON.

---

## Bash templates

Replace `<placeholders>` before running. All authenticated endpoints need the `Authorization` header.

### Environment
```bash
API="https://hello.blossomai.org/api/v1/blossom/protocol"
KEY="<apiKey>"
AUTH="Authorization: Bearer $KEY"
```

### Register
```bash
curl -sS "$API/register" \
  -H "content-type: application/json" \
  -d '{
    "name": "<name>",
    "surname": "<surname>",
    "email": "<email>",
    "userType": "support",
    "passKey": "<passKey>",
    "rightToWork": true,
    "mobileCountry": "<+44>",
    "mobileNo": "<number>"
  }' | jq .
```

### Create address
```bash
curl -sS "$API/address" \
  -H "content-type: application/json" \
  -H "$AUTH" \
  -d '{
    "addresses": [{
      "id": 0,
      "street": "<street>",
      "city": "<city>",
      "country": "<country>",
      "postcode": "<postcode>",
      "label": "Work location",
      "isHome": false,
      "isActive": true
    }]
  }' | jq .
```

### Create role
```bash
NOW=$(date +%s000)

curl -sS "$API/role" \
  -H "content-type: application/json" \
  -H "$AUTH" \
  -d '{
    "roles": [{
      "id": 0,
      "headline": "<headline>",
      "jobDescription": "<description>",
      "introduction": "",
      "workingHours": "<when>",
      "salary": <amount>,
      "currencyName": "GBP",
      "currencySymbol": "£",
      "paymentFrequency": { "choices": ["<frequency>"], "selectedIndex": 0 },
      "requirements": [],
      "benefits": [],
      "addressId": <ADDRESS_ID>,
      "isRemote": false,
      "isActive": true,
      "days": 30,
      "maxCrew": 1,
      "modified": '"$NOW"',
      "roleIdentifier": "openclaw-'"$NOW"'"
    }]
  }' | jq .
```

### Delete role
```bash
curl -sS -X DELETE "$API/role" \
  -H "content-type: application/json" \
  -H "$AUTH" \
  -d '{ "roles": [{ "id": <roleId> }] }' | jq .
```

### Delete address
```bash
curl -sS -X DELETE "$API/address" \
  -H "content-type: application/json" \
  -H "$AUTH" \
  -d '{ "addresses": [{ "id": <addressId> }] }' | jq .
```

### Ask Brian
```bash
curl -sS "$API/ask" \
  -H "content-type: application/json" \
  -H "$AUTH" \
  -d '{ "instructions": "Do I have any candidates?" }' | jq .
```

---

## Examples

### Example 1 — Post a shift

> **User:** I need café cover this Saturday 11–5 in Sherwood. £12/hour.

**Flow:**
1. Missing: street, postcode. Ask for them.
2. Confirm: *"Café cover — Sat 11am–5pm, Sherwood NG5 1AA — £12/hr. Shall I post it?"*
3. Collect identity (email, name, surname, mobile, passKey).
4. `POST /register` → store `API_KEY`, `PERSON_ID`.
5. `POST /address` → store `ADDRESS_ID`.
6. `POST /role` → return: *"Posted! Role ID 1042."*

### Example 2 — Check candidates

> **User:** Any candidates yet?

**Flow:**
1. If `API_KEY` not stored → ask for identity, register first.
2. `POST /ask` with `"instructions": "Do I have any candidates?"`.
3. If empty: *"Waiting for responses."*
4. Otherwise: display the candidate list as returned.

### Example 3 — Update a listing

> **User:** Change the pay to £14/hour on my café role.

**Flow:**
1. `POST /role` with the existing role `id` and updated `salary: 14`.
2. Confirm: *"Updated — café cover now shows £14/hr."*

### Example 4 — Remove a listing

> **User:** Take down the café role.

**Flow:**
1. `DELETE /role` with the role `id`.
2. Confirm: *"Removed."*