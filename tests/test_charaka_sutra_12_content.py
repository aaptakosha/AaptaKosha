import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def test_charaka_sutra_12_contract():
    c=load("content/samhita/charaka/sutrasthana/adhyaya-12.json")
    assert c["chapter_id"]=="charaka.sutra.12"
    assert c["curriculum_refs"]==["AyUG-SA1"]
    assert c["verse_count"]==6 and c["passage_count"]==22 and c["prose_count"]==16
    assert len(c["passages"])==22
    ids=[p["passage_id"] for p in c["passages"]]
    assert len(ids)==len(set(ids)) and ids[0]=="charaka.sutra.12.001" and ids[-1]=="charaka.sutra.12.017cd"
    assert sum(p["type"]=="prose" for p in c["passages"])==16
    assert sum(p["type"]=="verse_half" for p in c["passages"])==6
    assert all(p["sanskrit_original"] and p["translation_hi"] and p["explanation_hi"] and p["tika_hi"] for p in c["passages"])
    assert len({p["explanation_hi"] for p in c["passages"]})==22
    assert len({p["tika_hi"] for p in c["passages"]})==22
    assert not any("यह श्लोक" in p["explanation_hi"] for p in c["passages"])
def test_charaka_sutra_12_sequence():
    c=load("content/samhita/charaka/sutrasthana/adhyaya-12.json")
    ids=[p["passage_id"] for p in c["passages"]]
    assert ids[14:]==["charaka.sutra.12.015","charaka.sutra.12.015ab","charaka.sutra.12.015cd","charaka.sutra.12.016","charaka.sutra.12.016ab","charaka.sutra.12.016cd","charaka.sutra.12.017ab","charaka.sutra.12.017cd"]
def test_charaka_sutra_12_assessment():
    c=load("content/samhita/charaka/sutrasthana/adhyaya-12.json"); a=load("content/assessments/charaka-sutra-12-revision.json"); ids={p["passage_id"] for p in c["passages"]}
    assert a["assessment_id"]=="charaka.sutra.12.revision" and a["curriculum_refs"]==["AyUG-SA1"] and len(a["questions"])==20
    assert all(len(q["options"])==4 and sum(o["is_correct"] for o in q["options"])==1 and set(q["content_refs"]).issubset(ids) for q in a["questions"])
def test_charaka_sutra_12_research():
    r=(ROOT/"docs/charaka-sutra-12-research.md").read_text(encoding="utf-8")
    assert "22 passages" in r and "16 in prose" in r and "Chapter 13 onward" in r

def test_charaka_sutra_12_api_reader_wiring():
    api=(ROOT/"api"/"assessments.py").read_text(encoding="utf-8")
    reader=(ROOT/"frontend"/"samhita-study.js").read_text(encoding="utf-8")
    assert 'path == "/content/samhita"' in api
    assert "_seed_samhita_assessments(service, repo)" in api
    assert "charaka.sutra.12.revision" in api
    assert "assessmentIdForChapter" in reader
    assert 'id+".revision"' in reader
