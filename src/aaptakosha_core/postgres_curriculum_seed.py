"""Controlled NCISM curriculum seed loader for PostgreSQL.

Run this as an offline/admin operation, never during learner requests.
"""
from __future__ import annotations
import os, sqlite3
from pathlib import Path
import psycopg
from .postgres_curriculum_repository import PostgresCurriculumRepository

MIGRATIONS = tuple(
    f"{n:03d}_{name}.sql" for n, name in [
        (1,"catalog"),(4,"bams_content_layout"),(5,"curriculum_hierarchy"),
        (6,"first_professional_hierarchy"),(7,"first_professional_data_quality"),
        (8,"third_professional_paper_layout"),(9,"second_professional_paper_layout"),
        (10,"first_professional_paper_layout"),(11,"first_professional_padartha_paper2"),
        (12,"first_professional_rachana_paper2"),(13,"first_professional_kriya_paper2"),
        (14,"correct_kriya_paper2_partb"),(15,"first_professional_padartha_samhita_layout"),
        (16,"first_professional_sanskrit_history_paper2"),(17,"second_professional_samhita_layout"),
        (18,"second_professional_agada_paper1"),(19,"second_professional_roga_nidan_paper1"),
        (20,"second_professional_dravyaguna_paper1"),(21,"second_professional_rasashastra_layout"),
        (22,"second_professional_swasthavritta_paper1"),(23,"third_professional_verified_paper_metadata"),
        (24,"third_professional_kaumarabhritya_paper1"),(25,"third_professional_prasuti_stree_roga_layout"),
        (26,"third_professional_kaumarabhritya_paper_metadata"),(27,"third_professional_kayachikitsa_paper_metadata"),
        (28,"third_professional_remaining_paper_metadata"),(29,"third_professional_kayachikitsa_panchakarma_topics"),
        (30,"third_professional_shalya_shalakya_metadata"),(31,"third_professional_sa3_rm_em_verified_metadata"),
        (32,"third_professional_sa3_structure"),(33,"third_professional_source_quality_cleanup"),
        (34,"third_professional_research_methodology_topics"),(35,"third_professional_shalya_paper1_topics"),
        (36,"third_professional_kaumarabhritya_complete_paper1"),(37,"third_professional_shalakya_complete_papers"),
        (38,"third_professional_samhita_adhyayan3_complete"),(39,"third_professional_shalya_complete_topics"),\n        (40,"third_professional_source_locator_cleanup")
    ]
)

def seed(database_url: str, root: Path) -> None:
    source = sqlite3.connect(":memory:")
    source.execute("PRAGMA foreign_keys=ON")
    for name in MIGRATIONS:
        source.executescript((root/"migrations"/name).read_text(encoding="utf-8"))
    with psycopg.connect(database_url) as connection:
        repo = PostgresCurriculumRepository(connection)
        repo.apply_migrations()
        with connection.cursor() as cur:
            for row in source.execute("SELECT curriculum_id,version,professional_year FROM curricula"):
                cur.execute("INSERT INTO curricula VALUES (%s,%s,%s) ON CONFLICT (curriculum_id,version) DO UPDATE SET professional_year=EXCLUDED.professional_year", row)
            for row in source.execute("SELECT curriculum_id,curriculum_version,subject_id,name FROM subjects"):
                cur.execute("INSERT INTO subjects VALUES (%s,%s,%s,%s) ON CONFLICT (curriculum_id,curriculum_version,subject_id) DO UPDATE SET name=EXCLUDED.name", row)
            for row in source.execute("SELECT node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,status,sort_order FROM curriculum_nodes ORDER BY node_id"):
                cur.execute(
                    "INSERT INTO curriculum_nodes VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                    "ON CONFLICT (node_id) DO UPDATE SET name=EXCLUDED.name,node_type=EXCLUDED.node_type,parent_node_id=EXCLUDED.parent_node_id,code=EXCLUDED.code,source_reference=EXCLUDED.source_reference,source_locator=EXCLUDED.source_locator,term=EXCLUDED.term,marks=EXCLUDED.marks,lecture_hours=EXCLUDED.lecture_hours,non_lecture_hours=EXCLUDED.non_lecture_hours,status=EXCLUDED.status,sort_order=EXCLUDED.sort_order", row)
        for row in source.execute("SELECT text_id,canonical_name,display_name,text_type,collection,description,status,sort_order FROM classical_texts ORDER BY sort_order,text_id"):
                cur.execute(
                    "INSERT INTO classical_texts VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
                    "ON CONFLICT (text_id) DO UPDATE SET canonical_name=EXCLUDED.canonical_name,display_name=EXCLUDED.display_name,text_type=EXCLUDED.text_type,collection=EXCLUDED.collection,description=EXCLUDED.description,status=EXCLUDED.status,sort_order=EXCLUDED.sort_order", row)
            for row in source.execute("SELECT text_id,professional_year FROM classical_text_professional_links ORDER BY text_id,professional_year"):
                cur.execute(
                    "INSERT INTO classical_text_professional_links VALUES (%s,%s) ON CONFLICT (text_id,professional_year) DO NOTHING", row)
            for row in source.execute("SELECT text_id,tag FROM classical_text_tags ORDER BY text_id,tag"):
                cur.execute(
                    "INSERT INTO classical_text_tags VALUES (%s,%s) ON CONFLICT (text_id,tag) DO NOTHING", row)
        connection.commit()

if __name__ == "__main__":
    url=os.environ.get("DATABASE_URL")
    if not url: raise SystemExit("DATABASE_URL is required")
    seed(url, Path(__file__).resolve().parents[2])
