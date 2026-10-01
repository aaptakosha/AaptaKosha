import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
CHAPTER = ROOT / "content" / "samhita" / "charaka" / "sutrasthana" / "adhyaya-02.json"
BANK = ROOT / "content" / "assessments" / "charaka-sutra-02-revision.json"


def test_chapter2_has_complete_canonical_verse_sequence():
    chapter = json.loads(CHAPTER.read_text(encoding="utf-8"))
    assert chapter["chapter_id"] == "charaka.sutra.02"
    assert chapter["verse_count"] == 36
    assert [v["verse_no"] for v in chapter["verses"]] == list(range(1, 37))
    assert all(v["sanskrit_original"] and v["translation_hi"] and v["explanation_hi"] and v["tika_hi"] for v in chapter["verses"])


def test_chapter2_units_cover_all_verses_without_overlap():
    chapter = json.loads(CHAPTER.read_text(encoding="utf-8"))
    seen = []
    for unit in chapter["learning_units"]:
        seen.extend(range(unit["start_verse"], unit["end_verse"] + 1))
    assert seen == list(range(1, 37))


def test_chapter2_assessment_maps_to_canonical_content():
    chapter = json.loads(CHAPTER.read_text(encoding="utf-8"))
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    refs = {v["verse_id"] for v in chapter["verses"]}
    assert bank["assessment_id"] == "charaka.sutra.02.revision"
    assert len(bank["questions"]) == 12
    assert all(ref in refs for q in bank["questions"] for ref in q["content_refs"])
    assert {q["question_id"] for q in bank["questions"]} == {f"charaka.sutra.02.q{i:02d}" for i in range(1, 13)}


def test_chapter2_covers_ncism_four_focus_ranges():
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    joined = " ".join(q["prompt"] for q in bank["questions"])
    assert "शिरोविरेचन" in joined
    assert "वमन" in joined
    assert "विरेचन" in joined
    assert "आस्थापन" in joined
