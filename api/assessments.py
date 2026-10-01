"""Vercel Python entrypoint for the learner assessment API."""
from __future__ import annotations

import json
import os
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from aaptakosha_core.assessment import Assessment, AssessmentQuestion, QuestionOption
from aaptakosha_core.assessment_http_api import AssessmentHttpApi
from aaptakosha_core.assessment_learning_api import AssessmentLearningApi
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository
from aaptakosha_core.assessment_services import AssessmentService
from aaptakosha_core.clerk_identity import build_identity_provider
from aaptakosha_core.postgres_repository import PostgresAssessmentRepository, PostgresProgressRepository
from aaptakosha_core.progress import LearningProgressService
from aaptakosha_core.progress_http_api import ProgressHttpApi
from aaptakosha_core.progress_repository import SQLiteProgressRepository

DB_PATH = os.path.join("/tmp", "aaptakosha-assessment.sqlite3")
CONTENT_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "samhita")

def _load_samhita(content_id: str):
    if not content_id.startswith("charaka.sutra."):
        return None
    try:
        chapter_no = int(content_id.rsplit(".", 1)[-1])
    except ValueError:
        return None
    if chapter_no not in {1, 2, 3}:
        return None
    path = os.path.join(CONTENT_ROOT, "charaka", "sutrasthana", f"adhyaya-{chapter_no:02d}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)
DATABASE_BACKEND = "sqlite"
DATABASE_CONNECTION = None
IDENTITY_PROVIDER = build_identity_provider()
REQUIRE_IDENTITY = bool(os.environ.get("VERCEL")) or os.environ.get("AAPTOKOSHA_REQUIRE_IDENTITY", "").strip().lower() in {"1", "true", "yes"}


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

def _seed_samhita_ncism_assessment(service: AssessmentService, repo) -> None:
    assessment_id = "charaka.sutra.01.ncism-revision"
    if repo.get(assessment_id) is not None:
        return
    path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "content", "assessments", "charaka-sutra-01-ncism.json",
    )
    with open(path, encoding="utf-8") as fh:
        payload = json.load(fh)
    questions = []
    for item in payload["questions"]:
        questions.append(AssessmentQuestion(
            item["question_id"],
            item["prompt"],
            tuple(
                QuestionOption(
                    option["option_id"],
                    option["text"],
                    option["is_correct"],
                )
                for option in item["options"]
            ),
            points=item["points"],
            content_refs=tuple(item["content_refs"]),
        ))
    assessment = Assessment(
        assessment_id,
        payload["title_hi"],
        curriculum_refs=tuple(payload["curriculum_refs"]),
        questions=tuple(questions),
    )
    service.create(assessment)
    service.publish(assessment_id)



def _seed_samhita_chapter2_assessment(service: AssessmentService, repo) -> None:
    assessment_id = "charaka.sutra.02.revision"
    if repo.get(assessment_id) is not None:
        return
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "assessments", "charaka-sutra-02-revision.json")
    with open(path, encoding="utf-8") as fh:
        payload = json.load(fh)
    questions = [
        AssessmentQuestion(
            item["question_id"], item["prompt"],
            tuple(QuestionOption(o["option_id"], o["text"], o["is_correct"]) for o in item["options"]),
            points=item["points"], content_refs=tuple(item["content_refs"]),
        )
        for item in payload["questions"]
    ]
    assessment = Assessment(assessment_id, payload["title_hi"], curriculum_refs=tuple(payload["curriculum_refs"]), questions=tuple(questions))
    service.create(assessment)
    service.publish(assessment_id)

def _seed_samhita_chapter3_assessment(service: AssessmentService, repo) -> None:
    assessment_id = "charaka.sutra.03.revision"
    if repo.get(assessment_id) is not None:
        return
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "assessments", "charaka-sutra-03-revision.json")
    with open(path, encoding="utf-8") as fh:
        payload = json.load(fh)
    questions = [
        AssessmentQuestion(
            item["question_id"], item["prompt"],
            tuple(QuestionOption(o["option_id"], o["text"], o["is_correct"]) for o in item["options"]),
            points=item["points"], content_refs=tuple(item["content_refs"]),
        )
        for item in payload["questions"]
    ]
    assessment = Assessment(assessment_id, payload["title_hi"], curriculum_refs=tuple(payload["curriculum_refs"]), questions=tuple(questions))
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
    _seed_samhita_ncism_assessment(service, repo)
    _seed_samhita_chapter2_assessment(service, repo)
    _seed_samhita_chapter3_assessment(service, repo)
    return (
        AssessmentHttpApi(AssessmentLearningApi(service), require_identity=REQUIRE_IDENTITY),
        ProgressHttpApi(LearningProgressService(progress_repo), require_identity=REQUIRE_IDENTITY),
    )


API, PROGRESS_API = build_api()


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
                "identity_provider": "clerk" if IDENTITY_PROVIDER is not None else "unconfigured",
            }))
            return

        if self.command == "GET" and path == "/health":
            try:
                cursor = DATABASE_CONNECTION.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.execute("SELECT COUNT(*) FROM assessments")
                assessment_count = cursor.fetchone()[0]
                configured = IDENTITY_PROVIDER is not None
                healthy = (not REQUIRE_IDENTITY) or configured
                self._reply(200 if healthy else 503, json.dumps({
                    "status": "ok" if healthy else "degraded",
                    "database": DATABASE_BACKEND,
                    "assessment_count": assessment_count,
                    "identity_provider": "clerk" if configured else "unconfigured",
                    "identity_required": REQUIRE_IDENTITY,
                    "ready": healthy,
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

        principal = None
        if IDENTITY_PROVIDER is not None:
            try:
                principal = IDENTITY_PROVIDER.resolve(self)
            except Exception:
                self._reply(401, json.dumps({"error": {"code": "authentication_failed"}}))
                return
        if REQUIRE_IDENTITY and IDENTITY_PROVIDER is None:
            self._reply(503, json.dumps({"error": {"code": "identity_provider_not_configured"}}))
            return

        try:
            if path == "/progress" or path.startswith("/progress/"):
                result = PROGRESS_API.handle(self.command, path, body, query, principal=principal)
            else:
                result = API.handle(self.command, path, body, query, principal=principal)
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
