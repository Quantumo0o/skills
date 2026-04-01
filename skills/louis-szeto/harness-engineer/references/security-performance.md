# SECURITY & PERFORMANCE

Priority order is fixed. Security is always first.

---

## SECURITY

### Input Validation
- Validate ALL external inputs at system boundaries.
- Reject malformed input early -- never pass it deeper.
- Use allowlists over denylists where possible.

### Injection Prevention
- Parameterize all database queries.
- Sanitize before any eval, exec, or template rendering.
- Never construct SQL/shell commands via string concatenation.

### Least Privilege
- Services request only the permissions they need.
- Credentials are never hardcoded -- use environment variables or secret managers.
- File/network access is scoped to the minimum required path/host.

### Dependency Security
- Run `dependency_audit()` before every merge.
- No package with a known critical CVE ships without a mitigation plan.
- Pin dependency versions in lockfiles.

---

## PERFORMANCE

### Algorithmic Complexity
- Prefer O(n) over O(n2) for any operation on user-controlled data.
- Document time complexity in function docstrings for non-trivial algorithms.

### Memory
- Avoid unnecessary allocations in hot paths.
- Reuse buffers where safe.
- Release resources explicitly (connections, file handles, large allocations).

### I/O
- Batch external calls where possible.
- Cache results that are expensive to recompute and safe to reuse.
- Use async/non-blocking I/O for network and file operations.

### Profiling Rule
- Baseline `performance_profile()` before any optimization.
- Measure again after -- optimizations without measurements are not optimizations.
- Never optimize without confirmed correctness first.
