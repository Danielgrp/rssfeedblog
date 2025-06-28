# backend/app.py
import json
import os
from flask import Flask, send_from_directory, jsonify

# Path to the scraped data
HERE = os.path.dirname(__file__)
DATA_FILE = os.path.join(HERE, "rss_data.json")

# Where Vite’s production build will live
FRONTEND_DIST = os.path.abspath(os.path.join(HERE, "..", "frontend", "dist"))

app = Flask(
    __name__,
    static_folder=FRONTEND_DIST,    # serve React’s build files
    static_url_path=""              # at the root
)

@app.route("/api/articles")
def articles():
    """Return the scraped RSS articles as JSON."""
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    """
    Serve any file in frontend/dist by path,
    otherwise fall back to index.html (for React Router).
    """
    target = os.path.join(FRONTEND_DIST, path)
    if path and os.path.exists(target):
        return send_from_directory(FRONTEND_DIST, path)
    return send_from_directory(FRONTEND_DIST, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
