#!/usr/bin/env python3
import json, feedparser, datetime, os, sys

HERE        = os.path.dirname(__file__)
FEEDS_FILE  = os.path.join(HERE, "rss_feeds.json")
OUTPUT_FILE = os.path.join(HERE, "rss_data.json")
DAYS_BACK   = 10

def load_feeds():
    if not os.path.exists(FEEDS_FILE):
        print(f"❌ Missing {FEEDS_FILE}", file=sys.stderr)
        sys.exit(1)
    return json.load(open(FEEDS_FILE, encoding="utf-8"))

def extract_image(entry):
    # media:content or any link[type=image]
    for media in entry.get("media_content", []):
        if media.get("url"):
            return media["url"]
    for link in entry.get("links", []):
        if link.get("type","").startswith("image"):
            return link.get("href")
    return "https://via.placeholder.com/400x200"

def fetch_recent(url):
    parsed = feedparser.parse(url)
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=DAYS_BACK)
    items  = []
    for e in parsed.entries:
        dp = e.get("published_parsed") or e.get("updated_parsed")
        if not dp:
            continue
        dt = datetime.datetime(*dp[:6], tzinfo=datetime.timezone.utc)
        if dt < cutoff:
            continue
        items.append({
            "title":   e.get("title",""),
            "link":    e.get("link",""),
            "date":    dt.isoformat(),
            "excerpt": e.get("summary","")[:900],
            "image":   extract_image(e),
        })
    return items

def main():
    feeds = load_feeds()
    all_items = []

    for f in feeds:
        uni, url = f["university"], f["feed_url"]
        print(f"→ Fetching {uni} …", end=" ")
        try:
            recs = fetch_recent(url)
            for r in recs:
                r["university"] = uni
            all_items.extend(recs)
            print(f"✔ {len(recs)} articles")
        except Exception as e:
            print(f"⚠ {e.__class__.__name__}")

    with open(OUTPUT_FILE,"w",encoding="utf-8") as out:
        json.dump(all_items, out, ensure_ascii=False, indent=2)

    print(f"\n🎉 Total collected: {len(all_items)} articles")
    print(f"✅ Written to `{os.path.basename(OUTPUT_FILE)}`")

if __name__=="__main__":
    main()
