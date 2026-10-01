from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_vercel_entrypoint_wires_assessment_service_to_persistent_progress():
    source = (ROOT / "api" / "assessments.py").read_text(encoding="utf-8")
    assert "progress_service = LearningProgressService(progress_repo)" in source
    assert "AssessmentService(repo, repo, progress_service)" in source


def test_assessment_service_syncs_attempt_lifecycle_when_progress_is_configured():
    source = (ROOT / "src" / "aaptakosha_core" / "assessment_services.py").read_text(encoding="utf-8")
    assert "self._sync_progress(saved)" in source
    assert "AssessmentProgressService(" in source
    assert 'RESOURCE_TYPE = "assessment"' in (ROOT / "src" / "aaptakosha_core" / "assessment_analytics.py").read_text(encoding="utf-8")


def test_results_page_uses_real_progress_and_notes_routes():
    html = (ROOT / "frontend" / "assessment-results.html").read_text(encoding="utf-8")
    assert 'href="./progress.html"' in html
    assert 'href="./notes.html"' in html
    assert 'href="#progress"' not in html
    assert 'href="#notes"' not in html


def test_progress_ui_excludes_assessment_resources_from_syllabus_percentage():
    source = (ROOT / "frontend" / "progress.js").read_text(encoding="utf-8")
    assert 'resource_type !== "assessment"' in source
    assert "tracked syllabus resources" in source


def test_progress_ui_loads_authenticated_assessment_analytics():
    source = (ROOT / "frontend" / "progress.js").read_text(encoding="utf-8")
    assert 'request("/analytics")' in source
    assert "data-assessment-average" in (ROOT / "frontend" / "progress.html").read_text(encoding="utf-8")
    assert "data-score-list" in source


def test_assessment_analytics_route_requires_authenticated_learner_identity():
    source = (ROOT / "src" / "aaptakosha_core" / "assessment_http_api.py").read_text(encoding="utf-8")
    assert 'parts == ["analytics"] and method == "GET"' in source
    assert "analytics_learner_id = learner_id or query.get(\"learner_id\")" in source
    assert '"authentication_required"' in source


def test_progress_ui_renders_live_overall_syllabus_metric():
    source = (ROOT / "frontend" / "progress.js").read_text(encoding="utf-8")
    html = (ROOT / "frontend" / "progress.html").read_text(encoding="utf-8")
    assert 'data-overall-progress' in html
    assert 'querySelector("[data-overall-progress]")' in source
    assert "tracked syllabus resources" in source


def test_progress_dashboard_does_not_ship_fake_live_metric_fallbacks():
    html = (ROOT / "frontend" / "progress.html").read_text(encoding="utf-8")
    assert 'data-overall-progress>42%' not in html
    assert 'data-assessment-average>78%' not in html
    assert 'Attempt 1 · 68%' not in html
