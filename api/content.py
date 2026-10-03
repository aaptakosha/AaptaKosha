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
        if path.name in {"registry.json", "research.json"}:
            continue
        try:
            with path.open(encoding="utf-8") as fh:
                payload = json.load(fh)
        except (OSError, ValueError, TypeError):
            continue
        content_id = str(payload.get("content_id") or payload.get("chapter_id") or "").strip()
        if not _CONTENT_ID.fullmatch(content_id):
            text_id = str(payload.get("text_id", "")).strip().lower()
            section = str(payload.get("section_id") or payload.get("khand_id") or payload.get("sthana_id") or "").strip().lower()
            chapter_number = payload.get("chapter_number") or payload.get("chapter_no") or payload.get("adhyaya_no")
            if text_id and section and chapter_number is not None:
                content_id = f"{text_id}.{section}.{int(chapter_number):02d}"
        if not _CONTENT_ID.fullmatch(content_id):
            continue
        # A duplicate content_id is never silently selected.
        if content_id in index:
            index[content_id] = Path()
        else:
            index[content_id] = path
    return index



def _parse_legacy_sanskrit(text: str) -> list[dict]:
    """Convert legacy numbered Sanskrit text into the reader's verse shape."""
    if not isinstance(text, str) or not text.strip():
        return []
    import re as _re
    pattern = _re.compile(r"(.*?)(?:॥|।)\s*([0-9०-९]+)\s*(?:॥|।)", _re.S)
    items = []
    last = 0
    for match in pattern.finditer(text):
        chunk = match.group(0).strip()
        if not chunk:
            continue
        raw_no = match.group(2)
        try:
            number = int(raw_no)
        except ValueError:
            number = int(raw_no.translate(str.maketrans("०१२३४५६७८९", "0123456789")))
        items.append({
            "verse_no": number,
            "verse_id": f"legacy-{number:02d}",
            "sanskrit_original": chunk,
        })
        last = match.end()
    if not items and text.strip():
        items.append({"verse_no": 1, "verse_id": "legacy-01", "sanskrit_original": text.strip()})
    return items


def _range_for_number(value, number: int):
    import re as _re
    entries = value if isinstance(value, list) else (list(value.values()) if isinstance(value, dict) else [])
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        raw = entry.get("range") or entry.get("verses")
        if not raw:
            start, end = entry.get("start_verse"), entry.get("end_verse")
        else:
            match = _re.search(r"([0-9०-९]+)\s*[-–]\s*([0-9०-९]+)", str(raw))
            if not match:
                continue
            digits = str(raw).translate(str.maketrans("०१२३४५६७८९", "0123456789"))
            nums = [int(x) for x in _re.findall(r"\d+", digits)]
            start, end = (nums[0], nums[1]) if len(nums) >= 2 else (None, None)
        if start is not None and end is not None and int(start) <= number <= int(end):
            return entry.get("text", "")
    return ""


def _normalize_payload(payload: dict, content_id: str) -> dict:
    """Expose legacy chapter records through the canonical study-reader schema."""
    data = dict(payload)
    text = data.get("sanskrit_text", "")
    raw_verses = data.get("verses")
    if not isinstance(raw_verses, list):
        raw_verses = data.get("passages") if isinstance(data.get("passages"), list) else None
    if raw_verses is None:
        canonical = data.get("canonical_sanskrit")
        if isinstance(canonical, list):
            raw_verses = [
                {
                    "verse_no": (x.get("verse") or x.get("verse_number")) if isinstance(x, dict) else i + 1,
                    "verse_id": f"legacy-{int((x.get('verse') or x.get('verse_number')) if isinstance(x, dict) else i + 1):02d}",
                    "sanskrit_original": x.get("text", "") if isinstance(x, dict) else str(x),
                }
                for i, x in enumerate(canonical)
            ]
        else:
            raw_verses = _parse_legacy_sanskrit(text)
    verses = []
    for i, verse in enumerate(raw_verses or [], 1):
        if not isinstance(verse, dict):
            verse = {"text": str(verse)}
        raw_number = verse.get("verse_no") or verse.get("passage_no") or verse.get("verse") or verse.get("verse_number") or i
        try:
            number = int(raw_number)
        except (TypeError, ValueError):
            number = raw_number
        item = dict(verse)
        item["verse_no"] = number
        item["verse_id"] = item.get("verse_id") or (f"legacy-{int(number):02d}" if str(number).isdigit() else f"legacy-{number}")
        item["sanskrit_original"] = item.get("sanskrit_original") or item.get("text") or item.get("sanskrit") or item.get("sanskrit_text") or ""
        item["translation_hi"] = item.get("translation_hi") or _range_for_number(data.get("hindi_translation"), number)
        item["explanation_hi"] = item.get("explanation_hi") or _range_for_number(data.get("hindi_learning_summary"), number)
        verses.append(item)
    units = []
    for i, unit in enumerate(data.get("learning_units") or [], 1):
        if isinstance(unit, (list, tuple)):
            unit = {"unit_id": unit[0] if len(unit) > 0 else None, "range": unit[1] if len(unit) > 1 else None, "title": unit[2] if len(unit) > 2 else None}
        if not isinstance(unit, dict):
            continue
        u = dict(unit)
        u["unit_id"] = u.get("unit_id") or u.get("id") or f"unit-{i:02d}"
        u["title_hi"] = u.get("title_hi") or u.get("title") or f"Unit {i}"
        raw_range = u.get("range") or u.get("verses")
        if raw_range and not u.get("start_verse"):
            import re as _re
            nums = [int(x) for x in _re.findall(r"\d+", str(raw_range))]
            if len(nums) >= 2:
                u["start_verse"], u["end_verse"] = nums[0], nums[1]
        units.append(u)
    data["content_id"] = content_id
    # Preserve the source chapter_id for legacy texts such as Śārṅgadhara;
    # content_id remains the stable API identifier used for lookup/deep links.
    if not (data.get("text_id") == "sarangadhara" and data.get("chapter_id")):
        data["chapter_id"] = content_id
    data["title"] = data.get("title") or data.get("title_roman") or data.get("title_sanskrit") or content_id
    data["title_hi"] = data.get("title_hi") or data.get("title_roman") or data.get("title_sanskrit") or data["title"]
    data["verses"] = verses
    data["verse_count"] = len(verses)
    data["learning_units"] = units
    return data


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
        return _normalize_payload(json.load(fh), canonical)


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
        payload = _normalize_payload(payload, content_id)
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
