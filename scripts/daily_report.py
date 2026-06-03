"""
Nazar — Daily Report Engine
Compiles yesterday vs day-before comparison with full metric parsing.

Usage:
    python daily_report.py

Environment variables required:
    META_ACCESS_TOKEN — Your Meta Graph API access token
    META_ACCOUNT_ID    — Your Meta Ads account ID (e.g., act_123456)
"""

import requests, json, os
from collections import defaultdict
from datetime import datetime, timezone, timedelta

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
ACCOUNT_ID = os.getenv("META_ACCOUNT_ID")
API_VERSION = 'v22.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

if not ACCESS_TOKEN:
    raise EnvironmentError("META_ACCESS_TOKEN not set.")
if not ACCOUNT_ID:
    raise EnvironmentError("META_ACCOUNT_ID not set.")

# Timezone
bangkok = timezone(timedelta(hours=7))
now = datetime.now(bangkok)
yesterday_date = (now - timedelta(days=1)).strftime('%Y-%m-%d')
day_before_date = (now - timedelta(days=2)).strftime('%Y-%m-%d')


def fetch_date(date_str, level='account', extra_fields=''):
    resp = requests.get(f'{BASE_URL}/{ACCOUNT_ID}/insights', params={
        'access_token': ACCESS_TOKEN,
        'time_range': json.dumps({'since': date_str, 'until': date_str}),
        'level': level,
        'fields': 'spend,impressions,clicks,cpc,cpm,ctr,reach,actions,cost_per_action_type,action_values' + extra_fields,
        'limit': 200
    })
    return resp.json().get('data', [])


def parse(entry):
    spend = float(entry.get('spend', 0))
    impr = int(entry.get('impressions', 0))
    clicks = int(entry.get('clicks', 0))
    cpc = float(entry.get('cpc', 0))
    cpm = float(entry.get('cpm', 0))
    ctr = float(entry.get('ctr', 0))
    reach = int(entry.get('reach', 0))
    pur, pval, lc, lpv = 0, 0, 0, 0

    for act in entry.get('actions', []):
        at, v = act['action_type'], int(act['value'])
        if at == 'purchase': pur = v
        elif at == 'link_click': lc = v
        elif at == 'landing_page_view': lpv = v

    for av in entry.get('action_values', []):
        if av['action_type'] == 'purchase':
            pval = float(av['value'])

    cost_lpv = spend / lpv if lpv > 0 else 0
    lpv_rate = (lpv / lc * 100) if lc > 0 else 0
    click_to_pur = (pur / lc * 100) if lc > 0 else 0
    roas = pval / spend if spend > 0 else 0
    cpa = spend / pur if pur > 0 else 0

    return {
        'spend': spend, 'impr': impr, 'reach': reach, 'clicks': clicks,
        'lc': lc, 'lpv': lpv, 'cpc': cpc, 'cpm': cpm, 'ctr': ctr,
        'cost_lpv': cost_lpv, 'lpv_rate': lpv_rate, 'pur': pur,
        'pval': pval, 'click_to_pur': click_to_pur, 'roas': roas, 'cpa': cpa
    }


def delta(new, old):
    """Compare two values and return a formatted delta string."""
    pct = ((new - old) / old * 100) if old != 0 else 0
    if new > old:
        return f"🟢 +{pct:.0f}%"
    elif new < old:
        return f"🔴 {pct:.0f}%"
    return "≈"


def fmt_rp(v):
    """Format an integer as Rupiah."""
    return f"Rp {v:,.0f}" if v else "Rp 0"


def fmt_roas(v):
    return f"{v:.2f}x" if v else "0x"


# --- Main ---
if __name__ == '__main__':
    print(f"=== Daily Report: {yesterday_date} vs {day_before_date} ===")

    yesterday_acc = fetch_date(yesterday_date)
    day_before_acc = fetch_date(day_before_date)

    if yesterday_acc:
        y = parse(yesterday_acc[0])
        print(f"\nYesterday ({yesterday_date}):")
        print(f"  Spend: {fmt_rp(y['spend'])} | Impr: {y['impr']:,} | Reach: {y['reach']:,}")
        print(f"  Clicks: {y['clicks']} | LC: {y['lc']} | LPV: {y['lpv']}")
        print(f"  CPC: {fmt_rp(y['cpc'])} | CPM: {fmt_rp(y['cpm'])} | CTR: {y['ctr']:.2f}%")
        print(f"  Purchases: {y['pur']} | Value: {fmt_rp(y['pval'])} | ROAS: {fmt_roas(y['roas'])} | CPA: {fmt_rp(y['cpa'])}")

    if day_before_acc:
        d = parse(day_before_acc[0])
        print(f"\nDay Before ({day_before_date}):")
        print(f"  Spend: {fmt_rp(d['spend'])} | Impr: {d['impr']:,} | Reach: {d['reach']:,}")
        print(f"  Clicks: {d['clicks']} | LC: {d['lc']} | LPV: {d['lpv']}")
        print(f"  CPC: {fmt_rp(d['cpc'])} | CPM: {fmt_rp(d['cpm'])} | CTR: {d['ctr']:.2f}%")
        print(f"  Purchases: {d['pur']} | Value: {fmt_rp(d['pval'])} | ROAS: {fmt_roas(d['roas'])} | CPA: {fmt_rp(d['cpa'])}")

    if yesterday_acc and day_before_acc:
        print(f"\nDelta (Yesterday vs Day Before):")
        print(f"  Purchases: {d['pur']} → {y['pur']}  {delta(y['pur'], d['pur'])}")
        print(f"  ROAS: {fmt_roas(d['roas'])} → {fmt_roas(y['roas'])}  {delta(y['roas'], d['roas'])}")
        print(f"  CPA: {fmt_rp(d['cpa'])} → {fmt_rp(y['cpa'])}  {delta(y['cpa'], d['cpa'])}")
