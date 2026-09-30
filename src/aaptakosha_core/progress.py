"""Domain-neutral learning-progress contracts and application service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Tuple


NOT_STARTED = "not_started"
IN_PROGRESS = "in_progress"
COMPLETED = "completed"
VALID_STATUSES = (NOT_STARTED, IN_PROGRESS, COMPLETED)


@dataclass(frozen=True, slots=True)
class LearningProgress:
    """A learner's progress snapshot for one addressable learning resource."""

    subject_id: str
    resource_type: str
    resource_id: str
    status: str = NOT_STARTED
    completion_percent: int = 0

    def __post_init__(self) -> None:
        for value, field in (
            (self.subject_id, "subject_id"),
            (self.resource_type, "resource_type"),
            (self.resource_id, "resource_id"),
        ):
            if not value.strip():
                raise ValueError(f"{field} must not be empty")
        if self.status not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}")
        if not 0 <= self.completion_percent <= 100:
            raise ValueError("completion_percent must be between 0 and 100")
        if self.status == NOT_STARTED and self.completion_percent != 0:
            raise ValueError("not_started progress must be 0 percent")
        if self.status == COMPLETED and self.completion_percent != 100:
            raise ValueError("completed progress must be 100 percent")


class LearningProgressRepository(Protocol):
    """Persistence boundary for learner progress snapshots."""

    def get(
        self, subject_id: str, resource_type: str, resource_id: str
    ) -> LearningProgress | None: ...

    def list_for_subject(self, subject_id: str) -> Tuple[LearningProgress, ...]: ...

    def save(self, progress: LearningProgress) -> LearningProgress: ...


class LearningProgressService:
    """Application use cases for reading and recording learning progress."""

    def __init__(self, repository: LearningProgressRepository):
        self.repository = repository

    def get(
        self, subject_id: str, resource_type: str, resource_id: str
    ) -> LearningProgress | None:
        return self.repository.get(subject_id, resource_type, resource_id)

    def list_for_subject(self, subject_id: str) -> Tuple[LearningProgress, ...]:
        if not subject_id.strip():
            raise ValueError("subject_id must not be empty")
        return self.repository.list_for_subject(subject_id)

    def record(
        self,
        subject_id: str,
        resource_type: str,
        resource_id: str,
        *,
        status: str,
        completion_percent: int,
    ) -> LearningProgress:
        progress = LearningProgress(
            subject_id=subject_id,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            completion_percent=completion_percent,
        )
        return self.repository.save(progress)


__all__ = [
    "COMPLETED",
    "IN_PROGRESS",
    "LearningProgress",
    "LearningProgressRepository",
    "LearningProgressService",
    "NOT_STARTED",
    "VALID_STATUSES",
]
