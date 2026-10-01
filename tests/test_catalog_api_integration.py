from pathlib import Path
import sqlite3

from aaptakosha_core.api import CatalogApi
from aaptakosha_core.curriculum_hierarchy_api import CurriculumHierarchyApi
from aaptakosha_core.curriculum_hierarchy_services import CurriculumHierarchyService
from aaptakosha_core.services import CatalogService
from aaptakosha_core.sqlite_repository import SQLiteCatalogRepository

ROOT = Path(__file__).resolve().parents[1]


def _api():
    connection = sqlite3.connect(":memory:")
    repo = SQLiteCatalogRepository(connection)
    for name in (
        "001_catalog.sql",
        "004_bams_content_layout.sql",
        "005_curriculum_hierarchy.sql",
        "006_first_professional_hierarchy.sql",
        "007_first_professional_data_quality.sql",
        "008_third_professional_paper_layout.sql",
    ):
        repo.apply_migrations(ROOT / "migrations" / name)
    return CatalogApi(CatalogService(repo)), CurriculumHierarchyApi(
        CurriculumHierarchyService(repo)
    )


def test_real_catalog_contains_all_three_professional_years():
    catalog, _ = _api()
    for curriculum_id, year in (
        ("bams_ncism_1", 1),
        ("bams_ncism_2", 2),
        ("bams_ncism_3", 3),
    ):
        result = catalog.get_curriculum(curriculum_id, "2021-22")
        assert result["status"] == 200
        assert result["data"]["professional_year"] == year
        assert result["data"]["subjects"]


def test_real_hierarchy_returns_nested_nodes():
    _, hierarchy = _api()
    roots = hierarchy.list_nodes("bams_ncism_2", "AyUG-DG", "2021-22")
    assert roots["status"] == 200
    assert roots["data"]["nodes"][0]["node_type"] == "paper"
    children = hierarchy.list_nodes(
        "bams_ncism_2", "AyUG-DG", "2021-22",
        roots["data"]["nodes"][0]["node_id"],
    )
    assert children["status"] == 200
    assert [node["name"] for node in children["data"]["nodes"]] == [
        "Dravyaguna Vigyana", "Dravya", "Guna", "Rasa"
    ]


def test_real_hierarchy_rejects_unknown_node():
    _, hierarchy = _api()
    result = hierarchy.get_node("does-not-exist", "bams_ncism_2", "2021-22")
    assert result["status"] == 404


def test_first_professional_verified_structure_is_present():
    _, hierarchy = _api()
    rs = hierarchy.list_nodes("bams_ncism_1", "AyUG-RS", "2021-22")
    assert [node["name"] for node in rs["data"]["nodes"]] == ["Paper I"]
    rs_units = hierarchy.list_nodes(
        "bams_ncism_1", "AyUG-RS", "2021-22", "y1-rs-paper1"
    )
    assert len(rs_units["data"]["nodes"]) == 8
    ks_units = hierarchy.list_nodes(
        "bams_ncism_1", "AyUG-KS", "2021-22", "y1-ks-paper1"
    )
    assert len(ks_units["data"]["nodes"]) == 10
    assert all(node["marks"] is None for node in ks_units["data"]["nodes"][3:8])


def test_third_professional_paper_layout_is_present():
    _, hierarchy = _api()
    expected = {
        "AyUG-KC": ["I", "II", "III"],
        "AyUG-PK": ["I"],
        "AyUG-ST": ["I", "II"],
        "AyUG-SL": ["I", "II"],
        "AyUG-PS": ["I", "II"],
        "AyUG-KB": ["I"],
        "AyUG-SA3": ["I"],
        "AyUG-RM": ["I"],
        "AyUG-EM": ["I"],
    }
    for subject_id, paper_codes in expected.items():
        roots = hierarchy.list_nodes("bams_ncism_3", subject_id, "2021-22")
        assert roots["status"] == 200
        assert [node["code"] for node in roots["data"]["nodes"]] == paper_codes
        assert all(node["node_type"] == "paper" for node in roots["data"]["nodes"])
