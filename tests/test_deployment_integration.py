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
    assert "assessmentIdForChapter" in reader
    assert '"/api/content/samhita?content_id="' in reader
    assert 'id+".revision"' in reader
    assert "passages" in reader

def test_frontend_scripts_do_not_contain_known_broken_contracts():
    scripts = ["app.js", "ui-state.js", "assessment-results.js", "samhita-study.js"]
    for name in scripts:
        text = (ROOT / "frontend" / name).read_text(encoding="utf-8")
        assert "\\n\\n" not in text
    assert 'replace(/\\/+$/, "")' not in (ROOT / "frontend" / "app.js").read_text(encoding="utf-8")


def test_protected_api_initializes_lazily_and_uses_content_driven_assessments():
    api = (ROOT / "api" / "assessments.py").read_text(encoding="utf-8")
    assert "API, PROGRESS_API = build_api()" in api
    assert "def _get_apis():" in api
    assert "IDENTITY_PROVIDER = None" in api
    assert "def _get_identity_provider():" in api
    assert "_seed_samhita_chapter2_assessment" not in api
    assert "_seed_samhita_chapter12_assessment" not in api
    assert "_seed_samhita_assessments(service, repo)" in api
    assert "identity_provider_misconfigured" in api

def test_curriculum_subject_hierarchy_uses_the_inline_hierarchy_container():
    script = (ROOT / "frontend" / "curriculum.js").read_text(encoding="utf-8")
    assert 'const wrap=button.nextElementSibling;' in script
    assert 'button.parentElement.nextElementSibling' not in script
    assert 'wrap.hidden=true;' in script
    assert 'button.setAttribute("aria-expanded","true");' in script
def test_vercel_routes_curriculum_hierarchy_to_catalog_handler():
    import json
    config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    routes = {r["source"]: r["destination"] for r in config["rewrites"]}
    assert routes["/api/curriculum/:path*"] == "/api/catalog.py?route=curriculum/:path*"


def test_curriculum_hierarchy_has_direct_function_fallback_and_explicit_route():
    script = (ROOT / "frontend" / "curriculum.js").read_text(encoding="utf-8")
    assert 'new URL("/api/catalog.py",location.origin)' in script
    assert 'fallback.searchParams.set("route","curriculum/nodes")' in script
    config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    routes = {r["source"]: r["destination"] for r in config["rewrites"]}
    assert routes["/api/curriculum/nodes"] == "/api/catalog.py?route=curriculum/nodes"


def test_samhita_newline_renderer_uses_real_newline_regex():
    script = (ROOT / "frontend" / "samhita-study.js").read_text(encoding="utf-8")
    assert '.replace(/\\n/g,"<br>")' in script
    assert '.replace(/\\\\n/g,"<br>")' not in script
