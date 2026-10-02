import json, sqlite3, threading, urllib.request
from http.server import ThreadingHTTPServer
from aaptakosha_core.assessment import Assessment, AssessmentQuestion, QuestionOption
from aaptakosha_core.assessment_http_api import AssessmentHttpApi
from aaptakosha_core.assessment_learning_api import AssessmentLearningApi
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository
from aaptakosha_core.assessment_services import AssessmentService
from aaptakosha_core.http_server import AaptaKoshaRequestHandler

def make_server():
    repo=SQLiteAssessmentRepository(sqlite3.connect(":memory:",check_same_thread=False)); repo.apply_migrations()
    service=AssessmentService(repo,repo)
    service.create(Assessment("a1","Rachana Practice",status="draft",questions=(AssessmentQuestion("q1","Which?",(QuestionOption("a","First",is_correct=True),QuestionOption("b","Second")),points=2),)))
    service.publish("a1")
    handler=type("TestHandler",(AaptaKoshaRequestHandler,),{"api":AssessmentHttpApi(AssessmentLearningApi(service))})
    srv=ThreadingHTTPServer(("127.0.0.1",0),handler); threading.Thread(target=srv.serve_forever,daemon=True).start(); return srv

def test_real_http_endpoint():
    srv=make_server()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{srv.server_port}/assessments") as r:
            data=json.load(r)
        assert r.status==200 and data["data"]["assessments"][0]["assessment_id"]=="a1"
    finally: srv.shutdown(); srv.server_close()

def test_cors_preflight():
    srv=make_server()
    try:
        req=urllib.request.Request(f"http://127.0.0.1:{srv.server_port}/assessments",method="OPTIONS")
        with urllib.request.urlopen(req) as r: assert r.status==204 and r.headers["Access-Control-Allow-Origin"]=="*"
    finally: srv.shutdown(); srv.server_close()
