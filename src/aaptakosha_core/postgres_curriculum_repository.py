"""PostgreSQL persistence adapter for the NCISM curriculum catalogue."""
from __future__ import annotations

from typing import Any, Tuple

from psycopg import Connection

from .catalog import Curriculum, CurriculumNode, Subject


_SCHEMA = """
CREATE TABLE IF NOT EXISTS curricula (
  curriculum_id TEXT NOT NULL,
  version TEXT NOT NULL,
  professional_year INTEGER NOT NULL CHECK (professional_year BETWEEN 1 AND 4),
  PRIMARY KEY (curriculum_id, version)
);
CREATE TABLE IF NOT EXISTS subjects (
  curriculum_id TEXT NOT NULL,
  curriculum_version TEXT NOT NULL,
  subject_id TEXT NOT NULL,
  name TEXT NOT NULL,
  PRIMARY KEY (curriculum_id, curriculum_version, subject_id),
  FOREIGN KEY (curriculum_id, curriculum_version)
    REFERENCES curricula(curriculum_id, version) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS curriculum_nodes (
  node_id TEXT PRIMARY KEY,
  curriculum_id TEXT NOT NULL,
  curriculum_version TEXT NOT NULL,
  subject_id TEXT NOT NULL,
  parent_node_id TEXT,
  node_type TEXT NOT NULL,
  code TEXT,
  name TEXT NOT NULL,
  source_reference TEXT,
  source_locator TEXT,
  term INTEGER,
  marks DOUBLE PRECISION,
  lecture_hours DOUBLE PRECISION,
  non_lecture_hours DOUBLE PRECISION,
  status TEXT NOT NULL DEFAULT 'structure_ready',
  sort_order INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (curriculum_id, curriculum_version, subject_id)
    REFERENCES subjects(curriculum_id, curriculum_version, subject_id) ON DELETE CASCADE,
  FOREIGN KEY (parent_node_id) REFERENCES curriculum_nodes(node_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_pg_curriculum_subject
  ON curriculum_nodes(curriculum_id, curriculum_version, subject_id, sort_order);
CREATE INDEX IF NOT EXISTS idx_pg_curriculum_parent
  ON curriculum_nodes(parent_node_id, sort_order);
CREATE TABLE IF NOT EXISTS classical_texts (
  text_id TEXT PRIMARY KEY,
  canonical_name TEXT NOT NULL,
  display_name TEXT NOT NULL,
  text_type TEXT NOT NULL,
  collection TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL DEFAULT 'planned',
  sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS classical_text_professional_links (
  text_id TEXT NOT NULL REFERENCES classical_texts(text_id) ON DELETE CASCADE,
  professional_year INTEGER NOT NULL CHECK (professional_year BETWEEN 1 AND 3),
  PRIMARY KEY (text_id, professional_year)
);
CREATE TABLE IF NOT EXISTS classical_text_tags (
  text_id TEXT NOT NULL REFERENCES classical_texts(text_id) ON DELETE CASCADE,
  tag TEXT NOT NULL,
  PRIMARY KEY (text_id, tag)
);
"""


class PostgresCurriculumRepository:
    """Durable PostgreSQL repository for curriculum metadata and hierarchy."""

    def __init__(self, connection: Connection[Any]):
        self.connection = connection

    def apply_migrations(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(_SCHEMA)
        self.connection.commit()

    def list_curricula(self) -> Tuple[Curriculum, ...]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT curriculum_id, version, professional_year "
                "FROM curricula ORDER BY professional_year, version"
            )
            rows = cursor.fetchall()
        return tuple(self._curriculum(row) for row in rows)

    def get_curriculum(
        self, curriculum_id: str, version: str | None = None
    ) -> Curriculum | None:
        with self.connection.cursor() as cursor:
            if version:
                cursor.execute(
                    "SELECT curriculum_id, version, professional_year "
                    "FROM curricula WHERE curriculum_id=%s AND version=%s",
                    (curriculum_id, version),
                )
            else:
                cursor.execute(
                    "SELECT curriculum_id, version, professional_year "
                    "FROM curricula WHERE curriculum_id=%s "
                    "ORDER BY version DESC LIMIT 1",
                    (curriculum_id,),
                )
            row = cursor.fetchone()
        return self._curriculum(row) if row else None

    def list_nodes(
        self,
        curriculum_id: str,
        subject_id: str | None = None,
        version: str | None = None,
        parent_node_id: str | None = None,
    ) -> Tuple[CurriculumNode, ...]:
        sql = (
            "SELECT node_id, name, node_type, parent_node_id, code "
            "FROM curriculum_nodes WHERE curriculum_id=%s"
        )
        params: list[Any] = [curriculum_id]
        if version:
            sql += " AND curriculum_version=%s"
            params.append(version)
        if subject_id:
            sql += " AND subject_id=%s"
            params.append(subject_id)
        if parent_node_id is None:
            if subject_id:
                sql += " AND parent_node_id IS NULL"
        else:
            sql += " AND parent_node_id=%s"
            params.append(parent_node_id)
        sql += " ORDER BY sort_order, node_id"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        return tuple(CurriculumNode(r[0], r[1], r[2], r[3], r[4]) for r in rows)

    def get_node(
        self,
        node_id: str,
        curriculum_id: str | None = None,
        version: str | None = None,
    ) -> CurriculumNode | None:
        sql = (
            "SELECT node_id,name,node_type,parent_node_id,code "
            "FROM curriculum_nodes WHERE node_id=%s"
        )
        params: list[Any] = [node_id]
        if curriculum_id:
            sql += " AND curriculum_id=%s"
            params.append(curriculum_id)
        if version:
            sql += " AND curriculum_version=%s"
            params.append(version)
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            row = cursor.fetchone()
        return CurriculumNode(row[0], row[1], row[2], row[3], row[4]) if row else None

    def _curriculum(self, row: tuple[Any, ...]) -> Curriculum:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT subject_id,name FROM subjects "
                "WHERE curriculum_id=%s AND curriculum_version=%s "
                "ORDER BY subject_id",
                (row[0], row[1]),
            )
            subjects = cursor.fetchall()
        return Curriculum(
            row[0], row[1], row[2], tuple(Subject(s[0], s[1]) for s in subjects)
        )
