# MagicPay Operating Guide

This reference expands the main skill with the practical rules for running a
protected-form task.

## Start From The Prepared Page

- If the browser is already on the correct form page, attach to that browser
  instead of reopening or navigating it.
- If the CDP endpoint changes, rerun `magicpay attach` before retrying
  session-bound commands.
- Do not carry one workflow session across different browser instances.

## Protected-Form Recovery

- If `find-form` returns `protected_form_not_found`, confirm that the browser
  is still on the intended login, identity, or payment step before retrying.
- If `find-form` returns `protected_form_ambiguous`, surface the candidates
  and ask the user to choose. Do not guess.
- If `fill-secret` reports that automatic submit was skipped, inspect the
  refreshed page state before deciding whether `submit-form` is appropriate.
- If `submit-form` returns `submit_binding_stale` or `fillable_form_absent`,
  rerun `find-form` on the current page before requesting or submitting
  anything else.
- If `submit-form` or the embedded auto-submit in `fill-secret` returns
  `validation_blocked`, report the visible blocker and wait for the page state
  to change before retrying.

## Multiple Protected Fields

When one form needs several protected fields:

1. Complete one request-poll-fill cycle for each field.
2. Refresh the current form contract after each fill if the page mutates.
3. Let the final `fill-secret` auto-submit when the guarded refresh resolves a
   live submit control.
4. Use `submit-form` only as manual recovery on a fresh protected-form
   snapshot.

## When To Stop

Stop and report back when:

- approval reaches a terminal denied, expired, failed, or canceled state;
- the browser is no longer on the intended protected page;
- the form stays ambiguous after rerunning discovery;
- `magicpay status` still fails after `magicpay init <apiKey>` and
  `magicpay doctor` confirms a local config problem that needs repair;
- `magicpay status` says the account or API key is invalid.
