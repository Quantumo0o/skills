---
name: campaign-calendar-planner
description: Plan ecommerce campaign calendars across Shopify, Amazon, TikTok Shop, Xiaohongshu, and other channels using built-in seasonal frameworks, promotion playbooks, and channel-timing templates. Use when preparing quarterly campaign plans, monthly promotion schedules, holiday retail calendars, or multi-channel campaign sequencing without live project-management or ad-platform integrations.
---

# Campaign Calendar Planner

## Overview

Use this skill to turn rough campaign ideas, seasonal goals, and channel priorities into an operator-ready campaign calendar. It applies a built-in seasonal framework, promotion playbook library, and channel-timing matrix to generate a structured markdown brief.

This MVP is heuristic. It does **not** connect to live ad platforms, calendars, or ERP systems. It relies on the user's provided campaign context, seasonal intent, and channel mix.

## Trigger

Use this skill when the user wants to:
- build a quarterly or monthly campaign calendar from scratch
- map a holiday or seasonal promotion across multiple channels
- sequence campaign types (awareness → conversion → retention) over a time window
- audit whether campaign timing, frequency, and channel mix are aligned
- turn rough campaign notes into an organized execution calendar

### Example prompts

- "Create a Q2 campaign calendar for our Shopify store"
- "Build a Mother's Day promotion plan across TikTok Shop and Xiaohongshu"
- "Help me plan a summer flash-sale series across Amazon and our DTC store"
- "Map our channel campaign sequencing for the next 90 days"

## Workflow

1. Capture the planning window, primary campaign type, and target channels.
2. Apply the seasonal framework to identify high-signal periods and key dates.
3. Map campaign types to channels and sequence them across the window.
4. Generate a channel-timing matrix and priority calendar.
5. Return a markdown brief with calendar grid, campaign cards, and execution notes.

## Inputs

The user can provide any mix of:
- planning window: Q1 / Q2 / Q3 / Q4, half-year, full year, or specific date range
- campaign goal: awareness, traffic, conversion, revenue, retention, or brand
- channels: Shopify, Amazon, TikTok Shop, Xiaohongshu, WeChat, email, Meta Ads, Google Ads
- seasonal context: holiday name, shopping festival, or rough seasonal theme
- budget tone: aggressive, steady, experimental
- product focus: new launch, clearance, core SKUs, premium push

## Outputs

Return a markdown brief with:
- planning window and campaign thesis
- seasonal framework and key-date map
- channel-timing matrix (channel × week/month)
- campaign card for each major promotion (name, type, channels, timing, goal)
- frequency and cadence recommendations
- execution notes and common pitfalls

## Safety

- No live calendar, ad platform, or ERP access.
- Seasonal-date references are directional; users should verify official festival and sale dates.
- Campaign budgets and media spend recommendations are advisory.
- All channel activation decisions remain human-approved.

## Best-fit Scenarios

- SMB and mid-market ecommerce teams planning quarterly or seasonal campaigns
- brands running multi-channel promotions without a dedicated campaign manager
- teams that need a reusable planning framework instead of scattered notes

## Not Ideal For

- real-time campaign management, live ad spend control, or automated execution
- very small experimental runs with no defined planning window
- regulated categories requiring pre-approval for promotional claims

## Acceptance Criteria

- Return markdown text.
- Include calendar grid, campaign cards, and execution notes.
- Cover at least 3 key seasonal dates within the planning window.
- Make timing assumptions explicit.
- Keep the brief practical for ecommerce operators and channel managers.
