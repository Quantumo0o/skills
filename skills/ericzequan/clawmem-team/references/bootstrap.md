# Bootstrap Reference

Use this reference to execute a Team blueprint safely.

## Order of operations

1. Inspect first.
2. Reconcile existing state with the blueprint.
3. Create missing governance objects.
4. Create missing repos.
5. Apply access and membership.
6. Create the canonical Team artifact.
7. Seed the first workflow object only if the blueprint requires it.
8. Hand off to verification.

## Inspection checklist

Inspect:
- organizations
- teams
- repo existence
- repo access
- collaborator state
- pending invitations if access is not visible yet

## Mutation rules

- Require explicit approval before writes that change orgs, teams, invites, memberships, or permissions.
- Reuse existing names when they already satisfy the blueprint.
- Do not create extra repos or teams "just in case."
- Keep one authoritative Team artifact. Do not split the contract across multiple uncoordinated places.

## Canonical artifact options

The blueprint may choose one of these:
- markdown document
- bootstrap issue
- durable memory node
- another explicit artifact

When the blueprint does not specify one, stop and ask rather than guessing.

## Seed object

If the Team needs a first runnable example, create only one seed object:
- first queue task
- first review request
- first operating note

That seed object should prove the workflow works without polluting the workspace.
