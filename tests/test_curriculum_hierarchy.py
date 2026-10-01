from aaptakosha_core import (
    CurriculumHierarchyApi,
    CurriculumHierarchyService,
    SQLiteCatalogRepository,
)


def _repo_with_nodes(tmp_path):
    repo = SQLiteCatalogRepository(tmp_path / "catalog.db")
    repo.apply_migrations("migrations/001_catalog.sql")
    repo.apply_migrations("migrations/004_bams_content_layout.sql")
    repo.apply_migrations("migrations/005_curriculum_hierarchy.sql")
    return repo


def test_hierarchy_lists_root_nodes_and_children(tmp_path):
    repo = _repo_with_nodes(tmp_path)
    try:
        service = CurriculumHierarchyService(repo)
        roots = service.list_nodes("bams_ncism_2", "AyUG-DG", "2021-22")
        assert [n.node_id for n in roots] == ["y2-dg-paper1"]
        children = service.children("bams_ncism_2", "y2-dg-paper1", "AyUG-DG", "2021-22")
        assert [n.name for n in children] == ["Dravyaguna Vigyana", "Dravya", "Guna", "Rasa"]
    finally:
        repo.close()


def test_hierarchy_api_returns_serializable_nodes(tmp_path):
    repo = _repo_with_nodes(tmp_path)
    try:
        api = CurriculumHierarchyApi(CurriculumHierarchyService(repo))
        response = api.list_nodes("bams_ncism_1", "AyUG-PV", "2021-22")
        assert response["status"] == 200
        assert response["data"]["nodes"][0]["node_type"] == "paper"
        assert response["data"]["nodes"][0]["name"] == "Paper I"
    finally:
        repo.close()


def test_hierarchy_api_returns_404_for_missing_node(tmp_path):
    repo = _repo_with_nodes(tmp_path)
    try:
        api = CurriculumHierarchyApi(CurriculumHierarchyService(repo))
        response = api.get_node("does-not-exist")
        assert response["status"] == 404
    finally:
        repo.close()
