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
