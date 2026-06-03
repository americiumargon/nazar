# Nazar (نَظَر) — Autonomous Meta Ads Intelligence Agent

**Nazar** is a specialized AI agent that monitors, analyzes, and reports on Meta Ads performance — daily, weekly, and monthly — without human intervention.

It connects directly to the Meta Graph API, pulls data across all levels (account → campaign → ad set → creative), and delivers structured intelligence with ranked breakdowns, anomaly flags, actionable recommendations, and **end-date tracking**.

---

## ❌ The Problem

Running Meta Ads is noisy. Every campaign has dozens of metrics. Making sense of it every single day takes real time:

- Open Ads Manager, pull the right date ranges, compare manually
- Check every creative individually
- Remember which ad sets are about to expire
- Type up a summary
- Do this at the same time, every morning, without fail

But there's a hidden problem most teams don't catch: **Meta doesn't auto-update campaign status after the end date passes.** An ad set that "looks" ACTIVE in the dashboard may have stopped spending days ago because its `end_time` passed — and nobody noticed.

---

## ✅ How Nazar Solves It

| Before | After Nazar |
|---|---|
| Manual dashboard check, screenshots — when someone gets to it | Report lands at **08:00 sharp, every day** |
| Surface-level top-line glance | **16-metric comparison** with day-over-day delta |
| "Which creative is winning?" — dig manually | **Ranked creative breakdown** with CPA, ROAS, CTR per ad |
| Dead campaigns stay "ACTIVE" in dashboard — unnoticed for days | Checks `end_time`, not `status` — **end-date radar flags expiring & expired ad sets** |
| Ad sets expire silently, spend drops to zero — discovered too late | **Proactive warnings** 48-72 hours before expiration with recommended actions |
| One person is the bottleneck | **Anyone can ask Nazar** in chat |
| Problems found days later | **Proactive anomaly detection** — zero purchases, LPV drops, CPC spikes flagged same day |

---

## 📊 What Nazar Does

### 🔁 Scheduled (No Human Trigger)
- **Daily** at 08:00 GMT+7 — yesterday vs day-before comparison, 3 charts, creative ranking, **end-date radar**
- **Weekly** every Monday — 7-day trends, creative lifecycle, weekend vs weekday patterns
- **Monthly** every 1st — full P&L, fatigue detection, month-over-month efficiency

### 💬 On-Demand
- "How did Campaign X perform?"
- "Which creative is winning in Ad Set Y?"
- "What ad sets are ending this week?"
- Natural language — English or Bahasa Indonesia

### 🔍 Proactive
- **End-date radar** — scans every ad set's `end_time`, flags imminent expirations and silently-expired assets
- **Activity scan** — flags new (🆕) and ended (⏹️) campaigns
- **Anomaly detection** — creative fatigue, spend anomalies, LP View Rate drops, zero-purchase alerts
- **Recommended actions** — prioritized P0/P1/P2 tasks based on urgency

---

## 🏗️ Architecture

```
  ┌────────── Cron ──────────┐
  │  08:00 GMT+7 daily       │
  │  Monday → + weekly       │
  │  1st → + monthly         │
  └──────────┬───────────────┘
             ▼
  ┌─────────────────────────┐
  │  Nazar Agent (LLM)       │
  │  ├─ Meta Graph API v22   │
  │  ├─ Python analytics     │
  │  ├─ matplotlib charts     │
  │  └─ Persistent memory    │
  └──────────┬──────────────┘
             ▼
  ┌─────────────────────────┐
  │  Telegram / Chat         │
  │  (text + 3 charts)       │
  └─────────────────────────┘
```

**Stack:** Python → Meta Graph API v22.0 → QwenPaw Agent Framework → matplotlib → Telegram

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/americiumargon/nazar.git
cd nazar
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
cp .env.example .env
# Edit .env with your Meta access token and account ID
```

You'll need:
- `META_ACCESS_TOKEN` — from [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- `META_ACCOUNT_ID` — your ad account ID (format: `act_XXXXXXXXX`)

### 3. Test
```bash
python scripts/fetch_ads.py          # Pull account data
python scripts/analyze_creatives.py   # Rank creatives
python scripts/full_breakdown.py      # Full campaign → ad breakdown
python scripts/daily_report.py        # Yesterday vs day-before comparison
```

### 4. Deploy as Full Agent (QwenPaw)

To unlock the full autonomous agent — scheduled reports, conversational queries, persistent memory:

**Step 1: Create a QwenPaw Agent**
1. Go to [QwenPaw](https://github.com/agentscope-ai/QwenPaw) and create a new agent
2. Name it `Nazar` (or anything you like)

**Step 2: Upload Identity Files**
In your agent's workspace, upload the entire `agent/` folder:
- `SOUL.md` → defines personality, rules, and tone
- `AGENTS.md` → safety conventions and boundaries
- `PROFILE.md` → identity and user preferences

Edit `PROFILE.md` with your details (name, timezone, KPIs).

**Step 3: Upload Scripts**
Upload all files from `scripts/` into your agent's workspace.

**Step 4: Configure Environment**
Set these environment variables in QwenPaw:
```
META_ACCESS_TOKEN=your_token_here
META_ACCOUNT_ID=act_your_account_id
```

**Step 5: Set the Cron Schedule**
Configure a cron job for `08:00 Asia/Bangkok` (or your timezone) with this prompt:

```
Pull Meta Ads report for yesterday vs the day before. Format exactly like this:

1. Executive Summary — 2-3 sentence performance highlight, mention ROAS, CPA, and significant changes. Use emoji.

2. Comparison Table — include: Spend, Impressions, Reach, Clicks, Link Clicks, Landing Page Views, CPC, CPM, CTR, Cost per LPV, LP View Rate, Purchase*, Purchase Value, Click to Purchase rate, ROAS (est.), CPA (est.). Add delta column with green/yellow/red indicators.

3. Insights — 3-4 analysis points, specific numbers. Flag anomalies.

4. Creative Breakdown — per ad: Spend, CPC, CTR, LPV, Cost per LPV, Purchase*, CPA, Click to Purchase rate. Flag top performers.

5. End-Date Radar — scan all ad sets for expiring/expired end_time. Flag assets still ACTIVE past end_date.

6. Recommended Actions — prioritized P0/P1/P2 tasks.

7. Caveat — ROAS and CPA are Pixel estimates, confirm actual closings in CRM.

Also scan for new (🆕) and ended (⏹️) campaigns. Mention @team in the report.
```

**Step 6: Enable Telegram Delivery**
Connect your Telegram session in QwenPaw to deliver reports to a group or channel.

**That's it.** Nazar will now run autonomously — daily reports, end-date radar, creative rankings — without anyone touching Ads Manager.

---

---

## ⚙️ What Runs Standalone vs What Needs an Agent

Nazar is two things: **Python scripts** (the tools) and an **LLM agent** (the analyst).

### ✅ Standalone (Python Only — No Agent Required)

These work right out of the box with just `pip install`:

- Pull raw account/campaign/adset/ad data from Meta API
- Rank creatives by spend, ROAS, CPA, CTR
- Generate matplotlib charts from data
- Print day-over-day comparison tables

```bash
python scripts/daily_report.py   # Works immediately
python scripts/analyze_creatives.py
python scripts/full_breakdown.py
```

**Use case:** developer wants programmatic access to Meta Ads data without opening Ads Manager.

### ⚡ Full Agent (Requires QwenPaw or Equivalent)

These capabilities need an LLM agent framework for scheduling, reasoning, and memory:

| Feature | Why an agent? |
|---|---|
| Scheduled delivery (08:00 daily) | Cron + Telegram integration |
| Conversational queries ("How is Campaign X?") | LLM interprets questions, pulls relevant data |
| Executive summaries & insights | LLM generates natural language from raw metrics |
| End-date radar with recommendations | Persistent memory tracks campaign lifecycles |
| Anomaly flags & opinions | LLM detects patterns, forms judgments |
| Multi-language (English / Bahasa Indonesia) | LLM adapts language per context |

**Use case:** autonomous team member that replaces the daily manual ad check.

Nazar was built on [QwenPaw](https://github.com/agentscope-ai/QwenPaw), but the scripts are framework-agnostic — deploy them in any agent platform.

---

## 📁 Repository Structure

```
nazar/
├── README.md
├── LICENSE
├── .env.example
├── requirements.txt
├── agent/
│   ├── SOUL.md              ← Agent personality & rules
│   ├── AGENTS.md            ← Safety conventions
│   └── PROFILE.md           ← Identity template
├── scripts/
│   ├── fetch_ads.py         ← Account-level data puller
│   ├── daily_report.py      ← Daily comparison engine
│   ├── analyze_creatives.py ← Creative ranking tool
│   ├── full_breakdown.py    ← Multi-level breakdown
│   └── generate_report.py   ← Chart generator (matplotlib)
└── examples/
    └── sample_report.md     ← Real output with end-date radar
```

---

## 📸 Example Output

> ### 📊 Meta Ads Daily Report — Account 1
> **June 1 vs May 31, 2026**
>
> ### ⚠️ Executive Summary
> **🔴 3 ad sets ending within 48 hours.** 4 purchases at $124.50 spend, ROAS 5.2x. **All Products ad set ends TOMORROW (June 3)** — no replacement scheduled. If not extended, we lose 60% of daily spend by end of week.
>
> ### 🚨 End-Date Radar
> | Ad Set | End Date | Status | Spend | Action |
> |---|---|---|---|---|
> | All Products Carousel ⚠️ | June 3 (TOMORROW) | ACTIVE | $32.70 | 🔴 Extend or replace |
> | Launch - Variant 2 | June 5 (3 days) | ACTIVE | $48.20 | 🟡 Monitor |
> | Product A - Original | June 1 (EXPIRED) | ⚠️ STILL ACTIVE | $1.80 | ⏹️ Archive |
>
> ### 📋 Recommended Actions
> | Priority | Action |
> |---|---|
> | 🔴 P0 | Extend All Products Carousel end date (ends tomorrow) |
> | 🟡 P1 | Decide on Campaign A ad sets — extend or replace |
> | 🟢 P2 | Archive silently-expired ad sets still showing "ACTIVE" |
>
> *"Meta's status field is lying — again. Always check `end_time`, not the green dot."*
>
> → [Full sample report](examples/sample_report.md)

---

## 🔒 Safety

**Read-only.** Nazar never touches budgets, pauses campaigns, or modifies ads. It analyzes and reports — all decisions remain with the operator.

---

## 📝 License

MIT — see [LICENSE](LICENSE).

---

*نَظَر — gaze, observation, insight. The name says it all.*
