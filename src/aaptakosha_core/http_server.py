"""Small dependency-free HTTP server for the AaptaKosha transport adapters."""
from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from typing import Any
from .assessment_http_api import AssessmentHttpApi
from .api import CatalogApi
from .curriculum_hierarchy_api import CurriculumHierarchyApi

class AaptaKoshaHttpApi:
    """Route assessment, catalog, and curriculum-hierarchy API adapters together."""

    def __init__(
        self,
        assessment: AssessmentHttpApi,
        catalog: CatalogApi | None = None,
        hierarchy: CurriculumHierarchyApi | None = None,
    ):
        self.assessment = assessment
        self.catalog = catalog
        self.hierarchy = hierarchy

    def handle(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
        query: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        body, query = body or {}, query or {}
        parts = [p for p in path.strip("/").split("/") if p]

        if self.catalog is not None and parts[:2] == ["api", "catalog"] and method == "GET":
            if len(parts) == 3:
                return self.catalog.get_curriculum(parts[2], query.get("version"))
            if len(parts) == 4 and parts[3] == "subjects":
                return self.catalog.list_subjects(parts[2], query.get("version"))
            if len(parts) == 5 and parts[3] == "subjects":
                return self.catalog.get_subject(parts[2], parts[4], query.get("version"))

        if self.hierarchy is not None and parts[:3] == ["api", "curriculum", "nodes"] and method == "GET":
            if len(parts) == 3:
                curriculum_id = query.get("curriculum_id")
                if not curriculum_id:
                    return {"status": 400, "error": {"code": "invalid_request", "message": "curriculum_id is required"}}
                return self.hierarchy.list_nodes(
                    curriculum_id,
                    query.get("subject_id"),
                    query.get("version"),
                    query.get("parent_node_id"),
                )
            if len(parts) == 4:
                return self.hierarchy.get_node(
                    parts[3], query.get("curriculum_id"), query.get("version")
                )

        # Preserve all existing assessment routes exactly as before.
        assessment_path = "/" + "/".join(parts[1:] if parts[:1] == ["api"] else parts)
        return self.assessment.handle(method, assessment_path, body, query)

    @staticmethod
    def json_response(result: dict[str, Any]) -> tuple[int, str]:
        return AssessmentHttpApi.json_response(result)


class AaptaKoshaRequestHandler(BaseHTTPRequestHandler):
    api: AaptaKoshaHttpApi | AssessmentHttpApi | None = None
    def _send(self, status: int, payload: str) -> None:
        data = payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)
    def _handle(self) -> None:
        if self.api is None:
            self._send(503, json.dumps({"error":{"code":"not_configured"}})); return
        parsed=urlparse(self.path)
        query={k:v[-1] for k,v in parse_qs(parsed.query).items()}
        length=int(self.headers.get("Content-Length","0"))
        body=None
        if length:
            try: body=json.loads(self.rfile.read(length))
            except (json.JSONDecodeError, UnicodeDecodeError):
                self._send(400,json.dumps({"error":{"code":"invalid_json"}})); return
        result=self.api.handle(self.command,parsed.path,body,query)
        self._send(*self.api.json_response(result))
    def do_GET(self): self._handle()
    def do_POST(self): self._handle()
    def do_PUT(self): self._handle()
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","GET,POST,PUT,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()
    def log_message(self, format, *args): return

def serve(\n    api: AssessmentHttpApi,\n    host="127.0.0.1",\n    port=8787,\n    *,\n    catalog: CatalogApi | None = None,\n    hierarchy: CurriculumHierarchyApi | None = None,\n):
    routed_api = AaptaKoshaHttpApi(api, catalog, hierarchy) if catalog is not None or hierarchy is not None else api\n    handler=type("ConfiguredAaptaKoshaHandler",(AaptaKoshaRequestHandler,),{"api":routed_api})
    server=ThreadingHTTPServer((host,port),handler)
    server.serve_forever()
    return server
__all__=["AaptaKoshaHttpApi","AaptaKoshaRequestHandler","serve"]
