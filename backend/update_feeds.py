#!/usr/bin/env python3
import csv, json, os, sys, re
from collections import defaultdict

CSV_IN   = "rss_discovery_results.csv"
JSON_OUT = "rss_feeds.json"
RSS_RE   = re.compile(r"rss", re.IGNORECASE)

def load_candidates(path):
    cands = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            uni   = (row.get("university") or row.get("name") or "").strip()
            url   = (row.get("feed_url") or row.get("rss_feed_url") or "").strip()
            text  = (row.get("link_text") or "").strip()
            depth = row.get("depth") or row.get("level") or "0"
            if not uni or not url:
                continue
            try:    d = int(depth)
            except: d = 999
            cands[uni].append({"url":url, "text":text, "depth":d})
    return cands

def pick_primary(c):
    # 1) prefer any whose link_text mentions “rss”
    rssy = [x for x in c if RSS_RE.search(x["text"])]
    if not rssy:
        rssy = c[:]
    # 2) pick shallowest
    mind = min(x["depth"] for x in rssy)
    shallow = [x for x in rssy if x["depth"]==mind]
    return shallow[0]

def main():
    if not os.path.exists(CSV_IN):
        print(f"❌ {CSV_IN} not found", file=sys.stderr)
        sys.exit(1)

    all_c = load_candidates(CSV_IN)
    primary = []
    for uni, cand in sorted(all_c.items()):
        choice = pick_primary(cand)
        primary.append({"university":uni, "feed_url":choice["url"]})

    with open(JSON_OUT,"w",encoding="utf-8") as f:
        json.dump(primary, f, ensure_ascii=False, indent=2)
    print(f"✅ Picked {len(primary)} primary feeds → {JSON_OUT}")

if __name__=="__main__":
    main()
