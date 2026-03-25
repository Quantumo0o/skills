#!/usr/bin/env bash
# mock/scripts/script.sh — Mock Data & API Simulation Tool
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
set -euo pipefail

SKILL_VERSION="1.0.0"
DATA_DIR="$HOME/.mock"
DATA_FILE="$DATA_DIR/data.jsonl"
CONFIG_FILE="$DATA_DIR/config.json"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"
[ -f "$CONFIG_FILE" ] || echo '{"port":8080,"delay_ms":0,"cors":true,"data_dir":"~/.mock"}' > "$CONFIG_FILE"

COMMAND="${1:-help}"

case "$COMMAND" in

  server)
    python3 << 'PYEOF'
import os, json, http.server, socketserver, re

data_file = os.environ.get("MOCK_DATA_FILE", os.path.expanduser("~/.mock/data.jsonl"))
config_file = os.environ.get("MOCK_CONFIG_FILE", os.path.expanduser("~/.mock/config.json"))
port = int(os.environ.get("MOCK_PORT", "8080"))

endpoints = {}
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("type") == "endpoint":
            key = f"{rec['method'].upper()} {rec['path']}"
            endpoints[key] = rec

responses = {}
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("type") == "response":
            responses[rec["id"]] = rec

class MockHandler(http.server.BaseHTTPRequestHandler):
    def _handle(self):
        key = f"{self.command} {self.path}"
        if key in endpoints:
            ep = endpoints[key]
            status = ep.get("status", 200)
            resp_id = ep.get("response_id", "")
            body = "{}"
            if resp_id in responses:
                body = responses[resp_id].get("body", "{}")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body.encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found", "path": self.path}).encode())

    def do_GET(self): self._handle()
    def do_POST(self): self._handle()
    def do_PUT(self): self._handle()
    def do_DELETE(self): self._handle()
    def log_message(self, fmt, *args):
        print(f"[MOCK] {self.command} {self.path} -> {args[1] if len(args) > 1 else '?'}")

print(f"Mock server starting on port {port}...")
print(f"Loaded {len(endpoints)} endpoint(s), {len(responses)} response(s)")
with socketserver.TCPServer(("", port), MockHandler) as httpd:
    httpd.serve_forever()
PYEOF
    ;;

  endpoint)
    python3 << 'PYEOF'
import os, json, uuid, datetime

data_file = os.path.expanduser("~/.mock/data.jsonl")
method = os.environ.get("MOCK_METHOD", "GET").upper()
path = os.environ.get("MOCK_PATH", "")
status = int(os.environ.get("MOCK_STATUS", "200"))
response_id = os.environ.get("MOCK_RESPONSE_ID", "")
action = os.environ.get("MOCK_ACTION", "create")
delete_id = os.environ.get("MOCK_DELETE_ID", "")

if action == "delete" and delete_id:
    lines = []
    removed = False
    with open(data_file, "r") as f:
        for line in f:
            rec = json.loads(line.strip())
            if rec.get("id") == delete_id and rec.get("type") == "endpoint":
                removed = True
            else:
                lines.append(line)
    with open(data_file, "w") as f:
        f.writelines(lines)
    print(json.dumps({"status": "deleted" if removed else "not_found", "id": delete_id}))
elif action == "list":
    with open(data_file, "r") as f:
        for line in f:
            rec = json.loads(line.strip())
            if rec.get("type") == "endpoint":
                print(json.dumps(rec))
else:
    if not path:
        print(json.dumps({"error": "MOCK_PATH is required"}))
        exit(1)
    record = {
        "id": "ep_" + uuid.uuid4().hex[:12],
        "type": "endpoint",
        "method": method,
        "path": path,
        "status": status,
        "response_id": response_id,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    with open(data_file, "a") as f:
        f.write(json.dumps(record) + "\n")
    print(json.dumps(record, indent=2))
PYEOF
    ;;

  response)
    python3 << 'PYEOF'
import os, json, uuid, datetime

data_file = os.path.expanduser("~/.mock/data.jsonl")
body = os.environ.get("MOCK_BODY", "{}")
name = os.environ.get("MOCK_NAME", "unnamed")
action = os.environ.get("MOCK_ACTION", "create")
delete_id = os.environ.get("MOCK_DELETE_ID", "")

if action == "delete" and delete_id:
    lines = []
    removed = False
    with open(data_file, "r") as f:
        for line in f:
            rec = json.loads(line.strip())
            if rec.get("id") == delete_id and rec.get("type") == "response":
                removed = True
            else:
                lines.append(line)
    with open(data_file, "w") as f:
        f.writelines(lines)
    print(json.dumps({"status": "deleted" if removed else "not_found", "id": delete_id}))
elif action == "list":
    with open(data_file, "r") as f:
        for line in f:
            rec = json.loads(line.strip())
            if rec.get("type") == "response":
                print(json.dumps(rec))
else:
    record = {
        "id": "resp_" + uuid.uuid4().hex[:12],
        "type": "response",
        "name": name,
        "body": body,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    with open(data_file, "a") as f:
        f.write(json.dumps(record) + "\n")
    print(json.dumps(record, indent=2))
PYEOF
    ;;

  record)
    python3 << 'PYEOF'
import os, json, uuid, datetime, subprocess

data_file = os.path.expanduser("~/.mock/data.jsonl")
url = os.environ.get("MOCK_URL", "")
method = os.environ.get("MOCK_METHOD", "GET").upper()
headers_str = os.environ.get("MOCK_HEADERS", "")

if not url:
    print(json.dumps({"error": "MOCK_URL is required"}))
    exit(1)

try:
    cmd = ["curl", "-s", "-X", method, "-w", "\n%{http_code}", url]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    output_lines = result.stdout.strip().rsplit("\n", 1)
    response_body = output_lines[0] if len(output_lines) > 1 else ""
    status_code = int(output_lines[-1]) if output_lines else 0
except Exception as e:
    response_body = ""
    status_code = 0
    print(json.dumps({"warning": f"curl failed: {e}"}))

record = {
    "id": "rec_" + uuid.uuid4().hex[:12],
    "type": "recording",
    "method": method,
    "url": url,
    "status_code": status_code,
    "response_body": response_body[:5000],
    "recorded_at": datetime.datetime.utcnow().isoformat() + "Z"
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
print(json.dumps(record, indent=2))
PYEOF
    ;;

  replay)
    python3 << 'PYEOF'
import os, json

data_file = os.path.expanduser("~/.mock/data.jsonl")
record_id = os.environ.get("MOCK_RECORD_ID", "")

if not record_id:
    print(json.dumps({"error": "MOCK_RECORD_ID is required"}))
    exit(1)

found = None
with open(data_file, "r") as f:
    for line in f:
        rec = json.loads(line.strip())
        if rec.get("id") == record_id and rec.get("type") == "recording":
            found = rec
            break

if found:
    print(f"Replaying {found['method']} {found['url']}")
    print(f"Status: {found.get('status_code', '?')}")
    print(f"Recorded: {found.get('recorded_at', '?')}")
    print("--- Response Body ---")
    print(found.get("response_body", ""))
else:
    print(json.dumps({"error": "Recording not found", "id": record_id}))
PYEOF
    ;;

  schema)
    python3 << 'PYEOF'
import os, json, uuid, datetime

data_file = os.path.expanduser("~/.mock/data.jsonl")
schema_name = os.environ.get("MOCK_SCHEMA_NAME", "")
schema_def = os.environ.get("MOCK_SCHEMA", "")
action = os.environ.get("MOCK_ACTION", "create")

if action == "list":
    with open(data_file, "r") as f:
        for line in f:
            rec = json.loads(line.strip())
            if rec.get("type") == "schema":
                print(json.dumps(rec))
elif action == "validate":
    schema_id = os.environ.get("MOCK_SCHEMA_ID", "")
    test_data = os.environ.get("MOCK_TEST_DATA", "{}")
    schema_rec = None
    with open(data_file, "r") as f:
        for line in f:
            rec = json.loads(line.strip())
            if rec.get("id") == schema_id:
                schema_rec = rec
                break
    if schema_rec:
        schema_obj = json.loads(schema_rec.get("schema", "{}"))
        data_obj = json.loads(test_data)
        errors = []
        props = schema_obj.get("properties", {})
        for key, spec in props.items():
            if key not in data_obj:
                errors.append(f"Missing field: {key}")
        print(json.dumps({"valid": len(errors) == 0, "errors": errors}))
    else:
        print(json.dumps({"error": "Schema not found"}))
else:
    if not schema_name:
        print(json.dumps({"error": "MOCK_SCHEMA_NAME is required"}))
        exit(1)
    record = {
        "id": "sch_" + uuid.uuid4().hex[:12],
        "type": "schema",
        "name": schema_name,
        "schema": schema_def,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    with open(data_file, "a") as f:
        f.write(json.dumps(record) + "\n")
    print(json.dumps(record, indent=2))
PYEOF
    ;;

  seed)
    python3 << 'PYEOF'
import os, json, uuid, datetime, random, string, hashlib

data_file = os.path.expanduser("~/.mock/data.jsonl")
schema_id = os.environ.get("MOCK_SCHEMA_ID", "")
count = int(os.environ.get("MOCK_COUNT", "10"))

if not schema_id:
    print(json.dumps({"error": "MOCK_SCHEMA_ID is required"}))
    exit(1)

schema_rec = None
with open(data_file, "r") as f:
    for line in f:
        rec = json.loads(line.strip())
        if rec.get("id") == schema_id and rec.get("type") == "schema":
            schema_rec = rec
            break

if not schema_rec:
    print(json.dumps({"error": "Schema not found", "id": schema_id}))
    exit(1)

schema_obj = json.loads(schema_rec.get("schema", "{}"))
props = schema_obj.get("properties", {})

first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Moore"]
domains = ["example.com", "test.org", "mock.dev", "fake.io", "demo.net"]

def gen_value(field_name, field_spec, seed_i):
    random.seed(hashlib.md5(f"{schema_id}{seed_i}{field_name}".encode()).hexdigest())
    ftype = field_spec.get("type", "string")
    fn_lower = field_name.lower()
    if ftype == "integer" or ftype == "number":
        return random.randint(1, 10000)
    elif "email" in fn_lower:
        return f"{random.choice(first_names).lower()}{random.randint(1,999)}@{random.choice(domains)}"
    elif "name" in fn_lower:
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    elif "id" in fn_lower:
        return uuid.uuid4().hex[:12]
    elif "date" in fn_lower:
        d = datetime.date(2024, random.randint(1,12), random.randint(1,28))
        return d.isoformat()
    elif "url" in fn_lower:
        return f"https://{random.choice(domains)}/{uuid.uuid4().hex[:6]}"
    elif ftype == "boolean":
        return random.choice([True, False])
    else:
        return ''.join(random.choices(string.ascii_lowercase, k=random.randint(5,15)))

generated = []
for i in range(count):
    item = {}
    for field_name, field_spec in props.items():
        item[field_name] = gen_value(field_name, field_spec, i)
    seed_record = {
        "id": "seed_" + uuid.uuid4().hex[:12],
        "type": "seed",
        "schema_id": schema_id,
        "data": item,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    generated.append(seed_record)

with open(data_file, "a") as f:
    for rec in generated:
        f.write(json.dumps(rec) + "\n")

print(json.dumps({"generated": count, "schema_id": schema_id, "sample": generated[:3]}, indent=2))
PYEOF
    ;;

  list)
    python3 << 'PYEOF'
import os, json

data_file = os.path.expanduser("~/.mock/data.jsonl")
filter_type = os.environ.get("MOCK_TYPE", "all")

records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if filter_type == "all" or rec.get("type") == filter_type:
            records.append(rec)

if not records:
    print(json.dumps({"message": "No records found", "filter": filter_type}))
else:
    summary = {}
    for r in records:
        t = r.get("type", "unknown")
        summary[t] = summary.get(t, 0) + 1
    print(f"Total records: {len(records)}")
    for t, c in sorted(summary.items()):
        print(f"  {t}: {c}")
    print("---")
    for r in records:
        compact = {"id": r["id"], "type": r["type"]}
        if "name" in r: compact["name"] = r["name"]
        if "method" in r: compact["method"] = r["method"]
        if "path" in r: compact["path"] = r["path"]
        if "url" in r: compact["url"] = r["url"]
        print(json.dumps(compact))
PYEOF
    ;;

  export)
    python3 << 'PYEOF'
import os, json

data_file = os.path.expanduser("~/.mock/data.jsonl")
output_file = os.environ.get("MOCK_OUTPUT", "")
filter_type = os.environ.get("MOCK_TYPE", "all")

records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if filter_type == "all" or rec.get("type") == filter_type:
            records.append(rec)

export_data = {"total": len(records), "filter": filter_type, "records": records}

if output_file:
    with open(output_file, "w") as f:
        json.dump(export_data, f, indent=2)
    print(json.dumps({"exported": len(records), "file": output_file}))
else:
    print(json.dumps(export_data, indent=2))
PYEOF
    ;;

  config)
    python3 << 'PYEOF'
import os, json

config_file = os.path.expanduser("~/.mock/config.json")
key = os.environ.get("MOCK_KEY", "")
value = os.environ.get("MOCK_VALUE", "")

with open(config_file, "r") as f:
    config = json.load(f)

if key and value:
    try:
        value = json.loads(value)
    except (json.JSONDecodeError, ValueError):
        pass
    config[key] = value
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    print(json.dumps({"updated": key, "value": config[key]}))
elif key:
    print(json.dumps({key: config.get(key, None)}))
else:
    print(json.dumps(config, indent=2))
PYEOF
    ;;

  help)
    cat << 'HELPEOF'
Mock — Mock Data & API Simulation Tool v1.0.0

Usage: bash scripts/script.sh <command>

Commands:
  server        Start mock HTTP server (MOCK_PORT)
  endpoint      Create/list/delete API endpoints (MOCK_METHOD, MOCK_PATH, MOCK_STATUS, MOCK_RESPONSE_ID)
  response      Define response body templates (MOCK_BODY, MOCK_NAME)
  record        Record HTTP interactions (MOCK_URL, MOCK_METHOD)
  replay        Replay recorded interactions (MOCK_RECORD_ID)
  schema        Define JSON schemas (MOCK_SCHEMA_NAME, MOCK_SCHEMA)
  seed          Generate mock data from schemas (MOCK_SCHEMA_ID, MOCK_COUNT)
  list          List all records (MOCK_TYPE to filter)
  export        Export data to file (MOCK_OUTPUT, MOCK_TYPE)
  config        View/update config (MOCK_KEY, MOCK_VALUE)
  help          Show this help message
  version       Show version

Environment Variables:
  MOCK_PORT          Server port (default: 8080)
  MOCK_METHOD        HTTP method (GET, POST, PUT, DELETE)
  MOCK_PATH          Endpoint path (e.g., /api/users)
  MOCK_STATUS        HTTP status code (default: 200)
  MOCK_RESPONSE_ID   Response template ID to attach to endpoint
  MOCK_BODY          JSON response body
  MOCK_NAME          Name for response template
  MOCK_URL           URL to record
  MOCK_RECORD_ID     Recording ID to replay
  MOCK_SCHEMA_NAME   Schema name
  MOCK_SCHEMA        JSON schema definition
  MOCK_SCHEMA_ID     Schema ID for seed generation
  MOCK_COUNT         Number of seed records (default: 10)
  MOCK_TYPE          Filter type (endpoint, response, schema, seed, recording, all)
  MOCK_OUTPUT        Output file path for export
  MOCK_ACTION        Action modifier (create, list, delete)
  MOCK_DELETE_ID     ID to delete

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
HELPEOF
    ;;

  version)
    echo "mock v${SKILL_VERSION}"
    ;;

  *)
    echo "Unknown command: $COMMAND"
    echo "Run 'bash scripts/script.sh help' for usage."
    exit 1
    ;;
esac
