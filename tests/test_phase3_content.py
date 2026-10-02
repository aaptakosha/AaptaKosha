import pytest

from aaptakosha_core.content import (
    DRAFT,
    PUBLISHED,
    ContentProvenance,
    ContentResource,
)


def test_content_resource_is_immutable_and_domain_neutral():
    resource = ContentResource(
        "r-1",
        "article",
        "Dinacharya",
        status=DRAFT,
        provenance=(ContentProvenance("NCISM", "official-source"),),
        curriculum_refs=("subject:svt", "topic:dinacharya"),
    )

    assert resource.resource_type == "article"
    assert resource.curriculum_refs == ("subject:svt", "topic:dinacharya")


def test_content_rejects_invalid_status():
    with pytest.raises(ValueError):
        ContentResource("r-1", "note", "Title", status="unknown")


def test_content_rejects_duplicate_curriculum_refs():
    with pytest.raises(ValueError):
        ContentResource(
            "r-1",
            "note",
            "Title",
            curriculum_refs=("topic:x", "topic:x"),
        )


def test_provenance_requires_source():
    with pytest.raises(ValueError):
        ContentProvenance("")


def test_published_is_a_supported_lifecycle_state():
    resource = ContentResource("r-1", "video", "Title", status=PUBLISHED)
    assert resource.status == PUBLISHED
