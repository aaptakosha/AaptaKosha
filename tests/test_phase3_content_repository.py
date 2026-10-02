import sqlite3

from aaptakosha_core.content import ContentProvenance, ContentResource
from aaptakosha_core.content_repository import SQLiteContentRepository


def test_content_repository_round_trip_and_status_filter():
    repo = SQLiteContentRepository(sqlite3.connect(":memory:"))
    repo.apply_migrations()
    resource = ContentResource(
        "r-1",
        "article",
        "Title",
        summary="Summary",
        provenance=(ContentProvenance("NCISM", "locator", "author"),),
        curriculum_refs=("subject:s1",),
    )

    repo.save(resource)

    assert repo.get("r-1") == resource
    assert repo.list() == (resource,)
    assert repo.list("published") == ()


def test_content_repository_upserts_resource():
    repo = SQLiteContentRepository(sqlite3.connect(":memory:"))
    repo.apply_migrations()
    repo.save(ContentResource("r-1", "note", "First"))
    updated = ContentResource("r-1", "article", "Second", status="review")

    repo.save(updated)

    assert repo.get("r-1") == updated
