from pathlib import Path


def test_postgres_seed_includes_classical_text_catalogue_and_latest_cleanup():
    source = Path("src/aaptakosha_core/postgres_curriculum_seed.py").read_text(encoding="utf-8")
    assert '(40,"third_professional_source_locator_cleanup")' in source
    assert 'SELECT text_id,canonical_name,display_name,text_type,collection,description,status,sort_order FROM classical_texts' in source
    assert 'SELECT text_id,professional_year FROM classical_text_professional_links' in source
    assert 'SELECT text_id,tag FROM classical_text_tags' in source
