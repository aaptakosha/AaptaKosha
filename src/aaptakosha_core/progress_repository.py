"""SQLite persistence adapter for learner progress snapshots.

Progress is intentionally stored separately from curriculum/content so UI data
can evolve without changing the authoritative NCISM catalog.
"""

from __future__ import annotations

import sqlite3
from typing import Tuple

from .progress import LearningProgress, LearningProgressRepository


class SQLiteProgressRepository(LearningProgressRepository):
    """Persistent implementation of the domain-neutral progress boundary."""

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.connection.execute("PRAGMA foreign_keys = ON")

    def apply_migrations(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS learning_progress (
                subject_id TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                resource_id TEXT NOT NULL,
                status TEXT NOT NULL,
                completion_percent INTEGER NOT NULL,
                PRIMARY KEY (subject_id, resource_type, resource_id)
            );
            CREATE INDEX IF NOT EXISTS idx_learning_progress_subject
                ON learning_progress(subject_id);
            """
        )
        self.connection.commit()

    def get(
        self, subject_id: str, resource_type: str, resource_id: str
    ) -> LearningProgress | None:
        row = self.connection.execute(
            """
            SELECT subject_id, resource_type, resource_id, status, completion_percent
            FROM learning_progress
            WHERE subject_id = ? AND resource_type = ? AND resource_id = ?
            """,
            (subject_id, resource_type, resource_id),
        ).fetchone()
        return self._from_row(row) if row else None

    def list_for_subject(self, subject_id: str) -> Tuple[LearningProgress, ...]:
        rows = self.connection.execute(
            """
            SELECT subject_id, resource_type, resource_id, status, completion_percent
            FROM learning_progress
            WHERE subject_id = ?
            ORDER BY resource_type, resource_id
            """,
            (subject_id,),
        ).fetchall()
        return tuple(self._from_row(row) for row in rows)

    def save(self, progress: LearningProgress) -> LearningProgress:
        self.connection.execute(
            """
            INSERT INTO learning_progress (
                subject_id, resource_type, resource_id, status, completion_percent
            ) VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(subject_id, resource_type, resource_id) DO UPDATE SET
                status=excluded.status,
                completion_percent=excluded.completion_percent
            """,
            (
                progress.subject_id,
                progress.resource_type,
                progress.resource_id,
                progress.status,
                progress.completion_percent,
            ),
        )
        self.connection.commit()
        return progress

    @staticmethod
    def _from_row(row) -> LearningProgress:
        return LearningProgress(
            subject_id=row[0],
            resource_type=row[1],
            resource_id=row[2],
            status=row[3],
            completion_percent=row[4],
        )


__all__ = ["SQLiteProgressRepository"]
