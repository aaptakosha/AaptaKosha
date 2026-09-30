"""Persistence boundary for Phase 4 assessments and learner attempts."""

from __future__ import annotations

import json
import sqlite3
from typing import Protocol, Tuple

from .assessment import Assessment, AssessmentAttempt, AssessmentQuestion, QuestionOption


class AssessmentRepository(Protocol):
    def get(self, assessment_id: str) -> Assessment | None: ...
    def list(self, status: str | None = None) -> Tuple[Assessment, ...]: ...
    def save(self, assessment: Assessment) -> Assessment: ...


class AssessmentAttemptRepository(Protocol):
    def get(self, attempt_id: str) -> AssessmentAttempt | None: ...
    def list_for_learner(self, learner_id: str) -> Tuple[AssessmentAttempt, ...]: ...
    def save(self, attempt: AssessmentAttempt) -> AssessmentAttempt: ...


class SQLiteAssessmentRepository:
    """SQLite adapter for assessment definitions and learner attempts."""

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.connection.execute("PRAGMA foreign_keys = ON")

    def apply_migrations(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS assessments (
                assessment_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                status TEXT NOT NULL,
                curriculum_refs_json TEXT NOT NULL,
                questions_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS assessment_attempts (
                attempt_id TEXT PRIMARY KEY,
                assessment_id TEXT NOT NULL,
                learner_id TEXT NOT NULL,
                status TEXT NOT NULL,
                answers_json TEXT NOT NULL,
                FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
            );
            CREATE INDEX IF NOT EXISTS idx_assessment_attempts_learner
                ON assessment_attempts(learner_id, attempt_id);
            """
        )
        self.connection.commit()

    def get(self, assessment_id: str) -> Assessment | None:
        row = self.connection.execute(
            "SELECT assessment_id, title, status, curriculum_refs_json, questions_json "
            "FROM assessments WHERE assessment_id = ?", (assessment_id,)
        ).fetchone()
        return self._assessment_from_row(row) if row else None

    def list(self, status: str | None = None) -> Tuple[Assessment, ...]:
        sql = ("SELECT assessment_id, title, status, curriculum_refs_json, questions_json "
               "FROM assessments")
        params = ()
        if status is not None:
            sql += " WHERE status = ?"
            params = (status,)
        rows = self.connection.execute(sql + " ORDER BY assessment_id", params).fetchall()
        return tuple(self._assessment_from_row(row) for row in rows)

    def save(self, assessment: Assessment) -> Assessment:
        self.connection.execute(
            """
            INSERT INTO assessments
                (assessment_id, title, status, curriculum_refs_json, questions_json)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(assessment_id) DO UPDATE SET
                title=excluded.title, status=excluded.status,
                curriculum_refs_json=excluded.curriculum_refs_json,
                questions_json=excluded.questions_json
            """,
            (assessment.assessment_id, assessment.title, assessment.status,
             json.dumps(list(assessment.curriculum_refs)),
             json.dumps([
                 {"question_id": q.question_id, "prompt": q.prompt, "points": q.points,
                  "options": [{"option_id": o.option_id, "text": o.text, "is_correct": o.is_correct}
                              for o in q.options]}
                 for q in assessment.questions
             ])),
        )
        self.connection.commit()
        return assessment

    def get(self, attempt_id: str) -> AssessmentAttempt | None:
        row = self.connection.execute(
            "SELECT attempt_id, assessment_id, learner_id, status, answers_json "
            "FROM assessment_attempts WHERE attempt_id = ?", (attempt_id,)
        ).fetchone()
        return self._attempt_from_row(row) if row else None

    def list_for_learner(self, learner_id: str) -> Tuple[AssessmentAttempt, ...]:
        rows = self.connection.execute(
            "SELECT attempt_id, assessment_id, learner_id, status, answers_json "
            "FROM assessment_attempts WHERE learner_id = ? ORDER BY attempt_id", (learner_id,)
        ).fetchall()
        return tuple(self._attempt_from_row(row) for row in rows)

    def save(self, attempt: AssessmentAttempt) -> AssessmentAttempt:
        self.connection.execute(
            """
            INSERT INTO assessment_attempts
                (attempt_id, assessment_id, learner_id, status, answers_json)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(attempt_id) DO UPDATE SET
                assessment_id=excluded.assessment_id, learner_id=excluded.learner_id,
                status=excluded.status, answers_json=excluded.answers_json
            """,
            (attempt.attempt_id, attempt.assessment_id, attempt.learner_id, attempt.status,
             json.dumps([{"question_id": q, "selected_option_ids": list(options)}
                         for q, options in attempt.answers])),
        )
        self.connection.commit()
        return attempt

    @staticmethod
    def _assessment_from_row(row) -> Assessment:
        return Assessment(
            assessment_id=row[0], title=row[1], status=row[2],
            curriculum_refs=tuple(json.loads(row[3])),
            questions=tuple(
                AssessmentQuestion(
                    question_id=item["question_id"], prompt=item["prompt"], points=item["points"],
                    options=tuple(QuestionOption(o["option_id"], o["text"], o["is_correct"])
                                  for o in item["options"]),
                ) for item in json.loads(row[4])
            ),
        )

    @staticmethod
    def _attempt_from_row(row) -> AssessmentAttempt:
        return AssessmentAttempt(
            attempt_id=row[0], assessment_id=row[1], learner_id=row[2], status=row[3],
            answers=tuple((item["question_id"], tuple(item["selected_option_ids"]))
                          for item in json.loads(row[4])),
        )


__all__ = ["AssessmentAttemptRepository", "AssessmentRepository", "SQLiteAssessmentRepository"]
