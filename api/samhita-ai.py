"""On-demand Samhita translation and simple-meaning pilot endpoint."""
from __future__ import annotations

import json
import os
import time
import urllib.request
from http.server import BaseHTTPRequestHandler

try:
    from clerk_backend_api import AuthenticateRequestOptions, authenticate_request
except ImportError:  # pragma: no cover - dependency is declared in pyproject.toml
    AuthenticateRequestOptions = None
    authenticate_request = None
from urllib.error import HTTPError, URLError

GATEWAY = "https://ai-gateway.vercel.sh/v1/chat/completions"
MODEL = "google/gemini-3.1-flash-lite"
PILOT_CONTENT_ID = "ashtanga.hridaya.sutra.01"
MAX_INPUT_CHARS = 6000
RATE_LIMIT_MAX = 10
RATE_LIMIT_WINDOW_SECONDS = 600
_RATE_LIMIT: dict[str, list[float]] = {}
LANGUAGES = {
    "hi": "Hindi",
    "en": "English",
    "mr": "Marathi",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "bo": "Tibetan",
}


def _reply(handler: BaseHTTPRequestHandler, status: int, payload: dict):
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def _require_user(handler: BaseHTTPRequestHandler) -> str:
    """Require a verified Clerk session token sent explicitly as Bearer auth."""
    # Clerk can authenticate from the Authorization header or the same-origin
    # session cookie. The browser may not have a usable bearer token immediately
    # after Clerk bootstraps, so do not reject cookie-authenticated sessions here.
    if authenticate_request is None or AuthenticateRequestOptions is None:
        raise RuntimeError("Clerk authentication is not configured")

    authorized_parties = [
        item.strip()
        for item in os.environ.get("CLERK_AUTHORIZED_PARTIES", "").split(",")
        if item.strip()
    ]
    if not authorized_parties:
        raise RuntimeError("Clerk authorized parties are not configured")

    try:
        state = authenticate_request(
            handler,
            AuthenticateRequestOptions(
                secret_key=os.environ.get("CLERK_SECRET_KEY"),
                jwt_key=os.environ.get("CLERK_JWT_KEY"),
                authorized_parties=authorized_parties,
                accepts_token=["session_token"],
            ),
        )
    except Exception as exc:
        raise PermissionError("authentication_invalid") from exc

    if not getattr(state, "is_signed_in", False):
        raise PermissionError("authentication_invalid")

    payload = getattr(state, "payload", None) or {}
    user_id = payload.get("sub") if isinstance(payload, dict) else None
    if not user_id:
        raise PermissionError("authentication_invalid")
    return str(user_id)


def _rate_limit(user_id: str) -> int | None:
    """Small per-user pilot guard; durable rate limiting can be added before broad rollout."""
    now = time.time()
    recent = [t for t in _RATE_LIMIT.get(user_id, []) if now - t < RATE_LIMIT_WINDOW_SECONDS]
    if len(recent) >= RATE_LIMIT_MAX:
        _RATE_LIMIT[user_id] = recent
        return max(1, int(RATE_LIMIT_WINDOW_SECONDS - (now - recent[0])))
    recent.append(now)
    _RATE_LIMIT[user_id] = recent
    return None


def _gateway_token(handler: BaseHTTPRequestHandler) -> str:
    # Prefer the deployment's own short-lived OIDC credential. Do not trust a
    # browser-supplied header for gateway authentication.
    return (
        os.environ.get("VERCEL_OIDC_TOKEN")
        or os.environ.get("AI_GATEWAY_API_KEY")
        or os.environ.get("VERCEL_AI_GATEWAY_KEY")
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
            if length <= 0 or length > 16000:
                _reply(self, 413, {"error": {"code": "request_too_large"}})
                return
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            action = str(body.get("action", "")).strip()
            text = str(body.get("text", "")).strip()
            target = str(body.get("target", "hi")).strip()
            content_id = str(body.get("content_id", "")).strip()

            if content_id != PILOT_CONTENT_ID:
                _reply(self, 403, {"error": {"code": "pilot_scope_required"}})
                return
            if action not in {"translate", "meaning"}:
                _reply(self, 400, {"error": {"code": "invalid_action"}})
                return
            if not text or len(text) > MAX_INPUT_CHARS:
                _reply(self, 400, {"error": {"code": "invalid_text"}})
                return
            if target not in LANGUAGES:
                _reply(self, 400, {"error": {"code": "unsupported_language"}})
                return

            user_id = _require_user(self)
            retry_after = _rate_limit(user_id)
            if retry_after is not None:
                self.send_response(429)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Retry-After", str(retry_after))
                self.end_headers()
                self.wfile.write(json.dumps({"error": {"code": "rate_limited"}}, separators=(",", ":")).encode("utf-8"))
                return

            result = _generate(self, action, text, target)
            _reply(self, 200, {"data": {"action": action, "language": target, "text": result}})
        except HTTPError as exc:
            exc.read()
            if exc.code in {401, 403}:
                _reply(self, 503, {"error": {"code": "ai_gateway_auth", "message": "AI Gateway authentication/authorization failed"}})
            elif exc.code == 404:
                _reply(self, 503, {"error": {"code": "ai_gateway_model", "message": "Configured AI Gateway model is unavailable"}})
            else:
                _reply(self, 502, {"error": {"code": "ai_gateway_error", "message": "AI Gateway request failed", "gateway_status": exc.code}})
        except (URLError, TimeoutError):
            _reply(self, 504, {"error": {"code": "ai_gateway_timeout"}})
        except PermissionError as exc:
            _reply(self, 401, {"error": {"code": str(exc)}})
        except RuntimeError as exc:
            _reply(self, 503, {"error": {"code": "ai_unavailable", "message": str(exc)}})
        except (ValueError, TypeError, json.JSONDecodeError):
            _reply(self, 400, {"error": {"code": "invalid_request"}})
        except Exception:
            _reply(self, 500, {"error": {"code": "internal_error"}})
# Production AI Gateway credentials are supplied through Vercel environment variables.
