# Azure DevOps PR Skill for Gemini CLI

This is a custom skill for the [Gemini CLI](https://github.com/google/gemini-cli) that equips the AI agent with the ability to create pull requests in Azure DevOps repositories using the Azure DevOps REST API (v7.1).

## Prerequisites

- [Node.js](https://nodejs.org/) installed (for running the bundled API script).
- An **Azure DevOps Personal Access Token (PAT)** with `Code (Read & Write)` scope.

## Environment Variables

For the best experience, set these environment variables in your terminal or a `.env` file before launching Gemini CLI so the agent doesn't have to ask you for them every time:

```bash
export AZURE_DEVOPS_ORG="your-organization"
export AZURE_DEVOPS_PROJECT="your-project"
export AZURE_DEVOPS_REPO="your-repository"
export AZURE_DEVOPS_PAT="your-personal-access-token"
```

## Installation

You can install the packaged `.skill` file using the Gemini CLI:

**1. Install globally (available in all directories):**
```bash
gemini skills install azure-devops-pr.skill --scope user
```

**2. Or install locally (only active in this workspace):**
```bash
gemini skills install azure-devops-pr.skill --scope workspace
```

After installing, run `/skills reload` inside an active Gemini CLI interactive session to load the new skill.

## Usage

Once the skill is loaded, you can ask Gemini CLI to create pull requests using natural language. For example:

- *"Create a PR for the `feature/add-auth` branch into `main` with the title 'Add JWT Authentication'."*
- *"Open a draft PR for my current branch targeting `develop`."*
- *"Can you make a pull request in Azure DevOps from `bugfix/typo` to `main`? Set the description to 'Fixes header typo'."*

The agent will automatically map your request to the required API payload and execute the PR creation securely.

---

*Note: As per Gemini CLI skill guidelines, `README.md` and other user-facing documentation are kept outside of the skill directory itself to optimize the AI's context window. The agent relies entirely on the `SKILL.md` file for its instructions.*
