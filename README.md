# AaptaKosha

AaptaKosha is an extensible knowledge and learning platform designed around the NCISM BAMS curriculum as its academic backbone, while keeping the architecture open for future domains beyond study.

## Project principles

- NCISM-first academic backbone.
- Extensible by design.
- Automation-friendly operations.
- Auditable changes.
- Connector-first external integrations.

## Repository structure

- `src/aaptakosha_ingestion/` — Phase 1 ingestion and reconciliation core
- `src/aaptakosha_core/` — Phase 2 product contracts plus Phase 3 knowledge/content contracts
- `docs/architecture/` — architecture baselines
- `docs/governance/` — project gates and governance
- `docs/sources/` — authoritative source registry
- `tests/` — automated tests

## Current phase

**Phase 3 — Knowledge & Content Layer**

Phase 2 is complete. Phase 3 currently defines domain-neutral content resources, provenance, and explicit content lifecycle states above the authoritative curriculum catalog. See `docs/architecture/phase-3-knowledge-content.md`.

Phase 1 remains the authoritative ingestion/reconciliation path for published curriculum.
