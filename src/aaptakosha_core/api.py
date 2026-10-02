"""Framework-neutral API boundary for the AaptaKosha catalog.

This module maps transport-level inputs to application use cases and returns
small serializable response objects. A web framework adapter can translate
these results into HTTP responses without coupling the domain layer to HTTP.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .services import CatalogNotFoundError, CatalogService


def _topic_payload(topic: Any) -> dict[str, str]:
    return asdict(topic)


def _subject_payload(subject: Any) -> dict[str, Any]:
    return {
        "subject_id": subject.subject_id,
        "name": subject.name,
        "topics": [_topic_payload(topic) for topic in subject.topics],
    }


def _curriculum_payload(curriculum: Any) -> dict[str, Any]:
    return {
        "curriculum_id": curriculum.curriculum_id,
        "version": curriculum.version,
        "professional_year": curriculum.professional_year,
        "subjects": [_subject_payload(subject) for subject in curriculum.subjects],
    }


class CatalogApi:
    """Transport-neutral catalog endpoint handlers."""

    def __init__(self, service: CatalogService):
        self.service = service

    def get_curriculum(self, curriculum_id: str, version: str | None = None) -> dict[str, Any]:
        try:
            return {
                "status": 200,
                "data": _curriculum_payload(
                    self.service.get_curriculum(curriculum_id, version)
                ),
            }
        except CatalogNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}

    def list_subjects(self, curriculum_id: str, version: str | None = None) -> dict[str, Any]:
        try:
            subjects = self.service.list_subjects(curriculum_id, version)
            return {
                "status": 200,
                "data": {"subjects": [_subject_payload(subject) for subject in subjects]},
            }
        except CatalogNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}

    def get_subject(
        self, curriculum_id: str, subject_id: str, version: str | None = None
    ) -> dict[str, Any]:
        try:
            return {
                "status": 200,
                "data": _subject_payload(
                    self.service.get_subject(curriculum_id, subject_id, version)
                ),
            }
        except CatalogNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}


__all__ = ["CatalogApi"]
