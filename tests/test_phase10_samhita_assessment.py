import json
from pathlib import Path

from aaptakosha_core.assessment import PUBLISHED
from aaptakosha_core.assessment_repository import SQLiteAssessmentRepository
from aaptakosha_core.assessment_services import AssessmentService

ROOT = Path(__file__).parents[1]
BANK = ROOT / "content" / "assessments" / "charaka-sutra-01-ncism.json"
CHAPTER = ROOT / "content" / "samhita" / "charaka" / "sutrasthana" / "adhyaya-01.json"


def test_ncism_assessment_bank_has_all_required_recitation_verses():
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    chapter = json.loads(CHAPTER.read_text(encoding="utf-8"))
    refs = {v["verse_id"] for v in chapter["verses"]}
    assert bank["assessment_id"] == "charaka.sutra.01.ncism-revision"
    assert bank["question_count"] == 33
    assert len(bank["questions"]) == 33
    assert {q["verse_no"] for q in bank["questions"]} == set(chapter["recitation_verses"])
    assert all(ref in refs or ".unit-" in ref for q in bank["questions"] for ref in q["content_refs"])
    assert all(sum(o["is_correct"] for o in q["options"]) == 1 for q in bank["questions"])


def test_ncism_assessment_bank_can_be_seeded_and_published():
    import sqlite3
    conn = sqlite3.connect(":memory:")
    repo = SQLiteAssessmentRepository(conn)
    repo.apply_migrations()
    service = AssessmentService(repo, repo)
    payload = json.loads(BANK.read_text(encoding="utf-8"))
    from aaptakosha_core.assessment import Assessment, AssessmentQuestion, QuestionOption
    assessment = Assessment(
        payload["assessment_id"], payload["title_hi"],
        curriculum_refs=tuple(payload["curriculum_refs"]),
        questions=tuple(
            AssessmentQuestion(
                q["question_id"], q["prompt"],
                tuple(QuestionOption(o["option_id"], o["text"], o["is_correct"]) for o in q["options"]),
                points=q["points"], content_refs=tuple(q["content_refs"]),
            ) for q in payload["questions"]
        ),
    )
    service.create(assessment)
    published = service.publish(assessment.assessment_id)
    assert published.status == PUBLISHED
    assert len(published.questions) == 33
