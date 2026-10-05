"""Public read-only canonical Samhita content endpoint."""
from __future__ import annotations

import json
import os
import re
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from aaptakosha_core.content_contract import validate_markdown, CONTENT_STANDARD_VERSION

ROOT = Path(__file__).resolve().parents[1]
SAMHITA_ROOT = ROOT / "content" / "samhita"
PADARTHA_ROOT = ROOT / "content" / "padartha-vijnanam"
PADARTHA_FILES = {f"y1-pv-{i}": f"{i:02d}-{name}.md" for i, name in enumerate(["ayurveda-nirupana","padartha-darshana-nirupana","dravya-vijnaneeyam","guna-vijnaneeyam","karma-vijnaneeyam","samanya-vijnaneeyam","vishesha-vijnaneeyam","samavaya-vijnaneeyam","abhava-vijnaneeyam","pariksha-vijnaneeyam","aptopadesha-pariksha-pramana","pratyaksha-pariksha-pramana","anumana-pariksha-pramana","yukti-pariksha-pramana","upamana-pramana","karya-karana-siddhanta"], 1)}
SAMHITA_REGISTRY = ROOT / "content" / "samhita-registry.json"
_CONTENT_INDEX_CACHE: dict[str, Path] | None = None
_CONTENT_REGISTRY_CACHE: list[dict] | None = None
_CONTENT_ID = re.compile(
    r"^(?P<text>charaka|madhava|sarangadhara|sharangadhara|ashtanga\.hridaya)\.(?P<section>[a-z]+)\.(?P<chapter>\d{2})$"
)


def _content_registry() -> list[dict]:
    """Load the compact chapter registry without bundling the chapter payloads."""
    global _CONTENT_REGISTRY_CACHE
    if _CONTENT_REGISTRY_CACHE is not None:
        return _CONTENT_REGISTRY_CACHE
    try:
        with SAMHITA_REGISTRY.open(encoding="utf-8") as fh:
            payload = json.load(fh)
        entries = payload.get("entries") if isinstance(payload, dict) else None
        _CONTENT_REGISTRY_CACHE = entries if isinstance(entries, list) else []
    except (OSError, ValueError, TypeError):
        _CONTENT_REGISTRY_CACHE = []
    return _CONTENT_REGISTRY_CACHE


def _content_index() -> dict[str, Path]:
    """Index canonical chapter paths from the compact registry."""
    global _CONTENT_INDEX_CACHE
    if _CONTENT_INDEX_CACHE is not None:
        return _CONTENT_INDEX_CACHE
    index: dict[str, Path] = {}
    for entry in _content_registry():
        if not isinstance(entry, dict):
            continue
        content_id = str(entry.get("content_id") or "").strip()
        path_value = str(entry.get("path") or "").strip()
        if not _CONTENT_ID.fullmatch(content_id) or not path_value:
            continue
        path = (ROOT / path_value).resolve()
        content_root = (ROOT / "content").resolve()
        try:
            path.relative_to(content_root)
        except ValueError:
            continue
        if content_id in index:
            index[content_id] = Path()
        else:
            index[content_id] = path
    _CONTENT_INDEX_CACHE = index
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
    try:
        numeric_number = int(number)
    except (TypeError, ValueError):
        return ""
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
        if start is not None and end is not None and int(start) <= numeric_number <= int(end):
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
        if isinstance(canonical, dict):
            canonical = list(canonical.values())
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
        item["translation_hi"] = (
            item.get("translation_hi")
            or item.get("student_meaning")
            or item.get("meaning_hi")
            or item.get("hindi_translation")
            or _range_for_number(data.get("hindi_translation"), number)
        )
        item["explanation_hi"] = (
            item.get("explanation_hi")
            or item.get("student_explanation_hi")
            or item.get("hindi_explanation")
            or item.get("explanation")
            or _range_for_number(data.get("hindi_learning_summary"), number)
        )
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
    # Preserve legacy Samhita identity fields used by the reader and API contract.
    data["text_id"] = data.get("text_id") or data.get("text") or (content_id.split(".", 1)[0] if "." in content_id else content_id)
    data["khand_id"] = data.get("khand_id") or data.get("section") or (content_id.split(".")[1] if len(content_id.split(".")) > 2 else None)
    data["chapter_id"] = data.get("chapter_id") or data.get("chapter") or data.get("adhyaya_id")
    data["chapter_no"] = data.get("chapter_no") or data.get("chapter_number") or data.get("adhyaya_no")
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


def _static_content_url(content_id: str) -> str | None:
    """Return a stable public URL for a chapter payload without bundling all content into the function."""
    for entry in _content_registry():
        if entry.get("content_id") != content_id:
            continue
        rel = str(entry.get("path") or "").lstrip("/")
        if not rel:
            return None
        host = os.environ.get("VERCEL_URL") or os.environ.get("VERCEL_PROJECT_PRODUCTION_URL")
        if host:
            return f"https://{host}/{rel}"
        commit = os.environ.get("VERCEL_GIT_COMMIT_SHA") or "main"
        return f"https://raw.githubusercontent.com/aaptakosha/AaptaKosha/{commit}/{rel}"
    return None


def _load_remote_content(content_id: str):
    urls = []
    primary = _static_content_url(content_id)
    if primary:
        urls.append(primary)
    for entry in _content_registry():
        if entry.get("content_id") == content_id:
            rel = str(entry.get("path") or "").lstrip("/")
            if rel:
                commit = os.environ.get("VERCEL_GIT_COMMIT_SHA") or "main"
                fallback = f"https://raw.githubusercontent.com/aaptakosha/AaptaKosha/{commit}/{rel}"
                if fallback not in urls:
                    urls.append(fallback)
            break
    for url in urls:
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                return json.loads(response.read().decode("utf-8"))
        except (OSError, ValueError, TypeError, urllib.error.URLError):
            continue
    return None


def load_content(content_id: str):
    canonical = _canonical_id(content_id)
    if canonical is None:
        return None
    path = _content_index().get(canonical)
    if path is not None and path.is_file():
        try:
            path.resolve().relative_to((ROOT / "content").resolve())
            with path.open(encoding="utf-8") as fh:
                return _normalize_payload(json.load(fh), canonical)
        except (OSError, ValueError, TypeError):
            return None
    payload = _load_remote_content(canonical)
    if isinstance(payload, dict):
        return _normalize_payload(payload, canonical)
    return None


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
    for entry in _content_registry():
        if not isinstance(entry, dict):
            continue
        content_id = str(entry.get("content_id") or "").strip()
        if not _CONTENT_ID.fullmatch(content_id):
            continue
        path = _content_index().get(content_id)
        payload = None
        if path is not None and path.is_file():
            try:
                with path.open(encoding="utf-8") as fh:
                    payload = _normalize_payload(json.load(fh), content_id)
            except (OSError, ValueError, TypeError):
                payload = None
        if payload is not None:
            entries.append(_catalog_entry(content_id, payload))
            continue
        match = _CONTENT_ID.fullmatch(content_id)
        text_slug = match.group("text")
        if text_slug == "sarangadhara":
            text_slug = "sharangadhara"
        elif text_slug == "ashtanga.hridaya":
            text_slug = "ashtanga-hridaya"
        chapter = int(match.group("chapter"))
        entries.append({
            "content_id": content_id,
            "text_slug": text_slug,
            "section_key": match.group("section"),
            "chapter_code": f"{chapter:02d}",
            "chapter_label": f"Chapter {chapter}",
            "title": None,
            "title_hi": None,
            "chapter_no": chapter,
            "samhita": None,
            "sthana": None,
        })
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
        if path == "/content/padartha":
            node_id = str(query.get("node_id") or "").strip()
            filename = PADARTHA_FILES.get(node_id)
            if not filename:
                self._reply(400, {"error": {"code": "invalid_node_id"}}); return
            target = (PADARTHA_ROOT / filename).resolve()
            try:
                target.relative_to(PADARTHA_ROOT.resolve())
                markdown = target.read_text(encoding="utf-8")
            except (OSError, ValueError):
                self._reply(404, {"error": {"code": "content_not_found"}}); return
            validation = validate_markdown(markdown)
            if not validation.valid:
                self._reply(409, {"error": {"code": "content_schema_validation_failed",
                    "standard_version": CONTENT_STANDARD_VERSION, "node_id": node_id,
                    "errors": list(validation.errors), "components": dict(validation.components)}}); return
            self._reply(200, {"data": {"node_id": node_id, "content_type": "markdown",
                "content_standard_version": CONTENT_STANDARD_VERSION,
                "components": dict(validation.components), "warnings": list(validation.warnings),
                "content": markdown}})
            return
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
