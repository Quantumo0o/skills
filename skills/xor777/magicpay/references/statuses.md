# MagicPay Request And Submit States

## Protected-Form Discovery

- `form_found`
  A supported protected form is available on the current page.
- `protected_form_not_found`
  The current page does not expose a supported protected form. Verify the page
  context before retrying.
- `protected_form_ambiguous`
  Several supported forms match. Surface the ambiguity and ask the user to
  choose.

## Secret Request States

- `pending`
  Approval is still outstanding. Keep polling.
- `fulfilled`
  The one-time payload is ready. Continue with `magicpay fill-secret`.
- terminal `denied`, `expired`, `failed`, or `canceled`
  Stop the protected-fill path and report the exact state.

## Fill And Submit Results

- `filled`
  Protected values were filled, but no safe automatic submit was completed.
  Inspect the refreshed page state before deciding the next manual step.
- `submitted`
  Form submission produced an observable progress signal. This can come from
  the guarded auto-submit inside `fill-secret` or from an explicit
  `submit-form` retry.
- `validation_blocked`
  The form stayed blocked by client-side validation.
- `submit_binding_stale`
  The saved submit binding is no longer live on the page.
- `no_observable_progress`
  The submit attempt produced no defensible progress signal.
