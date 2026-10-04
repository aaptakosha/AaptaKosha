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

The current production hardening includes clean Samhita study routes, PWA/offline content caching, accessibility regression checks, and open-source contribution governance.

Phases 0–7 are complete. Phase 8 connects the existing student-facing surfaces to the authenticated durable application APIs, with a shared learner session/bootstrap boundary, reusable API client, continuous study-to-assessment-to-progress journey, and browser/integration verification.

See `docs/architecture/phase-8-authenticated-learner-experience.md`.

## Working conventions

### Samhita learning unit

Each learning unit should preserve this order: authentic **श्लोक**, faithful **हिन्दी अनुवाद**, separate **व्याख्या**, and source-faithful **टीका अनुवाद** where available. Add comparison tables, diagrams, and other study aids when they materially improve understanding. Mark NCISM recitation only where the curriculum explicitly requires it.

### Validation before merge

- Run affected regression/content tests.
- Check API and frontend routes touched by the change.
- Verify Sanskrit sequence and chapter references.
- Verify assessment content references and learner navigation.
- Avoid merging stale branches without synchronising them with current `main`.
- Avoid unnecessary production deployments when deployment-rate limits are active.

### Deployment

Production is sourced from `main` through Vercel. Runtime errors and deployment status should be checked after changes affecting routing, APIs, authentication, or content loading.

### Academic-content boundary

Classical formulations are presented for academic Samhita study and should not be transformed into individualized self-treatment instructions.
