"""
Nazar — Full Breakdown
Pulls performance across Campaign → AdSet → Ad levels for the last 7 days.

Usage:
    python full_breakdown.py

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


def fetch_level(level, extra_fields=""):
    resp = requests.get(f'{BASE_URL}/{ACCOUNT_ID}/insights', params={
        'access_token': ACCESS_TOKEN,
        'date_preset': 'last_7d',
        'level': level,
        'fields': f'campaign_id,campaign_name,adset_id,adset_name,ad_id,ad_name,spend,impressions,clicks,cpc,ctr,reach,actions,purchase_roas,action_values{extra_fields}',
        'time_increment': 1,
        'limit': 500
    })
    return resp.json()


def aggregate(data, group_key):
    agg = defaultdict(lambda: {
        'spend': 0, 'impressions': 0, 'clicks': 0, 'reach': 0,
        'purchases': 0, 'purchase_value': 0, 'link_clicks': 0,
        'landing_page_views': 0
    })
    for entry in data.get('data', []):
        if group_key == 'campaign':
            key = f"{entry.get('campaign_name','?')} ({entry.get('campaign_id','?')})"
        elif group_key == 'adset':
            key = f"{entry.get('adset_name','?')} ({entry.get('adset_id','?')})"
        else:
            key = f"{entry.get('ad_name','?')} ({entry.get('ad_id','?')})"

        a = agg[key]
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
    return agg


def print_table(title, agg_data):
    print(f"\n{'='*120}")
    print(f"  {title}")
    print(f"{'='*120}")
    print(f"{'Name':<55} {'Spend':>12} {'CPC':>9} {'CTR':>7} {'Purch':>6} {'ROAS':>7} {'CPA':>11}")
    print("-" * 120)

    sorted_items = sorted(agg_data.items(), key=lambda x: x[1]['spend'], reverse=True)
    for name, a in sorted_items:
        spend = a['spend']
        clicks = a['clicks']
        impr = a['impressions']
        pur = a['purchases']
        pval = a['purchase_value']
        cpc = spend / clicks if clicks > 0 else 0
        ctr = (clicks / impr * 100) if impr > 0 else 0
        roas = pval / spend if spend > 0 else 0
        cpa = spend / pur if pur > 0 else 0

        print(f"{name:<55} Rp{spend:>10,.0f} Rp{cpc:>7,.0f} {ctr:>5.2f}% {pur:>5} {roas:>5.2f}x Rp{cpa:>9,.0f}")


if __name__ == '__main__':
    data = fetch_level('ad', ',frequency')

    print_table("📊 Campaign-Level (Last 7 Days)", aggregate(data, 'campaign'))
    print_table("📋 AdSet-Level (Last 7 Days)", aggregate(data, 'adset'))
    print_table("🎨 Ad-Level (Last 7 Days)", aggregate(data, 'ad'))
