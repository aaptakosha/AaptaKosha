# Phase 8 — Authenticated Learner Experience Integration

**Status:** In progress  
**Date:** 2026-10-01

## Purpose

Phase 8 turns the existing framework-neutral frontend surfaces into one coherent learner experience backed by the authenticated Phase 6–7 application APIs.

The goal is not to replace the existing UI. It is to connect and harden it so a learner can move through study, practice, assessment, progress, planning, notes, and settings without duplicating domain or authorization logic in the browser.

## Scope

### Application shell
- Establish one shared learner-session/bootstrap contract for frontend pages.
- Provide consistent loading, empty, error, and signed-out states.
- Keep navigation and feature discovery coherent across existing pages.

### Authenticated API integration
- Connect learner-facing pages to the durable assessment and progress endpoints.
- Send authenticated requests without exposing provider secrets in browser code.
- Treat the authenticated principal from Phase 7 as the source of learner identity.
- Remove browser assumptions that a user can choose or override another learner ID.

### Learner journey
- Study → practice → assessment → results → progress should form a continuous journey.
- Preserve progress after refresh and across sessions when production persistence is configured.
- Surface useful next actions from existing durable data without introducing a new recommendation engine.

### UI quality
- Preserve the student-friendly visual language and touch of greenery.
- Keep pages responsive and accessible.
- Reuse shared presentation patterns instead of creating feature-specific navigation systems.

### Verification
- Add frontend/API integration checks for authenticated learner flows.
- Verify protected routes reject missing or mismatched identity.
- Verify production deployment after integration changes.
- Keep Phase 0–7 regression coverage green.

## Architectural constraints

- NCISM remains the academic backbone.
- Domain and persistence contracts remain the source of truth; frontend state is a projection, not a second domain model.
- Authentication and authorization stay at the application/API boundary.
- No Clerk secret, database credential, or privileged token is shipped to browser code.
- Existing SQLite local fallback remains usable for development.
- Future non-study modules must be able to reuse the learner shell without coupling to BAMS-specific UI code.

## Initial implementation order

1. Frontend session/bootstrap contract and shared API client.
2. Authenticated progress integration.
3. Assessment/practice integration and journey continuity.
4. Shared loading/error/empty states and navigation consistency.
5. Integration tests and browser verification.
6. Production deployment verification and Phase 8 gate update.

## Non-goals

- Replacing the current frontend framework-neutral approach.
- Rebuilding the Phase 7 identity provider.
- Introducing a new database/domain model.
- Adding AI tutoring or automated content generation.
- Adding unrelated analytics or social features.
