"""Application use cases for the AaptaKosha catalog."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Tuple
from .catalog import Curriculum, Subject

class CatalogRepository(Protocol):
    def get_curriculum(self, curriculum_id: str, version: str | None = None) -> Curriculum | None: ...
    def list_subjects(self, curriculum_id: str, version: str | None = None) -> Tuple[Subject, ...]: ...
    def get_subject(self, curriculum_id: str, subject_id: str, version: str | None = None) -> Subject | None: ...

class CatalogNotFoundError(LookupError):
    """Raised when a requested catalog item does not exist."""

@dataclass(frozen=True, slots=True)
class CatalogService:
    repository: CatalogRepository

    def get_curriculum(self, curriculum_id: str, version: str | None = None) -> Curriculum:
        curriculum = self.repository.get_curriculum(curriculum_id, version)
        if curriculum is None:
            raise CatalogNotFoundError("curriculum not found: " + curriculum_id + (f"@{version}" if version else ""))
        return curriculum

    def list_subjects(self, curriculum_id: str, version: str | None = None) -> Tuple[Subject, ...]:
        self.get_curriculum(curriculum_id, version)
        return self.repository.list_subjects(curriculum_id, version)

    def get_subject(self, curriculum_id: str, subject_id: str, version: str | None = None) -> Subject:
        self.get_curriculum(curriculum_id, version)
        subject = self.repository.get_subject(curriculum_id, subject_id, version)
        if subject is None:
            raise CatalogNotFoundError(f"subject not found: {curriculum_id}/{subject_id}")
        return subject

__all__ = ["CatalogNotFoundError", "CatalogRepository", "CatalogService"]
