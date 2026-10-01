import json
from pathlib import Path

ROOT=Path(__file__).parents[1]
CHAPTER=ROOT/"content/samhita/charaka/sutrasthana/adhyaya-04.json"
BANK=ROOT/"content/assessments/charaka-sutra-04-revision.json"

def test_chapter4_has_complete_29_verse_sequence():
    c=json.loads(CHAPTER.read_text(encoding="utf-8"))
    assert c["chapter_id"]=="charaka.sutra.04"
    assert c["verse_count"]==29
    assert [v["verse_no"] for v in c["verses"]]==list(range(1,30))
    assert all(v["sanskrit_original"] and v["translation_hi"] and v["explanation_hi"] and v["tika_hi"] for v in c["verses"])

def test_chapter4_units_cover_all_verses_without_overlap():
    c=json.loads(CHAPTER.read_text(encoding="utf-8"))
    seen=[]
    for u in c["learning_units"]:
        seen.extend(range(u["start_verse"],u["end_verse"]+1))
    assert seen==list(range(1,30))

def test_chapter4_has_core_study_index():
    c=json.loads(CHAPTER.read_text(encoding="utf-8"))
    assert c["study_index"]["virechana_count"]==600
    assert c["study_index"]["kashaya_group_count"]==500
    assert c["study_index"]["mahakashaya_count"]==50
    assert len(c["study_index"]["virechana_ashraya"])==6
    assert len(c["study_index"]["kashaya_yoni"])==5
    assert len(c["study_index"]["kashaya_kalpana"])==5

def test_chapter4_assessment_maps_to_canonical_content():
    c=json.loads(CHAPTER.read_text(encoding="utf-8"))
    b=json.loads(BANK.read_text(encoding="utf-8"))
    refs={v["verse_id"] for v in c["verses"]}
    units={f'charaka.sutra.04.unit-{i:02d}' for i in range(1,len(c["learning_units"])+1)}
    assert b["assessment_id"]=="charaka.sutra.04.revision"
    assert len(b["questions"])==14
    assert len({ref for q in b["questions"] for ref in q["content_refs"] if ".unit-" not in ref})==len(b["questions"])
    assert all(q["content_refs"][0] in refs and q["content_refs"][1] in units for q in b["questions"])
