from pathlib import Path
import json

ROOT = Path(__file__).parents[1]
CHAPTER = ROOT / "content" / "samhita" / "charaka" / "sutrasthana" / "adhyaya-01.json"


def test_charaka_chapter_has_actionable_learning_units_and_ncism_recitation():
    data = json.loads(CHAPTER.read_text(encoding="utf-8"))
    assert data["chapter_id"] == "charaka.sutra.01"
    assert len(data["learning_units"]) == 23
    assert data["recitation_count"] == 33
    assert [v["verse_no"] for v in data["verses"] if v["recitation_status"] == "ncism_explicit"] == data["recitation_verses"]
    assert sum(u["end_verse"] - u["start_verse"] + 1 for u in data["learning_units"]) == 140


def test_samhita_reader_is_connected_to_canonical_content_and_progress():
    api = (ROOT / "api" / "assessments.py").read_text(encoding="utf-8")
    js = (ROOT / "frontend" / "samhita-study.js").read_text(encoding="utf-8")
    assert 'path == "/content/samhita"' in api
    assert 'chapter_no not in {1, 2, 3, 4, 5, 6}' in api
    assert 'api("/api/progress")' in js
    assert 'saveProgress("samhita_unit"' in js
    assert 'saveProgress("samhita_recitation"' in js
    assert 'saveProgress("samhita_chapter"' in js


def test_assessment_questions_can_reference_canonical_content():
    source = (ROOT / "src" / "aaptakosha_core" / "assessment.py").read_text(encoding="utf-8")
    repo = (ROOT / "src" / "aaptakosha_core" / "assessment_repository.py").read_text(encoding="utf-8")
    api = (ROOT / "src" / "aaptakosha_core" / "assessment_api.py").read_text(encoding="utf-8")
    assert "content_refs" in source
    assert '"content_refs": list(q.content_refs)' in repo
    assert '"content_refs": list(question.content_refs)' in api


def test_samhita_reader_exposes_revision_and_ncism_modes():
    html = (ROOT / "frontend" / "samhita-study.html").read_text(encoding="utf-8")
    js = (ROOT / "frontend" / "samhita-study.js").read_text(encoding="utf-8")
    assert 'data-filter="recitation"' in html
    assert 'data-filter="revision"' in html
    assert 'data-recite' in js
    assert 'markUnitComplete' in html
