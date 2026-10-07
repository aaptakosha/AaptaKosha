import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_samhita_registry_is_valid_and_nonempty():
    data = json.loads((ROOT / "content/samhita-registry.json").read_text(encoding="utf-8"))
    books = [b for c in data["library_sources"]["categories"] for b in c["books"]]
    assert data["version"] >= 1
    assert len(books) >= 1
    assert len({b["id"] for b in books}) == len(books)

def test_autopilot_is_additive_only():
    text = (ROOT / "scripts/samhita_autopilot.py").read_text(encoding="utf-8")
    assert "never deletes" in text
    assert "missing_source_content" in text
