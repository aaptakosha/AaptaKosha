import sqlite3

from aaptakosha_core.assessment import Assessment, AssessmentAttempt, AssessmentQuestion, QuestionOption
from aaptakosha_core.assessment_api import AssessmentApi
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository
from aaptakosha_core.assessment_services import AssessmentService


def question():
    return AssessmentQuestion(
        "q1",
        "Which is correct?",
        (QuestionOption("a", "First", True), QuestionOption("b", "Second")),
        points=2,
    )


def api():
    repo = SQLiteAssessmentRepository(sqlite3.connect(":memory:"))
    repo.apply_migrations()
    return AssessmentApi(AssessmentService(repo, repo))


def publish(api):
    svc = api.service
    svc.create(Assessment("a1", "Test", questions=(question(),)))
    assert svc.publish("a1").status == "published"


def test_assessment_serialization_hides_answer_keys():
    api_instance = api()
    publish(api_instance)
    response = api_instance.get_assessment("a1")
    assert response["status"] == 200
    assert response["data"]["questions"][0]["options"] == [
        {"option_id": "a", "text": "First"},
        {"option_id": "b", "text": "Second"},
    ]
    assert "is_correct" not in response["data"]["questions"][0]["options"][0]


def test_unpublished_assessments_are_hidden_from_learner_reads():
    api_instance = api()
    api_instance.service.create(Assessment("draft", "Draft", questions=(question(),)))
    assert api_instance.get_assessment("draft")["status"] == 404
    assert api_instance.list_assessments()["data"]["assessments"] == []

    publish(api_instance)
    assert [x["assessment_id"] for x in api_instance.list_assessments()["data"]["assessments"]] == ["a1"]


def test_attempt_lifecycle_and_score_api():
    api_instance = api()
    publish(api_instance)
    started = api_instance.start_attempt(
        AssessmentAttempt("at1", "a1", "learner-1", answers=(("q1", ("a",)),))
    )
    assert started["status"] == 201
    assert started["data"]["status"] == "in_progress"

    fetched = api_instance.get_attempt("at1")
    assert fetched["status"] == 200

    submitted = api_instance.submit_attempt("at1")
    assert submitted["status"] == 200
    assert submitted["data"]["status"] == "submitted"
    assert api_instance.score_attempt("at1") == {
        "status": 200,
        "data": {"attempt_id": "at1", "score": 2},
    }


def test_api_maps_missing_and_invalid_attempts():
    api_instance = api()
    assert api_instance.get_assessment("missing")["status"] == 404
    assert api_instance.get_attempt("missing")["status"] == 404

    publish(api_instance)
    assert api_instance.start_attempt(
        AssessmentAttempt("at1", "a1", "learner-1")
    )["status"] == 201
    assert api_instance.submit_attempt("at1")["status"] == 200
    assert api_instance.submit_attempt("at1")["status"] == 409
    assert api_instance.score_attempt("missing")["status"] == 404
