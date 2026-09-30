"""Auditable curriculum-to-content linking contracts and service."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Tuple

from .content_repository import ContentRepository

@dataclass(frozen=True, slots=True)
class CurriculumContentLink:
    curriculum_ref: str
    resource_id: str
    relationship: str = "supports"

    def __post_init__(self):
        if not self.curriculum_ref.strip() or not self.resource_id.strip():
            raise ValueError("curriculum_ref and resource_id must not be empty")
        if not self.relationship.strip():
            raise ValueError("relationship must not be empty")

class CurriculumContentLinkRepository(Protocol):
    def save(self, link: CurriculumContentLink) -> CurriculumContentLink: ...
    def list_for_curriculum(self, curriculum_ref: str) -> Tuple[CurriculumContentLink, ...]: ...
    def list_for_resource(self, resource_id: str) -> Tuple[CurriculumContentLink, ...]: ...

class CurriculumContentLinkService:
    def __init__(self, repository: CurriculumContentLinkRepository, content_repository: ContentRepository):
        self.repository = repository
        self.content_repository = content_repository

    def link(self, curriculum_ref: str, resource_id: str, relationship: str = "supports") -> CurriculumContentLink:
        if self.content_repository.get(resource_id) is None:
            raise LookupError(f"content resource not found: {resource_id}")
        return self.repository.save(CurriculumContentLink(curriculum_ref, resource_id, relationship))

    def for_curriculum(self, curriculum_ref: str) -> Tuple[CurriculumContentLink, ...]:
        return self.repository.list_for_curriculum(curriculum_ref)

    def for_resource(self, resource_id: str) -> Tuple[CurriculumContentLink, ...]:
        return self.repository.list_for_resource(resource_id)

__all__ = ["CurriculumContentLink", "CurriculumContentLinkRepository", "CurriculumContentLinkService"]
