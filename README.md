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
- `src/aaptakosha_core/` — Phase 2 framework-agnostic product-domain contracts
- `docs/architecture/` — architecture baselines
- `docs/governance/` — project gates and governance
- `docs/sources/` — authoritative source registry
- `tests/` — automated tests

## Current phase

**Phase 2 — Application & Product Layer**

The Phase 2 foundation currently defines framework-agnostic Curriculum, Subject, and Topic contracts. See `docs/architecture/phase-2-product-layer.md`.

Phase 1 remains the authoritative ingestion/reconciliation path for published curriculum.
