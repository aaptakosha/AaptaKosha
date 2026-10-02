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
    khanda_root = BASE / khanda
    matches = sorted(khanda_root.glob(f"chapter-{number:02d}-*/chapter.json"))
    assert len(matches) == 1, f"expected one chapter package for {khanda} {number}, found {matches}"
    return json.loads(matches[0].read_text(encoding="utf-8"))


def extent_candidates(chapter):
    raw = chapter.get("verse_extent")
    if raw is None:
        raw = chapter.get("verse_range")
    if raw is None:
        raw = chapter.get("chapter_extent")
    if raw is None and isinstance(chapter.get("verse_count"), int):
        return [f"1-{chapter['verse_count']}"]
    if isinstance(raw, str):
        return [raw]
    if isinstance(raw, dict):
        return [v for v in raw.values() if isinstance(v, str)]
    return []


def provenance_present(chapter):
    return bool(
        chapter.get("sources")
        or chapter.get("source_basis")
        or chapter.get("source_critical_note")
        or chapter.get("source_reconciliation")
        or chapter.get("canonical_policy")
        or chapter.get("canonical_source_policy")
    )


def transcription_state_present(chapter):
    payload = json.dumps(chapter, ensure_ascii=False).lower()
    explicit_fields = (
        "canonical_status",
        "source_critical_note",
        "source_reconciliation",
        "canonical_policy",
        "canonical_source_policy",
        "quality_gates",
        "next_gate",
    )
    return any(chapter.get(key) for key in explicit_fields) and (
        "pending" in payload
        or "partial" in payload
        or "anchor" in payload
        or "complete" in payload
        or "verified" in payload
        or "reconciled" in payload
        or "blocked" in payload
    )


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
            assert expected_extent in extent_candidates(chapter)


def test_source_reconciliation_and_transcription_state_are_explicit():
    for khanda, chapters in EXPECTED.items():
        for number in chapters:
            chapter = load(khanda, number)
            assert provenance_present(chapter), f"missing provenance for {khanda} {number}"
            assert transcription_state_present(chapter), f"missing explicit transcription state for {khanda} {number}"


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



def test_canonical_layers_or_verified_legacy_sanskrit_are_present():
    for khanda, chapters in EXPECTED.items():
        for number, (_, expected_extent) in chapters.items():
            chapter = load(khanda, number)
            start, end = (int(x) for x in expected_extent.split("-", 1))
            if chapter.get("canonical_sanskrit"):
                canonical = chapter["canonical_sanskrit"]
                assert len(canonical) == end - start + 1
                assert [v.get("verse_number") for v in canonical.values()] == list(range(start, end + 1))
                assert all(isinstance(v.get("text"), str) and v["text"].strip() for v in canonical.values())
            elif isinstance(chapter.get("verses"), list):
                verses = chapter["verses"]
                assert len(verses) == end - start + 1
                assert [v.get("verse_number", v.get("verse_no")) for v in verses] == list(range(start, end + 1))
                assert all(isinstance(v.get("text", v.get("sanskrit")), str) and v.get("text", v.get("sanskrit")).strip() for v in verses)
            elif isinstance(chapter.get("sanskrit_text"), str) and chapter["sanskrit_text"].strip():
                assert expected_extent in extent_candidates(chapter)
            else:
                assert transcription_state_present(chapter)
                payload = json.dumps(chapter, ensure_ascii=False).lower()
                assert "pending" in payload or "blocked" in payload
