from pathlib import Path
import sqlite3


def test_third_professional_curriculum_data_integrity():
    root = Path(__file__).resolve().parents[1]
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys=ON")
    names = ["001_catalog.sql"] + [
        p.name for p in sorted((root / "migrations").glob("*.sql"))
        if 4 <= int(p.name[:3]) <= 42
    ]
    for name in names:
        db.executescript((root / "migrations" / name).read_text(encoding="utf-8"))
    orphan_count = db.execute("""
        SELECT COUNT(*) FROM curriculum_nodes n
        WHERE n.parent_node_id IS NOT NULL
          AND NOT EXISTS (SELECT 1 FROM curriculum_nodes p WHERE p.node_id=n.parent_node_id)
    """).fetchone()[0]
    assert orphan_count == 0
    duplicate_codes = db.execute("""
        SELECT curriculum_id, subject_id, parent_node_id, code, COUNT(*)
        FROM curriculum_nodes
        WHERE code IS NOT NULL
        GROUP BY curriculum_id, subject_id, parent_node_id, code
        HAVING COUNT(*) > 1
    """).fetchall()
    allowed_seed_duplicates = set()\n    assert set(duplicate_codes) == allowed_seed_duplicates
    row = db.execute("""
        SELECT node_id, code, name FROM curriculum_nodes
        WHERE node_id='y3-sa3-17'
    """).fetchone()
    assert row[0:2] == ('y3-sa3-17', '17')
    assert row[2] == 'Cha.Chi.17.Hikka Shwasa Chikitsitam'
    assert db.execute("SELECT COUNT(*) FROM curriculum_nodes WHERE curriculum_id='bams_ncism_3' AND subject_id='AyUG-SA3'").fetchone()[0] == 49
