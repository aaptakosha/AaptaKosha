from aaptakosha_core import Curriculum, Subject, Topic


def test_catalog_contract_is_immutable_and_structured():
    topic = Topic("T-001", "Introduction")
    subject = Subject("S-001", "Padartha Vijnana", (topic,))
    curriculum = Curriculum("BAMS-UG", "2026.1", 2, (subject,))

    assert curriculum.subjects[0].topics[0].topic_id == "T-001"


def test_catalog_rejects_duplicate_subject_ids():
    subject = Subject("S-001", "One")

    try:
        Curriculum("BAMS-UG", "2026.1", 2, (subject, subject))
    except ValueError as exc:
        assert "unique subject_id" in str(exc)
    else:
        raise AssertionError("duplicate subject IDs must be rejected")


def test_catalog_rejects_invalid_professional_year():
    try:
        Curriculum("BAMS-UG", "2026.1", 0)
    except ValueError as exc:
        assert "professional_year" in str(exc)
    else:
        raise AssertionError("invalid professional year must be rejected")
