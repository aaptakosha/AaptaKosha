import sqlite3

from aaptakosha_core.assessment import Assessment, AssessmentAttempt, AssessmentQuestion, QuestionOption, SUBMITTED
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository


def question(question_id="q1"):
    return AssessmentQuestion(
        question_id, "Which option is correct?",
        (QuestionOption("a", "Correct", is_correct=True), QuestionOption("b", "Incorrect")),
    )


def test_assessment_repository_round_trip_and_status_filter():
    repo = SQLiteAssessmentRepository(sqlite3.connect(":memory:"))
    repo.apply_migrations()
    assessment = Assessment("a1", "Assessment 1", curriculum_refs=("subject:s1",), questions=(question(),))
    repo.save(assessment)
    assert repo.get("a1") == assessment
    assert repo.list() == (assessment,)
    assert repo.list("published") == ()


def test_assessment_repository_round_trip_attempts():
    repo = SQLiteAssessmentRepository(sqlite3.connect(":memory:"))
    repo.apply_migrations()
    assessment = Assessment("a1", "Assessment 1", questions=(question(),))
    repo.save(assessment)
    attempt = AssessmentAttempt("attempt-1", "a1", "learner-1", status=SUBMITTED, answers=(("q1", ("a",)),))
    repo.save(attempt)
    assert repo.get("attempt-1") == attempt
    assert repo.list_for_learner("learner-1") == (attempt,)


def test_assessment_repository_upserts_definition():
    repo = SQLiteAssessmentRepository(sqlite3.connect(":memory:"))
    repo.apply_migrations()
    first = Assessment("a1", "First", questions=(question(),))
    second = Assessment("a1", "Second", status="published", questions=(question(),))
    repo.save(first)
    repo.save(second)
    assert repo.get("a1") == second
