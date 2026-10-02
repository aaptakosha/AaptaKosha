# Phase 6 — Durable Application API & Persistence

**Status:** Complete; CI verified  
**Date:** 2026-10-01

## Purpose

Phase 6 makes the learner-facing application path durable in deployed environments while preserving the framework-neutral domain boundaries established in Phases 1–5.

## Completed scope

- Durable PostgreSQL adapters for assessments, learner attempts, and learning progress.
- Live HTTP adapter for learner progress with GET/POST/PUT operations.
- Vercel entrypoint wiring for assessment and progress APIs.
- PostgreSQL selected automatically when `DATABASE_URL` is configured.
- SQLite remains the local/development fallback.
- Health endpoint verifies database connectivity and reports the active backend.
- Focused Phase 6 tests for assessment HTTP behavior, learning APIs, progress APIs/repositories, PostgreSQL adapters, and the real HTTP server.
- Existing answer-key protection and learner scoping remain enforced at the application boundary.

## Persistence boundary

The deployed API uses the same domain contracts regardless of storage backend. PostgreSQL repositories provide durable storage for:
- assessments and questions/options
- learner assessment attempts
- learner learning-progress snapshots

SQLite remains available for local development and fallback operation.

## API boundary

The deployed entrypoint exposes:
- assessment routes through the existing assessment HTTP adapter
- `/progress` routes through `ProgressHttpApi`
- `/health` for operational verification

The API composition does not import persistence models into the frontend.

## Verification

GitHub Actions product workflow run #106 completed successfully on the main branch after the Phase 6 implementation. The Phase 6 focused test suite is included in the repository test suite.

## Non-goals

- Production authentication/identity provider integration.
- Adaptive assessment.
- AI-generated assessment content without provenance/review controls.
- Replacing the framework-neutral domain layer with a UI-specific data model.
