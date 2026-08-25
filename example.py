"""Minimal Google Trends — trending now API call — one typed row per trend.

Docs & schema: https://quanticdata.io/collectors/google-trends-api/
"""
import json
import os

import requests

API = "https://api.quanticdata.io/v1/scraper/collectors/google_trends/run"
KEY = os.environ["QD_API_KEY"]  # https://quanticdata.io/

payload = {
        "country": "us",
        "max_results": 10
    }

r = requests.post(
    API,
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json=payload,
    timeout=180,
)
r.raise_for_status()
data = r.json()["payload"]

for row in data["results"]:
    print(row.get("query"), row.get("approx_traffic"), row.get("published"))
print(f"{len(data['results'])} trends, cost ${data['cost']}")
