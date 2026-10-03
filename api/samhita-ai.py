"""On-demand Samhita translation and simple-meaning pilot endpoint."""
from __future__ import annotations

import json
import os
import urllib.request
from http.server import BaseHTTPRequestHandler
from urllib.error import HTTPError, URLError

GATEWAY = "https://ai-gateway.vercel.sh/v1/chat/completions"
MODEL = "google/gemini-3.1-flash-lite"
LANGUAGES = {
    "hi": "Hindi",
    "en": "English",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu",
}


def _reply(handler: BaseHTTPRequestHandler, status: int, payload: dict):
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def _gateway_token(handler: BaseHTTPRequestHandler) -> str:
    return (
        handler.headers.get("x-vercel-oidc-token")
        or os.environ.get("AI_GATEWAY_API_KEY")
        or os.environ.get("VERCEL_OIDC_TOKEN")
        or ""
    )


def _generate(handler: BaseHTTPRequestHandler, action: str, text: str, target: str):
    language = LANGUAGES[target]
    if action == "translate":
        system = (
            "You are a careful classical Sanskrit translator for an Ayurveda education site. "
            "Translate the supplied Sanskrit faithfully into the requested language. "
            "Preserve technical Ayurvedic terms when a precise equivalent is uncertain, "
            "do not invent commentary, and return only the translation."
        )
        prompt = f"Translate this Sanskrit Ayurveda passage into {language}:\n\n{text}"
    else:
        system = (
            "You are an Ayurveda education assistant. Give a short, student-friendly meaning "
            "of the supplied Sanskrit verse in the requested language. Stay grounded in the "
            "verse, do not add medical advice, and clearly distinguish simple meaning from "
            "the original text. Return only the meaning."
        )
        prompt = f"Give the simple meaning of this Sanskrit Ayurveda verse in {language}:\n\n{text}"

    token = _gateway_token(handler)
    if not token:
        raise RuntimeError("AI Gateway authentication is not configured")

    body = json.dumps(
        {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 700 if action == "meaning" else 500,
            "stream": False,
        },
        ensure_ascii=False,
    ).encode("utf-8")

    req = urllib.request.Request(
        GATEWAY,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=25) as response:
        payload = json.loads(response.read().decode("utf-8"))
    result = payload.get("choices", [{}])[0].get("message", {}).get("content", "")
    if not isinstance(result, str) or not result.strip():
        raise RuntimeError("AI Gateway returned no text")
    return result.strip()


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            action = str(body.get("action", "")).strip()
            text = str(body.get("text", "")).strip()
            target = str(body.get("target", "hi")).strip()

            if action not in {"translate", "meaning"}:
                _reply(self, 400, {"error": {"code": "invalid_action"}})
                return
            if not text or len(text) > 12000:
                _reply(self, 400, {"error": {"code": "invalid_text"}})
                return
            if target not in LANGUAGES:
                _reply(self, 400, {"error": {"code": "unsupported_language"}})
                return

            result = _generate(self, action, text, target)
            _reply(self, 200, {"data": {"action": action, "language": target, "text": result}})
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            _reply(self, 502, {"error": {"code": "ai_gateway_error", "detail": detail}})
        except (URLError, TimeoutError):
            _reply(self, 504, {"error": {"code": "ai_gateway_timeout"}})
        except RuntimeError as exc:
            _reply(self, 503, {"error": {"code": "ai_unavailable", "message": str(exc)}})
        except (ValueError, TypeError, json.JSONDecodeError):
            _reply(self, 400, {"error": {"code": "invalid_request"}})
        except Exception:
            _reply(self, 500, {"error": {"code": "internal_error"}})
