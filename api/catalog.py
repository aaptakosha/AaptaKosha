"""Vercel entrypoint for the public NCISM curriculum structure APIs."""
from __future__ import annotations

import json
import os
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aaptakosha_core.api import CatalogApi
from aaptakosha_core.curriculum_hierarchy_api import CurriculumHierarchyApi
from aaptakosha_core.curriculum_hierarchy_services import CurriculumHierarchyService
from aaptakosha_core.services import CatalogService
from aaptakosha_core.sqlite_repository import SQLiteCatalogRepository

DB_PATH = Path("/tmp") / "aaptakosha-catalog.sqlite3"
CONNECTION = sqlite3.connect(str(DB_PATH), check_same_thread=False)

REPO = SQLiteCatalogRepository(CONNECTION)
REPO.apply_migrations(ROOT / "migrations" / "001_catalog.sql")
REPO.apply_migrations(ROOT / "migrations" / "004_bams_content_layout.sql")
REPO.apply_migrations(ROOT / "migrations" / "005_curriculum_hierarchy.sql")
REPO.apply_migrations(ROOT / "migrations" / "006_first_professional_hierarchy.sql")
REPO.apply_migrations(ROOT / "migrations" / "007_first_professional_data_quality.sql")
REPO.apply_migrations(ROOT / "migrations" / "008_third_professional_paper_layout.sql")
REPO.apply_migrations(ROOT / "migrations" / "009_second_professional_paper_layout.sql")
REPO.apply_migrations(ROOT / "migrations" / "010_first_professional_paper_layout.sql")
REPO.apply_migrations(ROOT / "migrations" / "011_first_professional_padartha_paper2.sql")
REPO.apply_migrations(ROOT / "migrations" / "012_first_professional_rachana_paper2.sql")
REPO.apply_migrations(ROOT / "migrations" / "013_first_professional_kriya_paper2.sql")
REPO.apply_migrations(ROOT / "migrations" / "014_correct_kriya_paper2_partb.sql")
REPO.apply_migrations(ROOT / "migrations" / "015_first_professional_padartha_samhita_layout.sql")
REPO.apply_migrations(ROOT / "migrations" / "016_first_professional_sanskrit_history_paper2.sql")
        "017_second_professional_samhita_layout.sql",
        "018_second_professional_agada_paper1.sql",

CATALOG_API = CatalogApi(CatalogService(REPO))
HIERARCHY_API = CurriculumHierarchyApi(CurriculumHierarchyService(REPO))


class handler(BaseHTTPRequestHandler):
    def _reply(self, status: int, payload: dict) -> None:
        data = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        origin = os.environ.get("AAPTOKOSHA_ALLOWED_ORIGIN", "").strip()
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        origin = os.environ.get("AAPTOKOSHA_ALLOWED_ORIGIN", "").strip()
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        query = {key: values[-1] for key, values in parse_qs(parsed.query).items()}
        path = parsed.path
        if path.startswith("/api"):
            path = path[4:] or "/"

        if path.startswith("/catalog/"):
            parts = [part for part in path.strip("/").split("/") if part]
            if len(parts) == 2:
                result = CATALOG_API.get_curriculum(parts[1], query.get("version"))
            elif len(parts) == 3 and parts[2] == "subjects":
                result = CATALOG_API.list_subjects(parts[1], query.get("version"))
            elif len(parts) == 4 and parts[2] == "subjects":
                result = CATALOG_API.get_subject(parts[1], parts[3], query.get("version"))
            else:
                result = {"status": 404, "error": {"code": "route_not_found"}}
        elif path == "/curriculum/nodes":
            curriculum_id = query.get("curriculum_id")
            if not curriculum_id:
                result = {"status": 400, "error": {"code": "invalid_request", "message": "curriculum_id is required"}}
            else:
                result = HIERARCHY_API.list_nodes(
                    curriculum_id,
                    query.get("subject_id"),
                    query.get("version"),
                    query.get("parent_node_id"),
                )
        elif path.startswith("/curriculum/nodes/"):
            node_id = path.rsplit("/", 1)[-1]
            result = HIERARCHY_API.get_node(
                node_id, query.get("curriculum_id"), query.get("version")
            )
        else:
            result = {"status": 404, "error": {"code": "route_not_found"}}

        self._reply(result["status"], result)


    def do_POST(self):
        self._reply(405, {"error": {"code": "method_not_allowed"}})
