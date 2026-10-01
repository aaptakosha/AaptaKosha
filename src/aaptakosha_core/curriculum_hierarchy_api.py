"""Framework-neutral API adapter for curriculum hierarchy navigation."""
from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .curriculum_hierarchy_services import (
    CurriculumHierarchyNotFoundError,
    CurriculumHierarchyService,
)


def _node_payload(node: Any) -> dict[str, Any]:
    return asdict(node)


class CurriculumHierarchyApi:
    """Transport-neutral handlers for NCISM curriculum tree endpoints."""

    def __init__(self, service: CurriculumHierarchyService):
        self.service = service

    def list_nodes(
        self,
        curriculum_id: str,
        subject_id: str | None = None,
        version: str | None = None,
        parent_node_id: str | None = None,
    ) -> dict[str, Any]:
        try:
            nodes = self.service.list_nodes(
                curriculum_id, subject_id, version, parent_node_id
            )
            return {"status": 200, "data": {"nodes": [_node_payload(node) for node in nodes]}}
        except CurriculumHierarchyNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}

    def get_node(
        self,
        node_id: str,
        curriculum_id: str | None = None,
        version: str | None = None,
    ) -> dict[str, Any]:
        try:
            return {"status": 200, "data": _node_payload(
                self.service.get_node(node_id, curriculum_id, version)
            )}
        except CurriculumHierarchyNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}


__all__ = ["CurriculumHierarchyApi"]
