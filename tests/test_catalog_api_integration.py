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
        "009_second_professional_paper_layout.sql",
        "010_first_professional_paper_layout.sql",
        "011_first_professional_padartha_paper2.sql",
        "012_first_professional_rachana_paper2.sql",
        "013_first_professional_kriya_paper2.sql",
        "014_correct_kriya_paper2_partb.sql",
        "015_first_professional_padartha_samhita_layout.sql",
        "016_first_professional_sanskrit_history_paper2.sql",
        "017_second_professional_samhita_layout.sql",
        "018_second_professional_agada_paper1.sql",
        "019_second_professional_roga_nidan_paper1.sql",
        "020_second_professional_dravyaguna_paper1.sql",
        "021_second_professional_rasashastra_layout.sql",
        "022_second_professional_swasthavritta_paper1.sql",
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


def test_second_professional_paper_layout_is_present():
    _, hierarchy = _api()
    expected = {
        "AyUG-RB": ["I", "II"],
        "AyUG-AT": ["I"],
        "AyUG-SA2": ["I"],
        "AyUG-DG": ["I", "II"],
        "AyUG-RN": ["I", "II"],
        "AyUG-SW": ["I", "II"],
    }
    for subject_id, paper_codes in expected.items():
        roots = hierarchy.list_nodes("bams_ncism_2", subject_id, "2021-22")
        assert roots["status"] == 200
        assert [node["code"] for node in roots["data"]["nodes"]] == paper_codes
        assert all(node["node_type"] == "paper" for node in roots["data"]["nodes"])
def test_first_professional_paper_layout_is_present():
    _, hierarchy = _api()
    expected = {
        "AyUG-PV": ["I", "II"],
        "AyUG-RS": ["I", "II"],
        "AyUG-KS": ["I", "II"],
        "AyUG-SN-AI": ["I", "II"],
        "AyUG-SA1": ["I"],
    }
    for subject_id, paper_codes in expected.items():
        roots = hierarchy.list_nodes("bams_ncism_1", subject_id, "2021-22")
        assert roots["status"] == 200
        assert [node["code"] for node in roots["data"]["nodes"]] == paper_codes
        assert all(node["node_type"] == "paper" for node in roots["data"]["nodes"])
def test_first_professional_padartha_paper2_units_are_present():
    _, hierarchy = _api()
    result = hierarchy.list_nodes(
        "bams_ncism_1", "AyUG-PV", "2021-22", "y1-pv-paper2"
    )
    assert result["status"] == 200
    assert [node["name"] for node in result["data"]["nodes"]] == [
        "Pariksha",
        "Aptopdesha Pariksha/Pramana",
        "Pratyaksha Pariksha/Pramana",
        "Anumana Pariksha/Pramana",
        "Yukti Pariksha/Pramana",
        "Upamana Pramana",
        "Karya-Karana Siddhanta",
    ]
def test_first_professional_rachana_paper2_units_are_present():
    _, hierarchy = _api()
    result = hierarchy.list_nodes(
        "bams_ncism_1", "AyUG-RS", "2021-22", "y1-rs-paper2"
    )
    assert result["status"] == 200
    assert [node["name"] for node in result["data"]["nodes"]] == [
        "Pramana Sharira",
        "Koshtha Evam Ashaya Sharira",
        "Sira Sharir",
        "Dhamani Sharir",
        "Strotas Shaarira",
        "Kala Shaarira",
        "Indriya Shaarira",
        "Twacha Sharir",
        "Marma Sharira",
    ]
def test_first_professional_kriya_paper2_structure_is_complete():
    _, hierarchy = _api()
    result = hierarchy.list_nodes(
        "bams_ncism_1", "AyUG-KS", "2021-22", "y1-ks2-paper2"
    )
    assert result["status"] == 200
    names = [node["name"] for node in result["data"]["nodes"]]
    assert names[:16] == [
        "Dhatu", "Rasa Dhatu", "Rakta Dhatu", "Mamsa Dhatu", "Meda Dhatu",
        "Asthi Dhatu", "Majja Dhatu", "Shukra Dhatu",
        "Concept of Ashraya-Ashrayi bhava", "Ojas", "Upadhatu",
        "Mala", "Indriya vidnyan", "Manas", "Atma", "Nidra & Swapna"
    ]
    assert names[16:] == [
        "Haemopoetic system", "Immunity",
        "Physiology of cardio-vascular system", "Muscle physiology",
        "Adipose tissue", "Physiology of male and female reproductive systems",
        "Physiology of Excretion", "Special Senses, Sleep and Dreams"
    ]
def test_first_professional_sanskrit_history_paper2_partitions():
    _, hierarchy = _api()
    result = hierarchy.list_nodes(
        "bams_ncism_1", "AyUG-SN-AI", "2021-22", "y1-snai-paper2"
    )
    assert result["status"] == 200
    assert [node["name"] for node in result["data"]["nodes"]] == [
        "Sanskrit", "Ayurved Itihas"
    ]
def test_first_professional_subjects_have_paper_roots():
    _, hierarchy = _api()
    expected = {
        "AyUG-SN-AI": ["I", "II"],
        "AyUG-PV": ["I", "II"],
        "AyUG-RS": ["I", "II"],
        "AyUG-KS": ["I", "II"],
        "AyUG-SA1": ["I"],
    }
    for subject_id, papers in expected.items():
        result = hierarchy.list_nodes(
            "bams_ncism_1", subject_id, "2021-22", None
        )
        assert result["status"] == 200
        roots = [
            node["code"] for node in result["data"]["nodes"]
            if node["node_type"] == "paper"
        ]
        assert roots == papers


def test_first_professional_samhita_advisory_structure_is_complete():
    _, hierarchy = _api()
    result = hierarchy.list_nodes(
        "bams_ncism_1", "AyUG-SA1", "2021-22", "y1-sa1-paper1"
    )
    assert result["status"] == 200
    assert [node["name"] for node in result["data"]["nodes"]] == [
        "Introduction to Samhita",
        "AH Su.1 Ayushkamiya Adhyaya",
        "AH Su.2 Dinacharya Adhyaya",
        "AH Su.3 Rutucarya Adhyaya",
        "AH Su.4 Roganutpadaniya Adhyaya",
        "AH Su.5 Dravadravya Vijnaniya Adhyaya",
        "AH Su.6 Annaswaroopa Vijnaneeya Adhyaya",
        "AH Su.7 Annaraksha Adhyaya",
        "AH Su.8 Matrashitiya Adhyaya",
        "AH Su.9 Dravyaadi Vijnaniya Adhyaya",
        "AH Su.10 Rasabhediya Adhyaya",
        "AH Su.11 Doshadi Vijnaniya Adhyaya",
        "AH Su.12 Doshabhediya Adhyaya",
        "AH Su.13 Doshopakramaniya Adhyaya",
        "AH Su.14 Dvividhopakramaniya Adhyaya",
        "AH Su.15 Shodhanadigana Sangraha Adhyaya",
        "Ch Su.1 Deerghanjiviteeya Adhyaya",
        "Ch Su.2 Apamarga Tanduliya Adhyaya",
        "Ch Su.3 Aragvadhiya Adhyaya",
        "Ch Su.4 Shadvirechana-shatashritiya Adhyaya",
        "Ch Su.5 Matrashiteeya Adhyaya",
        "Ch Su.6 Tasyashiteeya Adhyaya",
        "Ch Su.7 Naveganadharaniya Adhyaya",
        "Ch Su.8 Indriyopakramaniya Adhyaya",
        "Ch Su.9 Khuddakachatushpada Adhyaya",
        "Ch Su.10 Mahachatushpada Adhyaya",
        "Ch Su.11 Tisraishaniya Adhyaya",
        "Ch Su.12 Vatakalakaliya Adhyaya",
    ]


def test_second_professional_samhita_layout_contains_all_54_chapters():
    _, hierarchy = _api()
    result = hierarchy.list_nodes(
        "bams_ncism_2", "AyUG-SA2", "2021-22", "y2-sa2-paper1"
    )
    assert result["status"] == 200
    assert len(result["data"]["nodes"]) == 54
    assert result["data"]["nodes"][0]["code"] == "Cha.Su.13"
    assert result["data"]["nodes"][17]["code"] == "Cha.Su.30"
    assert result["data"]["nodes"][18]["code"] == "Cha.Ni.01"
    assert result["data"]["nodes"][25]["code"] == "Cha.Ni.08"
    assert result["data"]["nodes"][26]["code"] == "Cha.Vi.01"
    assert result["data"]["nodes"][33]["code"] == "Cha.Vi.08"
    assert result["data"]["nodes"][34]["code"] == "Cha.Sha.01"
    assert result["data"]["nodes"][41]["code"] == "Cha.Sha.08"
    assert result["data"]["nodes"][42]["code"] == "Cha.In.1"
    assert result["data"]["nodes"][53]["code"] == "Cha.In.12"


def test_second_professional_agada_paper1_structure_is_present():
    _, hierarchy = _api()
    result = hierarchy.list_nodes("bams_ncism_2", "AyUG-AT", "2021-22", "y2-at-paper1")
    assert result["status"] == 200
    assert len(result["data"]["nodes"]) == 20
    assert result["data"]["nodes"][0]["name"] == "Concepts of Agada Tantra"
    assert result["data"]["nodes"][-1]["name"] == "Sexual offences"


def test_second_professional_roga_nidan_paper1_structure_is_present():
    _, hierarchy = _api()
    result = hierarchy.list_nodes("bams_ncism_2", "AyUG-RN", "2021-22", "y2-rn-paper1")
    assert result["status"] == 200
    assert len(result["data"]["nodes"]) == 28
    assert result["data"]["nodes"][0]["name"].startswith("Roga nidana")
    assert result["data"]["nodes"][-1]["name"].startswith("Digital health")


def test_second_professional_dravyaguna_paper1_structure_is_present():
    _, hierarchy = _api()
    result = hierarchy.list_nodes("bams_ncism_2", "AyUG-DG", "2021-22", "y2-dg-paper1")
    assert result["status"] == 200
    assert len(result["data"]["nodes"]) == 22
    assert [n["name"] for n in result["data"]["nodes"][:7]] == ["Dravyaguna Vigyana", "Dravya", "Guna", "Rasa", "Vipaka", "Virya", "Prabhava"]
    assert result["data"]["nodes"][-1]["name"] == "Network pharmacology and Bioinformatics"


def test_second_professional_rasashastra_layout_is_present():
    _, hierarchy = _api()
    p1 = hierarchy.list_nodes("bams_ncism_2", "AyUG-RB", "2021-22", "y2-rb-paper1")
    p2 = hierarchy.list_nodes("bams_ncism_2", "AyUG-RB", "2021-22", "y2-rb-paper2")
    assert len(p1["data"]["nodes"]) == 14
    assert len(p2["data"]["nodes"]) == 12
    assert p1["data"]["nodes"][0]["name"].startswith("Chronological development")
    assert p2["data"]["nodes"][-1]["name"] == "Pharmacovigilance for Ayurveda drugs"


def test_second_professional_swasthavritta_paper1_structure_is_present():
    _, hierarchy = _api()
    result = hierarchy.list_nodes("bams_ncism_2", "AyUG-SW", "2021-22", "y2-sw-paper1")
    assert result["status"] == 200
    assert len(result["data"]["nodes"]) == 6
    assert result["data"]["nodes"][0]["code"] == "A"
    assert result["data"]["nodes"][-1]["code"] == "F"


def test_third_professional_kaumarabhritya_paper1_structure_is_present():
    _, hierarchy = _api()
    result = hierarchy.list_nodes("bams_ncism_3", "AyUG-KB", "2021-22", "y3-kb-paper1")
    assert result["status"] == 200
    assert len(result["data"]["nodes"]) == 9
    assert result["data"]["nodes"][0]["name"] == "Introduction to Kaumarabhritya"
    assert result["data"]["nodes"][-1]["name"].startswith("Graha Rogas")
