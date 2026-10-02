import pytest

from aaptakosha_core.progress import (
    COMPLETED,
    IN_PROGRESS,
    LearningProgress,
    LearningProgressService,
    NOT_STARTED,
)


class InMemoryProgress:
    def __init__(self):
        self.items = {}

    def get(self, subject_id, resource_type, resource_id):
        return self.items.get((subject_id, resource_type, resource_id))

    def list_for_subject(self, subject_id):
        return tuple(
            progress for progress in self.items.values()
            if progress.subject_id == subject_id
        )

    def save(self, progress):
        self.items[(progress.subject_id, progress.resource_type, progress.resource_id)] = progress
        return progress


def test_progress_contract_supports_partial_learning():
    progress = LearningProgress("user-1", "topic", "dg-1", IN_PROGRESS, 40)
    assert progress.completion_percent == 40


def test_progress_contract_enforces_status_invariants():
    with pytest.raises(ValueError):
        LearningProgress("user-1", "topic", "dg-1", NOT_STARTED, 20)
    with pytest.raises(ValueError):
        LearningProgress("user-1", "topic", "dg-1", COMPLETED, 80)
    with pytest.raises(ValueError):
        LearningProgress("user-1", "topic", "dg-1", "paused", 50)


def test_service_records_and_reads_progress():
    service = LearningProgressService(InMemoryProgress())
    saved = service.record(
        "user-1", "topic", "dg-1", status=IN_PROGRESS, completion_percent=60
    )
    assert service.get("user-1", "topic", "dg-1") == saved
    assert service.list_for_subject("user-1") == (saved,)


def test_service_rejects_blank_subject_id():
    with pytest.raises(ValueError):
        LearningProgressService(InMemoryProgress()).list_for_subject(" ")
