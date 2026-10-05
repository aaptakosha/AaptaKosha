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


_FIRST_PROFESSIONAL_CONTENT_PATCH = """
UPDATE curriculum_nodes SET code='AH.Su.2', node_type='chapter' WHERE node_id='y1-sa1-3' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.3', node_type='chapter' WHERE node_id='y1-sa1-4' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.4', node_type='chapter' WHERE node_id='y1-sa1-5' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.5', node_type='chapter' WHERE node_id='y1-sa1-6' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.6', node_type='chapter' WHERE node_id='y1-sa1-7' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.7', node_type='chapter' WHERE node_id='y1-sa1-8' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.8', node_type='chapter' WHERE node_id='y1-sa1-9' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.9', node_type='chapter' WHERE node_id='y1-sa1-10' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.10', node_type='chapter' WHERE node_id='y1-sa1-11' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.11', node_type='chapter' WHERE node_id='y1-sa1-12' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.12', node_type='chapter' WHERE node_id='y1-sa1-13' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.13', node_type='chapter' WHERE node_id='y1-sa1-14' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.14', node_type='chapter' WHERE node_id='y1-sa1-15' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.15', node_type='chapter' WHERE node_id='y1-sa1-16' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.1', node_type='chapter' WHERE node_id='y1-sa1-17' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.2', node_type='chapter' WHERE node_id='y1-sa1-18' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.3', node_type='chapter' WHERE node_id='y1-sa1-19' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.4', node_type='chapter' WHERE node_id='y1-sa1-20' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.5', node_type='chapter' WHERE node_id='y1-sa1-21' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.6', node_type='chapter' WHERE node_id='y1-sa1-22' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.7', node_type='chapter' WHERE node_id='y1-sa1-23' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.8', node_type='chapter' WHERE node_id='y1-sa1-24' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.9', node_type='chapter' WHERE node_id='y1-sa1-25' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.10', node_type='chapter' WHERE node_id='y1-sa1-26' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.11', node_type='chapter' WHERE node_id='y1-sa1-27' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.12', node_type='chapter' WHERE node_id='y1-sa1-28' AND subject_id='AyUG-SA1';
INSERT INTO curriculum_nodes (node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,sort_order)
VALUES
('y1-snai1-1','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','1','संस्कृतवर्णानाम् परिचयः','AaptaKosha published student content','content/sanskrit/01-varnamala-uccharana.md',1,10),
('y1-snai1-2','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','2','संज्ञा-प्रकरणम्','AaptaKosha published student content','content/sanskrit/02-samjna-avyaya.md',1,20),
('y1-snai1-3','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','3','उपसर्गाः','AaptaKosha published student content','content/sanskrit/08-upasarga-pratyaya.md',2,30),
('y1-snai1-4','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','4','अव्ययम्','AaptaKosha published student content','content/sanskrit/02-samjna-avyaya.md',1,40),
('y1-snai1-5','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','5','कारक-प्रकरणम् तथा वाच्यप्रयोगः','AaptaKosha published student content','content/sanskrit/05-karaka-vibhakti.md',2,50),
('y1-snai1-6','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','6','सन्धि','AaptaKosha published student content','content/sanskrit/06-sandhi.md',2,60),
('y1-snai1-7','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','7','समास-प्रकरणम्','AaptaKosha published student content','content/sanskrit/07-samasa.md',2,70),
('y1-snai1-8','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','8','शब्दरूपाणि','AaptaKosha published student content','content/sanskrit/03-shabdarupa-sarvanama.md',2,80),
('y1-snai1-9','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','9','धातुरूपाणि','AaptaKosha published student content','content/sanskrit/04-dhaturupa.md',2,90),
('y1-snai1-10','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','10','प्रत्ययाः','AaptaKosha published student content','content/sanskrit/08-upasarga-pratyaya.md',3,100),
('y1-snai1-11','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','11','विशेषण-विशेष्यम्','NCISM syllabus node; detailed lesson pending','',3,110)
ON CONFLICT (node_id) DO NOTHING;
INSERT INTO curriculum_nodes (node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,sort_order)
VALUES
('y1-snai2-a1','bams_ncism_1','2021-22','AyUG-SN-AI','y1-snai2-a','unit','1','निरुक्ति तथा पर्यायपदानि','AaptaKosha published student content','content/sanskrit/paper-2/part-a/01-nirukti-paryaya.md',1,10),
('y1-snai2-a2','bams_ncism_1','2021-22','AyUG-SN-AI','y1-snai2-a','unit','2','परिभाषापदानि','AaptaKosha published student content','content/sanskrit/paper-2/part-a/02-paribhasha.md',1,20),
('y1-snai2-a3','bams_ncism_1','2021-22','AyUG-SN-AI','y1-snai2-a','unit','3','अष्टाङ्गहृदयम् — prescribed selected chapters','AaptaKosha published student content','content/sanskrit/paper-2/part-a/03-ashtanga-hridaya.md',2,30),
('y1-snai2-a4','bams_ncism_1','2021-22','AyUG-SN-AI','y1-snai2-a','unit','4','आयुर्वेद सुभाषित','AaptaKosha published student content','content/sanskrit/paper-2/part-a/04-ayurveda-subhashita.md',2,40),
('y1-snai2-a5','bams_ncism_1','2021-22','AyUG-SN-AI','y1-snai2-a','unit','5','पञ्चतन्त्रम् — prescribed stories','AaptaKosha published student content','content/sanskrit/paper-2/part-a/05-panchatantra.md',2,50)
ON CONFLICT (node_id) DO NOTHING;
""";


class PostgresCurriculumRepository:
    """Durable PostgreSQL repository for curriculum metadata and hierarchy."""

    def __init__(self, connection: Connection[Any]):
        self.connection = connection

    def apply_migrations(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(_SCHEMA)
            cursor.execute(_FIRST_PROFESSIONAL_CONTENT_PATCH)
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
