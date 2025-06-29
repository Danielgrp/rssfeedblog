#!/usr/bin/env python3
import csv
import feedparser

INPUT_CSV  = "rss_discovery_results.csv"
OUTPUT_CSV = "rss_verified.csv"

with open(INPUT_CSV, newline="", encoding="utf-8") as inf, \
     open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as outf:

    reader = csv.DictReader(inf)
    writer = csv.writer(outf)
    writer.writerow(["university","candidate_url","link_text","depth","entries_found"])

    for row in reader:
        url      = row.get("feed_url") or ""
        uni      = row.get("university") or row.get("name","")
        text     = row.get("link_text","")
        depth    = row.get("depth",row.get("level",""))
        parsed   = feedparser.parse(url)
        count    = len(parsed.entries or [])
        writer.writerow([uni, url, text, depth, count])

print("✅ Wrote verification results to rss_verified.csv")
