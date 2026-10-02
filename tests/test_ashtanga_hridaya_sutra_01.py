import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_ashtanga_hridaya_sutra_01_structure():
    p = ROOT / "content/samhita/ashtanga_hridaya/sutrasthana/adhyaya-01.json"
    c = json.loads(p.read_text(encoding="utf-8"))
    assert c["chapter_id"] == "ashtanga.hridaya.sutra.01"
    assert c["verse_count"] == 39
    assert c["passage_count"] == 41
    assert c["prose_count"] == 2
    assert len(c["passages"]) == 41
    verses = [x for x in c["passages"] if x["type"] == "verse"]
    assert [int(x["passage_no"]) for x in verses] == list(range(1, 40))
    assert all(x["sanskrit_original"] for x in verses)
    assert all(x["translation_hi"] for x in verses)
    assert all(x["tika_sarvangasundara_hi"] for x in verses)
    assert all(x["tika_ayurvedarasayana_hi"] for x in verses)
    assert len(c["learning_units"]) == 11

def test_ashtanga_hridaya_sutra_01_assessment():
    p = ROOT / "content/assessments/ashtanga-hridaya-sutra-01-revision.json"
    a = json.loads(p.read_text(encoding="utf-8"))
    assert len(a["questions"]) == 20
    for q in a["questions"]:
        assert len(q["options"]) == 4
        assert sum(o["is_correct"] for o in q["options"]) == 1
        assert q["content_refs"]

def test_ashtanga_hridaya_sutra_01_hierarchy_and_bold_reader_contract():
    js = (ROOT / "frontend/samhita-detail.js").read_text(encoding="utf-8")
    study = (ROOT / "frontend/samhita-study.js").read_text(encoding="utf-8")
    assert '"01","आयुष्कामीय"' in js
    assert '"30","क्षाराग्निकर्मविधि"' in js
    assert "ashtanga.hridaya.sutra." in js
    assert "tika_sarvangasundara_hi" in study
    assert "tika_ayurvedarasayana_hi" in study
    assert 'class="sanskrit"' in study
    assert 'data-audio' in study
