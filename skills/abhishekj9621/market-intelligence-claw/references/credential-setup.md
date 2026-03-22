# Credential Setup Guide

## Philosophy
All external API keys are **completely optional**. This skill works without any of them
using the built-in web_search tool. External APIs provide better structured data but
the same intelligence goals can be achieved without them.

When guiding a user to set up keys, always recommend:
- Create a **dedicated key** for this skill (don't reuse keys from other services)
- Set the **lowest quota** that meets their needs
- Use **read-only permissions** wherever the platform allows
- Never grant write/admin permissions to any key used here

---

## SerpApi

**What it unlocks:** Structured Google Shopping prices, Google Trends data, Amazon results, Google News
**Cost:** Free tier = 100 searches/month. Developer = $50/month for 5,000 searches.
**Recommended starting quota:** 500 searches/month cap

### How to get a key (step by step for non-technical users)
1. Go to **serpapi.com** and click **Sign Up** (top right)
2. Enter your email and create a password
3. Verify your email
4. On your dashboard, find **API Key** — it's a long string of letters and numbers
5. Copy it and paste it here

### Recommended safety setting
In your SerpApi dashboard → **Billing** → set a **monthly spend cap** to avoid surprise charges.
$5–10/month cap is plenty for casual use.

### What queries will look like (examples of what gets sent to SerpApi)
- `"wireless earbuds India price"` (Google Shopping)
- `"athleisure brands"` (Google Search)
- `"running shoes"` (Google Trends)
- `"Nike India news"` (Google News)

None of these queries will contain your business name, revenue, customer data, or any private information unless you explicitly instruct otherwise.

---

## NewsAPI

**What it unlocks:** Real-time news monitoring for brands, competitors, and industry topics
**Cost:** Free developer tier = 100 requests/day (articles from last month). Paid = $449/month for production.
**Free tier is sufficient for most users.**

### How to get a key
1. Go to **newsapi.org/register**
2. Fill in your name, email, and password
3. Your API key is shown immediately after registration — copy it

### What queries will look like
- `"Myntra news"`
- `"fashion ecommerce India trends"`
- `"Nykaa competitor launch"`

---

## Reddit API

**What it unlocks:** Raw community sentiment — what real customers say in forums
**Cost:** Completely free for non-commercial use (60 requests/minute)

### How to get credentials
1. Log in to Reddit (create an account if you don't have one)
2. Go to **reddit.com/prefs/apps**
3. Scroll to the bottom and click **"Create App"**
4. Fill in:
   - Name: "Market Research" (or anything)
   - Type: select **"script"**
   - Redirect URI: `http://localhost:8080`
5. Click **Create app**
6. You'll see:
   - **Client ID**: the string under your app name (looks like: `aBcDeFgH123456`)
   - **Client Secret**: labeled "secret"
7. Paste both here

### What queries will look like
- Reddit search for: `"wireless earbuds review"`
- Reddit search for: `"running shoes alternative"`
- Subreddit search in r/india: `"best skincare brand"`

---

## Storing Keys — Session Only

When the user provides API keys, confirm:
> "Got it — I'll use this key for our session. It's only in this conversation and isn't stored anywhere after our chat ends. When you come back next time, you'll need to provide it again."

Never:
- Echo back full API keys in responses
- Include API keys in summaries or reports
- Store keys across sessions
- Use keys for any purpose other than the research the user has approved

If the user asks "where is my key stored?", answer honestly:
> "It's only in this conversation's memory. It disappears when you close the chat. Nothing is saved to a database or server on our end."
