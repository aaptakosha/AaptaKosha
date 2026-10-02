import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def test_chapter7_contract():
 c=load("content/samhita/ashtanga_hridaya/sutrasthana/adhyaya-07.json")
 assert c["verse_count"]==77 and c["passage_count"]==78
 assert len(c["passages"])==78 and len(c["learning_units"])==10
 assert len({p["passage_id"] for p in c["passages"]})==78
 assert all(p["sanskrit_original"] and p["translation_hi"] and p["tika_sarvangasundara_hi"] and p["tika_ayurvedarasayana_hi"] for p in c["passages"])
def test_chapter7_assessment_refs():
 c=load("content/samhita/ashtanga_hridaya/sutrasthana/adhyaya-07.json")
 a=load("content/assessments/ashtanga-hridaya-sutra-07-revision.json")
 ids={p["passage_id"] for p in c["passages"]}
 assert len(a["questions"])==20
 assert all(sum(o["is_correct"] for o in q["options"])==1 and set(q["content_refs"])<=ids for q in a["questions"])
