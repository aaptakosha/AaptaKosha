"""Framework-neutral HTTP routing adapter for learner assessment workflows."""

from __future__ import annotations
import json
from typing import Any, Callable
from .assessment import AssessmentAttempt, IN_PROGRESS
from .assessment_learning_api import AssessmentLearningApi

class AssessmentHttpApi:
    """Translate HTTP-like method/path/body inputs to AssessmentLearningApi."""

    def __init__(self, api: AssessmentLearningApi):
        self.api = api

    def handle(self, method: str, path: str, body: dict[str, Any] | None = None, query: dict[str, str] | None = None) -> dict[str, Any]:
        body, query = body or {}, query or {}
        parts = [p for p in path.strip("/").split("/") if p]
        if parts[:1] == ["assessments"] and len(parts) == 1 and method == "GET":
            return self.api.list_assessments(query.get("curriculum_ref"))
        if len(parts) == 3 and parts[0] == "assessments" and parts[2] == "attempts" and method == "POST":
            return self.api.start(parts[1], str(body["learner_id"]))
        if len(parts) == 3 and parts[0] == "attempts" and parts[2] == "answers" and method in {"PUT", "POST"}:
            answers = tuple((str(x["question_id"]), tuple(str(v) for v in x.get("selected_option_ids", []))) for x in body.get("answers", []))
            return self.api.save_answers(parts[1], str(body["learner_id"]), answers)
        if len(parts) == 3 and parts[0] == "attempts" and parts[2] == "submit" and method == "POST":
            return self.api.submit(parts[1], str(body["learner_id"]))
        if len(parts) == 2 and parts[0] == "attempts" and method == "GET":
            return self.api.result(parts[1], str(query["learner_id"]))
        return {"status": 404, "error": {"code": "route_not_found", "message": f"{method} {path}"}}

    @staticmethod
    def json_response(result: dict[str, Any]) -> tuple[int, str]:
        return result["status"], json.dumps(result, separators=(",", ":"), sort_keys=True)

__all__ = ["AssessmentHttpApi"]
