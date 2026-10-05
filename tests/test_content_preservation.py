from pathlib import Path
import json
import tempfile
from aaptakosha_core.content_preservation import validate_content_preservation

def _tree(root: Path):
    (root / "content" / "samhita").mkdir(parents=True)
    (root / "content" / "samhita-registry.json").write_text(json.dumps({
        "version": 1, "entries": [{"content_id": "charaka.sutra.01",
        "path": "content/samhita/charaka/sutrasthana/adhyaya-01.json"}]}), encoding="utf-8")
    path = root / "content/samhita/charaka/sutrasthana/adhyaya-01.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"content_id":"charaka.sutra.01","verses":[{
        "verse_id":"sutra-01","verse_no":1,
        "sanskrit_original":"धर्मार्थकाममोक्षाणाम् आरोग्यं मूलमुत्तमम् ॥"}]}, ensure_ascii=False), encoding="utf-8")

def test_additive_content_is_allowed():
    with tempfile.TemporaryDirectory() as tmp:
        base, candidate = Path(tmp)/"base", Path(tmp)/"candidate"
        _tree(base); _tree(candidate)
        extra = candidate/"content/samhita/charaka/sutrasthana/adhyaya-02.json"
        extra.write_text('{"content_id":"charaka.sutra.02","verses":[]}', encoding="utf-8")
        assert validate_content_preservation(base, candidate) == []

def test_existing_registry_entry_cannot_disappear():
    with tempfile.TemporaryDirectory() as tmp:
        base, candidate = Path(tmp)/"base", Path(tmp)/"candidate"
        _tree(base); _tree(candidate)
        p=candidate/"content/samhita-registry.json"
        data=json.loads(p.read_text()); data["entries"]=[]
        p.write_text(json.dumps(data), encoding="utf-8")
        assert any(i.kind=="registry-entry-removed" for i in validate_content_preservation(base,candidate))

def test_existing_sanskrit_source_cannot_be_replaced():
    with tempfile.TemporaryDirectory() as tmp:
        base, candidate = Path(tmp)/"base", Path(tmp)/"candidate"
        _tree(base); _tree(candidate)
        p=candidate/"content/samhita/charaka/sutrasthana/adhyaya-01.json"
        data=json.loads(p.read_text()); data["verses"][0]["sanskrit_original"]="प्रतिस्थापित पाठ ॥"
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        assert any(i.kind=="source-text-changed" for i in validate_content_preservation(base,candidate))

def test_existing_verse_cannot_disappear():
    with tempfile.TemporaryDirectory() as tmp:
        base, candidate = Path(tmp)/"base", Path(tmp)/"candidate"
        _tree(base); _tree(candidate)
        p=candidate/"content/samhita/charaka/sutrasthana/adhyaya-01.json"
        data=json.loads(p.read_text()); data["verses"]=[]
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        assert any(i.kind=="verse-removed" for i in validate_content_preservation(base,candidate))
