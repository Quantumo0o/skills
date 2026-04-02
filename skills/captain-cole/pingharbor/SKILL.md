{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fmodern\fcharset0 Courier;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs26 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 ---\
name: pingharbor\
description: Query uptime monitors, retrieve incidents, create monitors, and fetch SLA reports from your PingHarbor account.\
homepage: https://pingharbor.com\
user-invocable: true\
metadata: \{"openclaw":\{"emoji":"\'e2\'9a\'93","homepage":"https://pingharbor.com","primaryEnv":"PINGHARBOR_API_KEY","requires":\{"env":["PINGHARBOR_API_KEY"]\}\}\}\
---\
\
# PingHarbor \'e2\'80\'94 Uptime Monitoring\
\
Connect to your PingHarbor account to monitor website uptime, query incidents, and pull SLA reports \'e2\'80\'94 all via the PingHarbor MCP server.\
\
## Authentication\
\
Set your PingHarbor API key as an environment variable:\
\
```\
PINGHARBOR_API_KEY=ph_your_api_key_here\
```\
\
Generate a key at: **Administration \'e2\'86\'92 API Keys** inside your PingHarbor dashboard.\
\
## MCP Endpoint\
\
```\
https://aeuudydvwlmbvuqgqsqu.supabase.co/functions/v1/mcp\
```\
\
Pass the key as a Bearer token:\
\
```\
Authorization: Bearer $PINGHARBOR_API_KEY\
```\
\
## Available Tools\
\
| Tool | Description |\
|------|-------------|\
| `list_monitors` | List all monitors and their current status |\
| `get_incidents` | Retrieve recent incidents and downtime events |\
| `create_monitor` | Create a new uptime monitor programmatically |\
| `get_monitor_report` | Fetch SLA and response time report for a monitor |\
\
## Example Usage\
\
> "List all my monitors and show me which ones are currently down."\
\
> "Get incidents from the last 7 days for monitor ID xyz."\
\
> "Create a monitor for https://example.com with a 60-second check interval."\
\
> "Show me the SLA report for my main API monitor."\
\
## Config (~/.openclaw/openclaw.json)\
\
```json\
\{\
  "skills": \{\
    "entries": \{\
      "pingharbor": \{\
        "enabled": true,\
        "apiKey": "ph_your_api_key_here"\
      \}\
    \}\
  \}\
\}\
```\
\
Or via environment variable injection:\
\
```json\
\{\
  "skills": \{\
    "entries": \{\
      "pingharbor": \{\
        "enabled": true,\
        "env": \{\
          "PINGHARBOR_API_KEY": "ph_your_api_key_here"\
        \}\
      \}\
    \}\
  \}\
\}\
```\
}