# Phase 4 — Assessment & Learner Experience

**Status:** In progress — assessment contracts implemented; verification pending
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
- future adapters for persistence, APIs, analytics, and spaced practice

Curriculum remains authoritative. Assessments may reference curriculum/content resources but do not mutate them.

## Implementation sequence

1. Assessment domain contracts — Implemented; verification pending
2. Assessment persistence boundary
3. Assessment application service and scoring
4. Learner attempt API boundary
5. Assessment analytics/progress integration
6. Tests and CI expansion

## Initial lifecycle

Assessment:
- draft
- published
- archived

Attempt:
- in_progress
- submitted

Publishing requires at least one question. Scoring is deterministic and based on the submitted answers against the question answer keys.

## Non-goals

- No frontend/exam UI yet.
- No adaptive testing yet.
- No AI-generated questions without provenance and review controls.
- No external exam-provider integration yet.
