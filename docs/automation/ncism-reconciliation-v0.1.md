# NCISM Automation & Reconciliation Design v0.1

Status: Phase 0 design baseline
Last updated: 2026-09-30

## Purpose

Define how AaptaKosha detects, validates, reconciles, publishes, and audits changes in authoritative NCISM curriculum sources while preserving historical versions.

## Design principles

1. Official NCISM sources are authoritative for curriculum facts.
2. Source records are immutable historical evidence; new authoritative versions create new records.
3. Automation may detect and propose changes, but ambiguous changes must not be silently published.
4. Every published authoritative fact must retain provenance.
5. Reconciliation must be idempotent: processing the same source/version again must not create duplicate semantic records.
6. Every material change must be auditable.

## Reconciliation lifecycle

Schedule -> Discover -> Fingerprint -> Capture -> Parse -> Normalize -> Compare -> Classify -> Validate -> Review (if required) -> Publish -> Audit

## 1. Schedule

A configurable job periodically checks registered NCISM sources. Initial policy can use daily discovery with deeper document processing only when a source fingerprint changes.

## 2. Discover

For every active source registry entry:
- resolve the canonical URL;
- capture retrieval timestamp;
- record HTTP/document metadata when available;
- identify linked curriculum documents;
- detect additions, replacements, redirects, and superseded documents.

Discovery must never delete the previous source record.

## 3. Fingerprint

Compute a stable fingerprint for the retrieved artifact using document identity and normalized content. Store:
- source ID;
- canonical URL;
- document locator;
- retrieval timestamp;
- content fingerprint;
- detected publication/version/effective metadata.

If the fingerprint is unchanged, the pipeline may stop after audit/logging.

## 4. Capture and parse

When a fingerprint changes:
- preserve the original artifact reference;
- extract text/tables/structured fields;
- retain page/section/table locators;
- preserve the source's subject codes and names exactly before normalization.

Parsing failures create a reviewable ingestion error rather than a partial publication.

## 5. Normalize

Map source structures into the Phase 0 entity model:
curriculum -> professional_year -> subject -> topic -> learning_item/resource/assessment.

Normalization must not discard source wording, units, assessment context, or provenance.

## 6. Compare

Compare the candidate version against the latest applicable published version using stable entity identity where possible.

Classify changes as:
- ADD: new authoritative entity/fact;
- MODIFY: existing fact materially changed;
- REMOVE: fact no longer present in the candidate source;
- MOVE: hierarchy/location changed;
- RENAME: label changed while identity appears stable;
- SCOPE_CHANGE: batch/effective applicability changed;
- SOURCE_CHANGE: locator/document metadata changed without a curriculum-semantic change;
- AMBIGUOUS: automated comparison cannot establish the intended semantic change.

## 7. Validate

Automated validation checks:
- official source authority;
- document identity/version/effective scope;
- valid curriculum and professional-year mapping;
- subject identity and source code/name preservation;
- hierarchy integrity;
- assessment units/context;
- provenance for every authoritative fact;
- no accidental duplicate stable IDs;
- no conflicting active versions for the same scope.

A validation failure blocks publication of the affected candidate changes.

## 8. Review routing

Human review is required when:
- a change is AMBIGUOUS;
- an entity appears removed but the source may be incomplete;
- effective/batch scope conflicts with an existing version;
- parsing or identity matching confidence is below configured threshold;
- authoritative documents disagree;
- a large unexplained change exceeds a configurable anomaly threshold.

Review records must contain the proposed diff, source evidence, validation errors, and decision.

## 9. Publish

Approved changes are published as a new versioned curriculum state. Existing historical states remain queryable.

Publication must be transactional at the curriculum-version boundary: either the complete validated version is published or none of its authoritative facts are.

## 10. Audit

For every run record:
- run ID;
- start/end time;
- source ID;
- input fingerprint;
- previous fingerprint;
- parser/normalizer version;
- validation result;
- change counts by classification;
- review decision, if any;
- publication ID/version;
- error details;
- actor/system identity.

Every material entity change creates a change_event linked to provenance and the reconciliation run.

## Confidence and automation policy

Use confidence only to route workflow, not to hide uncertainty.

Suggested routing:
- High-confidence + all validations pass -> auto-publish if source/version policy permits.
- Medium-confidence -> review queue.
- Low-confidence or conflicting evidence -> block and review.

Thresholds must be configurable and versioned. They should not be hard-coded into curriculum data.

## Failure and recovery

- Retry transient retrieval failures with bounded backoff.
- Preserve failed run metadata.
- Never publish from an incomplete parse.
- Resume from the last durable stage where safe.
- Reprocessing the same fingerprint must be idempotent.
- A failed candidate must not alter the last published authoritative version.

## Supersession rules

When NCISM issues a new curriculum:
- create a new curriculum version;
- set applicability/effective/batch scope;
- link it to its source record;
- mark the prior version superseded only when the source establishes that relationship;
- retain the prior version for historical queries.

Do not overwrite historical curriculum content in place.

## Operational controls

The future implementation should expose:
- source health status;
- last successful check;
- last changed fingerprint;
- pending review count;
- failed ingestion count;
- current published curriculum version;
- reconciliation run history;
- audit/change-event history.

## Phase 1 implementation targets

1. Define reconciliation-run and review-queue entities.
2. Implement source fingerprinting and artifact capture.
3. Implement deterministic curriculum diffing.
4. Implement validation gates and configurable confidence thresholds.
5. Implement transactional version publication.
6. Implement reconciliation audit events.
7. Add monitoring and retry controls.

## Phase 0 exit condition

G0.9 is complete when this design is versioned and linked to the Phase 0 exit criteria. Implementation belongs to Phase 1.
