"""Framework-neutral API boundary for knowledge content."""
from __future__ import annotations
from typing import Any
from .content_services import ContentNotFoundError, ContentService, ContentTransitionError
from .content_links import CurriculumContentLinkService

def _payload(resource: Any) -> dict[str, Any]:
    return {
        "resource_id": resource.resource_id,
        "resource_type": resource.resource_type,
        "title": resource.title,
        "summary": resource.summary,
        "status": resource.status,
        "provenance": [{"source": p.source, "locator": p.locator, "attribution": p.attribution} for p in resource.provenance],
        "curriculum_refs": list(resource.curriculum_refs),
    }

class ContentApi:
    def __init__(self, service: ContentService, links: CurriculumContentLinkService | None = None):
        self.service, self.links = service, links
    def get(self, resource_id: str) -> dict[str, Any]:
        try: return {"status": 200, "data": _payload(self.service.get(resource_id))}
        except ContentNotFoundError as exc: return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}
    def list(self, status: str | None = None) -> dict[str, Any]:
        return {"status": 200, "data": {"resources": [_payload(r) for r in self.service.list(status)]}}
    def publish(self, resource_id: str) -> dict[str, Any]:
        try: return {"status": 200, "data": _payload(self.service.publish(resource_id))}
        except ContentNotFoundError as exc: return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}
        except ContentTransitionError as exc: return {"status": 409, "error": {"code": "invalid_transition", "message": str(exc)}}
    def links_for_curriculum(self, curriculum_ref: str) -> dict[str, Any]:
        if self.links is None: return {"status": 501, "error": {"code": "linking_unavailable", "message": "content linking is not configured"}}
        return {"status": 200, "data": {"links": [vars(x) for x in self.links.for_curriculum(curriculum_ref)]}}

__all__=["ContentApi"]
