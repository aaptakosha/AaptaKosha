import sqlite3

from aaptakosha_core.assessment import Assessment, AssessmentAttempt, AssessmentQuestion, QuestionOption
from aaptakosha_core.assessment_analytics import AssessmentAnalyticsService
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository
from aaptakosha_core.assessment_services import AssessmentService
from aaptakosha_core.progress import COMPLETED, LearningProgressService


class InMemoryProgress:
    def __init__(self):
        self.items = {}

    def get(self, subject_id, resource_type, resource_id):
        return self.items.get((subject_id, resource_type, resource_id))

    def list_for_subject(self, subject_id):
        return tuple(
            value for value in self.items.values()
            if value.subject_id == subject_id
        )

    def save(self, progress):
        self.items[(progress.subject_id, progress.resource_type, progress.resource_id)] = progress
        return progress


def question():
    return AssessmentQuestion(
        "q1",
        "Which option is correct?",
        (
            QuestionOption("a", "Correct", is_correct=True),
            QuestionOption("b", "Incorrect"),
        ),
        points=2,
    )


def setup():
    repo = SQLiteAssessmentRepository(sqlite3.connect(":memory:"))
    repo.apply_migrations()
    progress = LearningProgressService(InMemoryProgress())
    service = AssessmentService(repo, repo, progress)
    service.create(Assessment("a1", "Assessment", questions=(question(),)))
    service.publish("a1")
    return repo, progress, service


def test_submitted_assessment_syncs_completed_learning_progress():
    repo, progress, service = setup()

    service.start_attempt(
        AssessmentAttempt("at1", "a1", "learner-1", answers=(("q1", ("a",)),))
    )
    service.submit_attempt("at1")

    saved = progress.get("learner-1", "assessment", "a1")
    assert saved is not None
    assert saved.status == COMPLETED
    assert saved.completion_percent == 100


def test_in_progress_assessment_syncs_in_progress_learning_state():
    repo, progress, service = setup()

    service.start_attempt(AssessmentAttempt("at1", "a1", "learner-1"))

    saved = progress.get("learner-1", "assessment", "a1")
    assert saved.status == "in_progress"
    assert saved.completion_percent == 0


def test_analytics_reports_best_and_latest_submitted_scores():
    repo, progress, service = setup()

    service.start_attempt(
        AssessmentAttempt("at1", "a1", "learner-1", answers=(("q1", ("b",)),))
    )
    service.submit_attempt("at1")

    service.start_attempt(
        AssessmentAttempt("at2", "a1", "learner-1", answers=(("q1", ("a",)),))
    )
    service.submit_attempt("at2")

    analytics = AssessmentAnalyticsService(repo, repo)
    summary = analytics.for_assessment("learner-1", "a1")

    assert summary.attempt_count == 2
    assert summary.submitted_attempt_count == 2
    assert summary.maximum_score == 2
    assert summary.best_score == 2
    assert summary.best_percent == 100
    assert summary.latest_score == 2


def test_analytics_is_scoped_to_learner():
    repo, progress, service = setup()

    service.start_attempt(
        AssessmentAttempt("at1", "a1", "learner-1", answers=(("q1", ("a",)),))
    )
    service.submit_attempt("at1")

    analytics = AssessmentAnalyticsService(repo, repo)
    summary = analytics.for_assessment("learner-2", "a1")

    assert summary.attempt_count == 0
    assert summary.submitted_attempt_count == 0
    assert summary.best_score == 0
    assert summary.latest_score is None


def test_analytics_lists_assessments_deterministically():
    repo, progress, service = setup()
    service.create(Assessment("a2", "Second", questions=(question(),)))
    service.publish("a2")

    service.start_attempt(AssessmentAttempt("at2", "a2", "learner-1"))
    service.start_attempt(AssessmentAttempt("at1", "a1", "learner-1"))

    analytics = AssessmentAnalyticsService(repo, repo)
    assert tuple(x.assessment_id for x in analytics.for_learner("learner-1")) == ("a1", "a2")
