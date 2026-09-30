"""Domain-neutral assessment contracts for Phase 4."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

DRAFT = "draft"
PUBLISHED = "published"
ARCHIVED = "archived"
VALID_ASSESSMENT_STATUSES = (DRAFT, PUBLISHED, ARCHIVED)

IN_PROGRESS = "in_progress"
SUBMITTED = "submitted"
VALID_ATTEMPT_STATUSES = (IN_PROGRESS, SUBMITTED)


@dataclass(frozen=True, slots=True)
class QuestionOption:
    option_id: str
    text: str
    is_correct: bool = False

    def __post_init__(self) -> None:
        if not self.option_id.strip():
            raise ValueError("option_id must not be empty")
        if not self.text.strip():
            raise ValueError("text must not be empty")


@dataclass(frozen=True, slots=True)
class AssessmentQuestion:
    question_id: str
    prompt: str
    options: Tuple[QuestionOption, ...]
    points: int = 1

    def __post_init__(self) -> None:
        if not self.question_id.strip():
            raise ValueError("question_id must not be empty")
        if not self.prompt.strip():
            raise ValueError("prompt must not be empty")
        if not self.options:
            raise ValueError("a question must have at least one option")
        if len({o.option_id for o in self.options}) != len(self.options):
            raise ValueError("question options must have unique option_id values")
        if not 0 < self.points:
            raise ValueError("points must be greater than zero")
        if not any(o.is_correct for o in self.options):
            raise ValueError("question must have at least one correct option")


@dataclass(frozen=True, slots=True)
class Assessment:
    assessment_id: str
    title: str
    status: str = DRAFT
    curriculum_refs: Tuple[str, ...] = ()
    questions: Tuple[AssessmentQuestion, ...] = ()

    def __post_init__(self) -> None:
        if not self.assessment_id.strip():
            raise ValueError("assessment_id must not be empty")
        if not self.title.strip():
            raise ValueError("title must not be empty")
        if self.status not in VALID_ASSESSMENT_STATUSES:
            raise ValueError(f"unsupported assessment status: {self.status}")
        if len(set(self.curriculum_refs)) != len(self.curriculum_refs):
            raise ValueError("curriculum_refs must be unique")
        if any(not ref.strip() for ref in self.curriculum_refs):
            raise ValueError("curriculum_refs must not contain empty values")
        if len({q.question_id for q in self.questions}) != len(self.questions):
            raise ValueError("questions must have unique question_id values")


@dataclass(frozen=True, slots=True)
class AssessmentAttempt:
    attempt_id: str
    assessment_id: str
    learner_id: str
    status: str = IN_PROGRESS
    answers: Tuple[Tuple[str, Tuple[str, ...]], ...] = ()

    def __post_init__(self) -> None:
        for value, field in (
            (self.attempt_id, "attempt_id"),
            (self.assessment_id, "assessment_id"),
            (self.learner_id, "learner_id"),
        ):
            if not value.strip():
                raise ValueError(f"{field} must not be empty")
        if self.status not in VALID_ATTEMPT_STATUSES:
            raise ValueError(f"unsupported attempt status: {self.status}")
        question_ids = [q for q, _ in self.answers]
        if len(set(question_ids)) != len(question_ids):
            raise ValueError("answers must have unique question IDs")
        if any(not question_id.strip() for question_id in question_ids):
            raise ValueError("answer question IDs must not be empty")


def score_attempt(assessment: Assessment, attempt: AssessmentAttempt) -> int:
    if attempt.assessment_id != assessment.assessment_id:
        raise ValueError("attempt does not belong to assessment")
    if attempt.status != SUBMITTED:
        raise ValueError("only submitted attempts can be scored")

    answer_map = dict(attempt.answers)
    total = 0
    for question in assessment.questions:
        selected = set(answer_map.get(question.question_id, ()))
        correct = {option.option_id for option in question.options if option.is_correct}
        if selected == correct:
            total += question.points
    return total


__all__ = [
    "ARCHIVED",
    "Assessment",
    "AssessmentAttempt",
    "AssessmentQuestion",
    "DRAFT",
    "IN_PROGRESS",
    "PUBLISHED",
    "QuestionOption",
    "SUBMITTED",
    "VALID_ASSESSMENT_STATUSES",
    "VALID_ATTEMPT_STATUSES",
    "score_attempt",
]
