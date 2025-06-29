#!/usr/bin/env python3
import sys
import types

# ─── Python 3.13 has removed the stdlib 'cgi' module, but Feedparser still does:
#       import cgi;  ... = cgi.parse_header(...)
# ─── So we inject our own tiny 'cgi' module before feedparser loads.

if "cgi" not in sys.modules:
    _cgi = types.ModuleType("cgi")
    def parse_header(header_value):
        """
        Splits a header like "text/html; charset=UTF-8" into
        ("text/html", {"charset": "UTF-8"})
        """
        parts = header_value.split(";")
        main_value = parts[0].strip()
        params = {}
        for p in parts[1:]:
            if "=" in p:
                k, v = p.split("=", 1)
                k = k.strip().lower()
                v = v.strip().strip('"').strip("'")
                params[k] = v
        return main_value, params

    _cgi.parse_header = parse_header
    sys.modules["cgi"] = _cgi

# ─── Now the real import
import os
import json
import datetime
import feedparser

# ——— CONFIG —————————————————————————————————————————————————————————————————
HERE        = os.path.dirname(__file__)
FEEDS_FILE  = os.path.join(HERE, "rss_feeds.json")
OUTPUT_FILE = os.path.join(HERE, "rss_data.json")
DAYS_LIMIT  = 10

# ——— LOAD PRIMARY RSS URLs ——————————————————————————————————————————————————
def load_feeds():
    """
    Load the list of primary feeds you picked in update_feeds.py.
    Expects JSON of the form:
      [
        { "university": "...", "feed_url": "https://..." },
        ...
      ]
    """
    with open(FEEDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ——— FETCH AN INDIVIDUAL FEED —————————————————————————————————————————————————
def fetch_recent_articles(feed, days=DAYS_LIMIT):
    uni = feed["university"]
    url = feed["feed_url"]
    parsed = feedparser.parse(url)
    entries = []

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    cutoff  = now_utc - datetime.timedelta(days=days)

    for e in parsed.entries:
        ts = e.get("published_parsed") or e.get("updated_parsed")
        if not ts:
            continue
        dt = datetime.datetime(*ts[:6], tzinfo=datetime.timezone.utc)
        if dt < cutoff:
            continue

        # pick an image if any
        img = None
        if "media_content" in e:
            for m in e.media_content:
                if m.get("url"):
                    img = m["url"]
                    break
        if not img and "links" in e:
            for l in e.links:
                if l.get("type","").startswith("image"):
                    img = l["href"]
                    break
        if not img:
            img = "https://via.placeholder.com/400x200"

        summary = e.get("summary") or e.get("description") or ""
        excerpt = summary[:900]

        entries.append({
            "university": uni,
            "title":      e.get("title","No Title"),
            "link":       e.get("link",""),
            "date":       dt.isoformat(),
            "excerpt":    excerpt,
            "image":      img
        })

    return entries

# ——— COLLECT ALL FEEDS ————————————————————————————————————————————————————
def fetch_all_articles():
    all_articles = []
    feeds = load_feeds()

    for feed in feeds:
        try:
            arts = fetch_recent_articles(feed)
            count = len(arts)
            print(f"→ Fetching {feed['university']} … ✔ {count} article{'s' if count!=1 else ''}")
            all_articles.extend(arts)
        except Exception as e:
            print(f"⚠ Failed to parse {feed['university']} → {feed['feed_url']}  ({e})")

    print(f"🎉 Total collected: {len(all_articles)} articles")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)
    print(f"✅ Written to `{os.path.basename(OUTPUT_FILE)}`")

    return all_articles

# ——— STAND-ALONE RUNNER ——————————————————————————————————————————————————
if __name__ == "__main__":
    fetch_all_articles()
