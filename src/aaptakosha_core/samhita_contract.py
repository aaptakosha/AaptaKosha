"""Semantic validation for the canonical Samhita v1 contract."""

from __future__ import annotations

from typing import Any


class SamhitaContractError(ValueError):
    pass


def validate_samhita_chapter(data: dict[str, Any]) -> None:
    if data.get("schema_version") != "1.0":
        raise SamhitaContractError("unsupported schema_version")

    text = data.get("text") or {}
    sthana = data.get("sthana") or {}
    adhyaya = data.get("adhyaya") or {}
    verses = data.get("verses") or []
    sources = data.get("source_metadata") or []

    for key in ("text_id", "title"):
        if not text.get(key):
            raise SamhitaContractError(f"text.{key} is required")
    for obj, label in ((sthana, "sthana"), (adhyaya, "adhyaya")):
        for key in ("id", "number", "title"):
            if not obj.get(key):
                raise SamhitaContractError(f"{label}.{key} is required")

    source_ids = {s.get("source_id") for s in sources}
    if not source_ids or None in source_ids:
        raise SamhitaContractError("source_metadata must contain stable source_id values")

    verse_ids = [v.get("verse_id") for v in verses]
    verse_nos = [v.get("verse_no") for v in verses]
    if len(verse_ids) != len(set(verse_ids)):
        raise SamhitaContractError("verse_id values must be unique")
    if verse_nos != sorted(verse_nos) or len(verse_nos) != len(set(verse_nos)):
        raise SamhitaContractError("verses must be ordered by unique verse_no")
    if any(not v.get("canonical_sanskrit") for v in verses):
        raise SamhitaContractError("every verse requires canonical_sanskrit")
    for verse in verses:
        refs = verse.get("source_refs") or []
        if not refs:
            raise SamhitaContractError(f"{verse['verse_id']} requires source_refs")
        missing = set(refs) - source_ids
        if missing:
            raise SamhitaContractError(
                f"{verse['verse_id']} references unknown sources: {sorted(missing)}"
            )

    expected = adhyaya.get("verse_count")
    if expected is not None and expected != len(verses):
        raise SamhitaContractError(
            f"adhyaya.verse_count={expected} but {len(verses)} verses are present"
        )

    unit_ids = {u.get("unit_id") for u in data.get("learning_units", [])}
    assessment_ids = {a.get("assessment_id") for a in data.get("assessment", [])}
    verse_set = set(verse_ids)
    for verse in verses:
        for key, allowed in (
            ("learning_unit_refs", unit_ids),
            ("assessment_refs", assessment_ids),
            ("revision_refs", None),
        ):
            refs = verse.get(key, [])
            if allowed is not None and not set(refs) <= allowed:
                raise SamhitaContractError(f"{verse['verse_id']} has unresolved {key}")
            if key == "revision_refs" and any(not isinstance(x, str) or not x for x in refs):
                raise SamhitaContractError(f"{verse['verse_id']} has invalid revision_refs")

    for unit in data.get("learning_units", []):
        if not unit.get("verse_refs") or not set(unit["verse_refs"]) <= verse_set:
            raise SamhitaContractError(f"{unit.get('unit_id')} has unresolved verse_refs")

    for assessment in data.get("assessment", []):
        refs = assessment.get("content_refs") or []
        if not refs or not set(refs) <= (verse_set | unit_ids):
            raise SamhitaContractError(
                f"{assessment.get('assessment_id')} has unresolved content_refs"
            )

    revision_refs = data.get("revision_refs", [])
    if any(not isinstance(ref, str) or not ref for ref in revision_refs):
        raise SamhitaContractError("revision_refs must contain non-empty strings")

__all__ = ["SamhitaContractError", "validate_samhita_chapter"]
