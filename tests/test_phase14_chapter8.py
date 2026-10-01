import json
from pathlib import Path
ROOT=Path(__file__).parents[1]
CHAPTER=ROOT/"content/samhita/charaka/sutrasthana/adhyaya-08.json"
BANK=ROOT/"content/assessments/charaka-sutra-08-revision.json"

def test_chapter8_canonical_sequence_and_units():
    data=json.loads(CHAPTER.read_text(encoding="utf-8"))
    assert data["chapter_id"]=="charaka.sutra.08"
    assert data["verse_count"]==34
    assert [v["verse_no"] for v in data["verses"]]==list(range(1,35))
    assert len({v["verse_id"] for v in data["verses"]})==34
    assert all(v["sanskrit_original"] and v["translation_hi"] and v["explanation_hi"] and v["tika_hi"] for v in data["verses"])
    assert sum(u["end_verse"]-u["start_verse"]+1 for u in data["learning_units"])==34

def test_chapter8_assessment_refs():
    bank=json.loads(BANK.read_text(encoding="utf-8")); refs={f"charaka.sutra.08.{i:03d}" for i in range(1,35)}
    assert bank["question_count"]==20 and len(bank["questions"])==20
    assert all(sum(o["is_correct"] for o in q["options"])==1 for q in bank["questions"])
    assert all(r in refs for q in bank["questions"] for r in q["content_refs"])
