import sqlite3
from aaptakosha_core.catalog import Curriculum, Subject, Topic
from aaptakosha_core.services import CatalogService
from aaptakosha_core.sqlite_repository import SQLiteCatalogRepository
from aaptakosha_core.learning_api import LearningCatalogApi

def test_learning_catalog_api_maps_real_catalog_contracts(tmp_path):
    connection=sqlite3.connect(":memory:")
    repo=SQLiteCatalogRepository(connection)
    repo.apply_migrations("migrations/001_catalog.sql")
    repo.seed_curriculum(Curriculum("ncism-bams","2026",2,(Subject("dravyaguna","Dravyaguna",(Topic("dg-1","Guna"),)),)))
    api=LearningCatalogApi(CatalogService(repo), None, None)
    result=api.subjects("ncism-bams","2026")
    assert result["status"] == 200
    assert result["data"]["subjects"][0]["subject_id"] == "dravyaguna"
    assert result["data"]["subjects"][0]["topics"][0]["topic_id"] == "dg-1"
