# clawhub-plugin-packager

A ClawHub / OpenClaw skill for turning rough plugin ideas, partial code, or broken package material into one publish-ready native plugin package zip plus one separate plain-text critique file.

## Display Name
ClawHub Plugin Packager

## Goal
Take any combination of:

- a user description
- existing plugin files
- partial package metadata
- draft naming
- tool/provider/channel behavior notes
- API/auth requirements
- publishing notes

and turn it into exactly two user-facing outputs for the plugin-generation job:

1. a publish-ready plugin package zip
2. a separate plain-text critique file

## Core philosophy

This skill is built for low-friction handoff.

The user should be able to hand over draft material and receive:

- a completed plugin package zip
- a separate critique file
- a clear summary of what was inferred, fixed, changed, or flagged

The package is the main product.  
The critique file is the support layer.

## Unified identity

By default this package keeps one identity everywhere:

- Display name: `ClawHub Plugin Packager`
- Slug: `clawhub-plugin-packager`
- Runtime name: `clawhub-plugin-packager`
- Folder name: `clawhub-plugin-packager`
- Skill key: `clawhub-plugin-packager`

## Invocation

Recommended invocation:

- `/skill clawhub-plugin-packager`

Direct skill alias:

- `/clawhub-plugin-packager`

## What it does

This skill:

- audits what is already present
- identifies what is missing
- fills gaps using safe defaults when needed
- repairs naming and manifest issues
- selects the narrowest sufficient native plugin type
- builds the final plugin folder
- performs a second-pass self-review
- produces one pure plugin package zip
- produces one separate plain-text critique file

## Default plugin target

Unless the user specifies otherwise, this skill generates a **native TypeScript tool plugin** with:

- `package.json`
- `openclaw.plugin.json`
- `index.ts`
- `README.md`
- `tsconfig.json`

## Release boundary

This skill zip is the full release artifact for the skill itself.

The separate critique-file rule applies to downstream plugin-generation jobs, not to the packaging of this skill release.

## Included support files in this skill package

These are part of the skill and can be kept in the published skill bundle:

- `PLUGIN-SPEC-TEMPLATE.yaml`
- `REVIEW-CHECKLIST.txt`
- `REVIEW-RECORD-TEMPLATE.txt`
- `PORTABILITY.md`
- `examples/`
- `templates/`

## Publish fields

- Slug: `clawhub-plugin-packager`
- Runtime name: `clawhub-plugin-packager`
- Skill key: `clawhub-plugin-packager`
- Version: `1.0.0`
- Suggested tags: `latest, clawhub, openclaw, plugin, packaging, codegen`

## Maintainer notes

- Keep the generated plugin zip free of critique material.
- Keep critique outside the plugin zip by default.
- Prefer native plugins over bundles unless the user explicitly requests a bundle.
- Prefer minimal publishable output over speculative overbuilding.
- Preserve inference-first behavior.
