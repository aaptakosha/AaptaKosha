from pathlib import Path
ROOT=Path(__file__).parents[1]
def read(p): return (ROOT/"frontend"/p).read_text(encoding="utf-8")
def test_samhita_landing_links_to_individual_text_pages():
    js=read("samhita.js")
    assert "samhita-detail.html?text=" in js
    assert 'href="./samhita-detail.html?text=' in js
def test_samhita_detail_is_section_only_and_section_links_are_dedicated():
    js=read("samhita-detail.js")
    assert "samhita-section.html?text=" in js
    assert "samhita-chapter.html?text=" in js
    assert "chapter-link" in js
def test_samhita_dedicated_pages_have_breadcrumbs_and_shared_navigation():
    for p in ("samhita-detail.html","samhita-section.html","samhita-chapter.html"):
        html=read(p)
        assert 'nav-list' in html
        assert 'samhitaBreadcrumb' in html or 'samhita-breadcrumb' in html
    study=read("samhita-study.js")
    assert 'samhita-section.html?text=' in study
    assert 'Samhita Library' in study


def test_generated_samhita_catalog_drives_discoverability():
    api=(ROOT/"api"/"content.py").read_text(encoding="utf-8")
    js=read("samhita-detail.js")
    assert 'query.get("catalog") == "1"' in api
    assert '"chapters": catalog()' in api
    assert 'generatedChapters' in js
    assert 'loadGeneratedCatalog' in js
    assert 'chapterIsAvailable' in js

def test_samhita_content_api_supports_generated_ashtanga_and_sharangadhara_ids():
    api=(ROOT/"api"/"content.py").read_text(encoding="utf-8")
    assert "ashtanga\\.hridaya" in api
    assert "sarangadhara|sharangadhara" in api


def test_sharangadhara_legacy_chapters_are_normalized():
    api=(ROOT/"api"/"content.py").read_text(encoding="utf-8")
    js=read("samhita-detail.js")
    assert 'payload.get("khand_id")' in api
    assert 'chapter_number' in api
    assert 'const chapters=chapterRows(selectedSection[2]);' in js


def test_legacy_samhita_payloads_are_normalized_for_reader():
    api=(ROOT/"api"/"content.py").read_text(encoding="utf-8")
    assert "def _normalize_payload" in api
    assert 'data["verses"] = verses' in api
    assert 'data["verse_count"] = len(verses)' in api
    assert 'data["content_id"] = content_id' in api
    assert "canonical_sanskrit" in api
    assert "sanskrit_text" in api
    assert "hindi_translation" in api


def test_sharangadhara_reader_preserves_all_three_khandas():
    detail=read("samhita-detail.js")
    assert '["Pūrva Khanda","purva"' in detail or '"purva",' in detail
    assert '"madhyama"' in detail
    assert '"uttara"' in detail
    study=read("samhita-study.js")
    assert 'text+ "." +section' not in study
    assert 'text+ "."+section' not in study
    assert 'text+"." +section' not in study


def test_existing_chapter_id_is_accepted_by_content_index():
    api=(ROOT/"api"/"content.py").read_text(encoding="utf-8")
    assert 'payload.get("chapter_id")' in api
    assert 'payload.get("chapter_no")' in api
    assert 'payload.get("adhyaya_no")' in api


def test_ashtanga_and_charaka_stored_chapters_have_stable_ids():
    import json
    checks = [
        ("content/samhita/ashtanga_hridaya/sutrasthana/adhyaya-01.json", "ashtanga.hridaya.sutra.01"),
        ("content/samhita/ashtanga_hridaya/sutrasthana/adhyaya-04.json", "ashtanga.hridaya.sutra.04"),
        ("content/samhita/charaka/sutrasthana/adhyaya-01.json", "charaka.sutra.01"),
        ("content/samhita/charaka/sutrasthana/adhyaya-12.json", "charaka.sutra.12"),
    ]
    for rel, expected in checks:
        payload=json.loads((ROOT/rel).read_text(encoding="utf-8"))
        assert payload.get("content_id") == expected or payload.get("chapter_id") == expected


def test_every_stored_samhita_chapter_file_is_indexed():
    import importlib.util
    import json
    api_path=ROOT/"api"/"content.py"
    spec=importlib.util.spec_from_file_location("aapta_content",api_path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    chapter_files=[]
    for path in (ROOT/"content"/"samhita").rglob("*.json"):
        if path.name=="chapter.json" or path.name.startswith("adhyaya-"):
            chapter_files.append(path)
    index=module._content_index()
    assert len(chapter_files)==48
    assert len([p for p in index.values() if p.is_file()])==48
    assert all(path.resolve() in {p.resolve() for p in index.values() if p.is_file()} for path in chapter_files)
    assert len(module.catalog())==48




def test_every_catalog_entry_resolves_through_reader_api():
    import importlib.util
    spec=importlib.util.spec_from_file_location("aapta_content",ROOT/"api"/"content.py")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entries=module.catalog()
    assert len(entries)==48
    for entry in entries:
        assert module.load_content(entry["content_id"]) is not None
        assert module.load_content(entry["content_id"])["content_id"]==entry["content_id"]


def test_sharangadhara_frontend_slug_resolves_to_canonical_api_ids():
    js=read("samhita-study.js")
    detail=read("samhita-detail.js")
    assert 'text+"."+section+"."+chapter' in js
    assert '"sharangadhara"' in detail
    assert "slugMatches(entry.text_slug)" in detail


def test_samhita_frontend_accepts_backend_text_slug_aliases_for_availability():
    js=read("samhita-detail.js")
    assert "TEXT_SLUG_ALIASES" in js
    assert '"sharangadhara":["sharangadhara","sarangadhara"]' in js
    assert '"ashtanga-hridaya":["ashtanga-hridaya","ashtanga.hridaya"]' in js
    assert "slugMatches(entry.text_slug)" in js
    assert "generatedChapters.has(slug+" not in js


def test_populated_catalog_sections_exist_in_frontend_maps():
    import importlib.util
    spec=importlib.util.spec_from_file_location("aapta_content",ROOT/"api"/"content.py")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    detail=read("samhita-detail.js")
    entries=module.catalog()
    populated=[e for e in entries if e["text_slug"] in {"charaka","ashtanga-hridaya","sharangadhara"}]
    assert populated
    for entry in populated:
        assert f'"{entry["section_key"]}"' in detail or f'"{entry["section_key"]},' in detail


def test_mapped_canonical_chapters_cannot_be_marked_unavailable_by_catalog_mismatch():
    js=read("samhita-detail.js")
    assert "const manuallyMapped=Array.isArray(selectedSection?.[3])" in js
    assert "const available=manuallyMapped||!catalogLoaded||chapterIsAvailable" in js
