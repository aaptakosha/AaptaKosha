import json
from pathlib import Path
ROOT=Path(__file__).parents[1]
CHAPTER=ROOT/"content/samhita/charaka/sutrasthana/adhyaya-03.json"
BANK=ROOT/"content/assessments/charaka-sutra-03-revision.json"
def test_chapter3_has_complete_30_verse_sequence():
    c=json.loads(CHAPTER.read_text(encoding="utf-8")); assert c["chapter_id"]=="charaka.sutra.03"; assert c["verse_count"]==30; assert [v["verse_no"] for v in c["verses"]]==list(range(1,31)); assert all(v["sanskrit_original"] and v["translation_hi"] and v["explanation_hi"] and v["tika_hi"] for v in c["verses"])
def test_chapter3_units_cover_all_verses_without_overlap():
    c=json.loads(CHAPTER.read_text(encoding="utf-8")); seen=[]; [seen.extend(range(u["start_verse"],u["end_verse"]+1)) for u in c["learning_units"]]; assert seen==list(range(1,31))
def test_chapter3_assessment_maps_to_canonical_content():
    c=json.loads(CHAPTER.read_text(encoding="utf-8")); b=json.loads(BANK.read_text(encoding="utf-8")); refs={v["verse_id"] for v in c["verses"]}; units={f'charaka.sutra.03.unit-{i:02d}' for i in range(1,len(c["learning_units"])+1)}; assert b["assessment_id"]=="charaka.sutra.03.revision"; assert len(b["questions"])==15; assert all(q["content_refs"][0] in refs and q["content_refs"][1] in units for q in b["questions"])
