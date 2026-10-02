import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHAPTERS = {
    1: ("swarasakalpana", "1-42"), 2: ("kvathakalpana", "1-176"),
    3: ("phantadikalpana", "1-12"), 4: ("himakalpana", "1-8"),
    5: ("kalkakalpana", "1-28"), 6: ("churnakalpana", "1-166"),
    7: ("vatakalpana", "1-105"), 8: ("avalehakalpana", "1-48"),
    9: ("ghrtatailakalpana", "1-210"), 10: ("asavarishtakalpana", "1-92"),
    11: ("dhatushodhanamaranakalpana", "1-104"),
    12: ("rasadishodhanamaranakalpana", "1-293"),
}


def load_chapter(number):
    slug, _ = CHAPTERS[number]
    path = ROOT / "content" / "samhita" / "sarangadhara" / "madhyama" / f"chapter-{number:02d}-{slug}" / "chapter.json"
    return json.loads(path.read_text(encoding="utf-8"))


def extent_end(value):
    return int(value.split("-", 1)[1])


def test_madhyama_chapter_contracts():
    for number, (_, online_extent) in CHAPTERS.items():
        chapter = load_chapter(number)
        assert chapter["schema_version"] == "1.0"
        assert chapter["text_id"] == "sarangadhara"
        assert chapter["khand_id"] == "madhyama"
        assert chapter["chapter_number"] == number
        assert chapter["chapter_id"].startswith(f"madhyama-{number:02d}-")
        assert chapter["colophon"]
        assert chapter["learning_units"]
        if chapter.get("verse_extent"):
            extent = chapter["verse_extent"]
            observed = extent.get("online_sanskrit_witness") or extent.get("primary_online_witness") or extent.get("verified")
            if observed:
                assert extent_end(observed) == extent_end(online_extent)


def test_madhyama_witness_discrepancies_are_explicit():
    chapter10 = load_chapter(10)
    chapter12 = load_chapter(12)
    assert chapter10["verse_extent"]["status"] == "discrepant"
    assert chapter10["verse_extent"]["primary_online_witness"] == "1-92"
    assert chapter10["verse_extent"]["printed_dipika_witness"] == "1-94"
    assert chapter10["quality_gates"]["numbering_discrepancy_preserved"] is True
    assert chapter12["verse_extent"]["status"] == "discrepant"
    assert chapter12["verse_extent"]["primary_online_witness"] == "1-293"
    assert chapter12["verse_extent"]["printed_dipika_witness"] == "1-295"
    assert chapter12["quality_gates"]["numbering_discrepancy_preserved"] is True


def test_madhyama_transcription_is_not_silent_or_misrepresented():
    for number in CHAPTERS:
        quality = load_chapter(number)["quality_gates"]
        transcription = quality.get("canonical_full_verse_transcription") or quality.get("full_verse_transcription")
        assert transcription
        lowered = transcription.lower()
        assert any(token in lowered for token in ("full", "pending", "partial", "source-reconciled", "anchor"))


def test_madhyama_hazardous_materials_keep_safety_separation():
    for number in (10, 11, 12):
        chapter = load_chapter(number)
        reconciliation = chapter.get("source_reconciliation", {})
        safety = reconciliation.get("safety_note", "")
        assert safety
        assert "historical" in safety.lower() or "classical" in safety.lower()
