"""Learner-facing assessment workflow for Practice and Results screens.

This adapter keeps assessment persistence/scoring in the Phase 4 domain services
while exposing one composition boundary for learner UI integrations.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from .assessment import AssessmentAttempt, IN_PROGRESS, PUBLISHED, SUBMITTED, score_attempt
from .assessment_analytics import AssessmentAnalyticsService, AssessmentRevisionService
from .assessment_services import (
    AssessmentAttemptError,
    AssessmentAttemptNotFoundError,
    AssessmentNotFoundError,
    AssessmentService,
)


def _question(question: Any, *, reveal_answer: bool = False) -> dict[str, Any]:
    options = []
    correct_ids = []
    for option in question.options:
        options.append({"option_id": option.option_id, "text": option.text})
        if option.is_correct:
            correct_ids.append(option.option_id)
    payload = {
        "question_id": question.question_id,
        "prompt": question.prompt,
        "points": question.points,
        "options": options,
    }
    if reveal_answer:
        payload["correct_option_ids"] = correct_ids
    return payload


class AssessmentLearningApi:
    """Composition boundary for Assessment -> Practice -> Results."""

    def __init__(self, service: AssessmentService):
        self.service = service

    def list_assessments(self, curriculum_ref: str | None = None) -> dict[str, Any]:
        assessments = self.service.list(PUBLISHED)
        if curriculum_ref is not None:
            assessments = tuple(
                item for item in assessments if curriculum_ref in item.curriculum_refs
            )
        return {
            "status": 200,
            "data": {
                "assessments": [
                    {
                        "assessment_id": item.assessment_id,
                        "title": item.title,
                        "curriculum_refs": list(item.curriculum_refs),
                        "question_count": len(item.questions),
                        "maximum_score": sum(q.points for q in item.questions),
                    }
                    for item in assessments
                ]
            },
        }

    def learner_analytics(self, learner_id: str) -> dict[str, Any]:
        analytics = AssessmentAnalyticsService(
            self.service.assessment_repository,
            self.service.attempt_repository,
        ).for_learner(learner_id)
        submitted = [item for item in analytics if item.submitted_attempt_count]
        total_attempts = sum(item.submitted_attempt_count for item in analytics)
        weighted_percent = sum(item.average_percent * item.submitted_attempt_count for item in submitted)
        average_percent = round(weighted_percent / total_attempts) if total_attempts else 0
        return {
            "status": 200,
            "data": {
                "assessment_count": len(analytics),
                "attempt_count": total_attempts,
                "average_percent": average_percent,
                "assessments": [
                    {
                        "assessment_id": item.assessment_id,
                        "attempt_count": item.submitted_attempt_count,
                        "best_score": item.best_score,
                        "best_percent": item.best_percent,
                        "latest_score": item.latest_score,
                        "maximum_score": item.maximum_score,
                    }
                    for item in analytics
                ],
            },
        }

    def revision_recommendations(
        self,
        learner_id: str,
        *,
        content_id: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        recommendations = AssessmentRevisionService(
            self.service.assessment_repository,
            self.service.attempt_repository,
        ).recommendations(learner_id, content_id=content_id, limit=limit)
        return {
            "status": 200,
            "data": {
                "content_id": content_id,
                "recommendations": list(recommendations),
            },
        }

    def start(self, assessment_id: str, learner_id: str) -> dict[str, Any]:
        assessment = self.service.get(assessment_id)
        if assessment.status != PUBLISHED:
            return {"status": 404, "error": {"code": "not_found", "message": assessment_id}}
        attempt = AssessmentAttempt(
            attempt_id=str(uuid4()),
            assessment_id=assessment_id,
            learner_id=learner_id,
            status=IN_PROGRESS,
        )
        return self.service.start_attempt(attempt) and {
            "status": 201,
            "data": self._practice_payload(assessment_id, attempt.attempt_id, learner_id),
        }

    def save_answers(
        self,
        attempt_id: str,
        learner_id: str,
        answers: tuple[tuple[str, tuple[str, ...]], ...],
    ) -> dict[str, Any]:
        try:
            attempt = self.service.save_answers(attempt_id, learner_id, answers)
            return {"status": 200, "data": self._attempt_payload(attempt)}
        except AssessmentAttemptNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}
        except AssessmentNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}
        except AssessmentAttemptError as exc:
            return {"status": 409, "error": {"code": "invalid_attempt", "message": str(exc)}}

    def submit(self, attempt_id: str, learner_id: str) -> dict[str, Any]:
        try:
            attempt = self.service.get_attempt(attempt_id)
            if attempt.learner_id != learner_id:
                return {"status": 404, "error": {"code": "not_found", "message": attempt_id}}
            submitted = self.service.submit_attempt(attempt_id)
            return {"status": 200, "data": self._results_payload(submitted)}
        except (AssessmentAttemptNotFoundError, AssessmentNotFoundError) as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}
        except AssessmentAttemptError as exc:
            return {"status": 409, "error": {"code": "invalid_attempt", "message": str(exc)}}

    def result(self, attempt_id: str, learner_id: str) -> dict[str, Any]:
        try:
            attempt = self.service.get_attempt(attempt_id)
            if attempt.learner_id != learner_id:
                return {"status": 404, "error": {"code": "not_found", "message": attempt_id}}
            if attempt.status != SUBMITTED:
                return {"status": 409, "error": {"code": "not_scored", "message": "attempt is not submitted"}}
            return {"status": 200, "data": self._results_payload(attempt)}
        except AssessmentAttemptNotFoundError as exc:
            return {"status": 404, "error": {"code": "not_found", "message": str(exc)}}

    def _practice_payload(self, assessment_id: str, attempt_id: str, learner_id: str) -> dict[str, Any]:
        assessment = self.service.get(assessment_id)
        attempt = self.service.get_attempt(attempt_id)
        return {
            "attempt": self._attempt_payload(attempt),
            "assessment": {
                "assessment_id": assessment.assessment_id,
                "title": assessment.title,
                "questions": [_question(q) for q in assessment.questions],
                "maximum_score": sum(q.points for q in assessment.questions),
            },
        }

    def _results_payload(self, attempt: AssessmentAttempt) -> dict[str, Any]:
        assessment = self.service.get(attempt.assessment_id)
        score = score_attempt(assessment, attempt)
        maximum = sum(q.points for q in assessment.questions)
        answer_map = dict(attempt.answers)
        breakdown = []
        for question in assessment.questions:
            selected = list(answer_map.get(question.question_id, ()))
            correct = [o.option_id for o in question.options if o.is_correct]
            breakdown.append({
                "question_id": question.question_id,
                "prompt": question.prompt,
                "options": [{"option_id": o.option_id, "text": o.text} for o in question.options],
                "selected_option_ids": selected,
                "correct_option_ids": correct,
                "is_correct": set(selected) == set(correct),
                "points": question.points if set(selected) == set(correct) else 0,
                "maximum_points": question.points,
            })
        analytics = AssessmentAnalyticsService(
            self.service.assessment_repository,
            self.service.attempt_repository,
        ).for_assessment(attempt.learner_id, attempt.assessment_id)
        return {
            "attempt": self._attempt_payload(attempt),
            "assessment": {"assessment_id": assessment.assessment_id, "title": assessment.title},
            "score": score,
            "maximum_score": maximum,
            "percent": round(score * 100 / maximum) if maximum else 0,
            "breakdown": breakdown,
            "analytics": {
                "attempt_count": analytics.attempt_count,
                "submitted_attempt_count": analytics.submitted_attempt_count,
                "best_score": analytics.best_score,
                "best_percent": analytics.best_percent,
                "latest_score": analytics.latest_score,
            },
        }

    @staticmethod
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


__all__ = ["AssessmentLearningApi"]
