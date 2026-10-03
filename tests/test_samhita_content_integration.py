from pathlib import Path
import importlib.util

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("aaptakosha_api_content", ROOT / "api" / "content.py")
content_module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(content_module)
load_content = content_module.load_content

SARANGADHARA_EXTENTS = {"purva": 7, "madhyama": 12, "uttara": 13}


def test_charaka_resolver_remains_compatible():
    content = load_content("charaka.sutra.01")
    assert content is not None
    assert content["chapter_id"] == "charaka.sutra.01"
    assert content["adhyaya_no"] == 1
    assert content["verses"]


@pytest.mark.parametrize("khanda,number", [
    (khanda, number)
    for khanda, maximum in SARANGADHARA_EXTENTS.items()
    for number in range(1, maximum + 1)
])
def test_all_sarangadhara_chapter_ids_resolve(khanda, number):
    content = load_content(f"sarangadhara.{khanda}.{number:02d}")
    assert content is not None
    assert content["text_id"] == "sarangadhara"
    assert content["khand_id"] == khanda
    assert content["chapter_number"] == number
    assert content["chapter_id"].startswith(f"{khanda}-{number:02d}-")
    assert content["content_id"] == f"sarangadhara.{khanda}.{number:02d}"
    if not content["verses"]:
        assert content.get("canonical_status") in {"source_reconciled", "source_reconciled_printed_edition_primary", "printed_dipika_sequence_primary_source_reconciled", "printed_dipika_sequence_primary_source_reconciled_for_extent"}
        return


def test_representative_content_is_served_from_canonical_tree():
    checks = [
        ("sarangadhara.purva.01", "Paribhāṣākathanam"),
        ("sarangadhara.madhyama.09", "Ghṛtatailakalpanā"),
        ("sarangadhara.uttara.13", "Netraprasādanavidhi"),
    ]
    for content_id, expected_title in checks:
        content = load_content(content_id)
        assert content["title_roman"] == expected_title


@pytest.mark.parametrize("content_id", [
    "", "sarangadhara.other.01", "sarangadhara.purva.00",
    "sarangadhara.purva.999", "charaka.sutra.99",
    "../content/samhita/sarangadhara/purva/chapter-01-paribhasha/chapter.json",
    "charaka.sutra.01/../../sarangadhara/purva/chapter-01-paribhasha/chapter.json",
])
def test_unknown_or_unsafe_content_ids_are_rejected(content_id):
    assert load_content(content_id) is None


def test_sarangadhara_library_navigation_contract():
    frontend = (ROOT / "frontend" / "samhita.js").read_text(encoding="utf-8")
    assert "Sharangadhara Samhita" in frontend
    assert "sarangadharaChapters" in frontend
    assert "samhita-chapter.html?text=" in frontend
    for khanda in SARANGADHARA_EXTENTS:
        assert f'"{khanda}"' in frontend


def test_all_indexed_samhita_items_expose_sanskrit_text():
    """Every served verse/passage must render an actual Sanskrit source string."""
    entries = content_module.catalog()
    assert entries
    for entry in entries:
        content = load_content(entry["content_id"])
        items = content.get("verses") or content.get("passages") or []
        if not items:
            # Some chapters are deliberately metadata-only while controlled source transcription is pending.
            assert content.get("canonical_text_status") or content.get("canonical_import_plan") or content.get("canonical_status"), entry["content_id"]
            continue
        for item in items:
            assert str(item.get("sanskrit_original") or item.get("text") or item.get("sanskrit") or "").strip(), (entry["content_id"], item.get("verse_no"), item.get("passage_no"))


def test_mixed_ashtanga_passages_keep_verse_identity():
    for chapter in ("01", "02", "03"):
        content = load_content(f"ashtanga.hridaya.sutra.{chapter}")
        verses = [item for item in content["passages"] if item.get("type") == "verse"]
        assert verses
        assert all(str(item.get("sanskrit_original") or "").strip() for item in verses)


def test_tika_display_is_text_specific():
    frontend = (ROOT / "frontend" / "samhita-study.js").read_text(encoding="utf-8")
    assert 'charaka:[[' in frontend
    assert 'सर्वाङ्गसुन्दरी' in frontend
    assert 'आयुर्वेदरसायन' in frontend
    assert 'function tikaEntries' in frontend
