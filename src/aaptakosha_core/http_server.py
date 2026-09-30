"""Small dependency-free HTTP server for the AaptaKosha transport adapters."""
from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from typing import Any
from .assessment_http_api import AssessmentHttpApi

class AaptaKoshaRequestHandler(BaseHTTPRequestHandler):
    api: AssessmentHttpApi | None = None
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

def serve(api: AssessmentHttpApi, host="127.0.0.1", port=8787):
    handler=type("ConfiguredAaptaKoshaHandler",(AaptaKoshaRequestHandler,),{"api":api})
    server=ThreadingHTTPServer((host,port),handler)
    server.serve_forever()
    return server
__all__=["AaptaKoshaRequestHandler","serve"]
