"""Framework-agnostic academic catalog contracts for Phase 2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _require(value: str, field: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{field} must not be empty")
    return value


@dataclass(frozen=True, slots=True)
class Topic:
    topic_id: str
    name: str

    def __post_init__(self) -> None:
        _require(self.topic_id, "topic_id")
        _require(self.name, "name")


@dataclass(frozen=True, slots=True)
class Subject:
    subject_id: str
    name: str
    topics: Tuple[Topic, ...] = ()

    def __post_init__(self) -> None:
        _require(self.subject_id, "subject_id")
        _require(self.name, "name")
        if len({topic.topic_id for topic in self.topics}) != len(self.topics):
            raise ValueError("topics must have unique topic_id values")


@dataclass(frozen=True, slots=True)
class Curriculum:
    curriculum_id: str
    version: str
    professional_year: int
    subjects: Tuple[Subject, ...] = ()

    def __post_init__(self) -> None:
        _require(self.curriculum_id, "curriculum_id")
        _require(self.version, "version")
        if self.professional_year < 1:
            raise ValueError("professional_year must be >= 1")
        if len({subject.subject_id for subject in self.subjects}) != len(self.subjects):
            raise ValueError("subjects must have unique subject_id values")
