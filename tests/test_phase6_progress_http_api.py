import sqlite3

from aaptakosha_core.progress import COMPLETED, IN_PROGRESS, LearningProgressService
from aaptakosha_core.progress_http_api import ProgressHttpApi
from aaptakosha_core.progress_repository import SQLiteProgressRepository


def api():
    repository = SQLiteProgressRepository(sqlite3.connect(":memory:"))
    repository.apply_migrations()
    return ProgressHttpApi(LearningProgressService(repository))


def test_progress_can_be_recorded_and_listed():
    service = api()
    saved = service.handle("POST", "/progress", {
        "subject_id": "dravyaguna", "resource_type": "topic", "resource_id": "dg-1",
        "status": IN_PROGRESS, "completion_percent": 40,
    })
    assert saved["status"] == 200
    assert saved["progress"]["completion_percent"] == 40

    listed = service.handle("GET", "/progress", query={"subject_id": "dravyaguna"})
    assert listed["status"] == 200
    assert listed["progress"][0]["resource_id"] == "dg-1"


def test_progress_get_and_validation():
    service = api()
    assert service.handle("GET", "/progress/dravyaguna/topic/dg-1")["status"] == 404
    invalid = service.handle("POST", "/progress", {
        "subject_id": "dravyaguna", "resource_type": "topic", "resource_id": "dg-1",
        "status": COMPLETED, "completion_percent": 40,
    })
    assert invalid["status"] == 400


def test_progress_upsert():
    service = api()
    first = {
        "subject_id": "dravyaguna", "resource_type": "topic", "resource_id": "dg-1",
        "status": IN_PROGRESS, "completion_percent": 40,
    }
    updated = {**first, "status": COMPLETED, "completion_percent": 100}
    assert service.handle("POST", "/progress", first)["status"] == 200
    assert service.handle("PUT", "/progress", updated)["status"] == 200
    result = service.handle("GET", "/progress/dravyaguna/topic/dg-1")
    assert result["progress"]["status"] == COMPLETED
    assert result["progress"]["completion_percent"] == 100
