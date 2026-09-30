import sqlite3
import pytest

from aaptakosha_core.content import ContentResource
from aaptakosha_core.content_repository import SQLiteContentRepository
from aaptakosha_core.content_links import CurriculumContentLinkService
from aaptakosha_core.content_link_repository import SQLiteCurriculumContentLinkRepository

def services():
    conn = sqlite3.connect(":memory:")
    content = SQLiteContentRepository(conn)
    content.apply_migrations()
    links = SQLiteCurriculumContentLinkRepository(conn)
    links.apply_migrations()
    return content, CurriculumContentLinkService(links, content)

def test_curriculum_content_links_are_separate_and_deterministic():
    content, svc = services()
    content.save(ContentResource("r-1", "article", "One"))
    content.save(ContentResource("r-2", "article", "Two"))
    svc.link("subject:svt", "r-2")
    svc.link("subject:svt", "r-1", "explains")
    assert [x.resource_id for x in svc.for_curriculum("subject:svt")] == ["r-1", "r-2"]
    assert svc.for_resource("r-1")[0].curriculum_ref == "subject:svt"

def test_link_requires_existing_content():
    _, svc = services()
    with pytest.raises(LookupError):
        svc.link("subject:svt", "missing")

def test_duplicate_link_is_idempotent():
    content, svc = services()
    content.save(ContentResource("r-1", "article", "One"))
    first = svc.link("subject:svt", "r-1")
    second = svc.link("subject:svt", "r-1")
    assert first == second
    assert svc.for_resource("r-1") == (first,)


def test_database_link_integrity_rejects_unknown_resource():
    conn = sqlite3.connect(":memory:")
    content = SQLiteContentRepository(conn)
    content.apply_migrations()
    links = SQLiteCurriculumContentLinkRepository(conn)
    links.apply_migrations()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO curriculum_content_links "
            "(curriculum_ref, resource_id, relationship) VALUES (?, ?, ?)",
            ("subject:svt", "missing", "supports"),
        )
