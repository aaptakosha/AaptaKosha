#!/usr/bin/env python3
"""AaptaKosha autonomous Samhita/library reconciliation and safe ingestion queue.

This worker is intentionally additive:
- it never deletes or replaces published content;
- it treats Sanskrit mūla and historical ṭīkā as source-backed artifacts;
- it creates a durable queue for missing/partial books;
- it only promotes content when a configured source adapter reports verification.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "content" / "samhita-registry.json"
STATE_DIR = ROOT / "content" / ".automation"
STATE = STATE_DIR / "samhita-autopilot-state.json"

DEVANAGARI = re.compile(r"[\u0900-\u097F]")
TIKA_KEYS = ("tika", "tīkā", "tika_", "commentary", "comment")

def now():
    return datetime.now(timezone.utc).isoformat()

def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))

def all_books(reg):
    return [b for c in reg.get("library_sources", {}).get("categories", []) for b in c.get("books", [])]

def content_files(reg):
    for e in reg.get("entries", []):
        p = ROOT / e["path"]
        if p.exists() and p.is_file():
            yield e, p

def inspect_file(path):
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"parse_error": str(exc), "verses": 0, "sanskrit": 0, "tika": 0}
    verses = obj.get("verses") or obj.get("passages") or []
    if not isinstance(verses, list):
        verses = []
    sanskrit = 0
    tika = 0
    for v in verses:
        text = v.get("sanskrit_original") or v.get("sanskrit") or ""
        if text and DEVANAGARI.search(text):
            sanskrit += 1
        tika += sum(1 for k, value in v.items() if value and any(k.startswith(prefix) for prefix in TIKA_KEYS))
    return {
        "verses": len(verses),
        "sanskrit": sanskrit,
        "tika": tika,
        "chapter_id": obj.get("chapter_id") or obj.get("content_id") or obj.get("passage_id"),
        "source_metadata": obj.get("source_metadata", []),
    }

def book_key(path):
    base = ROOT / "content" / "samhita"
    try:
        parts = path.relative_to(base).parts
    except ValueError:
        return None
    return parts[0] if parts else None

def build_report(reg):
    files = list(content_files(reg))
    by_book = {}
    for e, p in files:
        key = book_key(p)
        if key is None:
            continue
        info = inspect_file(p)
        b = by_book.setdefault(key, {"files": 0, "verses": 0, "sanskrit": 0, "tika": 0, "source_backed": 0})
        b["files"] += 1
        for k in ("verses", "sanskrit", "tika"):
            b[k] += info[k]
        if info["source_metadata"]:
            b["source_backed"] += 1

    books = all_books(reg)
    queue = []
    for b in books:
        key = b["id"].replace("-samhita", "").replace("-nidana", "").replace("-", "_")
        key = key.replace("_samhita", "")
        match = next((v for k, v in by_book.items() if k == key or k.replace("_","-") == b["id"]), None)
        if match:
            status = "complete_candidate" if match["verses"] and match["sanskrit"] == match["verses"] else "partial"
            if match["tika"] < match["verses"]:
                status = "partial"
            queue.append({**b, "observed": match, "queue_status": status})
        else:
            queue.append({**b, "observed": None, "queue_status": "missing_source_content"})
    return queue

def fingerprint(payload):
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-state", action="store_true")
    args = ap.parse_args()
    reg = load_registry()
    queue = build_report(reg)
    report = {
        "schema_version": 1,
        "generated_at": now(),
        "registry_version": reg.get("version"),
        "book_count": len(queue),
        "counts": {},
        "queue": queue,
    }
    for x in queue:
        report["counts"][x["queue_status"]] = report["counts"].get(x["queue_status"], 0) + 1
    report["fingerprint"] = fingerprint(report)
    if args.write_state:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "generated_at": report["generated_at"],
        "registry_version": report["registry_version"],
        "book_count": report["book_count"],
        "counts": report["counts"],
        "state": str(STATE.relative_to(ROOT)) if args.write_state else None,
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

# Scheduled reconciliation is intentionally idempotent.
