# Data Source Connection Patterns

## Turso (LibSQL / SQLite Cloud)

Query via HTTP API:

```bash
curl -s -X POST "https://[DB_NAME]-[USERNAME].[REGION].turso.io/v2/pipeline" \
  -H "Authorization: Bearer [AUTH_TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{"requests":[{"type":"execute","stmt":{"sql":"SELECT * FROM bookings ORDER BY created_at DESC"}},{"type":"close"}]}'
```

Parameterized queries (prevent SQL injection):

```json
{
  "requests": [
    {
      "type": "execute",
      "stmt": {
        "sql": "SELECT * FROM bookings WHERE id = ?",
        "args": [{"type": "integer", "value": "1"}]
      }
    },
    {"type": "close"}
  ]
}
```

Text args: `{"type": "text", "value": "email@example.com"}`

### Schema setup (if creating from scratch)

```sql
CREATE TABLE IF NOT EXISTS bookings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  service TEXT NOT NULL,
  appointment_datetime_local TEXT NOT NULL,
  appointment_datetime_utc TEXT NOT NULL,
  created_at TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_bookings_email_utc
  ON bookings(email, appointment_datetime_utc);

CREATE TABLE IF NOT EXISTS booking_locks (
  email TEXT PRIMARY KEY
);
```

## PostgreSQL

Connect via `psql`:

```bash
PGPASSWORD=[password] psql -h [host] -p [port] -U [user] -d [database] \
  --set=sslmode=require -c "SELECT * FROM bookings;"
```

Schema is identical to Turso but use `SERIAL PRIMARY KEY` instead of
`INTEGER PRIMARY KEY AUTOINCREMENT`, and `NOW()` instead of `datetime('now')`.

## Google Sheets

Use the Google Sheets API v4. Requires a service account JSON key.

```bash
# Read all rows
curl -s "https://sheets.googleapis.com/v4/spreadsheets/[SHEET_ID]/values/[RANGE]" \
  -H "Authorization: Bearer [ACCESS_TOKEN]"

# Append a row
curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets/[SHEET_ID]/values/[RANGE]:append?valueInputOption=RAW" \
  -H "Authorization: Bearer [ACCESS_TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{"values":[["name","email","phone","service","date","time"]]}'
```

Expected columns: Name | Email | Phone | Service | Date | Time | Status | Created

## REST APIs (Calendly, Square, Fresha)

Each platform has its own API. General pattern:

1. Authenticate (OAuth2 or API key)
2. Poll for new events: `GET /bookings?created_after=[timestamp]`
3. Update status: `PATCH /bookings/[id]` or `POST /bookings/[id]/confirm`
4. Extract customer details from response for email sending

Consult the specific platform's API docs for endpoints and auth.
