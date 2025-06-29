#!/usr/bin/env python3
import os
from flask import Flask, jsonify, send_from_directory
from fetch_rss import fetch_all_articles

# point this at wherever your front-end build lives
STATIC_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../frontend/dist")
)

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path="")

@app.route("/api/feeds")
def api_feeds():
    """
    Fetch the latest articles from all your RSS feeds
    and return them as JSON.
    """
    try:
        articles = fetch_all_articles()
        return jsonify(articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    """
    Serve your React/Vite app. If the requested file exists in
    the built `dist` folder, serve it; otherwise fall back to index.html.
    """
    full_path = os.path.join(STATIC_FOLDER, path)
    if path and os.path.exists(full_path):
        return send_from_directory(STATIC_FOLDER, path)
    return send_from_directory(STATIC_FOLDER, "index.html")

if __name__ == "__main__":
    # Use PORT env var if available (e.g. on Render), else default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Listen on all interfaces so it’s reachable externally
    app.run(host="0.0.0.0", port=port)
