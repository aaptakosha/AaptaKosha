"""Framework-neutral HTTP adapter for learner progress workflows."""

from __future__ import annotations

import json
from typing import Any

from .auth import Principal
from .progress import LearningProgressService


class ProgressHttpApi:
    """Translate HTTP-like requests into progress service operations."""

    def __init__(self, service: LearningProgressService, *, require_identity: bool = False):
        self.service = service
        self.require_identity = require_identity

    def handle(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
        query: dict[str, str] | None = None,
        *,
        principal: Principal | None = None,
    ) -> dict[str, Any]:
        body, query = body or {}, query or {}
        parts = [p for p in path.strip("/").split("/") if p]
        if self.require_identity and principal is None:
            return {"status": 401, "error": {"code": "authentication_required"}}
        subject_id = str(principal.subject_id) if principal is not None else None
        path_subject = parts[1] if len(parts) == 4 and parts[0] == "progress" else ""
        supplied_subject = str(body.get("subject_id", query.get("subject_id", path_subject))).strip()
        if subject_id is not None and supplied_subject and supplied_subject != subject_id:
            return {"status": 403, "error": {"code": "learner_identity_mismatch"}}
        if subject_id is not None:
            if method == "GET" and parts == ["progress"]:
                query = {**query, "subject_id": subject_id}
            elif method in {"POST", "PUT"}:
                body = {**body, "subject_id": subject_id}

        if parts == ["progress"] and method == "GET":
            subject_id = str(query.get("subject_id", "")).strip()
            if not subject_id:
                return {"status": 400, "error": {"code": "subject_id_required"}}
            return self._list(subject_id)

        if parts == ["progress"] and method in {"POST", "PUT"}:
            try:
                progress = self.service.record(
                    str(body["subject_id"]), str(body["resource_type"]), str(body["resource_id"]),
                    status=str(body["status"]), completion_percent=int(body["completion_percent"]),
                )
            except (KeyError, TypeError, ValueError):
                return {"status": 400, "error": {"code": "invalid_progress"}}
            return {"status": 200, "progress": self._serialize(progress)}

        if len(parts) == 4 and parts[0] == "progress" and method == "GET":
            progress = self.service.get(parts[1], parts[2], parts[3])
            if progress is None:
                return {"status": 404, "error": {"code": "progress_not_found"}}
            return {"status": 200, "progress": self._serialize(progress)}

        return {"status": 404, "error": {"code": "route_not_found", "message": f"{method} {path}"}}

    def _list(self, subject_id: str) -> dict[str, Any]:
        return {"status": 200, "progress": [self._serialize(item) for item in self.service.list_for_subject(subject_id)]}

    @staticmethod
    def _serialize(progress) -> dict[str, Any]:
        return {
            "subject_id": progress.subject_id,
            "resource_type": progress.resource_type,
            "resource_id": progress.resource_id,
            "status": progress.status,
            "completion_percent": progress.completion_percent,
        }

    @staticmethod
    def json_response(result: dict[str, Any]) -> tuple[int, str]:
        return result["status"], json.dumps(result, separators=(",", ":"), sort_keys=True)


__all__ = ["ProgressHttpApi"]
