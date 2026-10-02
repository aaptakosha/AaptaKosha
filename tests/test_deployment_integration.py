import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_vercel_exposes_catalog_function_and_route():
    cfg = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    assert any(item.get("src") == "api/catalog.py" for item in cfg["builds"])
    assert any(item.get("source") == "/api/catalog/:path*" for item in cfg["rewrites"])

def test_reader_and_assessment_support_all_completed_charaka_chapters():
    reader = (ROOT / "frontend" / "samhita-study.js").read_text(encoding="utf-8")
    assessment = (ROOT / "frontend" / "assessment.js").read_text(encoding="utf-8")
    for n in range(1, 13):
        chapter = f"charaka.sutra.{n:02d}"
        assert chapter in reader
        assert chapter in assessment
    assert "charaka.sutra.12.revision" in reader
    assert "passages" in reader

def test_frontend_scripts_do_not_contain_known_broken_contracts():
    scripts = ["app.js", "ui-state.js", "assessment-results.js", "samhita-study.js"]
    for name in scripts:
        text = (ROOT / "frontend" / name).read_text(encoding="utf-8")
        assert "\\n\\n" not in text
    assert 'replace(/\\/+$/, "")' not in (ROOT / "frontend" / "app.js").read_text(encoding="utf-8")
