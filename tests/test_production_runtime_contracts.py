from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_read_only_content_is_separate_from_authenticated_assessment_function():
    cfg=json.loads((ROOT/"vercel.json").read_text(encoding="utf-8"))
    assert any(x.get("src")=="api/content.py" for x in cfg["builds"])
    assert any(x.get("source")=="/api/content/:path*" for x in cfg["rewrites"])
    assert "REQUIRE_IDENTITY" not in (ROOT/"api/content.py").read_text(encoding="utf-8")

def test_catalog_has_unseeded_postgres_snapshot_fallback():
    text=(ROOT/"api/catalog.py").read_text(encoding="utf-8")
    assert 'get_curriculum("bams_ncism_1", "2021-22")' in text
    assert "SQLiteCatalogRepository" in text


def test_catalog_runtime_initialization_is_lazy():
    text=(ROOT/"api/catalog.py").read_text(encoding="utf-8")
    assert "def _get_apis():" in text
    assert "psycopg.connect(DATABASE_URL)" in text
    assert "CATALOG_API, HIERARCHY_API = _get_apis()" in text
    assert "class handler(BaseHTTPRequestHandler):" in text
