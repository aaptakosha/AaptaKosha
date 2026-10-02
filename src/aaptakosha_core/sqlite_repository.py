"""SQLite reference adapter for the Phase 2 catalog repository boundary."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Tuple

from .catalog import Curriculum, CurriculumNode, Subject, Topic


class SQLiteCatalogRepository:
    """Read-oriented SQLite implementation of CatalogRepository.

    The adapter stores immutable published catalog snapshots. Application code
    should use CatalogService rather than mutating these tables directly.
    """

    def __init__(self, database: str | Path | sqlite3.Connection):
        if isinstance(database, sqlite3.Connection):
            self.connection = database
            self._owns_connection = False
        else:
            self.connection = sqlite3.connect(str(database))
            self._owns_connection = True
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")

    def close(self) -> None:
        if self._owns_connection:
            self.connection.close()

    def apply_migrations(self, migration_path: str | Path) -> None:
        sql = Path(migration_path).read_text(encoding="utf-8")
        with self.connection:
            self.connection.executescript(sql)

    def get_curriculum(self, curriculum_id: str, version: str | None = None) -> Curriculum | None:
        if version is None:
            row = self.connection.execute(
                "SELECT curriculum_id, version, professional_year "
                "FROM curricula WHERE curriculum_id = ? ORDER BY version DESC LIMIT 1",
                (curriculum_id,),
            ).fetchone()
        else:
            row = self.connection.execute(
                "SELECT curriculum_id, version, professional_year "
                "FROM curricula WHERE curriculum_id = ? AND version = ?",
                (curriculum_id, version),
            ).fetchone()
        if row is None:
            return None
        return Curriculum(
            curriculum_id=row["curriculum_id"],
            version=row["version"],
            professional_year=row["professional_year"],
            subjects=self.list_subjects(row["curriculum_id"], row["version"]),
        )

    def list_subjects(self, curriculum_id: str, version: str | None = None) -> Tuple[Subject, ...]:
        resolved_version = self._resolve_version(curriculum_id, version)
        if resolved_version is None:
            return ()
        rows = self.connection.execute(
            "SELECT subject_id, name FROM subjects "
            "WHERE curriculum_id = ? AND curriculum_version = ? "
            "ORDER BY subject_id",
            (curriculum_id, resolved_version),
        ).fetchall()
        return tuple(
            Subject(
                subject_id=row["subject_id"],
                name=row["name"],
                topics=self._list_topics(curriculum_id, resolved_version, row["subject_id"]),
            )
            for row in rows
        )

    def get_subject(
        self, curriculum_id: str, subject_id: str, version: str | None = None
    ) -> Subject | None:
        resolved_version = self._resolve_version(curriculum_id, version)
        if resolved_version is None:
            return None
        row = self.connection.execute(
            "SELECT subject_id, name FROM subjects "
            "WHERE curriculum_id = ? AND curriculum_version = ? AND subject_id = ?",
            (curriculum_id, resolved_version, subject_id),
        ).fetchone()
        if row is None:
            return None
        return Subject(
            subject_id=row["subject_id"],
            name=row["name"],
            topics=self._list_topics(curriculum_id, resolved_version, subject_id),
        )

    def _resolve_version(self, curriculum_id: str, version: str | None) -> str | None:
        if version is not None:
            row = self.connection.execute(
                "SELECT version FROM curricula WHERE curriculum_id = ? AND version = ?",
                (curriculum_id, version),
            ).fetchone()
        else:
            row = self.connection.execute(
                "SELECT version FROM curricula WHERE curriculum_id = ? "
                "ORDER BY version DESC LIMIT 1",
                (curriculum_id,),
            ).fetchone()
        return None if row is None else row["version"]

    def _list_topics(
        self, curriculum_id: str, version: str, subject_id: str
    ) -> Tuple[Topic, ...]:
        rows = self.connection.execute(
            "SELECT topic_id, name FROM topics "
            "WHERE curriculum_id = ? AND curriculum_version = ? AND subject_id = ? "
            "ORDER BY topic_id",
            (curriculum_id, version, subject_id),
        ).fetchall()
        return tuple(Topic(topic_id=row["topic_id"], name=row["name"]) for row in rows)

    def list_nodes(
        self,
        curriculum_id: str,
        subject_id: str | None = None,
        version: str | None = None,
        parent_node_id: str | None = None,
    ) -> Tuple["CurriculumNode", ...]:
        resolved_version = self._resolve_version(curriculum_id, version)
        if resolved_version is None:
            return ()
        clauses = ["curriculum_id = ?", "curriculum_version = ?"]
        params: list[object] = [curriculum_id, resolved_version]
        if subject_id is not None:
            clauses.append("subject_id = ?")
            params.append(subject_id)
        if parent_node_id is None:
            clauses.append("parent_node_id IS NULL")
        else:
            clauses.append("parent_node_id = ?")
            params.append(parent_node_id)
        rows = self.connection.execute(
            "SELECT node_id, name, node_type, parent_node_id, code "
            "FROM curriculum_nodes WHERE " + " AND ".join(clauses) +
            " ORDER BY sort_order, node_id",
            tuple(params),
        ).fetchall()
        return tuple(
            CurriculumNode(
                node_id=row["node_id"],
                name=row["name"],
                node_type=row["node_type"],
                parent_node_id=row["parent_node_id"],
                code=row["code"],
            )
            for row in rows
        )

    def get_node(
        self,
        node_id: str,
        curriculum_id: str | None = None,
        version: str | None = None,
    ) -> "CurriculumNode" | None:
        clauses = ["node_id = ?"]
        params: list[object] = [node_id]
        if curriculum_id is not None:
            resolved_version = self._resolve_version(curriculum_id, version)
            if resolved_version is None:
                return None
            clauses.extend(["curriculum_id = ?", "curriculum_version = ?"])
            params.extend([curriculum_id, resolved_version])
        row = self.connection.execute(
            "SELECT node_id, name, node_type, parent_node_id, code "
            "FROM curriculum_nodes WHERE " + " AND ".join(clauses),
            tuple(params),
        ).fetchone()
        if row is None:
            return None
        return CurriculumNode(
            node_id=row["node_id"],
            name=row["name"],
            node_type=row["node_type"],
            parent_node_id=row["parent_node_id"],
            code=row["code"],
        )

    def seed_curriculum(self, curriculum: Curriculum) -> None:
        """Insert a complete snapshot for adapter/bootstrap tests and controlled imports."""
        with self.connection:
            self.connection.execute(
                "INSERT INTO curricula(curriculum_id, version, professional_year) VALUES (?, ?, ?)",
                (curriculum.curriculum_id, curriculum.version, curriculum.professional_year),
            )
            for subject in curriculum.subjects:
                self.connection.execute(
                    "INSERT INTO subjects(curriculum_id, curriculum_version, subject_id, name) "
                    "VALUES (?, ?, ?, ?)",
                    (curriculum.curriculum_id, curriculum.version, subject.subject_id, subject.name),
                )
                self.connection.executemany(
                    "INSERT INTO topics(curriculum_id, curriculum_version, subject_id, topic_id, name) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        (
                            curriculum.curriculum_id,
                            curriculum.version,
                            subject.subject_id,
                            topic.topic_id,
                            topic.name,
                        )
                        for topic in subject.topics
                    ),
                )


__all__ = ["SQLiteCatalogRepository"]
