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
from aaptakosha_core.postgres_repository import PostgresAssessmentRepository

DB_PATH = os.path.join("/tmp", "aaptakosha-assessment.sqlite3")


def _seed_demo(service: AssessmentService, repo) -> None:
    if repo.get("demo-dravyaguna-3") is not None:
        return
    service.create(
        Assessment(
            "demo-dravyaguna-3",
            "Dravyaguna · Chapter 3 Assessment",
            curriculum_refs=("subject:dravyaguna",),
            questions=(
                AssessmentQuestion(
                    "q1",
                    "Which principle is most useful for organising related dravyas during study?",
                    (
                        QuestionOption("a", "Memorising each dravya as an isolated fact"),
                        QuestionOption(
                            "b",
                            "Connecting source, properties, action and use",
                            is_correct=True,
                        ),
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
        )
    )
    service.publish("demo-dravyaguna-3")


def build_api():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        import psycopg

        conn = psycopg.connect(database_url)
        repo = PostgresAssessmentRepository(conn)
    else:
        conn = sqlite3.connect(DB_PATH)
        repo = SQLiteAssessmentRepository(conn)

    repo.apply_migrations()
    service = AssessmentService(repo, repo)
    _seed_demo(service, repo)
    return AssessmentHttpApi(AssessmentLearningApi(service))


API = build_api()


class handler(BaseHTTPRequestHandler):
    def _reply(self, status, payload):
        data = payload.encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
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

        body = None
        length = int(self.headers.get("Content-Length", "0"))
        if length:
            try:
                body = json.loads(self.rfile.read(length))
            except (json.JSONDecodeError, UnicodeDecodeError):
                self._reply(400, json.dumps({"error": {"code": "invalid_json"}}))
                return

        result = API.handle(self.command, path, body, query)
        self._reply(*API.json_response(result))

    def do_GET(self):
        self._handle()

    def do_POST(self):
        self._handle()

    def do_PUT(self):
        self._handle()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
