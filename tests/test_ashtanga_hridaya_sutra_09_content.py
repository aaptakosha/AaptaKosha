import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
CH = ROOT / "content/samhita/ashtanga_hridaya/sutrasthana/adhyaya-09.json"
AS = ROOT / "content/assessments/ashtanga-hridaya-sutra-09-revision.json"

def test_chapter_09_integrity():
    c=json.loads(CH.read_text(encoding="utf-8"))
    assert c["chapter_id"]=="ashtanga.hridaya.sutra.09"
    assert c["verse_count"]==28
    assert len(c["passages"])==29
    assert len(c["learning_units"])==5
    ids={p["passage_id"] for p in c["passages"]}
    assert len(ids)==29
    assert all(p.get("sanskrit_original") and p.get("translation_hi") and p.get("tika_sarvangasundara_hi") and p.get("tika_ayurvedarasayana_hi") for p in c["passages"])
    assert all(ref in ids for u in c["learning_units"] for ref in u["passage_refs"])

def test_chapter_09_assessment_refs():
    c=json.loads(CH.read_text(encoding="utf-8")); a=json.loads(AS.read_text(encoding="utf-8"))
    ids={p["passage_id"] for p in c["passages"]}
    assert len(a["questions"])==20
    assert all(len([o for o in q["options"] if o["is_correct"]])==1 for q in a["questions"])
    assert all(ref in ids for q in a["questions"] for ref in q["content_refs"])
