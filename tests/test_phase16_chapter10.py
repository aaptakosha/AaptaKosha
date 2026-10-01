import json
from pathlib import Path
ROOT=Path(__file__).parents[1]
CHAPTER=ROOT/"content/samhita/charaka/sutrasthana/adhyaya-10.json"
BANK=ROOT/"content/assessments/charaka-sutra-10-revision.json"

def test_chapter10_canonical_sequence_and_units():
    data=json.loads(CHAPTER.read_text(encoding="utf-8"))
    assert data["chapter_id"]=="charaka.sutra.10"
    assert data["verse_count"]==24
    assert [v["verse_no"] for v in data["verses"]]==list(range(1,25))
    assert len({v["verse_id"] for v in data["verses"]})==24
    assert all(v["sanskrit_original"] and v["translation_hi"] and v["explanation_hi"] and v["tika_hi"] for v in data["verses"])
    assert sum(u["end_verse"]-u["start_verse"]+1 for u in data["learning_units"])==24

def test_chapter10_assessment_refs():
    bank=json.loads(BANK.read_text(encoding="utf-8")); refs={f"charaka.sutra.10.{i:03d}" for i in range(1,25)}
    assert bank["question_count"]==20 and len(bank["questions"])==20
    assert all(sum(o["is_correct"] for o in q["options"])==1 for q in bank["questions"])
    assert all(r in refs for q in bank["questions"] for r in q["content_refs"])
