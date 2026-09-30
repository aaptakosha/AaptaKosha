"""Persistence boundary for knowledge/content resources."""

from __future__ import annotations

import json
import sqlite3
from typing import Protocol, Tuple

from .content import ContentProvenance, ContentResource


class ContentRepository(Protocol):
    def get(self, resource_id: str) -> ContentResource | None: ...
    def list(self, status: str | None = None) -> Tuple[ContentResource, ...]: ...
    def save(self, resource: ContentResource) -> ContentResource: ...


class SQLiteContentRepository:
    """SQLite adapter implementing the framework-neutral content repository."""

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.connection.execute("PRAGMA foreign_keys = ON")

    def apply_migrations(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS content_resources (
                resource_id TEXT PRIMARY KEY,
                resource_type TEXT NOT NULL,
                title TEXT NOT NULL,
                summary TEXT NOT NULL,
                status TEXT NOT NULL,
                provenance_json TEXT NOT NULL,
                curriculum_refs_json TEXT NOT NULL
            );
            """
        )
        self.connection.commit()

    def get(self, resource_id: str) -> ContentResource | None:
        row = self.connection.execute(
            "SELECT resource_id, resource_type, title, summary, status, "
            "provenance_json, curriculum_refs_json FROM content_resources "
            "WHERE resource_id = ?",
            (resource_id,),
        ).fetchone()
        return self._from_row(row) if row else None

    def list(self, status: str | None = None) -> Tuple[ContentResource, ...]:
        if status is None:
            rows = self.connection.execute(
                "SELECT resource_id, resource_type, title, summary, status, "
                "provenance_json, curriculum_refs_json FROM content_resources "
                "ORDER BY resource_id"
            ).fetchall()
        else:
            rows = self.connection.execute(
                "SELECT resource_id, resource_type, title, summary, status, "
                "provenance_json, curriculum_refs_json FROM content_resources "
                "WHERE status = ? ORDER BY resource_id",
                (status,),
            ).fetchall()
        return tuple(self._from_row(row) for row in rows)

    def save(self, resource: ContentResource) -> ContentResource:
        self.connection.execute(
            """
            INSERT INTO content_resources (
                resource_id, resource_type, title, summary, status,
                provenance_json, curriculum_refs_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(resource_id) DO UPDATE SET
                resource_type=excluded.resource_type,
                title=excluded.title,
                summary=excluded.summary,
                status=excluded.status,
                provenance_json=excluded.provenance_json,
                curriculum_refs_json=excluded.curriculum_refs_json
            """,
            (
                resource.resource_id,
                resource.resource_type,
                resource.title,
                resource.summary,
                resource.status,
                json.dumps([{"source": p.source, "locator": p.locator, "attribution": p.attribution} for p in resource.provenance]),
                json.dumps(list(resource.curriculum_refs)),
            ),
        )
        self.connection.commit()
        return resource

    @staticmethod
    def _from_row(row) -> ContentResource:
        provenance = tuple(
            ContentProvenance(**item) for item in json.loads(row[5])
        )
        return ContentResource(
            resource_id=row[0],
            resource_type=row[1],
            title=row[2],
            summary=row[3],
            status=row[4],
            provenance=provenance,
            curriculum_refs=tuple(json.loads(row[6])),
        )


__all__ = ["ContentRepository", "SQLiteContentRepository"]
