import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "content" / "samhita" / "sarangadhara"

EXPECTED = {
    "purva": {
        1: ("paribhasha", "1-61"), 2: ("bhaishajyakhyanaka", "1-50"),
        3: ("nadiparikshvidhi", "1-41"), 4: ("dipanapachanadikathana", "1-35"),
        5: ("kaladikakhyana", "1-122"), 6: ("aharaadigati", "1-78"),
        7: ("rogaganana", "1-204"),
    },
    "madhyama": {
        1: ("swarasakalpana", "1-42"), 2: ("kvathakalpana", "1-176"),
        3: ("phantadikalpana", "1-12"), 4: ("himakalpana", "1-8"),
        5: ("kalkakalpana", "1-28"), 6: ("churnakalpana", "1-166"),
        7: ("vatakalpana", "1-105"), 8: ("avalehakalpana", "1-48"),
        9: ("ghrtatailakalpana", "1-210"), 10: ("asavarishtakalpana", "1-92"),
        11: ("dhatushodhanamaranakalpana", "1-104"),
        12: ("rasadishodhanamaranakalpana", "1-293"),
    },
    "uttara": {
        1: ("snehapanavidhi", "1-33"), 2: ("svedavidhi", "1-35"),
        3: ("vamanavidhi", "1-36"), 4: ("virecanavidhi", "1-49"),
        5: ("snehabastividhi", "1-51"), 6: ("niruhabastividhi", "1-35"),
        7: ("uttarabastividhi", "1-15"), 8: ("nasyavidhi", "1-63"),
        9: ("dhumapanavidhi", "1-25"), 10: ("gandushadividhi", "1-21"),
        11: ("lepamurdhatailakarnapuranavidhi", "1-152"),
        12: ("shonitasravavidhi", "1-45"), 13: ("netraprasadanavidhi", "1-128"),
    },
}


def load(khanda, number):
    slug, _ = EXPECTED[khanda][number]
    path = BASE / khanda / f"chapter-{number:02d}-{slug}" / "chapter.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_all_32_chapters_have_locked_identity_and_extent():
    assert sum(len(v) for v in EXPECTED.values()) == 32
    for khanda, chapters in EXPECTED.items():
        for number, (slug, expected_extent) in chapters.items():
            chapter = load(khanda, number)
            assert chapter["schema_version"] == "1.0"
            assert chapter["text_id"] == "sarangadhara"
            assert chapter["khand_id"] == khanda
            assert chapter["chapter_number"] == number
            assert chapter["chapter_id"].startswith(f"{khanda}-{number:02d}-")
            assert chapter["title_sanskrit"]
            assert chapter["title_roman"]
            assert chapter["canonical_status"]
            assert chapter["verse_extent"]["verified"] == expected_extent
            assert chapter["sources"]


def test_source_reconciliation_and_transcription_state_are_explicit():
    for khanda, chapters in EXPECTED.items():
        for number in chapters:
            chapter = load(khanda, number)
            status = chapter["canonical_status"].lower()
            note = json.dumps(chapter, ensure_ascii=False).lower()
            assert chapter["sources"]
            assert chapter.get("source_critical_note") or chapter.get("canonical_policy") or chapter.get("source_reconciliation")
            if "pending" in note or "partial" in note or "anchor" in note:
                assert any(token in status for token in ("partial", "source-reconciled", "verified", "printed"))
            else:
                assert status


def test_known_witness_discrepancies_are_explicit():
    checks = {
        ("madhyama", 10): ("1-92", "1-94"),
        ("madhyama", 12): ("1-293", "1-295"),
    }
    for (khanda, number), (online, printed) in checks.items():
        chapter = load(khanda, number)
        extent = chapter.get("verse_extent", {})
        assert extent.get("primary_online_witness") == online
        assert extent.get("printed_dipika_witness") == printed
        assert chapter.get("quality_gates", {}).get("numbering_discrepancy_preserved") is True
