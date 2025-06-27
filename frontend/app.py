from flask import Flask, render_template
import feedparser
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/feeds")
def show_feeds():
    feed_url = "https://www.nature.com/nature.rss"  # Example feed
    feed = feedparser.parse(feed_url)
    entries = feed.entries[:5]  # Limit to top 5 entries

    return render_template("feeds.html", entries=entries)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
