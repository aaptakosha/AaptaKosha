import pytest

from aaptakosha_core.content import ARCHIVED, DRAFT, PUBLISHED, REVIEW, ContentProvenance, ContentResource
from aaptakosha_core.content_repository import SQLiteContentRepository
from aaptakosha_core.content_services import ContentService, ContentTransitionError
import sqlite3


def service():
    repo = SQLiteContentRepository(sqlite3.connect(":memory:"))
    repo.apply_migrations()
    return ContentService(repo)


def resource(**kwargs):
    return ContentResource(
        resource_id="r-1", resource_type="article", title="Title", **kwargs
    )


def test_content_lifecycle_requires_explicit_transitions():
    svc = service()
    svc.create(resource())
    assert svc.get("r-1").status == DRAFT
    assert svc.submit_for_review("r-1").status == REVIEW
    with pytest.raises(ContentTransitionError):
        svc.publish("r-1")


def test_publish_requires_provenance_and_curriculum_reference():
    svc = service()
    svc.create(resource())
    svc.submit_for_review("r-1")
    with pytest.raises(ContentTransitionError):
        svc.publish("r-1")


def test_publish_and_archive_are_governed():
    svc = service()
    svc.create(resource(
        provenance=(ContentProvenance("NCISM", "official"),),
        curriculum_refs=("topic:dinacharya",),
    ))
    assert svc.submit_for_review("r-1").status == REVIEW
    assert svc.publish("r-1").status == PUBLISHED
    assert svc.archive("r-1").status == ARCHIVED


def test_invalid_transition_is_rejected():
    svc = service()
    svc.create(resource())
    with pytest.raises(ContentTransitionError):
        svc.archive("r-1")
