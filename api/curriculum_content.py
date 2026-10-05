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


def _markdown_path(subject: str, node_id: str):
    maps = {
        "AyUG-PV": {
            "y1-pv-1": "content/padartha-vijnanam/01-ayurveda-nirupana.md",
            "y1-pv-2": "content/padartha-vijnanam/02-padartha-darshana-nirupana.md",
            "y1-pv1-3": "content/padartha-vijnanam/03-dravya-vijnaneeyam.md",
            "y1-pv1-4": "content/padartha-vijnanam/04-guna-vijnaneeyam.md",
            "y1-pv1-5": "content/padartha-vijnanam/05-karma-vijnaneeyam.md",
            "y1-pv1-6": "content/padartha-vijnanam/06-samanya-vijnaneeyam.md",
            "y1-pv1-7": "content/padartha-vijnanam/07-vishesha-vijnaneeyam.md",
            "y1-pv1-8": "content/padartha-vijnanam/08-samavaya-vijnaneeyam.md",
            "y1-pv1-9": "content/padartha-vijnanam/09-abhava-vijnaneeyam.md",
            "y1-pv2-1": "content/padartha-vijnanam/10-pariksha-vijnaneeyam.md",
            "y1-pv2-2": "content/padartha-vijnanam/11-aptopadesha-pariksha-pramana.md",
            "y1-pv2-3": "content/padartha-vijnanam/12-pratyaksha-pariksha-pramana.md",
            "y1-pv2-4": "content/padartha-vijnanam/13-anumana-pariksha-pramana.md",
            "y1-pv2-5": "content/padartha-vijnanam/14-yukti-pariksha-pramana.md",
            "y1-pv2-6": "content/padartha-vijnanam/15-upamana-pramana.md",
            "y1-pv2-7": "content/padartha-vijnanam/16-karya-karana-siddhanta.md",
        },
        "AyUG-KS": {
            "y1-ks-1": "content/kriya-sharir/01-sharir.md",
        },
        "AyUG-SN-AI": {
            "y1-snai1-1": "content/sanskrit/01-varnamala-uccharana.md",
            "y1-snai1-2": "content/sanskrit/02-samjna-avyaya.md",
            "y1-snai1-3": "content/sanskrit/08-upasarga-pratyaya.md",
            "y1-snai1-4": "content/sanskrit/02-samjna-avyaya.md",
            "y1-snai1-5": "content/sanskrit/05-karaka-vibhakti.md",
            "y1-snai1-6": "content/sanskrit/06-sandhi.md",
            "y1-snai1-7": "content/sanskrit/07-samasa.md",
            "y1-snai1-8": "content/sanskrit/03-shabdarupa-sarvanama.md",
            "y1-snai1-9": "content/sanskrit/04-dhaturupa.md",
            "y1-snai1-10": "content/sanskrit/08-upasarga-pratyaya.md",
            "y1-snai2-a1": "content/sanskrit/paper-2/part-a/01-nirukti-paryaya.md",
            "y1-snai2-a2": "content/sanskrit/paper-2/part-a/02-paribhasha.md",
            "y1-snai2-a3": "content/sanskrit/paper-2/part-a/03-ashtanga-hridaya.md",
            "y1-snai2-a4": "content/sanskrit/paper-2/part-a/04-ayurveda-subhashita.md",
            "y1-snai2-a5": "content/sanskrit/paper-2/part-a/05-panchatantra.md",
        },
    }
    rel = maps.get(subject, {}).get(node_id)
    if not rel:
        return None
    path = (ROOT / rel).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return path


def _markdown_payload(subject: str, node_id: str, code: str):
    path = _markdown_path(subject, node_id)
    if path is None or not path.is_file():
        return None
    try:
        return {
            "node_id": node_id,
            "node_code": code,
            "content_type": "markdown",
            "content": path.read_text(encoding="utf-8"),
            "source_path": str(path.relative_to(ROOT)),
        }
    except (OSError, UnicodeError):
        return None


def load_content(subject_id: str, node_code: str, node_id: str = ""):
    subject = _safe(subject_id)
    code = _safe(node_code)
    node_id = _safe(node_id)
    if not subject or not code:
        return None
    markdown = _markdown_payload(subject, node_id or "", code)
    if markdown is not None:
        return markdown
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
    elif subject == "AyUG-SA1" and code == "AH.Su.9":
        path = CONTENT_ROOT / subject / "AH-Su-09-DravyadiVijnaniya.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.10":
        path = CONTENT_ROOT / subject / "AH-Su-10-Rasabhediya.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.11":
        path = CONTENT_ROOT / subject / "AH-Su-11-DoshadiVijnaniya.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.12":
        path = CONTENT_ROOT / subject / "AH-Su-12-Doshabhediya.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.13":
        path = CONTENT_ROOT / subject / "AH-Su-13-Doshopakramaniya.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.14":
        path = CONTENT_ROOT / subject / "AH-Su-14-Dvividhopakramaniya.json"
    elif subject == "AyUG-SA1" and code == "AH.Su.15":
        path = CONTENT_ROOT / subject / "AH-Su-15-ShodhanadiganaSangraha.json"
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
        content = load_content(query.get("subject_id", ""), query.get("node_code", ""), query.get("node_id", ""))
        if content is None:
            self._reply(404, {"error": {"code": "content_not_found"}})
            return
        self._reply(200, {"data": content})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.end_headers()

    def do_POST(self, _request=None):
        self._reply(405, {"error": {"code": "method_not_allowed"}})
