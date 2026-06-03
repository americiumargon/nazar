"""
Nazar — Creative Analyzer
Ranks all active ads by 7-day performance across key metrics.

Usage:
    python analyze_creatives.py

Environment variables required:
    META_ACCESS_TOKEN — Your Meta Graph API access token
    META_ACCOUNT_ID    — Your Meta Ads account ID
"""

import requests, json, os
from collections import defaultdict

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
ACCOUNT_ID = os.getenv("META_ACCOUNT_ID")
API_VERSION = 'v22.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

if not ACCESS_TOKEN:
    raise EnvironmentError("META_ACCESS_TOKEN not set.")
if not ACCOUNT_ID:
    raise EnvironmentError("META_ACCOUNT_ID not set.")

resp = requests.get(f'{BASE_URL}/{ACCOUNT_ID}/insights', params={
    'access_token': ACCESS_TOKEN,
    'date_preset': 'last_7d',
    'level': 'ad',
    'fields': 'ad_id,ad_name,spend,impressions,clicks,cpc,ctr,reach,actions,cost_per_action_type,purchase_roas,action_values',
    'time_increment': 1,
    'limit': 200
})
data = resp.json()

agg = defaultdict(lambda: {
    'spend': 0, 'impressions': 0, 'clicks': 0, 'reach': 0,
    'purchases': 0, 'purchase_value': 0, 'link_clicks': 0,
    'landing_page_views': 0
})

for entry in data.get('data', []):
    name = entry['ad_name']
    a = agg[name]
    a['spend'] += float(entry.get('spend', 0))
    a['impressions'] += int(entry.get('impressions', 0))
    a['clicks'] += int(entry.get('clicks', 0))
    a['reach'] += int(entry.get('reach', 0))

    for act in entry.get('actions', []):
        if act['action_type'] == 'purchase':
            a['purchases'] += int(act['value'])
        elif act['action_type'] == 'link_click':
            a['link_clicks'] += int(act['value'])
        elif act['action_type'] == 'landing_page_view':
            a['landing_page_views'] += int(act['value'])

    for av in entry.get('action_values', []):
        if av['action_type'] == 'purchase':
            a['purchase_value'] += float(av['value'])

sorted_ads = sorted(agg.items(), key=lambda x: x[1]['spend'], reverse=True)

print(f"{'Creative':<35} {'Spend':>12} {'Impr':>8} {'CPC':>10} {'CTR':>7} {'Purch':>6} {'ROAS':>7} {'CPA':>10} {'LinkClk':>8} {'LPV':>6}")
print("-" * 135)

for name, a in sorted_ads:
    spend = a['spend']
    impr = a['impressions']
    clicks = a['clicks']
    pur = a['purchases']
    pval = a['purchase_value']
    cpc = spend / clicks if clicks > 0 else 0
    ctr = (clicks / impr * 100) if impr > 0 else 0
    roas = pval / spend if spend > 0 else 0
    cpa = spend / pur if pur > 0 else 0
    lc = a['link_clicks']
    lpv = a['landing_page_views']

    print(f"{name:<35} Rp{spend:>10,.0f} {impr:>7,} Rp{cpc:>8,.0f} {ctr:>5.2f}% {pur:>5} {roas:>5.2f}x Rp{cpa:>8,.0f} {lc:>7,} {lpv:>5,}")
