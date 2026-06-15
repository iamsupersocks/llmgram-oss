from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "sample_data"


def load_json(name: str) -> Any:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def filter_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    q = (request.args.get("q") or "").strip().lower()
    category = (request.args.get("category") or "").strip().lower()
    if q:
        rows = [row for row in rows if q in json.dumps(row, ensure_ascii=False).lower()]
    if category:
        rows = [row for row in rows if str(row.get("category", "")).lower() == category]
    limit = max(min(int(request.args.get("limit", 20) or 20), 100), 1)
    offset = max(int(request.args.get("offset", 0) or 0), 0)
    return rows[offset:offset + limit]


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def home():
        weekly = load_json("weekly.json")
        signals = load_json("signals.json")
        sources = load_json("sources.json")
        return render_template("index.html", weekly=weekly, signals=signals, sources=sources)

    @app.get("/api/signals")
    def signals():
        return jsonify({"items": filter_rows(load_json("signals.json"))})

    @app.get("/api/weekly")
    def weekly():
        return jsonify(load_json("weekly.json"))

    @app.get("/api/sources")
    def sources():
        return jsonify({"items": load_json("sources.json")})

    @app.get("/api/stats")
    def stats():
        weekly = load_json("weekly.json")
        signals = load_json("signals.json")
        return jsonify({
            **weekly.get("stats", {}),
            "sample_signals": len(signals),
            "sample_sources": len(load_json("sources.json")),
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
