---
name: booking-manager
version: 1.0.0
description: >
  AI-powered booking manager that connects to any existing booking system and lets
  business owners manage appointments through their phone (Telegram, WhatsApp, etc.). Use when: setting up an AI
  assistant to monitor bookings, notify owners of new enquiries, confirm/reschedule/cancel
  appointments conversationally, send professional customer emails with calendar invites,
  and provide schedule summaries. Works with any data source: SQL databases (PostgreSQL,
  SQLite/Turso, MySQL), REST APIs (Calendly, Square, Fresha), Google Sheets, or webhooks.
  Triggers on: "booking assistant", "appointment manager", "manage bookings via phone",
  "AI receptionist", "booking notifications", "salon booking system".
---

# Booking Manager

An AI assistant layer that sits on top of any booking system, turning your phone into a
full booking management interface via Telegram, WhatsApp, or any supported channel.

## How It Works

```
Customer books → Data saved (DB/API/Sheet) → Agent polls for new bookings
                                                    ↓
                                          Notifies owner via phone (Telegram/WhatsApp)
                                                    ↓
                              Owner replies: "confirm" / "reschedule" / "delete"
                                                    ↓
                                    Agent updates data + emails customer
```

## Setup

### 1. Identify the data source

Determine how the business stores bookings. Read `references/data-sources.md` for
connection patterns for each supported platform.

### 2. Configure credentials

Store connection details in TOOLS.md:

```markdown
## Booking Data Source
- Type: [turso | postgres | google-sheets | api]
- Connection: [URL/credentials]

## Email
- From: [Business Name] <business@email.com>
- SMTP: smtp.gmail.com:587
- Password: [Gmail App Password]
```

### 3. Set up heartbeat polling

Add to HEARTBEAT.md to check for new bookings every 15-30 minutes:

```markdown
## Check for new bookings
- Query the data source for bookings created since last check
- If new bookings found: notify the owner with details and send acknowledgement email
```

### 4. Configure the agent identity

Set SOUL.md with the business context:

```markdown
You are the booking manager for **[Business Name]**.

## Your Role
- Monitor for new booking enquiries and notify the owner on their phone
- Confirm, reschedule, or delete bookings when instructed
- Send professional emails to customers
- Provide schedule summaries on demand

## Rules
- All times in [timezone]
- Always clean up booking locks when confirming or deleting
- Send calendar invites (.ics) when confirming
```

## Core Workflows

### New booking notification

When a new booking is detected, notify the owner:

```
📋 New booking enquiry!

Name: [name]
Service: [service] ([duration] min)
Date: [formatted date and time]
Phone: [phone]
Email: [email]

Reply: "confirm [id]", "reschedule [id] to [date] [time]", or "delete [id]"
```

Send an acknowledgement email to the customer. See `references/email-templates.md`.

### Confirm booking

1. Mark booking as confirmed in data source
2. Remove any booking lock for the customer's email
3. Send confirmation email with .ics calendar invite attached
4. Notify owner: "✅ Booking #[id] confirmed. Email sent to [name]."

### Reschedule booking

1. Update date/time in data source
2. Remove booking lock
3. Send updated confirmation email with new .ics
4. Notify owner: "✅ Booking #[id] rescheduled to [new date/time]. Email sent."

### Delete booking

1. Record the customer email before deleting
2. Delete the booking from data source
3. Remove booking lock
4. Optionally send cancellation email
5. Notify owner: "🗑️ Booking #[id] deleted."

### Schedule queries

Respond naturally to:
- "What bookings do I have today?"
- "Show this week's schedule"
- "How many bookings this month?"
- "Any new bookings?"

## Calendar Invites

Generate .ics files when confirming. See `references/ics-format.md` for the template
and timezone/DST conversion logic.

## Email Sending

Send via Gmail SMTP using curl or a shell script. See `references/email-templates.md`
for HTML templates (enquiry acknowledgement, confirmation, cancellation) and the
booking policy text.

## Booking Locks

Many booking systems use a lock/hold mechanism to prevent duplicate pending enquiries
from the same customer. **Always** release locks when confirming or deleting a booking,
otherwise the customer cannot book again.

## Adapting to Different Businesses

Customise these per client:
- Business name and branding in email templates
- Services list with durations (for calendar invite end times)
- Operating hours and timezone
- Booking policy text
- Data source connection method
