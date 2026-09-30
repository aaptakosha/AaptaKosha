# Phase 4 — Assessment & Learner Experience

**Status:** Implementation complete for current slice; CI verified; analytics/progress integration pending  
**Date:** 2026-09-30

## Purpose

Phase 4 builds learner-facing assessment capabilities on top of the authoritative curriculum and Phase 3 content layers. It remains domain-neutral so the platform can support BAMS and later other learning domains.

## Boundaries

Initial assessment capabilities:
- assessment definitions
- question and option contracts
- explicit assessment status
- learner attempts and submitted responses
- deterministic scoring rules
- persistence adapters
- future adapters for APIs, analytics, and spaced practice

Curriculum remains authoritative. Assessments may reference curriculum/content resources but do not mutate them.

## Implementation sequence

1. Assessment domain contracts — Implemented and CI verified
2. Assessment persistence boundary — Implemented and CI verified
3. Assessment application service and scoring — Implemented and CI verified
4. Learner attempt API boundary — Implemented and CI verified
5. Assessment analytics/progress integration
6. Tests and CI expansion — Complete; GitHub Actions product workflow verified

## Persistence design

The initial SQLite adapter stores assessment definitions and learner attempts as JSON snapshots:
- assessment identity, title, status, curriculum references, questions, and options
- attempt identity, assessment reference, learner identity, status, and selected answers
- deterministic identifier ordering for list operations
- foreign-key protection from orphaned attempts
- a dedicated migration is provided under `migrations/002_assessment.sql`

The repository boundary is framework-neutral so another storage adapter can replace SQLite without changing domain contracts.

## Application service

The application service governs lifecycle transitions and learner operations. It permits publication only for non-empty draft assessments, permits attempts only against published assessments, validates submitted question/option references, prevents re-submission, and delegates final scoring to the deterministic domain scorer.

## Learner attempt API

The framework-neutral `AssessmentApi` exposes published assessment retrieval/listing plus learner-attempt start, retrieval, submission, and deterministic scoring. Attempt retrieval, submission, and scoring are scoped to the supplied learner identity. API serialization intentionally omits question answer keys so published assessments do not expose `is_correct` to learners. Domain/application errors are mapped to stable transport-neutral status codes without coupling the core to a web framework.

## Initial lifecycle

Assessment:
- draft
- published
- archived

Attempt:
- in_progress
- submitted

Publishing requires at least one question. Scoring is deterministic and based on the submitted answers against the question answer keys. Lifecycle enforcement belongs in the application service rather than the raw persistence adapter.

GitHub Actions product workflow run #57 for commit 429c766 completed successfully on Python 3.11 and 3.12, verifying the current Phase 4 implementation and test suite. Assessment analytics/progress integration remains the next Phase 4 implementation slice.

## Non-goals

- No frontend/exam UI yet.
- No adaptive testing yet.
- No AI-generated questions without provenance and review controls.
- No external exam-provider integration yet.
