from pathlib import Path
ROOT=Path(__file__).parents[1]
def read(p): return (ROOT/"frontend"/p).read_text(encoding="utf-8")
def test_curriculum_landing_has_only_year_links():
    html=read("curriculum.html")
    assert 'id="yearGrid"' in html
    assert 'curriculum.js' in html
    js=read("curriculum.js")
    assert 'year1.html' in js and 'year2.html' in js and 'year3.html' in js
    assert 'subjectCard(' not in js
    assert 'fetchHierarchyNodes' not in js
def test_professional_pages_exist_and_use_shared_renderer():
    for name in ("year1.html","year2.html","year3.html","subject.html","chapter.html"):
        html=read(name)
        assert 'curriculum-pages.js' in html
        assert 'id="curriculumPage"' in html
def test_curriculum_renderer_produces_breadcrumb_back_and_page_links():
    js=read("curriculum-pages.js")
    assert 'function crumbs(' in js
    assert 'class="back-link"' in js
    assert './subject.html?' in js
    assert './chapter.html?' in js
