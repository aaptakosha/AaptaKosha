"""Vercel Python entrypoint for the learner assessment API."""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
import urllib.request
from urllib.error import HTTPError, URLError
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from aaptakosha_core.assessment import Assessment, AssessmentQuestion, QuestionOption
from aaptakosha_core.assessment_http_api import AssessmentHttpApi
from aaptakosha_core.assessment_learning_api import AssessmentLearningApi
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository
from aaptakosha_core.assessment_services import AssessmentService
from aaptakosha_core.clerk_identity import ClerkConfigurationError, build_identity_provider
from aaptakosha_core.postgres_repository import PostgresAssessmentRepository, PostgresProgressRepository
from aaptakosha_core.progress import LearningProgressService
from aaptakosha_core.progress_http_api import ProgressHttpApi
from aaptakosha_core.progress_repository import SQLiteProgressRepository

DB_PATH = os.path.join("/tmp", "aaptakosha-assessment.sqlite3")
CONTENT_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "samhita")

def _load_samhita(content_id: str):
    if content_id.startswith("charaka.sutra."):
        family = "charaka"
    elif content_id.startswith("ashtanga.hridaya.sutra."):
        family = "ashtanga_hridaya"
    else:
        return None
    try:
        chapter_no = int(content_id.rsplit(".", 1)[-1])
    except ValueError:
        return None
    if family == "charaka":
        if chapter_no not in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}:
            return None
        path = os.path.join(CONTENT_ROOT, "charaka", "sutrasthana", f"adhyaya-{chapter_no:02d}.json")
    else:
        if chapter_no not in {1, 2, 3}:
            return None
        path = os.path.join(CONTENT_ROOT, "ashtanga_hridaya", "sutrasthana", f"adhyaya-{chapter_no:02d}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)
DATABASE_BACKEND = "sqlite"
DATABASE_CONNECTION = None
API = None
PROGRESS_API = None
IDENTITY_PROVIDER = None
IDENTITY_ERROR = None

REQUIRE_IDENTITY = bool(os.environ.get("VERCEL")) or os.environ.get("AAPTOKOSHA_REQUIRE_IDENTITY", "").strip().lower() in {"1", "true", "yes"}

AI_GATEWAY = "https://ai-gateway.vercel.sh/v1/chat/completions"
AI_MODEL = "google/gemini-3.1-flash-lite"
AI_CONTENT_PREFIX = "ashtanga.hridaya."
AI_MAX_INPUT_CHARS = 6000
AI_RATE_LIMIT_MAX = 10
AI_RATE_LIMIT_WINDOW_SECONDS = 600
AI_RATE_LIMIT: dict[str, list[float]] = {}
AI_LANGUAGES = {
    "hi": "Hindi", "en": "English", "mr": "Marathi", "ta": "Tamil",
    "te": "Telugu", "kn": "Kannada", "ml": "Malayalam", "bo": "Tibetan",
}


def _gateway_tokens() -> list[str]:
    values = [
        os.environ.get("VERCEL_OIDC_TOKEN", "").strip(),
        os.environ.get("VERCEL_AI_GATEWAY_KEY", "").strip(),
        os.environ.get("AI_GATEWAY_API_KEY", "").strip(),
    ]
    return list(dict.fromkeys(value for value in values if value))


def _generate_samhita_ai(action: str, text: str, target: str, source_kind: str) -> str:
    language = AI_LANGUAGES[target]
    if action == "translate":
        if source_kind == "Tika":
            system = (
                "You are a careful translator of classical Sanskrit Ayurveda tika/commentary. "
                "Translate the supplied commentary faithfully into the requested language. "
                "Preserve technical Ayurvedic terms when a precise equivalent is uncertain, "
                "do not invent commentary, and return only the translation."
            )
        else:
            system = (
                "You are a careful classical Sanskrit translator for an Ayurveda education site. "
                "Translate the supplied Sanskrit faithfully into the requested language. "
                "Preserve technical Ayurvedic terms when a precise equivalent is uncertain, "
                "do not invent commentary, and return only the translation."
            )
        prompt = f"Translate this Sanskrit Ayurveda passage into {language}:\\n\\n{text}"
    else:
        system = (
            "You are an Ayurveda education assistant. Give a short, student-friendly meaning "
            "of the supplied Sanskrit verse in the requested language. Stay grounded in the "
            "verse, do not add medical advice, and return only the meaning."
        )
        prompt = f"Give the simple meaning of this Sanskrit Ayurveda verse in {language}:\\n\\n{text}"

    tokens = _gateway_tokens()
    if not tokens:
        raise RuntimeError("AI Gateway authentication is not configured")

    body = json.dumps({
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 700 if action == "meaning" else 500,
        "stream": False,
    }, ensure_ascii=False).encode("utf-8")

    last_auth_error = None
    for token in tokens:
        req = urllib.request.Request(
            AI_GATEWAY,
            data=body,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=25) as response:
                payload = json.loads(response.read().decode("utf-8"))
            result = payload.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not isinstance(result, str) or not result.strip():
                raise RuntimeError("AI Gateway returned no text")
            return result.strip()
        except HTTPError as exc:
            if exc.code in {401, 403} and token != tokens[-1]:
                exc.read()
                last_auth_error = exc
                continue
            raise
    if last_auth_error is not None:
        raise last_auth_error
    raise RuntimeError("AI Gateway request failed")


def _handle_samhita_ai(handler, body, principal):
    if principal is None:
        handler._reply(401, json.dumps({"error": {"code": "authentication_invalid"}}))
        return

    action = str(body.get("action", "")).strip()
    text = str(body.get("text", "")).strip()
    target = str(body.get("target", "hi")).strip()
    content_id = str(body.get("content_id", "")).strip()
    source_kind = str(body.get("source_kind", "Sanskrit verse")).strip() or "Sanskrit verse"

    if not content_id.startswith(AI_CONTENT_PREFIX):
        handler._reply(403, json.dumps({"error": {"code": "ashtanga_scope_required"}}))
        return
    if action not in {"translate", "meaning"}:
        handler._reply(400, json.dumps({"error": {"code": "invalid_action"}}))
        return
    if not text or len(text) > AI_MAX_INPUT_CHARS:
        handler._reply(400, json.dumps({"error": {"code": "invalid_text"}}))
        return
    if target not in AI_LANGUAGES:
        handler._reply(400, json.dumps({"error": {"code": "unsupported_language"}}))
        return

    now = time.time()
    recent = [t for t in AI_RATE_LIMIT.get(principal.subject_id, []) if now - t < AI_RATE_LIMIT_WINDOW_SECONDS]
    if len(recent) >= AI_RATE_LIMIT_MAX:
        retry_after = max(1, int(AI_RATE_LIMIT_WINDOW_SECONDS - (now - recent[0])))
        AI_RATE_LIMIT[principal.subject_id] = recent
        handler.send_response(429)
        handler.send_header("Content-Type", "application/json; charset=utf-8")
        handler.send_header("Retry-After", str(retry_after))
        handler.end_headers()
        handler.wfile.write(json.dumps({"error": {"code": "rate_limited"}}, separators=(",", ":")).encode("utf-8"))
        return
    recent.append(now)
    AI_RATE_LIMIT[principal.subject_id] = recent

    try:
        result = _generate_samhita_ai(action, text, target, source_kind)
        handler._reply(200, json.dumps({"data": {"action": action, "language": target, "text": result}}, ensure_ascii=False))
    except HTTPError as exc:
        gateway_body = exc.read().decode("utf-8", "replace")[:1000]
        if exc.code in {401, 403}:
            handler._reply(503, json.dumps({"error": {
                "code": "ai_gateway_auth",
                "message": "AI Gateway authentication/authorization failed",
                "gateway_status": exc.code,
                "gateway_detail": gateway_body,
            }, "ensure_ascii": False}))
        elif exc.code == 404:
            handler._reply(503, json.dumps({"error": {"code": "ai_gateway_model", "message": "Configured AI Gateway model is unavailable"}}))
        else:
            handler._reply(502, json.dumps({"error": {"code": "ai_gateway_error", "gateway_status": exc.code}}))
    except (URLError, TimeoutError):
        handler._reply(504, json.dumps({"error": {"code": "ai_gateway_timeout"}}))
    except RuntimeError as exc:
        handler._reply(503, json.dumps({"error": {"code": "ai_unavailable", "message": str(exc)}}))
    except Exception:
        handler._reply(500, json.dumps({"error": {"code": "internal_error"}}))



def _seed_demo(service: AssessmentService, repo) -> None:
    if repo.get("demo-dravyaguna-3") is not None:
        return
    service.create(Assessment(
        "demo-dravyaguna-3",
        "Dravyaguna · Chapter 3 Assessment",
        curriculum_refs=("subject:dravyaguna",),
        questions=(
            AssessmentQuestion(
                "q1",
                "Which principle is most useful for organising related dravyas during study?",
                (
                    QuestionOption("a", "Memorising each dravya as an isolated fact"),
                    QuestionOption("b", "Connecting source, properties, action and use", is_correct=True),
                    QuestionOption("c", "Studying only the common names"),
                    QuestionOption("d", "Grouping topics only by page number"),
                ),
            ),
            AssessmentQuestion(
                "q2",
                "Which relationship best supports therapeutic application?",
                (
                    QuestionOption("a", "Properties → action → use", is_correct=True),
                    QuestionOption("b", "Page → chapter → book"),
                    QuestionOption("c", "Name → spelling → page"),
                    QuestionOption("d", "Source → index → appendix"),
                ),
            ),
        ),
    ))
    service.publish("demo-dravyaguna-3")

def _seed_samhita_assessments(service: AssessmentService, repo) -> None:
    """Load canonical Charaka and Ashtanga Hridaya assessment definitions from content files."""
    root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "assessments")
    for filename in sorted(os.listdir(root)):
        if not filename.endswith(".json"):
            continue
        if filename.startswith("charaka-sutra-"):
            family = "charaka"
        elif filename.startswith("ashtanga-hridaya-sutra-"):
            family = "ashtanga_hridaya"
        else:
            continue
        path = os.path.join(root, filename)
        with open(path, encoding="utf-8") as fh:
            payload = json.load(fh)
        stem = filename[:-5]
        chapter_token = stem.split("-")[-2]
        try:
            chapter_no = int(chapter_token)
        except ValueError:
            continue
        suffix = "ncism-revision" if family == "charaka" and chapter_no == 1 else "revision"
        prefix = "charaka.sutra" if family == "charaka" else "ashtanga.hridaya.sutra"
        assessment_id = f"{prefix}.{chapter_no:02d}.{suffix}"
        if repo.get(assessment_id) is not None:
            continue
        questions = []
        for item in payload.get("questions", []):
            prompt = item.get("prompt") or item.get("prompt_hi") or item.get("question") or item.get("question_hi")
            options = []
            for option in item.get("options", []):
                option_id = option.get("option_id") or option.get("id")
                option_text = option.get("text") or option.get("text_hi") or option.get("label_hi")
                options.append(QuestionOption(option_id, option_text, bool(option.get("is_correct"))))
            questions.append(
                AssessmentQuestion(
                    item["question_id"],
                    prompt,
                    tuple(options),
                    points=int(item.get("points", 1)),
                    content_refs=tuple(item.get("content_refs", ())),
                )
            )
        assessment = Assessment(
            assessment_id,
            payload.get("title_hi") or payload.get("title") or assessment_id,
            curriculum_refs=tuple(payload.get("curriculum_refs", ())),
            questions=tuple(questions),
        )
        service.create(assessment)
        service.publish(assessment_id)


def build_api():
    global DATABASE_BACKEND, DATABASE_CONNECTION
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        import psycopg
        conn = psycopg.connect(database_url)
        DATABASE_BACKEND = "postgres"
        DATABASE_CONNECTION = conn
        repo = PostgresAssessmentRepository(conn)
    else:
        conn = sqlite3.connect(DB_PATH)
        DATABASE_BACKEND = "sqlite"
        DATABASE_CONNECTION = conn
        repo = SQLiteAssessmentRepository(conn)
    repo.apply_migrations()
    progress_repo = PostgresProgressRepository(conn) if database_url else SQLiteProgressRepository(conn)
    progress_repo.apply_migrations()
    progress_service = LearningProgressService(progress_repo)
    service = AssessmentService(repo, repo, progress_service)
    _seed_demo(service, repo)
    _seed_samhita_assessments(service, repo)
    return (
        AssessmentHttpApi(AssessmentLearningApi(service), require_identity=REQUIRE_IDENTITY),
        ProgressHttpApi(LearningProgressService(progress_repo), require_identity=REQUIRE_IDENTITY),
    )


def _get_apis():
    global API, PROGRESS_API
    if API is None or PROGRESS_API is None:
        API, PROGRESS_API = build_api()
    return API, PROGRESS_API


def _get_identity_provider():
    global IDENTITY_PROVIDER, IDENTITY_ERROR
    if IDENTITY_PROVIDER is not None or IDENTITY_ERROR is not None:
        return IDENTITY_PROVIDER
    try:
        IDENTITY_PROVIDER = build_identity_provider()
    except ClerkConfigurationError as exc:
        IDENTITY_ERROR = str(exc)
    return IDENTITY_PROVIDER


class handler(BaseHTTPRequestHandler):
    def _reply(self, status, payload):
        data = payload.encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        origin = os.environ.get("AAPTOKOSHA_ALLOWED_ORIGIN", "").strip()
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.end_headers()
        self.wfile.write(data)

    def _handle(self):
        parsed = urlparse(self.path)
        query = {k: v[-1] for k, v in parse_qs(parsed.query).items()}
        path = parsed.path
        if path.startswith("/api"):
            path = path[4:] or "/"
        route = query.pop("route", None)
        if route is not None:
            path = "/" + route.lstrip("/")

        if self.command == "OPTIONS":
            allowed_origin = os.environ.get("AAPTOKOSHA_ALLOWED_ORIGIN", "").strip()
            request_origin = self.headers.get("Origin", "").strip()
            if allowed_origin and request_origin and request_origin != allowed_origin:
                self._reply(403, json.dumps({"error": {"code": "cors_origin_not_allowed"}}))
                return
            self.send_response(204)
            self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
            if allowed_origin:
                self.send_header("Access-Control-Allow-Origin", allowed_origin)
                self.send_header("Vary", "Origin")
            self.end_headers()
            return

        if self.command == "GET" and path == "/content/samhita":
            chapter = _load_samhita(query.get("content_id", "").strip())
            if chapter is None: self._reply(404, json.dumps({"error": {"code": "content_not_found"}}))
            else: self._reply(200, json.dumps({"data": chapter}, ensure_ascii=False))
            return

        if self.command == "GET" and path == "/config":
            # The publishable key is safe to expose to the browser;
            # the Clerk secret key is never returned here.
            publishable_key = os.environ.get("CLERK_PUBLISHABLE_KEY", "").strip()
            self._reply(200, json.dumps({
                "clerk_publishable_key": publishable_key,
                "identity_provider": "clerk" if _get_identity_provider() is not None else "unconfigured",
                "identity_configuration_error": IDENTITY_ERROR,
            }))
            return

        if self.command == "GET" and path == "/health":
            try:
                _get_apis()
                identity_provider = _get_identity_provider()
                cursor = DATABASE_CONNECTION.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                configured = identity_provider is not None and IDENTITY_ERROR is None
                assessment_count = None
                healthy = (not REQUIRE_IDENTITY) and IDENTITY_ERROR is None or (REQUIRE_IDENTITY and configured)
                self._reply(200 if healthy else 503, json.dumps({
                    "status": "ok" if healthy else "degraded",
                    "database": DATABASE_BACKEND,
                    "assessment_count": assessment_count,
                    "identity_provider": "clerk" if configured else "unconfigured",
                    "identity_required": REQUIRE_IDENTITY,
                    "ready": healthy,
                    "identity_configuration_error": IDENTITY_ERROR,
                }))
            except Exception:
                self._reply(503, json.dumps({"status": "error", "code": "readiness_check_failed", "ready": False}))
            return

        body = None
        length = int(self.headers.get("Content-Length", "0"))
        if length:
            try:
                body = json.loads(self.rfile.read(length))
            except (json.JSONDecodeError, UnicodeDecodeError):
                self._reply(400, json.dumps({"error": {"code": "invalid_json"}}))
                return
            if not isinstance(body, dict):
                self._reply(400, json.dumps({"error": {"code": "invalid_request_body"}}))
                return

        identity_provider = _get_identity_provider()
        if IDENTITY_ERROR is not None:
            self._reply(503, json.dumps({"error": {"code": "identity_provider_misconfigured"}}))
            return
        principal = None
        if identity_provider is not None:
            try:
                principal = identity_provider.resolve(self)
            except Exception:
                self._reply(401, json.dumps({"error": {"code": "authentication_failed"}}))
                return
        if REQUIRE_IDENTITY and identity_provider is None:
            self._reply(503, json.dumps({"error": {"code": "identity_provider_not_configured"}}))
            return

        try:
            assessment_api, progress_api = _get_apis()
            if path == "/progress" or path.startswith("/progress/"):
                result = progress_api.handle(self.command, path, body, query, principal=principal)
            else:
                result = assessment_api.handle(self.command, path, body, query, principal=principal)
            response = PROGRESS_API.json_response(result) if path == "/progress" or path.startswith("/progress/") else API.json_response(result)
            self._reply(*response)
        except Exception:
            self._reply(500, json.dumps({"error": {"code": "internal_server_error"}}))


    def do_GET(self):
        self._handle()

    def do_POST(self):
        self._handle()

    def do_PUT(self):
        self._handle()

    def do_OPTIONS(self):
        self._handle()
