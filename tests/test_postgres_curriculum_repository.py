from __future__ import annotations
import sqlite3
from aaptakosha_core.catalog import Curriculum, Subject, CurriculumNode
from aaptakosha_core.postgres_curriculum_repository import PostgresCurriculumRepository

def test_postgres_repository_has_durable_schema_contract():
    assert hasattr(PostgresCurriculumRepository, "apply_migrations")
    assert hasattr(PostgresCurriculumRepository, "list_curricula")
    assert hasattr(PostgresCurriculumRepository, "get_curriculum")
    assert hasattr(PostgresCurriculumRepository, "list_nodes")
    assert hasattr(PostgresCurriculumRepository, "get_node")

def test_curriculum_models_support_hierarchy_metadata():
    node = CurriculumNode("n1", "Paper I", "paper", code="I")
    subject = Subject("AyUG-ST", "Shalya Tantra")
    curriculum = Curriculum("bams_ncism_3", "2021-22", 3, (subject,))
    assert node.code == "I"
    assert curriculum.subjects[0].subject_id == "AyUG-ST"
