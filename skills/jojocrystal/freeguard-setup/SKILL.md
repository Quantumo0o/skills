---
name: freeguard-setup
description: Use when a user wants to set up, use, or troubleshoot FreeGuard VPN - guides non-technical users through installation, login, connection, and daily usage with friendly step-by-step instructions
---

# FreeGuard VPN Setup Guide

An agent skill for guiding users through FreeGuard VPN setup and daily usage. Designed for non-technical users — use friendly language instead of internal technical terms.

## Required Tools

This skill uses the `freeguard` CLI binary (installed via official channels below). All commands are run through the user's terminal with standard tool-call permissions.

## Credentials & Data Handling

- **Email**: asked from user for login/subscription (sent to freeguards.com API)
- **Verification code**: 6-digit code sent to user's email, entered by user
- **Subscription URL / Access token**: provided by user, stored locally in `~/.freeguard/credentials.yaml` with 0600 permissions
- No credentials are stored or transmitted by this skill itself — all handled by the `freeguard` CLI

## Tone

- Friendly, patient, encouraging
- Use simple language: "open your terminal" not "execute in shell"
- Celebrate progress: "Great, you're logged in!"
- If something fails, reassure: "No worries, let's try another way"
- Use friendly language instead of internal terms like "mihomo", "YAML", "runtime config", "API port", "GeoIP rule-provider"

## Agent Flow

```dot
digraph setup {
    rankdir=TB;
    start [label="User wants VPN" shape=doublecircle];
    installed [label="Installed?" shape=diamond];
    install [label="Guide installation" shape=box];
    hassub [label="Has subscription?" shape=diamond];
    subscribe [label="Guide purchase" shape=box];
    loggedin [label="Logged in?" shape=diamond];
    login [label="Guide login" shape=box];
    region [label="Ask region\n& apply settings" shape=box];
    auth [label="Ask user for\nadmin permission" shape=box];
    canroot [label="User grants\nadmin?" shape=diamond];
    sudoconnect [label="sudo connect\n(full protection)" shape=box];
    normalconnect [label="connect\n(standard mode)" shape=box];
    verify [label="Verify & teach\ndaily usage" shape=box];
    done [label="All set!" shape=doublecircle];

    start -> installed;
    installed -> install [label="no"];
    installed -> hassub [label="yes"];
    install -> hassub;
    hassub -> subscribe [label="no"];
    hassub -> loggedin [label="yes"];
    subscribe -> loggedin;
    loggedin -> login [label="no"];
    loggedin -> region [label="yes"];
    login -> region;
    region -> auth;
    auth -> canroot;
    canroot -> sudoconnect [label="yes"];
    canroot -> normalconnect [label="no"];
    sudoconnect -> verify;
    normalconnect -> verify;
    verify -> done;
}
```

## Step 1: Check Environment

Run the diagnostic command and summarize the result to the user:

```bash
freeguard doctor --json
```

From the result, determine:
- **Not installed** → Go to Installation
- **Installed, no subscription** → Go to Subscribe
- **Installed, has subscription but not logged in** → Go to Login
- **Logged in with subscription** → Go to Region & Connect

Tell the user the current state in friendly terms:
- "Looks like FreeGuard isn't installed yet. Let me help you set it up!"
- "FreeGuard is installed! Now we need to get you a subscription."
- "You have a subscription but aren't logged in yet. Let's fix that."
- "You're already logged in! Let's get you connected."

## Step 2: Installation

Ask the user's operating system if unclear, then recommend the best install method.

**Preferred — package managers (verified, signed):**
- **macOS with Homebrew**: `brew install planetlinkinc/tap/freeguardvpn`
- **Direct download**: Binary releases at https://github.com/planetlinkinc/freeguard-cli/releases (GitHub-hosted, checksums in release notes)

**Alternative — install scripts (ask user to confirm before running):**
- **macOS / Linux**: `curl -fsSL https://downloadcli.freeguardvpn.com/cli/install.sh | sh`
- **Windows (PowerShell)**: `irm https://downloadcli.freeguardvpn.com/cli/install.ps1 | iex`

When suggesting script install, tell the user:
> "This will download and install FreeGuard from the official site (downloadcli.freeguardvpn.com). The source code is on GitHub at github.com/planetlinkinc/freeguard-cli. Shall I go ahead?"

Only proceed after user confirms. After install, verify with `freeguard doctor --json`.

## Step 3: Subscribe (if no subscription)

First check if user already has a subscription:

```bash
freeguard subscribe info --json
```

If they have an active subscription, skip to Login. If expired, tell them:
> "Your subscription has expired. Let's renew it!"

If no subscription, check available plans:

```bash
freeguard subscribe list --json
```

Then present the options in friendly terms:

> "To use FreeGuard VPN, you'll need a subscription. Here are the plans available:
>
> | Plan | Price |
> |------|-------|
> | Weekly | $3.99/week |
> | Monthly | $7.99/month |
> | Yearly | $49.99/year (best value) |
>
> Which plan works for you?"

After the user picks a plan, ask for their email:

> "Great choice! What email address should we use for your account?"

Then create the subscription:

```bash
freeguard subscribe create --plan <price_id> --email <email> --json
```

Map user's choice to price_id from the `subscribe list` response. The command will return a checkout URL.

Tell the user:

> "I've opened a payment page for you. Please complete the payment there, and let me know when you're done."

After they confirm payment, proceed to Login.

## Step 4: Login

Ask the user how they'd like to log in:

> "How would you like to log in?
> 1. **Email** — I'll send you a verification code
> 2. **Subscription link** — if you have a Clash subscription URL
> 3. **Access token** — if you received one after purchase"

If the user just completed a purchase in Step 3, skip this question and go straight to Email Login using the email they already provided.

### Email Login (most common)

1. Ask: "What's your email address?"
2. Tell user: "I'll send a verification code to your email now."
3. Run: `freeguard login --email <email> --send-code --json`
4. Tell user: "A verification code has been sent. Please check your inbox (and spam folder) and tell me the 6-digit code."
5. User provides code
6. Run: `freeguard login --email <email> --code <code> --json`
7. On success: "Great, you're logged in!"
8. On failure: "That code didn't work. Want me to send a new one?"

### URL Login

1. Ask: "Please paste your subscription URL"
2. Run: `freeguard login --url <url> --json`
3. On success: "Logged in successfully!"

### Token Login

1. Ask: "Please paste your access token"
2. Run: `freeguard login --token <token> --json`
3. On success: "Logged in successfully!"

## Step 5: Region & Settings

Ask the user where they are:

> "One more thing — where are you located? This helps optimize your connection for the best speed.
>
> For example: China, Japan, US, Korea, Russia, etc."

Map their answer to a region code:

| User says | Region code |
|-----------|-------------|
| China / mainland / CN | CN |
| US / America / United States | US |
| Japan / JP | JP |
| Korea / KR / South Korea | KR |
| Russia / RU | RU |
| Iran / IR | IR |
| Indonesia / ID | ID |
| UAE / Dubai / AE | AE |
| Other / not listed above | (skip GeoIP) |

Tell the user what settings you're applying:
> "I'm going to optimize your settings: enable system-wide VPN protection, network sharing, and fast DNS. This will give you the best experience."

Then apply settings:

```bash
freeguard config set proxy.tun true --json
freeguard config set proxy.allow_lan true --json
freeguard config set dns.enable true --json
```

Only if user's region matches one of the 8 supported codes:
```bash
freeguard config set geoip_region <CODE> --json
```

Also ask if the user wants a specific country for their VPN exit:
> "Which country do you want to appear as when browsing? For example: US, Japan, Hong Kong..."

If they specify:
```bash
freeguard config set preferred_country <country> --json
```

Tell the user:
> "Settings applied! VPN will protect all apps on this computer and devices on your local network can share the connection too."

## Step 6: Authorize & Connect

**TUN mode requires administrator/root privileges.** Without it, only apps that respect proxy settings will go through VPN. Always explain WHY admin access is needed and ask for explicit confirmation.

**macOS / Linux:**
> "To protect all your apps (not just the browser), VPN needs admin privileges. This is because system-wide traffic capture requires low-level network access.
>
> I'll need to run `sudo freeguard connect`. **Is that OK?** You'll be asked for your password."

Only proceed after user confirms. Then run:
```bash
sudo freeguard connect --json
```

**Windows:**
> "To protect all your apps, we need to run as Administrator. This is because system-wide traffic capture requires elevated permissions.
>
> Please right-click your terminal and select 'Run as Administrator', then tell me when you're ready."

After they confirm:
```bash
freeguard connect --json
```

**If user declines admin access:**
> "No problem! I'll connect in standard mode. Your browser and most apps will still be protected, but some apps like terminal commands may not go through VPN."

Then connect without sudo:
```bash
freeguard connect --json
```

The connect command runs automatic health checks (DNS, direct access, proxy, streaming, download speed). Parse the JSON output and report to user:
- All 5 checks pass: "You're connected! Everything is working perfectly — browsing, streaming, and downloads all good."
- Some checks fail: "You're connected, but some features need attention..." (explain which failed in simple terms)

On failure, check the error:
- **subscription_expired**: "Your subscription has expired. Would you like to renew?" → Go to Step 3
- **auth_required**: "It seems your login session expired. Let's log in again."
- **core_download_failed**: "There was a download issue. Please check your internet and try again."
- Other: "Something went wrong. Let me run a diagnostic..." → run `freeguard doctor --json`

## Step 7: Verify

Check the connection status and report to the user:

```bash
freeguard status --json
```

If connected, tell the user:
> "Everything looks good! Here's what you need to know:
>
> - **Check status**: just ask me 'am I connected?'
> - **Disconnect**: ask me to 'disconnect' or run `freeguard disconnect`
> - **Reconnect**: ask me to 'connect' or run `freeguard connect`
> - **Switch server location**: ask me to 'switch to Japan' or similar
> - **Check subscription**: ask me 'when does my plan expire?'
> - **Start on boot**: ask me to 'enable autostart'
>
> Enjoy your secure internet!"

## Daily Usage Commands

When the user asks about ongoing usage, run the appropriate command and summarize the result in friendly terms:

| User says | What to do |
|-----------|------------|
| "Am I connected?" / "Status" | `freeguard status --json` → report connection, node, mode, subscription expiry |
| "Connect" / "Turn on VPN" | `freeguard connect --json` → "Connected!" + report health check results |
| "Connect to US" / "Use Japan server" | `freeguard connect --country US --json` |
| "Disconnect" / "Turn off VPN" | `freeguard disconnect --json` → "Disconnected" |
| "Show nodes" / "Server list" | `freeguard node list --json` → summarize locations |
| "Switch to Tokyo" | `freeguard node switch "Tokyo" --json` → "Switched to Tokyo" |
| "Switch to hysteria2 protocol" | `freeguard node switch "<current-node>" hysteria2 --json` |
| "Speed test" | `freeguard node test --all --json` → show top 5 fastest |
| "Check my account" | `freeguard subscribe info --json` → report plan status and expiry |
| "Renew my subscription" | `freeguard subscribe list --json` → show plans |
| "Manage billing" | `freeguard subscribe portal --email <email> --code <code>` → open Stripe portal |
| "Something's not working" | `freeguard doctor --json` → diagnose and suggest fixes |
| "Log out" | `freeguard disconnect --json` then `freeguard logout --json` |
| "Share VPN with my phone" | Explain: set proxy to this computer's IP, port 7997 |
| "Start VPN on boot" | `freeguard autostart enable --json` |
| "Stop autostart" | `freeguard autostart disable --json` |

## Troubleshooting

When things go wrong, run `freeguard doctor --json` and interpret the results:

| Check fails | What to tell user |
|-------------|-------------------|
| Network | "Your internet connection seems to be down. Please check your WiFi or cable." |
| Credentials | "Your login session has expired. Let's log in again." |
| Subscription | "You need an active subscription. Would you like to pick a plan?" → Go to Step 3 |
| Subscription expired | "Your subscription has expired. Let's renew it!" → Go to Step 3 |
| Port in use | "Another app is using the same port. FreeGuard will find an available one automatically." |
| Core Binary | "A component needs to be downloaded. Let me try connecting — it should download automatically." |

## Language Guide

Use friendly language instead of internal technical terms:

| Technical term | User-friendly alternative |
|----------------|--------------------------|
| mixed port 7997 | proxy settings |
| TUN mode | system-wide VPN protection |
| allow LAN | share VPN with other devices on your network |
| GeoIP region CN | optimized for your location in China |
| fake-ip DNS | fast DNS |
| rule-provider | smart routing |
| node switch | switch server |
| autostart enable | start VPN on boot |
| subscribe info | check your account |
| Trojan/AnyTLS/Hysteria2 | connection protocols (only mention if user asks) |
| mihomo | VPN engine (only mention if user asks) |
| config.yaml / runtime.yaml | settings (only mention if user asks) |
