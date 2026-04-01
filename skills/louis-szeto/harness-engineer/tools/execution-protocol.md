# TOOL EXECUTION PROTOCOL

Every tool call follows this exact lifecycle. No exceptions.

---

## STEP 1: REQUEST
Agent submits a Tool Request with all fields filled:

```
TOOL:            <tool name from TOOL_REGISTRY.md>
INPUT:           <exact parameters>
EXPECTED OUTPUT: <what a successful result looks like>
VALIDATION:      <how the agent will verify correctness>
PLAN REF:        <PLAN-NNN.md that authorized this action>
```

---

## STEP 2: ROUTE
Tool Router validates the request (see `tools/tool-router.md`):
- Input schema is correct.
- Tool is registered.
- Action is not blocked.
- Rate limit has not been exceeded.

---

## STEP 3: EXECUTE
Tool Router executes the tool and returns a normalized response (see router output format).

---

## STEP 4: VALIDATE
**The calling agent MUST:**
- Check `status` field -- treat anything other than `"success"` as a failure.
- Compare `data` against `EXPECTED OUTPUT` from the request.
- If mismatch: retry (up to 3 times) with adjusted input.
- If still failing after 3 retries: log to `MEMORY.md`, dispatch `debugger_agent`.

---

## STEP 5: LOG
Tool interaction **metadata** is stored in `docs/generated/tool-logs/`. Logs must contain
only: tool name, timestamp, status (success/failure/blocked), and a one-line outcome
summary. Logs must never contain:
- Raw tool input values (file contents, query strings, log text, API responses)
- Environment variables, tokens, passwords, or any credential-shaped string
- Application log lines (which may contain PII, keys, or stack traces with secrets)
- Full web_search responses

**Web search findings**: results from `web_search` must be staged in
`docs/generated/search-staging/` as candidate references. A human operator reviews and
manually promotes useful findings to `docs/references/`. Agents must not write directly
to `docs/references/`.

---

## RETRY RULES
- Retry limit: 3 per tool call (overrides `CONFIG.yaml` for tool-level granularity).
- On retry: modify input if possible; do not retry identical failing calls blindly.
- On final failure: do not halt -- log, dispatch debugger, and continue other tasks.
