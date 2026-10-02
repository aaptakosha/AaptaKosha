from aaptakosha_core.samhita_adapter import (
    from_charaka_legacy,
    from_sarangadhara_legacy,
)
from aaptakosha_core.samhita_contract import validate_samhita_chapter


def test_charaka_legacy_adapter_normalizes_verse_objects():
    legacy = {
        "chapter_id": "charaka.sutra.01",
        "title_hi": "दीर्घञ्जीवितीय अध्याय",
        "sthana": "सूत्रस्थान",
        "adhyaya_no": 1,
        "verse_count": 2,
        "source_metadata": [
            {"source": "Primary witness", "role": "primary", "locator": "https://example.test/charaka"},
        ],
        "learning_units": [
            {
                "start_verse": 1,
                "end_verse": 2,
                "title_hi": "अध्यायारम्भ",
                "explanation_hi": "भूमिका",
                "recitation_verses": [1],
            }
        ],
        "verses": [
            {
                "verse_id": "charaka.sutra.01.001",
                "verse_no": 1,
                "sanskrit_original": "अथातो दीर्घञ्जीवितीयम्",
                "translation_hi": "अब आरम्भ करते हैं।",
                "explanation_hi": "भूमिका।",
                "tika_hi": "अर्थ।",
                "recitation_status": "verified",
            },
            {
                "verse_id": "charaka.sutra.01.002",
                "verse_no": 2,
                "sanskrit_original": "दीर्घं जीवितमन्विच्छन्",
                "translation_hi": "दीर्घ जीवन की इच्छा से।",
                "explanation_hi": "प्रसंग।",
                "tika_hi": "अर्थ।",
            },
        ],
    }

    canonical = from_charaka_legacy(legacy)
    validate_samhita_chapter(canonical)
    assert canonical["verses"][0]["verse_id"] == "charaka.sutra.01.001"
    assert canonical["verses"][0]["source_refs"] == ["charaka.source.01"]
    assert canonical["verses"][0]["learning_unit_refs"] == ["charaka.sutra.01.unit.01"]


def test_sarangadhara_legacy_adapter_normalizes_sequence_and_assessments():
    legacy = {
        "text_id": "sarangadhara",
        "khand_id": "madhyama",
        "chapter_number": 1,
        "chapter_id": "madhyama-01-swarasakalpana",
        "title_sanskrit": "स्वरसादिकल्पना",
        "sources": [
            {"name": "Primary witness", "role": "primary", "url": "https://example.test/sarangadhara"},
            {"name": "Commentary witness", "role": "commentary"},
        ],
        "canonical_sanskrit": [
            {"verse_no": 1, "text": "रसः स्वरस इत्युक्तः"},
            {"verse_no": 2, "text": "कल्कः पेषितद्रव्यं"},
        ],
        "learning_units": [
            {"id": "LU1", "range": "1-2", "title": "पञ्च कषाय कल्पनाएँ"},
        ],
        "assessments": [
            {"type": "mcq", "question": "पञ्च कषाय कौन से हैं?", "answer": "स्वरसादि"},
        ],
        "quality_gates": {
            "online_sanskrit_witness_cross_checked": True,
            "verse_extent_verified": "1-2",
            "fabricated_missing_verses_avoided": True,
        },
        "commentary_mapping": [{"range": "1-2", "coverage": "commentary"}],
    }

    canonical = from_sarangadhara_legacy(legacy)
    validate_samhita_chapter(canonical)
    assert canonical["sthana"]["number"] == 2
    assert canonical["verses"][1]["verse_id"] == "sarangadhara.madhyama.01.002"
    assert canonical["assessment"][0]["content_refs"] == ["sarangadhara.madhyama.01.unit.01"]
