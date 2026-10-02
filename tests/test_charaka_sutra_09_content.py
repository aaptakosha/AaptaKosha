import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def test_charaka_sutra_09_canonical_contract():
    chapter = load("content/samhita/charaka/sutrasthana/adhyaya-09.json")
    assert chapter["chapter_id"] == "charaka.sutra.09"
    assert chapter["curriculum_refs"] == ["AyUG-SA1"]
    assert chapter["verse_count"] == 52
    assert chapter["passage_count"] == 55
    assert chapter["prose_count"] == 3
    assert len(chapter["passages"]) == 55
    ids = [p["passage_id"] for p in chapter["passages"]]
    assert len(ids) == len(set(ids))
    assert ids[0] == "charaka.sutra.09.001"
    assert ids[-1] == "charaka.sutra.09.028cd"
    assert sum(p["type"] == "prose" for p in chapter["passages"]) == 3
    assert sum(p["type"] == "verse_half" for p in chapter["passages"]) == 52
    assert [p["passage_id"] for p in chapter["passages"] if p["type"] == "prose"] == [
        "charaka.sutra.09.001", "charaka.sutra.09.002", "charaka.sutra.09.027"
    ]
    assert all(p["sanskrit_original"] and p["translation_hi"] and p["explanation_hi"] and p["tika_hi"] for p in chapter["passages"])
    assert len({p["explanation_hi"] for p in chapter["passages"]}) == 55
    assert len({p["tika_hi"] for p in chapter["passages"]}) == 55

def test_charaka_sutra_09_assessment_contract():
    chapter = load("content/samhita/charaka/sutrasthana/adhyaya-09.json")
    assessment = load("content/assessments/charaka-sutra-09-revision.json")
    canonical = {p["passage_id"] for p in chapter["passages"]}
    assert assessment["assessment_id"] == "charaka.sutra.09.revision"
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

def test_charaka_sutra_09_research_contract():
    manifest = (ROOT / "docs" / "charaka-sutra-09-research.md").read_text(encoding="utf-8")
    assert "Khuḍḍākacatuṣpāda" in manifest
    assert "55 passages, 3 in prose" in manifest
    assert "Chapter 13 onward" in manifest


def test_charaka_sutra_09_reader_and_api_are_wired():
    api = (ROOT / "api" / "assessments.py").read_text(encoding="utf-8")
    reader = (ROOT / "frontend" / "samhita-study.js").read_text(encoding="utf-8")
    assert 'path == "/content/samhita"' in api
    assert "_seed_samhita_assessments(service, repo)" in api
    assert "charaka.sutra.09.revision" in api
    assert "assessmentIdForChapter" in reader
    assert 'id+".revision"' in reader
