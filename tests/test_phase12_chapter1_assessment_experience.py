import json
import sqlite3
from pathlib import Path

from aaptakosha_core.assessment import Assessment, AssessmentAttempt, AssessmentQuestion, QuestionOption, SUBMITTED
from aaptakosha_core.assessment_learning_api import AssessmentLearningApi
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository
from aaptakosha_core.assessment_services import AssessmentService
from aaptakosha_core.assessment_analytics import AssessmentRevisionService
from aaptakosha_core.progress import LearningProgressService
from aaptakosha_core.progress_repository import SQLiteProgressRepository

ROOT = Path(__file__).parents[1]
BANK = ROOT / "content" / "assessments" / "charaka-sutra-01-ncism.json"
CHAPTER = ROOT / "content" / "samhita" / "charaka" / "sutrasthana" / "adhyaya-01.json"


def _api():
    conn = sqlite3.connect(":memory:")
    repo = SQLiteAssessmentRepository(conn)
    progress_repo = SQLiteProgressRepository(conn)
    repo.apply_migrations()
    progress_repo.apply_migrations()
    service = AssessmentService(repo, repo, LearningProgressService(progress_repo))
    payload = json.loads(BANK.read_text(encoding="utf-8"))
    assessment = Assessment(
        payload["assessment_id"], payload["title_hi"],
        curriculum_refs=tuple(payload["curriculum_refs"]),
        questions=tuple(
            AssessmentQuestion(
                q["question_id"], q["prompt"],
                tuple(QuestionOption(o["option_id"], o["text"], o["is_correct"]) for o in q["options"]),
                points=q["points"], content_refs=tuple(q["content_refs"]),
            )
            for q in payload["questions"]
        ),
    )
    service.create(assessment)
    service.publish(assessment.assessment_id)
    return AssessmentLearningApi(service)


def test_chapter1_full_attempt_returns_canonical_weak_shloka_refs():
    api = _api()
    started = api.start("charaka.sutra.01.ncism-revision", "learner")
    attempt_id = started["data"]["attempt"]["attempt_id"]
    saved = api.save_answers(
        attempt_id,
        "learner",
        (
            ("charaka.sutra.01.q01", ("b",)),
            ("charaka.sutra.01.q02", ("a",)),
        ),
    )
    assert saved["status"] == 200
    result = api.submit(attempt_id, "learner")
    assert result["status"] == 200
    assert result["data"]["maximum_score"] == 33
    assert result["data"]["score"] == 1
    q1 = next(x for x in result["data"]["breakdown"] if x["question_id"] == "charaka.sutra.01.q01")
    assert q1["is_correct"] is False
    assert "charaka.sutra.01.015" in q1["content_refs"]
    assert "charaka.sutra.01.unit-02" in q1["content_refs"]


def test_chapter1_revision_recommendation_is_same_canonical_verse():
    api = _api()
    started = api.start("charaka.sutra.01.ncism-revision", "learner")
    attempt_id = started["data"]["attempt"]["attempt_id"]
    api.save_answers(attempt_id, "learner", (("charaka.sutra.01.q01", ("b",)),))
    api.submit(attempt_id, "learner")
    rows = AssessmentRevisionService(
        api.service.assessment_repository,
        api.service.attempt_repository,
    ).recommendations("learner", content_id="charaka.sutra.01")
    assert any(row["content_ref"] == "charaka.sutra.01.015" for row in rows)


def test_chapter1_frontend_wires_test_and_results_actions():
    study_html = (ROOT / "frontend" / "samhita-study.html").read_text(encoding="utf-8")
    assessment_js = (ROOT / "frontend" / "assessment.js").read_text(encoding="utf-8")
    results_js = (ROOT / "frontend" / "assessment-results.js").read_text(encoding="utf-8")
    practice_js = (ROOT / "frontend" / "practice.js").read_text(encoding="utf-8")
    reader_js = (ROOT / "frontend" / "samhita-study.js").read_text(encoding="utf-8")
    assert "id=\"chapterActions\"" in study_html
    assert "charaka.sutra.01.ncism-revision" in reader_js
    assert "assessment_id" in assessment_js
    assert "weakShlokaList" in results_js
    assert "content_refs" in results_js
    assert "a.title" in practice_js
    assert "verse=" in reader_js
