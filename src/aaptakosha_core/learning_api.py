"""Learner-facing composition API for the Phase 5 Learn/Study screens.

This adapter composes existing catalog and published-content services. It does
not introduce a second curriculum model or bypass publication governance.
"""
from __future__ import annotations
from typing import Any
from .services import CatalogService
from .content_services import ContentService
from .content_links import CurriculumContentLinkService

class LearningCatalogApi:
    def __init__(self, catalog: CatalogService, content: ContentService, links: CurriculumContentLinkService | None = None):
        self.catalog, self.content, self.links = catalog, content, links

    def subjects(self, curriculum_id: str, version: str | None = None) -> dict[str, Any]:
        curriculum = self.catalog.get_curriculum(curriculum_id, version)
        return {"status": 200, "data": {"curriculum_id": curriculum.curriculum_id, "version": curriculum.version,
            "professional_year": curriculum.professional_year,
            "subjects": [{"subject_id": s.subject_id, "name": s.name,
                          "topics": [{"topic_id": t.topic_id, "name": t.name} for t in s.topics]}
                         for s in curriculum.subjects]}}

    def subject(self, curriculum_id: str, subject_id: str, version: str | None = None) -> dict[str, Any]:
        subject = self.catalog.get_subject(curriculum_id, subject_id, version)
        data = {"subject_id": subject.subject_id, "name": subject.name,
                "topics": [{"topic_id": t.topic_id, "name": t.name} for t in subject.topics]}
        return {"status": 200, "data": data}

    def published_content(self, curriculum_ref: str) -> dict[str, Any]:
        if self.links is None:
            return {"status": 501, "error": {"code": "linking_unavailable", "message": "content linking is not configured"}}
        resources = []
        for link in self.links.for_curriculum(curriculum_ref):
            resource = self.content.get(link.resource_id)
            if resource.status == "published":
                resources.append({"resource_id": resource.resource_id, "resource_type": resource.resource_type,
                                  "title": resource.title, "summary": resource.summary,
                                  "relationship": link.relationship})
        return {"status": 200, "data": {"resources": resources}}

__all__ = ["LearningCatalogApi"]
