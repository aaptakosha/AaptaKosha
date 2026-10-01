from __future__ import annotations

from typing import Any

from aaptakosha_core.assessment import Assessment, AssessmentQuestion, QuestionOption
from aaptakosha_core.postgres_repository import (
    PostgresAssessmentRepository,
    PostgresProgressRepository,
)
from aaptakosha_core.progress import COMPLETED, LearningProgress


class FakeCursor:
    def __init__(self, connection):
        self.connection = connection
        self.row = None
        self.rows = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def execute(self, sql, params=()):
        self.connection.statements.append((sql, params))
        if sql.lstrip().upper().startswith("SELECT"):
            if "FROM assessments" in sql:
                self.row = self.connection.assessment_row
                self.rows = [self.row] if self.row else []
            elif "FROM learning_progress" in sql:
                self.row = self.connection.progress_row
                self.rows = [self.row] if self.row else []
            else:
                self.row = None
                self.rows = []
        return self

    def fetchone(self):
        return self.row

    def fetchall(self):
        return self.rows


class FakeConnection:
    def __init__(self):
        self.statements: list[tuple[str, Any]] = []
        self.assessment_row = None
        self.progress_row = None

    def cursor(self):
        return FakeCursor(self)

    def commit(self):
        self.committed = True


def test_postgres_assessment_repository_creates_schema_and_round_trips_definition():
    connection = FakeConnection()
    repository = PostgresAssessmentRepository(connection)
    repository.apply_migrations()

    assessment = Assessment(
        "a1",
        "Demo",
        curriculum_refs=("subject:dravyaguna",),
        questions=(
            AssessmentQuestion(
                "q1",
                "Prompt",
                (QuestionOption("a", "Wrong"), QuestionOption("b", "Right", is_correct=True)),
            ),
        ),
    )
    repository.save(assessment)

    assert any("CREATE TABLE IF NOT EXISTS assessments" in sql for sql, _ in connection.statements)
    assert any("INSERT INTO assessments" in sql for sql, _ in connection.statements)

    connection.assessment_row = (
        assessment.assessment_id,
        assessment.title,
        assessment.status,
        '["subject:dravyaguna"]',
        '[{"question_id":"q1","prompt":"Prompt","points":1,"options":[{"option_id":"a","text":"Wrong","is_correct":false},{"option_id":"b","text":"Right","is_correct":true}]}]',
    )
    assert repository.get("a1") == assessment


def test_postgres_progress_repository_uses_parameterized_upsert():
    connection = FakeConnection()
    repository = PostgresProgressRepository(connection)
    repository.apply_migrations()

    progress = LearningProgress("dravyaguna", "topic", "dg-1", COMPLETED, 100)
    repository.save(progress)

    assert any("ON CONFLICT (subject_id, resource_type, resource_id)" in sql for sql, _ in connection.statements)
    assert connection.statements[-1][1] == (
        "dravyaguna",
        "topic",
        "dg-1",
        COMPLETED,
        100,
    )

    connection.progress_row = ("dravyaguna", "topic", "dg-1", COMPLETED, 100)
    assert repository.get("dravyaguna", "topic", "dg-1") == progress
