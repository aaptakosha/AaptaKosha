"""NCISM curriculum teaching-content endpoint.

Content is stored as small static JSON files so curriculum chapters do not inflate
the Python function bundle. The endpoint maps a curriculum subject + node to the
corresponding static lesson payload.
"""
from __future__ import annotations
import json
import re
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOT = ROOT / "content" / "curriculum" / "ncism-first-professional"

SAFE = re.compile(r"^[A-Za-z0-9._-]+$")


def _safe(value: str) -> str | None:
    value = str(value or "").strip()
    return value if value and SAFE.fullmatch(value) else None


def load_content(subject_id: str, node_code: str):
    subject = _safe(subject_id)
    code = _safe(node_code)
    if not subject or not code:
        return None
    # Current file convention: AH.Su.1 -> AH-Su-01-*.json
    if subject == "AyUG-SA1" and code == "AH.Su.1":
        path = CONTENT_ROOT / subject / "AH-Su-01-Ayushkamiya.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.2":
        path = CONTENT_ROOT / subject / "AH-Su-02-Dinacharya.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.3":
        path = CONTENT_ROOT / subject / "AH-Su-03-Ritucharya.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.4":
        path = CONTENT_ROOT / subject / "AH-Su-04-Roganutpadaniya.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.5":
        path = CONTENT_ROOT / subject / "AH-Su-05-DravadravyaVijnaniya.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.6":
        path = CONTENT_ROOT / subject / "AH-Su-06-AnnasvarupaVijnaniya.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.7":
        path = CONTENT_ROOT / subject / "AH-Su-07-Annaraksha.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.8":
        path = CONTENT_ROOT / subject / "AH-Su-08-Matrashitiya.json"
    else:
        return None
    try:
        path.relative_to(CONTENT_ROOT)
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError, TypeError):
        return None


class handler(BaseHTTPRequestHandler):
    def _reply(self, status: int, payload: dict):
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "public, max-age=300, s-maxage=3600, stale-while-revalidate=86400")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        query = {k: v[-1] for k, v in parse_qs(parsed.query).items()}
        path = parsed.path
        if path.startswith("/api"):
            path = path[4:] or "/"
        if path != "/curriculum/content":
            self._reply(404, {"error": {"code": "route_not_found"}})
            return
        content = load_content(query.get("subject_id", ""), query.get("node_code", ""))
        if content is None:
            self._reply(404, {"error": {"code": "content_not_found"}})
            return
        self._reply(200, {"data": content})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.end_headers()

    def do_POST(self):
        self._reply(405, {"error": {"code": "method_not_allowed"}})
