"""Framework-neutral API boundary for learner assessments and attempts."""

from __future__ import annotations

from typing import Any

from .assessment import Assessment, AssessmentAttempt, PUBLISHED
from .assessment_services import (
    AssessmentAttemptError,
    AssessmentAttemptNotFoundError,
    AssessmentNotFoundError,
    AssessmentService,
    AssessmentTransitionError,
)


def _question_payload(question: Any) -> dict[str, Any]:
    return {
        "question_id": question.question_id,
        "prompt": question.prompt,
        "points": question.points,
        "options": [
            {"option_id": option.option_id, "text": option.text}
            for option in question.options
        ],
    }


def _assessment_payload(assessment: Assessment) -> dict[str, Any]:
    return {
        "assessment_id": assessment.assessment_id,
        "title": assessment.title,
        "status": assessment.status,
        "curriculum_refs": list(assessment.curriculum_refs),
        "questions": [_question_payload(question) for question in assessment.questions],
    }


def _attempt_payload(attempt: AssessmentAttempt) -> dict[str, Any]:
    return {
        "attempt_id": attempt.attempt_id,
        "assessment_id": attempt.assessment_id,
        "learner_id": attempt.learner_id,
        "status": attempt.status,
        "answers": [
            {"question_id": question_id, "selected_option_ids": list(selected)}
            for question_id, selected in attempt.answers
        ],
    }


class AssessmentApi:
    """Transport-neutral handlers for assessment and learner-attempt use cases."""

    def __init__(self, service: AssessmentService):
        self.service = service

    def get_assessment(self, assessment_id: str) -> dict[str, Any]:
        try:
            assessment = self.service.get(assessment_id)
            if assessment.status != PUBLISHED:
                return {"status": 404, "error": {"code": "not_found", "message": assessment_id}}
            return {"status": 200, "data": _assessment_payload(assessment)}
        except AssessmentNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}

    def list_assessments(self) -> dict[str, Any]:
        return {
            "status": 200,
            "data": {"assessments": [_assessment_payload(x) for x in self.service.list(PUBLISHED)]},
        }

    def start_attempt(self, attempt: AssessmentAttempt) -> dict[str, Any]:
        try:
            started = self.service.start_attempt(attempt)
            return {"status": 201, "data": _attempt_payload(started)}
        except AssessmentNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}
        except AssessmentAttemptError as exc:
            return {"status": 409, "error": {"code": "invalid_attempt", "message": str(exc)}}

    def get_attempt(self, attempt_id: str, learner_id: str) -> dict[str, Any]:
        try:
            attempt = self.service.get_attempt(attempt_id)
            if attempt.learner_id != learner_id:
                return {"status": 404, "error": {"code": "not_found", "message": attempt_id}}
            return {"status": 200, "data": _attempt_payload(attempt)}
        except AssessmentAttemptNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}

    def submit_attempt(self, attempt_id: str, learner_id: str) -> dict[str, Any]:
        try:
            attempt = self.service.get_attempt(attempt_id)
            if attempt.learner_id != learner_id:
                return {"status": 404, "error": {"code": "not_found", "message": attempt_id}}
            submitted = self.service.submit_attempt(attempt_id)
            return {"status": 200, "data": _attempt_payload(submitted)}
        except AssessmentAttemptNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}
        except AssessmentNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}
        except AssessmentAttemptError as exc:
            return {"status": 409, "error": {"code": "invalid_attempt", "message": str(exc)}}

    def score_attempt(self, attempt_id: str, learner_id: str) -> dict[str, Any]:
        try:
            attempt = self.service.get_attempt(attempt_id)
            if attempt.learner_id != learner_id:
                return {"status": 404, "error": {"code": "not_found", "message": attempt_id}}
            score = self.service.score_attempt(attempt_id)
            return {"status": 200, "data": {"attempt_id": attempt_id, "score": score}}
        except AssessmentAttemptNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}
        except AssessmentNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}
        except ValueError as exc:
            return {"status": 409, "error": {"code": "not_scored", "message": str(exc)}}


__all__ = ["AssessmentApi"]
