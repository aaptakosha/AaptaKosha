"""Public read-only canonical Samhita content endpoint."""
from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from aaptakosha_core.samhita_adapter import (
    from_charaka_legacy,
    from_sarangadhara_legacy,
)

ROOT = Path(__file__).resolve().parents[1]
SAMHITA_ROOT = ROOT / "content" / "samhita"
_CHARAKA_ID = re.compile(r"^charaka\.sutra\.(\d{2})$")
_SARANGADHARA_ID = re.compile(r"^sarangadhara\.(purva|madhyama|uttara)\.(\d{2})$")


def _safe_json_path(content_id: str) -> Path | None:
    """Resolve only allowlisted canonical content IDs to repository JSON files."""
    match = _CHARAKA_ID.fullmatch(content_id)
    if match:
        chapter_no = int(match.group(1))
        if chapter_no < 1 or chapter_no > 12:
            return None
        return SAMHITA_ROOT / "charaka" / "sutrasthana" / f"adhyaya-{chapter_no:02d}.json"

    match = _SARANGADHARA_ID.fullmatch(content_id)
    if match:
        khanda, chapter_text = match.groups()
        chapter_no = int(chapter_text)
        if chapter_no < 1:
            return None
        chapter_root = SAMHITA_ROOT / "sarangadhara" / khanda
        candidates = sorted(chapter_root.glob(f"chapter-{chapter_no:02d}-*/chapter.json"))
        if len(candidates) != 1:
            return None
        return candidates[0]

    return None


def load_content(content_id: str, *, canonical: bool = False):
    path = _safe_json_path(content_id.strip())
    if path is None or not path.is_file():
        return None
    try:
        path.resolve().relative_to(SAMHITA_ROOT.resolve())
    except ValueError:
        return None
    with path.open(encoding="utf-8") as fh:
        content = json.load(fh)
    if not canonical:
        return content
    if content_id.startswith("charaka.sutra."):
        return from_charaka_legacy(content)
    if content_id.startswith("sarangadhara."):
        return from_sarangadhara_legacy(content)
    return None


class handler(BaseHTTPRequestHandler):
    def _reply(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header(
            "Cache-Control",
            "public, max-age=300, s-maxage=3600, stale-while-revalidate=86400",
        )
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        query = {k: v[-1] for k, v in parse_qs(parsed.query).items()}
        path = parsed.path
        route = query.pop("route", None)
        if route is not None:
            path = "/" + route.lstrip("/")
        if path.startswith("/api"):
            path = path[4:] or "/"
        if path != "/content/samhita":
            self._reply(404, {"error": {"code": "route_not_found"}})
            return
        canonical = query.get("format", "").lower() == "canonical"
        content = load_content(query.get("content_id", ""), canonical=canonical)
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
