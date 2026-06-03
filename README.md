# Nazar (نَظَر) — Autonomous Meta Ads Intelligence Agent

**Nazar** is a specialized AI agent that monitors, analyzes, and reports on Meta Ads performance — daily, weekly, and monthly — without human intervention.

It connects directly to the Meta Graph API, pulls data across all levels (account → campaign → ad set → creative), and delivers structured intelligence with ranked breakdowns, anomaly flags, and actionable insights.

---

## ❌ The Problem

Running Meta Ads is noisy. Every campaign has dozens of metrics. Making sense of it every single day takes real time:

- Open Ads Manager, pull the right date ranges, compare manually
- Check every creative individually
- Type up a summary
- Remember which campaigns ended and which ones just appeared
- Do this at the same time, every morning, without fail

**What actually happens:** reports get skipped when busy, format varies, underperforming ads burn budget unnoticed, and one person becomes the bottleneck for all ad questions.

---

## ✅ How Nazar Solves It

| Before | After Nazar |
|---|---|
| Manual dashboard check, screenshots, typed notes — when someone gets to it | Report lands at **08:00 sharp, every day** |
| Surface-level top-line glance | **16-metric comparison** with day-over-day delta |
| "Which creative is winning?" — dig manually | **Ranked creative breakdown** with CPA, ROAS, CTR per ad |
| Dead campaigns stay "ACTIVE" in dashboard | Checks `end_time`, not `status` — **flags ended campaigns instantly** |
| One person is the bottleneck | **Anyone can ask Nazar** in chat |
| Problems found days later | **Proactive anomaly detection** — zero purchases, LPV drops, CPC spikes flagged same day |

---

## 📊 What Nazar Does

### 🔁 Scheduled (No Human Trigger)
- **Daily** at 08:00 GMT+7 — yesterday vs day-before, 3 charts, creative ranking
- **Weekly** every Monday — 7-day trends, creative lifecycle, weekend vs weekday patterns
- **Monthly** every 1st — full P&L, fatigue detection, month-over-month efficiency

### 💬 On-Demand
- "How did Campaign X perform?"
- "Which creative is winning in Ad Set Y?"
- Natural language — Bahasa Indonesia or English

### 🔍 Proactive
- Flags new (🆕) and ended (⏹️) campaigns
- Detects creative fatigue, spend anomalies, LP View Rate drops
- Tracks 50+ campaigns with lifetime context

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
git clone https://github.com/YOUR_USERNAME/nazar.git
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

### 4. Deploy as Agent
Deploy via [QwenPaw](https://qwenpaw.ai) (or your agent framework) with:
- `agent/` directory for identity & memory
- Cron configured for 08:00 GMT+7
- Telegram integration for delivery

---

## 📁 Repository Structure

```
nazar/
├── README.md
├── .env.example
├── requirements.txt
├── agent/
│   ├── SOUL.md           ← Agent personality & rules
│   ├── AGENTS.md         ← Safety conventions
│   └── PROFILE.md        ← Identity template
├── scripts/
│   ├── fetch_ads.py      ← Account-level data puller
│   ├── daily_report.py   ← Daily comparison engine
│   ├── analyze_creatives.py ← Creative ranking tool
│   ├── full_breakdown.py ← Multi-level breakdown
│   └── generate_report.py ← Chart generator (matplotlib)
└── examples/
    └── sample_report.md  ← Real output example
```

---

## 📸 Example Output

> ### 📊 Meta Ads Daily Report
> **28 Mei 2026 vs 27 Mei 2026**
>
> ### 🔥 Executive Summary
> Purchase value tembus **Rp 8.62M** — record high. 5 purchases, ROAS **14.05x**. LP View Rate full recovery to **78.3%** (+9.7pp). All 4 creatives delivering purchases.
>
> | Metric | Day Before | Yesterday | Δ |
> |---|---|---|---|
> | Purchase* | 5 | 5 | ≈ |
> | Purchase Value | Rp 2.7M | **Rp 8.6M** | 🟢 **+223%** |
> | ROAS | 4.75x | **14.05x** | 🟢 **+196%** |
> | CPA | Rp 112K | Rp 123K | 🟡 +9% |
>
> ### 🎯 Creative Ranking
> | Creative | Spend | Pur* | CPA |
> |---|---|---|---|
> | BAJRAIE 3 - LUKAN 🔥 | Rp 239K | 2 | Rp 120K |
> | AISC13 | Rp 207K | 1 | Rp 207K |
> | Carousel All Class | Rp 166K | 1 | Rp 166K |
>
> _Full sample report with charts: [`examples/sample_report.md`](examples/sample_report.md)_

---

## 🔒 Safety

**Read-only.** Nazar never touches budgets, pauses campaigns, or modifies ads. It analyzes and reports — all decisions remain with the operator.

---

## 📝 License

MIT — built by [Your Name]. Use it, fork it, build on it.

---

*نَظَر — gaze, observation, insight. The name says it all.*
