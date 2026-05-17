---
name: clawhub-plugin-packager
description: "Turn rough, partial, or missing plugin requirements into one publish-ready native OpenClaw/ClawHub plugin package zip plus one separate plain-text critique file using inference-first packaging."
version: "1.0.0"
user-invocable: true
disable-model-invocation: true
metadata:
  openclaw:
    emoji: "🧩"
    skillKey: "clawhub-plugin-packager"
---

# ClawHub Plugin Packager

Use this skill when the user wants to create, repair, review, rename, repackage, or republish a **native OpenClaw / ClawHub plugin package**.

## Product promise

This skill makes the **plugin package first**.

Then it makes the **separate critique file** for the generated plugin job.

The plugin package is the main product.  
The critique file is the support layer.

## Unified identity rule

By default this skill keeps one aligned identity across plugin surfaces unless the user explicitly requests a split:

- package name
- plugin id
- publish name
- folder name
- README title
- GitHub repo name when inferable

Prefer one clean identity over clever naming splits.

## Core job

This skill turns user input, existing plugin files, repo notes, or partial specs into a **publish-ready native OpenClaw plugin package**.

It is designed to:

- inspect what is present
- infer what is missing when reasonable
- repair inconsistencies
- build the package anyway when a safe best-effort package is possible
- self-audit the result
- return exactly one plugin package zip plus one separate plain-text critique file

## Operating stance

This skill is designed for **low-friction handoff**.

When the user provides material:

- inspect what is there
- infer what is missing when reasonable
- choose the best safe course based on current knowledge
- avoid unnecessary clarification loops
- return a concrete plugin package plus critique

Prefer **statements** over **questions**.

If something is missing but inferable:

- infer it
- note the inference
- keep moving

If something is risky, ambiguous, or likely to affect publishability:

- still produce the package when a safe best-effort package is possible
- highlight the issue clearly in the critique file
- mark it for human review

Do not stop at “more info needed” when a reasonable plugin package can still be built.

## Exact output contract

Always produce exactly **two user-facing deliverables** for the plugin-generation job.

### A. Plugin package zip

A zip-ready native OpenClaw plugin folder containing **only** files that directly belong to the plugin as a release artifact.

This bundle must include the files required for the chosen plugin type.  
For a standard native code plugin, that usually means:

- `package.json`
- `openclaw.plugin.json`
- runtime entrypoint such as `index.ts` or `index.js`
- `README.md`

Add other files only when they genuinely belong to the plugin, such as:

- `tsconfig.json`
- `src/`
- `schemas/`
- `assets/`
- `.github/workflows/package-publish.yml`
- bundled skill folders declared by the plugin manifest

Do **not** include inside the plugin zip:

- critique notes
- inference notes
- packaging commentary
- discussion transcripts
- release review records
- job-specific handoff notes

The plugin zip should look like it was created for the plugin itself, not for the conversation that created it.

### B. Separate plain-text critique file

A separate critique file in plain text.

Preferred format:

- `.txt`

This critique file should say:

- what inputs were provided
- what information was missing
- what assumptions were made
- what was added
- what was edited
- what was removed
- what was inferred
- what still deserves human review
- whether the package appears publish-ready
- the final publish/install handoff details

The critique file must remain **outside** the plugin zip unless the user explicitly asks to embed it.

## This skill's own release boundary

This skill package is its own standalone ClawHub skill release artifact.

The “separate critique file” rule applies to **future plugin-generation jobs performed by this skill**, not to the distribution of this skill itself.

Do not generate a sidecar critique file for this skill unless the user explicitly asks for a review of the skill package.

## Default plugin strategy

Unless the user clearly specifies otherwise:

1. Prefer a **native OpenClaw plugin**, not a bundle.
2. Prefer a **tool plugin** when the plugin type is underspecified.
3. Use **TypeScript + ESM** unless the user clearly asks for JavaScript.
4. Keep the first output minimal, publishable, and easy to extend.
5. Mark dangerous or side-effectful tools as optional when a narrower safe default exists.
6. Generate empty-but-valid config schema when no config is needed.

## Plugin type selection

Pick the narrowest sufficient native plugin type.

### 1. Tool plugin
Use when the package should expose one or more agent tools.

Typical outputs:

- `package.json`
- `openclaw.plugin.json`
- `index.ts`
- `tsconfig.json`
- `README.md`

### 2. Provider plugin
Use when the package should add a model provider, speech provider, or similar runtime provider surface.

Typical outputs:

- `package.json`
- `openclaw.plugin.json`
- `index.ts`
- provider registration code
- `README.md`

### 3. Channel plugin
Use when the package should add a channel or message transport surface.

Typical outputs:

- `package.json`
- `openclaw.plugin.json`
- `index.ts`
- `setup-entry.ts`
- channel registration/setup code
- `README.md`

### 4. Mixed plugin
Use when the user explicitly needs a combined capability surface.  
Keep the code and manifest structure explicit and easy to audit.

## Packaging workflow

### Step 1 — Inspect
Look at all provided material:

- text prompts
- existing plugin files
- `package.json`
- `openclaw.plugin.json`
- code entrypoints
- repo notes
- intended name
- intended id
- intended tool/provider/channel behavior
- docs about APIs or auth
- prior plugin artifacts if relevant

### Step 2 — Determine completeness
Check whether the package has enough information for:

- package name
- plugin id
- plugin type
- version
- description
- runtime entrypoint
- config requirements
- external API/auth expectations
- publish metadata
- compatibility metadata
- README handoff
- file set

### Step 3 — Infer or repair
If something is missing or inconsistent:

- choose the best safe default
- align naming surfaces
- repair parser-risky JSON or YAML
- generate missing files
- normalize compatibility/build metadata
- preserve intended behavior whenever possible

### Step 4 — Build the package
Create the final plugin folder and final file contents.

### Step 5 — Self-audit
Run a second-pass review using `REVIEW-CHECKLIST.txt`.

### Step 6 — Deliver
Deliver exactly two user-facing artifacts:

- the final plugin package zip
- the separate critique file built from `REVIEW-RECORD-TEMPLATE.txt`

Then provide a short summary telling the user:

- here is the plugin package
- here is the critique file
- here is what was inferred
- here is what was fixed
- here is what may still deserve review

## Native plugin rules

When generating a native OpenClaw plugin package, ensure the package includes:

- a valid `openclaw.plugin.json`
- an inline `configSchema`, even if empty
- explicit compatibility/build metadata in `package.json`
- a real runtime entrypoint
- a README that explains install, enable, config, and publish flow

If the user asks for bundled skills inside the plugin, place them inside a declared skill directory and reference them from the plugin manifest.

## Inference rules

When the user does not specify a value, infer in this order:

### Name and id
- derive a lowercase URL-safe package name from the requested title
- use the same base string for plugin id unless a stronger existing id is present

### Version
- default to `1.0.0` for first publishable output
- if repairing an existing package, preserve the provided version unless there is a strong reason to change it

### Plugin type
- default to native **tool plugin**

### Language
- default to **TypeScript**
- fall back to JavaScript only when the user asks or when a JS-only package is clearly better

### Config
- default to an empty object schema when no config is required

### Docs
- always include a usable `README.md`

## Output style for generated plugin package

The generated plugin package should be:

- publishable first
- minimal but real
- extendable
- readable by a human maintainer
- explicit about inferred assumptions
- free of critique material inside the zip

## Support files included in this skill package

These files are part of this skill itself and may be used as references during packaging:

- `PLUGIN-SPEC-TEMPLATE.yaml`
- `REVIEW-CHECKLIST.txt`
- `REVIEW-RECORD-TEMPLATE.txt`
- `PORTABILITY.md`
- `examples/`
- `templates/`

## Invocation

Preferred invocation:

- `/skill clawhub-plugin-packager`

Direct alias:

- `/clawhub-plugin-packager`

If the direct alias does not trigger on a given surface, prefer `/skill clawhub-plugin-packager`.

## Visibility rule

Do not bury final deliverables in an internal-only path without clearly surfacing them.
