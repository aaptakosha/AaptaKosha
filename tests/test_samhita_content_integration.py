from pathlib import Path

import pytest

from api.content import _safe_json_path, load_content

ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOT = ROOT / "content" / "samhita"

SARANGADHARA_EXTENTS = {"purva": 7, "madhyama": 12, "uttara": 13}


def test_charaka_resolver_remains_compatible():
    content = load_content("charaka.sutra.01")
    assert content is not None
    assert content["text_id"] == "charaka"
    assert content["chapter_number"] == 1


@pytest.mark.parametrize(
    "khanda,number",
    [
        (khanda, number)
        for khanda, max_number in SARANGADHARA_EXTENTS.items()
        for number in range(1, max_number + 1)
    ],
)
def test_all_sarangadhara_chapter_ids_resolve(khanda, number):
    content = load_content(f"sarangadhara.{khanda}.{number:02d}")
    assert content is not None
    assert content["text_id"] == "sarangadhara"
    assert content["khand_id"] == khanda
    assert content["chapter_number"] == number
    assert content["chapter_id"].startswith(f"{khanda}-{number:02d}-")
    assert content["learning_units"]
    assert content["assessments"]


def test_representative_content_is_served_from_canonical_tree():
    checks = [
        ("sarangadhara.purva.01", "Paribhāṣākathanam"),
        ("sarangadhara.madhyama.09", "Ghṛta-tailakalpanā"),
        ("sarangadhara.uttara.13", "Netraprasādanavidhi"),
    ]
    for content_id, expected_title in checks:
        content = load_content(content_id)
        assert content["title_roman"] == expected_title


@pytest.mark.parametrize(
    "content_id",
    [
        "",
        "sarangadhara.other.01",
        "sarangadhara.purva.00",
        "sarangadhara.purva.999",
        "charaka.sutra.99",
        "../content/samhita/sarangadhara/purva/chapter-01-paribhasha/chapter.json",
        "charaka.sutra.01/../../sarangadhara/purva/chapter-01-paribhasha/chapter.json",
    ],
)
def test_unknown_or_unsafe_content_ids_are_rejected(content_id):
    assert _safe_json_path(content_id) is None
    assert load_content(content_id) is None


def test_sarangadhara_library_navigation_contract():
    frontend = (ROOT / "frontend" / "samhita.js").read_text(encoding="utf-8")
    assert "Sharangadhara Samhita" in frontend
    assert "sarangadharaChapters" in frontend
    for khanda in SARANGADHARA_EXTENTS:
        assert f"chapter=sarangadhara.{khanda}." in frontend
