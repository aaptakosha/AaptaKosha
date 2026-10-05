from pathlib import Path
import re

ROOT = Path(__file__).parents[1] / "frontend"


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_shared_ui_state_is_loaded_before_feature_scripts():
    for name in ("progress.html", "assessment.html", "practice.html"):
        html = read(name)
        assert 'src="./ui-state.js"' in html
    assert read("practice.html").index('src="./ui-state.js"') < read("practice.html").index('src="./assessment-flow.js"')


def test_primary_learner_navigation_uses_real_routes():
    for name in ("index.html", "learn.html", "practice.html", "assessment.html", "progress.html", "notes.html"):
        html = read(name)
        assert 'href="./learn.html"' in html or name == "learn.html"
        assert 'href="./progress.html"' in html or name == "progress.html"


def test_protected_flows_use_shared_api_and_session_bootstrap():
    for name in ("assessment.html", "progress.html", "practice.html"):
        html = read(name)
        assert 'src="./api-client.js"' in html
        assert 'src="./session.js"' in html


def test_shared_state_helper_exports_public_contract():
    js = read("ui-state.js")
    assert "window.AaptaKoshaUi" in js
    assert "busy" in js and "status" in js and "empty" in js


def test_clerk_session_bootstrap_uses_safe_config_and_sdk():
    session = read("session.js")
    api = (Path(__file__).parents[1] / "api" / "assessments.py").read_text(encoding="utf-8")
    assert "fetch(" in session and "/api/config" in session
    assert 'clerk-js@6/dist/clerk.browser.js' in session
    assert 'CLERK_PUBLISHABLE_KEY' in api
    assert 'CLERK_SECRET_KEY' not in session
    assert 'clerk_publishable_key' in api


def test_authenticated_flows_do_not_accept_browser_selected_learner_ids():
    flow = read("assessment-flow.js")
    progress = read("progress.js")
    session = read("session.js")
    assert "AAPTAKOSHA_LEARNER_ID" not in flow
    assert 'requestLearnerPayload()' in flow
    assert '"/progress"' in progress
    assert '"/progress?subject_id=' not in progress
    assert 'window.AAPTAKOSHA_API_BASE || (window.AaptaKoshaSession && window.AaptaKoshaSession.authenticated)' in flow
    assert re.search(r"subjectId\s*:\s*clerk\??\.user\??\.id\s*\|\|\s*null", session)
    assert 'window.AaptaKoshaSessionReady' in progress
    assert 'window.AaptaKoshaUi?.status' in progress

def test_backend_identity_boundary_is_authoritative():
    root = Path(__file__).parents[1]
    assessment = (root / "src" / "aaptakosha_core" / "assessment_http_api.py").read_text(encoding="utf-8")
    progress = (root / "src" / "aaptakosha_core" / "progress_http_api.py").read_text(encoding="utf-8")

    assert "require_identity" in assessment
    assert '"authentication_required"' in assessment
    assert "principal.subject_id" in assessment
    assert '"learner_identity_mismatch"' in assessment
    assert "require_identity" in progress
    assert '"authentication_required"' in progress
    assert "principal.subject_id" in progress
    assert '"learner_identity_mismatch"' in progress

def test_results_refresh_prefers_authenticated_live_result_and_surfaces_failures():
    js = read("assessment-results.js")
    html = read("assessment-results.html")
    assert "window.AaptaKoshaSessionReady" in js
    assert "auth||!r" in js
    assert "const live=await api.result(id)" in js
    assert 'window.AaptaKoshaUi?.status' in js
    assert 'src="./ui-state.js"' in html
    assert 'data-ui-state' in html

def test_vercel_entrypoint_requires_identity_and_keeps_secret_server_side():
    root = Path(__file__).parents[1]
    entrypoint = (root / "api" / "assessments.py").read_text(encoding="utf-8")
    assert "REQUIRE_IDENTITY" in entrypoint
    assert 'os.environ.get("VERCEL")' in entrypoint
    assert 'CLERK_SECRET_KEY' not in entrypoint.split('publishable_key =', 1)[0]
    assert '"identity_provider_not_configured"' in entrypoint

def test_ncism_curriculum_renderer_exposes_three_professional_years():
    js = read("curriculum.js")
    assert 'curriculum_id:"bams_ncism_1"' in js
    assert 'curriculum_id:"bams_ncism_2"' in js
    assert 'curriculum_id:"bams_ncism_3"' in js
    assert 'year1.html?curriculum_id=' in js

def test_ncism_subject_search_matches_visible_year_name():
    js = read("curriculum.js")
    assert 'years.filter' in js
    assert 'y.label+" "+y.note' in js
