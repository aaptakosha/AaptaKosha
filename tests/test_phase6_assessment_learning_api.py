import sqlite3

from aaptakosha_core.assessment import Assessment, AssessmentQuestion, QuestionOption
from aaptakosha_core.assessment_learning_api import AssessmentLearningApi
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository
from aaptakosha_core.assessment_services import AssessmentService


def question(question_id, correct):
    return AssessmentQuestion(
        question_id,
        f"Question {question_id}",
        (
            QuestionOption("a", "First", is_correct=correct == "a"),
            QuestionOption("b", "Second", is_correct=correct == "b"),
        ),
        points=2,
    )


def setup():
    repo = SQLiteAssessmentRepository(sqlite3.connect(":memory:"))
    repo.apply_migrations()
    service = AssessmentService(repo, repo)
    service.create(Assessment(
        "a1", "Rachana Practice",
        status="draft",
        curriculum_refs=("subject:rachana",),
        questions=(question("q1", "a"), question("q2", "b")),
    ))
    service.publish("a1")
    return AssessmentLearningApi(service)


def test_practice_flow_starts_persists_submits_and_returns_results():
    api = setup()
    started = api.start("a1", "learner-1")
    assert started["status"] == 201
    attempt_id = started["data"]["attempt"]["attempt_id"]
    assert started["data"]["assessment"]["questions"][0]["options"] == [
        {"option_id": "a", "text": "First"},
        {"option_id": "b", "text": "Second"},
    ]
    assert "correct_option_ids" not in started["data"]["assessment"]["questions"][0]

    saved = api.save_answers(
        attempt_id,
        "learner-1",
        (("q1", ("a",)), ("q2", ("a",))),
    )
    assert saved["status"] == 200
    assert saved["data"]["answers"][0]["selected_option_ids"] == ["a"]

    submitted = api.submit(attempt_id, "learner-1")
    assert submitted["status"] == 200
    assert submitted["data"]["score"] == 2
    assert submitted["data"]["maximum_score"] == 4
    assert submitted["data"]["percent"] == 50
    assert submitted["data"]["breakdown"][0]["is_correct"] is True
    assert submitted["data"]["breakdown"][1]["is_correct"] is False
    assert submitted["data"]["analytics"]["submitted_attempt_count"] == 1


def test_assessment_list_can_be_scoped_to_curriculum_reference():
    api = setup()
    assert [x["assessment_id"] for x in api.list_assessments("subject:rachana")["data"]["assessments"]] == ["a1"]
    assert api.list_assessments("subject:dravyaguna")["data"]["assessments"] == []


def test_answer_save_and_results_are_learner_scoped():
    api = setup()
    started = api.start("a1", "learner-1")
    attempt_id = started["data"]["attempt"]["attempt_id"]
    assert api.save_answers(attempt_id, "learner-2", (("q1", ("a",)),))["status"] == 404
    assert api.result(attempt_id, "learner-2")["status"] == 404
    assert api.submit(attempt_id, "learner-1")["status"] == 200


def test_results_are_not_available_before_submission():
    api = setup()
    started = api.start("a1", "learner-1")
    attempt_id = started["data"]["attempt"]["attempt_id"]
    assert api.result(attempt_id, "learner-1")["status"] == 409
