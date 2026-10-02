from aaptakosha_core import CatalogNotFoundError, CatalogService, Curriculum, Subject, Topic

class InMemoryCatalog:
    def __init__(self):
        self.curriculum = Curriculum("BAMS-UG","2026.1",2,(Subject("S-001","Padartha Vijnana",(Topic("T-001","Introduction"),)),Subject("S-002","Dravyaguna")))
    def get_curriculum(self, curriculum_id, version=None):
        if curriculum_id != self.curriculum.curriculum_id or (version is not None and version != self.curriculum.version): return None
        return self.curriculum
    def list_subjects(self, curriculum_id, version=None): return self.curriculum.subjects
    def get_subject(self, curriculum_id, subject_id, version=None): return next((s for s in self.curriculum.subjects if s.subject_id == subject_id), None)

def test_service_returns_catalog_data():
    service = CatalogService(InMemoryCatalog())
    assert service.get_curriculum("BAMS-UG","2026.1").version == "2026.1"
    assert [s.subject_id for s in service.list_subjects("BAMS-UG","2026.1")] == ["S-001","S-002"]
    assert service.get_subject("BAMS-UG","S-001","2026.1").topics[0].topic_id == "T-001"

def test_missing_curriculum_is_explicit():
    try: CatalogService(InMemoryCatalog()).get_curriculum("UNKNOWN")
    except CatalogNotFoundError as exc: assert "curriculum not found" in str(exc)
    else: raise AssertionError("missing curriculum must raise")

def test_missing_subject_is_explicit():
    try: CatalogService(InMemoryCatalog()).get_subject("BAMS-UG","UNKNOWN","2026.1")
    except CatalogNotFoundError as exc: assert "subject not found" in str(exc)
    else: raise AssertionError("missing subject must raise")
