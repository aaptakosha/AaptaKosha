"""Application services for governed assessment lifecycle and attempts."""

from __future__ import annotations

from typing import Tuple

from .assessment import (
    ARCHIVED,
    DRAFT,
    IN_PROGRESS,
    PUBLISHED,
    SUBMITTED,
    Assessment,
    AssessmentAttempt,
    score_attempt,
)
from .assessment_repository import AssessmentAttemptRepository, AssessmentRepository
from .progress import LearningProgressService


class AssessmentNotFoundError(LookupError):
    """Raised when an assessment does not exist."""


class AssessmentAttemptNotFoundError(LookupError):
    """Raised when an attempt does not exist."""


class AssessmentTransitionError(ValueError):
    """Raised when an assessment lifecycle transition is not permitted."""


class AssessmentAttemptError(ValueError):
    """Raised when an attempt operation is not permitted."""


class AssessmentService:
    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        attempt_repository: AssessmentAttemptRepository,
        progress_service: LearningProgressService | None = None,
    ):
        self.assessment_repository = assessment_repository
        self.attempt_repository = attempt_repository
        self.progress_service = progress_service

    def create(self, assessment: Assessment) -> Assessment:
        if assessment.status != DRAFT:
            raise AssessmentTransitionError("new assessments must start in draft")
        return self.assessment_repository.save(assessment)

    def publish(self, assessment_id: str) -> Assessment:
        assessment = self._get_assessment(assessment_id)
        if assessment.status != DRAFT:
            raise AssessmentTransitionError("only draft assessments can be published")
        if not assessment.questions:
            raise AssessmentTransitionError("published assessments require at least one question")
        return self._save_assessment_status(assessment, PUBLISHED)

    def archive(self, assessment_id: str) -> Assessment:
        assessment = self._get_assessment(assessment_id)
        if assessment.status != PUBLISHED:
            raise AssessmentTransitionError("only published assessments can be archived")
        return self._save_assessment_status(assessment, ARCHIVED)

    def get(self, assessment_id: str) -> Assessment:
        return self._get_assessment(assessment_id)

    def list(self, status: str | None = None) -> Tuple[Assessment, ...]:
        return self.assessment_repository.list(status)

    def start_attempt(self, attempt: AssessmentAttempt) -> AssessmentAttempt:
        assessment = self._get_assessment(attempt.assessment_id)
        if assessment.status != PUBLISHED:
            raise AssessmentAttemptError("attempts can only start for published assessments")
        if attempt.status != IN_PROGRESS:
            raise AssessmentAttemptError("new attempts must start in progress")
        self._validate_answers(assessment, attempt)
        saved = self.attempt_repository.save(attempt)
        self._sync_progress(saved)
        return saved

    def submit_attempt(self, attempt_id: str) -> AssessmentAttempt:
        attempt = self._get_attempt(attempt_id)
        if attempt.status != IN_PROGRESS:
            raise AssessmentAttemptError("only in-progress attempts can be submitted")
        assessment = self._get_assessment(attempt.assessment_id)
        self._validate_answers(assessment, attempt)
        submitted = AssessmentAttempt(
            attempt_id=attempt.attempt_id,
            assessment_id=attempt.assessment_id,
            learner_id=attempt.learner_id,
            status=SUBMITTED,
            answers=attempt.answers,
        )
        saved = self.attempt_repository.save(submitted)
        self._sync_progress(saved)
        return saved

    def get_attempt(self, attempt_id: str) -> AssessmentAttempt:
        return self._get_attempt(attempt_id)

    def list_attempts_for_learner(self, learner_id: str) -> Tuple[AssessmentAttempt, ...]:
        return self.attempt_repository.list_for_learner(learner_id)

    def score_attempt(self, attempt_id: str) -> int:
        attempt = self._get_attempt(attempt_id)
        assessment = self._get_assessment(attempt.assessment_id)
        return score_attempt(assessment, attempt)

    def _get_assessment(self, assessment_id: str) -> Assessment:
        assessment = self.assessment_repository.get(assessment_id)
        if assessment is None:
            raise AssessmentNotFoundError(assessment_id)
        return assessment

    def _get_attempt(self, attempt_id: str) -> AssessmentAttempt:
        attempt = self.attempt_repository.get(attempt_id)
        if attempt is None:
            raise AssessmentAttemptNotFoundError(attempt_id)
        return attempt

    def _save_assessment_status(self, assessment: Assessment, status: str) -> Assessment:
        return self.assessment_repository.save(
            Assessment(
                assessment_id=assessment.assessment_id,
                title=assessment.title,
                status=status,
                curriculum_refs=assessment.curriculum_refs,
                questions=assessment.questions,
            )
        )

    def _sync_progress(self, attempt: AssessmentAttempt) -> None:
        if self.progress_service is None:
            return
        from .assessment_analytics import AssessmentProgressService

        AssessmentProgressService(
            self.assessment_repository,
            self.attempt_repository,
            self.progress_service,
        ).sync_attempt(attempt.attempt_id)

    @staticmethod
    def _validate_answers(assessment: Assessment, attempt: AssessmentAttempt) -> None:
        if attempt.assessment_id != assessment.assessment_id:
            raise AssessmentAttemptError("attempt does not belong to assessment")
        question_map = {question.question_id: question for question in assessment.questions}
        for question_id, selected in attempt.answers:
            question = question_map.get(question_id)
            if question is None:
                raise AssessmentAttemptError(f"unknown question: {question_id}")
            valid_options = {option.option_id for option in question.options}
            if any(option_id not in valid_options for option_id in selected):
                raise AssessmentAttemptError(f"unknown option for question: {question_id}")
            if len(set(selected)) != len(selected):
                raise AssessmentAttemptError(f"duplicate options for question: {question_id}")


__all__ = [
    "AssessmentAttemptError",
    "AssessmentAttemptNotFoundError",
    "AssessmentNotFoundError",
    "AssessmentService",
    "AssessmentTransitionError",
]
