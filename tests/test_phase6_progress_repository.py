import sqlite3

import pytest

from aaptakosha_core.progress import COMPLETED, IN_PROGRESS, NOT_STARTED, LearningProgress
from aaptakosha_core.progress_repository import SQLiteProgressRepository


def repo():
    repository = SQLiteProgressRepository(sqlite3.connect(":memory:"))
    repository.apply_migrations()
    return repository


def test_progress_round_trip_and_subject_listing():
    repository = repo()
    first = LearningProgress("dravyaguna", "topic", "dg-1", IN_PROGRESS, 40)
    second = LearningProgress("dravyaguna", "topic", "dg-2", COMPLETED, 100)
    repository.save(first)
    repository.save(second)

    assert repository.get("dravyaguna", "topic", "dg-1") == first
    assert repository.list_for_subject("dravyaguna") == (first, second)


def test_progress_upsert_keeps_one_snapshot_per_resource():
    repository = repo()
    first = LearningProgress("dravyaguna", "topic", "dg-1", IN_PROGRESS, 40)
    updated = LearningProgress("dravyaguna", "topic", "dg-1", COMPLETED, 100)

    repository.save(first)
    repository.save(updated)

    assert repository.get("dravyaguna", "topic", "dg-1") == updated
    assert repository.list_for_subject("dravyaguna") == (updated,)


def test_progress_domain_validation_is_preserved():
    repository = repo()
    with pytest.raises(ValueError):
        repository.save(LearningProgress("dravyaguna", "topic", "dg-1", NOT_STARTED, 20))
