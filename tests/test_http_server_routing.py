from aaptakosha_core.http_server import AaptaKoshaHttpApi


class FakeAssessment:
    def handle(self, method, path, body=None, query=None):
        return {"status": 200, "data": {"route": path, "method": method}}


class FakeCatalog:
    def get_curriculum(self, curriculum_id, version=None):
        return {"status": 200, "data": {"curriculum_id": curriculum_id, "version": version}}

    def list_subjects(self, curriculum_id, version=None):
        return {"status": 200, "data": {"subjects": [], "curriculum_id": curriculum_id}}

    def get_subject(self, curriculum_id, subject_id, version=None):
        return {"status": 200, "data": {"subject_id": subject_id, "curriculum_id": curriculum_id}}


class FakeHierarchy:
    def list_nodes(self, curriculum_id, subject_id=None, version=None, parent_node_id=None):
        return {"status": 200, "data": {"nodes": [], "curriculum_id": curriculum_id, "subject_id": subject_id}}

    def get_node(self, node_id, curriculum_id=None, version=None):
        return {"status": 200, "data": {"node_id": node_id}}


def test_catalog_routes_are_reached():
    router = AaptaKoshaHttpApi(FakeAssessment(), FakeCatalog(), FakeHierarchy())

    result = router.handle("GET", "/api/catalog/bams_ncism_1", query={"version": "2021-22"})
    assert result["status"] == 200
    assert result["data"]["curriculum_id"] == "bams_ncism_1"

    result = router.handle("GET", "/api/catalog/bams_ncism_1/subjects")
    assert result["status"] == 200


def test_hierarchy_routes_are_reached_and_validate_curriculum_id():
    router = AaptaKoshaHttpApi(FakeAssessment(), FakeCatalog(), FakeHierarchy())

    result = router.handle(
        "GET",
        "/api/curriculum/nodes",
        query={"curriculum_id": "bams_ncism_2", "subject_id": "AyUG-DG", "version": "2021-22"},
    )
    assert result["status"] == 200
    assert result["data"]["curriculum_id"] == "bams_ncism_2"

    result = router.handle("GET", "/api/curriculum/nodes")
    assert result["status"] == 400


def test_existing_assessment_routes_remain_backward_compatible():
    router = AaptaKoshaHttpApi(FakeAssessment(), FakeCatalog(), FakeHierarchy())

    result = router.handle("GET", "/assessments", query={})
    assert result["status"] == 200
    assert result["data"]["route"] == "/assessments"

    result = router.handle("GET", "/api/assessments", query={})
    assert result["status"] == 200
    assert result["data"]["route"] == "/assessments"
