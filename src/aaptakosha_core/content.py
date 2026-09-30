"""Domain-neutral knowledge/content contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


DRAFT = "draft"
REVIEW = "review"
PUBLISHED = "published"
ARCHIVED = "archived"
VALID_CONTENT_STATUSES = (DRAFT, REVIEW, PUBLISHED, ARCHIVED)


@dataclass(frozen=True, slots=True)
class ContentProvenance:
    """Source metadata kept separate from curriculum authority."""

    source: str
    locator: str = ""
    attribution: str = ""

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("source must not be empty")


@dataclass(frozen=True, slots=True)
class ContentResource:
    """A publishable knowledge resource linked by generic identifiers."""

    resource_id: str
    resource_type: str
    title: str
    summary: str = ""
    status: str = DRAFT
    provenance: Tuple[ContentProvenance, ...] = ()
    curriculum_refs: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value, field in (
            (self.resource_id, "resource_id"),
            (self.resource_type, "resource_type"),
            (self.title, "title"),
        ):
            if not value.strip():
                raise ValueError(f"{field} must not be empty")
        if self.status not in VALID_CONTENT_STATUSES:
            raise ValueError(f"unsupported content status: {self.status}")
        if len(set(self.curriculum_refs)) != len(self.curriculum_refs):
            raise ValueError("curriculum_refs must be unique")
        if any(not ref.strip() for ref in self.curriculum_refs):
            raise ValueError("curriculum_refs must not contain empty values")


__all__ = [
    "ARCHIVED",
    "DRAFT",
    "PUBLISHED",
    "REVIEW",
    "VALID_CONTENT_STATUSES",
    "ContentProvenance",
    "ContentResource",
]
