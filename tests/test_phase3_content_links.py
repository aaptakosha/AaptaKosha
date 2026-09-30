import sqlite3
from aaptakosha_core.content_links import CurriculumContentLinkService
from aaptakosha_core.content_link_repository import SQLiteCurriculumContentLinkRepository

def test_curriculum_content_links_are_separate_and_deterministic():
    repo=SQLiteCurriculumContentLinkRepository(sqlite3.connect(":memory:")); repo.apply_migrations(); svc=CurriculumContentLinkService(repo)
    svc.link("subject:svt","r-2"); svc.link("subject:svt","r-1","explains")
    assert [x.resource_id for x in svc.for_curriculum("subject:svt")] == ["r-1","r-2"]
    assert svc.for_resource("r-1")[0].curriculum_ref == "subject:svt"
