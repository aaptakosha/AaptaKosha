"""Public read-only canonical Samhita content endpoint."""
from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
SAMHITA_ROOT = ROOT / "content" / "samhita"
_CONTENT_ID = re.compile(
    r"^(?P<text>charaka|sarangadhara|sharangadhara|ashtanga\.hridaya)\.(?P<section>[a-z]+)\.(?P<chapter>\d{2})$"
)


def _content_index() -> dict[str, Path]:
    """Index canonical chapter JSON files by their embedded content_id."""
    index: dict[str, Path] = {}
    if not SAMHITA_ROOT.is_dir():
        return index
    for path in SAMHITA_ROOT.rglob("*.json"):
        try:
            with path.open(encoding="utf-8") as fh:
                payload = json.load(fh)
        except (OSError, ValueError, TypeError):
            continue
        content_id = str(payload.get("content_id", "")).strip()
        if not _CONTENT_ID.fullmatch(content_id):
            text_id = str(payload.get("text_id", "")).strip()
            section = str(payload.get("section_id") or payload.get("khand_id") or "").strip()
            chapter_number = payload.get("chapter_number")
            if text_id == "sarangadhara" and section and chapter_number is not None:
                content_id = f"sarangadhara.{section}.{int(chapter_number):02d}"
        if not _CONTENT_ID.fullmatch(content_id):
            continue
        # A duplicate content_id is never silently selected.
        if content_id in index:
            index[content_id] = Path()
        else:
            index[content_id] = path
    return index


def _canonical_id(content_id: str) -> str | None:
    match = _CONTENT_ID.fullmatch(content_id.strip())
    if not match:
        return None
    text = match.group("text")
    if text == "sharangadhara":
        text = "sarangadhara"
    return f"{text}.{match.group('section')}.{match.group('chapter')}"


def load_content(content_id: str):
    canonical = _canonical_id(content_id)
    if canonical is None:
        return None
    path = _content_index().get(canonical)
    if path is None or not path.is_file():
        return None
    try:
        path.resolve().relative_to(SAMHITA_ROOT.resolve())
    except ValueError:
        return None
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _catalog_entry(content_id: str, payload: dict) -> dict:
    match = _CONTENT_ID.fullmatch(content_id)
    text = match.group("text")
    if text == "sarangadhara":
        text_slug = "sharangadhara"
    elif text == "ashtanga.hridaya":
        text_slug = "ashtanga-hridaya"
    else:
        text_slug = text
    chapter = match.group("chapter")
    return {
        "content_id": content_id,
        "text_slug": text_slug,
        "section_key": match.group("section"),
        "chapter_code": chapter,
        "chapter_label": payload.get("title_hi") or payload.get("title") or f"Chapter {int(chapter)}",
        "title": payload.get("title"),
        "title_hi": payload.get("title_hi"),
        "chapter_no": payload.get("chapter_no") or int(chapter),
        "samhita": payload.get("samhita"),
        "sthana": payload.get("sthana"),
    }


def catalog():
    entries = []
    for content_id, path in _content_index().items():
        if not path.is_file():
            continue
        try:
            with path.open(encoding="utf-8") as fh:
                payload = json.load(fh)
        except (OSError, ValueError, TypeError):
            continue
        entries.append(_catalog_entry(content_id, payload))
    return sorted(entries, key=lambda x: (x["text_slug"], x["section_key"], int(x["chapter_code"])))


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
        if query.get("catalog") == "1":
            self._reply(200, {"data": {"chapters": catalog()}})
            return
        content = load_content(query.get("content_id", ""))
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
