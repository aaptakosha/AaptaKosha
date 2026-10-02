import sqlite3

from aaptakosha_core.assessment import Assessment, AssessmentQuestion, QuestionOption
from aaptakosha_core.assessment_learning_api import AssessmentLearningApi
from aaptakosha_core.assessment_http_api import AssessmentHttpApi
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository
from aaptakosha_core.assessment_services import AssessmentService
from aaptakosha_core.auth import Principal
from aaptakosha_core.progress import IN_PROGRESS, LearningProgressService
from aaptakosha_core.progress_http_api import ProgressHttpApi
from aaptakosha_core.progress_repository import SQLiteProgressRepository


def assessment_api(require_identity=True):
    repo = SQLiteAssessmentRepository(sqlite3.connect(":memory:"))
    repo.apply_migrations()
    service = AssessmentService(repo, repo)
    service.create(Assessment(
        "a1", "Practice", status="draft",
        questions=(AssessmentQuestion(
            "q1", "Which?", (QuestionOption("a", "First", is_correct=True),),
        ),),
    ))
    service.publish("a1")
    return AssessmentHttpApi(AssessmentLearningApi(service), require_identity=require_identity)


def progress_api(require_identity=True):
    repo = SQLiteProgressRepository(sqlite3.connect(":memory:"))
    repo.apply_migrations()
    return ProgressHttpApi(LearningProgressService(repo), require_identity=require_identity)


def test_protected_assessment_requires_identity():
    result = assessment_api().handle("POST", "/assessments/a1/attempts", {"learner_id": "l1"})
    assert result["status"] == 401


def test_assessment_identity_is_bound_to_attempt_owner():
    api = assessment_api()
    principal = Principal("l1")
    started = api.handle("POST", "/assessments/a1/attempts", {}, principal=principal)
    assert started["status"] == 201
    attempt_id = started["data"]["attempt"]["attempt_id"]
    mismatch = api.handle("PUT", f"/attempts/{attempt_id}/answers",
                           {"learner_id": "l2", "answers":[]}, principal=principal)
    assert mismatch["status"] == 403


def test_progress_identity_is_bound_to_subject():
    api = progress_api()
    principal = Principal("l1")
    saved = api.handle("POST", "/progress", {
        "subject_id": "l1", "resource_type": "topic", "resource_id": "dg-1",
        "status": IN_PROGRESS, "completion_percent": 40,
    }, principal=principal)
    assert saved["status"] == 200
    listed = api.handle("GET", "/progress", {}, {}, principal=principal)
    assert listed["status"] == 200
    assert listed["progress"][0]["subject_id"] == "l1"
    mismatch = api.handle("POST", "/progress", {
        "subject_id": "l2", "resource_type": "topic", "resource_id": "dg-2",
        "status": IN_PROGRESS, "completion_percent": 10,
    }, principal=principal)
    assert mismatch["status"] == 403


def test_progress_path_identity_is_bound_to_subject():
    api = progress_api()
    principal = Principal("l1")
    mismatch = api.handle("GET", "/progress/l2/topic/dg-2", {}, {}, principal=principal)
    assert mismatch["status"] == 403


def test_progress_invalid_payload_is_client_error():
    api = progress_api(require_identity=False)
    result = api.handle("POST", "/progress", {"subject_id": "l1"})
    assert result["status"] == 400


def test_legacy_local_mode_remains_available():
    api = assessment_api(require_identity=False)
    result = api.handle("POST", "/assessments/a1/attempts", {"learner_id": "l1"})
    assert result["status"] == 201
