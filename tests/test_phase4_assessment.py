import pytest

from aaptakosha_core.assessment import (
    Assessment,
    AssessmentAttempt,
    AssessmentQuestion,
    DRAFT,
    PUBLISHED,
    QuestionOption,
    SUBMITTED,
    score_attempt,
)


def question():
    return AssessmentQuestion(
        "q1",
        "Which is correct?",
        (
            QuestionOption("a", "First", True),
            QuestionOption("b", "Second"),
        ),
        points=2,
    )


def test_assessment_contract_rejects_invalid_questions():
    with pytest.raises(ValueError):
        AssessmentQuestion("q1", "Prompt", (), 1)
    with pytest.raises(ValueError):
        AssessmentQuestion("q1", "Prompt", (QuestionOption("a", "A"),), 1)


def test_assessment_contract_requires_unique_questions():
    q = question()
    with pytest.raises(ValueError):
        Assessment("a1", "Test", questions=(q, q))


def test_deterministic_scoring_of_submitted_attempt():
    assessment = Assessment("a1", "Test", status=PUBLISHED, questions=(question(),))
    attempt = AssessmentAttempt("at1", "a1", "learner-1", status=SUBMITTED, answers=(("q1", ("a",)),))
    assert score_attempt(assessment, attempt) == 2


def test_partial_or_incorrect_answer_scores_zero_for_question():
    assessment = Assessment("a1", "Test", status=PUBLISHED, questions=(question(),))
    attempt = AssessmentAttempt("at1", "a1", "learner-1", status=SUBMITTED, answers=(("q1", ("b",)),))
    assert score_attempt(assessment, attempt) == 0


def test_scoring_requires_submitted_matching_attempt():
    assessment = Assessment("a1", "Test", status=DRAFT, questions=(question(),))
    attempt = AssessmentAttempt("at1", "a1", "learner-1", status="in_progress")
    with pytest.raises(ValueError):
        score_attempt(assessment, attempt)
