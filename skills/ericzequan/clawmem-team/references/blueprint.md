# Team Blueprint Reference

Use this reference to produce a consistent Team blueprint.

## Goals

The blueprint should:
- be specific enough for bootstrap
- keep conventions explicit
- avoid hiding any Team protocol inside the plugin
- be minimal enough that the user can understand and approve it

## Required sections

Return the blueprint with these sections:

### 1. Team Summary

- team name
- target outcome
- why this Team shape fits

### 2. Participants

For each participant include:
- name or agent id
- role
- responsibilities
- whether it is human, agent, or mixed

### 3. Repo Plan

For each repo include:
- repo name
- owner
- purpose
- whether it stores durable memory, workflow coordination, or both
- whether it already exists or must be created

### 4. Access Model

Include:
- organization boundary
- teams to create or reuse
- direct collaborators if any
- repo permissions by actor

### 5. Workflow Contract

Make the operating protocol explicit:
- handoff model
- issue and comment usage
- label or state conventions
- when to create, update, close, or summarize work
- where final outputs land

The plugin does not own this contract. The blueprint does.

### 6. Canonical Artifact

Choose one authoritative place for the Team contract:
- a markdown file
- a bootstrap issue
- a memory node
- another explicit artifact approved by the user

Do not create duplicate sources of truth.

### 7. Bootstrap Plan

List the exact order of work:
1. inspect existing state
2. create missing org / repo / team objects
3. set access
4. materialize the canonical artifact
5. seed the first workflow object if needed

### 8. Verification Plan

Include:
- structural checks
- access checks
- workflow happy-path check
- failure conditions

## Output style

- Prefer short sections over dense prose.
- Use stable names that can be reused during bootstrap.
- If a template inspired the blueprint, say so explicitly.
