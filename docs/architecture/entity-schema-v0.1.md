# AaptaKosha Entity & Schema Specification v0.1

**Status:** Phase 0 baseline
**Version:** 0.1.0
**Date:** 2026-09-30

## Design rule

Core entities use stable IDs and keep provenance, lifecycle state, timestamps, and auditability separate from display content.

## Core entities

| Entity | Purpose | Key fields |
|---|---|---|
| `source` | External authority/document | id, authority, title, canonical_url, version, effective_date, verified_at, status |
| `curriculum` | A curriculum/version boundary | id, authority, programme, batch_scope, version, effective_from, effective_to, source_id |
| `professional_year` | Academic stage | id, curriculum_id, sequence, name |
| `subject` | Subject/course | id, professional_year_id, code, name, credits, status |
| `topic` | Topic/unit within a subject | id, subject_id, parent_topic_id, code, name, sequence |
| `learning_item` | Atomic learning target/content unit | id, topic_id, type, title, description, learning_outcome, status |
| `resource` | Linked learning resource | id, learning_item_id, type, title, locator, source_id, status |
| `assessment` | Assessment definition/item | id, subject_id, type, marks, weight, source_id, status |
| `provenance` | Evidence relationship | id, entity_type, entity_id, source_id, locator, captured_at |
| `change_event` | Audit record | id, entity_type, entity_id, action, actor, occurred_at, reason, before_ref, after_ref |

## Relationships

- `source` 1-to-many `provenance`
- `curriculum` 1-to-many `professional_year`
- `professional_year` 1-to-many `subject`
- `subject` 1-to-many `topic`
- `topic` supports recursive `parent_topic_id`
- `topic` 1-to-many `learning_item`
- `learning_item` 1-to-many `resource`
- `subject` 1-to-many `assessment`
- Any authoritative entity may have one-to-many `provenance` records.
- Mutable entities generate `change_event` records.

## ID convention

IDs should be opaque and stable, e.g. `src_...`, `cur_...`, `yr_...`, `sub_...`, `top_...`, `li_...`, `res_...`, `asm_...`, `prov_...`, `chg_...`. IDs must not encode names that can change.

## Versioning rules

A new authoritative curriculum version creates a new `curriculum` record. Existing records are not silently rewritten. Relationships may be mapped from old to new records with explicit migration/provenance metadata.

## Required audit fields

All mutable core records: `created_at`, `updated_at`, `status`. Authoritative records additionally require provenance. Significant modifications create `change_event` entries.

## Extensibility

Additional domains should introduce domain-specific entities around the same identity/provenance/audit primitives rather than modifying curriculum assumptions into the core model.
