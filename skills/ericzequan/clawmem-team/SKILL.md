---
name: clawmem-team
description: Single entry skill for ClawMem Team workflows. Use when a user wants to design, bootstrap, verify, adapt, or choose a Team workflow on top of ClawMem, including custom Team design, repo and access planning, main/worker/summary queue setups, reviewing flows, and step-by-step Team onboarding.
---

# ClawMem Team

Use this skill as the single entry point for ClawMem Team requests.

Keep the product boundary explicit:
- ClawMem plugin provides memory and atomic collaboration tools.
- This skill defines how those primitives are composed into a Team workflow.

## Select the right path

1. Confirm the user wants Team design, Team setup, Team verification, or a Team template.
2. If this is only an ordinary memory request, stay on the bundled `clawmem` skill instead.
3. Classify the Team request into one of three paths:
   - `main / worker / summary queue`
   - `reviewing`
   - `custom`

## Read the right reference

- For any Team blueprint, read [references/blueprint.md](references/blueprint.md).
- For Team bootstrap and mutation sequencing, read [references/bootstrap.md](references/bootstrap.md).
- For readiness checks and end-to-end proof, read [references/verification.md](references/verification.md).
- For the main/worker/summary queue template, read [references/templates/main-worker-summary-queue.md](references/templates/main-worker-summary-queue.md).
- For the reviewing template, read [references/templates/reviewing.md](references/templates/reviewing.md).

## Workflow

1. Identify the user's goal, constraints, participants, and preferred collaboration style.
2. Choose a template when it clearly fits. Otherwise design a custom Team.
3. Produce one explicit Team blueprint using `references/blueprint.md`.
4. Keep the Team contract explicit in the blueprint:
   - roles
   - repos
   - access model
   - issue or comment protocol
   - canonical Team artifact
   - verification path
5. If the user approves actual changes, bootstrap the Team using `references/bootstrap.md`.
6. When the Team is configured, verify it using `references/verification.md`.
7. If the user wants a demo, seed only one minimal workflow object.

## Decision rules

- Prefer a template when the user asks for a common Team shape.
- Prefer custom design when the user describes a unique workflow, org boundary, or access model.
- Ask for clarification only when the goal, participants, or execution model is still ambiguous after the first pass.
- Do not invent a hidden Team protocol inside the plugin. If a protocol is needed, make it explicit in the blueprint or template output.
- Do not refer to other sibling skills. This single skill owns the full Team journey.
- Keep one canonical Team artifact. Do not scatter the Team contract across multiple uncoordinated files or issues.
- Use ClawMem collaboration tools first. Use shell or raw API only when the required operation is not exposed by tools.
- Require explicit approval before writes that change orgs, teams, invites, memberships, or permissions.

## Required output

Before ending any major phase, summarize:
- chosen path
- why that path fits
- the blueprint or mutation plan
- the next concrete step
