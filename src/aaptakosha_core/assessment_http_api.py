"""Framework-neutral HTTP routing adapter for learner assessment workflows."""

from __future__ import annotations
import json
from typing import Any, Callable
from .assessment import AssessmentAttempt, IN_PROGRESS
from .assessment_learning_api import AssessmentLearningApi
from .auth import AuthorizationDeniedError, Principal

class AssessmentHttpApi:
    """Translate HTTP-like method/path/body inputs to AssessmentLearningApi."""

    def __init__(self, api: AssessmentLearningApi, *, require_identity: bool = False):
        self.api = api
        self.require_identity = require_identity

    def handle(self, method: str, path: str, body: dict[str, Any] | None = None, query: dict[str, str] | None = None, *, principal: Principal | None = None) -> dict[str, Any]:
        body, query = body or {}, query or {}
        if self.require_identity and principal is None:
            return {"status": 401, "error": {"code": "authentication_required"}}
        learner_id = str(principal.subject_id) if principal is not None else None
        if learner_id is not None and "learner_id" in body and str(body["learner_id"]) != learner_id:
            return {"status": 403, "error": {"code": "learner_identity_mismatch"}}
        if learner_id is not None and "learner_id" in query and str(query["learner_id"]) != learner_id:
            return {"status": 403, "error": {"code": "learner_identity_mismatch"}}
        parts = [p for p in path.strip("/").split("/") if p]
        if parts == ["analytics"] and method == "GET":
            return self.api.learner_analytics(learner_id or str(query["learner_id"]))
        if parts[:1] == ["assessments"] and len(parts) == 1 and method == "GET":
            return self.api.list_assessments(query.get("curriculum_ref"))
        if len(parts) == 3 and parts[0] == "assessments" and parts[2] == "attempts" and method == "POST":
            return self.api.start(parts[1], learner_id or str(body["learner_id"]))
        if len(parts) == 3 and parts[0] == "attempts" and parts[2] == "answers" and method in {"PUT", "POST"}:
            answers = tuple((str(x["question_id"]), tuple(str(v) for v in x.get("selected_option_ids", []))) for x in body.get("answers", []))
            return self.api.save_answers(parts[1], learner_id or str(body["learner_id"]), answers)
        if len(parts) == 3 and parts[0] == "attempts" and parts[2] == "submit" and method == "POST":
            return self.api.submit(parts[1], learner_id or str(body["learner_id"]))
        if len(parts) == 2 and parts[0] == "attempts" and method == "GET":
            return self.api.result(parts[1], learner_id or str(query["learner_id"]))
        return {"status": 404, "error": {"code": "route_not_found", "message": f"{method} {path}"}}

    @staticmethod
    def json_response(result: dict[str, Any]) -> tuple[int, str]:
        return result["status"], json.dumps(result, separators=(",", ":"), sort_keys=True)

__all__ = ["AssessmentHttpApi"]
