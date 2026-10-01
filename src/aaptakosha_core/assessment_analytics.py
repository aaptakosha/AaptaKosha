"""Assessment analytics and progress integration for Phase 4.

Analytics reports learner performance separately from learning-resource completion.
Progress integration maps attempt lifecycle to the existing domain-neutral progress model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .assessment import SUBMITTED, Assessment
from .assessment_repository import AssessmentAttemptRepository, AssessmentRepository
from .assessment_services import AssessmentAttemptNotFoundError, AssessmentNotFoundError
from .progress import (
    COMPLETED,
    IN_PROGRESS,
    LearningProgress,
    LearningProgressService,
)


@dataclass(frozen=True, slots=True)
class AssessmentAnalytics:
    """Deterministic performance summary for one learner and assessment."""

    assessment_id: str
    learner_id: str
    attempt_count: int
    submitted_attempt_count: int
    maximum_score: int
    best_score: int
    best_percent: int
    latest_score: int | None
    average_percent: int = 0

    def __post_init__(self) -> None:
        if not self.assessment_id.strip():
            raise ValueError("assessment_id must not be empty")
        if not self.learner_id.strip():
            raise ValueError("learner_id must not be empty")
        if self.attempt_count < 0 or self.submitted_attempt_count < 0:
            raise ValueError("attempt counts must not be negative")
        if self.submitted_attempt_count > self.attempt_count:
            raise ValueError("submitted attempts cannot exceed total attempts")
        if self.maximum_score < 0 or self.best_score < 0:
            raise ValueError("scores must not be negative")
        if self.best_score > self.maximum_score:
            raise ValueError("best_score cannot exceed maximum_score")
        if not 0 <= self.best_percent <= 100:
            raise ValueError("best_percent must be between 0 and 100")
        if self.latest_score is not None and not 0 <= self.latest_score <= self.maximum_score:
            raise ValueError("latest_score must be within the maximum score")
        if not 0 <= self.average_percent <= 100:
            raise ValueError("average_percent must be between 0 and 100")


class AssessmentAnalyticsService:
    """Computes learner assessment performance without exposing answer keys."""

    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        attempt_repository: AssessmentAttemptRepository,
    ):
        self.assessment_repository = assessment_repository
        self.attempt_repository = attempt_repository

    def for_assessment(self, learner_id: str, assessment_id: str) -> AssessmentAnalytics:
        if not learner_id.strip():
            raise ValueError("learner_id must not be empty")
        if not assessment_id.strip():
            raise ValueError("assessment_id must not be empty")

        assessment = self.assessment_repository.get(assessment_id)
        if assessment is None:
            raise AssessmentNotFoundError(assessment_id)

        attempts = tuple(
            attempt
            for attempt in self.attempt_repository.list_for_learner(learner_id)
            if attempt.assessment_id == assessment_id
        )
        submitted = tuple(attempt for attempt in attempts if attempt.status == SUBMITTED)
        maximum_score = sum(question.points for question in assessment.questions)

        scores = tuple(self._score(assessment, attempt) for attempt in submitted)
        best_score = max(scores, default=0)
        latest_score = scores[-1] if scores else None
        average_percent = round(sum(scores) * 100 / (len(scores) * maximum_score)) if scores and maximum_score else 0
        best_percent = round(best_score * 100 / maximum_score) if maximum_score else 0

        return AssessmentAnalytics(
            assessment_id=assessment_id,
            learner_id=learner_id,
            attempt_count=len(attempts),
            submitted_attempt_count=len(submitted),
            maximum_score=maximum_score,
            best_score=best_score,
            best_percent=best_percent,
            latest_score=latest_score,
            average_percent=average_percent,
        )

    def for_learner(self, learner_id: str) -> Tuple[AssessmentAnalytics, ...]:
        if not learner_id.strip():
            raise ValueError("learner_id must not be empty")

        assessment_ids = sorted(
            {attempt.assessment_id for attempt in self.attempt_repository.list_for_learner(learner_id)}
        )
        return tuple(self.for_assessment(learner_id, assessment_id) for assessment_id in assessment_ids)

    @staticmethod
    def _score(assessment: Assessment, attempt) -> int:
        answer_map = dict(attempt.answers)
        total = 0
        for question in assessment.questions:
            selected = set(answer_map.get(question.question_id, ()))
            correct = {
                option.option_id
                for option in question.options
                if option.is_correct
            }
            if selected == correct:
                total += question.points
        return total


class AssessmentProgressService:
    """Maps assessment-attempt lifecycle to the existing learning-progress model."""

    RESOURCE_TYPE = "assessment"

    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        attempt_repository: AssessmentAttemptRepository,
        progress_service: LearningProgressService,
    ):
        self.assessment_repository = assessment_repository
        self.attempt_repository = attempt_repository
        self.progress_service = progress_service

    def sync_attempt(self, attempt_id: str) -> LearningProgress:
        attempt = self.attempt_repository.get(attempt_id)
        if attempt is None:
            raise AssessmentAttemptNotFoundError(attempt_id)

        if self.assessment_repository.get(attempt.assessment_id) is None:
            raise AssessmentNotFoundError(attempt.assessment_id)

        if attempt.status == SUBMITTED:
            status = COMPLETED
            completion_percent = 100
        else:
            status = IN_PROGRESS
            completion_percent = 0

        return self.progress_service.record(
            attempt.learner_id,
            self.RESOURCE_TYPE,
            attempt.assessment_id,
            status=status,
            completion_percent=completion_percent,
        )


class AssessmentRevisionService:
    """Derives weak canonical content refs from submitted assessment performance."""

    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        attempt_repository: AssessmentAttemptRepository,
    ):
        self.assessment_repository = assessment_repository
        self.attempt_repository = attempt_repository

    def recommendations(
        self,
        learner_id: str,
        *,
        content_id: str | None = None,
        limit: int = 20,
    ) -> Tuple[dict, ...]:
        if not learner_id.strip():
            raise ValueError("learner_id must not be empty")
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        stats: dict[str, list[int]] = {}
        submitted_attempt_count = 0
        for attempt in self.attempt_repository.list_for_learner(learner_id):
            if attempt.status != SUBMITTED:
                continue
            assessment = self.assessment_repository.get(attempt.assessment_id)
            if assessment is None:
                continue
            submitted_attempt_count += 1
            answer_map = dict(attempt.answers)
            for question in assessment.questions:
                refs = tuple(
                    ref for ref in question.content_refs
                    if not content_id or ref == content_id or ref.startswith(content_id + ".")
                )
                if not refs:
                    continue
                selected = set(answer_map.get(question.question_id, ()))
                correct = {
                    option.option_id
                    for option in question.options
                    if option.is_correct
                }
                hit = int(selected == correct)
                for ref in refs:
                    bucket = stats.setdefault(ref, [0, 0])
                    bucket[0] += 1
                    bucket[1] += hit

        rows = []
        for ref, (attempts, correct) in stats.items():
            mastery_percent = round(correct * 100 / attempts)
            if mastery_percent >= 100:
                continue
            rows.append({
                "content_ref": ref,
                "attempts": attempts,
                "correct_attempts": correct,
                "mastery_percent": mastery_percent,
                "revision_priority": 100 - mastery_percent,
            })
        rows.sort(key=lambda item: (-item["revision_priority"], item["mastery_percent"], item["content_ref"]))
        return tuple(rows[:limit])


__all__ = [
    "AssessmentAnalytics",
    "AssessmentAnalyticsService",
    "AssessmentProgressService",
]
