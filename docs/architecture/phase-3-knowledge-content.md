# Phase 3 — Knowledge & Content Layer

**Status:** Content repository and persistence boundary implemented
**Date:** 2026-09-30

## Purpose

Phase 3 introduces the knowledge/content layer above the published curriculum catalog. Curriculum remains authoritative and immutable from product code; content resources reference curriculum concepts without becoming part of the curriculum source itself.

The layer is domain-neutral so AaptaKosha can later support BAMS, other academic domains, professional knowledge, or non-academic collections.

## Boundaries

A content resource has:
- stable resource ID
- resource type
- title
- optional summary
- lifecycle status
- source/provenance metadata
- references to curriculum resources through generic subject/resource identifiers

Initial lifecycle states:
- draft
- review
- published
- archived

Initial resource types are intentionally open strings rather than an enum. This permits notes, articles, videos, flashcards, question sets, references, media, and future types without schema changes.

## Provenance and auditability

Content must retain provenance separately from curriculum authority. A resource can cite an external source or internal author while Phase 1 continues to own NCISM curriculum ingestion and reconciliation.

Publishing is an explicit lifecycle transition. The Phase 3 core does not yet provide an editor UI, CMS, external content provider, search index, or binary object storage.

## Implementation sequence

1. Content-resource contracts — Complete
2. Content repository and persistence boundary — Next
3. Content application service and publication rules
4. Curriculum-to-content linking — Complete
5. Content API boundary — Complete
6. Search/indexing boundary — Complete
7. Phase 3 tests and CI expansion

## Non-goals

- No direct mutation of published curriculum.
- No vendor-specific CMS.
- No frontend/editor.
- No full-text search engine.
- No media/object-storage provider.
- No automatic publishing without explicit lifecycle rules.
