"""Public read-only canonical Samhita content endpoint."""
from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT=Path(__file__).resolve().parents[1]
CONTENT_ROOT=ROOT/"content"/"samhita"/"charaka"/"sutrasthana"

def load_content(content_id:str):
    if not content_id.startswith("charaka.sutra."):
        return None
    try:
        chapter_no=int(content_id.rsplit(".",1)[-1])
    except ValueError:
        return None
    path=CONTENT_ROOT/f"adhyaya-{chapter_no:02d}.json"
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)

class handler(BaseHTTPRequestHandler):
    def _reply(self,status,payload):
        data=json.dumps(payload,ensure_ascii=False,separators=(",",":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(data)))
        self.send_header("Cache-Control","public, max-age=300, s-maxage=3600, stale-while-revalidate=86400")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed=urlparse(self.path)
        query={k:v[-1] for k,v in parse_qs(parsed.query).items()}
        path=parsed.path
        route=query.pop("route",None)
        if route is not None:
            path="/"+route.lstrip("/")
        if path.startswith("/api"):
            path=path[4:] or "/"
        if path!="/content/samhita":
            self._reply(404,{"error":{"code":"route_not_found"}})
            return
        content=load_content(query.get("content_id","").strip())
        if content is None:
            self._reply(404,{"error":{"code":"content_not_found"}})
            return
        self._reply(200,{"data":content})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods","GET,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Authorization, Content-Type")
        self.end_headers()

    def do_POST(self):
        self._reply(405,{"error":{"code":"method_not_allowed"}})
