---
name: ghosthand
description: Use this skill when operating Ghosthand, a local Android control runtime exposed over a loopback HTTP API for OpenClaw or another agent. Trigger it for Ghosthand tasks involving runtime or capability checks, structured UI inspection, selector planning, semantic clicks, coordinate taps, text input, scrolling, app launch, wait conditions, clipboard transfer, notifications, screenshots, or debugging Ghosthand-specific route behavior such as partial-output warnings, snapshot-scoped node IDs, or text vs content description vs resource-id selection.
---

# Ghosthand

Use this skill to operate Ghosthand as an Android agent substrate.

Ghosthand is not generic Android advice. It is a local runtime with a route-based control surface. Use this skill only when the task is actually about Ghosthand routes, Ghosthand capability state, or acting through Ghosthand.

## What Ghosthand is

Ghosthand exposes a local HTTP API for Android observation and control. The important categories are:

- runtime and health: `/ping`, `/health`, `/state`, `/device`, `/foreground`, `/commands`
- structured UI inspection: `/screen`, `/tree`, `/focused`
- semantic or coordinate interaction: `/find`, `/click`, `/tap`, `/input`, `/setText`, `/scroll`, `/swipe`, `/longpress`, `/gesture`
- app and navigation control: `/launch`, `/back`, `/home`, `/recents`
- sensing and transport: `/screenshot`, `/wait`, `/clipboard`, `/notify`

Treat `/commands` as the current machine-readable capability catalog when route details matter.

## When to use this skill

Use it when the task requires any of the following:

- checking whether Ghosthand is running or ready
- checking whether a capability is both authorized by Android and allowed by Ghosthand policy
- inspecting the current Android surface before acting
- finding or clicking UI targets by `text`, `desc`, or `id`
- recovering from Ghosthand misses or ambiguous action results
- using Ghosthand to type, scroll, swipe, wait, launch apps, read clipboard, or read notifications
- debugging Ghosthand-specific behaviors such as partial output, stale assumptions about selectors, or snapshot-scoped node IDs

Do not use it for:

- generic Android usage advice unrelated to Ghosthand
- root-only methods that Ghosthand does not expose
- imaginary routes or undocumented behavior when `/commands` can answer directly

## Operating model

### 1. Start from truth, not intent

Before acting, establish three things:

1. Is Ghosthand alive and usable?
2. What surface is actually visible now?
3. Which selector surface is most plausible for the target?

Typical order:

1. read `/health` or `/state`
2. read `/commands` if route shape or selector support is uncertain
3. read `/screen` for the current actionable surface
4. only then choose `/find`, `/click`, or `/tap`

### 2. Capability access has two layers

A capability is usable only when both are true:

- Android/system authorization exists
- Ghosthand policy allows the capability

Do not confuse “permission granted” with “usable now”. Read `/state` before diagnosing failures, especially for accessibility and screenshot capture.

### 3. Node IDs are snapshot-scoped

Treat `nodeId` as ephemeral. Do not cache it across fresh observations unless the snapshot context is clearly the same. Prefer re-resolving via `/screen`, `/find`, or `/click` instead of assuming old node IDs remain valid.

## Primitive selection

### `/screen`

Use `/screen` first when you need a compact actionable view.

Use it to answer:

- what is visible now
- which elements are actionable or editable
- whether coordinates are trustworthy enough for `/tap`
- whether the current surface even contains the target

If `/screen` reports `partialOutput=true` or warnings, do not assume you saw the whole surface. Escalate to `/tree` or re-check the target before blaming the app.

### `/tree`

Use `/tree` when you need fuller structure, raw hierarchy, or to inspect why `/screen` may have omitted or shaped output. Use it for diagnosis, not as your default first read.

### `/find`

Use `/find` when you already have a selector hypothesis and want a bounded lookup.

Prefer it when you need:

- selector testing before interaction
- disambiguation by `index`
- confirmation that a target exists before a coordinate fallback

A miss usually means one of four things:

- wrong screen
- wrong selector surface
- wrong match semantics
- target not exposed the way you assumed

### `/click`

Prefer `/click` over `/tap` when you have a plausible semantic target. Ghosthand can resolve wrapper targets and expose how it actually landed on an actionable node.

Use `/click` first for:

- text-labeled controls
- content-description labeled controls
- stable resource IDs
- cases where ancestor click resolution may help

### `/tap`

Use `/tap` only when coordinates come from the current trusted surface. Do not guess coordinates. Coordinate fallback is justified only after semantic targeting has narrowed the uncertainty.

### `/input` and `/setText`

Use `/input` for the focused editable field.

Use `/setText` only when you have a trusted same-snapshot editable `nodeId` and need to target that exact node.

### `/scroll` and `/swipe`

Use `/scroll` when the goal is container movement or list advancement.

Use `/swipe` when the task is truly geometric.

Do not interpret `performed=true` as proof that content changed. Check returned change fields, then verify with `/screen`, `/tree`, or `/wait`.

### `/wait`

Use `/wait` after actions that may change UI state.

There are two different uses:

- `GET /wait`: wait for UI change and inspect final settled state
- `POST /wait`: wait for a selector condition

Do not confuse `changed=false` with action failure. It only means a transition was not observed during the wait window. Re-check the final surface before concluding the action failed.

### `/launch`

Use `/launch` when the package name is known. It is usually better than visually hunting an app icon from home.

### `/clipboard`, `/notify`, `/screenshot`

Use `/clipboard` as a transport primitive for long text or repeated entry.

Use `/notify` to read or post local notifications only when the task is explicitly notification-related.

Use `/screenshot` when visual truth is needed and structured UI output is insufficient, ambiguous, or suspected stale.

## Selector judgment

Selectors are not interchangeable.

### `text`

Use `text` when the visible label is likely the actual text field of the node.

### `desc`

Use `desc` when the control is icon-like, accessibility-labeled, nav-like, or visibly sparse. Many controls that look label-based are actually better matched through content description.

### `id`

Use `id` when a meaningful `resourceId` is present. This is often the strongest selector.

### Exact vs contains

Do not over-read exact-match misses.

If the visible phrase may be part of a longer text block, retry with a contains-style strategy where the route supports it. A visible phrase on screen is not proof that exact text lookup should succeed.

## Recovery rules

When a Ghosthand action misses, do not branch into random retries. Make one bounded correction:

- re-read `/screen`
- switch `text` to `desc` or `id`
- switch exact semantics to contains semantics when justified
- move from `/click` to `/tap` only after trustworthy coordinates exist
- use `/wait` to settle state before the next action

Repeated misses should be classified, not brute-forced.

## Minimal workflows

### Check whether Ghosthand is ready

1. read `/health`
2. read `/state`
3. if needed, read `/commands`

### Operate a visible control safely

1. read `/screen`
2. choose `text`, `desc`, or `id`
3. call `/click`
4. call `/wait` or re-read `/screen`
5. only use `/tap` if semantic action remains weak but coordinates are trusted

### Diagnose a miss

1. confirm Ghosthand and capability state with `/state`
2. re-read `/screen`
3. inspect selector surface mismatch
4. escalate to `/tree` if `/screen` is partial or misleading
5. retry one bounded correction

## Reporting standard

When summarizing a Ghosthand run, report only:

- what route you used
- what state changed
- whether the target was achieved
- the first narrow failing step if it was not
- the next best correction

Do not dump logs unless the task is explicitly diagnostic.

## Reference files

Detailed route notes are in `resources/references/ghosthand-api-quick-reference.md`.
