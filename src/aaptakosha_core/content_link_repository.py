"""SQLite adapter for curriculum-to-content links."""
from __future__ import annotations
import sqlite3
from typing import Tuple
from .content_links import CurriculumContentLink

class SQLiteCurriculumContentLinkRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.connection.execute("PRAGMA foreign_keys = ON")
    def apply_migrations(self):
        self.connection.execute("""CREATE TABLE IF NOT EXISTS curriculum_content_links (curriculum_ref TEXT NOT NULL, resource_id TEXT NOT NULL, relationship TEXT NOT NULL, PRIMARY KEY(curriculum_ref, resource_id, relationship), FOREIGN KEY(resource_id) REFERENCES content_resources(resource_id) ON DELETE CASCADE)""")
        self.connection.commit()
    def save(self, link):
        self.connection.execute("INSERT OR IGNORE INTO curriculum_content_links VALUES (?, ?, ?)",(link.curriculum_ref,link.resource_id,link.relationship)); self.connection.commit(); return link
    def list_for_curriculum(self, curriculum_ref):
        rows=self.connection.execute("SELECT curriculum_ref,resource_id,relationship FROM curriculum_content_links WHERE curriculum_ref=? ORDER BY resource_id,relationship",(curriculum_ref,)).fetchall(); return tuple(CurriculumContentLink(*r) for r in rows)
    def list_for_resource(self, resource_id):
        rows=self.connection.execute("SELECT curriculum_ref,resource_id,relationship FROM curriculum_content_links WHERE resource_id=? ORDER BY curriculum_ref,relationship",(resource_id,)).fetchall(); return tuple(CurriculumContentLink(*r) for r in rows)

__all__=["SQLiteCurriculumContentLinkRepository"]
