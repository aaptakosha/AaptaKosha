import sqlite3
from pathlib import Path

from aaptakosha_core.catalog import Curriculum, Subject, Topic
from aaptakosha_core.sqlite_repository import SQLiteCatalogRepository


MIGRATION = Path(__file__).parents[1] / "migrations" / "001_catalog.sql"


def sample_curriculum(version="2026.1"):
    return Curriculum(
        curriculum_id="bams-ug",
        version=version,
        professional_year=2,
        subjects=(
            Subject(
                "dravyaguna",
                "Dravyaguna Vigyan",
                (Topic("dg-001", "Rasa"), Topic("dg-002", "Virya")),
            ),
            Subject("swasthavritta", "Swasthavritta", (Topic("sv-001", "Dinacharya"),)),
        ),
    )


def repository():
    connection = sqlite3.connect(":memory:")
    repo = SQLiteCatalogRepository(connection)
    repo.apply_migrations(MIGRATION)
    return repo


def test_round_trip_curriculum_subjects_and_topics():
    repo = repository()
    curriculum = sample_curriculum()
    repo.seed_curriculum(curriculum)

    assert repo.get_curriculum("bams-ug") == curriculum
    assert repo.list_subjects("bams-ug") == curriculum.subjects
    assert repo.get_subject("bams-ug", "dravyaguna") == curriculum.subjects[0]


def test_multiple_versions_are_readable_and_latest_is_deterministic():
    repo = repository()
    older = sample_curriculum("2026.0")
    newer = sample_curriculum("2026.1")
    repo.seed_curriculum(older)
    repo.seed_curriculum(newer)

    assert repo.get_curriculum("bams-ug").version == "2026.1"
    assert repo.get_curriculum("bams-ug", "2026.0") == older


def test_missing_curriculum_and_subject_return_none():
    repo = repository()

    assert repo.get_curriculum("missing") is None
    assert repo.list_subjects("missing") == ()
    assert repo.get_subject("missing", "subject") is None


def test_foreign_keys_and_duplicate_snapshot_are_enforced():
    repo = repository()
    repo.seed_curriculum(sample_curriculum())

    try:
        repo.connection.execute(
            "INSERT INTO subjects(curriculum_id, curriculum_version, subject_id, name) "
            "VALUES ('bams-ug', 'missing', 'x', 'X')"
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("foreign key constraint was not enforced")

    try:
        repo.seed_curriculum(sample_curriculum())
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("duplicate curriculum version was not rejected")
