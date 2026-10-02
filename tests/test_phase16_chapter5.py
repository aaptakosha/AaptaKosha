import json
from pathlib import Path

ROOT=Path(__file__).parents[1]
CHAPTER=ROOT/"content/samhita/charaka/sutrasthana/adhyaya-05.json"
BANK=ROOT/"content/assessments/charaka-sutra-05-revision.json"
READER=ROOT/"frontend/samhita-study.js"
API=ROOT/"api/assessments.py"

def test_chapter5_has_complete_111_verse_sequence():
    c=json.loads(CHAPTER.read_text(encoding="utf-8"))
    assert c["chapter_id"]=="charaka.sutra.05"
    assert c["verse_count"]==111
    assert [v["verse_no"] for v in c["verses"]]==list(range(1,112))
    assert len({v["verse_id"] for v in c["verses"]})==111
    assert all(v["sanskrit_original"] and v["translation_hi"] and v["explanation_hi"] and v["tika_hi"] for v in c["verses"])

def test_chapter5_units_cover_all_verses_without_overlap():
    c=json.loads(CHAPTER.read_text(encoding="utf-8"))
    seen=[]
    for u in c["learning_units"]:
        seen.extend(range(u["start_verse"],u["end_verse"]+1))
    assert seen==list(range(1,112))

def test_chapter5_assessment_maps_to_canonical_content():
    c=json.loads(CHAPTER.read_text(encoding="utf-8"))
    b=json.loads(BANK.read_text(encoding="utf-8"))
    refs={v["verse_id"] for v in c["verses"]}
    units={f'charaka.sutra.05.unit-{i:02d}' for i in range(1,len(c["learning_units"])+1)}
    assert b["assessment_id"]=="charaka.sutra.05.revision"
    assert len(b["questions"])==20
    assert len({q["content_refs"][0] for q in b["questions"]})==20
    assert all(q["content_refs"][0] in refs and q["content_refs"][1] in units for q in b["questions"])

def test_chapter5_reader_and_api_are_wired():
    reader=READER.read_text(encoding="utf-8")
    api=API.read_text(encoding="utf-8")
    assert "assessmentIdForChapter" in reader
    assert 'id+".revision"' in reader
    assert 'path == "/content/samhita"' in api
    assert "_seed_samhita_assessments(service, repo)" in api
