import sqlite3
from aaptakosha_core.content import ContentResource, ContentProvenance, REVIEW
from aaptakosha_core.content_repository import SQLiteContentRepository
from aaptakosha_core.content_services import ContentService
from aaptakosha_core.content_api import ContentApi

def test_content_api_serializes_resource_and_publishes():
    conn=sqlite3.connect(":memory:"); repo=SQLiteContentRepository(conn); repo.apply_migrations()
    service=ContentService(repo); service.create(ContentResource("r1","lesson","SVT",status=REVIEW,provenance=(ContentProvenance("NCISM"),),curriculum_refs=("subject:svt",)))
    api=ContentApi(service); assert api.get("r1")["status"]==200
    assert api.publish("r1")["data"]["status"]=="published"

def test_content_api_missing_resource_is_404():
    conn=sqlite3.connect(":memory:"); repo=SQLiteContentRepository(conn); repo.apply_migrations()
    assert ContentApi(ContentService(repo)).get("missing")["status"]==404
