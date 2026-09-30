# Phase 1 — NCISM Ingestion & Reconciliation Implementation

**Status:** Implementation baseline complete  
**Date:** 2026-09-30

## Delivered
1. Source artifact capture with stable SHA-256 fingerprints.
2. Deterministic curriculum normalization.
3. Validation gates for required curriculum fields and stable subject IDs.
4. Deterministic ADD/MODIFY/REMOVE diffing for subjects and topics.
5. SQLite-backed reconciliation runs, immutable artifacts, review queue, change events, and published curriculum versions.
6. Transactional publication: invalid or review-routed candidates are not published.
7. Idempotent artifact storage through fingerprint primary keys.
8. Automated tests covering normalization, validation, diffing, publication, and review blocking.

## Scope boundary
The engine accepts normalized curriculum dictionaries. Source-specific HTML/PDF/table parsers are adapters at the capture/parse boundary and must preserve source wording and provenance before handing data to this engine.

## Operational model
Schedule -> Discover -> Capture -> Fingerprint -> Parse/Adapter -> Normalize -> Validate -> Diff -> Review or Publish -> Audit

## Verification
Run: python -m pytest -q
Runtime dependencies: Python standard library only.
