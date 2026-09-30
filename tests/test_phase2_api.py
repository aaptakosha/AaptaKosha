from aaptakosha_core.api import CatalogApi
from aaptakosha_core.catalog import Curriculum, Subject, Topic
from aaptakosha_core.services import CatalogService


class Repo:
    def __init__(self):
        self.curriculum = Curriculum(
            "bams-ug",
            "2026.1",
            2,
            (
                Subject("dravyaguna", "Dravyaguna", (Topic("dg-1", "Rasa"),)),
            ),
        )

    def get_curriculum(self, curriculum_id, version=None):
        if curriculum_id != "bams-ug" or (version and version != "2026.1"):
            return None
        return self.curriculum

    def list_subjects(self, curriculum_id, version=None):
        return self.curriculum.subjects if self.get_curriculum(curriculum_id, version) else ()

    def get_subject(self, curriculum_id, subject_id, version=None):
        if not self.get_curriculum(curriculum_id, version):
            return None
        return next((s for s in self.curriculum.subjects if s.subject_id == subject_id), None)


def api():
    return CatalogApi(CatalogService(Repo()))


def test_curriculum_response_is_serializable_and_stable():
    response = api().get_curriculum("bams-ug")
    assert response["status"] == 200
    assert response["data"]["curriculum_id"] == "bams-ug"
    assert response["data"]["subjects"][0]["topics"][0] == {"topic_id": "dg-1", "name": "Rasa"}


def test_subject_list_response():
    response = api().list_subjects("bams-ug")
    assert response == {
        "status": 200,
        "data": {
            "subjects": [
                {
                    "subject_id": "dravyaguna",
                    "name": "Dravyaguna",
                    "topics": [{"topic_id": "dg-1", "name": "Rasa"}],
                }
            ]
        },
    }


def test_missing_resources_map_to_not_found():
    assert api().get_curriculum("missing")["status"] == 404
    assert api().get_subject("bams-ug", "missing")["error"]["code"] == "not_found"
