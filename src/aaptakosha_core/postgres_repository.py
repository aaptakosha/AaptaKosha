"""PostgreSQL persistence adapters for durable learner data.

The adapters mirror the SQLite repositories so local development can continue
without a managed database while deployed environments use durable Postgres.
"""

from __future__ import annotations

import json
from typing import Any, Tuple

from psycopg import Connection

from .assessment import Assessment, AssessmentAttempt, AssessmentQuestion, QuestionOption
from .progress import LearningProgress, LearningProgressRepository


class PostgresAssessmentRepository:
    """PostgreSQL adapter for assessments and learner attempts."""

    def __init__(self, connection: Connection[Any]):
        self.connection = connection

    def apply_migrations(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
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
                    assessment_id TEXT NOT NULL REFERENCES assessments(assessment_id),
                    learner_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    answers_json TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_assessment_attempts_learner
                    ON assessment_attempts(learner_id, attempt_id);
                """
            )
        self.connection.commit()

    def get(self, resource_id: str) -> Assessment | AssessmentAttempt | None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT assessment_id, title, status, curriculum_refs_json, questions_json
                FROM assessments WHERE assessment_id = %s
                """,
                (resource_id,),
            )
            row = cursor.fetchone()
            if row:
                return self._assessment_from_row(row)
            cursor.execute(
                """
                SELECT attempt_id, assessment_id, learner_id, status, answers_json
                FROM assessment_attempts WHERE attempt_id = %s
                """,
                (resource_id,),
            )
            row = cursor.fetchone()
        return self._attempt_from_row(row) if row else None

    def list(self, status: str | None = None) -> Tuple[Assessment, ...]:
        query = (
            "SELECT assessment_id, title, status, curriculum_refs_json, questions_json "
            "FROM assessments"
        )
        params: tuple[Any, ...] = ()
        if status is not None:
            query += " WHERE status = %s"
            params = (status,)
        query += " ORDER BY assessment_id"
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
        return tuple(self._assessment_from_row(row) for row in rows)

    def save(self, entity: Assessment | AssessmentAttempt) -> Assessment | AssessmentAttempt:
        if isinstance(entity, Assessment):
            questions = [
                {
                    "question_id": q.question_id,
                    "prompt": q.prompt,
                    "points": q.points,
                    "options": [
                        {
                            "option_id": o.option_id,
                            "text": o.text,
                            "is_correct": o.is_correct,
                        }
                        for o in q.options
                    ],
                }
                for q in entity.questions
            ]
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO assessments
                        (assessment_id, title, status, curriculum_refs_json, questions_json)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (assessment_id) DO UPDATE SET
                        title=EXCLUDED.title,
                        status=EXCLUDED.status,
                        curriculum_refs_json=EXCLUDED.curriculum_refs_json,
                        questions_json=EXCLUDED.questions_json
                    """,
                    (
                        entity.assessment_id,
                        entity.title,
                        entity.status,
                        json.dumps(list(entity.curriculum_refs)),
                        json.dumps(questions),
                    ),
                )
        elif isinstance(entity, AssessmentAttempt):
            answers = [
                {
                    "question_id": question_id,
                    "selected_option_ids": list(selected_option_ids),
                }
                for question_id, selected_option_ids in entity.answers
            ]
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO assessment_attempts
                        (attempt_id, assessment_id, learner_id, status, answers_json)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (attempt_id) DO UPDATE SET
                        assessment_id=EXCLUDED.assessment_id,
                        learner_id=EXCLUDED.learner_id,
                        status=EXCLUDED.status,
                        answers_json=EXCLUDED.answers_json
                    """,
                    (
                        entity.attempt_id,
                        entity.assessment_id,
                        entity.learner_id,
                        entity.status,
                        json.dumps(answers),
                    ),
                )
        else:
            raise TypeError("entity must be Assessment or AssessmentAttempt")
        self.connection.commit()
        return entity

    def list_for_learner(self, learner_id: str) -> Tuple[AssessmentAttempt, ...]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT attempt_id, assessment_id, learner_id, status, answers_json
                FROM assessment_attempts
                WHERE learner_id = %s
                ORDER BY attempt_id
                """,
                (learner_id,),
            )
            rows = cursor.fetchall()
        return tuple(self._attempt_from_row(row) for row in rows)

    @staticmethod
    def _assessment_from_row(row: tuple[Any, ...]) -> Assessment:
        return Assessment(
            assessment_id=row[0],
            title=row[1],
            status=row[2],
            curriculum_refs=tuple(json.loads(row[3])),
            questions=tuple(
                AssessmentQuestion(
                    question_id=item["question_id"],
                    prompt=item["prompt"],
                    points=item["points"],
                    options=tuple(
                        QuestionOption(o["option_id"], o["text"], o["is_correct"])
                        for o in item["options"]
                    ),
                )
                for item in json.loads(row[4])
            ),
        )

    @staticmethod
    def _attempt_from_row(row: tuple[Any, ...]) -> AssessmentAttempt:
        return AssessmentAttempt(
            attempt_id=row[0],
            assessment_id=row[1],
            learner_id=row[2],
            status=row[3],
            answers=tuple(
                (item["question_id"], tuple(item["selected_option_ids"]))
                for item in json.loads(row[4])
            ),
        )


class PostgresProgressRepository(LearningProgressRepository):
    """PostgreSQL adapter for durable learner progress snapshots."""

    def __init__(self, connection: Connection[Any]):
        self.connection = connection

    def apply_migrations(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
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
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT subject_id, resource_type, resource_id, status, completion_percent
                FROM learning_progress
                WHERE subject_id = %s AND resource_type = %s AND resource_id = %s
                """,
                (subject_id, resource_type, resource_id),
            )
            row = cursor.fetchone()
        return self._from_row(row) if row else None

    def list_for_subject(self, subject_id: str) -> Tuple[LearningProgress, ...]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT subject_id, resource_type, resource_id, status, completion_percent
                FROM learning_progress
                WHERE subject_id = %s
                ORDER BY resource_type, resource_id
                """,
                (subject_id,),
            )
            rows = cursor.fetchall()
        return tuple(self._from_row(row) for row in rows)

    def save(self, progress: LearningProgress) -> LearningProgress:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO learning_progress
                    (subject_id, resource_type, resource_id, status, completion_percent)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (subject_id, resource_type, resource_id) DO UPDATE SET
                    status=EXCLUDED.status,
                    completion_percent=EXCLUDED.completion_percent
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
    def _from_row(row: tuple[Any, ...]) -> LearningProgress:
        return LearningProgress(
            subject_id=row[0],
            resource_type=row[1],
            resource_id=row[2],
            status=row[3],
            completion_percent=row[4],
        )


__all__ = ["PostgresAssessmentRepository", "PostgresProgressRepository"]
