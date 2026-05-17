# Portability Notes

This package is authored as a ClawHub / OpenClaw skill first, but the operating logic also ports well to:

- a custom GPT instruction pack
- a Claude project / system prompt
- a local agent prompt pack

## Keep these invariants if you port it

- The main product is the plugin package zip.
- The critique file is separate from the plugin zip.
- Missing information is inferred whenever safe.
- The default target is a native OpenClaw plugin, not a bundle.
- The default fallback is a minimal TypeScript tool plugin.
- The generated plugin package should be publishable first, conversational never.

## Porting caution

If you port this skill to a non-ClawHub surface, keep the plugin-generation contract intact even if that surface does not understand ClawHub metadata directly.
