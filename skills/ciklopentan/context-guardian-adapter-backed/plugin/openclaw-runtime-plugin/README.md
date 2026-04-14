# Context Guardian Runtime Plugin

Native OpenClaw hook-only plugin that integrates `context-guardian` through the official plugin system.

## What it does

- uses official OpenClaw plugin hooks
- calls the external `context-guardian-adapter.js` CLI
- keeps durable state outside OpenClaw core
- avoids patching bundled OpenClaw files

## Lifecycle coverage

- `session_start`
- `before_prompt_build`
- `before_tool_call`
- `after_tool_call`
- `before_compaction`
- `session_end`

## Safety model

- no core patch
- no OpenClaw fork
- no direct modification of bundled runtime
- persistent storage root stays outside package directories

## Install path

This plugin can be linked or installed as a normal OpenClaw external plugin and enabled via `plugins.entries.context-guardian-runtime`.
