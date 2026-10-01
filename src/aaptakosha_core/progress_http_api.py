"""Framework-neutral HTTP adapter for learner progress workflows."""

from __future__ import annotations

import json
from typing import Any

from .progress import LearningProgressService


class ProgressHttpApi:
    """Translate HTTP-like requests into progress service operations."""

    def __init__(self, service: LearningProgressService):
        self.service = service

    def handle(self, method: str, path: str, body: dict[str, Any] | None = None, query: dict[str, str] | None = None) -> dict[str, Any]:
        body, query = body or {}, query or {}
        parts = [p for p in path.strip("/").split("/") if p]

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
