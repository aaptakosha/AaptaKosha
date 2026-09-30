import sqlite3
from aaptakosha_core.assessment import Assessment, AssessmentQuestion, QuestionOption
from aaptakosha_core.assessment_learning_api import AssessmentLearningApi
from aaptakosha_core.assessment_http_api import AssessmentHttpApi
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository
from aaptakosha_core.assessment_services import AssessmentService

def api():
    repo=SQLiteAssessmentRepository(sqlite3.connect(":memory:")); repo.apply_migrations()
    service=AssessmentService(repo,repo)
    service.create(Assessment("a1","Rachana Practice",status="draft",curriculum_refs=("subject:rachana",),questions=(
        AssessmentQuestion("q1","Which?",(QuestionOption("a","First",is_correct=True),QuestionOption("b","Second")),points=2),)))
    service.publish("a1")
    return AssessmentHttpApi(AssessmentLearningApi(service))

def test_http_assessment_lifecycle():
    h=api()
    listed=h.handle("GET","/assessments",query={"curriculum_ref":"subject:rachana"})
    assert listed["status"]==200 and listed["data"]["assessments"][0]["assessment_id"]=="a1"
    started=h.handle("POST","/assessments/a1/attempts",{"learner_id":"l1"})
    assert started["status"]==201
    attempt=started["data"]["attempt"]["attempt_id"]
    saved=h.handle("PUT",f"/attempts/{attempt}/answers",{"learner_id":"l1","answers":[{"question_id":"q1","selected_option_ids":["a"]}]})
    assert saved["status"]==200
    submitted=h.handle("POST",f"/attempts/{attempt}/submit",{"learner_id":"l1"})
    assert submitted["status"]==200 and submitted["data"]["score"]==2

def test_http_json_and_route_errors():
    h=api()
    status,payload=h.json_response(h.handle("GET","/missing"))
    assert status==404 and '"route_not_found"' in payload
