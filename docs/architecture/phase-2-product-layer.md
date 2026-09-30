# Phase 2 — Application & Product Layer

**Status:** Foundation slice implemented
**Date:** 2026-09-30

## Goal

Turn the Phase 1 curriculum/reconciliation engine into a product-facing application layer without coupling the academic source model to a specific UI, database, authentication provider, or future domain.

## Architectural boundaries

1. Source layer — NCISM and future authoritative sources.
2. Ingestion layer — capture, fingerprint, normalize, validate, diff, review, publish.
3. Academic domain layer — stable curriculum/catalog contracts consumed by products.
4. Application layer — use cases such as browsing curriculum, retrieving subjects/topics, and recording learning activity.
5. Delivery layer — web/mobile/API/automation clients.
6. Integration layer — connectors for identity, messaging, storage, analytics, and other external services.

Phase 1 remains the source-of-truth pipeline for curriculum publication. Phase 2 must consume published versions rather than bypassing reconciliation.

## Initial product contract

The first Phase 2 slice defines a read-oriented academic catalog contract:

- Curriculum
- Subject
- Topic

Stable identifiers are required. Display names and descriptive fields remain source-derived data and must not become identifiers.

The contract is independent of HTTP frameworks, ORM/database vendors, frontend frameworks, authentication providers, and external connector implementations.

## Extension rules

Future domains (for example exams, notes, flashcards, social features, or non-academic knowledge) must reference domain IDs/contracts instead of embedding NCISM-specific assumptions into generic application infrastructure.

Learning activity should reference immutable published curriculum version + stable content ID where historical accuracy matters.

## Phase 2 implementation sequence

1. Product-domain contracts and catalog read model — In progress / foundation implemented
2. Application use-case services
3. Persistence adapter and migration baseline
4. API boundary
5. Identity and authorization boundary
6. Learning-progress model
7. Notifications/automation boundary
8. Product-facing test and CI expansion

## Non-goals for this slice

- No production authentication.
- No frontend.
- No vendor-specific database schema.
- No direct mutation of published curriculum from product code.
- No assumption that BAMS is the only future domain.
