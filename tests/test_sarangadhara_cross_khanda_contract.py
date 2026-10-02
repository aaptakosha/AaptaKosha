import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "content" / "samhita" / "sarangadhara"

EXPECTED = {
    "purva": {
        1: ("paribhasha", "1-61"),
        2: ("bhaishajyakhyanaka", "1-50"),
        3: ("nadiparikshvidhi", "1-41"),
        4: ("dipanapachanadikathana", "1-35"),
        5: ("kaladikakhyana", "1-122"),
        6: ("aharaadigati", "1-78"),
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


def end(value):
    return int(value.rsplit("-", 1)[1])


def test_all_32_chapters_have_locked_identity_and_extent():
    assert sum(len(v) for v in EXPECTED.values()) == 32
    for khanda, chapters in EXPECTED.items():
        for number, (slug, extent) in chapters.items():
            chapter = load(khanda, number)
            assert chapter["schema_version"] == "1.0"
            assert chapter["text_id"] == "sarangadhara"
            assert chapter["khand_id"] == khanda
            assert chapter["chapter_number"] == number
            assert chapter["chapter_id"].startswith(f"{khanda}-{number:02d}-")
            assert chapter["verse_extent"]["verified"] == extent
            assert chapter["colophon"]
            quality = chapter["quality_gates"]
            assert quality["chapter_identity_verified"] is True
            assert quality["colophon_verified"] is True
            assert quality["no_fabricated_missing_verses"] is True
            assert quality["one_chapter_one_commit"] is True
            assert chapter["learning_units"]
            assert chapter["assessments"]


def test_known_witness_discrepancies_are_explicit():
    checks = {
        ("purva", 2): ("1-50", "1-50"),
        ("purva", 6): ("1-78", None),
        ("purva", 7): ("1-204", None),
        ("madhyama", 10): ("1-92", "1-94"),
        ("madhyama", 12): ("1-293", "1-295"),
        ("uttara", 1): ("1-33", "1-35"),
        ("uttara", 3): ("1-33", "1-36"),
        ("uttara", 13): ("1-128", "1-129"),
    }
    for (khanda, number), (online, printed) in checks.items():
        chapter = load(khanda, number)
        extent = chapter["verse_extent"]
        assert end(extent.get("primary_online_witness", extent["verified"])) == end(online)
        if printed:
            assert end(extent.get("printed_dipika_witness", extent.get("printed_witness", online))) == end(printed)
            assert chapter["quality_gates"].get("numbering_discrepancy_preserved") is True or extent.get("discrepancy_note")


def test_partial_transcription_is_never_claimed_complete():
    for khanda, chapters in EXPECTED.items():
        for number in chapters:
            q = load(khanda, number)["quality_gates"]
            status = (q.get("canonical_full_verse_transcription") or q.get("full_verse_transcription") or "").lower()
            assert status
            if any(token in status for token in ("partial", "pending", "anchor", "source-reconciled")):
                assert "no_fabricated_missing_verses" in q or q.get("no_fabricated_missing_verses") is True
