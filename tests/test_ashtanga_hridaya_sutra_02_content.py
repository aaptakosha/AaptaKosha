import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def test_ashtanga_hridaya_chapter2_contract():
    c=load("content/samhita/ashtanga_hridaya/sutrasthana/adhyaya-02.json")
    assert c["chapter_id"]=="ashtanga.hridaya.sutra.02"
    assert c["curriculum_refs"]==["AyUG-SA1"]
    assert c["verse_count"]==48 and c["passage_count"]==51 and c["prose_count"]==0
    assert len(c["passages"])==51
    assert sum(p["type"]=="verse_half" for p in c["passages"])==3
    ids=[p["passage_id"] for p in c["passages"]]
    assert len(ids)==len(set(ids))
    assert all(p["sanskrit_original"] and p["translation_hi"] and p["tika_sarvangasundara_hi"] and p["tika_ayurvedarasayana_hi"] for p in c["passages"])
def test_ashtanga_hridaya_chapter2_units_and_assessment():
    c=load("content/samhita/ashtanga_hridaya/sutrasthana/adhyaya-02.json")
    a=load("content/assessments/ashtanga-hridaya-sutra-02-revision.json")
    ids={p["passage_id"] for p in c["passages"]}
    assert len(c["learning_units"])==10
    assert all(set(u["passage_refs"]).issubset(ids) for u in c["learning_units"])
    assert len(a["questions"])==20
    assert all(len(q["options"])==4 and sum(o["is_correct"] for o in q["options"])==1 and set(q["content_refs"]).issubset(ids) for q in a["questions"])
