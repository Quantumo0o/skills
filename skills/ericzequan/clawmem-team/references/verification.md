# Verification Reference

Use this reference to verify a Team against its blueprint.

## Verification layers

### 1. Structure

Confirm the expected:
- org
- repos
- teams
- members
- collaborators

### 2. Access

Confirm each actor has the intended access:
- read
- write
- admin

If access is missing, inspect whether the gap is caused by:
- missing membership
- missing team-repo grant
- pending invitation
- wrong repo target

### 3. Contract

Confirm the canonical Team artifact exists and matches the blueprint:
- same roles
- same repo purposes
- same workflow contract
- same verification target

### 4. Happy path

Run one minimal workflow proof:
- create or inspect one queue task
- create or inspect one review request
- verify one actor can act and one result can be observed

## Result format

Return:
- `ready` when all required checks pass
- `blocked` when the Team cannot be used
- `partial` when the Team exists but one or more required steps remain

Then list the smallest repair actions needed.
