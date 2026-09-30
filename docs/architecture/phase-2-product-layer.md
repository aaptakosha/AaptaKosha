# Phase 2 — Application & Product Layer

**Status:** Persistence foundation implemented
**Date:** 2026-09-30

## Delivered
- Immutable Curriculum, Subject, and Topic domain contracts.
- CatalogService for curriculum, subject-list, and subject retrieval.
- CatalogRepository protocol as the persistence boundary.
- Explicit CatalogNotFoundError for missing resources.
- Tests for service behavior.

Phase 1 remains the authoritative ingestion/reconciliation path for published curriculum. Product services consume published data and do not mutate it directly.

## Implementation sequence
1. Product-domain contracts and catalog read model — Complete
2. Application use-case services — Complete
3. Persistence adapter and migration baseline — Complete
4. API boundary — Next
5. Identity and authorization boundary
6. Learning-progress model
7. Notifications/automation boundary
8. Product-facing test and CI expansion

## Non-goals
- No production authentication.
- No frontend.
- No vendor-specific database schema.
- No direct mutation of published curriculum from product code.
- No assumption that BAMS is the only future domain.
