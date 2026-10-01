from pathlib import Path

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
