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
- `src/aaptakosha_core/` — domain, application, persistence, and HTTP contracts
- `frontend/` — Phase 5 framework-neutral responsive presentation layer
- `api/` — deployed HTTP entrypoints
- `docs/architecture/` — architecture baselines
- `docs/governance/` — project gates and governance
- `docs/sources/` — authoritative source registry
- `tests/` — automated tests

## Current phase

**Phase 6 — Durable Application API & Persistence: Complete**

Phases 0–5 are complete. Phase 6 wires the learner-facing application path to durable PostgreSQL storage for deployed environments while retaining SQLite for local development/fallback. The deployed API exposes assessment, learner-progress, and health routes through the framework-neutral application boundaries.

See `docs/architecture/phase-6-durable-api-persistence.md`.
