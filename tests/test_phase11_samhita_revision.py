import sqlite3
from pathlib import Path

from aaptakosha_core.assessment import Assessment, AssessmentAttempt, AssessmentQuestion, QuestionOption, SUBMITTED
from aaptakosha_core.assessment_analytics import AssessmentRevisionService
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository
from aaptakosha_core.assessment_services import AssessmentService
from aaptakosha_core.progress import LearningProgressService
from aaptakosha_core.progress_repository import SQLiteProgressRepository

ROOT = Path(__file__).parents[1]


def _fixture():
    conn = sqlite3.connect(":memory:")
    repo = SQLiteAssessmentRepository(conn)
    progress_repo = SQLiteProgressRepository(conn)
    repo.apply_migrations()
    progress_repo.apply_migrations()
    service = AssessmentService(repo, repo, LearningProgressService(progress_repo))
    assessment = Assessment(
        "charaka.sutra.01.ncism-revision",
        "Charaka Sutrasthana 1",
        questions=(
            AssessmentQuestion(
                "q1", "verse 15",
                (QuestionOption("a", "correct", True), QuestionOption("b", "wrong")),
                content_refs=("charaka.sutra.01.015", "charaka.sutra.01.unit-02"),
            ),
            AssessmentQuestion(
                "q2", "verse 24",
                (QuestionOption("a", "correct", True), QuestionOption("b", "wrong")),
                content_refs=("charaka.sutra.01.024", "charaka.sutra.01.unit-04"),
            ),
        ),
    )
    service.create(assessment)
    service.publish(assessment.assessment_id)
    return conn, repo, service


def test_revision_recommendations_map_missed_questions_to_canonical_refs():
    conn, repo, service = _fixture()
    # Persist a submitted fixture directly; lifecycle submission is covered elsewhere.
    repo.save(AssessmentAttempt("a1", "charaka.sutra.01.ncism-revision", "learner", SUBMITTED, (
        ("q1", ("b",)),
        ("q2", ("a",)),
    )))
    rows = AssessmentRevisionService(repo, repo).recommendations(
        "learner", content_id="charaka.sutra.01"
    )
    assert [row["content_ref"] for row in rows] == [
        "charaka.sutra.01.015",
        "charaka.sutra.01.unit-02",
    ]
    assert all(row["mastery_percent"] == 0 for row in rows)


def test_revision_recommendations_remove_mastered_refs():
    conn, repo, service = _fixture()
    repo.save(AssessmentAttempt("a1", "charaka.sutra.01.ncism-revision", "learner", SUBMITTED, (
        ("q1", ("a",)),
        ("q2", ("a",)),
    )))
    rows = AssessmentRevisionService(repo, repo).recommendations(
        "learner", content_id="charaka.sutra.01"
    )
    assert rows == ()
