import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_chapter6_canonical_content_and_assessment():
    chapter = json.loads((ROOT / "content/samhita/charaka/sutrasthana/adhyaya-06.json").read_text(encoding="utf-8"))
    assessment = json.loads((ROOT / "content/assessments/charaka-sutra-06-revision.json").read_text(encoding="utf-8"))

    assert chapter["chapter_id"] == "charaka.sutra.06"
    assert chapter["verse_count"] == 51
    assert [v["verse_no"] for v in chapter["verses"]] == list(range(1, 52))
    assert len({v["verse_id"] for v in chapter["verses"]}) == 51
    assert all(v["tika_hi"].strip() for v in chapter["verses"])

    assert assessment["assessment_id"] == "charaka.sutra.06.revision"
    assert assessment["question_count"] == 20
    assert len(assessment["questions"]) == 20
    verse_ids = {v["verse_id"] for v in chapter["verses"]}
    for q in assessment["questions"]:
        assert sum(o["is_correct"] for o in q["options"]) == 1
        assert q["content_refs"]
        assert set(q["content_refs"]) <= verse_ids
