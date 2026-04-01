# SENSITIVE PATH POLICY

Agents must never read, list, log, or store the contents of sensitive files.
This policy is enforced in the skill. Platform enforcement is an additional layer,
not the primary control.

---

## FORBIDDEN READ PATHS

The following path patterns are off-limits to ALL agents, including the researcher.
A matching path must be skipped silently and noted as "excluded -- sensitive" in output.

### Credential and secret files
  .env
  .env.*          (.env.local, .env.production, .env.staging, etc.)
  .envrc
  *.pem
  *.key
  *.p12
  *.pfx
  *.cer
  *.crt           (unless in a public CA bundle -- check context)
  id_rsa
  id_ed25519
  id_ecdsa
  authorized_keys
  known_hosts
  *.secret
  *credentials*   (file names containing the word "credentials")
  *secrets*       (file names containing the word "secrets")

### CI/CD and infrastructure configs (often contain tokens or cloud credentials)
  .github/workflows/*.yml     (may contain injected secrets)
  .gitlab-ci.yml
  .circleci/config.yml
  Jenkinsfile
  .travis.yml
  azure-pipelines.yml
  terraform.tfvars           (may contain cloud credentials)
  *.tfstate                  (contains sensitive infrastructure state)
  *.tfstate.backup
  .vault-token
  vault*.hcl

### Git internals
  .git/config                (may contain embedded credentials in remote URLs)
  .git/credentials
  .git/hooks/*               (executable -- do not read)

### Package manager auth files
  .npmrc                     (may contain registry tokens)
  .pypirc
  .netrc
  pip.conf                   (if in home directory)

### Application config that commonly embeds secrets
  config/database.yml
  config/secrets.yml
  config/credentials.yml.enc  (Rails encrypted credentials)
  config/master.key            (Rails master key)
  application.properties       (Spring Boot -- may contain DB passwords)
  application.yml              (Spring Boot -- may contain secrets)
  settings.py                  (Django -- check for SECRET_KEY)
  local_settings.py            (Django local overrides)

---

## ALLOWED READS (examples of what IS safe to read)

  src/**/*.ts, src/**/*.py, src/**/*.go   (source code)
  tests/**                                (test files)
  docs/**                                 (documentation)
  *.md                                    (markdown)
  package.json, pyproject.toml            (dependency manifests -- not lock files with hashes)
  tsconfig.json, .eslintrc                (tool config -- no secrets)
  Dockerfile                              (review for secrets before reading)
  docker-compose.yml                      (review for secret references before reading)

---

## RESEARCHER EXCLUSION PROTOCOL

When the researcher orchestrator scans the file structure (Phase A Step 1):

1. Run list_dir on each directory
2. Before dispatching a sub-researcher to any directory, filter its file list:
   - Remove any file matching the FORBIDDEN READ PATHS patterns above
   - Include the filtered list in the sub-researcher's scope
3. Note excluded files in RESEARCH-NNN.md under a "Excluded -- sensitive" section
4. Do NOT include the count or names of excluded files in any log that an agent
   stores in MEMORY.md (the existence of a .env file is itself sensitive context)

When a sub-researcher encounters a path matching FORBIDDEN READ PATHS mid-scan:
  - Skip it immediately
  - Do not log its contents or any value from it
  - Add one line to the Module Report: "Excluded: <pattern matched> -- sensitive path policy"

---

## CI/CD CONFIG EXCEPTION

CI/CD config files (GitHub Actions, GitLab CI, etc.) may be read for structural
analysis ONLY -- to understand the pipeline shape, not to extract values.
Rules for reading CI configs:
  - Read only the structural keys (job names, step names, trigger conditions)
  - Immediately discard any `env:` or `secrets:` sections from working memory
  - Do not log, store, or record any value from `env:` or `secrets:` sections
  - Do not pass CI config contents to MEMORY.md or tool-logs

---

## MEMORY REDACTION RULE

Before writing any entry to MEMORY.md, RESEARCH-NNN.md, GAPS-NNN.md, or any
tracking log, the agent must verify the content does not contain:

  - A file path from the FORBIDDEN READ PATHS list
  - Any value that looks like a secret (see tool-router.md redaction rule)
  - Any content extracted from a sensitive file

If uncertain: omit the value and write "redacted -- possible sensitive content".
