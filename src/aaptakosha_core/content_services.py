"""Application services for governed content lifecycle transitions."""

from __future__ import annotations

from typing import Tuple

from .content import ARCHIVED, DRAFT, PUBLISHED, REVIEW, ContentResource
from .content_repository import ContentRepository


class ContentNotFoundError(LookupError):
    """Raised when a requested content resource does not exist."""


class ContentTransitionError(ValueError):
    """Raised when a lifecycle transition is not permitted."""


class ContentService:
    """Application boundary for creating, reviewing, publishing, and archiving content."""

    def __init__(self, repository: ContentRepository):
        self.repository = repository

    def create(self, resource: ContentResource) -> ContentResource:
        if resource.status != DRAFT:
            raise ContentTransitionError("new content must start in draft")
        return self.repository.save(resource)

    def submit_for_review(self, resource_id: str) -> ContentResource:
        resource = self._get(resource_id)
        if resource.status != DRAFT:
            raise ContentTransitionError("only draft content can enter review")
        return self._save_with_status(resource, REVIEW)

    def publish(self, resource_id: str) -> ContentResource:
        resource = self._get(resource_id)
        if resource.status != REVIEW:
            raise ContentTransitionError("only content in review can be published")
        if not resource.provenance:
            raise ContentTransitionError("published content requires provenance")
        if not resource.curriculum_refs:
            raise ContentTransitionError("published content requires a curriculum reference")
        return self._save_with_status(resource, PUBLISHED)

    def archive(self, resource_id: str) -> ContentResource:
        resource = self._get(resource_id)
        if resource.status != PUBLISHED:
            raise ContentTransitionError("only published content can be archived")
        return self._save_with_status(resource, ARCHIVED)

    def get(self, resource_id: str) -> ContentResource:
        return self._get(resource_id)

    def list(self, status: str | None = None) -> Tuple[ContentResource, ...]:
        return self.repository.list(status)

    def _get(self, resource_id: str) -> ContentResource:
        resource = self.repository.get(resource_id)
        if resource is None:
            raise ContentNotFoundError(resource_id)
        return resource

    def _save_with_status(self, resource: ContentResource, status: str) -> ContentResource:
        return self.repository.save(
            ContentResource(
                resource_id=resource.resource_id,
                resource_type=resource.resource_type,
                title=resource.title,
                summary=resource.summary,
                status=status,
                provenance=resource.provenance,
                curriculum_refs=resource.curriculum_refs,
            )
        )


__all__ = ["ContentNotFoundError", "ContentService", "ContentTransitionError"]
