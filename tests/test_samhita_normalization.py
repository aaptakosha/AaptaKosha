from api.content import _normalize_payload

def test_passage_hindi_aliases_are_canonicalized():
    payload = {"title":"Test","passages":[
        {"passage_no":1,"sanskrit_original":"अथ ॥","hindi_translation":"हिन्दी अर्थ","hindi_explanation":"अलग व्याख्या"}
    ]}
    item=_normalize_payload(payload,"ashtanga.hridaya.sutra.99")["verses"][0]
    assert item["sanskrit_original"]=="अथ ॥"
    assert item["translation_hi"]=="हिन्दी अर्थ"
    assert item["explanation_hi"]=="अलग व्याख्या"

def test_student_meaning_is_preserved_as_translation():
    payload={"verses":[{"verse_number":1,"sanskrit":"अथ ॥","student_meaning":"अर्थ"}]}
    item=_normalize_payload(payload,"ashtanga.hridaya.sutra.99")["verses"][0]
    assert item["sanskrit_original"]=="अथ ॥"
    assert item["translation_hi"]=="अर्थ"
