import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
CH7 = ROOT / "content" / "samhita" / "charaka" / "sutrasthana" / "adhyaya-07.json"
CH1 = ROOT / "content" / "samhita" / "charaka" / "sutrasthana" / "adhyaya-01.json"
CH6 = ROOT / "content" / "samhita" / "charaka" / "sutrasthana" / "adhyaya-06.json"
SA2 = ROOT / "migrations" / "017_second_professional_samhita_layout.sql"


def test_charaka_sa1_content_boundary_is_explicit():
    for path in (CH1, CH6):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["curriculum_refs"] == ["AyUG-SA1"]
        assert 1 <= data["adhyaya_no"] <= 12


def test_charaka_chapter7_is_the_next_sa1_content_target():
    if CH7.exists():
        data = json.loads(CH7.read_text(encoding="utf-8"))
        assert data["chapter_id"] == "charaka.sutra.07"
        assert data["adhyaya_no"] == 7
        assert data["curriculum_refs"] == ["AyUG-SA1"]
    assert "AyUG-SA2" not in CH6.read_text(encoding="utf-8")


def test_charaka_chapter13_is_already_mapped_to_sa2():
    sql = SA2.read_text(encoding="utf-8")
    assert "'y2-sa2-1','bams_ncism_2','2021-22','AyUG-SA2','y2-sa2-paper1','chapter','Cha.Su.13','Sneha Adhyaya'" in sql
