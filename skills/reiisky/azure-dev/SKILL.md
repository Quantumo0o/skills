---
name: azure-devops-pr
description: Create pull requests in Azure DevOps repositories. Use when the user wants to open, draft, or create a PR in Azure Repos.
---

# Azure DevOps PR

## Overview

This skill allows you to create pull requests in Azure DevOps Repositories via the Azure DevOps REST API. It uses a bundled script to make the API call correctly using Personal Access Tokens (PAT).

## Usage Requirements

Before creating a PR, you need to gather or infer the following information:
1. **Organization**: The Azure DevOps organization name.
2. **Project**: The Azure DevOps project name.
3. **Repository**: The repository name or ID.
4. **Source Branch**: The branch containing the changes (e.g., `feature-branch`).
5. **Target Branch**: The branch to merge into (e.g., `main`).
6. **Title**: The title of the pull request.
7. **Description**: (Optional) Details about the changes.
8. **PAT (Personal Access Token)**: A token with `Code (Read & Write)` scope. *NEVER output the PAT to the user in plain text.*

**Note on credentials:** Prefer using environment variables (`AZURE_DEVOPS_ORG`, `AZURE_DEVOPS_PROJECT`, `AZURE_DEVOPS_REPO`, `AZURE_DEVOPS_PAT`) if they are available in the workspace. Otherwise, ask the user securely or run a command to fetch them if instructed.

## Execution

Use the bundled Node.js script to create the pull request. Ensure you execute it using `node`.

```bash
node ${skill.dir}/scripts/create_pr.mjs \
  --org "ORG_NAME" \
  --project "PROJECT_NAME" \
  --repo "REPO_NAME" \
  --pat "PERSONAL_ACCESS_TOKEN" \
  --source "source-branch" \
  --target "target-branch" \
  --title "My Pull Request Title" \
  --description "Description of changes" \
  [--draft]
```

**Script Arguments:**
- `--org`: Your Azure DevOps organization name.
- `--project`: Your Azure DevOps project name.
- `--repo`: Your repository name.
- `--pat`: Your Personal Access Token.
- `--source`: The branch to merge from (e.g., `feature-branch`).
- `--target`: The branch to merge into (e.g., `main`).
- `--title`: The title for the PR.
- `--description`: Optional. The markdown description for the PR.
- `--draft`: Optional. Pass this flag to create the PR as a draft.

**Example execution:**
```bash
node ${skill.dir}/scripts/create_pr.mjs --org "my-org" --project "my-project" --repo "my-repo" --pat "$AZURE_PAT" --source "feature/add-auth" --target "main" --title "Add Authentication" --description "Adds JWT auth mechanism."
```

## Handling Errors

- **401 Unauthorized:** The PAT is missing, invalid, or expired.
- **404 Not Found:** The organization, project, or repository may be incorrect.
- **400 Bad Request:** Likely invalid branch names. The script automatically prefixes branches with `refs/heads/` if missing, but ensure the source branch exists on the remote and has pushed changes.
