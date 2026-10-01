import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
CHAPTER = ROOT / "content" / "samhita" / "charaka" / "sutrasthana" / "adhyaya-06.json"
BANK = ROOT / "content" / "assessments" / "charaka-sutra-06-revision.json"


def test_chapter6_has_canonical_51_verse_sequence_and_units():
    data = json.loads(CHAPTER.read_text(encoding="utf-8"))
    assert data["chapter_id"] == "charaka.sutra.06"
    assert data["adhyaya_no"] == 6
    assert data["verse_count"] == 51
    assert [v["verse_no"] for v in data["verses"]] == list(range(1, 52))
    assert data["verses"][0]["sanskrit_original"] == "अथातस्तस्याशितीयमध्यायं व्याख्यास्यामः||१||"
    assert data["verses"][1]["sanskrit_original"] == "इति ह स्माह भगवानात्रेयः||२||"
    assert data["verses"][-1]["verse_id"] == "charaka.sutra.06.051"
    assert len(data["learning_units"]) == 8
    assert sum(u["end_verse"] - u["start_verse"] + 1 for u in data["learning_units"]) == 51


def test_chapter6_assessment_covers_canonical_refs():
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    chapter = json.loads(CHAPTER.read_text(encoding="utf-8"))
    refs = {v["verse_id"] for v in chapter["verses"]}
    assert bank["assessment_id"] == "charaka.sutra.06.revision"
    assert bank["question_count"] == 20
    assert len(bank["questions"]) == 20
    assert all(sum(o["is_correct"] for o in q["options"]) == 1 for q in bank["questions"])
    assert all(ref in refs for q in bank["questions"] for ref in q["content_refs"])


def test_chapter6_reader_and_api_are_wired():
    api = (ROOT / "api" / "assessments.py").read_text(encoding="utf-8")
    js = (ROOT / "frontend" / "samhita-study.js").read_text(encoding="utf-8")
    assert "chapter_no not in {1, 2, 3, 4, 5, 6}" in api
    assert '_seed_samhita_chapter6_assessment(service, repo)' in api
    assert 'charaka.sutra.06.revision' in js
