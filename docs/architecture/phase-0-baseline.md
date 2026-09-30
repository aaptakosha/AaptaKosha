# AaptaKosha Phase 0 — Architecture Baseline

**Status:** Draft baseline
**Version:** 0.1.0
**Date:** 2026-09-30

## Purpose

Phase 0 defines the minimum architectural rules required before implementation begins. It intentionally avoids locking the project into a framework, cloud provider, or database vendor.

## Domain model principles

Every major entity should have a stable internal identifier, lifecycle/status metadata, created/updated timestamps, provenance for externally sourced facts where applicable, and version/change history for mutable authoritative records.

The model separates identity, classification, content, provenance, workflow state, and audit history.

## Curriculum hierarchy

Professional Year -> Subject -> Topic / Unit -> Learning Item -> learning outcomes, resources, assessments, and metadata/provenance.

The hierarchy must remain extensible and must not assume that every future domain has the same depth.

## Source-of-truth model

Authoritative sources are first-class records with source ID, authority/publisher, canonical URL, document title, version identifier when available, publication/effective date when available, retrieval/verification date, scope, superseded-by relationship, and verification status.

External facts should link to their source records where practical.

## Status model

The project tracker uses Upcoming, Pending, Ongoing, Completed, with Blocked and Cancelled as side states. Application-domain state machines should be defined separately where needed.

## Automation model

Detect -> Validate -> Propose -> Review when required -> Apply -> Audit.

High-impact or ambiguous source changes should be reviewable before modifying published knowledge.

## Compatibility and extensibility

Avoid hard-coded assumptions about exactly four professional years, fixed subject counts, a single content format, a single user role, a single assessment method, or a single external provider.

## Phase 1 gate

Before Phase 1, the project should have an authoritative NCISM source registry, versioned schema/entity specification, stable ID conventions, audit/change-log conventions, curriculum ingestion mapping, and defined source update/supersession rules.
