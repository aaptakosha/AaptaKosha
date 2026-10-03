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
