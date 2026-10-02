from aaptakosha_core.content import ContentResource, PUBLISHED, DRAFT
from aaptakosha_core.content_search import InMemoryContentSearchIndex

def test_search_indexes_only_published_content_and_is_deterministic():
    index=InMemoryContentSearchIndex()
    index.index(ContentResource("r2","lesson","Ayurveda Basics",summary="dosha overview",status=PUBLISHED,curriculum_refs=("subject:basic",)))
    index.index(ContentResource("r1","note","Ayurveda Dosha",summary="overview",status=PUBLISHED,curriculum_refs=("subject:basic",)))
    index.index(ContentResource("r3","lesson","Draft Dosha",status=DRAFT))
    results=index.search("dosha")
    assert [x.resource_id for x in results] == ["r1","r2"]
    assert index.search("missing") == ()
