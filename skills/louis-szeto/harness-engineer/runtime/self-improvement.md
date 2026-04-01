# SELF-IMPROVEMENT ENGINE

Every failure is an opportunity to make the system better. This is not optional.

---

## THE RULE
Every failure must produce **at least one** of:
- A new **constraint** appended to `references/constraints.md`
- A new **test** in `tests/`
- A new **documentation** entry in `docs/`

A failure that produces none of these is an incomplete cycle.

---

## HARD LIMITS ON SELF-IMPROVEMENT

The self-improvement engine may **never**:
- Modify `SKILL.md`, `CONFIG.yaml`, or any file under `agents/`, `runtime/`, or `tools/`
- Delete or overwrite existing entries in `references/constraints.md`
- Relax or remove an existing constraint (only humans may do this)
- Change retry limits, loop mode, or parallelism settings
- Grant itself or any agent additional permissions

**Self-improvement is append-only and additive.** The harness becomes more constrained
over time, never less. If a constraint appears to be wrong, a human must review and
remove it -- the system cannot remove its own guardrails.

---

## IMPROVEMENT PROCESS

```
failure
  => root cause analysis (debugger_agent)
  => identify system gap (missing constraint, test, or doc)
  => create fix (implementer_agent / doc_writer_agent)
  => verify fix eliminates failure
  => update MEMORY.md with Prevention Rule
  => re-deploy
```

---

## IMPROVEMENT TRIGGERS

| Signal | Action |
|--------|--------|
| Test failure | New regression test + constraint |
| Security scan finding | New security rule in `references/constraints.md` |
| Performance regression | New benchmark baseline + optimization note |
| Doc gap discovered | Immediate doc update before next cycle |
| Same failure twice | Mandatory Prevention Rule |

---

## RESULT
Over time, agents accumulate constraints and tests that prevent classes of errors entirely.
The system's regression rate asymptotically approaches zero.
Quality improves continuously. "Done" is not a state -- it is a direction.
