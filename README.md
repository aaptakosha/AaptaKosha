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
- `frontend/` — framework-neutral responsive learner presentation layer
- `api/` — deployed HTTP entrypoints
- `docs/architecture/` — architecture baselines
- `docs/governance/` — project gates and governance
- `docs/sources/` — authoritative source registry
- `tests/` — automated tests

## Current phase

**Phase 8 — Authenticated Learner Experience Integration: In progress**

Phases 0–7 are complete. Phase 8 connects the existing student-facing surfaces to the authenticated durable application APIs, with a shared learner session/bootstrap boundary, reusable API client, continuous study-to-assessment-to-progress journey, and browser/integration verification.

See `docs/architecture/phase-8-authenticated-learner-experience.md`.
