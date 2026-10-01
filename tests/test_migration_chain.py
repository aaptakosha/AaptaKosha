from pathlib import Path
import sqlite3


def test_all_sqlite_curriculum_migrations_apply_in_order():
    root = Path(__file__).resolve().parents[1]
    migration_numbers = [1] + list(range(4, 41))
    names = {
        1: "catalog",
        4: "bams_content_layout",
        5: "curriculum_hierarchy",
        6: "first_professional_hierarchy",
        7: "first_professional_data_quality",
        8: "third_professional_paper_layout",
        9: "second_professional_paper_layout",
        10: "first_professional_paper_layout",
        11: "first_professional_padartha_paper2",
        12: "first_professional_rachana_paper2",
        13: "first_professional_kriya_paper2",
        14: "correct_kriya_paper2_partb",
        15: "first_professional_padartha_samhita_layout",
        16: "first_professional_sanskrit_history_paper2",
        17: "second_professional_samhita_layout",
        18: "second_professional_agada_paper1",
        19: "second_professional_roga_nidan_paper1",
        20: "second_professional_dravyaguna_paper1",
        21: "second_professional_rasashastra_layout",
        22: "second_professional_swasthavritta_paper1",
        23: "third_professional_verified_paper_metadata",
        24: "third_professional_kaumarabhritya_paper1",
        25: "third_professional_prasuti_stree_roga_layout",
        26: "third_professional_kaumarabhritya_paper_metadata",
        27: "third_professional_kayachikitsa_paper_metadata",
        28: "third_professional_remaining_paper_metadata",
        29: "third_professional_kayachikitsa_panchakarma_topics",
        30: "third_professional_shalya_shalakya_metadata",
        31: "third_professional_sa3_rm_em_verified_metadata",
        32: "third_professional_sa3_structure",
        33: "third_professional_source_quality_cleanup",
        34: "third_professional_research_methodology_topics",
        35: "third_professional_shalya_paper1_topics",
        36: "third_professional_kaumarabhritya_complete_paper1",
        37: "third_professional_shalakya_complete_papers",
        38: "third_professional_samhita_adhyayan3_complete",
        39: "third_professional_shalya_complete_topics",
        40: "third_professional_source_locator_cleanup",
    }
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys=ON")
    for number in migration_numbers:
        path = root / "migrations" / f"{number:03d}_{names[number]}.sql"
        assert path.exists(), path
        db.executescript(path.read_text(encoding="utf-8"))
    assert db.execute("SELECT COUNT(*) FROM curricula").fetchone()[0] == 3
    assert db.execute("SELECT COUNT(*) FROM classical_texts").fetchone()[0] >= 20
    assert db.execute("SELECT COUNT(*) FROM curriculum_nodes WHERE curriculum_id='bams_ncism_3'").fetchone()[0] > 250
