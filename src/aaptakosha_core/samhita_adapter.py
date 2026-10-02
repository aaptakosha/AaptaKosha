"""Adapters from legacy Samhita chapter packages to Canonical Samhita v1.

The adapters deliberately preserve existing storage formats. They normalize only at
the boundary so legacy chapters can continue serving existing consumers while all
new content can target one canonical contract.
"""

from __future__ import annotations

import re
from typing import Any, Mapping


def _require_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return value


def _source_id(text_id: str, index: int) -> str:
    return f"{text_id}.source.{index:02d}"


def _normalize_sources(
    text_id: str, sources: list[Mapping[str, Any]]
) -> tuple[list[dict[str, Any]], list[str]]:
    normalized: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, source in enumerate(sources, start=1):
        title = str(source.get("source") or source.get("name") or "").strip()
        role = str(source.get("role") or "source witness").strip()
        if not title:
            raise ValueError(f"source {index} has no title")
        source_id = _source_id(text_id, index)
        item: dict[str, Any] = {
            "source_id": source_id,
            "title": title,
            "role": role,
        }
        locator = source.get("locator") or source.get("url")
        if locator:
            item["locator"] = str(locator)
        if source.get("edition"):
            item["edition"] = str(source["edition"])
        if source.get("citation"):
            item["attribution"] = str(source["citation"])
        normalized.append(item)
        ids.append(source_id)
    if not normalized:
        raise ValueError("chapter must declare at least one source")
    return normalized, ids


def _range(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"\s*(\d+)\s*(?:-|–|—)\s*(\d+)\s*", value)
    if not match:
        raise ValueError(f"invalid verse range: {value!r}")
    start, end = int(match.group(1)), int(match.group(2))
    if start > end:
        raise ValueError(f"invalid verse range: {value!r}")
    return start, end


def _verse_refs(prefix: str, start: int, end: int) -> list[str]:
    return [f"{prefix}.{number:03d}" for number in range(start, end + 1)]


def _quality_from_legacy(
    gates: Mapping[str, Any] | None,
    *,
    translation_present: bool,
    commentary_present: bool,
    source_verified: bool,
) -> dict[str, bool]:
    gates = gates or {}
    return {
        "canonical_sequence_verified": bool(
            gates.get("canonical_sequence_verified", gates.get("online_sanskrit_witness_cross_checked", False))
        ),
        "verse_range_verified": bool(
            gates.get("verse_range_verified", gates.get("verse_extent_verified", False))
        ),
        "source_verified": bool(gates.get("source_verified", source_verified)),
        "hindi_translation_present": bool(
            gates.get("hindi_translation_present", translation_present)
        ),
        "commentary_mapped": bool(
            gates.get("commentary_mapped", commentary_present)
        ),
        "fabricated_commentary_avoided": bool(
            gates.get("fabricated_commentary_avoided", True)
        ),
        "assessment_refs_resolve": bool(gates.get("assessment_refs_resolve", True)),
        "learning_refs_resolve": bool(gates.get("learning_refs_resolve", True)),
        "revision_refs_resolve": bool(gates.get("revision_refs_resolve", True)),
    }


def from_charaka_legacy(chapter: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize the existing Charaka verse-object package."""

    chapter = _require_mapping(chapter, "chapter")
    chapter_id = str(chapter["chapter_id"])
    parts = chapter_id.split(".")
    if len(parts) != 3:
        raise ValueError("Charaka chapter_id must look like charaka.sutra.01")

    text_id, sthana_key, adhyaya_key = parts
    adhyaya_no = int(chapter["adhyaya_no"])
    sources, source_ids = _normalize_sources(text_id, chapter["source_metadata"])

    canonical: dict[str, Any] = {
        "schema_version": "1.0",
        "text": {
            "text_id": text_id,
            "title": "Charaka Saṃhitā",
            "title_hi": "चरक संहिता",
            "language": "sa",
        },
        "sthana": {
            "id": f"{text_id}.{sthana_key}",
            "number": 1,
            "title": str(chapter["sthana"]),
        },
        "adhyaya": {
            "id": chapter_id,
            "number": adhyaya_no,
            "title": str(chapter["title_hi"]),
            "title_hi": str(chapter["title_hi"]),
            "verse_count": int(chapter["verse_count"]),
        },
        "source_metadata": sources,
        "verses": [],
        "learning_units": [],
    }

    unit_ids: list[str] = []
    for index, unit in enumerate(chapter.get("learning_units", []), start=1):
        start, end = int(unit["start_verse"]), int(unit["end_verse"])
        unit_id = f"{chapter_id}.unit.{index:02d}"
        unit_ids.append(unit_id)
        item: dict[str, Any] = {
            "unit_id": unit_id,
            "verse_refs": _verse_refs(chapter_id, start, end),
            "title_hi": str(unit["title_hi"]),
        }
        if unit.get("explanation_hi"):
            item["explanation_hi"] = str(unit["explanation_hi"])
        if unit.get("recitation_verses"):
            item["recitation_verses"] = [int(v) for v in unit["recitation_verses"]]
        canonical["learning_units"].append(item)

    for verse in chapter["verses"]:
        number = int(verse["verse_no"])
        item: dict[str, Any] = {
            "verse_id": f"{chapter_id}.{number:03d}",
            "verse_no": number,
            "canonical_sanskrit": str(verse["sanskrit_original"]),
            "source_refs": source_ids,
        }
        for legacy_key, canonical_key in (
            ("translation_hi", "translation_hi"),
            ("explanation_hi", "explanation_hi"),
            ("tika_hi", "tika_hi"),
            ("recitation_status", "recitation_status"),
            ("editorial_note", "editorial_note"),
        ):
            if verse.get(legacy_key):
                item[canonical_key] = str(verse[legacy_key])
        item["learning_unit_refs"] = [
            unit_id
            for unit_id, unit in zip(
                unit_ids, chapter.get("learning_units", [])
            )
            if int(unit["start_verse"]) <= number <= int(unit["end_verse"])
        ]
        canonical["verses"].append(item)

    canonical["quality_gates"] = _quality_from_legacy(
        None,
        translation_present=all(bool(v.get("translation_hi")) for v in chapter["verses"]),
        commentary_present=all(bool(v.get("tika_hi")) for v in chapter["verses"]),
        source_verified=bool(chapter.get("source_metadata")),
    )
    return canonical


def from_sarangadhara_legacy(chapter: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize the existing Śārṅgadhara chapter-package format."""

    chapter = _require_mapping(chapter, "chapter")
    text_id = str(chapter["text_id"])
    khand_id = str(chapter["khand_id"])
    chapter_number = int(chapter["chapter_number"])
    chapter_id = str(chapter["chapter_id"])
    sources, source_ids = _normalize_sources(text_id, chapter["sources"])

    title_sanskrit = str(chapter.get("title_sanskrit") or chapter.get("title") or chapter_id)
    canonical_sanskrit = chapter.get("canonical_sanskrit")
    if not isinstance(canonical_sanskrit, list) or not canonical_sanskrit:
        raise ValueError("Śārṅgadhara chapter must contain canonical_sanskrit")
    if not all(isinstance(v, Mapping) for v in canonical_sanskrit):
        raise ValueError("canonical_sanskrit must contain verse objects")

    prefix = f"{text_id}.{khand_id}.{chapter_number:02d}"
    canonical: dict[str, Any] = {
        "schema_version": "1.0",
        "text": {
            "text_id": text_id,
            "title": "Śārṅgadhara Saṃhitā",
            "title_hi": "शार्ङ्गधर संहिता",
            "title_sanskrit": "शार्ङ्गधरसंहिता",
            "title_roman": "Śārṅgadhara Saṃhitā",
            "language": "sa",
        },
        "sthana": {
            "id": f"{text_id}.{khand_id}",
            "number": {"purva": 1, "madhyama": 2, "uttara": 3}.get(khand_id, chapter_number),
            "title": khand_id.title(),
        },
        "adhyaya": {
            "id": f"{text_id}.{khand_id}.{chapter_number:02d}",
            "number": chapter_number,
            "title": title_sanskrit,
            "verse_count": len(canonical_sanskrit),
        },
        "source_metadata": sources,
        "verses": [],
        "learning_units": [],
    }

    for index, unit in enumerate(chapter.get("learning_units", []), start=1):
        start, end = _range(str(unit["range"]))
        unit_id = f"{prefix}.unit.{index:02d}"
        item: dict[str, Any] = {
            "unit_id": unit_id,
            "verse_refs": _verse_refs(prefix, start, end),
            "title_hi": str(unit["title"]),
        }
        canonical["learning_units"].append(item)

    unit_ranges = [
        (unit["unit_id"], _range(str(raw["range"])))
        for unit, raw in zip(canonical["learning_units"], chapter.get("learning_units", []))
    ]

    for verse in canonical_sanskrit:
        number = int(verse["verse_no"])
        item: dict[str, Any] = {
            "verse_id": f"{prefix}.{number:03d}",
            "verse_no": number,
            "canonical_sanskrit": str(verse["text"]),
            "source_refs": source_ids,
        }
        item["learning_unit_refs"] = [
            unit_id for unit_id, (start, end) in unit_ranges if start <= number <= end
        ]
        canonical["verses"].append(item)

    assessments = []
    for index, assessment in enumerate(chapter.get("assessments", []), start=1):
        assessment_id = f"{prefix}.assessment.{index:02d}"
        assessments.append(
            {
                "assessment_id": assessment_id,
                "type": str(assessment["type"]),
                "prompt": str(assessment["question"]),
                "content_refs": [u["unit_id"] for u in canonical["learning_units"]],
            }
        )
        if assessment.get("answer"):
            assessments[-1]["rationale_hi"] = str(assessment["answer"])
    if assessments:
        canonical["assessment"] = assessments

    gates = chapter.get("quality_gates", {})
    canonical["quality_gates"] = _quality_from_legacy(
        gates,
        translation_present=False,
        commentary_present=bool(chapter.get("commentary_mapping")),
        source_verified=bool(chapter.get("sources")),
    )
    return canonical


__all__ = ["from_charaka_legacy", "from_sarangadhara_legacy"]
