import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def test_charaka_sutra_10_canonical_contract():
    chapter = load("content/samhita/charaka/sutrasthana/adhyaya-10.json")
    assert chapter["chapter_id"] == "charaka.sutra.10"
    assert chapter["curriculum_refs"] == ["AyUG-SA1"]
    assert chapter["verse_count"] == 36
    assert chapter["passage_count"] == 44
    assert chapter["prose_count"] == 8
    assert len(chapter["passages"]) == 44
    ids = [p["passage_id"] for p in chapter["passages"]]
    assert len(ids) == len(set(ids))
    assert ids[0] == "charaka.sutra.10.001"
    assert ids[-1] == "charaka.sutra.10.024cd"
    assert sum(p["type"] == "prose" for p in chapter["passages"]) == 8
    assert sum(p["type"] == "verse_half" for p in chapter["passages"]) == 36
    assert [p["passage_id"] for p in chapter["passages"] if p["type"] == "prose"] == [
        "charaka.sutra.10.001", "charaka.sutra.10.002", "charaka.sutra.10.003",
        "charaka.sutra.10.004", "charaka.sutra.10.005", "charaka.sutra.10.006",
        "charaka.sutra.10.007", "charaka.sutra.10.023"
    ]
    assert all(p["sanskrit_original"] and p["translation_hi"] and p["explanation_hi"] and p["tika_hi"] for p in chapter["passages"])
    assert len({p["explanation_hi"] for p in chapter["passages"]}) == 44
    assert len({p["tika_hi"] for p in chapter["passages"]}) == 44
    assert all("यह श्लोक" not in p["explanation_hi"] for p in chapter["passages"])

def test_charaka_sutra_10_assessment_contract():
    chapter = load("content/samhita/charaka/sutrasthana/adhyaya-10.json")
    assessment = load("content/assessments/charaka-sutra-10-revision.json")
    canonical = {p["passage_id"] for p in chapter["passages"]}
    assert assessment["assessment_id"] == "charaka.sutra.10.revision"
    assert assessment["curriculum_refs"] == ["AyUG-SA1"]
    assert assessment["question_count"] == 20
    assert len(assessment["questions"]) == 20
    qids = [q["question_id"] for q in assessment["questions"]]
    assert len(qids) == len(set(qids))
    for q in assessment["questions"]:
        assert len(q["options"]) == 4
        assert sum(o["is_correct"] for o in q["options"]) == 1
        assert q["content_refs"]
        assert set(q["content_refs"]).issubset(canonical)

def test_charaka_sutra_10_research_contract():
    manifest = (ROOT / "docs" / "charaka-sutra-10-research.md").read_text(encoding="utf-8")
    assert "Mahācatuṣpāda" in manifest
    assert "44 passages, 8 in prose" in manifest
    assert "Chapter 13 onward" in manifest
