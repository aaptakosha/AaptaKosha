import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def test_charaka_sutra_11_canonical_contract():
    chapter = load("content/samhita/charaka/sutrasthana/adhyaya-11.json")
    assert chapter["chapter_id"] == "charaka.sutra.11"
    assert chapter["curriculum_refs"] == ["AyUG-SA1"]
    assert chapter["verse_count"] == 64
    assert chapter["passage_count"] == 103
    assert chapter["prose_count"] == 39
    assert len(chapter["passages"]) == 103
    ids = [p["passage_id"] for p in chapter["passages"]]
    assert len(ids) == len(set(ids))
    assert ids[0] == "charaka.sutra.11.001"
    assert ids[-1] == "charaka.sutra.11.65cd"
    assert sum(p["type"] == "prose" for p in chapter["passages"]) == 39
    assert sum(p["type"] == "verse_half" for p in chapter["passages"]) == 64
    assert all(p["sanskrit_original"] and p["translation_hi"] and p["explanation_hi"] and p["tika_hi"] for p in chapter["passages"])
    assert len({p["explanation_hi"] for p in chapter["passages"]}) == 103
    assert len({p["tika_hi"] for p in chapter["passages"]}) == 103
    assert not any("यह श्लोक" in p["explanation_hi"] for p in chapter["passages"])

def test_charaka_sutra_11_source_sequence_contract():
    chapter = load("content/samhita/charaka/sutrasthana/adhyaya-11.json")
    ids = [p["passage_id"] for p in chapter["passages"]]
    prose = [p["passage_id"] for p in chapter["passages"] if p["type"] == "prose"]
    assert prose == [
        *(f"charaka.sutra.11.{i:03d}" for i in range(1, 10)),
        "charaka.sutra.11.017", "charaka.sutra.11.018",
        *(f"charaka.sutra.11.{i:03d}" for i in range(27, 51)),
        "charaka.sutra.11.054", "charaka.sutra.11.055", "charaka.sutra.11.056",
        "charaka.sutra.11.064",
    ]
    assert "charaka.sutra.11.047ab" in ids and "charaka.sutra.11.047cd" in ids
    assert "charaka.sutra.11.050ab" in ids and "charaka.sutra.11.050cd" in ids
    assert "charaka.sutra.11.056ab" in ids and "charaka.sutra.11.056cd" in ids
    assert "charaka.sutra.11.064ab" in ids and "charaka.sutra.11.065cd" in ids

def test_charaka_sutra_11_assessment_contract():
    chapter = load("content/samhita/charaka/sutrasthana/adhyaya-11.json")
    assessment = load("content/assessments/charaka-sutra-11-revision.json")
    canonical = {p["passage_id"] for p in chapter["passages"]}
    assert assessment["assessment_id"] == "charaka.sutra.11.revision"
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

def test_charaka_sutra_11_research_contract():
    manifest = (ROOT / "docs" / "charaka-sutra-11-research.md").read_text(encoding="utf-8")
    assert "Tisraiṣaṇīya" in manifest or "Tisraiṣanīya" in manifest
    assert "103 passages" in manifest
    assert "39 prose" in manifest
    assert "Chapter 13 onward" in manifest
