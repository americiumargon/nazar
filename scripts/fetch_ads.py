"""
Nazar — Meta Ads Data Fetcher
Pulls account-level insights from the Meta Graph API.

Usage:
    python fetch_ads.py

Environment variables required:
    META_ACCESS_TOKEN — Your Meta Graph API access token
"""

import requests, json, os
from datetime import datetime, timezone, timedelta

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
API_VERSION = "v22.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

if not ACCESS_TOKEN:
    raise EnvironmentError("META_ACCESS_TOKEN not set. Create a .env file or export it.")

bangkok = timezone(timedelta(hours=7))
today = datetime.now(bangkok).strftime("%Y-%m-%d")

print(f"=== Querying Meta Ads for {today} (GMT+7) ===")
print()

# Get ad accounts
resp = requests.get(f"{BASE_URL}/me/adaccounts", params={
    "access_token": ACCESS_TOKEN,
    "fields": "id,name,account_status,currency,timezone_name"
})
print("--- Ad Accounts ---")
data = resp.json()
print(json.dumps(data, indent=2))

if "data" in data and len(data["data"]) > 0:
    account_id = data["data"][0]["id"]
    account_name = data["data"][0]["name"]
    print(f"\nUsing account: {account_name} ({account_id})")

    # Today's insights
    print(f"\n--- Today's Insights ({today}) ---")
    insights = requests.get(f"{BASE_URL}/{account_id}/insights", params={
        "access_token": ACCESS_TOKEN,
        "date_preset": "today",
        "level": "account",
        "fields": "spend,impressions,clicks,cpc,cpm,ctr,reach,actions,cost_per_action_type,action_values,purchase_roas"
    })
    print(json.dumps(insights.json(), indent=2))

    # Yesterday's insights
    print(f"\n--- Yesterday's Insights ---")
    yesterday = requests.get(f"{BASE_URL}/{account_id}/insights", params={
        "access_token": ACCESS_TOKEN,
        "date_preset": "yesterday",
        "level": "account",
        "fields": "spend,impressions,clicks,cpc,cpm,ctr,reach,actions,cost_per_action_type,action_values,purchase_roas"
    })
    print(json.dumps(yesterday.json(), indent=2))

    # Last 7 days breakdown
    print(f"\n--- Last 7 Days Breakdown ---")
    week = requests.get(f"{BASE_URL}/{account_id}/insights", params={
        "access_token": ACCESS_TOKEN,
        "date_preset": "last_7d",
        "time_increment": 1,
        "level": "account",
        "fields": "spend,impressions,clicks,cpc,cpm,ctr,reach,actions,cost_per_action_type,purchase_roas"
    })
    print(json.dumps(week.json(), indent=2))
else:
    print("ERROR: No ad accounts found or access token invalid!")
