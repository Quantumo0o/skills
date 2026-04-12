# MagicPay Command Guide

## Setup And Readiness

### `magicpay init <apiKey> [--api-url <url>]`

Save the API key to `~/.magicpay/config.json`. When `--api-url` is provided,
`init` also stores the gateway base URL there.

### `magicpay status`

Check CLI health, authenticated identity, and update state. Use this as the
normal preflight command before a protected-form task.

### `magicpay doctor`

Inspect the local config file when `status` still fails after `init`.

### `magicpay --version`

Print the installed CLI version.

## Browser Attach And Session Control

### `magicpay attach <cdp-url> [--provider <name>]`

Connect MagicPay to an already running browser through CDP.

### `magicpay start-session [name] [--merchant-name <name>]`

Bind the attached browser to a MagicPay workflow session.

### `magicpay end-session`

Complete the active workflow session without closing the browser.

## Protected-Form Flow

### `magicpay find-form [--purpose <auto|login|identity|payment_card>]`

Discover the supported protected form on the current page and return the
current protected-form contract.

### `magicpay get-secrets-catalog [url]`

Refresh stored-secret metadata for the current host or an explicit URL.

### `magicpay request-secret <fillRef> <storedSecretRef> --merchant-name <name>`

Create an approval request for one protected field on the current page.

### `magicpay poll-secret <requestId>`

Check whether a request is still pending, fulfilled, or terminal.

### `magicpay fill-secret <fillRef> <requestId>`

Claim the approved secret, fill the protected field, refresh the page state,
and auto-submit when a live form-bound submit control is available.

### `magicpay submit-form <fillRef>`

Manually submit the current protected form when `fill-secret` explicitly
leaves submission unfinished or when you intentionally retry on a fresh
protected-form snapshot.
