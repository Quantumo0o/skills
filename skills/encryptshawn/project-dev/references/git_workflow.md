# Git Workflow — Branch and Commit Standards

This document defines how you interact with git throughout the development process. Your git skill handles the mechanics of these commands — this document tells you what to do and when.

## Branch Creation

### Always Start from Latest Main

Every new task gets a fresh branch from the latest main:

```
git checkout main
git pull origin main
git checkout -b feature/{task-id}-{role}-{slug}
```

### Branch Naming Convention

Format: `feature/{task-id}-{role}-{slug}`

| Component | Description | Example |
|---|---|---|
| `feature/` | Prefix — always "feature/" for task work | `feature/` |
| `{task-id}` | The Asana task ID or the spec section ID | `FE-003` or `BE-012` |
| `{role}` | `fe` for Frontend, `be` for Backend | `fe` |
| `{slug}` | Brief kebab-case description (2-4 words) | `user-registration-form` |

**Full examples:**
- `feature/FE-003-fe-user-registration-form`
- `feature/BE-012-be-auth-api-endpoints`
- `feature/BUG-047-fe-login-redirect-fix`

**Why this matters:**
- The task ID in the branch name lets the Engineer link PRs back to spec sections during review
- The role prefix (`fe`/`be`) prevents naming collisions when FE and BE are working related tasks
- The slug makes branches human-readable in git log

### One Branch Per Task

Never bundle multiple tasks on one branch. Even if two tasks seem related, separate branches mean:
- Cleaner PRs that are easier for QA to review
- Independent merging — one task doesn't block another if QA finds issues
- Clear audit trail from task → branch → PR → merge

## During Development

### Commit Frequently, Commit Meaningfully

**Commit frequency:** Commit after each meaningful unit of progress — a completed function, a working component, a passing test. Don't wait until "everything is done" to commit.

**Commit message format:**
```
[{task-id}] Brief description of what this commit does
```

**Examples:**
- `[FE-003] Add user registration form with email/password fields`
- `[FE-003] Add client-side validation for registration inputs`
- `[BE-012] Create POST /api/auth/register endpoint`
- `[BUG-047] Fix redirect loop on failed login attempt`

**What makes a good commit message:**
- Starts with the task ID in brackets — creates an audit trail the Engineer and PM can follow
- Uses imperative mood ("Add" not "Added", "Fix" not "Fixed")
- Describes what changed, not why (the "why" is in the task description and PR)
- Is specific enough that reading the git log tells a story of the implementation

### What Never Gets Committed

**Never commit any of the following:**
- API keys, tokens, passwords, or secrets of any kind
- `.env` files or environment configuration with real values
- Database connection strings with credentials
- Private keys or certificates
- Large binary files (images, videos, compiled assets) unless the spec explicitly requires them in the repo

If you accidentally commit a secret, do NOT just delete it in a follow-up commit — the secret is now in git history. Notify the Engineer immediately so they can rotate the credential and clean the history.

### Keeping Your Branch Current

Pull from main regularly to avoid painful merge conflicts at PR time:

```
git checkout main
git pull origin main
git checkout feature/{your-branch}
git merge main
```

**When to sync:** At minimum, sync before creating your PR. Ideally, sync daily if you're working on a multi-day task. If other developers are merging frequently, sync more often.

**If you hit merge conflicts:**
1. Resolve them carefully — understand what the other developer changed and why before overwriting
2. If the conflict is in code you don't understand (e.g., another developer's area), do NOT guess. Ask the Engineer or the other developer.
3. After resolving, test that your feature still works correctly

## PR Creation

### PRs Always Target Main

Your PR should merge into `main`. If the project uses a different target branch (e.g., `develop`), the Engineer will specify this — default to `main` unless told otherwise.

### PR Title Format

```
[{task-id}] Brief description of what this implements
```

Examples:
- `[FE-003] User registration form with validation`
- `[BE-012] Authentication API endpoints`
- `[BUG-047] Fix login redirect loop`

### PR Description

Follow the template in `pr_and_qa_handoff.md`. The PR description is your handoff document to QA — it needs to be thorough enough that QA can test your work without asking you what to do.

### Before Opening the PR

Final checks:
- [ ] Branch is up to date with main (no unresolved conflicts)
- [ ] All acceptance criteria from the task are addressed
- [ ] Code runs cleanly — no build errors, no unhandled exceptions in the feature path
- [ ] No secrets or env files in the diff
- [ ] Commit history tells a coherent story (consider squashing noise commits if your git skill supports it)
- [ ] PR description template is fully filled out (see `pr_and_qa_handoff.md`)

## After the PR is Open

- **Do not force-push** to the branch after QA has started reviewing (unless QA requests it) — it invalidates their review state
- **Do push fixes** to the same branch when addressing QA feedback — this keeps the review context intact
- **Do not merge your own PR** — QA merges after they approve. This is an ownership boundary that ensures quality gating is real.

## Branch Cleanup

After QA merges your PR:
- The branch can be deleted (most git platforms offer this automatically on merge)
- If you need to reference the old branch for any reason, it's preserved in the PR history
- Start fresh from main for your next task
