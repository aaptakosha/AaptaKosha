from aaptakosha_core.samhita_contract import SamhitaContractError, validate_samhita_chapter


def chapter():
    return {
        "schema_version": "1.0",
        "text": {"text_id": "charaka", "title": "Charaka Samhita", "language": "sa"},
        "sthana": {"id": "sutra", "number": 1, "title": "सूत्रस्थान"},
        "adhyaya": {"id": "charaka.sutra.01", "number": 1, "title": "दीर्घञ्जीवितीय", "verse_count": 2},
        "source_metadata": [{"source_id": "src.primary", "title": "Primary witness", "role": "canonical text"}],
        "verses": [
            {"verse_id": "charaka.sutra.01.001", "verse_no": 1, "canonical_sanskrit": "अथातो ...", "source_refs": ["src.primary"], "learning_unit_refs": ["lu.1"], "assessment_refs": ["a.1"]},
            {"verse_id": "charaka.sutra.01.002", "verse_no": 2, "canonical_sanskrit": "दीर्घं ...", "source_refs": ["src.primary"], "learning_unit_refs": ["lu.1"], "assessment_refs": ["a.1"]},
        ],
        "learning_units": [{"unit_id": "lu.1", "verse_refs": ["charaka.sutra.01.001", "charaka.sutra.01.002"], "title_hi": "आरम्भ"}],
        "assessment": [{"assessment_id": "a.1", "type": "mcq", "prompt": "क्या?", "content_refs": ["charaka.sutra.01.001"]}],
    }


def test_canonical_contract_accepts_valid_chapter():
    validate_samhita_chapter(chapter())


def test_contract_rejects_unknown_source():
    value = chapter()
    value["verses"][0]["source_refs"] = ["missing"]
    try:
        validate_samhita_chapter(value)
    except SamhitaContractError:
        return
    raise AssertionError("expected SamhitaContractError")


def test_contract_rejects_duplicate_verse_numbers():
    value = chapter()
    value["verses"][1]["verse_no"] = 1
    try:
        validate_samhita_chapter(value)
    except SamhitaContractError:
        return
    raise AssertionError("expected SamhitaContractError")
