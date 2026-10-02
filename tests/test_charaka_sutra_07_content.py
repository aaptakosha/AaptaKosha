import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_charaka_sutra_07_canonical_contract():
    chapter = load("content/samhita/charaka/sutrasthana/adhyaya-07.json")
    assert chapter["chapter_id"] == "charaka.sutra.07"
    assert chapter["curriculum_refs"] == ["AyUG-SA1"]
    assert chapter["verse_count"] == 64
    assert chapter["passage_count"] == 66
    assert chapter["prose_count"] == 2
    ids = [v["verse_id"] for v in chapter["verses"]]
    assert len(ids) == 64
    assert len(ids) == len(set(ids))
    assert ids[0] == "charaka.sutra.07.003"
    assert ids[-1] == "charaka.sutra.07.066"
    assert len(chapter["prose_passages"]) == 2
    assert [p["passage_id"] for p in chapter["editorial_passages"]] == [
        "charaka.sutra.07.033.1",
        "charaka.sutra.07.035.1",
        "charaka.sutra.07.035.2",
    ]
    assert all(v["sanskrit_original"] and v["translation_hi"] and v["explanation_hi"] and v["tika_hi"] for v in chapter["verses"])
    explanations = [v["explanation_hi"] for v in chapter["verses"]]
    tikas = [v["tika_hi"] for v in chapter["verses"]]
    assert len(set(explanations)) == len(explanations)
    assert len(set(tikas)) == len(tikas)
    assert all("यह श्लोक" not in text or len(text) > 45 for text in explanations)
    assert all("इस पदसमूह में शास्त्रीय निर्देश/लक्षण/उपाय" not in text for text in tikas)
    assert "2026-10-02" in chapter["recitation_policy"]


def test_charaka_sutra_07_assessment_contract():
    chapter = load("content/samhita/charaka/sutrasthana/adhyaya-07.json")
    assessment = load("content/assessments/charaka-sutra-07-revision.json")
    canonical = {v["verse_id"] for v in chapter["verses"]}
    assert assessment["assessment_id"] == "charaka.sutra.07.revision"
    assert assessment["curriculum_refs"] == ["AyUG-SA1"]
    assert assessment["question_count"] == 20
    assert len(assessment["questions"]) == 20
    question_ids = [q["question_id"] for q in assessment["questions"]]
    assert len(question_ids) == len(set(question_ids))
    for q in assessment["questions"]:
        assert len(q["options"]) == 4
        assert sum(o["is_correct"] for o in q["options"]) == 1
        assert q["content_refs"]
        assert set(q["content_refs"]).issubset(canonical)


def test_charaka_sutra_07_reader_and_api_are_wired():
    api = (ROOT / "api" / "assessments.py").read_text(encoding="utf-8")
    reader = (ROOT / "frontend" / "samhita-study.js").read_text(encoding="utf-8")
    assert 'path == "/content/samhita"' in api
    assert "_seed_samhita_assessments(service, repo)" in api
    assert "_seed_samhita_assessments(service, repo)" in api
    assert "assessmentIdForChapter" in reader
    assert 'charaka.sutra.07.revision' in reader
