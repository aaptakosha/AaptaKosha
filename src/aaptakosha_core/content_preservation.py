"""Universal content-preservation invariants for AaptaKosha."""
from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

@dataclass(frozen=True)
class PreservationIssue:
    kind: str
    path: str
    detail: str

def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def _content_id_map(registry: Any) -> dict[str, dict]:
    entries = registry.get("entries", []) if isinstance(registry, dict) else []
    return {str(e.get("content_id")): e for e in entries if isinstance(e, dict) and e.get("content_id")}

def _verse_map(payload: Any) -> dict[str, dict]:
    if not isinstance(payload, dict) or not isinstance(payload.get("verses"), list):
        return {}
    return {str(v.get("verse_id")): v for v in payload["verses"] if isinstance(v, dict) and v.get("verse_id")}

def validate_content_preservation(before_root: str | Path, after_root: str | Path) -> list[PreservationIssue]:
    """Reject removal of published files, registry records, or classical source text."""
    before, after = Path(before_root), Path(after_root)
    issues: list[PreservationIssue] = []
    before_content, after_content = before / "content", after / "content"
    if not before_content.exists():
        return issues
    if not after_content.exists():
        return [PreservationIssue("content-root-removed", "content", "published content root is missing")]

    before_files = {p.relative_to(before).as_posix() for p in before_content.rglob("*") if p.is_file()}
    after_files = {p.relative_to(after).as_posix() for p in after_content.rglob("*") if p.is_file()}
    for path in sorted(before_files - after_files):
        issues.append(PreservationIssue("file-removed", path, "published content file disappeared"))

    old_reg = before / "content" / "samhita-registry.json"
    new_reg = after / "content" / "samhita-registry.json"
    if old_reg.exists():
        if not new_reg.exists():
            issues.append(PreservationIssue("registry-removed", "content/samhita-registry.json", "published Samhita registry disappeared"))
        else:
            try:
                old_entries, new_entries = _content_id_map(_json(old_reg)), _content_id_map(_json(new_reg))
                for cid, old in sorted(old_entries.items()):
                    if cid not in new_entries:
                        issues.append(PreservationIssue("registry-entry-removed", "content/samhita-registry.json", f"published content_id removed: {cid}"))
                    elif str(new_entries[cid].get("path") or "") != str(old.get("path") or ""):
                        issues.append(PreservationIssue("registry-path-changed", "content/samhita-registry.json", f"{cid}: registry path changed"))
            except (OSError, ValueError, TypeError) as exc:
                issues.append(PreservationIssue("registry-invalid", "content/samhita-registry.json", f"cannot compare registry: {exc}"))

    old_samhita = before / "content" / "samhita"
    for old_path in old_samhita.rglob("*.json") if old_samhita.exists() else []:
        rel = old_path.relative_to(before).as_posix()
        new_path = after / rel
        if not new_path.exists():
            continue
        try:
            old_payload, new_payload = _json(old_path), _json(new_path)
        except (OSError, ValueError, TypeError) as exc:
            issues.append(PreservationIssue("json-invalid", rel, f"cannot compare payload: {exc}"))
            continue
        old_verses, new_verses = _verse_map(old_payload), _verse_map(new_payload)
        for vid, old_verse in sorted(old_verses.items()):
            new_verse = new_verses.get(vid)
            if new_verse is None:
                issues.append(PreservationIssue("verse-removed", rel, f"published verse_id removed: {vid}"))
                continue
            old_source = str(old_verse.get("sanskrit_original") or old_verse.get("text") or "").strip()
            new_source = str(new_verse.get("sanskrit_original") or new_verse.get("text") or "").strip()
            if old_source and new_source != old_source:
                issues.append(PreservationIssue("source-text-changed", rel, f"published Sanskrit source changed for {vid}"))
    return issues

def assert_content_preserved(before_root: str | Path, after_root: str | Path) -> None:
    issues = validate_content_preservation(before_root, after_root)
    if issues:
        raise ValueError("content preservation check failed:\n" + "\n".join(f"- [{x.kind}] {x.path}: {x.detail}" for x in issues))
