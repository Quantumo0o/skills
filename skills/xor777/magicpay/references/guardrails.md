# MagicPay Boundaries

## What This Skill Owns

- Attach to a prepared browser page.
- Start or continue the workflow session for that page.
- Discover the supported protected form.
- Request approval, poll, and fill the protected values safely.
- Retry submit only when the guarded fill path explicitly leaves work undone.

## Readiness Rules

- Use `magicpay status` before a new protected-form task.
- If `status` reports a missing or invalid API key, run `magicpay init`.
- If `status` reports `cliUpdate`, use only
  `npm i -g @mercuryo-ai/magicpay-cli@latest`, then rerun `status`.
- Use `doctor` only when local config still looks broken after `init`.

## Protected-Form Rules

- Start from a current `find-form` result, not from stale assumptions.
- Do not call `request-secret` without a matching `fillRef` and
  `storedSecretRef`.
- Treat `poll-secret` as a state check, not as payload delivery.
- Run `fill-secret` only when the request is ready and the page still matches
  the approved request context.
- Treat `submit-form` as manual recovery, not as the default next step.
- Never reuse a claimed request.

## Secrecy And Safety

- Never type, log, summarize, or echo protected values manually.
- Base progress claims on the visible form state.
- After page-level changes, rerun `find-form` before acting on old bindings.

## Ask The User When

- the prepared page context is missing;
- the form remains ambiguous;
- approval reaches a terminal blocked state;
- client-side validation or merchant-specific recovery needs a human choice.
