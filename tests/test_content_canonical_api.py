from api.content import load_content


def test_canonical_api_format_for_charaka():
    content = load_content("charaka.sutra.01", canonical=True)
    assert content["schema_version"] == "1.0"
    assert len(content["verses"]) == 140
    assert content["verses"][0]["canonical_sanskrit"]
    assert content["verses"][0]["source_refs"]


def test_canonical_api_format_for_sarangadhara():
    content = load_content("sarangadhara.madhyama.01", canonical=True)
    assert content["schema_version"] == "1.0"
    assert len(content["verses"]) == 42
    assert content["sthana"]["number"] == 2


def test_default_api_format_remains_legacy():
    content = load_content("charaka.sutra.01")
    assert content["chapter_id"] == "charaka.sutra.01"
    assert "sanskrit_original" in content["verses"][0]
    assert "canonical_sanskrit" not in content["verses"][0]
