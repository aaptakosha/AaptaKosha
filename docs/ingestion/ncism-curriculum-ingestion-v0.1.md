# NCISM Curriculum Ingestion Model v0.1

**Status:** Phase 0 baseline
**Version:** 0.1.0
**Date:** 2026-09-30

## Goal

Convert authoritative NCISM curriculum documents into normalized, traceable records without losing the source structure or document version.

## Pipeline

`Discover -> Capture -> Parse -> Normalize -> Validate -> Map -> Review -> Publish -> Audit`

## Mapping

| NCISM document concept | AaptaKosha target |
|---|---|
| Programme/curriculum document | `curriculum` |
| Professional course/year | `professional_year` |
| Subject/course code and name | `subject` |
| Unit/topic/subtopic | `topic` |
| Course objective/learning objective | `learning_item.learning_outcome` |
| Teaching-learning activity | `learning_item` or activity extension |
| Resource/reference | `resource` |
| Assessment scheme/paper/marks | `assessment` |
| Source page/table/section | `provenance.locator` |

## Source handling

The ingestion process must retain the exact source URL and document identity. If NCISM publishes a newer or transitional curriculum, it must be represented as a separate version with effective/batch scope rather than overwriting an existing curriculum.

This is important because NCISM currently publishes multiple curriculum variants and transitional documents; for example, its first-professional materials include a 2025-26 Ayurpraveshika transitional curriculum, while other first- and second-professional curriculum documents describe their own course and assessment structures. citeturn0search3turn0search2turn0search5

## Validation gates

1. Source is an official NCISM publication.
2. Document identity/version/effective scope is captured where available.
3. Professional year and subject mapping is unambiguous.
4. Subject codes/names are preserved exactly in source fields.
5. Hierarchy is internally consistent.
6. Assessment values retain their original units and context.
7. Every imported authoritative fact has provenance.
8. Ambiguous changes enter review rather than being auto-published.

## Batch and supersession

Curriculum records must support batch scope and effective dates. A later document can supersede an earlier record, but historical records remain queryable for students/batches to which they applied.

## First ingestion target

Start with the authoritative First Professional BAMS curriculum set, then extend the same pipeline to Second, Third, and Fourth Professional after validation. The model itself must not assume that only four stages exist.
