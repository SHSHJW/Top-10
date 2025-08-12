#!/usr/bin/env python3
import json, os, datetime, urllib.request

# Apple 공식 RSS (한국, 무료 앱 Top 10)
RSS_URL = "https://rss.applemarketingtools.com/api/v2/kr/apps/top-free/10/apps.json"

BASE_DIR = os.path.dirname(__file__)
OUT_PATH = os.path.join(BASE_DIR, "..", "public", "data", "appstore-kr.json")
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

with urllib.request.urlopen(RSS_URL) as resp:
    raw = json.load(resp)

items = []
for idx, entry in enumerate(raw.get('feed', {}).get('results', []), start=1):
    items.append({
        "rank": idx,
        "title": entry.get('name'),
        "artist": entry.get('artistName'),
        "category": (entry.get('genres') or [{}])[0].get('name'),
        "url": entry.get('url'),
        "icon": entry.get('artworkUrl100'),
        "rating": None,
        "ratings": None,
        "price": "무료"
    })

payload = {
    "updatedAt": datetime.datetime.now().isoformat(),
    "items": items
}

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"[OK] Updated {len(items)} items → {OUT_PATH}")
