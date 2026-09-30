import sqlite3

import pytest

from aaptakosha_core.assessment import (
    Assessment,
    AssessmentAttempt,
    AssessmentQuestion,
    QuestionOption,
    SUBMITTED,
)
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository
from aaptakosha_core.assessment_services import (
    AssessmentAttemptError,
    AssessmentService,
    AssessmentTransitionError,
)


def question(question_id="q1"):
    return AssessmentQuestion(
        question_id,
        "Which option is correct?",
        (
            QuestionOption("a", "Correct", is_correct=True),
            QuestionOption("b", "Incorrect"),
        ),
    )


def service():
    repo = SQLiteAssessmentRepository(sqlite3.connect(":memory:"))
    repo.apply_migrations()
    return AssessmentService(repo, repo)


def test_publish_requires_questions_and_valid_transition():
    svc = service()
    svc.create(Assessment("a1", "Empty"))
    with pytest.raises(AssessmentTransitionError):
        svc.publish("a1")

    svc.create(Assessment("a2", "Ready", questions=(question(),)))
    assert svc.publish("a2").status == "published"
    assert svc.archive("a2").status == "archived"


def test_attempt_requires_published_assessment():
    svc = service()
    svc.create(Assessment("a1", "Draft", questions=(question(),)))
    attempt = AssessmentAttempt("at1", "a1", "learner")
    with pytest.raises(AssessmentAttemptError):
        svc.start_attempt(attempt)


def test_start_submit_and_score_attempt():
    svc = service()
    svc.create(Assessment("a1", "Ready", questions=(question(),)))
    svc.publish("a1")
    attempt = AssessmentAttempt("at1", "a1", "learner", answers=(("q1", ("a",)),))

    started = svc.start_attempt(attempt)
    assert started.status == "in_progress"
    submitted = svc.submit_attempt("at1")
    assert submitted.status == SUBMITTED
    assert svc.score_attempt("at1") == 1


def test_invalid_attempt_answer_is_rejected():
    svc = service()
    svc.create(Assessment("a1", "Ready", questions=(question(),)))
    svc.publish("a1")
    with pytest.raises(AssessmentAttemptError):
        svc.start_attempt(
            AssessmentAttempt("at1", "a1", "learner", answers=(("unknown", ("a",)),))
        )


def test_submitted_attempt_cannot_be_submitted_again():
    svc = service()
    svc.create(Assessment("a1", "Ready", questions=(question(),)))
    svc.publish("a1")
    svc.start_attempt(AssessmentAttempt("at1", "a1", "learner"))
    svc.submit_attempt("at1")
    with pytest.raises(AssessmentAttemptError):
        svc.submit_attempt("at1")
